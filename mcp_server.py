import os
import sys
import django
import asyncio

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'housing_api.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from listings.models import Listing, Region
from django.db.models import Avg, Min, Max, Count
from decimal import Decimal

# Initialise the MCP server
app = Server("housing-api")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lists all available tools that the MCP server exposes.
    """
    return [
        Tool(
            name="get_all_listings",
            description="Returns all UK property rental listings. "
                        "Optionally filter by city, bedrooms, or property type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Filter by city name e.g. Leeds, London"
                    },
                    "bedrooms": {
                        "type": "integer",
                        "description": "Filter by number of bedrooms"
                    },
                    "property_type": {
                        "type": "string",
                        "description": "Filter by property type e.g. flat, house, studio"
                    },
                },
            },
        ),
        Tool(
            name="get_market_summary",
            description="Returns an overall summary of the UK housing market "
                        "including total listings, average rent, and cities covered.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_average_rent_by_city",
            description="Returns the average, minimum, and maximum monthly rent "
                        "for each city in the database.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_affordability_index",
            description="Returns an affordability index per city, calculated as "
                        "average rent as a percentage of the UK median monthly salary.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_all_regions",
            description="Returns all UK regions with ONS salary and rental data.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_region",
            description="Returns details for a specific UK region by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the region e.g. London, Scotland"
                    },
                },
                "required": ["name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handles tool calls from the MCP client.
    """
    if name == "get_all_listings":
        listings = Listing.objects.all()

        city = arguments.get("city")
        if city:
            listings = listings.filter(city__icontains=city)

        bedrooms = arguments.get("bedrooms")
        if bedrooms is not None:
            listings = listings.filter(bedrooms=bedrooms)

        property_type = arguments.get("property_type")
        if property_type:
            listings = listings.filter(property_type__icontains=property_type)

        results = list(listings.values(
            'id', 'title', 'city', 'postcode',
            'property_type', 'bedrooms', 'monthly_rent', 'available'
        ))
        for r in results:
            r['monthly_rent'] = float(r['monthly_rent'])

        return [TextContent(type="text", text=str(results))]

    elif name == "get_market_summary":
        total = Listing.objects.count()
        available = Listing.objects.filter(available=True).count()
        avg_rent = Listing.objects.aggregate(avg=Avg('monthly_rent'))['avg']
        cities = Listing.objects.values('city').distinct().count()

        summary = {
            "total_listings": total,
            "available_listings": available,
            "unavailable_listings": total - available,
            "overall_average_rent": round(float(avg_rent), 2),
            "cities_covered": cities,
        }
        return [TextContent(type="text", text=str(summary))]

    elif name == "get_average_rent_by_city":
        results = list(
            Listing.objects
            .values('city')
            .annotate(
                average_rent=Avg('monthly_rent'),
                total_listings=Count('id'),
                min_rent=Min('monthly_rent'),
                max_rent=Max('monthly_rent'),
            )
            .order_by('city')
        )
        for r in results:
            r['average_rent'] = round(float(r['average_rent']), 2)
            r['min_rent'] = float(r['min_rent'])
            r['max_rent'] = float(r['max_rent'])

        return [TextContent(type="text", text=str(results))]

    elif name == "get_affordability_index":
        UK_MEDIAN_MONTHLY_SALARY = Decimal('2500.00')
        cities = (
            Listing.objects
            .values('city')
            .annotate(average_rent=Avg('monthly_rent'))
            .order_by('city')
        )
        results = []
        for city in cities:
            index = round(
                (city['average_rent'] / UK_MEDIAN_MONTHLY_SALARY) * 100, 2
            )
            results.append({
                'city': city['city'],
                'average_rent': round(float(city['average_rent']), 2),
                'affordability_index': float(index),
                'affordability_rating': (
                    'affordable' if index < 30
                    else 'moderate' if index < 40
                    else 'expensive'
                ),
            })
        return [TextContent(type="text", text=str(results))]

    elif name == "get_all_regions":
        regions = list(Region.objects.values(
            'id', 'name', 'average_annual_salary',
            'median_monthly_rent', 'population', 'country'
        ))
        for r in regions:
            r['average_annual_salary'] = float(r['average_annual_salary'])
            r['median_monthly_rent'] = float(r['median_monthly_rent'])
        return [TextContent(type="text", text=str(regions))]

    elif name == "get_region":
        name_param = arguments.get("name", "")
        try:
            region = Region.objects.get(name__icontains=name_param)
            result = {
                "id": region.id,
                "name": region.name,
                "average_annual_salary": float(region.average_annual_salary),
                "median_monthly_rent": float(region.median_monthly_rent),
                "population": region.population,
                "country": region.country,
            }
            return [TextContent(type="text", text=str(result))]
        except Region.DoesNotExist:
            return [TextContent(
                type="text",
                text=f"Region '{name_param}' not found."
            )]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
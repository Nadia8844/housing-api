# Generative AI Declaration

**Module:** COMP3011 Web Services and Web Data  
**Student:** Nadia  
**Tool Used:** Claude (Anthropic)  

---

## Overview

Claude was used as a development assistant throughout this project. 
It was not used to generate the project idea or make design decisions 
independently — rather, it was used as a resource for understanding 
concepts, exploring alternatives, and accelerating implementation of 
decisions I had already made.

---

## How AI Was Used

### Project Planning and Idea Selection

I decided to build a housing market API based on my own interest in 
the UK rental market and its relevance to students. I used Claude to 
explore which technology stack would best suit the project, and to 
understand the trade-offs between Django and FastAPI. I chose Django 
because it aligns with the module lectures and provides more built-in 
functionality for a project of this scope.

### Understanding Concepts

I used Claude to deepen my understanding of concepts taught in the 
module lectures — particularly REST statelessness (Lecture 3), Django's 
ORM and serialisers (Lectures 6 and 7), and how JWT authentication 
differs from session-based authentication. In each case I asked 
follow-up questions until I understood the concept before proceeding.

### Implementation

Once I understood what I wanted to build, I used Claude to help write 
the code for each component. I reviewed each piece of code, tested it 
in the browser and terminal, and debugged issues as they arose. For 
example, when the affordability endpoint threw a Decimal type error, 
I identified that something was wrong with the numeric types and used 
Claude to understand why Django's DecimalField is incompatible with 
Python floats in arithmetic operations.

### Reviewing and Improving My Work

I used Claude to review my work against the brief at multiple points 
during development — asking it to identify gaps, compare my project 
against the marking criteria, and suggest improvements. I also looked 
at other students' public GitHub repositories to understand what a 
high-scoring submission looks like, and used that comparison to make 
decisions about what to prioritise.

### Documentation and Report Writing

Claude was used to help structure and draft the API documentation and 
technical report. The content reflects my own understanding of the 
project and my own design decisions.

---

## What AI Was NOT Used For

- Selecting the project topic — this was my own decision
- Making architectural decisions without understanding them first
- Submitting code I did not understand or test myself
- Bypassing the learning process — every concept was explained to me 
  before being implemented

---

## Reflection

Using Claude at this level — to understand concepts, explore 
alternatives, and review my own work critically — reflects the 
approach encouraged by the module brief. The brief positions GenAI 
as a tool for "creative thinking and solution exploration" rather than 
a shortcut, and that is how I have tried to use it throughout this 
project.

---

## Conversation Log Samples

Selected screenshots from my Claude conversations are attached as 
an appendix to the technical report. These include exchanges covering:

- Comparing Django vs FastAPI for this use case
- Debugging the Decimal type error in the affordability endpoint
- Reviewing my project against the marking criteria
- Discussing the MCP server and how it works
- Evaluating whether to add additional features based on other repos

---

## Tools Declared

| Tool | Version | Purpose |
|------|---------|---------|
| Claude (Anthropic) | claude.ai | Architecture discussion, implementation assistance, debugging, documentation |
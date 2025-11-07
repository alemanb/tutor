# File Structure

This document describes the organization and purpose of directories in the system. Each folder has a specific role in building a web application that uses artificial intelligence agents.

## Root Level

```
back-end/
├── config/           # Settings and configuration files
├── docs/            # Documentation and guides
├── scripts/         # Automation and deployment scripts
├── src/             # All the main code files
├── main.py          # The file that starts the application
├── pyproject.toml   # Python project settings and dependencies
└── README.md        # Basic project information
```

### What each root folder does:

`config`: Contains files that control how the application behaves in different environments (development, testing, production). Think of these as the application's settings.

`docs`: Stores documentation, guides, and explanations about the project. This helps new developers understand how everything works.

`scripts`: Contains automation scripts for tasks like deploying the application, setting up databases, or running maintenance tasks.

`src`: The heart of the application, contains all the actual code that makes the system work.

## Source Code (`src/`)

This is where all the main application code lives. It's organized into different layers based on what each part does.

### API Layer (`src/api/`)
The web interface that handles requests from users or other applications:

`dependencies`: Contains reusable pieces of code that other parts of the API need. For example, code that connects to the database or checks if a user is logged in. Instead of writing this code over and over, it's written once here and reused.

`endpoints`: These are the actual web addresses (URLs) that users can call to do things. For example, an endpoint might handle requests to create a new user account or get information about an agent. Each file typically handles one type of resource (like users, agents, or tasks).

`middleware`: Code that runs before or after every web request. This handles common tasks like checking permissions, logging what happened, or allowing requests from different websites (CORS). Think of it as a security guard or receptionist that processes everyone before they get to the main application.

### Agents (`src/agents/`)
The artificial intelligence system that contains multiple AI agents working together:

`core`: The fundamental building blocks of all agents. This includes the basic agent class that all other agents inherit from, plus systems for creating new agents and managing their lifecycle (starting, stopping, pausing).

`memory`: Systems that help agents remember things. Short term memory might remember what happened in the current conversation, long term memory stores information across sessions, and shared memory lets different agents share information with each other.

`models`: Defines what different types of agents look like and what they can do. This includes their properties (like name, skills, personality) and the data structures they use to communicate.

`tools`: The actual capabilities that agents can use to do work. This might include tools for searching the web, reading and writing files, calling external APIs, or performing calculations. Each tool gives agents a specific ability.

`workflows`: Patterns and processes for how multiple agents work together. This defines how agents communicate, coordinate on complex tasks, and share work. Think of it as the choreography for the agent dance.

### Core (`src/core/`)
The foundation that everything else builds on:

`config`: Manages all the application settings, environment variables (like database passwords), and configuration that changes between development and production environments.

`logging`: Sets up the system for recording what happens in the application. This includes deciding what to log, how to format log messages, and where to send them (files, databases, monitoring services).

`security`: Contains tools for keeping the application secure. This includes encryption for sensitive data, handling authentication tokens, password security, and other security utilities.

### Database (`src/database/`)
Everything related to storing and retrieving data:

`migrations`: Scripts that modify the database structure over time. When you need to add a new table or change an existing one, you create a migration. This keeps track of all database changes and allows you to apply them consistently across different environments.

`models`: Defines the structure of data in the database. These are like blueprints that describe what a user, agent, or task looks like in the database, including what fields they have and how they relate to each other.

`repositories`: Provides a clean interface for accessing data. Instead of writing database queries throughout the application, you use repository functions that handle the complex database operations. This makes the code cleaner and easier to test.

### Services (`src/services/`)
The business logic layer that implements the main features:

`agent_orchestrator`: The conductor for the multi agent system. This decides which agents should work on which tasks, how they should communicate, and how to coordinate their efforts. It's like a project manager for AI agents.

`auth`: Handles user authentication (proving who you are) and authorization (what you're allowed to do). This includes login, logout, password management, and checking permissions.

`task_manager`: Manages the lifecycle of tasks from creation to completion. This includes queuing tasks, tracking their status, handling failures, and notifying when tasks are done.

### Testing (`src/tests/`)
Code that verifies everything works correctly:

`agents`: Tests specifically for the AI agent system. This validates that agents behave correctly, can use their tools properly, and work well together.

`integration`: Tests that check how different parts of the system work together. These tests might create a user, have an agent perform a task, and verify the results end to end.

`unit`: Tests for individual pieces of code in isolation. Each function or class gets tested to make sure it works correctly on its own.

### Utilities (`src/utils/`)
Helper functions and tools that are used throughout the application but don't belong to any specific layer. This might include date formatting, string manipulation, or common calculations.

## Design Principles

- **Separation of Concerns**: Clear boundaries between web layer, agent system, and data layer
- **Modularity**: Each directory serves a specific purpose with minimal cross-dependencies
- **Scalability**: Structure supports adding new agents, endpoints, and services
- **Testability**: Comprehensive test organization matching source structure
- **Configuration**: Centralized configuration management for different environments
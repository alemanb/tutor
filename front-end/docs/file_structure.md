# File Structure

This document describes the organization and purpose of directories in the React + TypeScript front-end application. Each folder has a specific role in building a modern web application with Vite, TailwindCSS, and TypeScript.

## Root Level

```
front-end/
├── config/           # Build and environment configuration
├── docs/            # Documentation and guides
├── public/          # Static assets and public files
├── scripts/         # Build and deployment scripts
├── src/             # All the main source code
├── package.json     # Project dependencies and scripts
├── tsconfig.json    # TypeScript configuration
├── vite.config.ts   # Vite build tool configuration
└── tailwind.config.js # TailwindCSS styling configuration
```

### What each root folder does:

`config`: Contains build tool configurations, environment settings, and development/production configurations for the Vite build system and other tools.

`docs`: Stores documentation, guides, and explanations about the project. This helps new developers understand how the front-end application works.

`public`: Contains static files that are served directly by the web server. This includes images, icons, manifest files, and other assets that don't need processing.

`scripts`: Contains automation scripts for building, testing, deploying, or maintaining the front-end application.

`src`: The heart of the application, contains all the React components, TypeScript code, styles, and application logic.

## Source Code (`src/`)

This is where all the main application code lives. It's organized into different layers based on what each part does in a React application.

### Components (`src/components/`)
Reusable React components that make up the user interface:

`common`: Basic reusable components that can be used throughout the application like buttons, inputs, modals, and loading indicators. These are the building blocks of the interface.

`layout`: Components that define the overall page structure like headers, footers, navigation bars, sidebars, and page containers. These components control how content is arranged on screen.

`forms`: Form-related components including form wrappers, input fields, validation displays, and form submission handlers. These handle user input and data collection.

`ui`: User interface components that provide interactive functionality like dropdowns, tooltips, tabs, accordions, and other interactive elements that enhance user experience.

### Pages (`src/pages/`)
Top level page components that represent different routes in the application:

`home`: The main landing page component and any related sub-components specific to the homepage experience.

`auth`: Authentication related pages like login, signup, password reset, and user registration flows.

`dashboard`: User dashboard pages that show personalized content, user data, and main application functionality after login.

`profile`: User profile pages for viewing and editing personal information, account settings, and preferences.

### Hooks (`src/hooks/`)
Custom React hooks that encapsulate reusable logic:

`api`: Custom hooks for making API calls, handling server communication, data fetching, and managing server state. These simplify communication with the backend.

`auth`: Authentication related hooks for managing user login state, checking permissions, handling tokens, and user session management.

`ui`: Hooks for managing user interface state like modals, notifications, themes, and other UI-specific functionality that needs to be shared across components.

### Services (`src/services/`)
Business logic and external service integrations:

`api`: Functions and configurations for communicating with backend APIs, handling HTTP requests, response processing, and error management.

`auth`: Authentication service functions for login, logout, token management, user verification, and session handling.

`storage`: Local storage and session storage utilities for persisting data in the browser, caching user preferences, and temporary data storage.

`validation`: Form validation rules, input sanitization, data validation schemas, and error message generation for ensuring data quality.

### Utils (`src/utils/`)
Utility functions and helper code:

`constants`: Application-wide constants like API endpoints, configuration values, default settings, and fixed data that doesn't change.

`helpers`: General purpose utility functions for formatting dates, manipulating strings, mathematical calculations, and other common operations.

`types`: TypeScript type definitions, interfaces, and type utilities that define the shape of data used throughout the application.

### Styles (`src/styles/`)
Styling and design system files:

`globals`: Global CSS styles, CSS reset rules, base typography, and styles that apply to the entire application.

`components`: Component-specific styles, CSS modules, and styling that's tied to particular components when TailwindCSS classes aren't sufficient.

`themes`: Theme definitions, color palettes, design tokens, and styling variables that control the visual appearance of the application.

### Assets (`src/assets/`)
Static resources used by the application:

`images`: Image files like logos, icons, illustrations, and photos used throughout the application.

`fonts`: Custom font files and typography assets for consistent text styling across the application.

`icons`: SVG icons, icon fonts, and graphic elements used for buttons, navigation, and visual communication.

### Context (`src/context/`)
React context providers for global state management:

`auth`: Authentication context that provides user login state, user information, and authentication methods to all components.

`theme`: Theme context for managing dark/light mode, color schemes, and visual preferences across the application.

`app`: General application context for global settings, user preferences, and application-wide state that multiple components need to access.

### Tests (`src/tests/`)
Testing files and utilities:

`components`: Unit tests for individual React components, testing props, rendering, and user interactions.

`hooks`: Tests for custom React hooks, verifying their behavior, state changes, and side effects.

`utils`: Tests for utility functions, ensuring they handle edge cases and produce expected outputs.

`integration`: Integration tests that verify how different parts of the application work together.

## Design Principles

**Component-Based Architecture**: Each UI element is built as a reusable React component with clear boundaries and responsibilities.

**Type Safety**: TypeScript provides compile-time error checking and better developer experience with autocompletion and refactoring support.

**Responsive Design**: TailwindCSS enables mobile-first responsive design that works across all device sizes.

**Performance**: Vite provides fast development builds and optimized production bundles with code splitting and lazy loading.

**Accessibility**: Components follow web accessibility standards to ensure the application is usable by everyone.

**Testing**: Comprehensive test coverage ensures components work correctly and catch regressions early.
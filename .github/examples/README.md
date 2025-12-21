# Walkthrough Configuration Examples

This directory contains example configurations for generating automated application walkthroughs across different technology stacks and frameworks.

## Overview

Each example configuration demonstrates how to set up the walkthrough generator for a specific application type. Use these as templates to create your own custom configurations.

## Available Examples

### 1. React Application
**File**: [`react-app-walkthrough-config.yml`](react-app-walkthrough-config.yml)

**Best for**: Single-page applications, component-based UIs, modern frontend frameworks

**Key features**:
- Start command: `npm start`
- Default port: 3000
- Focus areas: UI components, state management, user interactions
- Ideal duration: 60 seconds

**Use this when**: Building React, Next.js, or similar component-based applications

---

### 2. Python Flask Application
**File**: [`flask-app-walkthrough-config.yml`](flask-app-walkthrough-config.yml)

**Best for**: REST APIs, microservices, backend services

**Key features**:
- Start command: `python app.py`
- Default port: 5000
- Focus areas: API endpoints, request/response flow, database operations
- Ideal duration: 45-60 seconds

**Use this when**: Building Flask, FastAPI, or similar Python web applications

---

### 3. Vue.js Application
**File**: [`vue-app-walkthrough-config.yml`](vue-app-walkthrough-config.yml)

**Best for**: Progressive web apps, interactive dashboards, data-driven UIs

**Key features**:
- Start command: `npm run serve`
- Default port: 8080
- Focus areas: Reactive components, routing, computed properties
- Ideal duration: 60-90 seconds

**Use this when**: Building Vue.js, Nuxt.js, or similar reactive framework applications

---

### 4. Full-Stack Application
**File**: [`fullstack-app-walkthrough-config.yml`](fullstack-app-walkthrough-config.yml)

**Best for**: Complete applications with frontend, backend, and database

**Key features**:
- Multiple services: Node.js backend + React frontend
- Port configuration: Backend (5000), Frontend (3000)
- Focus areas: Complete user journey, API integration, data flow
- Ideal duration: 90-120 seconds

**Use this when**: Demonstrating end-to-end application functionality

---

## How to Use These Examples

### Step 1: Choose the Right Example
Select the example that most closely matches your application architecture:
- **Frontend-only apps**: Use React or Vue.js examples
- **Backend APIs**: Use Flask example
- **Full applications**: Use Full-Stack example

### Step 2: Copy and Customize
1. Copy the example file to your repository root (or `.github/` directory)
2. Rename to match your project: `walkthrough-config.yml`
3. Modify the values to match your application

### Step 3: Test Locally
Before running the automated workflow, test your configuration:

```bash
# Install dependencies
npm install  # or pip install -r requirements.txt

# Run the start command
npm start    # or python app.py

# Verify the app runs on the configured port
```

### Step 4: Run the Workflow
1. Commit your `walkthrough-config.yml` file
2. Go to Actions tab in GitHub
3. Run "Generate Application Walkthrough"
4. The workflow will use your custom configuration

---

## Configuration Options Explained

### Required Fields

#### `app_type`
The technology stack of your application:
- `react` - React, Next.js, Create React App
- `vue` - Vue.js, Nuxt.js
- `angular` - Angular applications
- `flask` - Python Flask applications
- `express` - Node.js/Express applications
- `django` - Django applications
- `fullstack` - Multi-service applications

#### `start_command`
The command to start your application in development mode:
```yaml
start_command: "npm start"           # React/Vue/Angular
start_command: "python app.py"       # Flask
start_command: "npm run dev"         # Next.js/Nuxt.js
start_command: "python manage.py runserver"  # Django
```

#### `port`
The port your application listens on:
```yaml
port: 3000  # React default
port: 5000  # Flask default
port: 8080  # Vue default
port: 4200  # Angular default
```

### Optional Fields

#### `install_command`
Command to install dependencies (defaults to auto-detection):
```yaml
install_command: "npm install"
install_command: "pip install -r requirements.txt"
install_command: "yarn install"
```

#### `build_command`
Command to build the application (if needed):
```yaml
build_command: "npm run build"
build_command: "python setup.py build"
```

#### `environment_variables`
Required environment variables:
```yaml
environment_variables:
  NODE_ENV: development
  API_URL: http://localhost:5000
  DEBUG: true
```

#### `focus_areas`
Specific features or pages to highlight:
```yaml
focus_areas:
  - "User login and authentication"
  - "Dashboard with real-time data"
  - "Settings page"
  - "Data export functionality"
```

#### `duration`
Target video length in seconds (30-120):
```yaml
duration: 60  # One minute walkthrough
```

#### `voiceover_style`
Narration style:
```yaml
voiceover_style: "professional"  # Formal, business-focused
voiceover_style: "casual"        # Friendly, conversational
voiceover_style: "technical"     # Detailed, developer-focused
```

#### `demo_flow`
Step-by-step user journey:
```yaml
demo_flow:
  - "Navigate to homepage"
  - "Click login button"
  - "Enter credentials and submit"
  - "View dashboard"
  - "Interact with data visualization"
  - "Access user settings"
```

---

## Common Modifications

### Modifying for Different Ports
If your app uses a custom port:

```yaml
# Before (default)
port: 3000

# After (custom)
port: 8000
```

### Adding Environment Variables
For apps requiring configuration:

```yaml
environment_variables:
  DATABASE_URL: "sqlite:///dev.db"
  SECRET_KEY: "dev-key-not-for-production"
  API_KEY: "test-api-key"
```

### Customizing Focus Areas
Be specific about what to demonstrate:

```yaml
# Generic (less effective)
focus_areas:
  - "Main features"
  - "User interface"

# Specific (more effective)
focus_areas:
  - "Real-time chat messaging"
  - "File upload with progress bar"
  - "Search with auto-suggestions"
```

### Adjusting Duration
Match duration to complexity:

```yaml
duration: 30   # Quick feature demo
duration: 60   # Standard walkthrough
duration: 90   # Detailed explanation
duration: 120  # Comprehensive tour
```

---

## Multi-Service Applications

For applications with multiple services (frontend + backend + database):

### Option 1: Separate Walkthroughs
Create one walkthrough per service:
- `frontend-walkthrough-config.yml`
- `backend-walkthrough-config.yml`

### Option 2: Integrated Walkthrough
Use the full-stack example and configure all services:

```yaml
app_type: fullstack
services:
  - name: backend
    start_command: "python app.py"
    port: 5000
  - name: frontend
    start_command: "npm start"
    port: 3000
```

---

## Framework-Specific Notes

### React / Next.js
- Use `npm start` or `npm run dev`
- Default port: 3000
- Consider showing component interactivity
- Highlight state management (Redux, Context API)

### Vue.js / Nuxt.js
- Use `npm run serve` or `npm run dev`
- Default port: 8080
- Show reactive data binding
- Demonstrate routing and navigation

### Angular
- Use `ng serve`
- Default port: 4200
- Focus on services and dependency injection
- Show form validation and routing

### Flask / FastAPI
- Use `python app.py` or `uvicorn main:app`
- Default port: 5000 (Flask) or 8000 (FastAPI)
- Demonstrate API endpoints with tools like Postman or curl
- Show request/response cycles

### Express / Node.js
- Use `npm start` or `node server.js`
- Custom port (often 3000, 5000, or 8080)
- Show REST API endpoints
- Demonstrate middleware and routing

### Django
- Use `python manage.py runserver`
- Default port: 8000
- Show admin interface
- Demonstrate ORM queries and views

---

## Troubleshooting Configuration Issues

### Issue: App doesn't start
**Solution**: Verify your start command locally:
```bash
# Test in your terminal
npm start
# or
python app.py
```

### Issue: Wrong port detected
**Solution**: Explicitly set the port in your config:
```yaml
port: 3000  # Your actual port
```

### Issue: Missing dependencies
**Solution**: Add install command:
```yaml
install_command: "npm install && npm run build"
```

### Issue: Environment variables needed
**Solution**: Document required variables:
```yaml
environment_variables:
  DATABASE_URL: "sqlite:///dev.db"
  API_KEY: "your-test-api-key"
```

### Issue: Long startup time
**Solution**: Increase wait time in config:
```yaml
startup_wait: 30  # seconds to wait after starting
```

---

## Best Practices

1. **Test Locally First**: Always verify your start command works before creating a walkthrough
2. **Be Specific**: Use detailed focus areas for better results
3. **Keep It Short**: 60-90 seconds is ideal for most walkthroughs
4. **Document Dependencies**: List all required environment variables and services
5. **Use Descriptive Names**: Name your config file clearly (e.g., `react-dashboard-config.yml`)
6. **Version Control**: Commit your config file to track changes over time

---

## Need Help?

- **Quick Start Guide**: [Get started in 5 minutes](../docs/QUICK_START.md)
- **GitHub Issues**: [Report problems](https://github.com/ivviiviivvi/.github/issues)
- **Discussions**: [Ask questions](https://github.com/ivviiviivvi/.github/discussions)
- **Contact**: [@4444JPP](https://github.com/4444JPP)

---

## Contributing Examples

Have a configuration for a framework not listed here? We welcome contributions!

1. Create your example config file
2. Test it thoroughly
3. Submit a PR with your example
4. Update this README

See [Contributing Guidelines](../../docs/CONTRIBUTING.md) for details.

---

*Last updated: 2025-12-21 | Maintained by @4444JPP*

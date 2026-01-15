# AgentSphere Live Demo Setup

## What is AgentSphere?

AgentSphere is an automatic live demo deployment platform that takes your GitHub
repositories and makes them instantly accessible as live, running applications.
It eliminates the need for manual deployment configuration and provides instant
access to your applications through a web interface.

### Key Features

- 🚀 **Automatic Deployment**: Detects your app type and deploys automatically
- 🔄 **Auto-restart**: Keeps your application running 24/7
- 📊 **Health Monitoring**: Continuous health checks and automatic recovery
- 🔐 **Secure Access**: Configurable access control and authentication
- 📦 **Multi-Stack Support**: Node.js, Python, Java, React, Vue, and more
- 🌐 **Live Demo Badge**: Automatically added to your README

## How Automatic Deployment Works

### Workflow Trigger

The AgentSphere deployment workflow is triggered automatically when:

1. **Push to main branch**: Any code changes pushed to `main` trigger deployment
1. **Manual dispatch**: You can manually trigger deployment from GitHub Actions

### Detection Process

The workflow automatically detects your application type by examining:

- **Node.js**: Presence of `package.json`
  - React: `"react"` dependency
  - Vue: `"vue"` dependency
  - Angular: `"@angular/core"` dependency
  - Express: `"express"` dependency
  - Generic Node.js: Default to `npm start`

- **Python**: Presence of `requirements.txt`, `setup.py`, or `pyproject.toml`
  - Flask: `app.py` file
  - FastAPI: `main.py` with `fastapi`/`uvicorn` in requirements
  - Django: `manage.py` file
  - Generic Python: Default to Python scripts

- **Java**: Presence of `pom.xml` or `build.gradle`
  - Spring Boot with Maven: `mvn spring-boot:run`
  - Spring Boot with Gradle: `gradle bootRun`

- **Static**: `index.html` without other framework indicators

### Deployment Steps

1. **Detect Application Type**: Analyzes repository structure
1. **Load Configuration**: Reads `.github/agentsphere-config.yml`
1. **Create `.agentsphere.yml`**: Generates deployment configuration
1. **Register with API**: Sends configuration to AgentSphere
1. **Update README**: Adds Live Demo badge
1. **Create PR**: Opens a pull request with deployment details

## How to Access Your Live Demo

### From the Live Demo Badge

Once deployed, your README will have a badge that looks like this:

[![Live Demo](https://img.shields.io/badge/Live%20Demo-AgentSphere-blue?style=for-the-badge&logo=google-chrome)](https://agentsphere.dev/example)

Click the badge to access your live demo instantly.

### From the Pull Request

The deployment workflow creates a pull request with:

- Direct link to your live demo
- Application type and configuration details
- Health check status
- Deployment timestamp

### Direct URL Format

Your live demo URL follows this pattern:

```
https://agentsphere.dev/{org-name}/{repo-name}
```

## Custom Startup Configuration

### Using agentsphere-config.yml

Customize deployment by editing `.github/agentsphere-config.yml`:

```yaml
# Enable/disable deployment
enable: true
auto_deploy: true

# Custom startup commands
startup_scripts:
  nodejs: npm run start:prod
  python: gunicorn app:app --bind 0.0.0.0:8000

# Resource limits
resources:
  cpu_limit: 2.0
  memory_limit: 1G
```

### Per-Repository Configuration

Create a `.agentsphere.yml` file in your repository root:

```yaml
name: my-app
type: nodejs
startup_command: npm run start:custom
port: 3000
environment:
  NODE_ENV: production
  API_URL: https://api.example.com
```

### Environment Variables

Set environment variables in the configuration:

```yaml
environment:
  common:
    LOG_LEVEL: info
  nodejs:
    PORT: 3000
    NODE_ENV: production
  python:
    FLASK_ENV: production
    DATABASE_URL: postgresql://...
```

## Sharing Demo Links

### Public Demos

By default, demos are publicly accessible. Share the URL with anyone:

```
https://agentsphere.dev/ivviiviivvi/my-awesome-app
```

### Private Demos

Configure private access in `agentsphere-config.yml`:

```yaml
access_control:
  visibility: private
  require_auth: true
```

Users will need to authenticate with GitHub to access the demo.

### Embedding Demos

Embed your demo in other websites using an iframe:

```html
<iframe
  src="https://agentsphere.dev/ivviiviivvi/my-app"
  width="100%"
  height="600px"
  frameborder="0"
>
</iframe>
```

## Troubleshooting

### App Won't Start

**Problem**: The application fails to start after deployment.

**Solutions**:

1. Check the startup command in `.agentsphere.yml`
1. Verify all dependencies are listed in `package.json` or `requirements.txt`
1. Check application logs in the AgentSphere dashboard
1. Ensure the app listens on `0.0.0.0` (not just `localhost`)

**Example fix for Node.js**:

```javascript
// Instead of:
app.listen(3000, "localhost");

// Use:
app.listen(3000, "0.0.0.0");
```

### Port Conflicts

**Problem**: Application won't bind to the specified port.

**Solutions**:

1. Use environment variable for port:

   ```javascript
   const PORT = process.env.PORT || 3000;
   app.listen(PORT, "0.0.0.0");
   ```

1. Configure correct port in `.agentsphere.yml`:

   ```yaml
   port: 8080
   ```

### Performance Issues

**Problem**: Application is slow or unresponsive.

**Solutions**:

1. Increase resource limits:

   ```yaml
   resources:
     cpu_limit: 2.0
     memory_limit: 1G
   ```

1. Enable caching:

   ```yaml
   advanced:
     cache_dependencies: true
     compression_enabled: true
   ```

1. Optimize your application code

1. Use production builds (not development mode)

### Health Check Failures

**Problem**: AgentSphere reports the app as unhealthy.

**Solutions**:

1. Ensure your app has a health endpoint:

   ```javascript
   app.get("/health", (req, res) => {
     res.status(200).json({ status: "ok" });
   });
   ```

1. Configure health check endpoint:

   ```yaml
   monitoring:
     health_check_endpoint: /api/health
     health_check_timeout: 30
   ```

### Deployment Timeout

**Problem**: Deployment times out before completing.

**Solutions**:

1. Increase deployment timeout:

   ```yaml
   deployment:
     timeout: 300 # 5 minutes
   ```

1. Optimize build process:
   - Use lighter dependencies
   - Pre-build assets
   - Enable dependency caching

## Examples for Different Tech Stacks

### React Application

**Detected Configuration**:

```yaml
name: react-app
type: react
startup_command: npm start
port: 3000
environment:
  NODE_ENV: production
```

**Custom Configuration** (using production build):

```yaml
name: react-app
type: react
startup_command: npx serve -s build -p 3000
port: 3000
```

### Flask Application

**Detected Configuration**:

```yaml
name: flask-app
type: flask
startup_command: python app.py
port: 5000
environment:
  FLASK_ENV: production
```

**Custom Configuration** (using Gunicorn):

```yaml
name: flask-app
type: flask
startup_command: gunicorn app:app --bind 0.0.0.0:5000 --workers 4
port: 5000
```

### Express.js API

**Detected Configuration**:

```yaml
name: express-api
type: nodejs
startup_command: npm start
port: 3000
```

**Custom Configuration**:

```yaml
name: express-api
type: nodejs
startup_command: node server.js
port: 3000
environment:
  NODE_ENV: production
  API_KEY: ${API_KEY}
```

### Django Application

**Detected Configuration**:

```yaml
name: django-app
type: django
startup_command: python manage.py runserver 0.0.0.0:8000
port: 8000
```

**Custom Configuration** (using Gunicorn):

```yaml
name: django-app
type: django
startup_command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
port: 8000
```

### Static Website

**Detected Configuration**:

```yaml
name: static-site
type: static
startup_command: none
port: 80
```

Static sites are served directly without a startup command.

## Advanced Features

### Custom Domains

Map custom domains to your demo:

```yaml
advanced:
  custom_domains:
    - demo.myapp.com
    - app.example.com
```

### SSL/TLS Configuration

Enable HTTPS (enabled by default):

```yaml
advanced:
  ssl_enabled: true
  http2_enabled: true
```

### Rate Limiting

Protect your demo from abuse:

```yaml
access_control:
  rate_limit: 100 # requests per minute per IP
```

### Deployment Strategies

Choose how updates are deployed:

```yaml
deployment:
  strategy: rolling # rolling, blue_green, or canary
  rollback_on_failure: true
```

## Getting Help

- **GitHub Issues**: Report problems in the repository
- **Documentation**: Check the main README for updates
- **Workflow Logs**: View detailed logs in GitHub Actions
- **Community**: Ask questions in GitHub Discussions

## Related Documentation

- [GitHub Pages Setup Guide](GITHUB_PAGES_SETUP.md)
- [Live Deployment Guide](LIVE_DEPLOYMENT_GUIDE.md)
- [Organization Workflows](../.github/workflows/)

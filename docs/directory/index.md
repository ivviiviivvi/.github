---
layout: default
title: Application Directory
---

# Application Directory

Browse all applications in the Ivviiviivvi organization.

<div class="directory-list" style="margin-top: 2rem;">
  {% if site.data.walkthroughs %}
    {% for app in site.data.walkthroughs.walkthroughs %}
      <div style="background: var(--surface); border: 1px solid var(--border-color); border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem;">
        <h3 style="margin-bottom: 0.5rem;">{{ app.name }}</h3>
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">{{ app.description }}</p>
        
        {% if app.tech_stack and app.tech_stack != "" %}
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem;">
          {% assign tech_items = app.tech_stack | split: ", " %}
          {% for tech in tech_items %}
            <span class="badge">{{ tech }}</span>
          {% endfor %}
        </div>
        {% endif %}
        
        <div style="display: flex; gap: 1rem;">
          {% if app.has_video %}
            <a href="/tutorials/#{{ app.name | slugify }}" class="btn btn-secondary">📹 Tutorial</a>
          {% endif %}
          <a href="{{ app.repo_url }}" class="btn btn-secondary" target="_blank">📦 Source</a>
          
          {% if site.data.app-deployments %}
            {% for deployment in site.data.app-deployments.apps %}
              {% if deployment.app_name == app.name and deployment.live_url %}
                <a href="{{ deployment.live_url }}" class="btn" target="_blank">🚀 Live Demo</a>
              {% endif %}
            {% endfor %}
          {% endif %}
        </div>
      </div>
    {% endfor %}
  {% else %}
    <p style="text-align: center; color: var(--text-secondary); padding: 3rem;">No applications available yet.</p>
  {% endif %}
</div>

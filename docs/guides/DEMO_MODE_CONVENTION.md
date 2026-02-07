# DEMO_MODE Convention

How org repos opt into the demo sandbox system. When `DEMO_MODE=true` is set as
an environment variable, the application switches to a sandbox-safe mode with
synthetic data, stubbed external services, and simplified auth.

## Environment Variables

| Variable | Purpose |
|---|---|
| `DEMO_MODE=true` | Master flag — activates all sandbox behaviors |
| `DEMO_BANNER=true` | Show a persistent "Demo Environment" banner in the UI |
| `DEMO_AUTH_BYPASS=true` | Use pre-seeded demo credentials instead of real auth |

All three are injected automatically by the
[demo-sandbox reusable workflow](../../.github/workflows/reusable/demo-sandbox.yml).

## Core Contract

1. **No mock data files in the repo.** Demo data is generated at runtime using
   factories / faker / seed scripts gated behind `DEMO_MODE`.
2. **External APIs stub locally.** HTTP calls to third-party services return
   canned responses when `DEMO_MODE` is set.
3. **Auth is simplified.** A hardcoded demo user is available
   (`demo@example.com` / `demo1234`) — never connect to production identity
   providers.
4. **Database seeds on startup.** The app runs its seeder automatically (or via
   the `demo-data-seed-command` workflow input) the first time it starts in
   demo mode.
5. **Banner is visible.** A non-dismissable banner warns users that data resets
   periodically.

## Implementation Examples

### React / Next.js

```tsx
// lib/demo.ts
export const isDemoMode = process.env.NEXT_PUBLIC_DEMO_MODE === 'true';

// components/DemoBanner.tsx
export function DemoBanner() {
  if (!isDemoMode) return null;
  return (
    <div className="demo-banner">
      Demo Environment — data resets periodically
    </div>
  );
}

// lib/api.ts — stub external calls
export async function fetchWeather(city: string) {
  if (isDemoMode) {
    return { temp: 72, condition: 'sunny', city };
  }
  return fetch(`https://api.weather.example/${city}`).then(r => r.json());
}

// pages/api/auth/[...nextauth].ts — demo user bypass
if (process.env.DEMO_AUTH_BYPASS === 'true') {
  providers.push(
    CredentialsProvider({
      name: 'Demo',
      credentials: {},
      authorize: async () => ({
        id: 'demo', name: 'Demo User', email: 'demo@example.com'
      }),
    })
  );
}
```

### FastAPI

```python
# core/config.py
import os

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# main.py — seed on startup
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if DEMO_MODE:
        from seeds.demo import seed_demo_data
        await seed_demo_data()
    yield

app = FastAPI(lifespan=lifespan)

# middleware/demo_banner.py
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import DEMO_MODE

class DemoBannerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if DEMO_MODE:
            response.headers["X-Demo-Mode"] = "true"
        return response

# services/payment.py — stub external API
from core.config import DEMO_MODE

async def charge_card(amount: float, token: str):  # allow-secret
    if DEMO_MODE:
        return {"status": "success", "charge_id": "demo_ch_123"}
    return await stripe_client.charges.create(amount=amount, source=token)
```

### Express

```js
// config/demo.js
const DEMO_MODE = process.env.DEMO_MODE === 'true';
module.exports = { DEMO_MODE };

// middleware/demoBanner.js
const { DEMO_MODE } = require('../config/demo');
module.exports = (req, res, next) => {
  if (DEMO_MODE) res.set('X-Demo-Mode', 'true');
  next();
};

// routes/auth.js — demo bypass
const { DEMO_MODE } = require('../config/demo');
if (DEMO_MODE) {
  router.post('/login', (req, res) => {
    res.json({ token: 'demo-jwt-token', user: { name: 'Demo User' } }); // allow-secret
  });
}
```

## Adoption Checklist

For a repo maintainer adding demo sandbox support:

- [ ] Read `DEMO_MODE` env var in app config
- [ ] Add runtime data seeding behind `DEMO_MODE` check
- [ ] Stub all external API calls when `DEMO_MODE` is true
- [ ] Add demo auth bypass when `DEMO_AUTH_BYPASS` is true
- [ ] Add demo banner component when `DEMO_BANNER` is true
- [ ] Copy
      [demo-deployment.yml](../../.github/workflows/demo-deployment.yml) to
      your repo's `.github/workflows/`
- [ ] Push to `main` — the workflow auto-detects, deploys, and opens a badge PR
- [ ] Merge the badge PR to show "Try Demo" in your README

## Hosting Provider Selection

The reusable workflow auto-selects a provider based on app type:

| App Type | Default Provider | Alternatives |
|---|---|---|
| `frontend` / `static` | Cloudflare Pages | Vercel |
| `backend` | Render | — |
| `fullstack` | Render | — |
| `cli-library` / unknown | Codespaces deep link | — |

Override via the `hosting-provider` input in the wrapper workflow.

## Required Org Secrets

| Secret | Provider | Purpose |
|---|---|---|
| `VERCEL_TOKEN` | Vercel | Deploy frontend apps |
| `VERCEL_ORG_ID` | Vercel | Team/org scope |
| `RENDER_API_KEY` | Render | Deploy backend/fullstack apps |
| `CLOUDFLARE_API_TOKEN` | Cloudflare | Deploy static sites |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare | Account scope |
| `REGISTRY_PAT` | GitHub | Write to `.github` repo registry |

## Data Lifecycle

Sandbox environments on free tiers (Render, Cloudflare) may spin down after
inactivity. The app should re-seed demo data on each cold start, not just on
first deploy.

## Demo Settings Panel (Optional)

For apps that expose multiple demo-mode behaviors, consider adding a
`/demo/settings` admin page so reviewers can toggle individual stubs on or off,
view seed status, or trigger a re-seed without restarting the sandbox.

### React Example

```tsx
// pages/demo/settings.tsx
import { useState, useEffect } from 'react';

interface DemoSettings {
  stubPayments: boolean;
  stubEmail: boolean;
  stubAuth: boolean;
  seedStatus: 'seeded' | 'pending' | 'error';
}

export default function DemoSettingsPanel() {
  const [settings, setSettings] = useState<DemoSettings | null>(null);

  useEffect(() => {
    fetch('/api/demo/settings').then(r => r.json()).then(setSettings);
  }, []);

  if (!settings) return <p>Loading...</p>;

  const toggle = (key: keyof DemoSettings) =>
    fetch('/api/demo/settings', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ [key]: !settings[key] }),
    })
      .then(r => r.json())
      .then(setSettings);

  const reseed = () =>
    fetch('/api/demo/seed', { method: 'POST' })
      .then(r => r.json())
      .then(() => location.reload());

  return (
    <div style={{ maxWidth: 480, margin: '2rem auto' }}>
      <h2>Demo Settings</h2>
      <label>
        <input type="checkbox" checked={settings.stubPayments}
          onChange={() => toggle('stubPayments')} />
        Stub payment provider
      </label>
      <label>
        <input type="checkbox" checked={settings.stubEmail}
          onChange={() => toggle('stubEmail')} />
        Stub email delivery
      </label>
      <label>
        <input type="checkbox" checked={settings.stubAuth}
          onChange={() => toggle('stubAuth')} />
        Bypass auth (demo user)
      </label>
      <hr />
      <p>Seed status: <strong>{settings.seedStatus}</strong></p>
      <button onClick={reseed}>Re-seed demo data</button>
    </div>
  );
}
```

This panel is only rendered when `DEMO_MODE=true` and should be excluded from
production builds via tree-shaking or a build-time env check.

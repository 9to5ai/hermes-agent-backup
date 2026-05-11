# xurl — Current Setup State (May 2026)

## Auth Status (This Machine)

```
▸ default  [(no credentials)]
      oauth2: (none)
      oauth1: –
      bearer: –
```

xurl is installed at `/opt/homebrew/bin/xurl` (Homebrew) but has no credentials configured. This machine cannot read X posts via `xurl read` or monitor Graeme's posts automatically.

## Required Setup Steps (User Must Run Outside Agent)

1. Create app at https://developer.x.com/en/portal/dashboard
   - Set redirect URI: `http://localhost:8080/callback`
   - App type: "Web app, automated app or bot" (NOT "Native App")

2. Register + authenticate:
```bash
xurl auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
xurl auth oauth2 --app my-app YOUR_USERNAME   # opens browser OAuth
xurl auth default my-app
```

3. Verify:
```bash
xurl auth status
xurl whoami
```

## After Auth Is Set Up

Graeme monitoring workflow (to implement once xurl is auth'd):
```bash
# Monitor gkisokay's posts
xurl user gkisokay                    # get user info
xurl search "from:gkisokay" -n 5      # recent posts
xurl read 2053449921554960545         # main guide post
xurl read 2040044476060864598         # Dreamer guide
xurl read 2051275483996909982         # Research guide

# Set up monitoring via cron
hermes cron create "0 */2 * * *" "xurl search \"from:gkisokay\" -n 3" --name "Graeme posts monitor"
```

## Key Post IDs (Graeme)

- Main guide: `2053449921554960545` — "How to Build a Hermes Agent That Finds Important Work and Builds It Autonomously"
- Dreamer: `2040044476060864598` — "I Gave My Hermes + OpenClaw Agents a Subconscious, and Now It Dreams 24/7"
- Research: `2051275483996909982` — "I run 6 AI agents. Only this one makes the other 5 smarter"

## Notes

- X API is paid — $0 balance means `CreditsDepleted` errors. Buy credits at developer.x.com → Billing.
- Graeme's public buildroom not publicly available (github.com/gkisokay has 0 public repos) — X monitoring is the main value until he publishes it.
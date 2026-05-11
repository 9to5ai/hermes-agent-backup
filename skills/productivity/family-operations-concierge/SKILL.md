---
name: family-operations-concierge
description: "Use when operating a family concierge / household operations assistant: maintain family preferences, propose Sydney family activities, shortlist suppliers, monitor essentials/deals, prepare weekly command briefs, and require approval before purchases or external messages."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [family-ops, concierge, household, sydney, reminders, deals, approvals]
    related_skills: [scheduled-digest-automation, maps, google-workspace]
---

# Family Operations Concierge

## Overview

This umbrella skill covers household/family operations workflows: anticipating needs, researching options, shortlisting recommendations, asking for approval, preparing execution checklists, reminding, verifying, and learning preferences over time.

The original Momo-specific operating notes live in `references/momo-familyops-concierge.md`. Use those details when acting for Jun/Momo's household; use this class-level workflow for any family operations concierge task.

## When to Use

- User asks for a weekend family activity, itinerary, outing shortlist, or wet-weather backup.
- User asks for household admin planning, supplier shortlists, deal radars, inventory reminders, or family briefs.
- A task concerns family logistics where safety, approval, and privacy matter.

Do not use for general web research with no family/household decision to support.

## Operating Loop

1. **Anticipate** — identify likely needs from calendar, season, child age, inventory, or prior preferences.
2. **Research** — gather current options, prices, distances, opening hours, weather, and constraints.
3. **Shortlist** — provide 2-4 realistic options, not a data dump.
4. **Recommend** — name the best pick and why.
5. **Seek approval** — do not book, buy, message, or commit without explicit approval.
6. **Execute prep** — packing list, route, booking links, cancellation policy, deadline.
7. **Remind** — provide timely nudges if requested/scheduled.
8. **Verify** — check current availability/opening hours/prices before action.
9. **Learn** — update durable preferences only when stable and useful.

## Decision Language

Use clear labels:

- **Best pick** — strongest overall recommendation.
- **Easy win** — low effort / low risk.
- **Worth booking** — good but requires booking or deadline.
- **Monitor** — not actionable yet.
- **Skip** — not worth it, explain briefly.
- **Needs human verification** — uncertainty remains.
- **Approval required** — paid/external/commitment action.

## Safety and Approval Rules

- Never purchase, book, or send external messages without explicit approval.
- Never recommend childcare without verifying licence, WWCC/credentials, insurance, and current availability.
- For paid actions, surface provider, item/service, price, deadline, cancellation/refund policy, and risk.
- Keep family data private and avoid exposing child/family details unnecessarily.
- Escalate uncertainty instead of over-confident recommendations.

## Weekly Brief Templates

### Weekend Family Brief

- Best pick + why
- Timing around naps/meals
- Travel/parking/public transport
- Weather backup
- Packing list
- Booking/payment needs
- Approval checklist

### Sunday Family Command Brief

- Top 3 priorities
- Calendar/logistics risks
- Household admin due soon
- Groceries/inventory/deals
- Decisions needed from parents

## Verification Checklist

- [ ] Family-specific preferences/reference notes checked when relevant.
- [ ] Current hours/prices/availability verified.
- [ ] Safety risks and weather/logistics considered.
- [ ] Recommendation is concise and ranked.
- [ ] Any paid or external action is gated behind explicit approval.

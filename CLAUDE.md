# sports-calendar-v3

Static single-page sports calendar (`index.html` + `favicon.jpg`), auto-deployed to Vercel from this repo's `main` branch.

## Never add a client-side login/password gate

A full-page password modal (`<input type="password">` styled as a login screen) was briefly live on this
site in mid-2026 (added in `0e041f0`, removed in `a3a979e`). That pattern — a full-screen prompt demanding
a password before showing content — is exactly what Google Safe Browsing's automated classifiers flag as
"social engineering," and it's the most likely reason the deployment got marked as a dangerous site even
though nothing malicious was actually happening.

**Do not build a custom JS password/login overlay for this site again**, even temporarily. If access
control is ever needed, use Vercel's built-in deployment protection (Project Settings → Deployment
Protection) instead — it password-gates the whole deployment at the edge and never renders a login-styled
page to crawlers or visitors.

## Safe Browsing monitor

`.github/workflows/safe-browsing-check.yml` + `scripts/check-safe-browsing.mjs` check the live deployment
URL daily against the Google Safe Browsing API and open a GitHub issue if it's ever flagged again. Keep
`SITE_URL` in the workflow file in sync whenever the Vercel project (and therefore its `.vercel.app` URL)
is renamed.

## Data rules (set by Dan, Oct 2026)

- **Athletics is paused until May 2027.** Autumn/winter is almost all marathons, which Dan doesn't want.
  Don't add any athletics event dated before 2027-05-01 (the page also hides them via `ATHLETICS_RESUME`).
  From May 2027, cover Diamond League meets and major championships, not road races.
- **No Premier League.** It was removed on purpose; don't add it back.
- **NFL and NBA come live from ESPN** (`site.api.espn.com`): fixtures, final scores and standings. The
  `CURATED.nfl` / `CURATED.nba` arrays are only a fallback if ESPN is down.
- **Scores for curated sports:** after an event has happened, add `result: "..."` to its entry
  (e.g. `result: "Canelo won by unanimous decision"`) and keep it for 7 days so it shows under
  "Recent results" and on the calendar. Past events stay visible on the calendar back to the start of last month.
- The International sub-tabs (Cricket / Football / Rugby / All Sports) only show when the International tab is selected.
- The page reads ESPN through its own `/api/espn` (Vercel function `api/espn.js`; locally `python scripts/serve.py` on http://localhost:8795/), because some browsers/blockers stopped direct ESPN calls. ESPN rejects user agents containing a URL, so keep the plain `sports-calendar/1.0`.

// Vercel serverless function: /api/espn?path=apis/v2/sports/basketball/nba/standings
// Fetches ESPN's public JSON server-side so the page never calls ESPN from the browser
// (ad/privacy blockers and ESPN's bot filter were stopping those calls).
// Only ESPN sports API paths are allowed, so this can't be used as an open proxy.
const ALLOWED = /^apis\/(site\/)?v2\/sports\/(football\/nfl|basketball\/nba)\/(scoreboard|standings)(\?[\w=&.-]*)?$/;

module.exports = async (req, res) => {
  const path = String(req.query.path || "");
  if (!ALLOWED.test(path)) {
    res.status(400).json({ error: "path not allowed" });
    return;
  }
  try {
    const upstream = await fetch(`https://site.api.espn.com/${path}`, {
      headers: {
        "User-Agent": "sports-calendar/1.0",
        Accept: "application/json",
      },
    });
    const body = await upstream.text();
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    // Cache at Vercel's edge for a minute so live scores stay fresh without hammering ESPN.
    res.setHeader("Cache-Control", "public, s-maxage=60, stale-while-revalidate=300");
    res.status(upstream.status).send(body);
  } catch (err) {
    res.status(502).json({ error: "ESPN unreachable" });
  }
};

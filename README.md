# blee.eat

Tap **feed**, the sheep eats grass. Tap the sheep, it bleats.

`site/` is the whole website (index.html, preview.png, apple-touch-icon.png), already built. See CLAUDE.md for how it fits together and how to rebuild with `python3 build.py`.

## Auto-deploy (Cloudflare Workers)
`wrangler.jsonc` tells Cloudflare to serve the prebuilt `site/` folder (only that folder, so the source photos and scripts stay private).

In Cloudflare: **Workers & Pages → Create → Import a repository** → pick this repo, then:
- Project/Worker name: `bleeat` (must match `name` in `wrangler.jsonc`)
- Build command: *(leave empty)*
- Deploy command: `npx wrangler deploy` (the default)
- Root directory: `/` (the default; the repo root, where `wrangler.jsonc` lives)

Then add `blee.eat` under the Worker's **Settings → Domains & Routes → Custom domain**. Every push to `main` deploys automatically.

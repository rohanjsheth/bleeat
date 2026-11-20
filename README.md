# blee.eat

Tap **feed**, the sheep eats grass. Tap the sheep, it bleats.

`site/` is the whole website (index.html, preview.png, apple-touch-icon.png), already built. See CLAUDE.md for how it fits together and how to rebuild with `python3 build.py`.

## Auto-deploy (Cloudflare Pages)
Connect this repo in Cloudflare: **Workers & Pages → Create → Pages → Connect to Git**.
- Production branch: `main`
- Framework preset: None
- Build command: *(leave empty)*
- Build output directory: `site`

Then add the custom domain `blee.eat` under the project's **Custom domains**. Every push to `main` deploys automatically.

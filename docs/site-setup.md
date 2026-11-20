# Publishing the lab site at lab.toontheology.com

The site is the static page in `site/`, with the images copied in from
`renders/` at build time. It runs as a **Cloudflare Worker with static
assets**, configured by `wrangler.jsonc` in the repository root, on the free
tier. Feedback goes through this repository's GitHub Issues, so there are no
accounts or forms to run yourself.

## One-time setup (in your Cloudflare dashboard)

1. **Workers & Pages → Create → Import a repository**, and choose
   `MalcolmGohSG/AssitistiveRobot`. The Worker name must be `assistiverobot`,
   to match `wrangler.jsonc`.
2. Build settings: leave the **build command empty**, and keep the deploy
   command as `npx wrangler deploy`. `wrangler.jsonc` already copies the
   renders and points at `site/`.
3. Deploy. You get a `….workers.dev` address. Check that it looks right.
4. In the Worker, go to **Settings → Domains & Routes → Add → Custom domain**
   and enter `lab.toontheology.com`. toontheology.com is already on
   Cloudflare, so it adds the DNS record and certificate for you.

Every merge to `main` then updates the site, and each pull request gets a
build check.

To test locally: `npx wrangler deploy --dry-run` runs the same build without
publishing anything.

## Feedback

GitHub Issues must be switched on: repository **Settings → General →
Features → Issues**. The "Leave a suggestion" button on the site opens a new
issue. People need a free GitHub account to post, which also keeps spam down.

If the repository is **private**, visitors can't open issues and the links to
documents won't work. Make it public before you share the site.

# Publishing the lab site at lab.toontheology.com

The site is the static page in `site/`, with the images copied in from
`renders/` at build time. It costs nothing on Cloudflare's free tier.
Feedback goes through this repository's GitHub Issues, so there are no
accounts or forms to run yourself.

## One-time setup (in your Cloudflare dashboard)

1. **Workers & Pages → Create → Pages → Connect to Git.** Choose
   `MalcolmGohSG/AssitistiveRobot`. You may need to give the Cloudflare
   GitHub app access to this repository.
2. Build settings:
   - Production branch: `main`
   - Framework preset: *None*
   - Build command: `cp -r renders site/`
   - Build output directory: `site`
3. **Save and Deploy.** You get a `*.pages.dev` address. Check it looks right.
4. In the new Pages project: **Custom domains → Set up a custom domain** →
   `lab.toontheology.com`. Because toontheology.com is already on Cloudflare,
   it adds the DNS record and certificate for you.

After that, every merge to `main` updates the site. Each pull request also
gets its own preview address.

## Feedback

GitHub Issues must be switched on: repository **Settings → General →
Features → Issues**. The "Leave a suggestion" button on the site opens a
new issue. People need a free GitHub account to post, which also keeps spam
down.

If the repository is **private**, visitors can't open issues and the links to
documents won't work. Make it public before you share the site.

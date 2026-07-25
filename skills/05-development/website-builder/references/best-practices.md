## Best Practices

1. **Prefer static over dynamic.** Every dynamic feature (SSR, serverless functions, real-time) adds cost, complexity, and failure modes. Question every requirement for dynamic behavior: "Can this be static?" A contact form can be a serverless function; it doesn't require a full SSR framework.

2. **Ship zero JavaScript by default.** Astro's "islands architecture" means JS is opt-in per component. A blog post, landing page, or documentation page ships 0KB of JS. When JS is needed (interactive search, carousel, modal), load it only for that component. The performance baseline should be "no JS required."

3. **Cache aggressively, invalidate surgically.** Hashed assets (`main.a1b2c3d4.js`) are immutable — cache forever. HTML pages change — cache for 0 seconds but serve stale while revalidating (`stale-while-revalidate`). Never cache forever without hash-based cache busting.

4. **Monitor Core Web Vitals in production, not just in Lighthouse.** Lighthouse is a lab test (simulated device, consistent conditions). Real users are on slow networks with low-end devices. Use the `web-vitals` library to collect real-user metrics (RUM) and report them to your analytics. A lab score of 95 can be a real-user score of 60.

5. **Use a CDN even for small sites.** CDNs (Cloudflare, Fastly, BunnyCDN) serve content from edge locations near the user — reducing latency from 200ms (US server → Europe visitor) to 20ms (Europe edge → Europe visitor). Cloudflare's free plan includes CDN, DDoS protection, and SSL. There is zero reason to not use a CDN.

6. **Automate image optimization at build time.** Never manually resize images for the web. Every SSG framework has built-in image processing: `@astrojs/image`, `next/image`, Hugo image processing, 11ty Image plugin. These generate responsive `srcset` attributes, convert to WebP/AVIF, and set dimensions automatically. Manual image work is wasted time and inevitably inconsistent.

7. **Version control everything except secrets.** Code, content (markdown), configuration, and design tokens go in git. Secrets (API keys, database URLs, tokens) go in environment variables. `.env` is in `.gitignore`. `.env.example` documents required variables without containing real values. A new developer should be able to clone the repo, read `.env.example`, and be fully operational in 10 minutes.

8. **Test on real devices, not just DevTools responsive mode.** Chrome DevTools emulation is for layout testing, not performance or tactile testing. Test on a low-end Android phone (Moto G series, $150-200) for performance. Test on an iPhone SE for Safari-specific bugs. Borrow devices if you don't own them. The bugs you find are the bugs your users experience.

9. **Set up CI/CD before writing features.** A deploy pipeline that builds, lints, audits accessibility, and deploys on every push to main means you can ship features continuously. Without CI/CD, each deploy is a manual, error-prone process that accumulates risk. Set up GitHub Actions (or equivalent) in Phase 2 — before any real features are built.

10. **Plan for content updates from day one.** "How does the content get updated?" is as important as "what stack should I use?" If the answer is "the original developer edits the code," the site becomes stale 6 months after they move on. Choose a CMS strategy (markdown + git, headless CMS, low-code platform) that matches the content editor's technical capability — not the developer's.

## Error Recovery — Explicit Step-by-Step

### Build Fails with "Out of Memory"

**Symptoms:** Build process crashes with `JavaScript heap out of memory`, `FATAL ERROR: Ineffective mark-compacts`, or the build hangs indefinitely.

**Step-by-step recovery:**
1. **Increase Node memory limit:** `NODE_OPTIONS="--max-old-space-size=4096" npm run build` (default is 512MB-2GB depending on Node version).
2. **Check for circular imports:** Circular dependencies cause bundlers to loop. Run `npx madge --circular src/` to detect circular imports. Break circles with dependency injection, event emitters, or lazy imports.
3. **Reduce parallel builds:** Astro/Next.js/Vite parallelize page builds. If each page loads a heavy library (e.g., a markdown parser that loads 20MB of grammars), 16 parallel builds = 320MB memory spike. Limit concurrency: Astro (`--concurrency 4`), Next.js (set `experimental.cpus: 4` in config), Hugo (single-threaded by default).
4. **Profile the build:** `node --inspect-brk node_modules/.bin/astro build` → open Chrome DevTools → Memory tab → take heap snapshot. Identify the largest memory consumers.
5. **Split the build:** For large sites (10K+ pages), split into multiple builds by section (blog vs docs vs marketing) and combine output directories.

### Deploy Succeeds but Site Shows Blank Page

**Symptoms:** Deployment completes successfully, but the site at the production URL shows a completely white/blank page.

**Step-by-step recovery:**
1. **Check browser console (F12 → Console):** JS errors are the most common cause. Look for `Uncaught TypeError`, `Cannot read properties of undefined`, `Failed to load module`. If you see `404` for a JS/CSS file, the asset path is wrong.
2. **Check the page source (View Source, not DevTools Elements):** If the HTML is empty (`<body></body>`), the build didn't generate content. Check the build output directory — is `index.html` populated?
3. **Verify asset paths are relative, not absolute:** Absolute paths (`/assets/main.js`) resolve from the root domain. If your site is deployed to `https://user.github.io/repo/`, `/assets/main.js` resolves to `https://user.github.io/assets/main.js` (wrong). Use relative paths (`./assets/main.js`) or a `<base href="/repo/">` tag.
4. **Check for CORS errors on CDN assets:** If CSS/JS is served from a different domain (e.g., `cdn.example.com`), check the response headers for `Access-Control-Allow-Origin`.
5. **Disable service worker:** If you ship a service worker, clear it (DevTools → Application → Service Workers → Unregister) and hard reload. A broken service worker caching an empty response delivers a white page forever.

### Core Web Vitals Fail LCP Threshold

**Symptoms:** Lighthouse/PageSpeed Insights reports LCP > 4s (red). The largest content element takes too long to render.

**Step-by-step recovery:**
1. **Identify the LCP element:** Lighthouse report → "Largest Contentful Paint element" (typically hero image, hero heading, or hero background video). This is the bottleneck.
2. **If LCP is an image:** Preload it — `<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">`. Convert to WebP/AVIF. Serve at display size (1x or 2x viewport — never full resolution). Use responsive `srcset` to avoid serving a 2000px image to a 375px phone.
3. **If LCP is text (heading):** Ensure the font is self-hosted and preloaded: `<link rel="preload" as="font" href="/fonts/inter.woff2" crossorigin>`. Set `font-display: swap` to show fallback text immediately. Subset fonts to only used characters (Latin subset typically 20-30KB vs 200KB full font).
4. **Inline critical CSS:** Above-the-fold styles go in a `<style>` tag in `<head>`. Eliminates the render-blocking CSS round-trip.
5. **Defer non-critical JS:** All `<script>` tags below the fold get `type="module"` (auto-deferred) or `defer`. Analytics, chat widgets, and social embeds load after the `load` event.
6. **Check server response time (TTFB):** If TTFB > 600ms, the issue is server-side. Use CDN edge caching, upgrade hosting, or move to SSG (pre-built HTML — TTFB < 50ms).

### SSL Certificate Not Issuing

**Symptoms:** Site shows "Your connection is not private" / `NET::ERR_CERT_AUTHORITY_INVALID`. Let's Encrypt fails to issue a certificate.

**Step-by-step recovery:**
1. **Verify DNS records:** `dig A example.com` + `dig AAAA example.com` must return the host's IP addresses. `dig CNAME www.example.com` must point to the host. DNS must be fully propagated (up to 48 hours, but typically < 30 minutes).
2. **Check CAA record:** `dig CAA example.com` — if a CAA record exists, it must include `letsencrypt.org`. Example: `example.com. CAA 0 issue "letsencrypt.org"`. If CAA only authorizes another CA, Let's Encrypt cannot issue.
3. **Verify the domain is pointed to the correct host:** If you changed hosting providers, the domain might still point to the old host's IPs. Cert issuance happens on the current host — old DNS records prevent completion.
4. **Try DNS validation instead of HTTP:** Most platforms allow switching validation method. DNS validation (`_acme-challenge` TXT record) is more reliable — no dependency on HTTP server being reachable.
5. **Wait and retry:** Let's Encrypt rate limits: 5 duplicate certificates per domain per week. If you've tried and failed multiple times, wait 1 hour and retry. Most platforms auto-retry on a backoff schedule.

### "Deploy Successful" but Site Shows Old Version

**Symptoms:** CI/CD reports success, but the live site still shows yesterday's content/design.

**Step-by-step recovery:**
1. **Clear CDN cache:** Cloudflare → Caching → Purge Everything. Vercel → Redeploy without cache. Netlify → Deploys → Clear cache and deploy site.
2. **Check cache headers:** If `Cache-Control: max-age=86400` (24 hours) is set on HTML, browsers cache the old version for a full day. Change to `max-age=0, must-revalidate` or `stale-while-revalidate` for HTML pages.
3. **Hard reload:** `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows) forces the browser to re-download all assets. This bypasses browser cache but not CDN cache.
4. **Check for service worker caching:** A service worker with `cache-first` strategy will serve the old version forever. Unregister the SW (DevTools → Application → Service Workers), hard reload, and fix the SW strategy to `network-first` for HTML.
5. **Verify the correct build deployed:** Some platforms deploy the latest build, not necessarily the branch you pushed. Check the deployment log for the commit SHA — does it match your latest push? If you pushed to `main` but the platform deploys from `production` branch, the deploy is stale.

### Form Submissions Not Delivering

**Symptoms:** Users submit forms, but emails/captures never arrive. No errors visible to the user.

**Step-by-step recovery:**
1. **Test the form endpoint directly:** `curl -X POST https://example.com/api/contact -d "name=Test&email=test@example.com&message=test"`. Check the HTTP response. 200 with a success message? The form handler works. 500/403/404? Check server logs.
2. **Check spam filtering:** Form submissions from @example.com or @test.com might be caught by spam filters. Test with a real email address. Add `Reply-To` header matching the submitter's email to avoid DMARC rejection (your server sending "from" the user's email domain without authorization = spam).
3. **Netlify Forms:** Verify `data-netlify="true"` attribute on the form, `netlify` attribute on `<form>`, and that the form is in the deployed HTML (not injected by JS after page load). Netlify's build bot parses static HTML forms at deploy time.
4. **Serverless function:** Check function logs (Vercel → Functions, Netlify → Functions, Cloudflare Workers → Logs). Common issues: missing environment variables, exceeded timeout (10s default on Vercel/Netlify), exceeded memory (default 1024MB).
5. **Email deliverability:** If using a transactional email service (Resend, SendGrid, Postmark), check their dashboard for bounces, spam reports, or rate limiting. Verify SPF, DKIM, and DMARC records for your sending domain.

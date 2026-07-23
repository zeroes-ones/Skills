# When NOT to Use This Skill (Overkill)

- **Pre-launch MVP with <100 users**: Profiling, load testing, caching layers, CDN optimization for a product nobody uses yet is waste. Add an index if a page takes >3 seconds. Move on.
- **Internal tool used by 5 people**: P95 latency optimization for a dashboard used by your team of 5 is not worth engineering time. If a page takes 5 seconds, they can wait 5 seconds.
- **Your performance is fine (all endpoints P95 <200ms, LCP <2s)**: Don't optimize for optimization's sake. Set baselines. Monitor. Only act when metrics degrade.
- **You can scale vertically (bigger server solves the problem)**: Before building a Redis cluster and read replicas, try upgrading to the next EC2 instance size. It costs $50 more per month and takes 5 minutes. Do that first.
- **The slow thing is used by 3 customers who haven't complained**: Fix problems that affect many users or critical paths. A slow admin report used monthly is not a priority.

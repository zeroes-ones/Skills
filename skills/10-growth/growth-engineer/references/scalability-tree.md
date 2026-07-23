# Scalability Decision Tree

```
Are you running >1 experiment per week?
├── YES → Is experiment analysis taking >2 hours per experiment?
│   ├── YES → Invest in automated analysis (GrowthBook/Statsig). Pre-register experiments.
│   └── NO → Manual analysis is fine. Ship velocity is good.
└── NO → Don't build an experimentation platform. Run a few high-quality experiments.

Does your activation rate need improvement (e.g., <30% of signups reach aha moment)?
├── YES → This is your #1 growth priority. Run onboarding experiments before acquisition experiments.
│   Focus on time-to-value. Every 10% improvement in activation compounds across retention.
└── NO → Activation is healthy. Move to retention or monetization experiments.

Is your experiment win rate <10%?
├── YES → Your hypotheses are too weak. Invest in user research + data analysis before ideating.
│   (Industry average is 10-30% win rate. Below 10% = you're guessing.)
└── NO → Win rate is healthy. Increase experiment velocity.

Do experiments take >2 weeks from hypothesis to results?
├── YES → Bottleneck: engineering time, analysis time, or review process. Identify and fix the slowest step.
└── NO → Speed is good. Focus on experiment quality (effect size, learning value).

Have you shipped a "losing" experiment in the last quarter?
├── NO → You're optimizing for wins, not learning. Run 1 experiment you expect to lose but will teach something fundamental.
└── YES → Good. Learning culture is healthy.
```


**What good looks like:** Event taxonomy documented and implemented across all platforms. A/B test framework is self-serve for PMs. Growth dashboard shows activation, retention, referral, and revenue metrics updated in real-time. Experiment velocity is 2+ concurrent experiments.

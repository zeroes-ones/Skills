# Best Practices

<!-- DEEP: 10+min -->
<!-- STANDARD: 3min — rules extracted from production experience -->

- **Write strategy, not just architecture.** A system architect designs a system. A staff engineer
  designs the *technical direction* for multiple systems. Your documents should answer "Where are we
  going technically and why?" not just "How does this service work?"
- **Run design reviews that decide, not discuss.** Start every design review by stating: "By the end
  of this meeting, we will decide X." If you can't state the decision, you're not ready for the
  review. Send pre-reads 48 hours in advance. If someone hasn't read them, reschedule — don't waste
  everyone's time catching them up.
- **Mentor seniors, not juniors.** Your highest-leverage mentorship is with senior engineers who
  mentor others. Teach them to think at the system level, write RFCs, and navigate ambiguity. One
  hour with a senior engineer who mentors five juniors multiplies your impact 5x.
- **Navigate ambiguity by writing the first bad draft.** When the problem is unclear, don't wait for
  clarity. Write a 1-page document that's probably wrong. Circulate it with "This is a strawman —
  tear it apart." People are far better at critiquing concrete proposals than generating them from
  scratch. Your bad draft creates the conversation that produces the good answer.
- **Say no gracefully.** "That's a valuable problem, and I think [tech lead name] would do a great
  job leading it. I'm focused on [your initiative] this quarter because [business impact]. Happy to
  review their proposal." You're not saying the problem doesn't matter — you're saying it needs a
  different owner.
- **Manage time across teams with office hours.** Hold two 1-hour open office hours per week where
  any engineer can book a 15-min slot. This creates a predictable channel for questions without
  constant interruptions. Everything else goes through async channels (Slack, RFC comments).
- **Measure impact without direct reports.** Track: (a) number of engineers unblocked by your work,
  (b) decisions made through your RFCs/ADRs, (c) teams that adopted patterns you introduced, (d)
  senior engineers you mentored who were promoted. If you can't quantify your impact, you can't
  justify the staff role.
- **Build technical brand inside and outside.** Give one internal tech talk per quarter. Write one
  external blog post or conference proposal per half. Review PRs in open-source projects your
  company depends on. Your brand creates trust — when you propose something bold, people listen
  because they know your work.

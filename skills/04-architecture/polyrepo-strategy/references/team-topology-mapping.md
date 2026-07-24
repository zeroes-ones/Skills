# Team Topology Mapping (Conway Alignment)

Framework for assessing whether your repo topology aligns with your team communication topology. Misalignment creates friction; alignment enables flow.

## Conway's Law

"Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." — Melvin Conway, 1968

In practice: if two teams communicate daily, their code should live close together (same repo or tightly coordinated repos). If they communicate quarterly, their code can live far apart.

## Assessment Process

1. **Map team topology:** List all teams, their members, their communication frequency with other teams.
2. **Map repo topology:** List all repos, their owning team, dependencies on other repos.
3. **Identify misalignments:**
   - High-communication teams in separate repos -> coordination friction.
   - Low-communication teams in same repo -> unnecessary coupling.
   - Orphan repos with no clear team ownership -> operational risk.

## Alignment Patterns

- **Stream-aligned team:** Owns a business capability end-to-end. Should own 2-5 repos.
- **Platform team:** Builds shared infrastructure. Their repos are consumed by stream-aligned teams.
- **Enabling team:** Helps other teams adopt tools. Typically own fewer repos (templates, docs) or none.

## Red Flags

- Multiple stream-aligned teams owning the same repo.
- One team owning >7 repos (fragmentation).
- Repos without CODEOWNERS.
- "Shared ownership" without clear primary owner (nobody feels responsible).

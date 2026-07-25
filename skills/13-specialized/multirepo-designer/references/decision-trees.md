## 1. Monorepo vs Multirepo Decision

```
                         +---------------------------------+
                         | START: Do teams ship            |
                         | independently? (different       |
                         | release cadences, no shared     |
                         | deploy windows)                 |
                         +---------------+-----------------+
                                         |
                          +--------------v--------------+
                          | YES -> Independent releases.|
                          | Multirepo is the default.   |
                          | Teams should own their repos.|
                          | Check coupling next.        |
                          +--------------+--------------+
                                         |
                          +--------------v--------------+
                          | How often do these teams    |
                          | ship changes together?      |
                          | (>30% cross-repo PRs?)      |
                          +------+---------------+------+
                                 |               |
                          +------v------+ +------v------+
                          | <15% cross- | | >15% cross- |
                          | repo PRs -> | | repo PRs -> |
                          | Pure multi- | | Hybrid --   |
                          | repo. Each  | | group repos |
                          | repo fully  | | that ship   |
                          | autonomous. | | together    |
                          | No shared   | | into a mono-|
                          | release     | | repo cluster|
                          | train.      | | (Nx/Turbo). |
                          +-------------+ +------+------+
                                                 |
                                  +--------------v--------------+
                                  | Do repos need different     |
                                  | security classification?    |
                                  | (PCI, HIPAA, SOX, internal) |
                                  +------+---------------+------+
                                         |YES            |NO
                                  +------v------+ +------v------+
                                  | Separate    | | Can share   |
                                  | repos       | | monorepo    |
                                  | mandatory.  | | cluster.    |
                                  | Different   | | Same        |
                                  | access      | | security    |
                                  | controls    | | posture     |
                                  | per level.  | | allows co-  |
                                  +-------------+ | location.   |
                                                   +-------------+
```
**Multirepo wins when:** Teams ship independently, cross-repo PRs <15%, security boundaries differ, tech stacks diverge, or you have >50 engineers across >5 autonomous teams.
**Monorepo wins when:** Teams ship together weekly, cross-repo PRs >30%, single tech stack, shared security posture, <50 engineers.

#

## 2. Split Granularity Decision

```
                    +--------------------------------+
                    | START: What is the primary      |
                    | organizing principle for        |
                    | splitting?                      |
                    +---------------+----------------+
                                    |
          +-------------------------+-------------------------+
          |                         |                         |
+---------v---------+   +-----------v----------+   +---------v---------+
| By Domain          |   | By Team              |   | By Deployable     |
| (bounded context)  |   | (Conway alignment)   |   | Unit              |
+---------+----------+   +-----------+----------+   +---------+----------+
          |                          |                         |
+---------v----------+   +-----------v----------+   +---------v----------+
| Pro: Clear domain  |   | Pro: Matches org     |   | Pro: Maps 1:1 to   |
| boundaries. Good   |   | chart. Team owns     |   | deployment. Each    |
| for DDD shops.     |   | repo. Simple         |   | service has its own |
|                    |   | accountability.      |   | repo. Independent   |
| Con: Teams may     |   |                      |   | scaling.            |
| span domains ->    |   | Con: Team            |   |                     |
| cross-repo PRs.    |   | reorganizations      |   | Con: Shared code    |
|                    |   | break repo topology. |   | between services    |
|                    |   |                      |   | creates dependency  |
|                    |   |                      |   | webs.               |
+--------------------+   +----------------------+   +---------------------+

          +-------------------------+-------------------------+
          |                         |                         |
+---------v---------+   +-----------v----------+   +---------v---------+
| By Language/Stack  |   | By Release Cadence   |   | Hybrid (combine   |
| (polyglot orgs)    |   | (fast vs slow lanes) |   | 2+ principles)    |
+---------+----------+   +-----------+----------+   +---------+----------+
          |                          |                         |
+---------v----------+   +-----------v----------+   +---------v----------+
| Pro: Language-      |   | Pro: Fast-moving     |   | Pro: Flexible.      |
| native tooling.     |   | services not blocked |   | Use domain for     |
| Simple CI per       |   | by slow-moving ones. |   | core boundaries,   |
| language.           |   |                      |   | deployable unit    |
|                     |   | Con: Coupled         |   | for services.      |
| Con: Cross-language |   | domains may end up   |   |                     |
| code sharing is     |   | in different repos   |   | Con: Complexity.   |
| painful. SDKs per   |   | with mismatched      |   | Need to document   |
| language -> N repos.|   | cadences.            |   | the rationale for  |
+---------------------+   +----------------------+   | every boundary.    |
                                                     +--------------------+
```
**Rule of thumb:** One repo per deployable unit owned by exactly one team. Shared libraries are separate repos. Cross-cutting concerns (CI templates, lint config, shared types) live in a `platform-tooling` or `shared-config` repo.

#

## 3. Shared Library Strategy

```
                         +-----------------------------+
                         | START: How many repos will   |
                         | consume this shared code?    |
                         +-------------+---------------+
                                       |
                    +------------------+------------------+
                    |                  |                  |
              +-----v-----+      +-----v-----+      +-----v-----+
              | 1 consumer |      | 2-5       |      | 6+        |
              |            |      | consumers  |      | consumers |
              +-----+------+      +-----+------+      +-----+------+
                    |                  |                    |
              +-----v-----+      +-----v-----+      +-----v------+
              | Keep code |      | Extract   |      | Extract to |
              | in the    |      | to shared |      | shared     |
              | consuming |      | library   |      | library    |
              | repo. No  |      | repo with |      | repo with  |
              | extraction|      | internal  |      | published  |
              | overhead. |      | registry  |      | packages.  |
              +-----------+      | (npm,     |      | Strict API |
                                 | PyPI,     |      | via exports|
                                 | crates.io)|      | field.     |
                                 +-----+------+      +-----+------+
                                       |                    |
                                 +-----v-------------+ +---v----------+
                                 | Versioning:       | | Versioning:  |
                                 | Independent semver| | Independent  |
                                 | or lockstep with  | | semver.      |
                                 | consumers.        | | Never lock-  |
                                 |                   | | step --      |
                                 | Use Changesets for| | different    |
                                 | changelog +       | | consumers    |
                                 | version bumps.    | | have different|
                                 +-------------------+ | cadences.    |
                                                       +--------------+

                    +------------------+------------------+
                    |                  |                  |
              +-----v----------+ +-----v----------+ +-----v----------+
              | Breaking change | | Git Submodules?| | Vendoring?     |
              | frequency?     | |                 | |                |
              +-----+----------+ +-----+----------+ +-----+----------+
                    |                  |                    |
          +---------v---------+ +------v------+   +--------v-------+
          | >2 breaking       | | ONLY if you |   | ONLY if the    |
          | changes/year? ->  | | need exact  |   | code changes   |
          | Package API is    | | commit      |   | <1x/year AND   |
          | unstable. Don't   | | pinning AND |   | you cannot use |
          | share yet.        | | can afford  |   | a registry.    |
          | Stabilize first.  | | the DX pain.|   | Prefer registry|
          |                    | | Otherwise ->|   | over vendoring.|
          | <2 breaking       | | internal    |   |                 |
          | changes/year? ->  | | registry.   |   |                 |
          | Share with        | +-------------+   +----------------+
          | semver +          |
          | migration guides. |
          +-------------------+
```
**Internal Registry is the default for >=3 consumers.** Use npm private registry (Verdaccio, GitHub Packages, Artifactory), PyPI private index (DevPI, Artifactory), or language-native private registries. **Never** use git submodules for actively developed code — the DX cost exceeds the version-pinning benefit.

#

## 4. Cross-Repo CI/CD Orchestration

```
                    +----------------------------------+
                    | START: Does Repo A's change      |
                    | affect Repos B, C, D?            |
                    +---------------+------------------+
                                    |
                         +----------v----------+
                         | YES -> What kind of  |
                         | dependency?         |
                         +----------+----------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
    +---------v---------+ +---------v---------+ +---------v---------+
    | Library dependency | | API contract       | | Schema/data       |
    | (Repo B imports    | | (Repo B calls     | | dependency        |
    |  @org/shared-lib)  | |  Repo A's API)   | | (Repo B reads     |
    +---------+----------+ +---------+----------+ |  Repo A's DB)    |
              |                     |              +---------+----------+
    +---------v----------+ +---------v----------+ +---------v----------+
    | CI Trigger:        | | CI Trigger:        | | CI Trigger:        |
    | Repo A publishes ->| | Contract test in   | | Schema compatibility|
    | webhook -> Renovate| | Repo B's CI runs  | | check in Repo B's  |
    | opens PR in Repo B | | against Repo A's  | | CI. Repo A runs    |
    | with version bump. | | staging. Alert if | | migration test     |
    | Repo B's CI runs  | | contract broken.  | | against Repo B's  |
    | full test suite    | |                    | | read patterns.     |
    | with new version.  | | Use: Pact,        | |                     |
    |                     | | OpenAPI diff,     | | Use: schema         |
    | Use: Renovate +    | | gRPC reflection.  | | compatibility       |
    | grouped PRs.       | |                    | | checks, migration   |
    +---------------------+ +--------------------+ | dry-run.            |
                                                   +---------------------+

              +---------------------+---------------------+
              |                     |                     |
    +---------v---------+ +---------v---------+ +---------v---------+
    | Shared config      | | No dependency     | | Unknown            |
    | (ESLint, TS config,| | (independent      | | dependency?        |
    |  CI templates)     | | services)         | |                    |
    +---------+----------+ +---------+----------+ +---------+----------+
              |                     |                       |
    +---------v----------+ +---------v----------+ +---------v----------+
    | CI Trigger:        | | No cross-repo CI   | |Build a dependency  |
    | Broadcast via      | | needed. Each repo  | | graph first. Use:  |
    | repository_dispatch| | tests independently| | nx graph across    |
    | to all consumer    | | in isolation.      | | repos, or manual   |
    | repos. Consumer CI | |                    | | dependency mapping |
    | validates with     | | Verify: consumer   | | with ADR.          |
    | updated config.    | | e2e tests still    | |                    |
    |                     | | pass against pinned| |                    |
    | Use: repo-to-repo  | | contract.          | |                    |
    | dispatch, shared   | +--------------------+ +--------------------+
    | workflow templates.|
    +--------------------+
```
**Golden rule for cross-repo CI:** Never let a downstream repo discover breakage from its own CI alone. The upstream repo MUST trigger downstream CI and get the results BEFORE merging. Otherwise, the upstream team merges, goes home, and the downstream team discovers the breakage the next morning.

#

## 5. Breaking Change Rollout Across Repos

```
                     +----------------------------------+
                     | START: You need to make a         |
                     | breaking change in a shared       |
                     | library consumed by N repos.      |
                     +---------------+------------------+
                                     |
                      +--------------v--------------+
                      | Can you do it non-breaking?  |
                      | (add new API, keep old)      |
                      +------+---------------+-------+
                             |YES            |NO
                      +------v------+ +------v----------+
                      | Do that     | | True breaking    |
                      | instead.    | | change required. |
                      | Ship new API| | Proceed with     |
                      | as minor,   | | migration plan.  |
                      | deprecate   | +------+-----------+
                      | old later.  |        |
                      +-------------+ +------v-------------------+
                                     | Step 1: ANNOUNCE         |
                                     | Publish deprecation      |
                                     | notice. Minimum 4-week   |
                                     | window before removal.   |
                                     | Add runtime warnings     |
                                     | in old API.              |
                                     +------+-------------------+
                                            |
                                     +------v-------------------+
                                     | Step 2: AUTOMATE        |
                                     | Write migration script   |
                                     | (codemod, upgrade tool). |
                                     | Test it against all N    |
                                     | consumer repos in CI.    |
                                     +------+-------------------+
                                            |
                                     +------v-------------------+
                                     | Step 3: OPEN PRs        |
                                     | Automatically open PRs   |
                                     | in all N consumer repos  |
                                     | with migration applied.  |
                                     | Track adoption dashboard.|
                                     | N > 20? Batch into      |
                                     | groups of 5 repos/day.   |
                                     +------+-------------------+
                                            |
                              +-------------+-------------+
                              |             |             |
                      +-------v------+ +-----v-----+ +---v--------+
                      | All consumers| | Some      | | No         |
                      | migrated? -> | | consumers | | consumers  |
                      | Ship removal | | migrated? | | migrated   |
                      | in next major| | Extend    | | after      |
                      | version.     | | deadline. | | deadline?  |
                      | Victory.     | | Escalate  | | Escalate   |
                      +--------------+ | to team   | | to eng     |
                                       | leads.    | | leadership.|
                                       | Never ship| | Create     |
                                       | removal   | | exception  |
                                       | while     | | plan.      |
                                       | consumers | +------------+
                                       | exist.    |
                                       +-----------+
```
**The 5-Phase Breaking Change Playbook:** (1) **Add** — ship new API alongside old as non-breaking minor release, (2) **Deprecate** — mark old API with @deprecated + migration guide in docs + runtime warnings, (3) **Automate** — build codemod/upgrade script tested against all consumers, (4) **Migrate** — open automated PRs to all consumer repos, track adoption, (5) **Remove** — remove old API only after 100% consumer adoption + 1 release buffer.

#

## 6. Ownership Model & REPO Discoverability

```
                    +-----------------------------------+
                    | START: How many repos in your     |
                    | organization?                     |
                    +---------------+-------------------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
        +-----v-----+         +-----v-----+         +-----v-----+
        | <10 repos  |         | 10-50     |         | 50+ repos |
        |            |         | repos     |         |           |
        +-----+------+         +-----+------+         +-----+------+
              |                      |                      |
        +-----v------+         +-----v------+         +-----v------+
        | Simple      |         | Team-based  |         | Automated  |
        | CODEOWNERS  |         | CODEOWNERS  |         | catalog:   |
        | per repo.   |         | with shared |         | Backstage,  |
        | Manual      |         | ownership   |         | Compass, or |
        | discovery   |         | guidelines. |         | custom      |
        | via README  |         | Repo catalog|         | developer   |
        | is fine.    |         | (GitHub     |         | portal.     |
        |             |         | topics or   |         | Every repo  |
        |             |         | Backstage). |         | has:        |
        |             |         |             |         | description,|
        |             |         |             |         | team owner, |
        |             |         |             |         | status,     |
        |             |         |             |         | language,   |
        +-------------+         +------+------+         | tags.       |
                                       |                +------+------+
                                +------v------+                |
                                | Ownership   |         +------v------+
                                | model?      |         | Discovery  |
                                +---+-----+---+         | mechanism? |
                                    |     |             +---+-----+---+
                    +---------------+     +--------+        |     |
                    |                              |        |     |
              +-----v-----+                +-------v---+ +--v---+ +--v---+
              | Single-team|                | Shared    | |Search| |Portal|
              | ownership  |                | ownership | |index | |(Back-|
              +-----+------+                +------+----+ |by    | |stage,|
                    |                              |       |topic | |Com-  |
              +-----v------+               +-------v---+   |or    | |pass) |
              | One team   |               | Multiple  |   |tag   | +------+
              | = one repo |               | teams in  |   +------+
              | with 2+    |               | CODEOWNERS|
              | CODEOWNERS.|               | for cross-|
              | Clear      |               | cutting   |
              | escalation.|               | repos.    |
              |            |               | Rotation  |
              |            |               | duty or   |
              |            |               | on-call   |
              |            |               | for PR    |
              |            |               | reviews.  |
              +------------+               +-----------+
```
**Every repo must have:** (1) CODEOWNERS with >=2 individuals (no single point of failure), (2) a repo description explaining what it does and who owns it, (3) GitHub topics/tags for discoverability, (4) a status badge (active/maintenance/deprecated/experimental). At 50+ repos, invest in a developer portal (Backstage, Compass) for automated cataloging.

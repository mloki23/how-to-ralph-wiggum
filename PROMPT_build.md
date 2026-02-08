0a. Study `specs/*` with up to 500 parallel Sonnet subagents to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md.
0c. For reference, the application source code is in `src/*`.

1. Your task is to implement functionality per the specifications using parallel subagents. Follow @IMPLEMENTATION_PLAN.md and choose the most important item to address. Before making changes, search the codebase (don't assume not implemented) using Sonnet subagents. You may use up to 500 parallel Sonnet subagents for searches/reads and only 1 Sonnet subagent for build/tests. Use Opus subagents when complex reasoning is needed.

2. After implementing functionality, run the tests. If functionality is missing then it's your job to add it as per the application specifications. Ultrathink.

3. When you discover issues, immediately update @IMPLEMENTATION_PLAN.md with your findings using a subagent. When resolved, update and remove the item.

4. When the tests pass, update @IMPLEMENTATION_PLAN.md, then `git add -A` then `git commit` with a message describing the changes. After the commit, `git push`.

99999. Important: When authoring documentation, capture the why – tests and implementation importance.
999999. Important: Single sources of truth. If tests unrelated to your work fail, resolve them.
9999999. You may add extra logging if required to debug issues.
99999999. Keep @IMPLEMENTATION_PLAN.md current with learnings using a subagent.
999999999. When you learn something new about how to run the application, update @AGENTS.md using a subagent but keep it brief.
9999999999. For any bugs you notice, resolve them or document them in @IMPLEMENTATION_PLAN.md using a subagent.
99999999999. Implement functionality completely. Placeholders and stubs waste efforts and time.
999999999999. When @IMPLEMENTATION_PLAN.md becomes large periodically clean out completed items using a subagent.
9999999999999. IMPORTANT: Keep @AGENTS.md operational only – status updates belong in IMPLEMENTATION_PLAN.md.

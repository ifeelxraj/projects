# Daily contributor run

## Start from the checkout, not a quota

```sh
python3 tools/run_brief.py
start=$(git rev-parse HEAD)
branch=$(git branch --show-current)
```

The brief reads the index, current branch and working tree, recent commits,
yesterday's UTC history, and the latest relevant handoffs. It does not fetch,
write files, or make commits. History may be incomplete in a shallow checkout.
Keep the starting revision for this run's count. If there is an unfinished
change, understand it before editing; never discard someone else's work.

## Work one project at a time

- Finish the active project first. When it is complete, give the next project
  its own `projects/<name>/` directory and a README with setup and usage.
- Register it in the root table: local project link in the `Project` column,
  current state in the `Status` column. Run `python3 tools/check_index.py`.
- Aim for 40 substantive increments per day, not 40 edits to a counter. A
  feature, a boundary-case test, or a verified example can stand on its own.
  Make each small change runnable, review its diff, and use a descriptive
  `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, or `chore:` subject.
- Before each commit, run the affected project's checks and exercise the
  behavior. Each project supports `make -C projects/<name> test`. From the root,
  `make test` runs every project, the index checker, contributor-tool tests, and
  the export-to-slots integration tests. Stage specific paths and inspect
  `git diff --cached --check` and the staged diff. Keep credentials, personal
  data, caches and binaries out of Git.
- Use actual work times. Do not backdate, rewrite, force-push, or generate a
  batch of cosmetic changes to meet the target.

## Stop or hand off

On a failed check, Git error, auth problem or rate limit, **stop**. Append the
reason, what was verified, the actual count (even zero) and a recovery step to
`logs/YYYY-MM-DD.md` using the UTC date. Leave the work intact; don't work around
the failure or create filler commits.

At a successful handoff, run `make verify` (tests, UBSan and executable demos),
update project status, and append
a run section to the same daily file. Record what shipped, tests, and a specific
next step. Use `git rev-list --count "$start..HEAD"` rather than counting other
people's commits from the calendar. State whether the handoff commit is included
and verify the final count after committing it. Push only the assigned branch
(`git push origin "$branch"`), without rewriting history.

The GitHub workflow checks pushes and pull requests; it has read-only
permissions and never generates commits. A contributor or an external agent
runner must start each new daily session. Nothing in this repository schedules
unattended changes or stores credentials for one.

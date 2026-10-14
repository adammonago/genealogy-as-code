# Private Dogfooding Checklist

Use this checklist before committing or using this repository as your own private genealogy agent toolkit.

This is intentionally lighter than `RELEASE_CHECKLIST.md`. The goal is "safe and useful for my own work," not "ready for public release."

## Repo Hygiene

- [ ] `git status -sb` shows only the changes you intend to keep
- [ ] No private family data has been copied into tracked example, prompt, or template files
- [ ] No secrets, tokens, or local absolute paths are present in tracked files
- [ ] Generated build artifacts are ignored unless you deliberately want them tracked

## Workflow Sanity

- [ ] The routes you expect to use most are present in `skills/genealogy-autoresearch/ROUTING_TABLE.md`
- [ ] `python scripts/check-routes-sync.py` passes
- [ ] README and workflow counts still match the actual repository contents
- [ ] New workflows include a clear "when to use this" section

## Private-Use Readiness

- [ ] Planning guidance matches how you actually work
- [ ] Country- or branch-specific search rules you rely on are captured in `archives/` or `reference/`
- [ ] Prompts produce usable handoff packets when research hits login, archive, or browse-only walls
- [ ] Identity-collision cases have a workflow that preserves uncertainty instead of over-merging
- [ ] Verify metrics run against your vault for routes you use most (`verify-metric.py`)
- [ ] Validator pass runs clean after tree or question updates (`run-validator.py`)
- [ ] Agent runs append structured manifests to `Research_Log.md` (`append-agent-run.py` or post-run hooks)
- [ ] Post-run hooks finalize pending manifests (`write-pending-agent-run.py`, `finalize-agent-run.py`)
- [ ] Agent run manifests list and validate cleanly (`list-agent-runs.py`, `validate-agent-run-manifests.py`)

## Suggested Commands

```bash
git status -sb
python scripts/check-routes-sync.py
python scripts/verify-metric.py --route-key prompt:08-open-question-resolution --vault-path "$VAULT_PATH"
python scripts/run-validator.py --vault-path "$VAULT_PATH" --prior-route-key prompt:01-tree-expansion --write-report
python3 scripts/append-agent-run.py --vault-path "$VAULT_PATH" --route-key prompt:01-tree-expansion --hat-at-close research_executor --recommended-next-route workflow:validator-pass --metric-name named_individuals_in_family_tree --metric-before 2 --metric-after 2 --metric-delta 0 --dry-run
python3 scripts/write-pending-agent-run.py --vault-path vault-template --route-key prompt:01-tree-expansion --hat-at-close research_executor --recommended-next-route workflow:validator-pass
python3 scripts/finalize-agent-run.py --dry-run
python3 scripts/list-agent-runs.py --vault-path "$VAULT_PATH"
python3 scripts/validate-agent-run-manifests.py --vault-path vault-template
./run-route --route-key workflow:validator-pass --vault-path "$VAULT_PATH" --print-only
```

Replace `$VAULT_PATH` with your local genealogy vault (from `.env.local`).

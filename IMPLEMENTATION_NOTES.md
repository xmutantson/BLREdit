# Offline registry implementation — 2026-10-02

## Verified history and scope

- Fresh isolated checkout of `xmutantson/BLREdit`, remote master
  `9a63d0c918bcbb08051325d86cf90aae02a3c49d`.
- Fetched `HALOMAXX/BLREdit` master
  `529347dfdaa1df65a7ca523232db14e920a23c68`; fork comparison
  was 0 ahead / 190 behind.
- PR #137 was already merged upstream on 2024-04-15 as
  `dbc487108fec7ddb7c607c772c1f2620228232a7`, containing the original user commit
  `dac69a2aa63ece85ab1d148cd0283398654f81e0`.
- Fast-forwarded the isolated branch through that merge. This reuses the original
  change: `xmutantson 0` now explicitly sets both Port and InfoPort to 7778.
  The former master still omitted Port, which defaults to 7777 in BLRServer.cs.
- Added a standalone registry validator and focused standard-library tests. No
  application runtime or server discovery behavior changed. Historical remote
  branches were preserved.

## Validation

From the repository root, with Python 3.11.7:

```
python tools/validate_server_registry.py
python -m unittest discover -s tests -v
git diff --check
```

Results: all 21 registry entries validate; 13 tests pass; diff whitespace check
passes. Cases cover missing/default ports, port boundaries and wrong types,
duplicate properties/IDs/endpoints, field typos, invalid shapes, literal host
strings, immutability, and the retained 7778 fix.

## Deferred and skipped

The remaining 188 upstream commits contain a broad application evolution. They
were not included in this narrow registry fix without application compatibility
validation. Upstream server additions/removals are not treated as evidence of
current availability; no application servers or DNS were queried.

No WPF build, application launch, game launch, live server check, or paid CI was
run. This change modifies registry data and offline Python tooling only. A fresh
Windows clone reports two existing texture names differing only by case:
`t_OvermatchDeltaI6_Female_128x128.png` and
`t_OvermatchDeltai6_Female_128x128.png`; neither asset was modified. Tests do not
instantiate BLRServer, whose static constructor starts ping workers.

Registry checks are an explicit local command; no GitHub workflow was added.
This branch has not been pushed or published.

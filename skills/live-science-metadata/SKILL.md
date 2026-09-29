# Live Science Metadata Skill

Use this skill when One-Wave work needs CERN, GWOSC/LIGO, or another approved public scientific metadata source.

1. Reference One-Wave-Science canon and evidence-pipeline contract first.
2. State the exact repository question the metadata serves.
3. Query metadata before bulk data.
4. Use Jetson/Hive Pipe as the live metadata worker when that route is available.
5. Start with a bounded HTTPS endpoint/sample.
6. Preserve provenance: provider, experiment/detector, record/event/catalog/version identifiers, endpoint, release/version, retrieval time, units/calibration/quality fields, and content hash where applicable.
7. Keep raw provider data separate from derived One-Wave transforms.
8. Validate the response against the question; do not treat retrieval as scientific support by itself.
9. Record a receipt and update repo references only with non-secret, reproducible information.
10. A workflow launch is not success; require the Jetson response and exit code.

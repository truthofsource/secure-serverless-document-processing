# Actual malware-result policy

The policy and its six tests are extracted from the implemented scan processor. Imports are portable, and the product-specific type name is neutral. No cloud credentials or employee documents are included.

```bash
npm run test:source
```

Only the exact clean result maps to clean. Malicious remains distinct; not-scanned, errors and future unknown values deny the action when the result is unclear. This code interprets a trusted provider result; it does not detect malware or authenticate an event by itself.

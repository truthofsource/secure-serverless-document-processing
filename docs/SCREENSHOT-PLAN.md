# Actual nonproduction evidence to capture later

## Current evidence

The included images show executed source/reference checks and fictional local output. They are not Azure Portal screenshots or screenshots of the full hosted platform.

## Proposed portal/application captures

- Storage account/container private access and version/deletion protection
- Defender for Storage scanning configuration and actual saved state
- Event Grid topic/subscription and queue destination
- Separate scan processor runtime state and scoped identity
- One fictional scan-result trace with exact file/version; never real document contents

## Terminal captures

Use the commands in [the command guide](COMMANDS.md). Capture real output with tool versions and the source commit, including failures when relevant. Label local source tests and mock Terraform plans accurately. Do not draw a terminal transcript or label a mock plan as cloud acceptance.

## Operating boundary

Nonproduction/portal captures are optional follow-up work. No service was started merely for this documentation. If a capture needs a paused API, scanner, paid provider request or temporary access, use the existing operating procedure and restore the original state afterward. Do not activate production or spend provider requests for presentation alone.

Crop private names, tenant/subscription IDs, account URLs, secure links, phone/email recipients and secrets. Use approved fictional records. Never publish an identity document or its barcode.

# Optional AI adapter

The source platform includes image preparation for employee badges. The public example instead provides a smaller structured text-classification adapter so the API boundary can be inspected without publishing private document images or the entire badge system.

`lab/ai.py` uses the Responses API, `store:false`, a strict JSON schema, an environment-selected model, a 30-second timeout and one request with no automatic paid retry. The demo and CI use no API key and make no paid request. Unit tests use a fake transport and synthetic text.

To integrate it separately, provide `OPENAI_API_KEY` and `OPENAI_MODEL` through your secret-management process and call `classify(approved_text, allow_paid=True)`. Choosing opt-in is a paid external-data operation: review the actual input, model capabilities, cost and retention first. Never pass government IDs, employee records or credentials into this example.

Structured output restricts shape, not truthfulness. Treat the category as a suggestion, never as malware clearance, identity proof or an employment decision. Validate refusals, incomplete responses and unexpected fields. Keep provider error bodies out of logs.

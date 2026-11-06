# Implementation walkthrough

Staff and applicants needed to upload sensitive documents, see when file checks completed and retrieve only authorized clean versions. Event delivery could be delayed or duplicated, and optional AI processing needed an explicit trust boundary.

## 1. Submit a file

A protected upload records owner and immutable version. The UI may say uploaded while the scan remains pending; availability requires a later clean proof.

## 2. Process the event

At-least-once delivery means duplicates are normal. The event journal returns the existing outcome for an identical replay and rejects conflicting reuse of the same event ID.

## 3. Replace the file

A new version becomes pending again. A delayed clean event for the old version must not unlock the replacement. Download also checks the exact content hash and employee binding.

## 4. Keep AI optional

The Responses adapter classifies approved synthetic text into a strict schema. It is disabled by default, makes one bounded call when explicitly invoked and never decides identity, eligibility or file cleanliness.

## Read the implementation

Start with [the domain module](../lab/domain.py), then [its tests](../tests/test_domain.py). The [dashboard report](../lab/demo.py) runs the same implementation; it does not substitute static success labels. `python -B -m lab demo` exits with an error if a demonstration assertion fails.

## Discuss the result

Describe the business problem first, the trust boundary second and the observed result third. Claim only the evidence in the validation record. A portable reference test is useful evidence of code behavior; it is not live-provider acceptance.

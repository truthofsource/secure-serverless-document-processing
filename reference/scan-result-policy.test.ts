import assert from "node:assert/strict";
import test from "node:test";

import {
  MALWARE_SCAN_PROVIDER,
  mapDefenderScanResult,
} from "./scan-result-policy.ts";

test(
  "maps No threats found to clean",
  () => {
    assert.equal(
      mapDefenderScanResult(
        "No threats found"
      ),
      "clean"
    );
  }
);

test(
  "maps Malicious to malicious",
  () => {
    assert.equal(
      mapDefenderScanResult(
        "Malicious"
      ),
      "malicious"
    );
  }
);

test(
  "maps Not scanned to error",
  () => {
    assert.equal(
      mapDefenderScanResult(
        "Not scanned"
      ),
      "error"
    );
  }
);

test(
  "maps Error to error",
  () => {
    assert.equal(
      mapDefenderScanResult(
        "Error"
      ),
      "error"
    );
  }
);

test(
  "maps an unknown future result to error",
  () => {
    assert.equal(
      mapDefenderScanResult(
        "Unexpected future result"
      ),
      "error"
    );
  }
);

test(
  "uses the approved provider name",
  () => {
    assert.equal(
      MALWARE_SCAN_PROVIDER,
      "Microsoft Defender for Storage"
    );
  }
);

export type MalwareScanState =
  | "clean"
  | "malicious"
  | "error";

export const MALWARE_SCAN_PROVIDER =
  "Microsoft Defender for Storage";

export function mapDefenderScanResult(
  scanResultType: string
): MalwareScanState {
  switch (scanResultType) {
    case "No threats found":
      return "clean";

    case "Malicious":
      return "malicious";

    case "Not scanned":
    case "Error":
    default:
      return "error";
  }
}

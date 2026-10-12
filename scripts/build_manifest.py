#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path


def main() -> None:
    data_path = Path(sys.argv[1] if len(sys.argv) > 1 else "public/data/v1/fly-ash.json")
    manifest_path = Path(sys.argv[2] if len(sys.argv) > 2 else "public/data/v1/manifest.json")
    raw = data_path.read_bytes()
    records = json.loads(raw)
    checksum = hashlib.sha256(raw).hexdigest()
    latest_date = max(record["date"] for record in records)
    manifest = {
        "schemaVersion": 1,
        "dataVersion": checksum[:12],
        "updatedAt": f"{latest_date}T00:00:00+08:00",
        "recordCount": len(records),
        "flyAshURL": "fly-ash.json",
        "checksumSha256": checksum,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {manifest_path} ({len(records)} records, {checksum[:12]})")


if __name__ == "__main__":
    main()


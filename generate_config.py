#!/usr/bin/env python3
"""Generate per-switch Cisco IOS config files from deployment JSON."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from printer_vlan.generate import write_configs
from printer_vlan.loader import load_deployment
from printer_vlan.validate import ValidationError, validate_deployment


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Cisco IOS configs for EVE-NG / Ansible")
    parser.add_argument(
        "json_file",
        nargs="?",
        default=ROOT / "data" / "printer-vlan-deployment.json",
        type=Path,
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=ROOT / "output" / "generated",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Generate even if validation fails (not recommended)",
    )
    args = parser.parse_args()

    try:
        data = load_deployment(args.json_file)
        if not args.skip_validation:
            validate_deployment(data)
        written = write_configs(data, args.output_dir)
    except ValidationError as exc:
        print(f"Validation failed for {args.json_file}", file=sys.stderr)
        for msg in exc.messages:
            print(f"  - {msg}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Generated {len(written)} file(s) in {args.output_dir}:")
    for path in written:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import json
from pathlib import Path
from typing import Any


def load_deployment(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)

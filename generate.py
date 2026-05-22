from pathlib import Path
from typing import Any


def _build_interface_lines(port: dict[str, Any], defaults: dict[str, Any]) -> list[str]:
    base = defaults.get("switch_port", {})
    lines = list(base.get("ios_config", []))
    override = port.get("override", {})

    vlan_id = port.get("vlan_id", base.get("switchport_access_vlan"))
    description = port.get("description", base.get("description", "Printer"))

    result: list[str] = []
    for line in lines:
        if line.startswith("description "):
            result.append(f"description {description}")
        elif line.startswith("switchport access vlan "):
            result.append(f"switchport access vlan {vlan_id}")
        else:
            result.append(line)

    for key, value in override.items():
        if key == "ios_lines" and isinstance(value, list):
            result.extend(value)
        elif key == "append_ios" and isinstance(value, list):
            result.extend(value)

    return result


def generate_switch_configs(data: dict[str, Any]) -> dict[str, str]:
    defaults = data.get("defaults", {})
    configs: dict[str, str] = {}

    for site in data.get("sites", []):
        site_id = site.get("site_id", "unknown")
        for switch in site.get("switches", []):
            hostname = switch["hostname"]
            blocks: list[str] = [
                "!",
                f"! Generated for site {site_id}",
                f"! Switch: {hostname}",
                f"! Management IP: {switch.get('management_ip', 'n/a')}",
                f"! dry_run={data.get('deployment', {}).get('dry_run', True)}",
                "!",
            ]

            for port in switch.get("ports", []):
                if not port.get("enabled", True):
                    continue
                port_id = port["port_id"]
                lines = _build_interface_lines(port, defaults)
                blocks.append(f"interface {port_id}")
                blocks.extend(f" {line}" if not line.startswith(" ") else line for line in lines)
                blocks.append("!")

            blocks.append("end")
            configs[hostname] = "\n".join(blocks) + "\n"

    return configs


def write_configs(data: dict[str, Any], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for hostname, content in generate_switch_configs(data).items():
        path = output_dir / f"{hostname}.cfg"
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written

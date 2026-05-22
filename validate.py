import re
from typing import Any

from jsonschema import Draft202012Validator

HOSTNAME_RE = re.compile(
    r"^[A-Z]{2}_[A-Z0-9]+_[A-Z0-9]+-F[0-9]{2}-R[0-9]+-[12]$"
)
MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")

SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["template_version", "defaults", "sites", "deployment"],
    "properties": {
        "template_version": {"type": "string"},
        "defaults": {
            "type": "object",
            "required": ["switch_port"],
            "properties": {
                "switch_port": {
                    "type": "object",
                    "required": ["ios_config", "switchport_access_vlan"],
                }
            },
        },
        "sites": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["site_id", "vlans", "switches", "printers"],
                "properties": {
                    "site_id": {"type": "string", "minLength": 1},
                    "vlans": {"type": "array", "minItems": 1},
                    "switches": {"type": "array", "minItems": 1},
                    "printers": {"type": "array"},
                },
            },
        },
        "deployment": {
            "type": "object",
            "required": ["dry_run"],
            "properties": {"dry_run": {"type": "boolean"}},
        },
    },
}


class ValidationError(Exception):
    def __init__(self, messages: list[str]) -> None:
        self.messages = messages
        super().__init__("\n".join(messages))


def _expected_hostname(site_id: str, building: str, floor: str, stack_id: str, stack_member: int) -> str:
    floor_code = floor if floor.startswith("F") else f"F{floor}"
    return f"{site_id}_{building}-{floor_code}-{stack_id}-{stack_member}"


def validate_deployment(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    schema_errors = sorted(Draft202012Validator(SCHEMA).iter_errors(data), key=lambda e: list(e.path))
    for err in schema_errors:
        path = ".".join(str(p) for p in err.path) or "(root)"
        errors.append(f"[schema] {path}: {err.message}")

    default_vlan = data.get("defaults", {}).get("switch_port", {}).get("switchport_access_vlan")

    for site in data.get("sites", []):
        site_id = site.get("site_id", "")
        vlan_ids = {v["vlan_id"] for v in site.get("vlans", []) if "vlan_id" in v}
        printer_ids = {p["printer_id"] for p in site.get("printers", []) if "printer_id" in p}

        switches_by_host: dict[str, dict[str, Any]] = {}
        for sw in site.get("switches", []):
            host = sw.get("hostname", "")
            if host in switches_by_host:
                errors.append(f"[site {site_id}] duplicate switch hostname: {host}")
            switches_by_host[host] = sw

            expected = _expected_hostname(
                sw.get("site_id", site_id),
                sw.get("building", ""),
                sw.get("floor", ""),
                sw.get("stack_id", ""),
                int(sw.get("stack_member", 0)),
            )
            if host and host != expected:
                errors.append(
                    f"[site {site_id}] hostname '{host}' does not match convention (expected '{expected}')"
                )
            elif host and not HOSTNAME_RE.match(host):
                errors.append(f"[site {site_id}] hostname '{host}' fails pattern check")

            if sw.get("site_id") and sw["site_id"] != site_id:
                errors.append(f"[site {site_id}] switch {host}: site_id mismatch ({sw['site_id']})")

            ports = sw.get("ports", [])
            port_ids = [p.get("port_id") for p in ports]
            if len(port_ids) != len(set(port_ids)):
                errors.append(f"[site {site_id}] switch {host}: duplicate port_id entries")

            for port in ports:
                vid = port.get("vlan_id")
                if vid is not None and vid not in vlan_ids:
                    errors.append(
                        f"[site {site_id}] switch {host} port {port.get('port_id')}: "
                        f"vlan_id {vid} not defined in site vlans"
                    )
                pref = port.get("printer_ref")
                if pref and pref not in printer_ids:
                    errors.append(
                        f"[site {site_id}] switch {host} port {port.get('port_id')}: "
                        f"unknown printer_ref '{pref}'"
                    )

        for printer in site.get("printers", []):
            pid = printer.get("printer_id", "?")
            vref = printer.get("vlan_ref")
            if vref is not None and vref not in vlan_ids:
                errors.append(f"[site {site_id}] printer {pid}: vlan_ref {vref} not in site vlans")

            mac = printer.get("mac_address", "")
            if mac and not MAC_RE.match(mac):
                errors.append(f"[site {site_id}] printer {pid}: invalid mac_address '{mac}'")

            sref = printer.get("switch_ref", {})
            ref_host = sref.get("hostname")
            ref_port = sref.get("port_id")
            if ref_host:
                sw = switches_by_host.get(ref_host)
                if not sw:
                    errors.append(f"[site {site_id}] printer {pid}: switch_ref host '{ref_host}' not found")
                elif ref_port:
                    port_ids_on_sw = {p.get("port_id") for p in sw.get("ports", [])}
                    if ref_port not in port_ids_on_sw:
                        errors.append(
                            f"[site {site_id}] printer {pid}: port '{ref_port}' "
                            f"not on switch '{ref_host}'"
                        )

        if default_vlan and vlan_ids and default_vlan not in vlan_ids:
            errors.append(
                f"[site {site_id}] defaults.switch_port VLAN {default_vlan} "
                f"not present in site vlans {sorted(vlan_ids)}"
            )

    if errors:
        raise ValidationError(errors)
    return []

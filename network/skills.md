# Skills

Skills and technologies used in this repository's Printer VLAN automation lab.

## Network engineering

- **Cisco IOS switching**: access-port config, VLAN assignment (`switchport access vlan`), `spanning-tree portfast edge`
- **QoS**: `mls qos trust cos`, `auto qos trust`, SRR queue bandwidth sharing, priority queuing
- **VLAN design**: a dedicated printer VLAN per site, with client isolation and restricted egress (print servers, DNS, NTP)
- **Standard naming**: hostname convention (`<SITE>_<BLDG>-F<floor>-R<stack>-<member>`) and port description patterns
- **Lab testing**: EVE-NG used to validate changes before production

## Automation and infrastructure as code

- **Ansible**: two-stage playbook (validate and generate on localhost, then push to switches) using `cisco.ios.ios_config` over `ansible.netcommon.network_cli`
- **Safe change management**: `dry_run` flag, Ansible check mode, and a pre-push check that the config file exists
- **Data-driven config**: one JSON source of truth (defaults plus per-site VLANs, switches and printers) rendered into per-switch `.cfg` files
- **Inventory management**: YAML inventory with enable/become privilege escalation

## Python

- **Validation**: JSON Schema (Draft 2020-12, `jsonschema`) plus custom regex checks for hostnames and MAC addresses
- **Config generation**: default templates with per-port overrides (`ios_lines`, `append_ios`)
- **CLI tooling**: `argparse` scripts that return proper exit codes and error reporting
- **Modern practices**: type hints, `pathlib`, custom exception types, modular layout (`loader` / `validate` / `generate`)

## Tooling and workflow

- **PowerShell**: scripts to find Git and push the lab into the `Network_Automation` repo
- **Git / GitHub**: version control for network configs
- **Python environments**: `venv` and `requirements.txt`

## Workflow

```
JSON data → validate.py → generate_config.py → Ansible (check mode) → Ansible (apply) → EVE-NG lab switches
```

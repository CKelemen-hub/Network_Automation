# Printer VLAN Lab

Validate printer VLAN deployment JSON, generate Cisco IOS interface configs, and test in EVE-NG before production.

## Quick start

```powershell
cd printer-vlan-lab
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python scripts\validate.py
.\.venv\Scripts\python scripts\generate_config.py
```

Generated configs: `output/generated/*.cfg`

## Ansible (EVE-NG)

```powershell
copy ansible\inventory.lab.yml.example ansible\inventory.lab.yml
# Edit management IPs, then:
cd ansible
ansible-galaxy collection install cisco.ios ansible.netcommon
ansible-playbook -i inventory.lab.yml playbook-lab.yml
```

Keep `deployment.dry_run: true` in `data/printer-vlan-deployment.json` until lab testing is complete.

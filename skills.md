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

---

# Skill: Business Tax Accountant (Capital Gains Efficiency)

**Objective:** Legally minimise the tax a business pays on capital gains, so the business keeps as much cash as possible.

**Default jurisdiction:** UK. Ask first if the business is elsewhere, as rules and rates differ. Confirm current rates and thresholds on gov.uk before acting, because they change most Budgets.

## Operating principles

1. **Avoidance, not evasion.** Use reliefs, exemptions and timing that Parliament intended. Never misstate figures or hide disposals. Anything artificial risks the General Anti-Abuse Rule (GAAR).
2. **Model before advising.** Compare after-tax cash for every option, not just the tax saved.
3. **Tax follows commercial reality.** Don't let tax drive a bad business decision.
4. **Document everything.** Keep cost records, valuations, board minutes and claim dates.

## Entity check (first question)

| Seller | Gains taxed as | Key point |
|---|---|---|
| Limited company | Corporation Tax on chargeable gains (19%–25% depending on profits) | No annual exempt amount; indexation frozen at Dec 2017 |
| Sole trader / partnership | Capital Gains Tax (CGT) in the owner's hands | Annual exempt amount (£3,000) and personal reliefs apply |
| Owner selling shares | CGT (18%/24% for most gains) | Business Asset Disposal Relief (BADR) may apply |

## Tax-saving playbook

### 1. Reliefs and exemptions (biggest savings)
- **Substantial Shareholding Exemption (SSE):** gain on selling shares in a trading company or subsidiary is fully exempt if the seller held 10% or more for 12 months in the previous 6 years. Check eligibility before any share sale.
- **Rollover relief:** defer the gain on qualifying business assets (land, buildings, fixed plant) by reinvesting in replacement assets from 1 year before to 3 years after the sale.
- **Business Asset Disposal Relief (BADR):** for individuals selling a business or shares in a personal company (5% or more, officer or employee, 2 years). The rate is 18% from April 2026 on up to £1m of lifetime gains.
- **Gift holdover relief:** defers the gain when business assets are gifted, which is useful for succession.
- **Incorporation relief:** moving a sole trade into a company defers the gain automatically. Check that it applies and consider whether to disapply it.
- **EIS / SEIS deferral:** reinvest a gain into qualifying shares to defer or reduce tax.
- **Chattels exemption:** items with a life under 50 years that sell for £6,000 or less are exempt. Wasting assets are also exempt.

### 2. Group structure planning
- **Intra-group transfers** of assets between UK group companies are on a no-gain/no-loss basis, so gains can be moved to the company that has losses.
- **Group relief and gain/loss reallocation:** elect to transfer a gain or loss between group companies to use losses efficiently.
- **Degrouping charges:** plan around them if a company leaves the group within 6 years of receiving an asset.

### 3. Losses
- Set current-year capital losses against gains in the same period.
- Carry unused losses forward with no time limit, but **notify HMRC within 4 years** or the loss is lost.
- **Negligible value claims:** crystallise a loss on a worthless asset without an actual sale.
- Consider realising losses in the same accounting period as a large gain. Avoid buying back the same asset within 30 days (the bed-and-breakfasting rules).
- Losses in connected-party transactions can only be used against gains from that same person.

### 4. Timing
- Choose the accounting period end to split gains across periods and use lower Corporation Tax bands (marginal relief applies between £50k and £250k of profit).
- Individuals can spread disposals across tax years to use two annual exempt amounts and basic-rate band.
- The disposal date is the date of the contract, not completion. Check this near year end.

### 5. Reduce the gain itself
- Claim all allowable costs: acquisition costs, stamp duty, legal and valuation fees, capital improvement costs and disposal costs.
- Claim **capital allowances** (Annual Investment Allowance, full expensing) on plant and machinery purchases to cut trading profit.
- Consider pension contributions from company profits to lower the tax bill in the year of a large gain.
- Check whether IP and intangibles fall under the separate intangible fixed assets regime, which may be more favourable.

## Inputs to gather before advising
- Entity type, year end and profit level
- Asset being sold, purchase date, base cost, improvements, expected proceeds
- Ownership and group structure, and who the buyer is
- Existing losses (capital and trading), and any planned reinvestment
- Owner's plans: retire, exit, hold, gift or pass on

## Output format
1. Estimated tax bill with no planning
2. Reliefs that apply, with eligibility tests and deadlines
3. Ranked strategies with estimated tax saved and after-tax cash
4. Risks (GAAR, anti-avoidance, clawbacks, cash flow)
5. Actions with dates, and the evidence to keep

## Guardrails
- This is general guidance, not regulated tax advice. Larger transactions need a chartered accountant or tax adviser.
- Flag any scheme that looks aggressive or artificial rather than recommending it.
- Report disposals correctly on the Corporation Tax return (CT600) or Self Assessment.

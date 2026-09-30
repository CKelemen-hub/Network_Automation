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

# Skill: UK Corporate Tax Efficiency Accountant

**Jurisdiction:** United Kingdom.

**Objective:** Continuously maximise the company's *legally achievable* tax efficiency. That means minimising Corporation Tax and tax on corporate chargeable gains, using every legitimate deduction, relief, allowance, credit, loss, exemption and incentive, and timing and structuring transactions to keep the most after-tax cash.

## Operating principles

1. **Optimise after-tax cash and economic value**, not accounting profit or the reported tax charge.
2. **Analyse tax before acting.** Review the tax effect of every transaction, investment, financing, acquisition, disposal or reorganisation *before* it is executed.
3. **Continuous, not annual.** Treat tax planning as an ongoing function, not a year-end exercise.
4. **Multi-year view.** Compare multi-year outcomes, not single-year savings.
5. **Substance over artifice.** Prefer robust, commercially genuine structures over transactions created only to generate deductions.

## Compliance boundary (hard limits)

- Use only legitimate deductions, reliefs, allowances, credits and exemptions.
- Never fabricate expenses or transactions, or create false business purposes or documentation.
- Never conceal income, assets or beneficial ownership.
- Never recommend evasion or fraudulent claims.
- Document all material tax positions. Watch the General Anti-Abuse Rule (GAAR) and the Diverted Profits Tax (DPT).
- This is general guidance, not regulated tax advice. Material transactions need a chartered tax adviser.

## UK reference (verify at gov.uk each Budget; figures may have changed)

| Item | Position |
|---|---|
| Main rate | 25% on profits above £250,000 |
| Small profits rate | 19% on profits of £50,000 or less |
| Marginal relief | Profits between £50,000 and £250,000 (limits are shared across associated companies) |
| Allowances and reliefs | AIA, Full Expensing, First-Year Allowances, Structures and Buildings Allowance, R&D relief, RDEC, Patent Box, trading and capital loss relief, group relief, goodwill/intangibles reliefs, creative-industry reliefs |

## Core functions

### 1. Corporation Tax
- Audit all expenditure for deductibility and find missed or underclaimed deductions.
- Manage taxable-profit timing and model marginal relief.
- Check for overpaid tax and repayment opportunities.
- Monitor rates and thresholds.

### 2. Capital allowances
- Identify qualifying plant and machinery before purchase, since asset classification drives the relief.
- Maximise the Annual Investment Allowance (AIA), Full Expensing and First-Year Allowances, and evaluate the Structures and Buildings Allowance (SBA).
- Time purchases to maximise the allowances available.

### 3. Research and development
- Identify qualifying R&D activity and capture eligible staff, contractor, software, materials and other costs.
- Choose the correct scheme (RDEC or the SME-intensive route) and keep technical evidence for every claim.
- Watch for rule changes and new innovation incentives.

### 4. Intellectual property
- Identify qualifying IP and test **Patent Box** eligibility.
- Review development, ownership and exploitation structures.
- Ensure IP arrangements have genuine commercial substance.

### 5. Losses
- Track trading, capital and property-income losses.
- Evaluate carry-forward and carry-back (trading losses can go back 12 months in some cases; capital losses cannot be carried back) and use group relief where available.
- Watch loss-restriction rules on large carried-forward losses.
- Notify HMRC of capital losses within 4 years, or the loss is lost.

### 6. Corporate chargeable gains
- Identify **embedded gains** before disposal, and calculate allowable acquisition, improvement and disposal costs.
- **Reliefs:** Substantial Shareholding Exemption (10% or more held for 12 months in the prior 6 years), rollover relief on qualifying business assets (reinvest from 1 year before to 3 years after), intra-group no-gain/no-loss transfers (watch degrouping charges within 6 years), and negligible value claims.
- Model disposal timing, alternative disposal structures and replacement-asset options.
- Companies have no annual exempt amount, and indexation is frozen at Dec 2017.
- The disposal date is the date of the contract, not completion.

### 7. Financing
- Compare debt and equity, and leasing and buying, on after-tax cash flow.
- Analyse interest deductibility, including the Corporate Interest Restriction and late-paid interest rules.
- Evaluate refinancing and asset-backed structures, and financing costs.

### 8. Mergers and acquisitions
- Do tax analysis before every acquisition, disposal and reorganisation.
- Compare share and asset purchases, and the treatment of goodwill and intangibles.
- Identify transferable tax attributes (losses, allowances) and model post-deal consequences.
- Plan reorganisations and asset transfers.

### 9. International tax and transfer pricing
- Assess cross-border exposure, treaties, withholding taxes and permanent-establishment risk.
- Review intercompany transactions and apply arm's-length methods, with documentation that would stand up to challenge.
- Check controlled foreign company rules and minimum-tax regimes (Pillar Two applies to large groups).
- Structure only where commercially justified.

### 10. Tax timing
- Compare current-year and future-year deductions.
- Model asset acquisition and disposal timing, and loss utilisation timing.
- Time recognition of eligible expenditure.
- Consider pension contributions from company profits.

## Strategy and innovation (continuous scan)

Monitor HMRC guidance and manuals, Finance Acts, Budget announcements, tax tribunal and court decisions, and sector-specific incentives. In each review:
- Look for opportunities created by changes in law, company structure, financing, acquisitions, disposals or restructuring.
- Look for interactions between different tax rules, and for overlooked deductions and reliefs.
- Reassess existing structures for further optimisation.
- Benchmark publicly disclosed group tax strategies as context only, not as a template.

## Opportunity analysis

For each opportunity, calculate:
- Estimated tax saving and cash-flow impact
- Implementation cost and ongoing admin cost
- Accounting consequences
- Legal and tax risk, and HMRC challenge risk
- Commercial substance
- **Expected net after-tax economic benefit**

**Rank by:** net after-tax benefit, then saving relative to cost, legal certainty, commercial viability and long-term sustainability.

## Required output for every opportunity

1. **Mechanism:** how it works
2. **Eligibility conditions**
3. **Estimated financial benefit**
4. **Implementation requirements** and deadlines
5. **Relevant UK rules** (legislation or HMRC manual reference)
6. **Risks**
7. **Interaction** with the company's existing tax position

## Key metrics to track

Effective tax rate, cash Corporation Tax paid, tax as a percentage of operating cash flow, total deductions identified, reliefs and credits claimed, capital allowances claimed, R&D relief obtained, losses used, tax saved, implementation cost, and net after-tax benefit.

## Source priority

1. HMRC
2. HM Treasury
3. GOV.UK legislation and official guidance
4. UK tax tribunal and court decisions
5. OECD
6. Reputable UK tax and legal professional publications

## Inputs to gather first

Entity and group structure, year end and profit level, asset register and planned purchases and disposals, existing losses, financing arrangements, R&D and IP activity, cross-border operations, and any planned transactions.

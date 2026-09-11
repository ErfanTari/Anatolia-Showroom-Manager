# Human exchange tables

These files are derived from `../showroom.sqlite`. Edit the relevant fields, keep stable IDs and `base_revision`, and use **Data & guidelines → Source files & import** to validate before applying.

| File | Use |
|---|---|
| [products.csv](products.csv) | Positioning, Hit, lifecycle, required designs, color grouping |
| [variants.csv](variants.csv) | SKU, finish, format, thickness and availability |
| [slots.csv](slots.csv) | Visibility classification and repeat exceptions |
| [fixtures.csv](fixtures.csv) | Review dimensions/positions and mark geometry verification; moves use proposals |
| [placements.csv](placements.csv) | Review current occupants or propose replacements by slot |
| [rules.csv](rules.csv) | Confirm/edit guideline parameters |
| [questions.csv](questions.csv) | Collect team answers, owners and evidence |
| [tasks.csv](tasks.csv) | Read the work list; update stage/evidence through the app |

CSV imports are atomic. Existing-record updates reject unknown IDs. A stale revision must be re-exported and reconciled. Placement imports create drafts and do not mark products installed. To change a product, supply its variant ID and clear the old `face_id` unless you select a face for the new design.

The database contains fuller provenance, source rows, faces, scenarios and audit events. [Data contract](../../docs/DATA_AND_ASSETS.md) · [Team decisions](../../docs/TEAM_DECISIONS.md)

# ADR-0061: Schema 1.4 — Multidomain Coverage and Dataset Fields

Status: Decided — 2026-10-20
Date: 2026-10-20
Decided by: Sajan (sole owner), instruction to expand content across the sciences and
engineering and to upgrade the schema as needed to carry the datasets.
Relates to: ADR-0016 (extensions/external ids), ADR-0017 (adaptive metadata seam),
ADR-0021 (entity types), ADR-0044 (integrated foundation), ADR-0060 (delegated
canonicalization), ADR-0062 (open content acquisition)

## Context

Schema 1.3 was shaped around a physics-first corpus. The owner now requires bachelor-level
coverage across physics, chemistry, biology, astronomy, mathematics, and five engineering
disciplines. Those fields need entity kinds and payloads that the original enum and fields did
not express: theorems, algorithms, data structures, processes, materials, reactions,
organelles, instruments, protocols, standards, missions, and empirical datasets.

The extension seam (ADR-0017) is deliberately scalar and is not suitable for structured
datasets or formal statements. Silently stuffing structured data into `extensions` would make
it unvalidated and undiscoverable. The schema must evolve.

## Decision

Schema version **1.4.0** adds the following **optional** fields. Existing entities remain
valid; no migration is required.

### 1. Expanded `type` enum

Adds `constant`, `principle`, `theorem`, `operator`, `function`, `distribution`, `process`,
`structure`, `system`, `material`, `reaction`, `organelle`, `technique`, `instrument`,
`algorithm`, `data-structure`, `protocol`, `standard`, `dataset`, `mission`.

The enum remains closed so a typo cannot create a new kind. New kinds require a schema change,
not an extension.

### 2. `level`

`foundational | intermediate | advanced | null`. This is a complexity marker, not a grade or
curriculum tag; the Northstar prohibition on curriculum encoding remains in force.

### 3. Learning and application fields

- `learning_objectives: string[]`
- `applications: string[]`
- `limitations: string[]`

These describe what a learner should be able to do and where the entity applies or fails. They
do not encode a syllabus.

### 4. `formal`

A closed object for machine-readable formal content:

```yaml
formal:
  statement: ...
  equation: ...
  variables: [{symbol, meaning, unit}]
  conditions: [...]
  dimensions: "M L T^-2"
  approximations: [...]
```

This replaces ad-hoc prose for laws, theorems, equations, quantities, algorithms, and
protocols. The legacy `equation`, `symbol`, and `unit` fields remain for compatibility.

### 5. `datasets`

An array of dataset descriptors:

```yaml
datasets:
  - name: ...
    description: ...
    variables: [...]
    unit: ...
    source_ref: stemma:src....
    url: ...
    license: ...
    format: ...
    notes: ...
```

Datasets are attached to the entity that interprets them; the dataset itself is not a
canonical entity unless it has its own `type: dataset` record. This keeps measurements,
constants, material properties, and benchmark corpora discoverable without turning every table
into a top-level concept.

### 6. Provenance for delegated canonicalization

`provenance.review_mode`, `provenance.verification`, and `provenance.delegation` are added per
ADR-0060. They are optional and default to the human path.

## Versioning

- `schema_version` bumps to `1.4.0` in `schema/VERSION.yaml`.
- `export_version` stays `2.2.0`: the export schema already carries entity objects with open
  properties, and the additions are optional. Consumers that ignore them read the same export.
- `relation_registry_version` is unchanged.

## Consequences

**Easier.** A single schema can represent theorems, lab techniques, engineering standards,
biological structures, and datasets without abusing `extensions`.

**Harder.** More fields mean more validation surface. The validator must enforce cross-field
rules (for example, `type: quantity` still requires `quantity_kind`, `tensor_character`, and
`same_dimensional_quantities`). New tests cover the added shapes.

**Risk.** Broad enums can become a dumping ground. The type must describe the entity's
epistemic kind, not its topic; a "dataset about thermodynamics" is `type: dataset`, while
"thermodynamics" is `type: concept` or `type: principle`.

## Verification

- `schema/concept.schema.json` validates under Draft 2020-12.
- Existing entities validate unchanged.
- New tests cover each added field, the expanded enum, and delegated provenance.
- `scripts/validate.py` reads the schema enum as authoritative and its fallback `TYPES` set
  matches 1.4.0.

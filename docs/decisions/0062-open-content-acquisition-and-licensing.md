# ADR-0062: Open Content Acquisition and Licensing

Status: Decided — 2026-10-20
Date: 2026-10-20
Decided by: Sajan (sole owner), instruction to use free open sources, read major
publications, and verify before canonicalizing.
Relates to: ADR-0060 (delegated canonicalization), ADR-0061 (schema 1.4), ADR-0043
(source provenance), ADR-0044 (integrated foundation)

## Context

The content mandate requires large-scale acquisition from external sources. The repository's
canonical content is CC BY 4.0. Not every "free" source is compatible:

- OpenStax books are generally **CC BY-NC-SA 4.0** (checked via the OpenStax CMS API on
  2026-10-20). The NC and SA terms conflict with a CC BY 4.0 canonical corpus and with
  commercial reuse.
- Wikipedia/Wikibooks are CC BY-SA; MIT OCW is CC BY-NC-SA; many LibreTexts books are
  CC BY-NC-SA.
- US government works (NIST, NASA, NIH, USGS, DOE) are generally public domain.
- Some open textbooks are CC BY 4.0 or CC0 and can be reused with attribution.

Copying NC-SA prose into `content/` would relicense the corpus by accident. That is not
acceptable. The acquisition pipeline must separate **coverage discovery** from **expression**.

## Decision

### 1. Source tiers

| Tier | License | Use |
|---|---|---|
| A | CC0 / public domain | May copy or adapt text with attribution where required |
| B | CC BY 4.0 / CC BY 3.0 | May adapt with attribution and change notice |
| C | CC BY-SA / CC BY-NC-SA / CC BY-NC | **Reference only**: term inventory, scope checklist, factual verification; no copied prose |
| D | All rights reserved | Citation only; no text reuse |

### 2. OpenStax is a Tier C reference

OpenStax TOCs, chapter titles, and key-term lists are used to discover coverage and to build a
term inventory. OpenStax glossary text is **not** copied into canonical definitions. Canonical
definitions are independently phrased and then checked against the source's factual claims.
Source records carry the OpenStax title, authors, URL, ISBN, retrieval date, and the actual
CC BY-NC-SA license so consumers can see the reference relationship.

Term lists and facts are not treated as reusable prose. Where a definition is close to a
source's expression, it must be rewritten or the source must move to Tier A/B.

### 3. Source records are first-class

Every imported tranche creates a `sources/src.<slug>.yaml` record with:

- title, authors/editors, publisher, year, ISBN/DOI, URL;
- license name, version, and URL;
- `source_kind` (textbook, standards, institutional, academic);
- retrieval date and the exact pages/sections consulted;
- a `rights` note explaining what was and was not reused.

### 4. Verification before canonicalization

A candidate may be canonicalized only after:

1. schema and ID validation;
2. source resolution (the cited record exists and the locator is plausible);
3. an independent second pass (different process agent or deterministic check family);
4. a licensing check (no Tier C prose copied);
5. duplicate/identity checks within the domain.

The checks are recorded in `provenance.verification.checks`, not asserted in prose.

### 5. Attribution and change notices

CC BY 4.0 canonical content derived from Tier A/B sources carries attribution in the entity's
`provenance.original_author`/`source` and the source record. Adapted text carries a change
notice. Tier C sources are cited as references, not as text donors.

## Consequences

**Easier.** The pipeline can use the best open textbooks for coverage without contaminating
the corpus license. Source provenance is inspectable per entity.

**Harder.** Definitions must be written, not scraped. The acquisition step produces a term
inventory and a verification packet, not a finished corpus. That is the correct trade.

**Risk.** Independently phrased definitions can drift from the source. Mitigation: two-pass
verification, explicit source locators, and sampled human audit under ADR-0060.

## Verification

- `scripts/openstax_inventory.py` records license metadata and never emits canonical prose.
- `scripts/check_source_licenses.py` rejects a canonical entity whose source license is Tier C
  and whose definition is a verbatim/near-verbatim match.
- Tests cover license classification, source resolution, and a near-verbatim rejection case.

---
name: create-knowledge-graph
description: Creates knowledge graph serializations from free-form text—typically Turtle (.ttl), optionally YAML-LD in Markdown for publication workflows. Resolves entities with find-url-for, uses dereferenceable or labeled local IRIs, then runs validate-knowledge-graph (Iolanta kglint). Use when converting prose to RDF, adding TTL or YAML-LD data from a description.
---

# Create Knowledge Graph from Text

## Arguments

1. **Free-form text** — The user's description of entities, relationships, events, or facts to capture.
2. **File name** — Output file. Prefer **`.ttl`** for a standalone graph. For **Markdown + YAML-LD** (e.g. nanopublication assertion sources), use **`.md`** and put JSON-LD 1.1 as YAML in the frontmatter (`@context`, `@included` or `@graph`, etc.).

Determine both from the user message. If either is missing, ask.

## Workflow

1. **Ontology** — Use the project ontology if it fits; otherwise define classes and properties inline or use standard vocabularies.
2. **Extract** — Map the text to triples (subject–predicate–object).
3. **Resolve entities** — For each entity (person, place, work, series, organization, concept), use the [find-url-for](../find-url-for/SKILL.md) skill to find an existing linked-data URL (e.g. Wikidata, DBpedia, VIAF). Prefer reusing those URIs instead of minting new ones. Only define local individuals for entities that have no suitable external URI.
4. **Write** — Produce **Turtle** and/or **Markdown with YAML-LD frontmatter** in the project directory.
   - **Existing URLs first** — Use the URIs from step 3 where found (with the appropriate prefix, e.g. `wd:Q12345`).
   - **No labels/names for external linked-data entity URIs** — Do not add `rdfs:label` or `schema:name` for entities that use Wikidata, DBpedia, VIAF, etc.; the label can be resolved from the source. Add `rdfs:label` (and `schema:name` if used) for **locally minted** resources and for classes/properties from vocabularies that lack labels in the loaded context.
   - **Local IRIs must be usable in validation** — kglint reports `uri-label-identical` if a minted URI has no label and is not dereferenceable. Prefer one of:
     - **Canonical document URL + fragment** — Set `@base` to a **dereferenceable** URL for the file when published (e.g. `https://raw.githubusercontent.com/<org>/<repo>/<branch>/<path>/index.md`) and use fragment ids (`#article`, `#MyConcept`). A GET on that URL should return the file that contains the YAML-LD (after push). Avoid placeholder hosts that always 404.
     - **Slash-terminated namespace + local names** — `https://example.org/mykg/topics/foo/` + `bar` → `https://example.org/mykg/topics/foo/bar` only if you control that namespace or accept non-dereferenceable IRIs **and** supply `rdfs:label` / `schema:name` on those resources in the same graph.
   - **Do not** use example placeholder domains as real namespaces unless the user accepts non-resolution; the old example `knowledgegraph.tech/kgcmart/...` was illustrative only and may not resolve.
   - **Fragments (`#`)** — Allowed when the **base** is the **document IRI** (the markdown or ttl document URL). Do not use arbitrary `#` names without a coherent `@base` that points at that document.
   - **Referencing other documents** — If you use `dct:references` or similar with **full URL objects**, add a separate `@included` node with the **same `@id`** and a `schema:name` so kglint can label the referenced IRI (see validate-knowledge-graph skill).
5. **Validate** — Apply the [validate-knowledge-graph](../validate-knowledge-graph/SKILL.md) skill on the created file (`.ttl` or `.md`).

## YAML-LD in Markdown (optional)

- Use `---` frontmatter; put JSON-LD 1.1 as YAML (`"@context"`, `"@included"` or `"@graph"`, etc.).
- Prefer **`@included`** over **`@graph`** if you want to avoid the `@graph` keyword.
- After editing, run `iolanta <path/to/file.md> --as kglint/json` and fix until `assertions` is empty.

## Notes

- **Wikidata predicates** in YAML-LD (e.g. `wdt:P2283`) may lack human-readable labels in kglint; prefer vocabulary with labels, or `skos:related` when precision tradeoffs are acceptable.
- Prefer **simpler** shapes (`schema:CreativeWork`, `rdf:Property`) over heavy OWL/SKOS collections if tools mis-handle blank nodes.

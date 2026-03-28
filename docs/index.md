---
title: nanopublishing
subtitle: A coding-agent workflow for nanopublications
hide:
  - navigation
  - toc
---

# nanopublishing

<p class="site-subtitle">A coding-agent workflow for nanopublications</p>

This repository is a working nanopublishing workflow for coding agents.
Here is what using it looks like in one small end-to-end session.

<div class="terminal-session" markdown="1">

<div class="terminal-line user">user$ I want a nanopublication about which SSD form factors can use which interfaces.</div>
<div class="terminal-line agent">agent$ I'll draft the file, formalize it, and publish the result.</div>

### Stage 1: plain Markdown

```markdown
# SSD interface to form factor mapping

This publication records common compatibility facts between SSD form factors and the interfaces they can use.

## Common pairings

| Form factor | Interface | Note |
|-------------|-----------|------|
| **M.2** | **SATA** or **PCIe** | M.2 is a physical form factor and connector family, not a single protocol. |
| **mSATA** | **SATA** | Older mini-card SATA form factor. |
| **U.2** | **PCIe** | Commonly used for NVMe SSDs over PCIe in servers and workstations. |
| **Add-in card (AIC)** | **PCIe** | SSD implemented as a PCIe expansion card. |
| **2.5-inch** | **SATA** | The common consumer SSD pairing. |

## Caveat

These are common compatibility pairings, not an exhaustive compatibility matrix. Connector keying, controller support, and system design still determine what a given device or slot actually supports.
```

<div class="terminal-line user">user$ /find-url-for compatible with</div>
<div class="terminal-line agent">agent$ I can use Wikidata property <code>wd:P8956</code> for <code>compatible-with</code>.</div>
<div class="terminal-line user">user$ /semantify docs/examples/types-of-ssds/interface-to-form-factor-mapping/index.md</div>
<div class="terminal-line agent">agent$ I added YAML-LD frontmatter and mapped the compatibility facts to linked data.</div>

### Stage 2: after `/semantify`

```markdown
---
"@context":
  - https://json-ld.org/contexts/dollar-convenience.jsonld
  - "@language": en
    wd: https://www.wikidata.org/entity/
    wdt: http://www.wikidata.org/prop/direct/
    compatible-with:
      "@type": "@id"
      "@id": wd:P8956
"@included":
  - $id: wd:Q15528609
    compatible-with:
      - wd:Q188639
      - wd:Q206924
  - $id: wd:Q64538905
    compatible-with: wd:Q188639
  - $id: wd:Q65034999
    compatible-with: wd:Q206924
  - $id: wd:Q216158
    compatible-with: wd:Q206924
  - $id: wd:Q65037415
    compatible-with: wd:Q188639
---

# SSD interface to form factor mapping

This publication records common compatibility facts between SSD form factors and the interfaces they can use.

## Common pairings

| Form factor | Interface | Note |
|-------------|-----------|------|
| **M.2** | **SATA** or **PCIe** | M.2 is a physical form factor and connector family, not a single protocol. |
| **mSATA** | **SATA** | Older mini-card SATA form factor. |
| **U.2** | **PCIe** | Commonly used for NVMe SSDs over PCIe in servers and workstations. |
| **Add-in card (AIC)** | **PCIe** | SSD implemented as a PCIe expansion card. |
| **2.5-inch** | **SATA** | The common consumer SSD pairing. |

## Caveat

These are common compatibility pairings, not an exhaustive compatibility matrix. Connector keying, controller support, and system design still determine what a given device or slot actually supports.
```

<div class="terminal-line user">user$ /nanopublish docs/examples/types-of-ssds/interface-to-form-factor-mapping/index.md</div>
<div class="terminal-line agent">agent$ Published. The signed artifact stays next to the Markdown source.</div>

### Stage 3: after `/nanopublish`

```text
Trusty URI:
https://w3id.org/np/RAMIHkOctLsK2ZlbWS0gr0kz9wFffP0fHSIN-N_aKrgC8

Retained signed artifact:
docs/examples/types-of-ssds/interface-to-form-factor-mapping/signed.index.trig
```

```trig
@prefix sub: <https://w3id.org/np/RAMIHkOctLsK2ZlbWS0gr0kz9wFffP0fHSIN-N_aKrgC8/> .
@prefix this: <https://w3id.org/np/RAMIHkOctLsK2ZlbWS0gr0kz9wFffP0fHSIN-N_aKrgC8> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

sub:Head {
  this: a np:Nanopublication ;
    np:hasAssertion sub:assertion ;
    np:hasProvenance sub:provenance ;
    np:hasPublicationInfo sub:pubinfo .
}
```

</div>

## More examples

### :material-harddisk: Types of SSDs

<div class="grid cards" markdown>

-   [SSD host protocol classification](examples/types-of-ssds/interface-scheme/index.md)

    SATA, SAS, and NVMe as SSD host protocols.

-   [SSD form factor scheme](examples/types-of-ssds/form-factor-scheme/index.md)

    M.2, mSATA, U.2, 2.5-inch, and add-in card form factors.

-   [SSD interface to form factor mapping](examples/types-of-ssds/interface-to-form-factor-mapping/index.md)

    Which common SSD form factors pair with SATA or PCIe.

-   [M.2 keying scheme for SSDs](examples/types-of-ssds/m2-keying-scheme/index.md)

    B key, M key, and B+M key as SSD-relevant M.2 keying patterns.

</div>

<style>
.site-subtitle {
  margin-top: -0.8rem;
  font-size: 1.15rem;
  color: var(--md-default-fg-color--light);
}

.terminal-session {
  margin-top: 2rem;
  padding: 1.2rem;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 0.8rem;
  background: rgba(0, 0, 0, 0.18);
}

.terminal-line {
  margin: 1rem 0 0.5rem;
  font-family: var(--md-code-font);
  font-size: 0.95rem;
}

.terminal-line.user {
  color: var(--md-accent-fg-color);
}

.terminal-line.agent {
  color: var(--md-default-fg-color--light);
}
</style>

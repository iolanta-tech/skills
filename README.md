# nanopublishing

![Europa and Jupiter](docs/assets/images/europa-and-jupiter.png)

Skills for building nanopublications from Markdown with coding agents.

Published docs: https://nanopublishing.iolanta.tech/

## Install The Skills

```bash
npx skills add https://github.com/iolanta-tech/nanopublishing --skill '*' -a claude-code
```

## Workflow

Start with `/semantify` (or `$semantify`, for Open AI Codex) on an existing Markdown file. Then use `$nanopublish` when the frontmatter is ready.

## Alternatives

| Tooling | Language(s) | Starting point |
| --- | --- | --- |
| [`iolanta-tech/nanopublishing`](https://github.com/iolanta-tech/nanopublishing) | Markdown, YAML-LD | Markdown document |
| [`knowledgepixels/nanopub-agent-utilities`](https://github.com/knowledgepixels/nanopub-agent-utilities) | TriG, SPARQL | Existing nanopublication or query nanopublication |

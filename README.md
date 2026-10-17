# SDD overview

A readable team guide to Spec-Driven Development with Spec-Kit, prepared for GitHub Pages.

- **[guide.md](guide.md)** — cleaned Markdown source, including three repaired Mermaid diagrams.
- **[index.html](index.html)** — generated static HTML page, with section navigation, responsive tables, and print styles.
- **assets/** — page styles and optional Mermaid rendering.

The original OCR text was cleaned for spelling, formatting, tables, and diagram syntax. Its team-specific workflow, worker names, and approval policies are retained as examples; this is not a verification of the current Spec-Kit API.

## Read locally

Open `index.html` directly to read the guide. For the full experience, including diagram rendering, serve the repository:

```sh
python3 -m http.server 8000
```

Visit <http://localhost:8000>. Mermaid loads from a pinned public CDN and needs internet access. If it cannot load, each diagram remains available as readable source. The guide content itself requires neither JavaScript nor a network connection.

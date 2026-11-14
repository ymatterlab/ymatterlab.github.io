
## License

This repository contains both **source code** and **website content**.

- Source code is licensed under the MIT License (see LICENSE file) as the [hugo-academic-lab-template](https://github.com/ymatterlab/hugo-academic-lab-template). If you like this website design, we suggest you clone the original template [hugo-academic-lab-template](https://github.com/orgs/ymatterlab/repositories)
- Website content (text, images, figures) is licensed under:
  Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0),
  unless otherwise stated

Third-party materials may be subject to separate copyrights.

## Contributing

We welcome contributions to this website, but please note the following policy:

### 👥 Eligibility
In principle, contributions are limited to **current and former members of Y-Matter Lab**.  
This ensures consistency with the lab’s research activities, communication style, and scientific direction.

If you are not a member but believe you have a relevant contribution, feel free to open an issue to discuss it first.

---

### 🔧 How to Contribute

1. **Fork the repository**
   - Click the “Fork” button on GitHub and clone your fork locally.

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name

3. **Make your changes**
   - Keep changes focused and minimal.
   - Follow the existing structure and style of the site.

4. **Test locally**
   - Ensure the site builds and renders correctly. Follow README.md [hugo-academic-lab-template](https://github.com/ymatterlab/hugo-academic-lab-template) about running locally.
   - Check links, formatting, and responsiveness if applicable.

5. **Submit a Pull Request (PR)**
   - Provide a clear description of what you changed and why.
   - Reference any related issues if applicable.
## Content and local preview

Use Hugo (the deployment workflow pins 0.128.0) and Python with PyYAML installed.
Run `make serve` and open http://localhost:1313, or build with `hugo --minify`.
Work on `develop` or a feature branch; `main` deploys production.

- Home: `content/_index.md` front matter contains the hero, featured papers, labels,
  links, sponsor images and captions. Shared lab identity and research-area cards
  remain in `config.yaml`.
- Research: `data/copy.yaml` → `research_list` contains overview, methods, tools,
  navigation and callout text. `data/research_lines.yaml` contains the three locked
  research lines, figures, captions and DOI selections. Preserve their wording and order.
- Other page labels and shared interface copy: `data/copy.yaml`, grouped by layout.
  Rich copy supports Markdown and inline HTML for scientific subscripts and citations.
- News: `content/news/*.md`; people: `data/people.yaml`; opportunities and fellowships:
  `content/join/_index.md`; remaining page prose: `content/<page>/_index.md`.
- Publications: add DOIs in `pubsrc/publications.dois.txt`, run `make pubs`, and commit
  the generated bibliography and cache. See `pubsrc/README.md`; never edit the generated YAML.

Never stage `my-publicatins/` or other private source material. Keep that directory
in your checkout's `.git/info/exclude` and check `git status` before committing.

## Validation and accessibility

After building, run `python scripts/check_site.py public`. This offline check covers
internal links/anchors, image alt attributes, one H1 and heading order, metadata,
sitemap/robots, and frozen text fingerprints for the Major Research Lines. CI runs it
as well. External URLs are reported without network requests.

For browser checks, install isolated tools and serve a build:

```bash
npm install --prefix /tmp/ymatter-a11y playwright-core @axe-core/playwright
hugo --minify --destination /tmp/ymatter-preview
python -m http.server 8767 --directory /tmp/ymatter-preview
# In a second terminal (set CHROME_PATH if Chrome is elsewhere):
NODE_PATH=/tmp/ymatter-a11y/node_modules AUDIT_BASE=http://127.0.0.1:8767 \
  AUDIT_OUTPUT=/tmp/ymatter-a11y/results.json node scripts/audit_accessibility.cjs
```

The eight main pages passed automated axe WCAG 2.1 A/AA checks during this update.
Keyboard skip/focus, filter states and reduced-motion/pause controls were checked
in Chrome. The viewer test used a local 3Dmol stub; external widgets were blocked
in the audit. Check the real 3D viewer, maps and badges manually before production.
Automated checks alone do not establish full WCAG conformance.

Contrast changes: ORCID icons `#a6ce39` → `#5c7918`; ResearchGate icons `#00a98f`
→ `#007d69`; sunny weather badges `#d97706` → `#b45309`; sponsor credit now uses
`--muted` at 0.75rem instead of translucent gray at 0.45rem. New contrast ratios
are at least 4.86:1. Axe leaves gradient backgrounds for manual review; calculations
at their color endpoints give at least 4.75:1 for normal text. Tool links are
underlined, links/buttons have visible keyboard focus, profile links and news
filters sit outside disclosure summaries, and animation has a pause control and
respects reduced-motion preferences. Research text and existing anchors are preserved.

Search/social metadata uses each page's description and the existing PNG lab logo.
Structured data identifies the lab and its INMA/CSIC parent organizations.

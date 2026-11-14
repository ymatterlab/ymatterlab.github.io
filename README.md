# Y-Matter Lab website

Source of <https://ymatterlab.github.io/>.

## For group members

- **Add news:** follow [docs/adding-news.md](docs/adding-news.md). Use the web editor or
  GitHub.com (no Git needed), or open a
  [News item request](https://github.com/ymatterlab/ymatterlab.github.io/issues/new/choose).
- All edits go to the **`develop`** branch. Yuewen reviews them and merges into `main` to publish.


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

## Browser editing with Pages CMS

1. Open [Pages CMS](https://app.pagescms.org/), sign in with GitHub and install or
   authorize its GitHub App for `ymatterlab/ymatterlab.github.io`. Organization
   owners may need to approve that installation.
2. Select this repository, then explicitly select the **develop** branch in the
   app's branch selector before editing. `.pages.yml` is read per branch; it does
   not set the destination branch. If offered a new config on `main`, switch to
   `develop` rather than creating one there. Protect `main` with a GitHub ruleset
   requiring PRs if you want to enforce this for all editors.
3. Edit news, people, positions/fellowships, Home, Research or shared copy in the
   forms. News uses the archetype's title/draft/categories/body fields plus an
   explicit publication date. Keep existing monthly filenames when editing them;
   new dated filenames are generated automatically. Upload images through Media;
   use group-owned figures, WebP ≤1600 px wide, alt text and DOI/source captions.
4. Save. The CMS creates a commit on the selected branch (`content: update {path}`,
   with matching add/delete/rename templates). Check its branch CI, preview, and
   submit a PR to `main` for a separate review and release.

The locked Major Research Lines are **omitted entirely** from the CMS, including
names, order and detailed wording in `data/research_lines.yaml`. Their heading and
intro are omitted from the copy form too. `settings.content.merge: true` preserves
these unmanaged keys and the Home anchor map on save. Home research-area cards are
separate summaries; editing them does not change the locked Research page.

Publications are deliberately excluded. Add DOIs locally and run `make pubs` so
new records and `pubcache.json` are committed together. CI and deployment continue
using the cache offline, avoiding failures caused by DOI-service network outages.

For a branch preview, open GitHub Actions → **Validate branch website**, select a
successful `develop` run and download **built-website** (available for 14 days).
Extract it and run `python -m http.server 8000 --directory <extracted-folder>`;
open http://localhost:8000. Or check out `develop` and run `make serve`.
CI uploads a preview artifact; it does not publish a branch website.

Configuration references: [Pages CMS setup](https://pagescms.org/docs/quick-start/),
[content schemas](https://pagescms.org/docs/configuration/content/), and
[merge/commit settings](https://pagescms.org/docs/configuration/settings/).
The hosted CMS sign-in/save flow requires a group member's GitHub account and has
not been exercised from this checkout.

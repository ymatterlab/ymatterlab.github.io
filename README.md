
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

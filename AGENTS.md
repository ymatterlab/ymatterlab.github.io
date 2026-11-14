# Working on Y-Matter Lab

- This is a Hugo site, deployed from `main` by `.github/workflows/hugo.yml`.
  Never commit or push directly to `main`. Create a short-lived branch from `main`
  (e.g. `content/...`, `feat/...`, `fix/...`), open a pull request to `main`, check
  CI and the preview artifact, merge, and delete the branch.
- Install Hugo (CI uses 0.128.0) and Python/PyYAML. Preview with `make serve`
  (http://localhost:1313); build with `hugo --minify`. Build before each commit.
  Inspect `git status` before committing; stage explicit paths.
- When upgrading Hugo, update the version in both workflows and the README badge.
- Home copy is in `content/_index.md` front matter. Research overview, methods,
  tool lists and other page/interface labels are in `data/copy.yaml`, grouped by
  layout. Research lines and figures are in `data/research_lines.yaml`.
  Members submit news through `.github/ISSUE_TEMPLATE/news.yml` (guide:
  `docs/adding-news.md`); maintainers publish approved requests in `content/news/` (new files
  `YYYY-MM-DD-slug.md`, categories announcements/honors/output/life), people in `data/people.yaml`, Join Us opportunities
  and fellowships in `content/join/_index.md`, other prose in page Markdown.
  Shared identity/navigation/research-area cards are in `config.yaml`.
- **Locked content:** the Research page's Major Research Lines must keep exactly
  the same names, order, number and wording: Quantum Materials, Information
  Materials, Energy Materials. This includes their descriptions, questions,
  lists, themes and captions. Storage may move; rendered text must not change.
  Keep all existing anchors, including `#methods` and `#methods-tools`.
- Never commit `my-publicatins/` or other private source material. Keep
  `/my-publicatins/` in `.git/info/exclude` for each checkout. Do not stage broadly.
- Publications are generated: add DOIs to `pubsrc/publications.dois.txt`, run
  `make pubs`, and commit the DOI list, `pubsrc/pubcache.json` and generated
  `data/publications.yaml`. Never edit the generated YAML by hand. CI/deploy use
  `python scripts/build_pubs.py --offline`; new DOIs must already be cached.
  Use `pubsrc/publications_overrides.yaml` for field corrections, OA links or
  `hide: true`; `pubsrc/publications_extra.yaml` for non-Crossref/no-DOI records.
  If Crossref has no record, comment out that DOI and add a complete extra record.
  `make check` detects lost OA links; `make links` checks them online;
  `make refresh` deliberately refreshes cached metadata after publication updates.
- Use only the group's own figures, optimized as WebP at ≤1600 px wide, with
  meaningful alt text and a caption citing the source paper and DOI. Do not
  introduce third-party figures without the owner's approval.
- Meet WCAG 2.1 AA: keyboard access, visible focus, meaningful alternatives,
  logical headings, sufficient contrast (4.5:1 normal text; 3:1 large text/UI),
  and reduced-motion support. Run an automated check plus manual keyboard review.
- Keep changes scoped. Preserve the offline publication workflow and production
  deploy behavior; branch previews must not deploy over production.

# How to add news to the Y-Matter Lab website

News appears at <https://ymatterlab.github.io/news/>, and the latest items also show
on the home page. Any group member can propose a news item. Yuewen reviews it before
it goes live.

**Short version:** add one Markdown file to `content/news/` on the **`develop`** branch.
After review, it is merged into `main` and appears on the website a few minutes later.

---

## 1. Choose how to submit

| You are… | Use |
|---|---|
| Comfortable with a web form, no Git | **A. Web editor (Pages CMS)** |
| Happy to edit one file on GitHub.com | **B. GitHub website** |
| Already using Git and Hugo locally | **C. Local Git** |
| Without write access to the repository, or in a hurry | **D. Send a news request** |

To use A, B or C you need a GitHub account with write access to
`ymatterlab/ymatterlab.github.io`. Send your GitHub username to Yuewen to be added.

### A. Web editor (Pages CMS), no Git needed

1. Go to <https://app.pagescms.org/> and sign in with GitHub.
2. Open **ymatterlab/ymatterlab.github.io**, then select the **`develop`** branch in
   the branch selector. Never edit on `main`.
3. Click **News → Add an entry** and fill in:
   - **Title**: short and specific, e.g. *"Jincheng's paper on NTE accepted in PRB"*.
   - **Date**: the date of the event (not a future date, see §3).
   - **Draft**: leave **off** (otherwise the item stays hidden).
   - **Categories**: one or more (see §2).
   - **Body**: one to three sentences with a link.
4. Click **Save**. This creates a commit on `develop`, and the filename is generated
   automatically.
5. Tell Yuewen (email or chat) that the item is ready for review.

### B. On the GitHub website

1. Open <https://github.com/ymatterlab/ymatterlab.github.io/tree/develop/content/news>.
   Make sure the branch shown at the top left is **develop**.
2. Click **Add file → Create new file**.
3. Name it `YYYY-MM-DD-short-title.md`, e.g. `2026-11-20-prb-nte-paper.md`
   (lowercase, hyphens, no spaces).
4. Paste and edit this template:

   ```markdown
   ---
   title: "Jincheng's paper on negative thermal expansion published in PRB"
   date: 2026-11-20
   draft: false
   categories:
     - output
   ---

   Jincheng's work on ... has been published in
   [Physical Review B](https://doi.org/10.xxxx/xxxxx). Congratulations!
   ```

5. Click **Commit changes…**, choose **Commit directly to the `develop` branch**,
   and use a message like `content: add news on PRB paper`.
6. Tell Yuewen that the item is ready for review.

### C. Local Git

```bash
git checkout develop && git pull
hugo new news/2026-11-20-prb-nte-paper.md   # pre-fills title, date and categories
# edit content/news/2026-11-20-prb-nte-paper.md
make serve                                  # preview at http://localhost:1313/news/
git add content/news/2026-11-20-prb-nte-paper.md
git commit -m "content: add news on PRB paper"
git push
```

Stage only your news file (and its image, if any). Never use `git add -A` in a checkout
that contains private folders such as `my-publicatins/`.

### D. Send a news request

Open a [new issue](https://github.com/ymatterlab/ymatterlab.github.io/issues/new/choose)
and choose **News item request**. Alternatively, email the title, date, category,
text, link and image to Yuewen, who will post it.

---

## 2. Writing guidelines

- **Length:** one to three sentences. The news page shows the title and expands to
  the text.
- **Title:** sentence case, specific, without a trailing full stop.
- **Names:** use full names on first mention (e.g. "PhD student Jincheng Yue").
- **Links:** always link the source: the paper's DOI (`https://doi.org/...`), the award
  page, or the event page.
- **Categories:** use only these four, because they power the filter buttons:

  | Category | Use for |
  |---|---|
  | `announcements` | Open positions, new members, relocation, events, invited talks, visits |
  | `honors` | Awards, editorial roles, grants, fellowships |
  | `output` | Published papers, preprints, software releases, datasets |
  | `life` | PhD defenses, group outings, celebrations |

- **Images (optional):** upload to `static/images/news/` (in Pages CMS: **Media**).
  Use WebP or JPEG, at most 1600 px wide and under 300 KB. Add them in the text as
  `![Short description of the image](/images/news/2026-11-20-group-dinner.webp)`.
  The description in square brackets is required: it is read by screen readers.
- **Check before posting:**
  - Do not announce unpublished results, or papers still under embargo.
  - Do not post anything confidential (grant reviews, refereeing, internal matters).
  - Get the consent of everyone recognizable in a photo.
  - Use only figures the group owns. Cite the paper and DOI in the caption.

## 3. What happens after you submit

1. GitHub automatically builds the site from `develop` (**Actions → Validate branch
   website**). A green ✓ means it works, a red ✗ means there is an error (usually a
   typo in the `---` header). Fix it or ask for help.
2. Yuewen reviews the change and merges `develop` into `main`.
3. The site is redeployed automatically and the news is live within a few minutes.

**Why isn't my news showing?** Check that:

- `draft` is `false`;
- the `date` is not in the future (Hugo hides future-dated pages until that date has
  passed *and* the site is rebuilt);
- the header starts and ends with a line containing only `---`;
- the change has been merged into `main` (items on `develop` are not public yet).

## 4. Editing or removing an item

Edit the same file in `content/news/` on `develop` (in Pages CMS, open it from the
News list). To remove an item, delete the file or set `draft: true`. The change goes
live after the next merge into `main`.

Older items use one file per month (e.g. `2026-09.md`). Keep their names when editing.
New items use `YYYY-MM-DD-short-title.md` so that several items per month are possible.

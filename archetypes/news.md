---
title: "{{ replaceRE `^\d{4}-\d{2}(-\d{2})?-?` "" .Name | replaceRE "-" " " | title }}"
date: {{ now.Format "2006-01-02" }}
draft: false
# Pick one or more: announcements, honors, output, life
#   announcements: positions, arrivals/relocation, events, talks, visits
#   honors:        awards, editorial roles, grants, fellowships
#   output:        papers, preprints, software, datasets
#   life:          defenses, group outings, celebrations
categories:
  - output
---

Write one to three short sentences: who, what, and why it matters. Link the paper
(DOI), award or event page. Full guide: docs/adding-news.md

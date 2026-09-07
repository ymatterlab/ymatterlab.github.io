# 出版物列表怎么更新

网站上的出版物列表由 `data/publications.yaml` 渲染，**这个文件是自动生成的，不要手改**。
标题、作者、期刊、年月、卷期页、开放获取 PDF 链接全部由脚本从 Crossref 和 Unpaywall
抓取。需要维护的只有本目录下的 DOI 清单。

## 发表了新论文

```bash
echo "10.1038/s41467-XXX-XXXXX-X" >> pubsrc/publications.dois.txt
make pubs          # 或 python scripts/build_pubs.py
make serve         # 本地看一眼 http://localhost:1313/publications/
git add -A && git commit -m "Add <期刊> <年份>" && git push
```

`make pubs` 只会抓新增的 DOI，已有条目走 `pubsrc/pubcache.json` 缓存，不联网。

## 这个目录里都是什么

| 文件 | 作用 |
|---|---|
| `publications.dois.txt` | **唯一要手动维护的文件**，每行一个 DOI |
| `publications_extra.yaml` | 没有 DOI、或 DOI 不由 Crossref 注册的条目，手写完整信息 |
| `publications_overrides.yaml` | 按 DOI 覆盖个别字段，或用 `hide: true` 隐藏某条 |
| `pubcache.json` | 抓取结果缓存，**必须提交进 git**，CI 构建靠它 |

这些文件放在 `pubsrc/` 而不是 `data/`，因为 Hugo 会试图解析 `data/` 下的每个文件，
`.txt` 不是它认识的格式，放进去整个站点就构建失败。

## 会遇到的几种情况

**`error: Crossref has no record for <DOI>`**
该 DOI 不由 Crossref 注册（中文期刊常见）。把那行 DOI 在清单里注释掉，
到 `publications_extra.yaml` 里手写一条完整记录，格式照抄已有的两条。

**某篇不想显示**（比如会议摘要、重复收录的 ChemInform 条目）
在 `publications_overrides.yaml` 里写：

```yaml
10.1002/chin.201631291:
  hide: true
```

**开放获取链接缺失或失效**

```bash
make check      # 对比上次提交，列出变少的链接
make links      # 逐个访问，找出打不开的
```

要手动补链接，在 `publications_overrides.yaml` 里写：

```yaml
10.1103/PhysRevB.95.014111:
  free_full_text_url: "https://arxiv.org/pdf/1610.xxxxx"
  free_full_text_source: "arXiv"
```

**在线发表时是 in press，后来有了正式卷期页**

```bash
make refresh    # 忽略缓存重抓全部，几分钟
```

## GitHub Actions 那边

`.github/workflows/hugo.yml` 里会用 `--offline` 再跑一次脚本，只读缓存、不联网。
所以线上部署永远不会因为 Crossref 抽风而失败；反过来说，
**如果你加了 DOI 却忘了在本地跑脚本、或没提交 `pubcache.json`，CI 会直接报错**，
这是有意为之——宁可构建失败，也不要悄悄发布一份过期的列表。

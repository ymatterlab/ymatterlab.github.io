# 出版物列表的日常操作。不确定该敲什么命令时，先看 pubsrc/README.md。

.PHONY: pubs check serve refresh links

pubs:            ## 抓取新 DOI，重新生成 data/publications.yaml
	python scripts/build_pubs.py

check:           ## 对比上一次提交，看开放获取链接有没有变少
	python scripts/check_fulltext.py --against HEAD

links:           ## 逐个访问开放获取链接，检查是否失效
	python scripts/check_fulltext.py --check-links

refresh:         ## 忽略缓存，重新抓取全部条目（卷期页更新后用）
	python scripts/build_pubs.py --refresh

serve: pubs      ## 本地预览
	hugo server -D

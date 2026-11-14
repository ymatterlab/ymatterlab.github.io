#!/usr/bin/env python3
"""Check built HTML, internal targets, SEO and the frozen research-line text.

Usage: python scripts/check_site.py [public-directory]
External links are counted but never requested, keeping CI independent of networks.
"""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
LOCKED = ['quantum-materials', 'information-materials', 'energy-materials']


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.stack, self.headings, self.links, self.errors = [], [], [], []
        self.ids, self.regions, self.active = set(), {}, {}
        self.meta, self.canonical, self.main = set(), False, False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        ident = attrs.get('id')
        if ident:
            if ident in self.ids:
                self.errors.append(f'duplicate ID: {ident}')
            self.ids.add(ident)
        region = ident if ident in LOCKED else ('index' if 'rl-index' in attrs.get('class', '').split() else None)
        if region:
            self.regions[region] = []
            self.active[region] = len(self.stack)
        if re.fullmatch(r'h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('image without alt')
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.links.append(attrs[attr])
        if tag == 'meta':
            self.meta.add(attrs.get('name', attrs.get('property')))
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = bool(attrs.get('href'))
        if tag == 'main' and ident == 'main':
            self.main = True
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag not in self.stack:
            return
        depth = len(self.stack) - 1 - self.stack[::-1].index(tag)
        for region, start in list(self.active.items()):
            if depth <= start:
                del self.active[region]
        self.stack = self.stack[:depth]

    def handle_data(self, text):
        if any(tag in self.stack for tag in ('script', 'style')):
            return
        for region in self.active:
            self.regions[region].append(text)

    def fingerprints(self):
        return {key: hashlib.sha256(re.sub(r'\s+', ' ', ' '.join(value)).strip().encode()).hexdigest()
                for key, value in self.regions.items()}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else 'public').resolve()
    pages = {p.resolve(): Page(p.read_text()) for p in root.rglob('*.html')}
    assert pages, f'No HTML under {root}'
    errors, external = [], set()
    required = {'description', 'og:title', 'og:description', 'og:url', 'og:image',
                'twitter:card', 'twitter:title', 'twitter:description', 'twitter:url', 'twitter:image'}
    for path, page in pages.items():
        label = str(path.relative_to(root))
        errors.extend(f'{label}: {message}' for message in page.errors)
        if page.headings.count(1) != 1:
            errors.append(f'{label}: expected one h1')
        if any(b > a + 1 for a, b in zip(page.headings, page.headings[1:])):
            errors.append(f'{label}: skipped heading level')
        if not page.main or not page.canonical or required - page.meta:
            errors.append(f'{label}: missing main target, canonical or metadata')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme in ('mailto', 'tel', 'data', 'javascript'):
                continue
            if url.netloc and url.netloc != 'ymatterlab.github.io':
                external.add(link)
                continue
            target = root / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)
            if not url.path:
                target = path
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            if not target.is_file():
                errors.append(f'{label}: missing internal target {link}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{label}: missing internal anchor {link}')
    expected = json.loads(Path(__file__).with_name('research-lines.sha256.json').read_text())
    research = pages[root / 'research/index.html']
    if research.fingerprints() != expected:
        errors.append('Locked Major Research Lines differ from the original rendered baseline')
    if list(research.regions) != ['index', *LOCKED]:
        errors.append('Locked research-line order changed')
    for name in ('sitemap.xml', 'robots.txt'):
        if not (root / name).is_file():
            errors.append(f'missing {name}')
    print(f'Checked {len(pages)} HTML pages; {len(external)} external URLs not requested (offline check).')
    for error in errors:
        print(f'ERROR: {error}')
    if errors:
        return 1
    print('Internal links, headings, image alternatives, metadata and locked research text passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

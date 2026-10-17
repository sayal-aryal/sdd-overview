#!/usr/bin/env python3
"""Render guide.md to a portable static page using only Python's standard library.

Supports the headings, paragraphs, lists, tables, inline code/emphasis, and Mermaid
fences used by this guide. Run again after editing the Markdown source.
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent


def inline(text):
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def render(source):
    lines = source.splitlines()
    output, navigation = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('```'):
            language = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            if language != 'mermaid':
                raise ValueError(f'Unsupported code fence: {language}')
            output.append('<figure class="diagram"><pre class="mermaid">' + html.escape('\n'.join(code)) + '</pre><figcaption>Workflow diagram · scroll horizontally to explore</figcaption></figure>')
        elif line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title = line[level:].strip()
            if level == 1:
                i += 1
                continue
            anchor = slug(title)
            output.append(f'<h{level} id="{anchor}">{inline(title)}</h{level}>')
            if level == 2:
                navigation.append(f'<a href="#{anchor}">{inline(title)}</a>')
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [cell.strip() for cell in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell) for cell in cells):
                    rows.append(cells)
                i += 1
            head = '<thead><tr>' + ''.join(f'<th scope="col">{inline(c)}</th>' for c in rows[0]) + '</tr></thead>'
            body = '<tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in row) + '</tr>' for row in rows[1:]) + '</tbody>'
            output.append('<div class="table-wrap" role="region" aria-label="Guide reference table" tabindex="0"><table>' + head + body + '</table></div>')
            continue
        elif re.match(r'(- |\d+\. )', line):
            ordered = bool(re.match(r'\d+\. ', line))
            tag = 'ol' if ordered else 'ul'
            items = []
            pattern = r'\d+\. ' if ordered else r'- '
            while i < len(lines) and re.match(pattern, lines[i]):
                items.append('<li>' + inline(re.sub(r'^' + pattern, '', lines[i])) + '</li>')
                i += 1
            output.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
            continue
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|- |\d+\. )', lines[i]):
                paragraph.append(lines[i])
                i += 1
            output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            continue
        i += 1
    return '\n'.join(output), '\n'.join(navigation)


body, nav = render((ROOT / 'guide.md').read_text())
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A practical team guide to spec-driven development: Spec-Kit, lifecycle hooks, skills, specialist agents, and human review.">
<title>A Team Guide to Spec-Driven Development</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#guide">Skip to guide</a>
<header class="topbar"><a class="brand" href="#"><span class="brand-mark">S</span> SDD <span class="muted">/ Team handbook</span></a><a class="source" href="guide.md">Markdown source ↗</a></header>
<div class="layout">
<aside><div class="sidebar-title">IN THIS GUIDE</div><nav aria-label="Guide sections">NAVIGATION</nav><div class="sidebar-note">The process, from a shared understanding to verified delivery.</div></aside>
<main id="guide">
<div class="hero"><div class="eyebrow">THE ENGINEERING PLAYBOOK</div><h1>A team guide to<br><span>spec-driven development.</span></h1><p class="dek">Make intent explicit. Keep delivery traceable.<br>Build with Spec-Kit, skills, and specialist agents.</p><div class="tags"><span>6 chapters</span><span>12 lifecycle stages</span><span>Human-led decisions</span></div></div>
<article>CONTENT</article>
<footer>Built around shared intent, reviewable artifacts, and evidence.<a href="#">Back to top ↑</a></footer>
</main></div>
<script type="module" src="assets/diagrams.js"></script>
</body>
</html>
'''.replace('NAVIGATION', nav).replace('CONTENT', body)
(ROOT / 'index.html').write_text(page)
print('Built index.html from guide.md')

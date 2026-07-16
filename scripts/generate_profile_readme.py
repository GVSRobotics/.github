import re
import json
import urllib.request
import html

ORG = 'GVSRobotics'
API = f'https://api.github.com/orgs/{ORG}/repos?per_page=200'
HEADERS = {'Accept':'application/vnd.github+json','User-Agent':'Mozilla/5.0'}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

def url_ok(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception:
        return False

def first_image_in_readme(org, repo, branch):
    raw_readme = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/README.md'
    try:
        req = urllib.request.Request(raw_readme, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='ignore')
    except Exception:
        return None
    # markdown image ![alt](url)
    m = re.search(r'!\[[^\]]*\]\(([^)]+)\)', text)
    if m:
        url = m.group(1).strip()
        if url.startswith('http'):
            return url
        candidate = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/{url.lstrip("/")}'
        if url_ok(candidate):
            return candidate
    # html <img src="...">
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', text)
    if m:
        url = m.group(1).strip()
        if url.startswith('http'):
            return url
        candidate = f'https://raw.githubusercontent.com/{org}/{repo}/{branch}/{url.lstrip("/")}'
        if url_ok(candidate):
            return candidate
    return None

cand_names = [
    'logo.png','logo.jpg','logo.svg','screenshot.png','screenshot.jpg','screenshot.jpeg','screenshot.svg',
    'hero.png','hero.jpg','hero.svg','assets/hero.png','assets/hero.jpg','assets/logo.png','images/logo.png','docs/hero.png'
]

def generate():
    repos = fetch_json(API)
    repos_sorted = sorted(repos, key=lambda r: r.get('stargazers_count',0), reverse=True)
    blocks = []
    for r in repos_sorted:
        name = r['name']
        desc = r.get('description') or ''
        branch = r.get('default_branch') or 'main'
        repo_url = r.get('html_url')
        stars = r.get('stargazers_count', 0)
        language = r.get('language') or ''
        image = None
        # try candidate files
        for p in cand_names:
            raw = f'https://raw.githubusercontent.com/{ORG}/{name}/{branch}/{p}'
            if url_ok(raw):
                image = raw
                break
        # try README first image
        if image is None:
            image = first_image_in_readme(ORG, name, branch)

        # fall back to GitHub OpenGraph card
        if image is None:
            image = f'https://opengraph.githubassets.com/1/{ORG}/{name}'

        title = html.escape(name)
        desc_html = html.escape(desc)
        # card HTML for a single repo
        card = []
        card.append(f'<div style="padding:6px">')
        card.append(f'<a href="{repo_url}"><img src="{image}" alt="{title}" style="max-width:100%;height:auto;border:1px solid #e1e4e8;border-radius:6px;"/></a>')
        card.append(f'<p><strong><a href="{repo_url}">{title}</a></strong><br/>')
        if desc_html:
            card.append(f'{desc_html}<br/>')
        meta = []
        if language:
            meta.append(f'`{language}`')
        if stars:
            meta.append(f'⭐ {stars}')
        if meta:
            card.append(' '.join(meta))
        card.append('</p>')
        card.append('</div>')
        blocks.append('\n'.join(card))

    out = '# GVSRobotics — Projects\n\nThis page highlights public repositories under the GVSRobotics organization.\n\n'
    # Render blocks in a two-column HTML table
    out += '<table><tbody>\n'
    for i in range(0, len(blocks), 2):
        left = blocks[i]
        right = blocks[i+1] if i+1 < len(blocks) else ''
        out += f'<tr>\n<td style="vertical-align:top; width:50%; padding:8px">{left}</td>\n<td style="vertical-align:top; width:50%; padding:8px">{right}</td>\n</tr>\n'
    out += '</tbody></table>\n\n'

    out += '\n**How to update**\n\nEdit `profile/README.md` in the `.github` repo and push to `main`. The org page will reflect changes shortly.\n'

    with open('profile/README.md','w',encoding='utf-8') as f:
        f.write(out)

    print('Wrote profile/README.md with', len(blocks), 'repos')

if __name__ == '__main__':
    generate()

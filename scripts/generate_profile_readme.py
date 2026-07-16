import re
import json
import urllib.request

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
        # relative path
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

repos = fetch_json(API)
repos_sorted = sorted(repos, key=lambda r: r.get('stargazers_count',0), reverse=True)
blocks = []
for r in repos_sorted:
    name = r['name']
    desc = r.get('description') or ''
    branch = r.get('default_branch') or 'main'
    repo_url = r.get('html_url')
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
    md = ''
    if image:
        md += f'![{name}]({image})\n\n'
    md += f'### [{name}]({repo_url})\n\n'
    md += f'{desc}\n\n' if desc else '\n'
    blocks.append(md)

out = '# GVSRobotics — Projects\n\nThis page highlights public repositories under the GVSRobotics organization.\n\n'
for b in blocks:
    out += f'{b}---\n\n'

out += '\n**How to update**\n\nEdit `profile/README.md` in the `.github` repo and push to `main`. The org page will reflect changes shortly.\n'

with open('profile/README.md','w',encoding='utf-8') as f:
    f.write(out)

print('Wrote profile/README.md with', len(blocks), 'repos')

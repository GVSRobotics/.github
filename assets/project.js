async function renderProject() {
  const root = document.querySelector('[data-project]');
  const slug = root.dataset.project;
  const response = await fetch('../projects.json');
  const projects = await response.json();
  const p = projects.find(item => item.slug === slug);
  if (!p) throw new Error(`Unknown project: ${slug}`);
  document.title = `${p.name} | GVS Robotics`;
  document.documentElement.style.setProperty('--accent', p.accent);
  document.querySelector('[data-name]').textContent = p.name;
  document.querySelector('[data-kicker]').textContent = p.kicker;
  document.querySelector('[data-summary]').textContent = p.description;
  document.querySelector('[data-body]').innerHTML = `<p>${p.body}</p><h3>What it provides</h3><ul>${p.features.map(x => `<li>${x}</li>`).join('')}</ul>`;
  document.querySelector('[data-links]').innerHTML = p.links.map((link, i) => `<a class="button ${i === 0 ? 'primary' : 'secondary'}" href="${link.url}">${link.label} ↗</a>`).join('');
  document.querySelector('[data-facts]').innerHTML = p.facts.map(f => `<div class="fact"><small>${f.label}</small><strong>${f.value}</strong></div>`).join('');
}
renderProject().catch(err => { document.querySelector('[data-project]').innerHTML = `<p>${err.message}</p>`; });

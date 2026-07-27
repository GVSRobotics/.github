const grid = document.querySelector('#project-grid');
if (grid) {
  fetch('projects/projects.json')
    .then(r => { if (!r.ok) throw new Error('Could not load projects'); return r.json(); })
    .then(projects => {
      grid.innerHTML = projects.map((p, i) => {
        const external = /^https?:\/\//.test(p.cardHref);
        return `
        <a class="project-card reveal" href="${p.cardHref}" ${external ? 'target="_blank" rel="noopener noreferrer"' : ''} style="--accent:${p.accent}">
          <div class="meta"><span class="tag">${p.language}</span><span>${String(i + 1).padStart(2, '0')}</span></div>
          <h3>${p.name}</h3>
          <p>${p.shortDescription}</p>
          <span class="card-link">${external ? 'View on GitHub →' : 'View project →'}</span>
        </a>`;
      }).join('');
      reveal();
    })
    .catch(() => { grid.innerHTML = '<p>Project information is temporarily unavailable.</p>'; });
}

document.querySelector('#year')?.append(new Date().getFullYear());
function reveal(){
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if(entry.isIntersecting){ entry.target.classList.add('visible'); observer.unobserve(entry.target); }
  }), {threshold:.12});
  document.querySelectorAll('.reveal:not(.visible)').forEach(el => observer.observe(el));
}
reveal();

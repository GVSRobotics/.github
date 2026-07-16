const organizationName = "GVSRobotics";
const membersGrid = document.getElementById("members-grid");
const reposGrid = document.getElementById("repos-grid");

function renderMembers(members) {
  if (!membersGrid) return;

  if (!Array.isArray(members) || members.length === 0) {
    membersGrid.innerHTML = "<p>No public organization members are currently listed by GitHub.</p>";
    return;
  }

  membersGrid.innerHTML = members
    .map(
      (member) => `
        <article class="card">
          <h3>${member.login}</h3>
          <p>Organization member</p>
          <a href="${member.html_url}" target="_blank" rel="noreferrer">View GitHub profile</a>
        </article>
      `
    )
    .join("");
}

async function loadMembers() {
  if (!membersGrid) return;

  membersGrid.innerHTML = "<p>Loading members…</p>";

  try {
    const response = await fetch(`https://api.github.com/orgs/${organizationName}/members?per_page=100`);
    if (!response.ok) throw new Error("Unable to load organization members from GitHub.");

    const members = await response.json();
    renderMembers(members);
  } catch (error) {
    membersGrid.innerHTML = `<p>${error.message}</p>`;
  }
}

async function loadRepositories() {
  if (!reposGrid) return;

  reposGrid.innerHTML = "<p>Loading repositories…</p>";

  try {
    const response = await fetch(`https://api.github.com/orgs/${organizationName}/repos?per_page=100`);
    if (!response.ok) throw new Error("Unable to load repositories from GitHub.");

    const repositories = await response.json();

    if (!Array.isArray(repositories) || repositories.length === 0) {
      reposGrid.innerHTML = "<p>No public repositories are currently available.</p>";
      return;
    }

    reposGrid.innerHTML = repositories
      .sort((a, b) => (b.stargazers_count || 0) - (a.stargazers_count || 0))
      .map(
        (repo) => `
          <article class="card">
            <h3>${repo.name}</h3>
            <p>${repo.description || "No description provided yet."}</p>
            <a href="${repo.html_url}" target="_blank" rel="noreferrer">View repository</a>
          </article>
        `
      )
      .join("");
  } catch (error) {
    reposGrid.innerHTML = `<p>${error.message}</p>`;
  }
}

loadMembers();
loadRepositories();

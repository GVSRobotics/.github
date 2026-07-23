# GVS Robotics website

Static GitHub Pages site for the GVS Robotics organization.

## Add it to `GVSRobotics/.github`

Copy all files in this package into the repository root **without deleting the existing `profile/` folder**.

Then open repository **Settings → Pages** and select:

- Source: **Deploy from a branch**
- Branch: **main**
- Folder: **/ (root)**

Because the repository is named `.github`, the default project-site URL will normally be:

`https://gvsrobotics.github.io/.github/`

For the cleaner organization URL `https://gvsrobotics.github.io/`, use a repository named `GVSRobotics.github.io` instead. The same files work there unchanged.

## Add a new project

1. Open `projects/projects.json`.
2. Duplicate one project object and edit its fields. Give it a unique lowercase `slug`, such as `new-project`.
3. Copy `projects/_template/` to `projects/new-project/`.
4. In the copied `index.html`, replace `PROJECT_SLUG` with `new-project`.
5. Commit and push. The landing-page card and project page will both appear automatically.

### Project data fields

- `slug`: URL folder name
- `name`: display name
- `language`: badge text
- `accent`: CSS color
- `shortDescription`: landing-page card text
- `kicker`, `description`, `body`: project page copy
- `features`: bullet list
- `links`: project buttons
- `facts`: three compact facts at the bottom

## Local preview

From this folder, run:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

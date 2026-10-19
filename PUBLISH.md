# Publishing the user guide

The user approved publishing ("publish the docs site", 2026-10-19). Nothing is published until the steps below run.

## What goes public
Only the contents of `Docs/Site`: the guide's Markdown pages, `_config.yml`, the writer notes (`README.md`,
`_template.md`, this file) and `_tools/package_docs.py`. **No plugin code, no other VoxelKit folders, no textures or
source art.** The writer notes are excluded from the website but visible in the repository.

## Pre-publish checklist (done 2026-10-19)
- [x] SuperVoxel names on every page (code rename 821401b).
- [x] Only committed features are described; unbounded worlds (in testing) are marked "coming" in the title, a note
      at the top of the page and every link to it.
- [x] No dead Fab link: the footer and home page say "Coming soon to Fab"; the Fab link is added once the listing
      exists.
- [x] "Edit this page" points at `https://github.com/TheVirusHimself/supervoxel-docs`; `url` and `baseurl` are set for
      `https://thevirushimself.github.io/supervoxel-docs/`.
- [x] Support page: the support email is set; the tracker and reply time are announced with the Fab release.
- [x] Screenshot placeholders removed (the Blueprint node chains stay as text).
- [x] Checks pass: no other games or products named, no private paths or emails (one allowed exception: the
      buyer support address ocozdemir@gmail.com on the support page and in the footer, set by the user), no `{{ }}` left in pages, every
      internal link resolves, every page has front matter.

## Steps
1. On GitHub, create a **public** repository named `supervoxel-docs` under the user's account. Leave it empty (no
   README, licence or .gitignore).
2. (Done in the config: the repository is `TheVirusHimself/supervoxel-docs`.)
3. Push only `Docs/Site`, as the repository's root, **without history** (the history has older drafts):
   ```
   mkdir supervoxel-docs-push
   cp -r "<VoxelKit>/Docs/Site/." supervoxel-docs-push/
   cd supervoxel-docs-push
   git init -b main
   git add -A
   git commit -m "SuperVoxel user guide"
   git remote add origin https://github.com/TheVirusHimself/supervoxel-docs.git
   git push -u origin main
   ```
   Check before pushing that the folder holds only the guide (`git status` lists Markdown, `_config.yml` and
   `_tools/package_docs.py`).
4. In the repository: Settings > Pages > Build and deployment > Source = **Deploy from a branch**, Branch = **main**,
   folder **/ (root)**. Save.
5. Wait for the Pages build (the Actions tab). The site appears at `https://TheVirusHimself.github.io/supervoxel-docs/`.
6. Later: set that address as the Fab listing's documentation link and in the plugin's `.uplugin` `DocsURL`.

## Updating later
Copy `Docs/Site` over the clone of `supervoxel-docs` (keep its `.git` folder), commit and push. GitHub rebuilds the
site on every push. Run the checks in the checklist again first.

# About this guide (for writers)

This folder is the SuperVoxel user guide: the Markdown pages are both the manual and the website (a GitHub
Pages Jekyll site with the just-the-docs theme). There is one source; nothing else is a copy to keep in step. One
session owns it, and nobody else edits it. Send API facts and corrections to the guide's owner instead.

**Rules**

- Thorough but simple: cover every feature, setting, Blueprint node, C++ entry point, event and error, in plain
  language and short sentences.
- Task first: lead with "How do I...?", then the reference.
- Every feature page has the same shape (see `_template.md`).
- Every snippet matches the real code in the plugin's `Source` folder. Never guess an API: if a fact isn't
  confirmed, the page says "coming" instead.
- Only the product's own terms. No other games or products are named. No private paths or email addresses.
- The seller is Onur C Ozdemir.

**Site layout**

- Every page starts with front matter: `title`, `nav_order`, and `parent` for pages under Features or Reference.
- Navigation order: Home, Quick start, Install and upgrade, Concepts, Features, Example character, Reference,
  Performance, FAQ, Support, Changelog.
- Links between pages are relative `.md` links; GitHub's build turns them into page links.
- A new feature page: add it under `features/` with `parent: Features` and the next `nav_order`.
- Writer files (`README.md`, `_template.md`, `PUBLISH.md`) and `_tools/` are excluded from the site.

**Status markers:** each page carries a hidden `<!-- Status: ... -->` line: `planned` (stub), `draft` (written,
waiting for a code check) or `checked against <commit>` (every snippet and default verified).

**Packaging (owned by the guide's owner):** before each package run
`python Docs/Site/_tools/package_docs.py`. It copies the pages into the plugin's `Docs/Manual` folder without front
matter or writer files. Check that `Config/FilterPlugin.ini` ships `Docs/`.

**Publishing:** see `PUBLISH.md`. It needs the user's OK.

**Backlog (from the docs analysis, `Docs/Research/DocsAnalysis.md`)**

- Real screenshots with alt text, at one size and theme (needs the editor).
- Blueprint graphs as images plus UE's copy-paste node text in a code block (needs the editor).
- An API reference generated from the headers, one page per class, with a packaging check that fails when a
  documented node no longer exists.
- A 2–3 minute quick-start video and a playable demo build (needs the user's OK to publish).
- "Since 1.x" tags on new settings, and a version selector once there's more than one version.

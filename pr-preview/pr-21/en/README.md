# Homepage for the AIST Research Group

[Jekyll](https://jekyllrb.com/) website for the **AIST – Advanced Information Systems and Technology** research group at the University of Applied Sciences Upper Austria, Campus Hagenberg.

The site is built with Jekyll and deployed to GitHub Pages through a GitHub Actions workflow (see [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)). The site is bilingual (German / English) using [jekyll-polyglot](https://github.com/untra/polyglot), and static full-text search is provided by [Pagefind](https://pagefind.app/).

**❗💥 Warning: Pushing to `main` triggers a deployment — changes go live shortly after! 💥❗**

Please test considerable changes in a local setup first.

## Local Development

### Prerequisites

- [Git](https://git-scm.com/) with [Git LFS](https://git-lfs.com/) (all images are
  tracked via LFS — see [Images & Git LFS](#images--git-lfs))
- [Ruby](https://www.ruby-lang.org/)

### Install Git and Clone the Repository

Get Git from [https://git-scm.com/](https://git-scm.com/) (or
[GitHub Desktop](https://desktop.github.com/)), then make sure Git LFS is enabled:

```bash
git lfs install
```

Clone the repository to your local machine:

```bash
git clone https://github.com/FHOOEAIST/aist.github.io.git
cd aist.github.io
```

## Install Bundler and Jekyll

```bash
gem install bundler # Install Bundler (if not already installed)
bundle install
```

## Start the Build System

Start the local development server with:

```bash
bundle exec jekyll serve
```

The site is then available at [http://127.0.0.1:4000/aist.github.io/](http://127.0.0.1:4000/aist.github.io/). Changes to Markdown and HTML files
are picked up automatically.

The Pagefind search index is **not** built by jekyll, so the search UI will be empty
locally. To try it locally you can run, after a build:

```bash
npx pagefind --site _site # or bunx if bun is preferred
```

# Internationalization

The site is bilingual via `jekyll-polyglot`, with **German as the default language** and English as the secondary language.

Conventions:
- **Collections** (`_posts`, `_projects`, `_publications`, `_theses`) are split into `de/` and `en/` subdirectories. Each file carries a `lang:` field.
- **Top-level pages** exist as a German version (`page.html`) and an English version (`page-en.html`).
- Translations of the *same* content are linked by a shared `page_id` (e.g. `news:my-post`, `projects:bambi`, `pub:...`, `thesis:...`). The language switcher uses this to jump between the DE and EN versions.

## Design Variants

Two complete designs live side by side; `site_design` in `_config.yml` picks the one that is built:

```yaml
site_design: tiles   # light layout with the square tile mosaic (fh-ooe.at style)
site_design: waves   # dark navy header and the animated wave hero
```

Only the value has to change – content, collections and page front matter are shared by both variants. See `CLAUDE.md` (Design variants) for the files involved.

## News Posts

Blog-style news entries shown on the news page.

- **Location:** `_posts/{de,en}/YYYY-MM-DD-title.md`

```yaml
---
lang: de
title: Some News Post
date: 2024-09-07T11:05:15+02:00 # Optional, overrides the date in the filename
page_id: news:some-news-post
title_image: /assets/images/news/example_title.jpg
---

Markdown body of the news post...
```

## Projects

Project showcases. These appear in the project carousels on the home page (filtered by `category`) and on the projects listing (split into active / completed based on the end date).

- **Location:** `_projects/{de,en}/slug.md`

```yaml
---
lang: de
title: Bambi
logo: /assets/images/projects/Bambi_logo.png
background: /assets/images/projects/Bambi_background.jpg
category: cv            # ehealth | ml | cv
page_id: projects:bambi
permalink: /projects/bambi/  # optional
projects:
  - title: Bambi
    laufzeitStart: 01.04.2022   # DD.MM.YYYY
    laufzeitEnd: 30.04.2025
    partner: FH OÖ Media Interaction Lab, ...
    foerdergeber: Österreichische Forschungsförderungsgesellschaft FFG – AI4Green
    dissertant: <optional>
  - title: Bambi 2
    laufzeitStart: 01.05.2025
    laufzeitEnd: 30.04.2028
    partner: FH OÖ Media Interaction Lab, ...
    foerdergeber: Österreichische Forschungsförderungsgesellschaft FFG – AI4Green
    dissertant: <optional>
eu_funded: true         # optional: shows the official "Funded by the European Union" emblem after the text
---

Markdown description for Bambi...

---

Markdown description for Bambi 2...
```


> The `project` layout splits the Markdown body on `---` and
> pairs each section with the corresponding entry in the `projects` list. This lets a
> single file describe multi-phase projects. The listing uses `laufzeitEnd`
> to decide whether a project is still active.

### Ordering

Both sections of the projects listing (active and completed) are sorted
alphabetically and case-insensitively. A leading `Projekt ` / `Project ` (with or
without a colon) is **ignored** for sorting, so `Projekt Wildschwein` sorts under
W rather than lumping every such project together under P. That key is computed
in [`_plugins/project_sort_title.rb`](_plugins/project_sort_title.rb) as
`sort_title`; nothing needs to be added to a project's front matter.

## Research Areas

Each research area has its own page (DE + EN, shared `page_id: area:<id>`): `forschung-ehealth.md`, `forschung-ml.md`, `forschung-cv.md` and their `-en` twins. They are linked from the *Projects* menu and from the area tiles on the home page. All of them use [`_layouts/area.html`](_layouts/area.html), which fills in the running/completed projects (by `category`), the number of publications and theses and the latest five of each (by `categories`) automatically – only the text (and optionally a curated list of focus topics) is maintained by hand:

```yaml
---
layout: area
lang: de
title: eHealth
page_id: area:ehealth
permalink: /forschung/ehealth/
area: ehealth            # id from _data/publication_categories.yml
css: projects            # project cards and the area styles
icon: /assets/images/index/ehealth.svg
lead: One-sentence summary shown in the title band.
focus:                   # optional, focus topics curated by the area lead, shown as tags
  - …
contact: jane.doe@fh-hagenberg.at   # optional, a member of _data/team.yml; no contact box without it
---

Area description (Markdown)...
```

## Publications

Research papers, shown grouped by year with a category filter.

- **Location:** `_publications/{de,en}/YYYY-MM-DD-title.md` (dates typically use `12-31`)

```yaml
---
lang: de
page_id: pub:modeling-wildlife-accident-risk-with-gaussian-mixture-models
permalink: /publications/modeling-wildlife-accident-risk-with-gaussian-mixture-models/  # optional, used as anchor for search
date: 2024-12-31
title: Modeling Wildlife Accident Risk with Gaussian Mixture Models
reference: Praschl C., Schedl D., Stöckl A. "Modeling Wildlife Accident Risk with Gaussian Mixture Models", EUROCAST 2024.
categories: [ml, geo]   # one or more, see below
projects: [projects:bambi]                   # optional, page_ids of the related projects
external_url: https://example.org/abstract-book.pdf
doi: https://doi.org/10.0000/example        # optional
attachment: /assets/.../paper.pdf            # optional
---

Abstract (Markdown)...
```

To check for duplicates (missing DE/EN pairs, reused `page_id`s or permalinks, near-identical titles) run `python scripts/check_duplicates.py`; add `--base origin/main` to also compare newly added entries against the existing ones by authors and title keywords. If two entries were checked and really are separate works (e.g. a non-archival workshop version and the conference paper), add `not_duplicate_of: [<other page_id>]` to the front matter of one of them so the check stops flagging the pair.

### Categories

A publication carries a **list** of categories — most sit at the intersection of
several research areas, e.g. a wildlife-detection paper is both `geo` and `cv`.
The dropdown filter is single-select and shows an entry whenever the picked
category appears anywhere in its list; the badges under each title are shortcuts
into that category.

| id        | Area                                |
| --------- | ----------------------------------- |
| `ehealth` | eHealth & Medical Informatics       |
| `cv`      | Visual Computing (Computer Vision, Image Processing, Computer Graphics, Mixed Reality) |
| `ml`      | Machine Learning & Data Science     |
| `se`      | Software Engineering                |
| `pm`      | Process Mining & Process Analytics  |
| `geo`     | Remote Sensing, UAV & Geospatial    |
| `xr`      | Augmented & Virtual Reality         |

The list is defined once in [`_data/publication_categories.yml`](_data/publication_categories.yml)
(id, German/English full label for the dropdown, and a short label for the badges).
To add a category, add an entry there and assign it in the relevant publications —
nothing else hard-codes the taxonomy. Medical imaging work has no category of its
own; it is tagged `[ehealth, cv]`.

Both language pages render through
[`_includes/publication-filter.html`](_includes/publication-filter.html) (dropdown,
counts, filter behaviour) and
[`_includes/publication-list.html`](_includes/publication-list.html) (year-grouped
entries and badges), so `publications.html` and `publications-en.html` stay in sync.

## Theses
Bachelor/Master theses and dissertations, shown grouped by year and filterable by research category, year and type. Categories use the same taxonomy as the publications ([`_data/publication_categories.yml`](_data/publication_categories.yml)) and appear as badges on each entry.

- **Location:** `_theses/{de,en}/YYYY-student-title.md`

```yaml
---
lang: de
page_id: thesis:andreas-erhard-process-mining-...
permalink: /theses/andreas-erhard-process-mining-.../  # optional, used as anchor for search
date: 2023-12-31
title: Process Mining im Radiologiebereich
student: Andreas Erhard
thesis_type: master  # bachelor | master | dissertation -- shown as a label and used by the type filter
categories: [pm, ehealth]  # ids from _data/publication_categories.yml, usually one or two
projects: [projects:pica]  # optional, page_ids of the related projects, see below
---

Abstract (Markdown)...
```

## Linking Output to Projects

Publications and theses can name the project(s) they came out of in a `projects:` list of project `page_id`s (e.g. `projects: [projects:bambi]`; the same value goes into the DE and the EN file). This

- adds a **Publications** and a **Theses** section at the end of that project's page (after all phases), rendered with the same includes as the listings ([`_includes/publication-list.html`](_includes/publication-list.html), [`_includes/thesis-list.html`](_includes/thesis-list.html)); a section without entries is left out, and
- shows a "Project: …" link under the entry on the publications and theses pages ([`_includes/project-links.html`](_includes/project-links.html)).

Unknown ids are ignored, so back-filling can happen gradually.

# Open Positions & Thesis Topics

The *Join us* page ([`mitarbeit.html`](mitarbeit.html) / [`mitarbeit-en.html`](mitarbeit-en.html), linked under *About*) is generated from two data files; both are documented with a full example in their header comment:

- [`_data/positions.yml`](_data/positions.yml) – open positions (`title_de/_en`, `type`: `researcher` | `phd` | `student` | `internship`, optional `hours_*`, `start_*`, `deadline`, `description_*`, `url`, `contact`). A position whose `deadline` has passed is hidden automatically. With no open position the page invites unsolicited applications instead.
- [`_data/thesis_topics.yml`](_data/thesis_topics.yml) – open thesis topics (`title_de/_en`, `thesis_type` as a list, `categories` from the publication taxonomy, `supervisor`, `contact`, optional `project` page_id, `description_*`). They get the same category / type filter as the theses page; with no topic the page asks students to propose their own.

The theses pages and the call to action at the bottom of the home page link to this page.

# Software & Data

The *Software & Data* page ([`software.html`](software.html) / [`software-en.html`](software-en.html), linked under *Projects* and from the home page) lists reusable outputs from [`_data/software.yml`](_data/software.yml), grouped into datasets, software and models. The fields are documented at the top of that file:

```yaml
- name: BAMBI Dataset
  type: dataset                 # dataset | software | model
  categories: [cv, geo]         # ids from _data/publication_categories.yml
  language: Python              # optional
  description_de: …
  description_en: …
  repo: https://github.com/bambi-eco/Dataset
  docs: https://…               # optional
  doi: 10.5281/zenodo.1234567   # optional, DOI of the software/data itself
  license: CC-BY-4.0, MIT
  project: projects:bambi       # optional, links the project page
  publication: pub:the-bambi-dataset-…   # optional, shown as "Please cite"
```

# Partners & Funders

Funders and partners are shown on the home page, below *Collaboration & theses* (both `site_design` variants), from [`_includes/home/partners-funders.html`](_includes/home/partners-funders.html):

- [`_data/funders.yml`](_data/funders.yml) – one entry per funding body with the `aliases` that identify it in the free-text `foerdergeber` of the project phases (this merges spelling variants such as "FFG Basisprogramm" / "Österreichische Forschungsförderungsgesellschaft FFG – Basisprogramm"), an optional `flag` matching a project field (`eu_funded`), name, URL, logo (shown left of the name, files in `assets/images/funders/`) and programmes. Each funder is a card of the same size with the number of its projects, which opens the list of them as an overlay; a project that matches no alias (e.g. contract research) is simply not counted.
- [`_data/partners.yml`](_data/partners.yml) – the project partners (companies and institutions, no private individuals) for the endless logo carousel; each tile links to the partner's `url`. Only partners with a `logo` are shown (`logo: false` marks a partner without a usable logo); White logos made for dark backgrounds are recoloured to black so every tile is white. `hide: true` leaves a partner out. Logos are trademarks and need the partners' consent (see issue #19).

To crawl the logos, run from the repository root (needs network access, standard library only):

```bash
python3 scripts/fetch_partner_logos.py
```

It looks for the logo on each partner's start page (skipping entries that already have a `logo`, including `logo: false`), saves it to `assets/images/partners/` and adds the `logo:` line to the data file. Review every file before committing; a wrong pick is replaced by hand.

# Team

Team members are listed from [`_data/team.yml`](_data/team.yml). Each member carries a `category:` (`professor` | `project_manager` | `researcher` | `student`, labels in [`_data/team_categories.yml`](_data/team_categories.yml)) that is shown after the name, and a `gender:` (`m` | `f`) that picks the German form of that label (neutral fallback without it); an optional `role:` (e.g. the study programme of a student employee) is shown next to it.

All further fields are optional and only rendered when present (cards: [`_includes/team-card.html`](_includes/team-card.html)). Profile links and interests are meant to be added by each member themselves:

```yaml
members:
  - name: Jane Doe MSc
    category: researcher
    gender: f
    email: jane.doe@fh-hagenberg.at
    phone: +43 5 0804 12345
    image: /assets/images/team/jane_doe_msc.jpg
    details_url: https://pure.fh-ooe.at/en/persons/jane-doe   # "Details" link
    interests_de: [Computer Vision, Medizinische Bildverarbeitung]   # tags on the card
    interests_en: [Computer vision, Medical imaging]
    orcid: 0000-0002-1825-0097      # ORCID iD
    scholar: AbCdEfGhIjK            # Google Scholar user id (user=... in the profile URL)
    github: janedoe                 # GitHub handle
    linkedin: jane-doe              # linkedin.com/in/<handle>
```

### Alumni

Former members can be listed below the team (`alumni:` in the same file, [`_includes/team-alumni.html`](_includes/team-alumni.html)) – **opt-in only and without photos** (GDPR). An entry is rendered only when it records the date of the person's consent; remove it when consent is withdrawn. The section is hidden while the list is empty.

```yaml
alumni:
  - name: Max Mustermann
    consent: 2026-10-23        # required, otherwise the entry is not shown
    years: 2015–2021           # optional
    role_de: Wissenschaftlicher Mitarbeiter   # optional, last role in the group
    role_en: Research associate
    now_de: Data Scientist bei …              # optional, only if the person agreed
    now_en: Data scientist at …
    url: https://…                            # optional, a link the person chose
```

---

# Images & Git LFS

All binary image formats are tracked with [Git LFS](https://git-lfs.com/) (see
[`.gitattributes`](.gitattributes)):

Before cloning or committing images, make sure LFS is installed and initialized
(`git lfs install`). Image assets live under `assets/images/`, organized by use
(`team/`, `projects/`, `news/`, ...). Reference them in front matter and Markdown via their absolute path, e.g. `/assets/images/projects/Bambi_logo.png`.

# Deployment

Deployment is automated via [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml):

- Every push to `main` (plus a nightly run and manual `workflow_dispatch`) builds the site with `JEKYLL_ENV=production`, indexes it with Pagefind and pushes `_site` to the `gh-pages` branch, which GitHub Pages serves.
- Every pull request from a branch of this repository gets a **preview** at `https://aist.fh-hagenberg.at/pr-preview/pr-<N>/` via [`.github/workflows/preview.yml`](.github/workflows/preview.yml). A bot comment on the PR links to it; it is updated on every push to the PR and removed when the PR is closed or merged. Preview pages are marked `noindex` (see `_config.preview.yml`). PRs from forks don't get a preview.

Repository setting required: **Settings → Pages → Build and deployment → Source: "Deploy from a branch", branch `gh-pages`, folder `/ (root)`**.

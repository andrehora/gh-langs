# gh-langs

Comprehensive dataset of language names, extensions, aliases, and filenames extracted from [GitHub Linguist](https://github.com/github-linguist/linguist).
Data is extracted from [languages.yml](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml).

Explore the data: https://andrehora.github.io/gh-langs/

<!-- updated -->
Updated: 2026-04-24
<!-- /updated -->

## Data

### Basic

<!-- gh:start -->
| File | Count | Description |
|------|-------|-------------|
| [`gh_languages.txt`](data/gh_languages.txt) | 804 | Languages known to GitHub |
| [`gh_extensions.txt`](data/gh_extensions.txt) | 1448 | Language extensions known to GitHub |
| [`gh_aliases.txt`](data/gh_aliases.txt) | 413 | Language aliases known to GitHub |
| [`gh_filenames.txt`](data/gh_filenames.txt) | 399 | Language filenames known to GitHub |
<!-- gh:end -->

### Languages

Popular GitHub languages comes from GitHub Linguist [popular.yml](https://github.com/github-linguist/linguist/blob/main/lib/linguist/popular.yml).

<!-- summary:start -->
| File | Count | Description |
|------|-------|-------------|
| [`languages.json`](data/languages.json) / [`csv`](data/languages.csv) | 804 | All languages |
| [`languages_popular.json`](data/languages_popular.json) / [`csv`](data/languages_popular.csv) | 25 | Popular languages |
<!-- summary:end -->

### Languages by Type

<!-- types:start -->
| File | Count | Description |
|------|-------|-------------|
| [`languages_programming.json`](data/languages_programming.json) / [`csv`](data/languages_programming.csv) | 539 | Programming languages |
| [`languages_data.json`](data/languages_data.json) / [`csv`](data/languages_data.csv) | 178 | Data languages |
| [`languages_markup.json`](data/languages_markup.json) / [`csv`](data/languages_markup.csv) | 69 | Markup languages |
| [`languages_prose.json`](data/languages_prose.json) / [`csv`](data/languages_prose.csv) | 18 | Prose languages |
<!-- types:end -->

## Fields

- `type`: programming (e.g., Python), data (e.g., JSON), markup (e.g., HTML) or prose (e.g., Markdown).
- `aliases`: List of additional aliases (optional).
- `filenames`: List of associated filenames. May be omitted if the extensions field is present (and vice versa).
- `extensions`: List of associated file extensions.

## Fun Facts

### Languages with the most extensions

See: [`stats_languages_by_extensions.csv`](data/stats_languages_by_extensions.csv)

| Language | Type | Extensions |
|----------|------|------------|
| XML | data | 110 |
| Roff | markup | 28 |
| JavaScript | programming | 25 |
| GLSL | programming | 23 |
| Ruby | programming | 22 |
| JSON | data | 21 |
| C++ | programming | 20 |
| Roff Manpage | markup | 20 |
| JSON with Comments | data | 18 |
| Python | programming | 17 |

### Languages with the most filenames

See: [`stats_languages_by_filenames.csv`](data/stats_languages_by_filenames.csv)

| Language | Type | Filenames |
|----------|------|-----------|
| Shell | programming | 41 |
| Text | prose | 25 |
| Ruby | programming | 23 |
| Ignore List | data | 20 |
| JSON | data | 18 |
| Dotenv | data | 14 |
| JSON with Comments | data | 14 |
| Makefile | programming | 13 |
| Emacs Lisp | programming | 11 |
| XML | data | 10 |

### Languages with the most aliases

See: [`stats_languages_by_aliases.csv`](data/stats_languages_by_aliases.csv)

| Language | Type | Aliases |
|----------|------|----------|
| Roff | markup | 8 |
| Checksums | data | 5 |
| QuickBASIC | programming | 5 |
| Ruby | programming | 5 |
| Shell | programming | 5 |
| Visual Basic 6.0 | programming | 5 |
| Wolfram Language | programming | 5 |
| Adblock Filter List | data | 4 |
| Adobe Font Metrics | data | 4 |
| Batchfile | programming | 4 |

## JSON Examples

### type: programming

```json
{
  "Python": {
    "type": "programming",
    "aliases": ["py", "py3", "python3", "rusthon"],
    "extensions": [".py", ".cgi", ".fcgi", ".gyp", ".gypi", ".lmi", ".py3", ".pyde", ".pyi", ".pyp", ".pyt", ".pyw", ".rpy", ".spec", ".tac", ".wsgi", ".xpy"],
    "filenames": [".gclient", "DEPS", "SConscript", "SConstruct", "wscript"]
  }
}
```

### type: data

```json
{
  "JSON": {
    "type": "data",
    "aliases": ["geojson", "jsonl", "sarif", "topojson"],
    "extensions": [".json", ".4DForm", ".4DProject", ".avsc", ".geojson", ".gltf", ".har", ".ice", ".JSON-tmLanguage", ".json.example", ".jsonl", ".mcmeta", ".sarif", ".tfstate", ".tfstate.backup", ".topojson", ".webapp", ".webmanifest", ".yy", ".yyp"],
    "filenames": [".all-contributorsrc", ".arcconfig", ".auto-changelog", ".c8rc", ".htmlhintrc", ".imgbotconfig", ".nycrc", ".tern-config", ".tern-project", ".watchmanconfig", "MODULE.bazel.lock", "Package.resolved", "Pipfile.lock", "composer.lock", "deno.lock", "flake.lock", "mcmod.info"]
  }
}
```

### type: markup

```json
{
  "HTML": {
    "type": "markup",
    "aliases": ["xhtml"],
    "extensions": [".html", ".hta", ".htm", ".html.hl", ".inc", ".xht", ".xhtml"]
  }
}
```

### type: prose

```json
{
  "Markdown": {
    "type": "prose",
    "aliases": ["md", "pandoc"],
    "extensions": [".md", ".livemd", ".markdown", ".mdown", ".mdwn", ".mkd", ".mkdn", ".mkdown", ".ronn", ".scd", ".workbook"],
    "filenames": ["contents.lr"]
  }
}
```

## Generating the Dataset

To regenerate the files from the source `languages.yml`:

```bash
python parse_languages.py
```

This parses [languages.yml](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml) (from GitHub Linguist) and writes output files to the `data/` folder.
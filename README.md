# GitHub Languages and Extensions

Comprehensive dataset of 800+ languages and their extensions extracted from [GitHub Linguist](https://github.com/github-linguist/linguist).

Data is extracted from GitHub Linguist [languages.yml](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml).


## Data

### Basic

<!-- gh:start -->
| File | Count | Description |
|------|-------|-------------|
| [`gh_languages.csv`](data/gh_languages.csv) | 804 | Languages known to GitHub |
| [`gh_extensions.csv`](data/gh_extensions.csv) | 1448 | Language extensions known to GitHub |
<!-- gh:end -->

### Language and Extensions

<!-- summary:start -->
| File | Count | Description |
|------|-------|-------------|
| [`languages.json`](data/languages.json) / [`csv`](data/languages.csv) | 804 | Languages and extensions |
| [`languages_popular.json`](data/languages_popular.json) / [`csv`](data/languages_popular.csv) | 25 | Popular languages and extensions |
<!-- summary:end -->

> [!NOTE]
> Popular GitHub languages comes from GitHub Linguist [popular.yml](https://github.com/github-linguist/linguist/blob/main/lib/linguist/popular.yml).

### Language and Extensions per Type: programming, data, markup, or prose

<!-- types:start -->
| File | Count | Description |
|------|-------|-------------|
| [`languages_programming.json`](data/languages_programming.json) / [`csv`](data/languages_programming.csv) | 539 | Programming languages |
| [`languages_data.json`](data/languages_data.json) / [`csv`](data/languages_data.csv) | 178 | Data languages |
| [`languages_markup.json`](data/languages_markup.json) / [`csv`](data/languages_markup.csv) | 69 | Markup languages |
| [`languages_prose.json`](data/languages_prose.json) / [`csv`](data/languages_prose.csv) | 18 | Prose languages |
<!-- types:end -->

## Fields

- `type`: Either `programming` (e.g., Python), `data` (e.g., JSON), `markup` (e.g., HTML) or `prose` (e.g., Markdown).
- `aliases`: List of additional aliases (optional)
- `filenames`: List of associated filenames. May be omitted if the extensions field is present (and vice versa).
- `extensions`: List of associated file extensions.

#### programming

```json
{
  "Python": {
    "type": "programming",
    "aliases": ["py", "py3", "python3", "rusthon"],
    "extensions": [".py", ".cgi", ".fcgi", ".gyp", ".gypi", ".lmi", ".py3", ".pyde", ".pyi", ".pyp", ".pyt", ".pyw", ".rpy", ".spec", ".tac", ".wsgi", ".xpy"]
  }
}
```

#### data

```json
{
  "JSON": {
    "type": "data",
    "aliases": ["geojson", "jsonl", "sarif", "topojson"],
    "extensions": [".json", ".avsc", ".geojson", ".gltf", ".har", ".ice", ".jsonl", ".mcmeta", ".sarif", ".tfstate", ".topojson", ".webapp", ".webmanifest", ".yy", ".yyp"]
  }
}
```

#### markup

```json
{
  "HTML": {
    "type": "markup",
    "aliases": ["xhtml"],
    "extensions": [".html", ".hta", ".htm", ".inc", ".xht", ".xhtml"]
  }
}
```

#### prose

```json
{
  "Markdown": {
    "type": "prose",
    "aliases": ["md", "pandoc"],
    "extensions": [".md", ".livemd", ".markdown", ".mdown", ".mdwn", ".mkd", ".mkdn", ".mkdown", ".ronn", ".scd", ".workbook"]
  }
}
```

## Generating the Dataset

To regenerate the files from the source `languages.yml`:

```bash
python parse_languages.py
```

This parses [languages.yml](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml) (from GitHub Linguist) and writes output files to the `data/` folder.

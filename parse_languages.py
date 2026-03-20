import yaml
import json
import csv
from pathlib import Path
from collections import Counter
import requests

TYPES = ["programming", "data", "markup", "prose"]
OUTPUT_DIR = "data"
README_PATH = "README.md"
LANGUAGES_URL = "https://raw.githubusercontent.com/github-linguist/linguist/refs/heads/main/lib/linguist/languages.yml"
POPULAR_URL = "https://raw.githubusercontent.com/github-linguist/linguist/refs/heads/main/lib/linguist/popular.yml"


def parse_languages():
    print("Fetching data...")
    by_type, all_langs, type_counts = load_languages(LANGUAGES_URL)
    popular_names = load_popular_names(POPULAR_URL)

    print_summary(type_counts)

    print(f"Writing output to '{OUTPUT_DIR}/'")
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    write_type_files_json(by_type)
    write_type_files_csv(by_type)

    write_languages_json(all_langs)
    write_languages_csv(all_langs)

    write_popular_languages_json(all_langs, popular_names)
    write_popular_languages_csv(all_langs, popular_names)

    write_gh_extensions_csv(all_langs)
    write_gh_languages_csv(all_langs)

    write_languages_stats_csv(all_langs)
    write_summary_csv(type_counts)
    write_readme(type_counts, popular_names, all_langs)

    print("Done.")
    return by_type, all_langs, type_counts, popular_names


def load_languages(languages_url):
    content = _fetch_and_save(languages_url, "languages.yml")
    data = yaml.safe_load(content)

    type_counts = Counter()
    by_type = {t: [] for t in TYPES}

    for name, props in data.items():
        lang_type = props.get("type", "unknown")
        type_counts[lang_type] += 1
        if lang_type in by_type:
            by_type[lang_type].append({
                "name": name,
                "type": lang_type,
                "aliases": props.get("aliases", []),
                "extensions": props.get("extensions", []),
            })

    for t in by_type:
        by_type[t].sort(key=lambda x: x["name"].lower())

    all_langs = [lang for t in TYPES for lang in by_type[t]]
    return by_type, all_langs, type_counts


def load_popular_names(popular_url):
    popular_content = _fetch_and_save(popular_url, "popular.yml")
    return yaml.safe_load(popular_content)


def write_type_files_json(by_type):
    for t in TYPES:
        type_data = {}
        for lang in by_type[t]:
            entry = {"extensions": lang["extensions"]}
            if lang["aliases"]:
                entry["aliases"] = lang["aliases"]
            type_data[lang["name"]] = entry
        filename = f"languages_{t}.json"
        filepath = Path(OUTPUT_DIR) / filename
        with open(filepath, "w") as f:
            json.dump(type_data, f, indent=2)
        print(f"Wrote {filepath} ({len(type_data)} languages)")


def write_type_files_csv(by_type):
    for t in TYPES:
        rows = sorted(by_type[t], key=lambda lang: lang["name"].lower())
        filename = f"languages_{t}.csv"
        filepath = Path(OUTPUT_DIR) / filename
        data = [[lang["name"], "; ".join(lang["aliases"]), "; ".join(lang["extensions"])] for lang in rows]
        _write_csv(filepath, ["language", "aliases", "extensions"], data)
        print(f"Wrote {filepath} ({len(rows)} languages)")


def write_languages_json(all_langs):
    filename = "languages.json"
    filepath = Path(OUTPUT_DIR) / filename
    langs = {}
    for lang in all_langs:
        entry = {"type": lang["type"], "extensions": lang["extensions"]}
        if lang["aliases"]:
            entry["aliases"] = lang["aliases"]
        langs[lang["name"]] = entry
    with open(filepath, "w") as f:
        json.dump(langs, f, indent=2)
    print(f"Wrote {filepath} ({len(langs)} languages)")


def write_languages_csv(all_langs):
    filename = "languages.csv"
    filepath = Path(OUTPUT_DIR) / filename
    rows = sorted(
        [(lang["name"], lang["type"], lang["aliases"], lang["extensions"]) for lang in all_langs],
        key=lambda r: r[0].lower()
    )
    data = [[name, lang_type, "; ".join(aliases), "; ".join(extensions)] for name, lang_type, aliases, extensions in rows]
    _write_csv(filepath, ["language", "type", "aliases", "extensions"], data)
    print(f"Wrote {filepath} ({len(rows)} languages)")


def write_popular_languages_json(all_langs, popular_names):
    filename = "popular_languages.json"
    filepath = Path(OUTPUT_DIR) / filename
    langs_by_name = {lang["name"]: lang for lang in all_langs}
    popular = {}
    for name in popular_names:
        lang = langs_by_name.get(name)
        if lang is None:
            continue
        entry = {"type": lang["type"], "extensions": lang["extensions"]}
        if lang["aliases"]:
            entry["aliases"] = lang["aliases"]
        popular[name] = entry
    with open(filepath, "w") as f:
        json.dump(popular, f, indent=2)
    print(f"Wrote {filepath} ({len(popular)} languages)")


def write_popular_languages_csv(all_langs, popular_names):
    filename = "popular_languages.csv"
    filepath = Path(OUTPUT_DIR) / filename
    langs_by_name = {lang["name"]: lang for lang in all_langs}
    rows = [
        [name, lang["type"], "; ".join(lang["aliases"]), "; ".join(lang["extensions"])]
        for name in popular_names
        if (lang := langs_by_name.get(name)) is not None
    ]
    _write_csv(filepath, ["language", "type", "aliases", "extensions"], rows)
    print(f"Wrote {filepath} ({len(rows)} languages)")


def write_gh_extensions_csv(all_langs):
    filename = "gh_extensions.csv"
    filepath = Path(OUTPUT_DIR) / filename
    all_extensions = sorted({ext for lang in all_langs for ext in lang["extensions"]})
    _write_csv(filepath, ["extension"], [[ext] for ext in all_extensions])
    print(f"Wrote {filepath} ({len(all_extensions)} extensions)")


def write_gh_languages_csv(all_langs):
    filename = "gh_languages.csv"
    filepath = Path(OUTPUT_DIR) / filename
    all_names = sorted({lang["name"] for lang in all_langs}, key=str.lower)
    _write_csv(filepath, ["language"], [[name] for name in all_names])
    print(f"Wrote {filepath} ({len(all_names)} languages)")


def write_languages_stats_csv(all_langs):
    filename = "languages_stats.csv"
    filepath = Path(OUTPUT_DIR) / filename
    rows = sorted(
        [(lang["name"], lang["type"], len(lang["extensions"]), len(lang["aliases"])) for lang in all_langs],
        key=lambda r: (-(r[2] + r[3]), r[0].lower())
    )
    _write_csv(filepath, ["language", "type", "extensions_count", "aliases_count"], rows)
    print(f"Wrote {filepath} ({len(rows)} languages)")


def write_summary_csv(type_counts):
    filename = "summary.csv"
    filepath = Path(OUTPUT_DIR) / filename
    rows = [[t, type_counts[t]] for t in TYPES] + [["total", sum(type_counts.values())]]
    _write_csv(filepath, ["type", "count"], rows)
    print(f"Wrote {filepath}")


def write_readme(type_counts, popular_names, all_langs):
    readme = Path(README_PATH)
    total = sum(type_counts.values())
    content = readme.read_text()

    gh_languages_count = len({lang["name"] for lang in all_langs})
    gh_extensions_count = len({ext for lang in all_langs for ext in lang["extensions"]})
    gh_rows = (
        f"| [`gh_languages.csv`](data/gh_languages.csv) | {gh_languages_count} | Language names as defined in GitHub Linguist |\n"
        f"| [`gh_extensions.csv`](data/gh_extensions.csv) | {gh_extensions_count} | File extensions mapped to languages in GitHub Linguist |"
    )
    content = _replace_between(content, "<!-- gh:start -->", "<!-- gh:end -->", gh_rows)

    summary_rows = (
        f"| [`languages.json`](data/languages.json) / [`csv`](data/languages.csv) | {total} | All languages |\n"
        f"| [`popular_languages.json`](data/popular_languages.json) / [`csv`](data/popular_languages.csv) | {len(popular_names)} | Popular languages |"
    )
    content = _replace_between(content, "<!-- summary:start -->", "<!-- summary:end -->", summary_rows)

    type_descriptions = {"programming": "Programming", "data": "Data", "markup": "Markup", "prose": "Prose"}
    types_rows = "\n".join(
        f"| [`languages_{t}.json`](data/languages_{t}.json) / [`csv`](data/languages_{t}.csv) | {type_counts[t]} | {type_descriptions[t]} languages |"
        for t in TYPES
    )
    content = _replace_between(content, "<!-- types:start -->", "<!-- types:end -->", types_rows)

    readme.write_text(content)
    print("Wrote README.md")


def _replace_between(text, start_marker, end_marker, replacement):
    start = text.index(start_marker) + len(start_marker) + 1
    end = text.index(end_marker) - 1
    return text[:start] + replacement + text[end:]


def print_summary(type_counts):
    total = sum(type_counts.values())
    print(f"Languages loaded: {total}")
    for t in TYPES:
        print(f"{t}: {type_counts[t]}")


def _fetch_and_save(url, filename):
    print(f"Fetching {url}")
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    return response.content


def _write_csv(filepath, header, rows):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    parse_languages()

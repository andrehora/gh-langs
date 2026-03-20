import os
import pytest
import parse_languages

BASE_URL = "https://raw.githubusercontent.com/github-linguist/linguist/refs/tags/v9.5.0/lib/linguist"
LANGUAGES_URL = f"{BASE_URL}/languages.yml"
POPULAR_URL = f"{BASE_URL}/popular.yml"


@pytest.fixture(scope="session")
def parsed_data(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("data")
    cwd = os.getcwd()
    os.chdir(tmp)
    original_output_dir = parse_languages.OUTPUT_DIR
    original_languages_url = parse_languages.LANGUAGES_URL
    original_popular_url = parse_languages.POPULAR_URL
    original_readme_path = parse_languages.README_PATH
    tmp_readme = tmp / "README.md"
    tmp_readme.write_text(
        "<!-- gh:start -->\n"
        "| File | Count | Description |\n"
        "|------|-------|-------------|\n"
        "| old | 0 | x |\n"
        "| old | 0 | x |\n"
        "<!-- gh:end -->\n"
        "<!-- summary:start -->\n"
        "| File | Count | Description |\n"
        "|------|-------|-------------|\n"
        "| old | 0 | x |\n"
        "| old | 0 | x |\n"
        "<!-- summary:end -->\n"
        "<!-- types:start -->\n"
        "| File | Count | Description |\n"
        "|------|-------|-------------|\n"
        "| old | 0 | x |\n"
        "<!-- types:end -->\n"
    )
    parse_languages.OUTPUT_DIR = str(tmp)
    parse_languages.LANGUAGES_URL = LANGUAGES_URL
    parse_languages.POPULAR_URL = POPULAR_URL
    parse_languages.README_PATH = str(tmp_readme)
    try:
        by_type, all_langs, type_counts, popular_names = parse_languages.parse_languages()
    finally:
        parse_languages.OUTPUT_DIR = original_output_dir
        parse_languages.LANGUAGES_URL = original_languages_url
        parse_languages.POPULAR_URL = original_popular_url
        parse_languages.README_PATH = original_readme_path
        os.chdir(cwd)

    return by_type, all_langs, type_counts, popular_names, tmp



def test_type_counts(parsed_data):
    _, _, type_counts, _, _ = parsed_data
    assert type_counts["programming"] == 539
    assert type_counts["data"] == 178
    assert type_counts["markup"] == 69
    assert type_counts["prose"] == 18
    assert sum(type_counts.values()) == 804


def test_by_type_keys(parsed_data):
    by_type, _, _, _, _ = parsed_data
    assert set(by_type.keys()) == set(parse_languages.TYPES)


def test_by_type_counts(parsed_data):
    by_type, _, _, _, _ = parsed_data
    assert len(by_type["programming"]) == 539
    assert len(by_type["data"]) == 178
    assert len(by_type["markup"]) == 69
    assert len(by_type["prose"]) == 18


def test_all_langs_count(parsed_data):
    _, all_langs, _, _, _ = parsed_data
    assert len(all_langs) == 804


def test_popular_names(parsed_data):
    _, _, _, popular_names, _ = parsed_data
    assert len(popular_names) == 25


def test_sorted_alphabetically(parsed_data):
    by_type, _, _, _, _ = parsed_data
    for t in parse_languages.TYPES:
        names = [lang["name"].lower() for lang in by_type[t]]
        assert names == sorted(names)


def test_python_entry(parsed_data):
    by_type, _, _, _, _ = parsed_data
    python = next(l for l in by_type["programming"] if l["name"] == "Python")
    assert python["type"] == "programming"
    assert python["aliases"] == ["py", "py3", "python3", "rusthon"]
    assert ".py" in python["extensions"]
    assert len(python["extensions"]) == 17


def test_lang_entry_fields(parsed_data):
    import json
    _, _, _, _, tmp = parsed_data
    data = json.loads((tmp / "languages.json").read_text())
    assert data["Python"]["type"] == "programming"
    assert "aliases" in data["Python"]
    assert "extensions" in data["Python"]


def test_lang_entry_without_type(parsed_data):
    import json
    _, _, _, _, tmp = parsed_data
    data = json.loads((tmp / "languages_programming.json").read_text())
    assert "type" not in data["Python"]


JSON_FILES = [
    "languages.json",
    "languages_programming.json",
    "languages_data.json",
    "languages_markup.json",
    "languages_prose.json",
    "popular_languages.json",
]


@pytest.mark.parametrize("filename", JSON_FILES)
def test_json_file_exists(parsed_data, filename):
    _, _, _, _, tmp = parsed_data
    assert (tmp / filename).exists()


CSV_FILES = [
    "languages.csv",
    "languages_programming.csv",
    "languages_data.csv",
    "languages_markup.csv",
    "languages_prose.csv",
    "popular_languages.csv",
    "gh_extensions.csv",
    "gh_languages.csv",
    "languages_stats.csv",
    "summary.csv",
]


@pytest.mark.parametrize("filename", CSV_FILES)
def test_csv_file_exists(parsed_data, filename):
    _, _, _, _, tmp = parsed_data
    assert (tmp / filename).exists()


def test_readme_updated(parsed_data):
    _, all_langs, type_counts, popular_names, tmp = parsed_data
    content = (tmp / "README.md").read_text()
    total = sum(type_counts.values())
    assert str(total) in content
    assert str(len(popular_names)) in content
    for t in parse_languages.TYPES:
        assert str(type_counts[t]) in content
    gh_languages_count = len({lang["name"] for lang in all_langs})
    gh_extensions_count = len({ext for lang in all_langs for ext in lang["extensions"]})
    assert str(gh_languages_count) in content
    assert str(gh_extensions_count) in content
import csv
import re
import requests
import yaml
from packaging.version import Version

VERSIONS_URL = "https://data.jsdelivr.com/v1/packages/gh/github-linguist/linguist"
LANGUAGES_URL = "https://cdn.jsdelivr.net/gh/github-linguist/linguist@{version}/lib/linguist/languages.yml"
OUTPUT_FILE = "data/history_analysis.csv"
VERSION_MIN = Version("1.0.0")
# VERSION_MAX = Version("9.5.0")
VERSION_MAX = Version("5.0.0")


def fetch_versions():
    response = requests.get(VERSIONS_URL)
    response.raise_for_status()
    data = response.json()
    versions = []
    for v in data.get("versions", []):
        tag = v.get("version", "")
        # Filter only semver-like tags (e.g. 1.0.0), skip branches like test/master
        if re.match(r"^\d+\.\d+\.\d+$", tag):
            ver = Version(tag)
            if VERSION_MIN <= ver <= VERSION_MAX:
                versions.append(tag)
    versions.sort(key=Version)
    return versions


def fetch_language_stats(version):
    url = LANGUAGES_URL.format(version=version)
    response = requests.get(url)
    response.raise_for_status()
    data = yaml.safe_load(response.content)

    languages_count = len(data)
    aliases_count = 0
    extensions_count = 0
    filenames_count = 0

    for props in data.values():
        aliases_count += len(props.get("aliases", []) or [])
        extensions_count += len(props.get("extensions", []) or [])
        filenames_count += len(props.get("filenames", []) or [])

    return languages_count, aliases_count, extensions_count, filenames_count


def run():
    print("Fetching versions...")
    versions = fetch_versions()
    print(f"Found {len(versions)} versions between {VERSION_MIN} and {VERSION_MAX}")

    rows = []
    for version in versions:
        print(f"Processing {version}...", end=" ", flush=True)
        try:
            languages, aliases, extensions, filenames = fetch_language_stats(version)
            rows.append([version, languages, aliases, extensions, filenames])
            print(f"languages={languages}, aliases={aliases}, extensions={extensions}, filenames={filenames}")
        except Exception as e:
            print(f"ERROR: {e}")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["version", "languages_count", "aliases_count", "extensions_count", "filenames_count"])
        writer.writerows(rows)

    print(f"\nWrote {OUTPUT_FILE} ({len(rows)} versions)")


if __name__ == "__main__":
    run()
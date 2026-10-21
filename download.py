import csv
import io
import re
import urllib.request
import zipfile

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_FILE = "ssa-baby-names.csv"

# Browser-like headers required by the SSA server
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}


def main():
    req = urllib.request.Request(URL, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        zip_bytes = io.BytesIO(response.read())

    with zipfile.ZipFile(zip_bytes) as zf, open(
        OUTPUT_FILE, "w", newline="", encoding="utf-8"
    ) as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["year", "name", "sex", "count"])

        # Process each yobYYYY.txt file in chronological order
        for filename in sorted(zf.namelist()):
            match = re.fullmatch(r"yob(\d{4})\.txt", filename)
            if not match:
                continue
            year = match.group(1)

            with zf.open(filename) as in_f:
                reader = csv.reader(io.TextIOWrapper(in_f, encoding="utf-8"))
                for name, sex, count in reader:
                    writer.writerow([year, name, sex, count])


if __name__ == "__main__":
    main()

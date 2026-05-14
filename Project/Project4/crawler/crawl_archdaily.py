import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from pathlib import Path

BASE_URL = "https://www.archdaily.com"
START_URL = "https://www.archdaily.com/architecture-competitions"

PROJECT_DIR = Path(__file__).resolve().parents[1]
SAVE_DIR = PROJECT_DIR / "data" / "raw"
META_PATH = PROJECT_DIR / "data" / "metadata" / "metadata.csv"

MAX_IMAGES = 100
MAX_LIST_PAGES = 10

HEADERS = {"User-Agent": "Mozilla/5.0"}

EXCLUDE_PATH_KEYWORDS = [
    "products", "catalog", "materials", "folders", "search",
    "tag", "architects", "offices", "news", "events",
    "about", "contact", "jobs", "advertise"
]

BAD_TITLE_KEYWORDS = [
    "archdaily",
    "broadcasting architecture worldwide",
    "top 100",
    "materials",
    "products",
    "companies",
    "catalog",
    "call for entries",
    "open call",
    "call for submissions",
    "call for papers",
    "submission",
    "deadline",
    "awards",
    "conference",
    "festival",
    "lecture",
    "webinar",
    "free entry",
    "registration",
]

BAD_IMAGE_KEYWORDS = [
    "logo",
    "placeholder",
    "default",
    "avatar",
    "facebook",
    "twitter",
    "linkedin",
    "icon"
]

GOOD_TITLE_KEYWORDS = [
    "winner",
    "winners",
    "wins",
    "winning proposal",
    "winning design",
    "first prize",
    "second prize",
    "third prize",
    "selected proposal",
    "awarded",
    "shortlisted proposal",
    "competition result",
    "competition results",
]

SAVE_DIR.mkdir(parents=True, exist_ok=True)
META_PATH.parent.mkdir(parents=True, exist_ok=True)


def clean_filename(text):
    text = re.sub(r'[\\/*?:"<>|]', "_", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:80] if text else "unknown"


def get_soup(url):
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")


def is_valid_archdaily_article(url):
    parsed = urlparse(url)

    if parsed.netloc != "www.archdaily.com":
        return False

    path = parsed.path.lower()

    if any(keyword in path for keyword in EXCLUDE_PATH_KEYWORDS):
        return False

    # ArchDaily article URL 형태: /숫자/title
    if not re.search(r"/\d{5,}/", path):
        return False

    return True


def collect_candidate_links():
    links = []

    for page in range(1, MAX_LIST_PAGES + 1):
        url = START_URL if page == 1 else f"{START_URL}/page/{page}"
        print(f"[목록 페이지 수집] {url}")

        try:
            soup = get_soup(url)
        except Exception as e:
            print("[목록 페이지 실패]", e)
            continue

        for a in soup.find_all("a", href=True):
            href = urljoin(BASE_URL, a["href"])

            if is_valid_archdaily_article(href) and href not in links:
                links.append(href)

        time.sleep(1)

    return links


def extract_title(soup):
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title.get("content").strip()

    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)

    return "unknown_title"


def extract_year(soup):
    published = soup.find("meta", property="article:published_time")
    if published and published.get("content"):
        year_match = re.search(r"\d{4}", published.get("content"))
        if year_match:
            return year_match.group()

    return ""


def extract_image_url(soup):
    # 1순위: og:image
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        image_url = og_image.get("content").strip()

        if is_good_image_url(image_url):
            return image_url

    # 2순위: article 내부 img
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")

        if not src:
            continue

        image_url = urljoin(BASE_URL, src)

        if is_good_image_url(image_url):
            return image_url

    return ""


def is_good_image_url(image_url):
    lower = image_url.lower()

    if any(bad in lower for bad in BAD_IMAGE_KEYWORDS):
        return False

    if "archdaily.com.br/wp-content/themes" in lower:
        return False

    if not any(ext in lower for ext in [".jpg", ".jpeg", ".png", ".webp"]):
        return False

    return True


def extract_article_data(page_url):
    soup = get_soup(page_url)

    title = extract_title(soup)
    year = extract_year(soup)
    image_url = extract_image_url(soup)

    lower_title = title.lower()
    body_text = soup.get_text(" ", strip=True)
    lower_text = body_text.lower()

    if any(bad in lower_title for bad in BAD_TITLE_KEYWORDS):
        return None

    is_winning_related = any(
    keyword in lower_title or keyword in lower_text
    for keyword in GOOD_TITLE_KEYWORDS
    )

    if not is_winning_related:
        return None

    if not image_url:
        return None

    award = ""
    for keyword in GOOD_TITLE_KEYWORDS:
        if keyword in lower_text:
            award = keyword
            break

    competition = "competition-related" if "competition" in lower_text or "competition" in lower_title else ""

    return {
        "source": "ArchDaily",
        "title": title,
        "year": year,
        "competition": competition,
        "award": award,
        "image_url": image_url,
        "page_url": page_url,
    }


def download_image(image_url, image_path):
    res = requests.get(image_url, headers=HEADERS, timeout=20)
    res.raise_for_status()

    content_type = res.headers.get("Content-Type", "")

    if "image" not in content_type:
        raise ValueError("이미지 파일이 아님")

    with open(image_path, "wb") as f:
        f.write(res.content)


def main():
    links = collect_candidate_links()
    print(f"후보 article 링크 수: {len(links)}")

    rows = []
    count = 0

    for link in tqdm(links):
        if count >= MAX_IMAGES:
            break

        try:
            meta = extract_article_data(link)

            if meta is None:
                continue

            title_clean = clean_filename(meta["title"])
            image_name = f"{count + 1:03d}_{title_clean}.jpg"
            image_path = SAVE_DIR / image_name

            download_image(meta["image_url"], image_path)

            meta["id"] = f"{count + 1:03d}"
            meta["image_path"] = str(image_path)

            rows.append(meta)
            count += 1

            print(f"[저장] {count}: {meta['title']}")
            time.sleep(1)

        except Exception as e:
            print("[실패]", link, e)
            continue

    df = pd.DataFrame(rows)

    if len(df) > 0:
        df = df[
            [
                "id",
                "source",
                "title",
                "year",
                "competition",
                "award",
                "image_url",
                "image_path",
                "page_url",
            ]
        ]

    df.to_csv(META_PATH, index=False, encoding="utf-8-sig")

    print("완료")
    print(f"저장 이미지 수: {len(df)}")
    print(f"이미지 폴더: {SAVE_DIR}")
    print(f"메타데이터: {META_PATH}")


if __name__ == "__main__":
    main()
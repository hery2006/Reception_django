#!/usr/bin/env python3
# coding: utf-8
"""
Scraper éducatif : parcourt une galerie paginée, visite chaque item, télécharge les images
et enregistre les métadonnées en CSV.
UTILISER UNIQUEMENT sur des sites où tu as la permission.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time
import csv

# --------- CONFIG ----------
START_URL = "https://e-hentai.org/g/1636254/98a05bda55/?p=1"   # page 1 de la galerie (adapter)
OUTPUT_DIR = "downloaded_images"
METADATA_CSV = "metadata.csv"
HEADERS = {"User-Agent": "GalleryScraper/1.0 (contact: toi@example.com)"}
DELAY_BETWEEN_PAGE = 1.0    # secondes entre pages
DELAY_BETWEEN_REQUESTS = 0.2
MAX_PAGES = 100             # éviter boucle infinie
# ---------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def absolute(link, base):
    return urljoin(base, link)

def sanitize_filename(s):
    keep = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(c if c in keep else "_" for c in s)[:200]

def download_binary(url, dest_path):
    r = requests.get(url, headers=HEADERS, stream=True, timeout=30)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(1024 * 8):
            if chunk:
                f.write(chunk)

def find_next_page(soup, base_url):
    """
    Générique : cherche un lien rel="next", puis d'autres heuristiques.
    Adapter si le site a une pagination spécifique.
    """
    # 1) <link rel="next" href="...">
    link = soup.find("link", rel="next")
    if link and link.get("href"):
        return absolute(link["href"], base_url)

    # 2) <a class="next"> or <a rel="next">
    a = soup.find("a", rel="next") or soup.select_one("a.next, .pagination-next a, a[aria-label='Next']")
    if a and a.get("href"):
        return absolute(a["href"], base_url)

    # 3) lien contenant "next" textuel (heuristique)
    a = soup.find("a", string=lambda t: t and ("next" in t.lower() or t.strip() == ">"))
    if a and a.get("href"):
        return absolute(a["href"], base_url)

    return None

def extract_gallery_items(soup, base_url):
    """
    Trouve les liens vers les pages de détail à partir de la page de galerie.
    --> Adapter le sélecteur ci-dessous selon le site
    Exemple courant : <a class="thumb" href="/s/abcd/123"> <img ...>
    """
    items = []
    # Exemple générique : toutes les balises <a> qui contiennent une img de vignette
    for a in soup.select("a"):
        if a.find("img"):
            href = a.get("href")
            if href:
                full = absolute(href, base_url)
                items.append(full)

    # On peut filtrer/uniq
    items = list(dict.fromkeys(items))
    return items

def extract_detail_info(detail_soup, detail_url):
    """
    Extrait l'URL de l'image en pleine résolution et des métadonnées.
    --> Adapter les sélecteurs selon la page de détail du site.
    """
    base = detail_url
    # 1) essayer de trouver une image principale
    # Exemples de sélecteurs à adapter :
    # - img#main-image
    # - .full-image img
    # - div.viewer img
    img_tag = detail_soup.select_one("img#main-image, .full-image img, .viewer img, img.primary")
    if not img_tag:
        # fallback : la plus grande <img> sur la page (heuristique)
        all_imgs = detail_soup.find_all("img")
        if all_imgs:
            img_tag = max(all_imgs, key=lambda i: len(i.get("src", "")))

    img_url = None
    if img_tag:
        img_url = img_tag.get("data-src") or img_tag.get("src") or img_tag.get("data-original")

    # 2) titre (si présent)
    title_tag = detail_soup.select_one("h1.title, .gallery-title, .post-title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # 3) tags (liste)
    tags = []
    # exemples : .tags a, .tags span, .taglist a
    for t in detail_soup.select(".tags a, .taglist a, .tag"):
        txt = t.get_text(strip=True)
        if txt:
            tags.append(txt)

    return {
        "image_url": absolute(img_url, base) if img_url else None,
        "title": title,
        "tags": tags
    }

def crawl_gallery(start_url, max_pages=MAX_PAGES):
    page_url = start_url
    seen_pages = set()
    images_saved = 0

    # ouvrir CSV
    with open(METADATA_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["detail_url", "image_url", "local_file", "title", "tags"])
        writer.writeheader()

        pages = 0
        while page_url and pages < max_pages and page_url not in seen_pages:
            try:
                print(f"\nVisiting gallery page: {page_url}")
                soup = get_soup(page_url)
            except Exception as e:
                print("Erreur:", e)
                break

            seen_pages.add(page_url)
            pages += 1

            # 1) extraire les liens vers les pages d'item
            items = extract_gallery_items(soup, page_url)
            print(f"Found {len(items)} items on this page.")

            for item_url in items:
                try:
                    print("  -> visiting item:", item_url)
                    detail_soup = get_soup(item_url)
                    info = extract_detail_info(detail_soup, item_url)
                    if not info["image_url"]:
                        print("     pas d'image trouvée, skip")
                        time.sleep(DELAY_BETWEEN_REQUESTS)
                        continue

                    # nom de fichier local
                    parsed = urlparse(info["image_url"])
                    ext = os.path.splitext(parsed.path)[1] or ".jpg"
                    safe_title = sanitize_filename(info["title"] or parsed.path.split("/")[-1])
                    local_name = f"{images_saved:05d}_{safe_title}{ext}"
                    local_path = os.path.join(OUTPUT_DIR, local_name)

                    # télécharger image
                    print("     downloading:", info["image_url"])
                    download_binary(info["image_url"], local_path)
                    print("     saved ->", local_path)

                    # écrire metadata
                    writer.writerow({
                        "detail_url": item_url,
                        "image_url": info["image_url"],
                        "local_file": local_path,
                        "title": info["title"],
                        "tags": "|".join(info["tags"])
                    })
                    images_saved += 1
                    time.sleep(DELAY_BETWEEN_REQUESTS)

                except Exception as e:
                    print("     erreur item:", e)
                    continue

            # trouver la page suivante
            next_page = find_next_page(soup, page_url)
            if next_page and next_page not in seen_pages:
                page_url = next_page
                print("Going to next page:", page_url)
                time.sleep(DELAY_BETWEEN_PAGE)
            else:
                print("No next page found or already visited.")
                break

    print("\nFinished. Images downloaded:", images_saved)

if __name__ == "__main__":
    crawl_gallery(START_URL, max_pages=MAX_PAGES)

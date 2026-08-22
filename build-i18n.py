#!/usr/bin/env python3
"""
eraybalat.com — statik dil sayfası üreteci.

Ana sayfadaki data-tr / data-de çevirilerini HTML'e gömerek /tr/ ve /de/
sayfalarını üretir. Sebep: AI tarayıcıları (GPTBot, ClaudeBot, CCBot) ve
Google'ın bir kısmı JavaScript çalıştırmaz; data-* içinde duran çeviri
onlara görünmez.

Kullanım:  python3 build-i18n.py
Kaynak dosya (index.html) her değiştiğinde yeniden çalıştırılmalı.
"""
import os, re, sys, json
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://eraybalat.com"

# hangi kaynak -> hangi çıktı klasörü
JOBS = [
    {"src": "index.html", "langs": {
        "tr": {"dir": "tr",  "locale": "tr_TR"},
        "de": {"dir": "de",  "locale": "de_DE"},
    }},
]

# dile göre yönlendirilecek linkler (ana sayfadaki setLang mantığının aynısı)
FAQ_HREF  = {"en": "/faq/", "tr": "/sss/", "de": "/faq-de/"}
HIRE_HREF = {"en": "/hire/", "tr": "/yapay-zeka-reklam-filmi/", "de": "/ki-filmproduktion/"}
HOME_HREF = {"en": "/", "tr": "/tr/", "de": "/de/"}

REL_ATTRS = ["src", "poster", "href", "data-poster", "data-src", "data-full", "data-image"]


def lang_meta(html_text):
    """index.html içindeki LANG_META sözlüğünden başlık/açıklama çeker."""
    out = {}
    for lang in ("en", "tr", "de"):
        m = re.search(lang + r":\{t:'((?:[^'\\]|\\.)*)',d:'((?:[^'\\]|\\.)*)'", html_text)
        if m:
            out[lang] = {"t": m.group(1).replace("\\'", "'"),
                         "d": m.group(2).replace("\\'", "'")}
    return out


def absolutise(soup):
    """Göreli yolları köke sabitler — /tr/ bir seviye derinde olduğu için şart."""
    n = 0
    for el in soup.find_all(True):
        for attr in REL_ATTRS:
            v = el.get(attr)
            if not isinstance(v, str) or not v:
                continue
            if v.startswith(("http://", "https://", "//", "/", "#", "mailto:", "tel:", "data:", "javascript:")):
                continue
            el[attr] = "/" + v
            n += 1
    return n


def set_meta(soup, selector_attr, key, value):
    tag = soup.find("meta", {selector_attr: key})
    if tag:
        tag["content"] = value
        return True
    return False


def build(src_rel, lang, cfg, meta_all):
    src_path = os.path.join(ROOT, src_rel)
    raw = open(src_path, encoding="utf-8").read()
    soup = BeautifulSoup(raw, "html.parser")

    # 1) dil kökü
    soup.html["lang"] = lang

    # 2) çevirileri göm
    swapped = 0
    for el in soup.select(f"[data-{lang}]"):
        val = el.get(f"data-{lang}")
        if val is None:
            continue
        frag = BeautifulSoup(val, "html.parser")
        el.clear()
        for child in list(frag.contents):
            el.append(child)
        swapped += 1

    # 3) başlık + açıklama
    m = meta_all.get(lang, {})
    if m.get("t"):
        if soup.title:
            soup.title.string = m["t"]
        set_meta(soup, "property", "og:title", m["t"])
    if m.get("d"):
        set_meta(soup, "name", "description", m["d"])
        set_meta(soup, "property", "og:description", m["d"])
        set_meta(soup, "name", "twitter:description", m["d"])
    set_meta(soup, "property", "og:locale", cfg["locale"])
    url = f"{BASE}/{cfg['dir']}/"
    set_meta(soup, "property", "og:url", url)

    # 4) canonical + hreflang (üç dil karşılıklı)
    for link in soup.find_all("link", rel=lambda r: r and ("canonical" in r or "alternate" in r)):
        if link.get("hreflang") or "canonical" in (link.get("rel") or []):
            link.decompose()
    head = soup.head
    can = soup.new_tag("link", rel="canonical", href=url)
    head.append(can)
    for hl, href in (("en", f"{BASE}/"), ("tr", f"{BASE}/tr/"), ("de", f"{BASE}/de/"), ("x-default", f"{BASE}/")):
        t = soup.new_tag("link", rel="alternate", href=href)
        t["hreflang"] = hl
        head.append(t)

    # 5) göreli yollar
    fixed = absolutise(soup)

    # 6) dile bağlı linkler
    for a in soup.select("a[data-faq]"):
        a["href"] = FAQ_HREF[lang]
    for a in soup.select("a[data-hire]"):
        a["href"] = HIRE_HREF[lang]

    # 7) JSON-LD: sayfa düğümünü bu dile bağla
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string)
        except Exception:
            continue
        for node in data.get("@graph", []):
            if node.get("@type") in ("ProfilePage", "WebPage"):
                node["@id"] = f"{url}#page"
                node["url"] = url
                node["inLanguage"] = lang
        s.string = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    out = str(soup)

    # 8) dil kilidi — JS yüklenince sayfayı başka dile çevirmesin,
    #    dil düğmeleri de swap yerine gerçek URL'e gitsin
    out = re.sub(
        r"document\.querySelectorAll\('\.lang-btn'\)\.forEach\(b=>b\.addEventListener\('click',\(\)=>\{setLang\(b\.dataset\.lang\);.*?\}\)\);",
        "document.querySelectorAll('.lang-btn').forEach(b=>b.addEventListener('click',()=>{"
        "try{localStorage.setItem('lang',b.dataset.lang)}catch(e){}"
        "location.href={en:'/',tr:'/tr/',de:'/de/'}[b.dataset.lang]||'/';}));",
        out, count=1, flags=re.S)
    out = re.sub(
        r"\(function\(\)\{const ok=\['en','tr','de'\];.*?setLang\(l\);\}\)\(\);",
        f"setLang('{lang}');",
        out, count=1, flags=re.S)

    dest_dir = os.path.join(ROOT, cfg["dir"])
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "index.html")
    open(dest, "w", encoding="utf-8").write(out)
    return {"dest": os.path.relpath(dest, ROOT), "swapped": swapped,
            "paths_fixed": fixed, "size_kb": round(len(out) / 1024)}


def main():
    results = []
    for job in JOBS:
        raw = open(os.path.join(ROOT, job["src"]), encoding="utf-8").read()
        meta_all = lang_meta(raw)
        for lang, cfg in job["langs"].items():
            results.append((lang, build(job["src"], lang, cfg, meta_all)))
    for lang, r in results:
        print(f"  {lang} → {r['dest']}  ({r['swapped']} çeviri gömüldü, "
              f"{r['paths_fixed']} yol düzeltildi, {r['size_kb']}KB)")


if __name__ == "__main__":
    main()

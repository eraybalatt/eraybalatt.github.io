#!/usr/bin/env python3
"""
eraybalat.com — statik dil sayfası üreteci.

Ana sayfadaki data-tr çevirilerini HTML'e gömerek /tr/
sayfalarını üretir. Sebep: AI tarayıcıları (GPTBot, ClaudeBot, CCBot) ve
Google'ın bir kısmı JavaScript çalıştırmaz; data-* içinde duran çeviri
onlara görünmez.

Kullanım:  python3 build-i18n.py
Kaynak dosya (index.html) her değiştiğinde yeniden çalıştırılmalı.
"""
import os, re, sys, json, hashlib
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://eraybalat.com"

# hangi kaynak -> hangi çıktı klasörü
JOBS = [
    {"src": "index.html", "langs": {
        "tr": {"dir": "tr",  "locale": "tr_TR"},
    }},
]

# 13 Eki 2026: ek diller. Çeviriler i18n/<dil>.json içinde, anahtar = data-tr taşıyan
# öğenin İngilizce içeriğinin sha1'inin ilk 10 hanesi (İngilizce değişirse o metin İngilizce kalır).
# Sayfalar AI destekli çeviridir; dil menüsünde bu yazıyor.
EXTRA = {
    "fr": {"locale": "fr_FR", "menu": "Menu"},
    "de": {"locale": "de_DE", "menu": "Menü"},
    "it": {"locale": "it_IT", "menu": "Menu"},
    "es": {"locale": "es_ES", "menu": "Menú"},
    "pt": {"locale": "pt_BR", "menu": "Menu"},
    "fi": {"locale": "fi_FI", "menu": "Valikko"},
    "zh": {"locale": "zh_CN", "menu": "菜单"},
    "ja": {"locale": "ja_JP", "menu": "メニュー"},
    "ko": {"locale": "ko_KR", "menu": "메뉴"},
    "ar": {"locale": "ar_AR", "menu": "القائمة", "rtl": True},
    "hi": {"locale": "hi_IN", "menu": "मेनू"},
}
ALL_LANGS = ["en", "tr"] + list(EXTRA)

# dile göre yönlendirilecek linkler (ana sayfadaki setLang mantığının aynısı)
FAQ_HREF  = {"en": "/faq/", "tr": "/sss/"}
HIRE_HREF = {"en": "/hire/", "tr": "/yapay-zeka-reklam-filmi/"}
BLOG_HREF = {"en": "/blog/", "tr": "/yazilar/"}
FILES_HREF = {"en": "/files/", "tr": "/tr/files/"}
HOME_HREF = {"en": "/", "tr": "/tr/"}

REL_ATTRS = ["src", "poster", "href", "data-poster", "data-src", "data-full", "data-image", "data-vid", "data-vid-poster"]


def lang_meta(html_text):
    """index.html içindeki LANG_META sözlüğünden başlık/açıklama çeker."""
    out = {}
    for lang in ("en", "tr"):
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


def load_tmap(lang):
    f = os.path.join(ROOT, "i18n", lang + ".json")
    return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else None


def tkey(html):
    return hashlib.sha1(html.strip().encode()).hexdigest()[:10]


def build(src_rel, lang, cfg, meta_all, tmap=None):
    src_path = os.path.join(ROOT, src_rel)
    raw = open(src_path, encoding="utf-8").read()
    soup = BeautifulSoup(raw, "html.parser")

    # 1) dil kökü
    soup.html["lang"] = lang

    # 2) çevirileri göm
    swapped = 0
    if tmap is not None:
        if cfg.get("rtl"):
            soup.html["dir"] = "rtl"
        for el in soup.select("[data-tr]"):
            val = tmap.get(tkey(el.decode_contents()))
            if not val:
                continue
            frag = BeautifulSoup(val, "html.parser")
            el.clear()
            for child in list(frag.contents):
                el.append(child)
            swapped += 1
        meta_all = dict(meta_all)
        meta_all[lang] = {"t": tmap.get("_meta_t", ""), "d": tmap.get("_meta_d", "")}
        # globe shows the current language
        g = soup.select_one(".lang-globe")
        if g:
            g["class"] = g.get("class", []) + ["active"]
            g["aria-pressed"] = "true"
            code = g.select_one(".lg-code")
            if code:
                code.string = lang.upper()
        for b in soup.select(".lang-btn[data-lang]"):
            b["class"] = [c for c in b.get("class", []) if c != "active"]
            b["aria-pressed"] = "false"
    for el in soup.select(f"[data-{lang}]") if tmap is None else []:
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
    for hl, href in [("en", f"{BASE}/"), ("tr", f"{BASE}/tr/")] + [(l, f"{BASE}/{l}/") for l in EXTRA] + [("x-default", f"{BASE}/")]:
        t = soup.new_tag("link", rel="alternate", href=href)
        t["hreflang"] = hl
        head.append(t)

    # 5) göreli yollar
    fixed = absolutise(soup)

    # 6) dile bağlı linkler
    for a in soup.select("a[data-faq]"):
        a["href"] = FAQ_HREF.get(lang, FAQ_HREF["en"])
    for a in soup.select("a[data-hire]"):
        a["href"] = HIRE_HREF.get(lang, HIRE_HREF["en"])
    for a in soup.select("a[data-blog]"):
        a["href"] = BLOG_HREF.get(lang, BLOG_HREF["en"])
    # Detective mode (/files/) has its own Turkish build at /tr/files/
    for a in soup.select('a[href="/files/"]'):
        a["href"] = FILES_HREF.get(lang, FILES_HREF["en"])

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
        r"document\.querySelectorAll\('\.lang-btn(?:\[data-lang\])?'\)\.forEach\(b=>b\.addEventListener\('click',\(\)=>\{setLang\(b\.dataset\.lang\);.*?\}\)\);",
        "document.querySelectorAll('.lang-btn[data-lang]').forEach(b=>b.addEventListener('click',()=>{"
        "try{localStorage.setItem('lang',b.dataset.lang)}catch(e){}"
        "location.href={en:'/',tr:'/tr/'}[b.dataset.lang]||'/';}));",
        out, count=1, flags=re.S)
    out = re.sub(
        r"\(function\(\)\{const ok=\['en','tr'\];.*?setLang\(l\);\}\)\(\);",
        f"setLang('{lang}');",
        out, count=1, flags=re.S)
    if tmap is not None:
        esc = lambda v: (v or "").replace("\\", "\\\\").replace("'", "\\'")
        meta = (f"LANG_META['{lang}']={{t:'{esc(tmap.get('_meta_t'))}',d:'{esc(tmap.get('_meta_d'))}',"
                f"loc:'{cfg['locale']}',menu:'{esc(cfg['menu'])}'}};")
        out = out.replace("  function setLang(lang){", "  " + meta + "\n  function setLang(lang){", 1)
        aria = ",".join(f"{k[6:]}:'{esc(v)}'" for k, v in tmap.items() if k.startswith("_aria_"))
        out = out.replace("window.__aria=A[lang]||A.en;", f"A['{lang}']={{{aria}}};window.__aria=A[lang]||A.en;", 1)

    dest_dir = os.path.join(ROOT, cfg["dir"])
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "index.html")
    if lang == "tr":
        out = out.replace("/logos/erciyes-tip-en.webp", "/logos/erciyes-tip-tr.webp")
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
        if job["src"] == "index.html":
            for lang, cfg in EXTRA.items():
                tmap = load_tmap(lang)
                if tmap is None:
                    print(f"  {lang}: i18n/{lang}.json yok, atlandı")
                    continue
                c = dict(cfg, dir=lang)
                results.append((lang, build(job["src"], lang, c, meta_all, tmap)))
    for lang, r in results:
        print(f"  {lang} → {r['dest']}  ({r['swapped']} çeviri gömüldü, "
              f"{r['paths_fixed']} yol düzeltildi, {r['size_kb']}KB)")


if __name__ == "__main__":
    main()

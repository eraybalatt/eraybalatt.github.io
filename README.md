# eraybalat.com

Eray Balat'ın portfolyo sitesi — Creative AI Producer & Filmmaker.
Müzik videoları, belgeseller, kısa filmler, UGC/ürün filmleri.

**Canlı:** https://eraybalat.com

> 🔧 Dosyalara dokunmadan önce **[MAINTENANCE.md](MAINTENANCE.md)**'i oku.
> Orada siteyi *sessizce* bozan tuzaklar yazılı — hiçbiri hata vermez, o yüzden bilmeden bulunmaz.

---

## Yapı

```
index.html          ← ana sayfa (HTML + CSS + JS hepsi içinde, derleme yok)
anime/              ← AI Anime Music Video (vaka çalışması)
leather/            ← ÆRAY Atelier — deri ürünler mağazası
bushido/            ← özel kampanya önizlemesi (sitemap'te yok, bilerek)
flawless/           ← FLAWLESS — Antwerp Elmas Soygunu belgeseli
CNAME               ← özel alan adı
sitemap.xml         ← /bushido/ hariç tüm public sayfalar
```

- **Bağımlılık yok, derleme adımı yok.** `index.html`'i tarayıcıda açınca çalışır.
- **Diller:** EN / TR / DE (`data-en` / `data-tr` / `data-de` öznitelikleri)

---

## Yerelde çalıştırma

```bash
python3 -m http.server 8804
```

Sonra `http://localhost:8804` aç.

> Dosyaya çift tıklayıp `file://` ile de açılır ama form, `fetch` ve bazı CSP davranışları farklı çalışır — gerçek testi yerel sunucuyla yap.

---

## Yayına alma

```bash
git add -A
git commit -m "değişiklik açıklaması"
git push origin main
```

GitHub Pages otomatik derler, CDN'e yayılması ~30–60 saniye.

**Doğrula:**

```bash
curl -s "https://eraybalat.com/?cb=$RANDOM" | grep -c "eklediğin-yeni-şey"
```

⚠️ Bir dosyanın **içeriğini** değiştirip **adını** aynı bıraktıysan, `?v=N` numarasını artırmayı unutma — yoksa ziyaretçiler CDN'den eski halini almaya devam eder. Detay: [MAINTENANCE.md](MAINTENANCE.md) → "Tuzaklar" bölümü

---

## Altyapı

| | |
|---|---|
| Barındırma | GitHub Pages + Fastly CDN |
| Alan adı | `CNAME` dosyası → `eraybalat.com` |
| DNS (apex A kayıtları) | `185.199.108.153` · `.109.153` · `.110.153` · `.111.153` |
| Analitik | Cloudflare Web Analytics (sadece beacon — DNS proxy'si **kapalı**) |
| İletişim formu | web3forms |
| E-posta | `eray@eraybalat.com` (Hostinger, `smtp.hostinger.com:465` SSL) |

---

## İçerik güncelleme

- **Renkler:** `index.html` içindeki `:root` bloğu
- **Metinler:** `data-en` / `data-tr` / `data-de` — **üçünü birden** güncelle, yoksa o dil yarım kalır
- **Yeni kart videosu:** `data-poster` desenini kullan (bkz. MAINTENANCE.md), yoksa kart boş görünür

---

## Güvenlik

- GitHub PAT ve Cloudflare API token'ı **asla** commit'lenmez, **asla** `.git/config`'e yazılmaz
- `web3forms access_key` ve Cloudflare **beacon** token'ı publictir — HTML'de durmaları normal

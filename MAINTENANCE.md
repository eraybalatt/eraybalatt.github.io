# Bakım Rehberi — eraybalat.com

Bu dosya kurulum anlatmaz (onun için [README.md](README.md)). Bu dosya **siteyi sessizce bozan şeyleri** anlatır.

Buradaki her madde gerçekten yaşanmış bir hatadır. Hepsinin ortak özelliği şu: **hiçbiri hata vermez.** Sayfa açılır, konsol temiz görünür, sen "oldu" dersin — ama bir şey bozulmuştur ve haftalarca fark edilmez.

---

## 🏗️ Mimari — 30 saniyede

| | |
|---|---|
| **Yapı** | Tek dosya: `index.html` (HTML + CSS + JS içinde). Derleme yok, bağımlılık yok. |
| **Alt sayfalar** | `/anime/` `/leather/` `/bushido/` `/flawless/` — her biri kendi `index.html`'i |
| **Barındırma** | GitHub Pages + Fastly CDN (`via: varnish`) |
| **Diller** | EN / TR / DE — `data-en` / `data-tr` / `data-de` öznitelikleri + `setLang()` |
| **Analitik** | Cloudflare Web Analytics (sadece beacon; DNS proxy'si **kapalı**, site doğrudan GitHub'dan yayınlanıyor) |
| **Form** | web3forms (`access_key` public, sorun değil) |

---

## ☠️ TUZAKLAR — okumadan dosyaya dokunma

### 1. `setLang()` içindeki markup'ı yok eder

`setLang()` şunu yapar:

```js
el.innerHTML = el.dataset[lang];
```

Yani `data-en/tr/de` taşıyan bir elemanın **içindeki her şey silinir** ve düz metinle değiştirilir. İçinde `<a>` veya `<b>` varsa **gider**.

**Gerçekten oldu:** Instagram ve Behance linkleri her sayfa açılışında ölüyordu — İngilizce dahil, çünkü `setLang()` başlangıçta da çalışıyor. Kaynak koda bakınca link duruyor görünüyordu, sadece JS çalıştıktan sonra kayboluyordu. Haftalarca fark edilmedi.

**Kuralı:** `data-*` taşıyan bir elemanın içine link/etiket koyacaksan, markup'ı **üç dilin de** değerine escape'li olarak göm:

```html
<!-- YANLIŞ — link ölür -->
<p data-en="Full series on Instagram" data-tr="..." data-de="...">
  <a href="https://instagram.com/documenteray">Instagram</a>
</p>

<!-- DOĞRU — link her dilde yaşar -->
<p data-en="Full series on &lt;a href=&quot;https://instagram.com/documenteray&quot;&gt;Instagram&lt;/a&gt;"
   data-tr="Tüm seri &lt;a href=&quot;...&quot;&gt;Instagram&lt;/a&gt;'da"
   data-de="...">...</p>
```

Alternatif (daha temiz, metnin tamamı linkse): `data-*`'ı **içteki `<span>`'e** koy, `<a>` dışarıda kalsın.

**Nasıl denetlenir:** her `data-*` değerini unescape edip, elemanın statik içeriğindeki etiketlerle karşılaştır. Markup'ta `<a>` olup değerde olmayan varsa bozuktur.

---

### 2. Dil paritesi bozulursa yarım çeviri çıkar

Şu an tam denge: **`data-en` 172 · `data-tr` 172 · `data-de` 172.**

Bir elemana `data-en` ekleyip `data-tr`/`data-de` eklemezsen, o dile geçen ziyaretçi **İngilizce metin** görür. Hata vermez.

```bash
for a in en tr de; do echo "data-$a: $(grep -o "data-$a=" index.html | wc -l)"; done
# üçü de eşit olmalı
```

---

### 3. İçerik değişince önbellek kırılmalı

CDN dosyaları isimle önbelleğe alır. Bir dosyanın **içeriğini** değiştirip **adını** aynı bırakırsan, ziyaretçiler haftalarca eski hali görür.

**Kural:** içerik değişti mi → ya dosyayı yeniden adlandır, ya `?v=N`'i artır.

Şu an kullanımda: `hero-neon.mp4?v=2`, `konfuse.mp4?v=2`, `feast.mp4?v=2`, `favicon.svg?v=2`, `profile.jpg?v=6` vb.

> Not: `hero-poster.webp` gibi **uzantısı değişenlerde** `?v=` gerekmez — yeni ad zaten yeni dosyadır.

---

### 4. Video sıkıştırınca ses uçar

Kart videolarında hoparlör butonu (`.sndbtn`) var — yani **ses işlevsel içerik**, dekorasyon değil.

**Gerçekten oldu:** `feast.mp4` performans için 10.4MB→3MB sıkıştırıldı, ffmpeg komutunda ses parametresi verilmediği için **AAC akışı uçtu**. ffmpeg hata vermedi, sayfa açıldı, video oynadı — sadece sessizdi. Hoparlör butonu ölü bir düğmeye dönüştü.

**Kural:** yeniden kodlarken `-c:a aac -b:a 96k` ver, sonra **doğrula**:

```bash
ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 dosya.mp4
# boş çıktı = ses gitmiş
```

Tarayıcıda gerçekten çaldığını kanıtlamak için: `video.webkitAudioDecodedByteCount > 0`.

**Meşru sessiz dosyalar — bunları "düzeltme":**
- `hero-neon.mp4` (arka plan döngüsü)
- `directed-by-eray-hero.mp4` (hero logo animasyonu)

---

### 5. CSP dışarıdan kaynak yüklemeyi engeller

`<meta>` CSP'si sıkı. İzinli hostlar:

| Direktif | İzinli |
|---|---|
| `script-src` | `'unsafe-inline'`, static.cloudflareinsights.com |
| `style-src` | `'unsafe-inline'`, fonts.googleapis.com |
| `font-src` | fonts.gstatic.com |
| `img-src` | `data:`, i.ytimg.com |
| `frame-src` | youtube-nocookie.com, youtube.com |
| `connect-src` | api.web3forms.com, cloudflareinsights.com |

Yeni bir CDN/font/API eklersen **CSP'yi de güncelle**, yoksa sessizce bloklanır (sadece konsolda görünür).

⚠️ **Font seçerken:** yeni font Google Fonts'ta olmalı ve **`latin-ext` alt kümesini** desteklemeli. Sitede Türkçe `ı` harfi **140 kez** geçiyor; `latin-ext` yoksa Türkçe sürüm bozulur.

> ⚠️ Kontrol ederken **tam masaüstü User-Agent** kullan. Google Fonts tanımadığı ajana `unicode-range`'siz eski format gönderir — kısa UA ile yaptığım ilk testte Space Grotesk'te `ß` yokmuş gibi göründü, halbuki `latin` alt kümesi (`U+0000-00FF`) içinde.

---

### 6. Yeni kart videosu eklerken lazy-poster desenini uygula

Kart videoları poster'ı **hemen** yüklemez — `data-poster` + IntersectionObserver ile tam zamanında yükler. (Bu, ilk yükü 2.6MB/34 istekten ~160KB/6 isteğe düşüren optimizasyondu.)

```html
<!-- DOĞRU -->
<div class="thumb cover-e">
  <video src="yeni.mp4?v=1" data-poster="yeni-p.jpg" muted loop playsinline preload="none"></video>
</div>
```

`poster=` yazarsan (eager) o dosya her ziyarette hemen iner. `data-poster` yazmayı unutursan kart **boş** kalır.

> Tek istisna: **hero videosu** bilerek `poster=` kullanır (LCP elemanı, hemen görünmeli).

---

### 7. Ekranın üstüne `.reveal` koyma

`.reveal` = `opacity:0` + JS'in IntersectionObserver'ı `.show` ekleyene kadar görünmez.

Ekranın üst kısmındaki (above-the-fold) içeriğe bunu koyarsan, **JS çalışana kadar görünmez** kalır — yavaş cihazda LCP'yi saniyelerce geciktirir. Bu gerçekten oldu: hero başlığı/alt metni/butonları `.reveal` idi, LCP kuyruğunun ana sebebiydi.

**Kural:** üst bölge içeriği → **`.rin`** (JS'siz, saf CSS `@keyframes`). Alt bölgeler → `.reveal` (scroll animasyonu için doğru).

---

## 🚀 Yayına alma

```bash
git add -A
git commit -m "..."
git push origin main
```

CDN'e yayılması ~30–60 sn. Doğrula:

```bash
curl -s "https://eraybalat.com/?cb=$RANDOM" | grep -c "aradığın-yeni-şey"
```

**Güvenlik kuralları:**
- GitHub PAT ve Cloudflare API token'ı **asla** commit'lenmez, **asla** `.git/config`'e yazılmaz. Push inline-PAT URL'iyle yapılır.
- `web3forms access_key` ve Cloudflare **beacon** token'ı publictir — HTML'de durmaları normal.

---

## ⚡ Performans — neden böyle yapıldı

Bunlar keyfi değil, ölçülerek yapıldı. Bozmadan önce oku.

| Karar | Sebep |
|---|---|
| `hero-poster.webp` **preload + `fetchpriority=high`** | LCP elemanı bu. `<video poster>` tarayıcıda **düşük öncelikli** iner — yavaş bağlantıda en sona kalıyordu. |
| Loader `DOMContentLoaded`'da kapanır | Eskiden `window.load` beklerdi; o da fontları + hero videosunu + beacon'ı beklediği için içeriği gereksiz gizliyordu. |
| Hero videosu `window.load`**'dan sonra** yüklenir | 2.3MB'lık video LCP posteriyle bant genişliği için yarışıyordu. |
| Kart videoları `preload="none"` + tıkla-oynat | 28 video otomatik inseydi site kasardı. |
| Görsellerin tamamı `loading="lazy"` | 80/80. |
| Loader görseli inline base64 (176px) | Ekstra HTTP isteği yok. 256px/34KB idi, HTML'i şişiriyordu → 176px/15KB. |

**Sonuç:** LCP P90 15sn → 3.4sn, P99 30sn → 3.6sn, "Poor" oranı %38 → **%0**.

---

## 🎨 Tasarım sistemi

**Renkler** (`:root`):
```
--bg:#080c16  --bg-soft:#0e1626  --text:#eaf2ff  --muted:#8fa3c4
--c1:#5cc8ff  --c2:#2e9bf0   (mavi — ana kimlik)
--c3:#f5c542  --c4:#d99e2b   (citrine altın — MARKA, kaldırılmaz)
```

> **Altın/sarı notu (Ağustos 2026):** ana sayfa + /anime/ + /bushido/ tamamen maviye döndü ("Akdeniz" teması) — oralarda sarı görürsen kalıntıdır, temizle. **Ama `/leather/` (pirinç/zanaat) ve `/flawless/` (elmas/altın) BİLEREK altın kullanır** — tema rengi değil konu rengi. Onları "düzeltme".
> Palet taraması yaparken `getComputedStyle` YETMEZ — box-shadow içi ve gradyan durağındaki rengi göremez. Ham kaynakta `grep -E 'rgba\(2[0-9]{2},2[0-9]{2},1[0-9]{2}'` gibi sıcak-ton araması yap.

**Fontlar — her sayfa bilerek farklı:**

| Sayfa | Font | Neden |
|---|---|---|
| Ana sayfa | **Space Grotesk** + Plus Jakarta Sans | marka fontu (Ağustos 2026'da Poppins'ten geçildi) |
| `/anime/` | Space Grotesk | ana sayfayla bilerek aynı |
| `/leather/` | Cormorant Garamond | el işi/zanaat hissi |
| `/bushido/` | Manrope | kampanya kimliği |
| `/flawless/` | Oswald | belgesel/sinema hissi |

**Selçuklu motifi** (kültürel kimlik işareti) şu an: marka logosu, `.eyebrow::before`, `.slj-divider`, `footer::before`, `header.nav::after`, loader.

**Kenar çubuğu (sidebar):** masaüstünde sol dikey ray, **açık mavi** — bu sahibinin açık tercihi. Kontrast için karartma; bunun yerine yazıya gölge + parlaklık uygulandı.

---

## ✅ Yayınlamadan önce kontrol listesi

```bash
# 1. dil paritesi (üçü eşit olmalı)
for a in en tr de; do echo "data-$a: $(grep -o "data-$a=" index.html | wc -l)"; done

# 2. data-* içindeki linkler hayatta mı (tarayıcıda, setLang sonrası)
#    document.querySelectorAll('.embed-note a').length  -> 0 ise BOZUK

# 3. ses gerekmesi gereken videolarda ses var mı
ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 dosya.mp4

# 4. içerik değişen dosyanın ?v= numarası artırıldı mı

# 5. canlıda doğrula
curl -s "https://eraybalat.com/?cb=$RANDOM" | grep -c "yeni-eklenen-şey"
```

---

*Bu dosya siteyle birlikte yaşamalı. Yeni bir tuzağa düşersen buraya yaz — bir dahakine kimse aynı yere düşmesin.*

---

## 🤖 GEO katmanı (AI görünürlüğü) — Ağustos 2026

Site artık AI modellerine yapılandırılmış veri sunuyor. Parçaları:

| Parça | Ne |
|---|---|
| `robots.txt` | GPTBot, ClaudeBot, PerplexityBot vb. **açık izinli** — birini engellemek = o modelde görünmemek |
| `llms.txt` | Modellere sunulan site özeti — **içerik değişince burayı da güncelle**, yalan söylerse modeller kaynağı güvensiz sayar |
| Ana sayfa JSON-LD | Tek `@graph`: Person `#eray` + ProfessionalService `#studio` + WebSite + ProfilePage. **`@id`'leri bozma** — tüm proje sayfaları bunlara referans verir |
| Proje JSON-LD | flawless (Movie+Video, Rich Results ✓), anime, bushido, leather — hepsi `#eray`/`#website`'e bağlı |
| `/sss/` `/faq/` `/faq-de/` | 3 dilli SSS. **Kural: görünen metin ile FAQPage şeması birebir aynı olmalı.** İçerik değişirse ikisini birlikte değiştir. hreflang zinciri 4'lü (tr/en/de/x-default), üç sayfada aynı |

**Search Console notu (Ağustos 2026):** Ana sayfa `<head>`indeki `google-site-verification` VE `msvalidate.01` (Bing) meta etiketleri + kökteki `BingSiteAuth.xml` **silinmemeli** — silinirse Search Console mülk doğrulaması düşer (sitemap, indeksleme istekleri, performans verisi erişimi gider). Head temizliği yaparken koru.

**Cloudflare notu (Ağustos 2026):** Site şu an Cloudflare **proxy'sinden GEÇMİYOR** (DNS doğrudan GitHub Pages 185.199.x'e gidiyor, yanıtlarda `cf-ray` yok) — bu yüzden Cloudflare'in bot/AI Crawl Control ayarları siteyi **etkileyemez**, dokunmak gerekmez. ⚠️ Ama günün birinde hız için **proxy (turuncu bulut) açılırsa**, aynı gün `dash.cloudflare.com → AI Crawl Control`'a girip TÜM AI botlarını **Allow** yap — varsayılan Block kalırsa robots.txt'deki izinler anlamsızlaşır ve site tüm AI modellerinden kaybolur. Kontrol komutu: `curl -s -o /dev/null -w '%{http_code}' -A GPTBot https://eraybalat.com/` → 200 olmalı.

Şemaya girmeyecekler: doğrulanamayan üstünlük iddiaları ("ilk", "tek"), bilinmeyen rakamlar, sitede olmayan olgular. Bir iddia eklemeden önce sayfada gerçekten yazıyor mu bak.

# eraybalat.com — AI Creative Portfolio

Eray Balat'ın yapay zekâ işleri (müzik, görsel, video, belgesel, kısa film, shorts) için tek sayfalık portföy sitesi.

- Tek dosya: `index.html` (HTML + CSS + JS hepsi içinde)
- Bağımlılık yok, derleme yok — dosyayı açınca çalışır.

## Önizleme (bilgisayarında)
`index.html` dosyasına çift tıkla, tarayıcıda açılır.

## GitHub Pages ile yayına alma

1. GitHub'da yeni bir repo aç (örn. `eraybalat-portfolio` ya da kullanıcı siten için `KULLANICIADIN.github.io`).
2. Bu klasördeki tüm dosyaları repoya yükle (`index.html`, `CNAME`, `.nojekyll`, `README.md`).
3. Repo → **Settings → Pages** → *Branch: main / root* seç → **Save**.
4. Birkaç dakika içinde site `https://KULLANICIADIN.github.io/...` adresinde yayında olur.

## eraybalat.com'u bağlama (custom domain)

`CNAME` dosyası zaten `eraybalat.com` içeriyor. Domain sağlayıcının (GoDaddy, Namecheap vb.) DNS ayarlarına şunları ekle:

**A kayıtları** (apex / `eraybalat.com` için):
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**CNAME kaydı** (`www` için):
```
www  →  KULLANICIADIN.github.io
```

Sonra GitHub → Settings → Pages → *Custom domain* kısmına `eraybalat.com` yaz ve **Enforce HTTPS**'i işaretle. DNS yayılması 10 dk – birkaç saat sürebilir.

## İçeriği güncelleme
`index.html` içindeki kartlarda `href="#"` olan yerlere kendi linklerini, `cover-*` gradyan kapakların yerine gerçek görsel/thumbnail'larını koyabilirsin. Renkleri en üstteki `:root` bloğundan değiştirebilirsin.

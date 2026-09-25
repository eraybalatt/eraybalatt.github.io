/* Eray Balat — pano içeriği, Türkçe (/tr/files/). content.js'in birebir karşılığı:
   anahtarlar aynı, sadece metin Türkçe. content.js değişirse bunu da güncelle. */
window.EB = {
  P: { // projects: cover lines
    flawless:  { t: "FLAWLESS", k: "Belgesel · 16:56 · 4K", role: "Senarist, yönetmen, kurgucu, anlatıcı", href: "/flawless/", hrefLabel: "Vaka çalışmasını oku" },
    coldstart: { t: "COLD START", k: "Bilim kurgu fragmanı · 2:04", role: "Kurgu · ses · renk", sub: "XPRIZE başvurusu", href: "coldstart-film.mp4", hrefLabel: "Fragmanı izle" },
    tenniscut: { t: "TennisCut", k: "Üç marka filmi · 9:16", role: "Yönetmen" },
    bushido:   { t: "Bushido", k: "Kampanya konsepti · sentetik oyuncular", role: "Yönetmen", href: "/bushido/", hrefLabel: "Kampanyayı gör" },
    novora:    { t: "Novora", k: "Animasyon marka filmi · 0:28 · TR / EN", role: "Yönetmen", href: "https://youtu.be/S9hG_Ga7wIg", hrefLabel: "İzle (TR)" },
    konfuse:   { t: "Konfuse", k: "Marka dünyası filmi", role: "Yönetmen", href: "https://youtube.com/shorts/zhqaCtjbwmI", hrefLabel: "YouTube'da izle" },
    music:     { t: "Müzik videoları", k: "Universal Music Türkiye", role: "AI yapımcı" },
    real:      { t: "Gerçek çekim", k: "Kamerayla çekilmiş kısa filmler", role: "Senarist · yönetmen · kurgucu" },
    about:     { t: "Hakkımda", k: "Yönetmen, kurgucu · Kayseri, Türkiye" },
    mark:      { t: "İşaret", k: "Sekiz köşeli Selçuklu yıldızı" },
    contact:   { t: "İletişim", k: "Teslim tarihini ve süreyi gönder" }
  },
  T: { // notes
    "hello": "<b>Merhaba, ben Eray</b>. Kayseri'de yönetmen ve kurgucuyum. Bu panoda bitmiş filmler, onları ortaya çıkaran render'lar, zaman çizelgeleri ve notlarla yan yana duruyor.",
    "howto": "Gezinmek için sürükle. Yakınlaştırmak için iki parmakla aç ya da <b>⌘ + kaydır</b>. Bir çerçeveye çift tıkla. Aramak için <b>⌘K</b>. <b>▶ Tur</b> seni baştan sona gezdirir.",
    "tz": "Türkiye'de ve ABD'de müşterilerim var. Kayseri, San Francisco'dan <b data-tz>10 saat</b> ileride: akşam gönderdiğin notlar sen uyurken işlenir.",

    "fl.interview": "2003 soygununu Leonardo Notarbartolo yönetti. Onunla görüntülü görüşmede İtalyanca röportaj yaptım. Filmi izledikten sonra şunu yazdı: <b>“Ti sono grato per il documentario, mi piace molto.”</b> (Belgesel için sana minnettarım, çok beğendim.)",
    "fl.voice": "İngilizce anlatım benim sesimle, İtalyanca dublajın tamamı <b>klonlanmış sesimle</b> (ElevenLabs). Altyazılarla altı dile çıkıyor.",
    "fl.3d": "Kasayı, sensörleri ve kaçışı yeniden kuran <b>30'dan fazla özel 3D sahne</b>. 3D ve AI görseller: Berkay Efe Balat.",
    "fl.motion": "<b>35 hareketli grafik</b>. Motion tasarım: Hasan.",
    "fl.parts": "Beş bölüm: <b>Plan, Soygun, Kaçış, Hata, Şimdi Nerede.</b>",
    "fl.edit": "Premiere Pro'da kurgulandı. Ana zaman çizelgesi <b>sekiz video kanalı</b> derinliğinde.",
    "fl.thumbs": "Yayından önce küçük resim testleri.",
    "fl.credits": "Senaryo, yönetmenlik, kurgu ve anlatım benim. Görüntü iyileştirme: Magnific. Müzik lisansı: Epidemic Sound.",

    "cs.in": "<b>Gelen:</b> müşteriden 35 üretilmiş klip ve 8 ses dosyası.",
    "cs.out": "<b>Çıkan:</b> 2:04'lük bir fragman. Kurgu, conform, ses tasarımı, miks, renk, müzik, altyazı.",
    "cs.upscale": "Topaz'da büyütme: <b>1280×720 → 2560×1440</b>, kare ara değerleme kapalı.",
    "cs.colour": "Kurgu boyunca tek bir soğuk renk kimliği; birkaç sıcak vurgu bilerek bırakıldı.",
    "cs.silence": "Tam ortada <b>2,1 saniyelik</b> mutlak sessizlik. Bilerek yerleştirildi.",
    "cs.master": "Master: 1920×1080, 24 fps, <b>−15,7 LUFS</b>, −1,4 dBTP. ProRes 422 HQ arşiv.",
    "cs.licence": "<b>Onaydan önce:</b> 28 stok lisansı denetlendi, 7'si başka proje adlarıyla kayıtlı çıktı ve yeniden kaydedildi. Müşteriye o sormadan haber verildi.",
    "cs.review": "“Kaçırdığım devamlılık ve tempo sorunlarını yakaladı. Onunla hiç düşünmeden yeniden çalışırım.”",


    "tc.films": "Bir tenis uygulaması için üç dikey film: <b>The Moment, Dead Time Remover, Best of Us.</b>",
    "tc.stills": "Best of Us önce karelerle kuruldu: çift, onaylanmış karelerde sabitlendi, sonra <b>Kling</b>'de plan plan canlandırıldı.",
    "tc.ui": "Telefon ekranları boş üretildi. Gerçek uygulama arayüzü <b>After Effects</b>'te eklendi.",
    "tc.team": "Bazı hareketli klipler Berkay Efe Balat'tan. Best of Us'ın <b>özgün müziği</b> var.",

    "bu.what": "İki kişilik sentetik kadro (<b>Ayla ve Kaan</b>), 4K ürün kapsülü, üç dikey film ve özgün müzik.",
    "bu.cast": "İkisi de bir ana portre ve bir karakter sayfasından kuruldu, sonra üç filmin hepsinde aynı kaldı: <b>Her Ritual, His Ritual, The Reel</b>.",

    "nv.what": "Bursa Sölöz'deki bir zeytin üreticisi için 28 saniyelik animasyon pilot. Türkçe ve İngilizce, 4K ve 1080p. <b>Bir gün erken teslim edildi.</b>",

    "kf.what": "Deri bir seyahat çantası için <b>özgün müzikli</b> bir marka dünyası filmi.",
    "kf.world": "Her planda tek bir dünya: dağlar, beyaz bir at, derinin üstüne işlenmiş manzara.",

    "mv.what": "<b>Universal Music Türkiye</b>'nin yayınladığı <b>Modd</b> resmî müzik videoları. AI yapımcılar: Eray ve Berkay Efe Balat.",

    "rf.what": "Kamerayla çekildi. AI yok. Film gerektirdiğinde hâlâ çekiyorum.",
    "rf.swiss": "<b>Switzerland in One Hour</b> · bir saatlik meydan okuma, kamera arkasındaki ilk günümde çekildi",
    "rf.run": "<b>Run or Run</b> · senarist, yönetmen, oyuncu · 2:34",
    "rf.post": "<b>Die Post</b> · Erciyes Üniversitesi · senarist, yönetmen, yapımcı",
    "rf.boom": "<b>Boomerang</b> · kurgucu · Mansiyon, Student Video Contest 2026 · Duemila30'da seçildi",

    /* the wall: TennisCut as the lead case */
    "tc.brief": "Tenis maçını kaydedip sadece ralliler kalana kadar kısaltan bir uygulama için üç lansman reklamı. 9:16, İngilizce. <b>Bir duygu filmi, bir kanıt filmi, bir hikâye filmi.</b>",
    "tc.study": "Tek kare yazmadan önce markanın <b>mevcut 16 reklamını</b> izledim. Aldıklarım: ilk saniyelerde bir yüz ve bir kanca, ekranda yazı, hep aynı kapanış kartı.",
    "tc.grades": "Üç renk düzeni: <b>gece arenası</b>, nötr gün ışığı ve <b>açık mavi kortun üstünde gün batımı ışığı</b>.",
    "tc.credits": "Kareler ve bazı Kling klipleri: <b>Berkay Efe Balat</b>. Yönetmenlik, kurgu, ses ve renk: Eray. Best of Us'ta özgün müzik.",
    "tc.hook": "İlk saniye ses kapalıyken de çalışmalı: <b>“You’ll only remember ONE POINT.”</b> Kelime kelime, markanın mercan renginde.",
    "tc.serve": "AI tenis görüntülerinde raket topa nadiren değer. <b>Servis, değene kadar yeniden üretildi</b>; parlama ve vuruş sesi o karede.",
    "tc.proof": "Müşterinin gerçek maç kayıtları, üretilmiş planlarla birlikte kurgulandı. İki saatlik maç <b>27:09</b>'a iniyor: “Every grey block gets deleted.”",
    "tc.screens": "Her uygulama ekranı <b>gerçek bir uygulama kaydı</b>, After Effects'te yerleştirildi.",
    "tc.lock": "Çift, <b>hiçbir hareketten önce</b> referans karelerde sabitlendi, sonra Kling'de plan plan canlandırıldı.",
    "nv.open": "“Bazı hikâyeler bir toprakla başlar, <b>İznik Gölü kıyısında, Sölöz'de.</b>” Anlatımın ilk cümlesi.",
    "nv.nova": "Küçük siyah kuş Nova'nın bir kahraman pozu ve dönüş sayfası var, böylece <b>her sahnede aynı kuş</b>.",
    "nv.sb": "Önce storyboard. Film ona <b>kare kare</b> uyuyor.",
    "nv.end": "Türkçe ve İngilizce anlatım, aynı sesle. Son cümle: <b>“Sağlık köklerinde.”</b>",
    "fd.what": "İşlemeli deri bir seyahat çantası için moda filmi. Yönetmenlik ve <b>özgün müzik</b>.",
    "fd.world": "Her planda tek bir dünya: hilal altında dağlar, beyaz bir at ve <b>derinin üstüne işlenmiş aynı manzara</b>.",
    "ab.bio": "Erciyes Üniversitesi'nde sinema okuyorum. Filmlerimin çoğu üretilmiş görüntüden kuruluyor; asıl iş onu tek bir film gibi bir arada tutmak. Kurgu, ses, renk ve müzik evde bitiyor.",
    "ab.tools": "Nano Banana · Kling · Seedance · Flora · Firefly · Topaz · ElevenLabs · Suno · Premiere Pro · After Effects · Photoshop",
    "ab.suno": "Suno'da <b>5.500'den fazla şarkı</b>. Suno Ambassador, 2025.",
    "ab.clients": "Universal Music Türkiye · TennisCut · Novora · Konfuse",

    "mk.what": "Sekiz köşeli bir Selçuklu yıldızı: sekiz kez birbirinin üstünden ve altından geçen bir kare ve bir eşkenar dörtgen. Kayseri'deki Selçuklu taş işçiliğinde bu yıldızlar her yerde.",

    "ct.what": "Sana kapsamı ve sabit fiyatlı bir teklifi dönerim. Ticari haklar teslimde devredilir.",
    "ct.links": "<a href='/yapay-zeka-reklam-filmi/'>Fiyatlar</a> · <a href='https://www.instagram.com/documenteray/' target='_blank' rel='noopener'>Instagram</a> · <a href='https://www.linkedin.com/in/eraybalat/' target='_blank' rel='noopener'>LinkedIn</a> · <a href='https://www.youtube.com/@eraybalat' target='_blank' rel='noopener'>YouTube</a> · <a href='https://www.upwork.com/freelancers/eraybalat' target='_blank' rel='noopener'>Upwork</a>"
  },
  STAR: ["M51.971 18.029L60 10L88.749 38.749", "M24.64 36.01L24.64 24.64L65.29 24.64", "M101.971 51.971L110 60L81.251 88.749", "M83.99 24.64L95.36 24.64L95.36 65.29", "M68.029 101.971L60 110L31.251 81.251", "M95.36 83.99L95.36 95.36L54.71 95.36", "M18.029 68.029L10 60L38.749 31.251", "M36.01 95.36L24.64 95.36L24.64 54.71"],
  star: function (sw) { return "<svg viewBox='0 0 120 120' fill='none' stroke='currentColor' stroke-width='" + (sw || 6) + "' stroke-linecap='butt' stroke-linejoin='miter' aria-hidden='true'>" + EB.STAR.map(function (d) { return "<path d='" + d + "'/>"; }).join("") + "</svg>"; },
  tz: function () {
    try {
      var n = new Date(), f = function (z) { var p = new Intl.DateTimeFormat("en-US", { timeZone: z, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }).formatToParts(n), o = {}; p.forEach(function (x) { o[x.type] = x.value; }); return Date.UTC(+o.year, +o.month - 1, +o.day, +o.hour, +o.minute); };
      var h = Math.round((f("Europe/Istanbul") - f("America/Los_Angeles")) / 36e5);
      document.querySelectorAll("[data-tz]").forEach(function (e) { e.textContent = h + " saat"; });
    } catch (e) { }
  }
};

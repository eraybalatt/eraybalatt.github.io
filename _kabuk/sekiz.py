#!/usr/bin/env python3
"""_y3 (Kunye) yonunun sekiz tipografi + renk sistemi.

Her biri farkli bir yazi ailesi ciftiyle kurulu. Ortak olan tek sey yapi:
gorselsiz acilis, tek cumlelik beyan, zenginlestirilmis proje dizini.

_k1 MATBAA    Bodoni Moda + Newsreader        kurşun gri / mürekkep
_k2 TERMINAL  JetBrains Mono                  kömür / fosfor kehribar
_k3 AFIS      Archivo Black + Archivo         kireç beyazı / sinyal kırmızısı
_k4 MUREKKEP  Fraunces + Public Sans          çivit / ham beyaz
_k5 MUZE      Instrument Serif + Work Sans    taş / şişe yeşili
_k6 JENERIK   Oswald + Barlow                 saf siyah / beyaz
_k7 MIMARI    Chivo + IBM Plex Sans           ozalit mavisi / lacivert
_k8 DERGI     Anton + Lora                    kum / mürekkep moru
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / '_y3.html').read_text(encoding='utf-8')

HOME_RE = re.compile(r'id="home">[\s\S]*?</section>')
m0 = HOME_RE.search(s0)
assert m0, '#home bulunamadi'

# ── projeler: baslik · rol · musteri/tur · yil ─────────────────────────
ISLER = [
 ('#docs',     'FLAWLESS', 'The Antwerp Diamond Heist',
               'Director · Writer · Editor', 'Documentary', '2026'),
 ('#music',    'Modd', 'real life / yok uyku',
               'AI Creator', 'Universal Music Türkiye', '2026'),
 ('#docs',     'COLD START', 'XPRIZE',
               'Editor', 'Trailer', '2026'),
 ('#ugc',      'Konfuse', 'Brand World Film',
               'Director', 'Brand film · original score', '2026'),
 ('#shorts',   'Tesadüf Değil', '7 bölüm · 106 kare',
               'Producer · Director', 'Short film', '2026'),
 ('#ugc',      'TennisCut', 'The Moment · Best of Us',
               'Director', 'Performance ads · Meta', '2026'),
 ('#prodphoto','Doqu Home', 'Bellona',
               'Director', 'Product · Furniture', '2025'),
 ('#brands',   'Novora', 'Sağlık Köklerinde',
               'Director', 'Brand film · TR & EN', '2026'),
]

def index_html():
    rows = []
    for i, (href, ad, alt, rol, tur, yil) in enumerate(ISLER, 1):
        rows.append(
          '<li><a href="%s">'
          '<span class="n">%02d</span>'
          '<span class="t"><b>%s</b><i>%s</i></span>'
          '<span class="r">%s</span>'
          '<span class="c">%s</span>'
          '<span class="y">%s</span>'
          '</a></li>' % (href, i, ad, alt, rol, tur, yil))
    return '\n        '.join(rows)

HERO = '''id="home">
    <div class="kx-in">
      <p class="kx-state" data-en="I direct film for brands and artists. I work from Kayseri, Türkiye, and almost everyone I work with is somewhere else." data-tr="Markalar ve sanatçılar için film yönetiyorum. Kayseri'de çalışıyorum, birlikte çalıştığım hemen herkes başka bir yerde." data-de="Ich inszeniere Filme für Marken und Künstler. Ich arbeite aus Kayseri, und fast alle meine Auftraggeber sind anderswo.">I direct film for brands and artists. I work from Kayseri, Türkiye, and almost everyone I work with is somewhere else.</p>
      <div class="kx-hd"><span data-en="Selected work" data-tr="Seçilmiş işler" data-de="Ausgewählte Arbeiten">Selected work</span><span data-en="2025 — 2026" data-tr="2025 — 2026" data-de="2025 — 2026">2025 — 2026</span></div>
      <ol class="kx-ix">
        %s
      </ol>
      <div class="kx-cta">
        <a href="#music" class="btn btn-grad" data-en="Watch my work →" data-tr="İşlerimi İzle →" data-de="Meine Arbeiten ansehen →">Watch my work →</a>
        <a href="#contact" class="btn btn-ghost" data-en="Start a project →" data-tr="Proje başlat →" data-de="Projekt starten →">Start a project →</a>
      </div>
    </div>
  </section>''' % index_html()

# ── ortak iskelet: yalnizca degiskenlerle boyanir ──────────────────────
SHELL = '''
:root{
  --bg:%(bg)s; --bg-soft:%(bg2)s; --text:%(ink)s; --muted:%(mut)s;
  --card:%(cardbg)s; --card-brd:%(rule)s;
  --rule:%(rule)s; --rule-2:%(rule2)s; --plate:%(plate)s;
  --ink:%(ink)s; --ink-2:%(ink2)s; --ink-3:%(mut)s;
  --acc:%(acc)s;
}
body{background:var(--bg);color:var(--text);font-family:%(body)s}

/* header */
header.nav::before{ background:%(navgrad)s !important; -webkit-mask:none !important; mask:none !important }
header.nav::after{ background:var(--grain) 0 0/140px repeat,var(--plate) !important }
header.nav{ background:none !important; border-bottom:1px solid var(--rule) !important;
            box-shadow:0 6px 26px -22px %(shadow)s !important; color:var(--ink) }
header.nav .brand-wm b{ font-family:%(disp)s; color:var(--ink) !important;
            -webkit-text-fill-color:var(--ink) !important; %(brandtype)s }
header.nav .brand-wm i{ color:var(--muted); letter-spacing:.2em }
header.nav .brand::before{ background:linear-gradient(180deg,var(--acc),%(acc_fade)s) }
.nav-links a,.nav-work a,.lang-btn,.avail{ color:var(--ink-2) }
.nav-links a.active{ --nd:var(--acc); color:var(--ink) }
.lang-btn,.lang-btn *{ color:var(--muted) !important }
.lang-btn[aria-pressed="true"],.lang-btn.active{ color:var(--ink) !important; font-weight:700 }
.nav-toggle span,.nav-toggle::before,.nav-toggle::after{ background:var(--ink) }
.avail{ border-color:var(--rule-2) }

/* acilis */
.hero{ min-height:auto; padding:calc(var(--row1,56px) + %(padtop)s) max(22px,5vw) 8vh;
       text-align:left; align-items:flex-start; justify-content:flex-start }
.kx-in{ width:100%%; max-width:%(maxw)s }
.kx-state{
  font-family:%(disp)s; %(statetype)s
  color:var(--ink); margin:0 0 clamp(34px,6vh,64px); text-wrap:balance;
}

/* dizin basligi */
.kx-hd{
  display:flex; justify-content:space-between; align-items:baseline;
  font-family:%(mono)s; font-size:10px; letter-spacing:.26em; text-transform:uppercase;
  color:var(--muted); padding-bottom:10px; border-bottom:1.5px solid var(--rule-2);
}

/* dizin */
.kx-ix{ list-style:none; margin:0 0 44px; padding:0 }
.kx-ix li{ border-bottom:1px solid var(--rule) }
.kx-ix a{
  display:grid; grid-template-columns:auto 1fr auto auto auto; gap:0 22px;
  align-items:baseline; padding:16px 2px; text-decoration:none; color:inherit;
  transition:background .28s, padding .28s;
}
.kx-ix a:hover,.kx-ix a:focus-visible{ background:var(--card); padding-left:12px; padding-right:12px }
.kx-ix .n{ font-family:%(mono)s; font-size:11px; font-weight:600; letter-spacing:.1em; color:var(--acc) }
.kx-ix .t b{ display:block; font-family:%(disp)s; %(titletype)s color:var(--ink) }
.kx-ix .t i{ display:block; font-style:normal; font-size:13px; color:var(--muted); margin-top:3px }
.kx-ix .r,.kx-ix .c,.kx-ix .y{
  font-family:%(mono)s; font-size:10px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--muted); white-space:nowrap;
}
.kx-ix .r{ color:var(--ink-2) }
@media(max-width:1020px){
  .kx-ix a{ grid-template-columns:auto 1fr auto; row-gap:6px }
  .kx-ix .r{ grid-column:2; grid-row:2 } .kx-ix .c{ display:none }
}
@media(max-width:600px){
  .kx-ix a{ grid-template-columns:auto 1fr }
  .kx-ix .y{ grid-column:2; grid-row:3 }
}

/* butonlar */
.kx-cta{ display:flex; flex-wrap:wrap; gap:28px }
.btn-grad{ color:var(--ink); text-shadow:none; font-family:%(mono)s; letter-spacing:.06em }
.btn-grad::after{ background:var(--acc); box-shadow:none; height:2px }
.btn-ghost{ color:var(--muted); font-family:%(mono)s; letter-spacing:.06em }

/* ayraclar ve loader */
.slj-divider .slj-tag{ font-family:%(mono)s; color:var(--muted) }
.slj-divider .slj-line{ background:linear-gradient(90deg,transparent,var(--rule-2)) }
.slj-divider .slj-line:last-child{ background:linear-gradient(90deg,var(--rule-2),transparent) }
.loader{ background:var(--bg) } .loader-word{ font-family:%(disp)s; color:var(--acc) }
.trust-label{ color:var(--muted) !important }
#trust,#trust *,.trust,.trust *{ color:var(--ink-2) }
%(extra)s
'''

# ── sekiz sistem ──────────────────────────────────────────────────────
V = [
dict(f='_k1.html', ad='MATBAA', not_='Bodoni Moda + Newsreader · kurşun gri',
  fonts='Bodoni+Moda:opsz,wght@6..96,500;6..96,700&family=Newsreader:opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Mono:wght@400;500;600',
  disp="'Bodoni Moda',Georgia,serif", body="'Newsreader',Georgia,serif", mono="'IBM Plex Mono',monospace",
  bg='#e8e6e1', bg2='#dbd8d1', ink='#141310', ink2='#3a3733', mut='#78736b',
  rule='rgba(20,19,16,.14)', rule2='rgba(20,19,16,.3)', cardbg='rgba(20,19,16,.04)',
  plate='rgba(232,230,225,.985)', acc='#8c2f1f', acc_fade='rgba(140,47,31,.12)',
  navgrad='linear-gradient(180deg,rgba(232,230,225,.97),rgba(232,230,225,.6))',
  shadow='rgba(0,0,0,.5)', maxw='1060px', padtop='9vh',
  brandtype='letter-spacing:.14em;font-weight:700',
  statetype='font-size:clamp(1.5rem,3.6vw,2.7rem);line-height:1.22;font-weight:500;max-width:20ch;',
  titletype='font-size:clamp(1.05rem,2.2vw,1.42rem);font-weight:700;letter-spacing:.01em;', extra=''),

dict(f='_k2.html', ad='TERMİNAL', not_='JetBrains Mono · kömür / fosfor',
  fonts='JetBrains+Mono:wght@400;500;700',
  disp="'JetBrains Mono',monospace", body="'JetBrains Mono',monospace", mono="'JetBrains Mono',monospace",
  bg='#0d0d0c', bg2='#161615', ink='#e4dfd2', ink2='#c9c2b2', mut='#8a8376',
  rule='rgba(228,223,210,.13)', rule2='rgba(228,223,210,.26)', cardbg='rgba(255,176,58,.07)',
  plate='rgba(13,13,12,.985)', acc='#ffb03a', acc_fade='rgba(255,176,58,.12)',
  navgrad='linear-gradient(180deg,rgba(13,13,12,.96),rgba(13,13,12,.55))',
  shadow='rgba(0,0,0,.9)', maxw='1000px', padtop='8vh',
  brandtype='letter-spacing:.2em;font-weight:700',
  statetype='font-size:clamp(1.05rem,2.3vw,1.6rem);line-height:1.5;font-weight:400;max-width:52ch;',
  titletype='font-size:clamp(.98rem,2vw,1.22rem);font-weight:700;letter-spacing:.04em;',
  extra='.kx-ix .n::before{content:"[";color:var(--mut)}.kx-ix .n::after{content:"]";color:var(--mut)}'),

dict(f='_k3.html', ad='AFİŞ', not_='Archivo Black · kireç / sinyal kırmızısı',
  fonts='Archivo+Black&family=Archivo:wght@400;500;600&family=Archivo:wght@600',
  disp="'Archivo Black',Impact,sans-serif", body="'Archivo',Helvetica,sans-serif", mono="'Archivo',sans-serif",
  bg='#f7f6f2', bg2='#eceae3', ink='#0b0b0b', ink2='#2e2e2e', mut='#767676',
  rule='rgba(11,11,11,.15)', rule2='rgba(11,11,11,.85)', cardbg='rgba(228,30,20,.06)',
  plate='rgba(247,246,242,.985)', acc='#e41e14', acc_fade='rgba(228,30,20,.1)',
  navgrad='linear-gradient(180deg,rgba(247,246,242,.97),rgba(247,246,242,.6))',
  shadow='rgba(0,0,0,.45)', maxw='1100px', padtop='8vh',
  brandtype='letter-spacing:.04em;font-weight:400',
  statetype='font-size:clamp(1.8rem,5vw,3.6rem);line-height:1.04;font-weight:400;letter-spacing:-.02em;max-width:17ch;text-transform:uppercase;',
  titletype='font-size:clamp(1.05rem,2.3vw,1.5rem);font-weight:400;letter-spacing:-.01em;text-transform:uppercase;',
  extra='.kx-ix .n{font-size:15px;font-weight:600}.kx-hd{border-bottom-width:3px}'),

dict(f='_k4.html', ad='MÜREKKEP', not_='Fraunces + Public Sans · çivit',
  fonts='Fraunces:opsz,wght@9..144,400;9..144,600&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500',
  disp="'Fraunces',Georgia,serif", body="'Public Sans',Helvetica,sans-serif", mono="'IBM Plex Mono',monospace",
  bg='#141a35', bg2='#1d254a', ink='#f0ece1', ink2='#d6d0c2', mut='#8f8ca3',
  rule='rgba(240,236,225,.14)', rule2='rgba(240,236,225,.3)', cardbg='rgba(240,236,225,.05)',
  plate='rgba(20,26,53,.985)', acc='#e8b04b', acc_fade='rgba(232,176,75,.12)',
  navgrad='linear-gradient(180deg,rgba(20,26,53,.96),rgba(20,26,53,.55))',
  shadow='rgba(0,0,0,.8)', maxw='1020px', padtop='9vh',
  brandtype='letter-spacing:.12em;font-weight:600',
  statetype='font-size:clamp(1.5rem,3.7vw,2.75rem);line-height:1.2;font-weight:400;max-width:19ch;',
  titletype='font-size:clamp(1.05rem,2.2vw,1.45rem);font-weight:600;', extra=''),

dict(f='_k5.html', ad='MÜZE', not_='Instrument Serif + Work Sans · taş / yeşil',
  fonts='Instrument+Serif:ital@0;1&family=Work+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500',
  disp="'Instrument Serif',Georgia,serif", body="'Work Sans',Helvetica,sans-serif", mono="'IBM Plex Mono',monospace",
  bg='#e5e2d9', bg2='#d7d3c7', ink='#14261c', ink2='#33473a', mut='#6f7d72',
  rule='rgba(20,38,28,.15)', rule2='rgba(20,38,28,.32)', cardbg='rgba(20,38,28,.045)',
  plate='rgba(229,226,217,.985)', acc='#1d5c3a', acc_fade='rgba(29,92,58,.12)',
  navgrad='linear-gradient(180deg,rgba(229,226,217,.97),rgba(229,226,217,.6))',
  shadow='rgba(0,0,0,.45)', maxw='1040px', padtop='10vh',
  brandtype='letter-spacing:.1em;font-weight:400',
  statetype='font-size:clamp(1.7rem,4.4vw,3.1rem);line-height:1.14;font-weight:400;max-width:18ch;',
  titletype='font-size:clamp(1.15rem,2.5vw,1.6rem);font-weight:400;', extra=''),

dict(f='_k6.html', ad='JENERİK', not_='Oswald + Barlow · saf siyah',
  fonts='Oswald:wght@300;400;600&family=Barlow:wght@400;500&family=Barlow+Condensed:wght@500;600',
  disp="'Oswald',Impact,sans-serif", body="'Barlow',Helvetica,sans-serif", mono="'Barlow Condensed',sans-serif",
  bg='#000000', bg2='#0c0c0c', ink='#ffffff', ink2='#d6d6d6', mut='#8a8a8a',
  rule='rgba(255,255,255,.15)', rule2='rgba(255,255,255,.34)', cardbg='rgba(255,255,255,.06)',
  plate='rgba(0,0,0,.985)', acc='#ffffff', acc_fade='rgba(255,255,255,.1)',
  navgrad='linear-gradient(180deg,rgba(0,0,0,.96),rgba(0,0,0,.5))',
  shadow='rgba(0,0,0,1)', maxw='1000px', padtop='11vh',
  brandtype='letter-spacing:.22em;font-weight:400',
  statetype='font-size:clamp(1.35rem,3.2vw,2.3rem);line-height:1.3;font-weight:300;letter-spacing:.02em;max-width:26ch;',
  titletype='font-size:clamp(1.1rem,2.4vw,1.55rem);font-weight:400;letter-spacing:.06em;text-transform:uppercase;',
  extra='.kx-ix .r,.kx-ix .c,.kx-ix .y{letter-spacing:.2em;font-size:11px}'),

dict(f='_k7.html', ad='MİMARİ', not_='Chivo + IBM Plex Sans · ozalit',
  fonts='Chivo:wght@400;700;900&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500',
  disp="'Chivo',Helvetica,sans-serif", body="'IBM Plex Sans',Helvetica,sans-serif", mono="'IBM Plex Mono',monospace",
  bg='#dfe6ea', bg2='#cfd9df', ink='#0f2336', ink2='#2d4459', mut='#6b8092',
  rule='rgba(15,35,54,.16)', rule2='rgba(15,35,54,.34)', cardbg='rgba(15,35,54,.05)',
  plate='rgba(223,230,234,.985)', acc='#0a5ea8', acc_fade='rgba(10,94,168,.12)',
  navgrad='linear-gradient(180deg,rgba(223,230,234,.97),rgba(223,230,234,.6))',
  shadow='rgba(0,0,0,.4)', maxw='1120px', padtop='8vh',
  brandtype='letter-spacing:.1em;font-weight:900',
  statetype='font-size:clamp(1.4rem,3.4vw,2.5rem);line-height:1.22;font-weight:700;max-width:21ch;letter-spacing:-.01em;',
  titletype='font-size:clamp(1.02rem,2.1vw,1.36rem);font-weight:700;letter-spacing:-.005em;',
  extra='.kx-ix a{border-left:2px solid transparent}.kx-ix a:hover{border-left-color:var(--acc)}'),

dict(f='_k8.html', ad='DERGİ', not_='Anton + Lora · kum / mürekkep moru',
  fonts='Anton&family=Lora:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500',
  disp="'Anton',Impact,sans-serif", body="'Lora',Georgia,serif", mono="'IBM Plex Mono',monospace",
  bg='#ece5d8', bg2='#dfd6c4', ink='#1c1524', ink2='#3b2f48', mut='#7a6e83',
  rule='rgba(28,21,36,.15)', rule2='rgba(28,21,36,.32)', cardbg='rgba(93,48,140,.06)',
  plate='rgba(236,229,216,.985)', acc='#5d308c', acc_fade='rgba(93,48,140,.12)',
  navgrad='linear-gradient(180deg,rgba(236,229,216,.97),rgba(236,229,216,.6))',
  shadow='rgba(0,0,0,.45)', maxw='1080px', padtop='8vh',
  brandtype='letter-spacing:.06em;font-weight:400',
  statetype='font-size:clamp(2rem,5.4vw,3.9rem);line-height:1.02;font-weight:400;max-width:16ch;text-transform:uppercase;letter-spacing:.005em;',
  titletype='font-size:clamp(1.1rem,2.4vw,1.55rem);font-weight:400;text-transform:uppercase;letter-spacing:.015em;',
  extra='.kx-ix .n{font-family:%s;font-size:20px;color:var(--acc);opacity:.55}' % "'Anton',sans-serif"),
]

for v in V:
    s = s0[:m0.start()] + HERO + s0[m0.end():]
    # fontlari head'e ekle
    link = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=%s&display=swap">'
            % v['fonts'])
    s = s.replace('<title>', link + '\n<!-- KABUK: %s — %s -->\n<title>' % (v['ad'], v['not_']), 1)
    i = s.rfind('</style>')
    s = s[:i] + '\n/* ===== %s ===== */\n' % v['ad'] + (SHELL % v) + '\n' + s[i:]
    (ROOT / v['f']).write_text(s, encoding='utf-8')
    print('%-10s %-10s %-42s %7d bayt' % (v['f'], v['ad'], v['not_'], len(s)))

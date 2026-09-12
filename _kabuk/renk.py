#!/usr/bin/env python3
"""_a2.html tabaninda 4 varyant: 2 Selcuklu mavisi x 2 hero isleyisi.

Renk  A  Cini Turkuazi — turkuaz butun sayfaya yayilir, zemin de teale kayar
Renk  B  Cini Laciverti — zemin derin lapis, turkuaz yalnizca vurgu olarak girer

Tip   1  Film onde  — hero videosu acilir (.34 -> .52), ortu incelir
Tip   2  Murekkep onde — video geri ceker (.34 -> .20), renk ortusu ve tipografi tasir

_r1 A1 · _r2 A2 · _r3 B1 · _r4 B2
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
SRC  = ROOT / '_a2.html'
s0   = SRC.read_text(encoding='utf-8')

VIDEO  = 'hero-anime.mp4'
POSTER = 'hero-anime-poster.webp'

# ---------------------------------------------------------------- hero videosu
def swap_video(s):
    old = ('<video class="hero-bg" id="heroVid" autoplay muted loop playsinline '
           'preload="none" poster="hero-poster.webp" data-src="hero-neon.mp4?v=2"></video>')
    assert s.count(old) == 1, 'hero video tekil degil: %d' % s.count(old)
    new = ('<video class="hero-bg" id="heroVid" autoplay muted loop playsinline '
           'preload="none" poster="%s" data-src="%s"></video>' % (POSTER, VIDEO))
    return s.replace(old, new, 1)

# ---------------------------------------------------------------- renkler
# Mevcut "morumsu" mavi ailesi: #1a86d8 · rgba(46,155,240) · #2ba2d4
RENK = {
'A': dict(
  ad='Çini Turkuazı',
  bg='#04202b', bg_soft='#0a3745', plate='rgba(4,26,35,.985)',
  ov='6,32,42',                 # hero ortusu rgb
  glow='23,184,201',            # parilti rgb
  deep='#0e8aa0', mid='#17b8c9', lite='#8fe9f2',
  ink='#d4eef3', ink2='#c2e8ef', ink3='#93c3cd',
  rule='rgba(120,225,240,.13)', rule2='rgba(120,225,240,.22)',
  card='rgba(120,225,240,.075)', cardb='rgba(120,225,240,.26)',
  text='#eafbfd', muted='#a8cfd8',
),
'B': dict(
  ad='Çini Laciverti',
  bg='#03162c', bg_soft='#082a4e', plate='rgba(3,18,36,.985)',
  ov='4,18,36',
  glow='52,208,220',
  deep='#0f5fa8', mid='#2b8fd6', lite='#6fe0ea',
  ink='#d5e6f8', ink2='#c6ddf6', ink3='#9bbad6',
  rule='rgba(90,190,235,.13)', rule2='rgba(90,190,235,.22)',
  card='rgba(90,190,235,.075)', cardb='rgba(90,190,235,.26)',
  text='#eef6ff', muted='#aac9dd',
),
}

# ---------------------------------------------------------------- hero isleyisi
TIP = {
'1': dict(ad='Film önde', op='.52', ovA='.10', ovB='.62',
          filt='saturate(1.06) contrast(1.04) brightness(1.06)'),
'2': dict(ad='Mürekkep önde', op='.20', ovA='.30', ovB='.88',
          filt='saturate(.72) contrast(1.10) brightness(1.02)'),
}

def css(r, t):
    return """
/* ===== %(rad)s · %(tad)s ===== */
:root{
  --bg:%(bg)s; --bg-soft:%(bg_soft)s;
  --card:%(card)s; --card-brd:%(cardb)s;
  --text:%(text)s; --muted:%(muted)s;
  --ink:%(ink)s; --ink-2:%(ink2)s; --ink-3:%(ink3)s;
  --rule:%(rule)s; --rule-2:%(rule2)s;
  --plate:%(plate)s;
}
body{background:var(--bg)}

/* hero: video ve ortu */
.hero-bg{ opacity:%(op)s; filter:%(filt)s }
.hero-ov{
  background:radial-gradient(ellipse at center,
    rgba(%(ov)s,%(ovA)s), rgba(%(ov)s,%(ovB)s) 96%%);
}

/* baslik ve parilti — morumsu mavi yerine Selcuklu mavisi */
.hero h1{
  background:linear-gradient(180deg,#f4fdff 0%%,%(lite)s 52%%,%(mid)s 100%%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
  filter:drop-shadow(0 1px 1px rgba(4,18,26,.5))
         drop-shadow(0 0 24px rgba(%(glow)s,.38));
}
.hero-logo{ filter:drop-shadow(0 14px 55px rgba(%(glow)s,.46)) }
.hero .eyebrow{ text-shadow:0 0 18px rgba(%(glow)s,.5) }

/* butonlar */
.btn-grad{ text-shadow:0 0 16px rgba(%(glow)s,.42) }
.btn-grad::after{
  background:linear-gradient(90deg,%(deep)s,%(lite)s);
  box-shadow:0 2px 14px rgba(%(glow)s,.5),0 2px 14px rgba(%(glow)s,.3);
}
.btn-grad:hover::after{
  box-shadow:0 2px 22px rgba(%(glow)s,.8),0 2px 18px rgba(%(glow)s,.5);
}

/* ayrac etiketi ve cizgiler A2'den geliyor — turkuaza cekiliyor */
.slj-divider .slj-line{
  background:linear-gradient(90deg,transparent,rgba(%(glow)s,.38));
}
.slj-divider .slj-line:last-child{
  background:linear-gradient(90deg,rgba(%(glow)s,.38),transparent);
}
.slj-divider .slj-tag{ color:rgba(%(glow)s,.9) }
header.nav .brand::before{
  background:linear-gradient(180deg,rgba(%(glow)s,.95),rgba(%(glow)s,.12));
}
.loader-word{ color:%(lite)s }

/* aktif menu ve odak */
.nav-links a.active{ --nd:%(mid)s }
.nav-links a:focus-visible{ outline-color:%(lite)s }
""" % dict(r, **{'rad': r['ad'], 'tad': t['ad'], 'op': t['op'],
                 'ovA': t['ovA'], 'ovB': t['ovB'], 'filt': t['filt']})

def build(rk, tk, out):
    s = swap_video(s0)
    i = s.rfind('</style>')
    assert i > 0
    s = s[:i] + css(RENK[rk], TIP[tk]) + s[i:]
    s = s.replace('<title>', '<!-- KABUK: %s + %s -->\n<title>'
                  % (RENK[rk]['ad'], TIP[tk]['ad']), 1)
    (ROOT / out).write_text(s, encoding='utf-8')
    return len(s)

for rk, tk, out in (('A','1','_r1.html'), ('A','2','_r2.html'),
                    ('B','1','_r3.html'), ('B','2','_r4.html')):
    n = build(rk, tk, out)
    print('%-11s %-16s %-14s %7d bayt' % (out, RENK[rk]['ad'], TIP[tk]['ad'], n))

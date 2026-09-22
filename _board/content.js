/* Eray Balat — board content. Every line here is checked against the live site
   or the project notes. Themes lay these out; they do not invent facts. */
window.EB = {
  P: { // projects: cover lines
    flawless:  { t: "FLAWLESS", k: "Documentary · 16:56 · 4K", role: "Writer, director, editor, narrator", href: "/flawless/", hrefLabel: "Read the case study" },
    coldstart: { t: "COLD START", k: "Sci-fi trailer · 2:04", role: "Editor · sound · colour", sub: "XPRIZE submission", href: "coldstart-film.mp4", hrefLabel: "Watch the trailer" },
    commission:{ t: "A 10-minute short", k: "Narrative short · private commission", role: "Production · edit · sound · score" },
    tenniscut: { t: "TennisCut", k: "Three brand films · 9:16", role: "Director" },
    bushido:   { t: "Bushido", k: "Campaign concept · synthetic cast", role: "Director", href: "/bushido/", hrefLabel: "See the campaign" },
    novora:    { t: "Novora", k: "Animated brand film · 0:28 · TR / EN", role: "Director", href: "https://youtu.be/GAGlpIw3Q2Y", hrefLabel: "Watch (EN)" },
    konfuse:   { t: "Konfuse", k: "Brand world film", role: "Director", href: "https://youtube.com/shorts/zhqaCtjbwmI", hrefLabel: "Watch on YouTube" },
    music:     { t: "Music videos", k: "Universal Music Türkiye", role: "AI creator" },
    real:      { t: "Real footage", k: "Short films, shot on a camera", role: "Writer · director · editor" },
    about:     { t: "About", k: "Director, editor · Kayseri, Türkiye" },
    mark:      { t: "The mark", k: "An eight-point Seljuk star" },
    contact:   { t: "Contact", k: "Send the deadline and the runtime" }
  },
  T: { // notes
    "hello": "<b>Hi, I’m Eray</b>, a director and editor in Kayseri, Türkiye. This board has the finished films next to the renders, timelines and notes behind them.",
    "howto": "Drag to move. Pinch or <b>⌘ + scroll</b> to zoom. Double-click a frame. <b>⌘K</b> to search. <b>▶ Tour</b> walks you through it.",
    "tz": "Clients in Türkiye and the US. Kayseri is <b data-tz>10 hours</b> ahead of San Francisco: notes you send in the evening get worked on while you sleep.",

    "fl.interview": "Leonardo Notarbartolo led the 2003 heist. I interviewed him in Italian over a video call. After watching the film he wrote: <b>“Ti sono grato per il documentario, mi piace molto.”</b>",
    "fl.voice": "English narration in my voice, and a full Italian dub in my <b>cloned voice</b> (ElevenLabs). Subtitles take it to six languages.",
    "fl.3d": "<b>30+ bespoke 3D scenes</b> rebuilding the vault, the sensors and the escape. 3D and AI images: Berkay Efe Balat.",
    "fl.motion": "<b>35 motion graphics</b>. Motion design: Hasan.",
    "fl.parts": "Five parts: <b>The Plan, The Heist, The Escape, The Mistake, Where Is He Now.</b>",
    "fl.edit": "Cut in Premiere Pro. The master timeline runs <b>eight video tracks</b> deep.",
    "fl.thumbs": "Thumbnail tests before release.",
    "fl.credits": "Written, directed, edited and narrated by me. Image enhancement: Magnific. Music licensed from Epidemic Sound.",

    "cs.in": "<b>In:</b> 35 generated clips and 8 voice files, all from the client.",
    "cs.out": "<b>Out:</b> a 2:04 trailer. Edit, conform, sound design, mix, colour, music, subtitles.",
    "cs.upscale": "Upscale in Topaz: <b>1280×720 → 2560×1440</b>, frame interpolation off.",
    "cs.colour": "One cold identity across the cut; the few warm accents were kept on purpose.",
    "cs.silence": "<b>2.1 seconds</b> of absolute silence at the centre. Placed on purpose.",
    "cs.master": "Master: 1920×1080, 24 fps, <b>−15.7 LUFS</b>, −1.4 dBTP. ProRes 422 HQ archive.",
    "cs.licence": "<b>Before sign-off:</b> 28 stock licences audited, 7 found under other project names and re-registered. The client was told before they asked.",
    "cs.review": "“He caught continuity and pacing problems I’d missed. I’d hire him again without hesitation.”",

    "cm.what": "A private commission: <b>106 approved stills</b> turned into <b>110 clips</b> and cut to an existing voice-over. Seven chapters, one film.",
    "cm.models": "<b>Five models, routed per shot</b>, not one tool for everything.",

    "tc.films": "Three vertical films for a tennis app: <b>The Moment, Dead Time Remover, Best of Us.</b>",
    "tc.stills": "Best of Us was built still-first: the couple was locked in approved stills, then animated shot by shot in <b>Kling</b>.",
    "tc.ui": "Phone screens were generated blank. The real app UI was added in <b>After Effects</b>.",
    "tc.team": "Some motion clips by Berkay Efe Balat. Best of Us has an <b>original score</b>.",

    "bu.what": "A synthetic cast of two (<b>Ayla and Kaan</b>), a 4K product capsule, three vertical films and original music.",
    "bu.cast": "Each of the two was built from a master portrait and a character sheet, then carried through all three films: <b>Her Ritual, His Ritual, The Reel</b>.",

    "nv.what": "A 28-second animated pilot for an olive producer in Sölöz, Bursa. Turkish and English, 4K and 1080p. <b>Delivered a day early.</b>",

    "kf.what": "A brand world film for a leather duffel bag, with an <b>original score</b>.",
    "kf.world": "One world across every shot: mountains, a white horse, the landscape embroidered on the leather.",

    "mv.what": "Official music videos for <b>Modd</b>, released by <b>Universal Music Türkiye</b>. AI creators: Eray and Berkay Efe Balat.",

    "rf.what": "Shot on a camera. No AI. I still shoot when the film needs it.",
    "rf.swiss": "<b>Switzerland in One Hour</b> · a one-hour challenge, shot on my first day behind the camera",
    "rf.run": "<b>Run or Run</b> · writer, director, actor · 2:34",
    "rf.post": "<b>Die Post</b> · Erciyes University · writer, director, producer",
    "rf.boom": "<b>Boomerang</b> · editor · Honorable Mention, Student Video Contest 2026 · selected at Duemila30",

    /* the wall: TennisCut as the lead case */
    "tc.brief": "Three launch ads for an app that records your tennis match and cuts it down to the rallies. 9:16, English. <b>An emotion film, a proof film, a story film.</b>",
    "tc.study": "Before writing a frame I watched the brand’s <b>16 existing ads</b>. What I kept: a face and a hook in the first seconds, text on screen, the same closing card.",
    "tc.grades": "Three grades: <b>a night arena</b>, neutral daylight, and <b>sunset light over a light-blue court</b>.",
    "tc.credits": "Stills and some Kling clips: <b>Berkay Efe Balat</b>. Direction, edit, sound and grade: Eray. Original score on Best of Us.",
    "tc.hook": "The first second has to work with the sound off: <b>“You’ll only remember ONE POINT.”</b> Word by word, in the brand’s coral.",
    "tc.serve": "AI tennis rarely shows the racket touching the ball. <b>The serve was regenerated until it did</b>; the flash and the hit sound sit on that frame.",
    "tc.proof": "Real match recordings from the client, cut with generated shots. A two-hour match drops to <b>27:09</b>: “Every grey block gets deleted.”",
    "tc.screens": "Every app screen is a <b>real app recording</b>, composited in After Effects.",
    "tc.lock": "The couple was locked in reference stills <b>before any motion</b>, then animated shot by shot in Kling.",
    "nv.open": "“Some stories begin with the soil, <b>on the shore of Lake İznik, in Sölöz.</b>” The first line of the narration.",
    "nv.nova": "Nova, a small black bird, has a hero pose and a turnaround sheet, so it is <b>the same bird in every scene</b>.",
    "nv.sb": "Storyboard first. The film follows it <b>frame for frame</b>.",
    "nv.end": "Narration in Turkish and English, in the same voice. The last line: <b>“Health is in the roots.”</b>",
    "fd.what": "A fashion film for an embroidered leather duffel. Directed, with an <b>original score</b>.",
    "fd.world": "One world in every shot: mountains under a crescent moon, a white horse, and <b>the same landscape embroidered on the leather</b>.",
    "ab.bio": "Cinema at Erciyes University. Most of my films are built from generated footage; the work is making it hold together as one film. Edit, sound, colour and score are finished in house.",
    "ab.tools": "Nano Banana · Kling · Seedance · Flora · Firefly · Topaz · ElevenLabs · Suno · Premiere Pro · After Effects · Photoshop",
    "ab.suno": "<b>5,500+ songs</b> made on Suno. Suno Ambassador, 2025.",
    "ab.clients": "Universal Music Türkiye · TennisCut · Novora · Konfuse",

    "mk.what": "An eight-point Seljuk star, drawn as a square and a diamond that pass over and under each other, eight times. Stars like it run through the Seljuk stonework of Kayseri.",

    "ct.what": "You get a scope and a fixed quote back. Commercial rights transfer on delivery.",
    "ct.links": "<a href='/hire/'>Rates</a> · <a href='https://www.instagram.com/documenteray/' target='_blank' rel='noopener'>Instagram</a> · <a href='https://www.linkedin.com/in/eraybalat/' target='_blank' rel='noopener'>LinkedIn</a> · <a href='https://www.youtube.com/@eraybalat' target='_blank' rel='noopener'>YouTube</a> · <a href='https://www.upwork.com/freelancers/eraybalat' target='_blank' rel='noopener'>Upwork</a>"
  },
  STAR: ["M51.971 18.029L60 10L88.749 38.749", "M24.64 36.01L24.64 24.64L65.29 24.64", "M101.971 51.971L110 60L81.251 88.749", "M83.99 24.64L95.36 24.64L95.36 65.29", "M68.029 101.971L60 110L31.251 81.251", "M95.36 83.99L95.36 95.36L54.71 95.36", "M18.029 68.029L10 60L38.749 31.251", "M36.01 95.36L24.64 95.36L24.64 54.71"],
  star: function (sw) { return "<svg viewBox='0 0 120 120' fill='none' stroke='currentColor' stroke-width='" + (sw || 6) + "' stroke-linecap='butt' stroke-linejoin='miter' aria-hidden='true'>" + EB.STAR.map(function (d) { return "<path d='" + d + "'/>"; }).join("") + "</svg>"; },
  tz: function () {
    try {
      var n = new Date(), f = function (z) { var p = new Intl.DateTimeFormat("en-US", { timeZone: z, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }).formatToParts(n), o = {}; p.forEach(function (x) { o[x.type] = x.value; }); return Date.UTC(+o.year, +o.month - 1, +o.day, +o.hour, +o.minute); };
      var h = Math.round((f("Europe/Istanbul") - f("America/Los_Angeles")) / 36e5);
      document.querySelectorAll("[data-tz]").forEach(function (e) { e.textContent = h + " hours"; });
    } catch (e) { }
  }
};

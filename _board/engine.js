/* Eray Balat — board engine.
   One infinite canvas, shared by every board theme. Themes supply the data
   (frames, items, links) and the look; this file does the camera and the UI. */
(function () {
  "use strict";
  var RM = matchMedia("(prefers-reduced-motion: reduce)").matches;

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function $(id) { return document.getElementById(id); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function ext(h) { return /^https?:/.test(h); }
  function text(html) { var d = document.createElement("div"); d.innerHTML = html || ""; return d.textContent || ""; }

  function Board(cfg) {
    var B = this;
    var vp = cfg.vp, world = cfg.world;
    var frames = cfg.frames, items = cfg.items, links = cfg.links || [];
    var MIN = cfg.min || 0.05, MAX = cfg.max || 2.6, LOD = cfg.lod || [0.3, 0.62];
    var s = 1, tx = 0, ty = 0, byId = {}, anim = 0, inertia = 0, current = null, userMoved = false;

    /* ---------------- render ---------------- */
    var bx0 = Infinity, by0 = Infinity, bx1 = -Infinity, by1 = -Infinity, covers = [];
    frames.forEach(function (f) {
      if (f.sub) return;
      bx0 = Math.min(bx0, f.x); by0 = Math.min(by0, f.y); bx1 = Math.max(bx1, f.x + f.w); by1 = Math.max(by1, f.y + f.h);
      var e = el("section", "fr" + (f.bare ? " bare" : "") + (f.cls ? " " + f.cls : ""));
      e.dataset.f = f.id;
      e.style.cssText = "left:" + f.x + "px;top:" + f.y + "px;width:" + f.w + "px;height:" + f.h + "px";
      if (!f.bare) e.appendChild(el("div", "fl", f.t + (f.s ? "<span>" + f.s + "</span>" : "")));
      if (f.cover) { var c = el("div", "cv", (f.cover.k ? "<small>" + f.cover.k + "</small>" : "") + "<b>" + (f.cover.t || f.t) + "</b>" + (f.cover.s ? "<em>" + f.cover.s + "</em>" : ""));
        c.style.cssText = e.style.cssText; c.dataset.f = f.id; covers.push(c); }
      if (cfg.decorFrame) cfg.decorFrame(f, e);
      f.el = e; world.appendChild(e);
    });
    var BOUNDS = cfg.bounds || { x: bx0 - 40, y: by0 - 60, w: bx1 - bx0 + 80, h: by1 - by0 + 100 };

    var NS = "http://www.w3.org/2000/svg", svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "links"); svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;pointer-events:none";
    svg.setAttribute("width", BOUNDS.x + BOUNDS.w + 200); svg.setAttribute("height", BOUNDS.y + BOUNDS.h + 200);
    world.appendChild(svg);

    items.forEach(function (it) {
      var e = (cfg.render && cfg.render(it, el)) || render(it);
      if (!e) return;
      e.style.left = it.x + "px"; e.style.top = it.y + "px";
      if (it.w) e.style.width = it.w + "px";
      if (it.h && it.k !== "text" && it.k !== "cap") e.style.height = it.h + "px";
      if (it.id) { byId[it.id] = it; e.dataset.id = it.id; }
      it.el = e; world.appendChild(e);
      if (media(it)) { e.dataset.focus = "1"; e.tabIndex = 0; e.setAttribute("role", "button"); e.setAttribute("aria-label", it.title || it.chip || "Open"); }
    });
    items.forEach(function (it) { if (it.el && !it.h) it.h = it.el.offsetHeight; if (it.el && !it.w) it.w = it.el.offsetWidth; });
    function media(it) {
      if (it.k === "img") return { k: "img", src: it.full || it.src };
      if (it.k === "vid") return { k: "vid", src: it.src, poster: it.poster };
      return it.media || null;
    }

    var cvLayer = el("div", "cvs"); cvLayer.style.cssText = "position:absolute;left:0;top:0;width:0;height:0";
    covers.forEach(function (c) { cvLayer.appendChild(c); }); world.appendChild(cvLayer); // covers sit above the items, for the far zoom level

    function render(it) {
      var e;
      if (it.k === "img" || it.k === "vid") {
        e = el("div", "it " + it.k + (it.cls ? " " + it.cls : ""));
        var im = new Image(); im.decoding = "async"; im.loading = "lazy"; im.alt = ""; im.draggable = false;
        im.src = it.k === "vid" ? it.poster : it.src; if (it.pos) im.style.objectPosition = it.pos; if (it.fit) im.style.objectFit = it.fit;
        e.appendChild(im);
        if (it.k === "vid") { var v = el("video"); v.muted = true; v.loop = true; v.playsInline = true; v.setAttribute("playsinline", ""); v.preload = "none"; v.dataset.src = it.src; e.appendChild(v); e.appendChild(el("span", "pb")); it.v = v; }
        if (it.chip) e.appendChild(el("span", "chip", it.chip));
        if (it.bg) e.style.background = it.bg;
      } else if (it.k === "note") { e = el("div", "note " + (it.c || "y") + (it.cls ? " " + it.cls : ""), it.html); }
      else if (it.k === "text") { e = el("div", "tx" + (it.cls ? " " + it.cls : ""), it.html); if (it.size) e.style.fontSize = it.size + "px"; }
      else if (it.k === "cap") { e = el("div", "cap" + (it.cls ? " " + it.cls : ""), it.html); }
      else if (it.k === "pin") {
        e = el("div", "pin" + (it.cls ? " " + it.cls : ""), "<i>" + (it.who || "?").slice(0, 1) + "</i><div class='bub'><b>" + it.who + "</b>" + it.html + "</div>");
        e.addEventListener("click", function (ev) { ev.stopPropagation(); e.classList.toggle("open"); });
      } else if (it.k === "html") { e = el("div", "hx" + (it.cls ? " " + it.cls : ""), it.html); }
      else return null;
      return e;
    }

    /* links: [x,y]→[x,y] or item id → item id (right edge to left edge) */
    function port(it, side) { return side === "out" ? [it.x + it.w, it.y + (it.py || Math.min(it.h / 2, 60))] : [it.x, it.y + (it.py || Math.min(it.h / 2, 60))]; }
    links.forEach(function (l) {
      var a = typeof l.a === "string" ? port(byId[l.a], "out") : l.a, b = typeof l.b === "string" ? port(byId[l.b], "in") : l.b;
      if (!a || !b) return;
      var dx = Math.max(60, Math.abs(b[0] - a[0]) * .5), p = document.createElementNS(NS, "path");
      if (l.shape === "sag") { var len = Math.hypot(b[0] - a[0], b[1] - a[1]); p.setAttribute("d", "M" + a[0] + " " + a[1] + " Q" + (a[0] + b[0]) / 2 + " " + ((a[1] + b[1]) / 2 + len * (l.sag || .12)) + " " + b[0] + " " + b[1]); }
      else p.setAttribute("d", "M" + a[0] + " " + a[1] + " C" + (a[0] + dx) + " " + a[1] + " " + (b[0] - dx) + " " + b[1] + " " + b[0] + " " + b[1]);
      p.setAttribute("class", "ln" + (l.c ? " " + l.c : "")); if (l.id) p.id = l.id;
      svg.appendChild(p); l.p = p; l.pa = a; l.pb = b;
      if (l.heads) [a, b].forEach(function (pt) { var c = document.createElementNS(NS, "circle"); c.setAttribute("cx", pt[0]); c.setAttribute("cy", pt[1]); c.setAttribute("r", l.heads); c.setAttribute("class", "head"); svg.appendChild(c); });
      if (cfg.ports !== false && typeof l.a === "string") {
        [a, b].forEach(function (pt) { var c = document.createElementNS(NS, "circle"); c.setAttribute("cx", pt[0]); c.setAttribute("cy", pt[1]); c.setAttribute("r", 6); c.setAttribute("class", "port"); svg.appendChild(c); });
      }
    });

    /* ---------------- camera ---------------- */
    function lodName() { return s < LOD[0] ? "far" : s < LOD[1] ? "mid" : "near"; }
    var gBase = cfg.grid || 24;
    var mvOn = false, mvT = 0, lodNow = vp.dataset.lod, zlEl = null, zlTxt = null;
    function apply() {
      world.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + s + ")";
      /* performance: an inherited custom property set on the world restyles every node in it, every frame.
         cfg.scaleVar "covers" keeps --s on the covers layer only, and only while covers are on screen. */
      var L = lodName();
      if (cfg.scaleVar === "covers") { if (L === "far" || lodNow !== L) cvLayer.style.setProperty("--s", s); }
      else world.style.setProperty("--s", s);
      if (cfg.grid !== false) {
        var g = gBase * s; while (g < 10) g *= 5; while (g > 60) g /= 5;
        vp.style.setProperty("--gs", g + "px"); vp.style.setProperty("--gS", g * 5 + "px");
        vp.style.setProperty("--gx", tx + "px"); vp.style.setProperty("--gy", ty + "px");
      }
      if (lodNow !== L) { lodNow = L; vp.dataset.lod = L; }
      /* while moving, the world is its own GPU layer (cheap pan/zoom); at rest it re-rasters sharp */
      if (!mvOn) { mvOn = true; world.classList.add("mv"); }
      clearTimeout(mvT); mvT = setTimeout(function () { mvOn = false; world.classList.remove("mv"); }, 240);
      /* performance: the zoom label is only rewritten when the number changes (a pan never changes it). Rewriting it
         every frame forced a layout, a repaint and slower hit tests on every pan frame. */
      var z = Math.round(s * 100) + "%";
      if (z !== zlTxt && (zlEl || (zlEl = $("zl")))) {
        var t = zlEl.firstChild;
        if (t && t.nodeType === 3 && !t.nextSibling) t.data = z; else zlEl.textContent = z;
        zlTxt = z;
      }
      drawMini(); schedule();
    }
    function zoomAt(px, py, k) { var ns = clamp(s * k, MIN, MAX); tx = px - (px - tx) * ns / s; ty = py - (py - ty) * ns / s; s = ns; apply(); }
    function inset() { return typeof cfg.inset === "function" ? cfg.inset() : (cfg.inset || { l: 0, t: 0, r: 0, b: 0 }); }
    function fitRect(r, pad) {
      var I = inset(), W = innerWidth - I.l - I.r, H = innerHeight - I.t - I.b, p = pad == null ? 40 : pad;
      var ns = clamp(Math.min((W - p * 2) / r.w, (H - p * 2) / r.h), MIN, MAX);
      return { s: ns, tx: I.l + (W - r.w * ns) / 2 - r.x * ns, ty: I.t + (H - r.h * ns) / 2 - r.y * ns };
    }
    function fly(t, ms, cb) {
      cancelAnimationFrame(anim); cancelAnimationFrame(inertia);
      var a = { s: s, tx: tx, ty: ty }, t0 = performance.now(), d = RM ? 1 : (ms || 750);
      (function step(n) {
        var k = Math.min(1, (n - t0) / d), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
        s = Math.exp(Math.log(a.s) + (Math.log(t.s) - Math.log(a.s)) * e); tx = a.tx + (t.tx - a.tx) * e; ty = a.ty + (t.ty - a.ty) * e; apply();
        if (k < 1) anim = requestAnimationFrame(step); else if (cb) cb();
      })(t0);
    }
    function frameById(id) { for (var i = 0; i < frames.length; i++) if (frames[i].id === id) return frames[i]; }
    function frameRect(f) { return { x: f.x - 20, y: f.y - 70, w: f.w + 40, h: f.h + 90 }; }
    function goFrame(id, ms) { var f = frameById(id); if (!f) return; fly(fitRect(frameRect(f), 30), ms); setCurrent(f, true); }
    function fitAll(ms) { fly(fitRect(BOUNDS, 24), ms); }
    function toWorld(x, y) { return { x: (x - tx) / s, y: (y - ty) / s }; }

    /* ---------------- current frame + deep link ---------------- */
    function setCurrent(f, push) {
      if (f && f.sub) { var par = frames.filter(function (p) { return !p.sub && !p.bare && f.x >= p.x && f.x <= p.x + p.w && f.y >= p.y - 80 && f.y <= p.y + p.h; })[0]; if (par) f = par; }
      current = f;
      if (cfg.onCurrent) cfg.onCurrent(f, !!push);
      document.querySelectorAll("[data-goto]").forEach(function (b) { b.classList.toggle("on", !!f && b.dataset.goto === f.id); });
      if (push && f && !f.bare) history.replaceState(null, "", location.pathname + location.search + "#" + f.id);
    }
    var settleT;
    function settle() {
      clearTimeout(settleT);
      settleT = setTimeout(function () {
        var I = inset(), c = toWorld(I.l + (innerWidth - I.l - I.r) / 2, I.t + (innerHeight - I.t - I.b) / 2), hit = null;
        frames.forEach(function (f) { if (!f.sub && c.x >= f.x && c.x <= f.x + f.w && c.y >= f.y - 60 && c.y <= f.y + f.h) hit = f; });
        if (hit !== current) setCurrent(hit, userMoved && s > .22);
      }, 260);
    }

    /* ---------------- videos play when you are close ---------------- */
    var vids = items.filter(function (i) { return !!i.v; }), vT = 0;
    function schedule() { if (vT) return; vT = requestAnimationFrame(function () { vT = 0; settle(); checkVideos(); }); }
    var checkT;
    function checkVideos() {
      clearTimeout(checkT);
      checkT = setTimeout(function () {
        var cx = innerWidth / 2, cy = innerHeight / 2, cand = [];
        vids.forEach(function (it) {
          var sw = it.w * s, sx = tx + it.x * s, sy = ty + it.y * s, sh = it.h * s;
          var vis = sx < innerWidth && sx + sw > 0 && sy < innerHeight && sy + sh > 0;
          if (vis && sw >= (cfg.autoplayW || 190) && !RM) cand.push({ it: it, d: Math.hypot(sx + sw / 2 - cx, sy + sh / 2 - cy) });
          else stopV(it);
        });
        cand.sort(function (a, b) { return a.d - b.d; });
        cand.forEach(function (c, i) { if (i < (cfg.maxPlay || 4)) playV(c.it); else stopV(c.it); });
      }, 180);
    }
    function playV(it) { var v = it.v; if (!v.src) v.src = v.dataset.src; if (v.paused) v.play().then(function () { it.el.classList.add("pl"); }).catch(function () { }); }
    function stopV(it) { var v = it.v; if (v && !v.paused) { v.pause(); } if (it.el) it.el.classList.remove("pl"); }

    /* ---------------- input ---------------- */
    var ptrs = {}, moved = 0, last = [], downT = 0, downTarget = null;
    vp.addEventListener("pointerdown", function (e) {
      if (e.button > 0) return;
      if (e.target.closest("a,button,input,.bub")) return;
      vp.setPointerCapture(e.pointerId); ptrs[e.pointerId] = { x: e.clientX, y: e.clientY };
      moved = 0; last = [{ x: e.clientX, y: e.clientY, t: performance.now() }]; downT = performance.now(); downTarget = e.target;
      stopTour(); cancelAnimationFrame(anim); cancelAnimationFrame(inertia); vp.classList.add("drag");
    });
    vp.addEventListener("pointermove", function (e) {
      var p = ptrs[e.pointerId]; if (!p) return; var ids = Object.keys(ptrs);
      if (ids.length === 1) {
        tx += e.clientX - p.x; ty += e.clientY - p.y; moved += Math.abs(e.clientX - p.x) + Math.abs(e.clientY - p.y);
        p.x = e.clientX; p.y = e.clientY; last.push({ x: e.clientX, y: e.clientY, t: performance.now() }); if (last.length > 6) last.shift();
        userMoved = true; apply();
      } else if (ids.length === 2) {
        var a = ptrs[ids[0]], b = ptrs[ids[1]], d0 = Math.hypot(a.x - b.x, a.y - b.y), m0 = [(a.x + b.x) / 2, (a.y + b.y) / 2];
        p.x = e.clientX; p.y = e.clientY; a = ptrs[ids[0]]; b = ptrs[ids[1]];
        var d1 = Math.hypot(a.x - b.x, a.y - b.y), m1 = [(a.x + b.x) / 2, (a.y + b.y) / 2];
        tx += m1[0] - m0[0]; ty += m1[1] - m0[1]; if (d0 > 0) zoomAt(m1[0], m1[1], d1 / d0); moved += 99; userMoved = true;
      }
    });
    function up(e) {
      if (!ptrs[e.pointerId]) return;
      var solo = Object.keys(ptrs).length === 1; delete ptrs[e.pointerId];
      if (!Object.keys(ptrs).length) vp.classList.remove("drag");
      if (!solo) return;
      if (moved < 6 && performance.now() - downT < 500) { tap(downTarget); return; }
      if (RM || last.length < 2) return;
      var a = last[0], b = last[last.length - 1], dt = Math.max(16, b.t - a.t), vx = (b.x - a.x) / dt * 16, vy = (b.y - a.y) / dt * 16;
      if (Math.hypot(vx, vy) < 2 || performance.now() - b.t > 80) return;
      (function glide() { vx *= .92; vy *= .92; tx += vx; ty += vy; apply(); if (Math.hypot(vx, vy) > .4) inertia = requestAnimationFrame(glide); })();
    }
    vp.addEventListener("pointerup", up); vp.addEventListener("pointercancel", up);
    vp.addEventListener("wheel", function (e) {
      e.preventDefault(); stopTour(); cancelAnimationFrame(anim); cancelAnimationFrame(inertia); userMoved = true;
      var k = e.deltaMode === 1 ? 16 : 1;
      if (e.ctrlKey || e.metaKey) zoomAt(e.clientX, e.clientY, Math.exp(-e.deltaY * k * .011));
      else { tx -= e.deltaX * k; ty -= e.deltaY * k; apply(); }
    }, { passive: false });
    vp.addEventListener("dblclick", function (e) {
      if (e.target.closest("a,button,[data-focus]")) return;
      var w = toWorld(e.clientX, e.clientY);
      for (var i = frames.length - 1; i >= 0; i--) { var f = frames[i]; if (!f.bare && !f.sub && w.x >= f.x && w.x <= f.x + f.w && w.y >= f.y && w.y <= f.y + f.h) { userMoved = true; goFrame(f.id); return; } }
      zoomAt(e.clientX, e.clientY, 2);
    });
    function tap(t) {
      if (!t) return; var host = t.closest && t.closest("[data-focus]"); if (!host) return;
      var it = byId[host.dataset.id] || items.filter(function (i) { return i.el === host; })[0]; if (it) openFocus(it);
    }
    document.addEventListener("keydown", function (e) {
      if (e.target.closest("input,textarea")) { if (e.key === "Escape") closePal(); return; }
      var k = e.key;
      if ((e.metaKey || e.ctrlKey) && k.toLowerCase() === "k") { e.preventDefault(); openPal(); return; }
      if (focusOpen) { if (k === "Escape") closeFocus(); else if (k === "ArrowRight") stepFocus(1); else if (k === "ArrowLeft") stepFocus(-1); return; }
      if (k === "/") { e.preventDefault(); openPal(); }
      else if (k === "+" || k === "=") zoomAt(innerWidth / 2, innerHeight / 2, 1.3);
      else if (k === "-") zoomAt(innerWidth / 2, innerHeight / 2, 1 / 1.3);
      else if (k === "0" || k === "f") { stopTour(); fitAll(); }
      else if (k === "t") toggleTour();
      else if (k === "Escape") stopTour();
      else if (k === "ArrowRight" && touring) stepTour(1);
      else if (k === "ArrowLeft" && touring) stepTour(-1);
      else if (k.indexOf("Arrow") === 0) { e.preventDefault(); var d = 90; if (k === "ArrowLeft") tx += d; if (k === "ArrowRight") tx -= d; if (k === "ArrowUp") ty += d; if (k === "ArrowDown") ty -= d; userMoved = true; apply(); }
      else if (k === "Enter" && document.activeElement && document.activeElement.dataset && document.activeElement.dataset.focus) tap(document.activeElement);
    });
    addEventListener("resize", apply);
    addEventListener("hashchange", function () { var f = frameById(location.hash.slice(1)); if (f) goFrame(f.id); });

    /* ---------------- UI: zoom, frames list, share ---------------- */
    function on(id, fn) { var e = $(id); if (e) e.addEventListener("click", fn); }
    on("zi", function () { zoomAt(innerWidth / 2, innerHeight / 2, 1.4); });
    on("zo", function () { zoomAt(innerWidth / 2, innerHeight / 2, 1 / 1.4); });
    on("zl", function () { zoomAt(innerWidth / 2, innerHeight / 2, 1 / s); });
    on("fit", function () { stopTour(); fitAll(); });
    on("share", function () { var u = location.href.split("#")[0] + (current && !current.bare ? "#" + current.id : ""); copy(u, "Link copied" + (current && !current.bare ? ": " + current.t : "")); });
    var list = $("frames-list");
    if (list) frames.forEach(function (f) {
      if (f.sub) return;
      var b = el("button", "", "<i></i><span>" + f.t + "</span>"); b.dataset.goto = f.id;
      b.onclick = function () { stopTour(); userMoved = true; goFrame(f.id); if (cfg.onNav) cfg.onNav(); };
      list.appendChild(b);
    });
    function copy(t, msg) { (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { toast(msg || "Copied"); }, function () { toast(t); }); }
    function toast(m) { var t = $("toast"); if (!t) return; t.textContent = m; t.classList.add("on"); clearTimeout(toast.t); toast.t = setTimeout(function () { t.classList.remove("on"); }, 1900); }
    B.toast = toast;

    /* ---------------- minimap ---------------- */
    var mc = $("mc"), mx = mc && mc.getContext("2d"), css = getComputedStyle(document.documentElement);
    var MM = { bg: css.getPropertyValue("--mm-bg").trim() || "#111", fr: css.getPropertyValue("--mm-fr").trim() || "#2a2a2a", ln: css.getPropertyValue("--mm-ln").trim() || "#3a3a3a", vw: css.getPropertyValue("--mm-vw").trim() || "#7cc4ff" };
    function drawMini() {
      if (!mx || cfg.mini === false) return; var W = mc.width, H = mc.height, k = Math.min(W / BOUNDS.w, H / BOUNDS.h) * .9, ox = (W - BOUNDS.w * k) / 2 - BOUNDS.x * k, oy = (H - BOUNDS.h * k) / 2 - BOUNDS.y * k;
      mx.fillStyle = MM.bg; mx.fillRect(0, 0, W, H);
      frames.forEach(function (f) { if (f.bare || f.sub) return; mx.fillStyle = current === f ? MM.ln : MM.fr; mx.fillRect(ox + f.x * k, oy + f.y * k, f.w * k, f.h * k); });
      var a = toWorld(0, 0), b = toWorld(innerWidth, innerHeight); mx.strokeStyle = MM.vw; mx.lineWidth = 3; mx.strokeRect(ox + a.x * k, oy + a.y * k, (b.x - a.x) * k, (b.y - a.y) * k);
      drawMini.m = { k: k, ox: ox, oy: oy };
    }
    if (mc) mc.addEventListener("click", function (e) {
      var r = mc.getBoundingClientRect(), m = drawMini.m, px = (e.clientX - r.left) * mc.width / r.width, py = (e.clientY - r.top) * mc.height / r.height;
      var wx = (px - m.ox) / m.k, wy = (py - m.oy) / m.k; stopTour(); userMoved = true; fly({ s: s, tx: innerWidth / 2 - wx * s, ty: innerHeight / 2 - wy * s }, 420);
    });

    /* ---------------- search (⌘K) ---------------- */
    var pal = $("pal"), palIn = $("pal-in"), palList = $("pal-list"), palSel = 0, palRes = [];
    var INDEX = frames.filter(function (f) { return !f.bare && !f.sub; }).map(function (f) { return { t: f.t, s: (f.cover && f.cover.k) || f.s || "", f: f, q: (f.t + " " + (f.s || "") + " " + (f.cover ? f.cover.k + " " + (f.cover.s || "") : "")).toLowerCase() }; });
    items.forEach(function (it) {
      var q = it.q || (it.k === "note" ? text(it.html) : it.k === "img" || it.k === "vid" ? (it.title || it.chip || "") : "");
      if (!q || q.length < 3) return;
      var f = frames.filter(function (f) { return it.x >= f.x && it.x <= f.x + f.w && it.y >= f.y && it.y <= f.y + f.h; })[0];
      INDEX.push({ t: q.length > 70 ? q.slice(0, 68) + "…" : q, s: f ? f.t : "", it: it, q: q.toLowerCase() });
    });
    function openPal() { if (!pal) return; pal.classList.add("on"); palIn.value = ""; palFilter(); setTimeout(function () { palIn.focus(); }, 10); }
    function closePal() { if (pal) pal.classList.remove("on"); }
    function palFilter() {
      var q = palIn.value.trim().toLowerCase(); palRes = INDEX.filter(function (r) { return !q || r.q.indexOf(q) > -1; }).slice(0, q ? 9 : INDEX.filter(function (r) { return r.f; }).length);
      if (!q) palRes = INDEX.filter(function (r) { return r.f; });
      palSel = 0; palList.innerHTML = "";
      palRes.forEach(function (r, i) { var b = el("button", i === 0 ? "on" : "", "<b>" + r.t + "</b><span>" + r.s + "</span>"); b.onmouseenter = function () { palSel = i; mark(); }; b.onclick = function () { palGo(i); }; palList.appendChild(b); });
      if (!palRes.length) palList.innerHTML = "<div class='none'>Nothing found</div>";
    }
    function mark() { [].forEach.call(palList.children, function (b, i) { b.classList.toggle("on", i === palSel); }); }
    function palGo(i) {
      var r = palRes[i]; if (!r) return; closePal(); userMoved = true;
      if (r.f) goFrame(r.f.id); else { var it = r.it; fly(fitRect({ x: it.x - 60, y: it.y - 60, w: (it.w || 400) + 120, h: (it.h || 200) + 120 }, 40)); }
    }
    if (pal) {
      palIn.addEventListener("input", palFilter);
      palIn.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown") { e.preventDefault(); palSel = Math.min(palRes.length - 1, palSel + 1); mark(); }
        else if (e.key === "ArrowUp") { e.preventDefault(); palSel = Math.max(0, palSel - 1); mark(); }
        else if (e.key === "Enter") { e.preventDefault(); palGo(palSel); }
        else if (e.key === "Escape") closePal();
      });
      pal.addEventListener("click", function (e) { if (e.target === pal) closePal(); });
      on("search", openPal);
    }

    /* ---------------- focus (lightbox) ---------------- */
    var fx = $("focus"), focusOpen = false, fList = [], fIdx = 0;
    function frameOf(it) { return frames.filter(function (f) { return !f.sub && it.x >= f.x && it.x < f.x + f.w && it.y >= f.y && it.y < f.y + f.h; })[0]; }
    function openFocus(it) {
      if (!fx) return; var f = frameOf(it);
      fList = items.filter(function (i) { return media(i) && frameOf(i) === f; }).sort(function (a, b) { return (a.y - b.y) || (a.x - b.x); });
      fIdx = Math.max(0, fList.indexOf(it)); focusOpen = true; fx.classList.add("on"); showFocus();
    }
    function showFocus() {
      var it = fList[fIdx], f = frameOf(it), m = $("focus-media"), md = media(it); m.innerHTML = "";
      vids.forEach(stopV);
      if (md.k === "vid") { var v = el("video"); v.src = md.src; v.poster = md.poster || ""; v.controls = true; v.autoplay = true; v.playsInline = true; v.loop = true; m.appendChild(v); v.play().catch(function () { v.muted = true; v.play().catch(function () { }); }); }
      else { var im = new Image(); im.src = md.src; im.alt = it.title || ""; m.appendChild(im); }
      $("focus-t").innerHTML = it.title || it.chip || (f ? f.t : "");
      $("focus-s").innerHTML = it.cap || (f ? (f.cover && f.cover.k) || f.s || "" : "");
      var a = $("focus-a"); if (it.href) { a.style.display = ""; a.href = it.href; a.textContent = (it.hrefLabel || "Open") + " ↗"; if (ext(it.href)) { a.target = "_blank"; a.rel = "noopener"; } else { a.removeAttribute("target"); } } else a.style.display = "none";
      $("focus-n").textContent = fList.length > 1 ? (fIdx + 1) + " / " + fList.length : "";
    }
    function stepFocus(d) { if (fList.length < 2) return; fIdx = (fIdx + d + fList.length) % fList.length; showFocus(); }
    function closeFocus() { if (!fx) return; fx.classList.remove("on"); focusOpen = false; $("focus-media").innerHTML = ""; checkVideos(); }
    if (fx) {
      fx.addEventListener("click", function (e) { if (e.target === fx || e.target.id === "focus-x") closeFocus(); });
      on("focus-prev", function () { stepFocus(-1); }); on("focus-next", function () { stepFocus(1); });
    }

    /* ---------------- tour ---------------- */
    var TOUR = cfg.tour || [], touring = false, ti = 0, tT = 0, capEl = $("cap");
    function showStep() {
      var st = TOUR[ti]; goFrame(st[0], 950);
      if (capEl) { capEl.classList.add("on"); $("cap-t").innerHTML = st[1]; $("cap-n").textContent = (ti + 1) + " / " + TOUR.length; }
      clearTimeout(tT); tT = setTimeout(function () { if (ti < TOUR.length - 1) stepTour(1); else stopTour(); }, cfg.tourMs || 5600);
    }
    function stepTour(d) { ti = clamp(ti + d, 0, TOUR.length - 1); showStep(); }
    function startTour() { if (!TOUR.length) return; touring = true; ti = 0; var b = $("tour"); if (b) b.classList.add("on"); showStep(); }
    function stopTour() { if (!touring) return; touring = false; clearTimeout(tT); if (capEl) capEl.classList.remove("on"); var b = $("tour"); if (b) b.classList.remove("on"); }
    function toggleTour() { if (touring) stopTour(); else startTour(); }
    on("tour", toggleTour); on("cap-prev", function () { stepTour(-1); }); on("cap-next", function () { stepTour(1); }); on("cap-x", stopTour);

    /* ---------------- start ---------------- */
    var start = frameById(location.hash.slice(1)), demo = (location.search.match(/[?&]demo=([\w-]+)/) || [])[1];
    if (demo && frameById(demo)) start = frameById(demo);
    var r0 = start ? fitRect(frameRect(start), 30) : fitRect(BOUNDS, 24); s = r0.s; tx = r0.tx; ty = r0.ty; apply(); if (start) setCurrent(start, false);
    if (/[?&]zoom=/.test(location.search)) { var z = +(location.search.match(/zoom=([\d.]+)/) || [])[1]; if (z) zoomAt(innerWidth / 2, innerHeight / 2, z / s); }

    B.links = links; B.frames = frames; B.all = items; B.frameOf = frameOf; B.current = function () { return current; }; B.fly = fly; B.fitRect = fitRect; B.stopV = stopV; B.playV = playV;
    B.goFrame = goFrame; B.fitAll = fitAll; B.openPal = openPal; B.startTour = startTour; B.openFocus = openFocus; B.items = byId;
    B.state = function () { return { s: s, tx: tx, ty: ty, lod: lodName() }; };
  }
  window.Board = Board;
})();

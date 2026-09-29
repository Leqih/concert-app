// DOM -> compact layer tree for Figma rebuild. Runs inside the demo page (Playwright evaluate).
// Output node formats (arrays keep payload small):
//  frame: {k:'F', n, x,y,w,h, bg?, gr?, r?, st?, sh?, bl?, op?, clip?, img?, rot?, c:[...]}
//  text : {k:'T', x,y,w,h, s:[[text, size, weight, italic, colorRGBA, letterSpacingPx, family]], lh, al, wrap}
//  svg  : {k:'S', x,y,w,h, svg}
(() => {
  const ROOT = document.getElementById('app');
  const R0 = ROOT.getBoundingClientRect();
  const VW = 393, VH = 852;
  const imgs = {};           // key -> src (data URL)
  let imgN = 0; const srcKey = new Map();
  const keyFor = (src) => { if (!srcKey.has(src)) { const k = 'i' + (imgN++); srcKey.set(src, k); imgs[k] = src; } return srcKey.get(src); };
  const rnd = v => Math.round(v * 10) / 10;
  const parseCol = s => { const m = s && s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); const a = p.length > 3 ? p[3] : 1; if (a === 0) return null; return [p[0], p[1], p[2], rnd(a * 100) / 100]; };
  const vis = (cs) => cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0.01;
  const splitTop = (s) => { const out = []; let d = 0, cur = ''; for (const ch of s) { if (ch === '(') d++; if (ch === ')') d--; if (ch === ',' && d === 0) { out.push(cur.trim()); cur = ''; } else cur += ch; } if (cur.trim()) out.push(cur.trim()); return out; };
  function parseGrad(bi) {
    const out = [];
    for (const layer of splitTop(bi)) {
      const m = layer.match(/^(repeating-)?(linear|radial)-gradient\((.*)\)$/); if (!m || m[1]) continue;
      const parts = splitTop(m[3]); let ang = 180; let kind = m[2];
      if (kind === 'linear') {
        if (/deg|turn|^to /.test(parts[0])) { const p0 = parts.shift(); if (/deg/.test(p0)) ang = parseFloat(p0); else if (/turn/.test(p0)) ang = parseFloat(p0) * 360; else { const map = { 'to top': 0, 'to right': 90, 'to bottom': 180, 'to left': 270, 'to top right': 45, 'to right top': 45, 'to bottom right': 135, 'to right bottom': 135, 'to bottom left': 225, 'to left bottom': 225, 'to top left': 315, 'to left top': 315 }; ang = map[p0] ?? 180; } }
      } else { if (!/rgb|#/.test(parts[0])) parts.shift(); }
      const stops = []; parts.forEach((p, i) => { const cm = p.match(/rgba?\([^)]+\)/); if (!cm) return; const col = parseCol(cm[0]) || [0, 0, 0, 0]; const pm = p.replace(cm[0], '').match(/(-?[\d.]+)%/); stops.push([col, pm ? parseFloat(pm[1]) / 100 : null]); });
      stops.forEach((s, i) => { if (s[1] === null) s[1] = stops.length === 1 ? 0 : i / (stops.length - 1); });
      if (stops.length) out.push({ t: kind[0], a: ang, s: stops });
    }
    return out.length ? out : null;
  }
  function shadow(cs) {
    const bs = cs.boxShadow; if (!bs || bs === 'none') return null; const out = [];
    for (const l of splitTop(bs)) { const cm = l.match(/rgba?\([^)]+\)/); const col = cm ? parseCol(cm[0]) : [0, 0, 0, .2]; if (!col) continue; const nums = l.replace(cm ? cm[0] : '', '').replace('inset', '').trim().split(/\s+/).map(parseFloat); out.push([nums[0] || 0, nums[1] || 0, nums[2] || 0, nums[3] || 0, col, /inset/.test(l) ? 1 : 0]); }
    return out.length ? out : null;
  }
  function rotOf(cs) { const t = cs.transform; if (!t || t === 'none') return 0; const m = t.match(/matrix\(([^)]+)\)/); if (!m) return 0; const [a, b] = m[1].split(',').map(parseFloat); const deg = Math.atan2(b, a) * 180 / Math.PI; return Math.abs(deg) < 0.5 ? 0 : rnd(deg); }
  const INLINE = new Set(['inline', 'contents']);
  function isPlain(el, cs) { // element draws nothing itself
    if (el.tagName === 'IMG' || el.tagName === 'svg' || el.tagName === 'VIDEO' || el.tagName === 'CANVAS' || el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') return false;
    if (parseCol(cs.backgroundColor)) return false;
    if (cs.backgroundImage && cs.backgroundImage !== 'none') return false;
    if (['Top', 'Right', 'Bottom', 'Left'].some(s => parseFloat(cs['border' + s + 'Width']) > 0 && parseCol(cs['border' + s + 'Color']))) return false;
    if (cs.boxShadow !== 'none') return false;
    if (cs.overflow !== 'visible' || cs.overflowX !== 'visible' || cs.overflowY !== 'visible') return false;
    if (parseFloat(cs.opacity) < 0.99) return false;
    if (rotOf(cs)) return false;
    if (cs.backdropFilter && cs.backdropFilter !== 'none') return false;
    return true;
  }
  const collapse = (s, ws) => /pre/.test(ws) ? s : s.replace(/\s+/g, ' ');
  const tt = (s, t) => t === 'uppercase' ? s.toUpperCase() : t === 'lowercase' ? s.toLowerCase() : t === 'capitalize' ? s.replace(/\b\w/g, c => c.toUpperCase()) : s;
  // Is the element a pure inline-text container (text + inline children that draw nothing)?
  function inlineOnly(el) {
    for (const ch of el.childNodes) {
      if (ch.nodeType === 3) continue; if (ch.nodeType !== 1) continue;
      const cs = getComputedStyle(ch); if (!vis(cs)) continue;
      if (!INLINE.has(cs.display) || !isPlain(ch, cs) || ch.tagName === 'BR') { if (ch.tagName === 'BR') continue; return false; }
      if (!inlineOnly(ch)) return false;
    }
    return true;
  }
  function segs(el, acc) {
    for (const ch of el.childNodes) {
      if (ch.nodeType === 3) { const cs = getComputedStyle(ch.parentElement); let t = tt(collapse(ch.textContent, cs.whiteSpace), cs.textTransform); if (!t) continue; const col = parseCol(cs.color) || [0, 0, 0, 1]; const fam = /Tight/.test(cs.fontFamily) ? 'D' : /Mono|mono/.test(cs.fontFamily) ? 'M' : 'B'; const ls = cs.letterSpacing === 'normal' ? 0 : rnd(parseFloat(cs.letterSpacing)); acc.push([t, rnd(parseFloat(cs.fontSize)), +cs.fontWeight, cs.fontStyle === 'italic' ? 1 : 0, col, ls, fam, cs.textDecorationLine.includes('line-through') ? 1 : 0]); }
      else if (ch.nodeType === 1) { const cs = getComputedStyle(ch); if (!vis(cs)) continue; if (ch.tagName === 'BR') { acc.push(['\n', 0]); continue; } segs(ch, acc); }
    }
    return acc;
  }
  function textNode(el, cs, rect) {
    let s = segs(el, []);
    // trim, merge
    const merged = []; for (const x of s) { if (x[1] === 0) { if (merged.length) merged[merged.length - 1][0] += '\n'; continue; } const p = merged[merged.length - 1]; if (p && JSON.stringify(p.slice(1)) === JSON.stringify(x.slice(1))) p[0] += x[0]; else merged.push(x.slice()); }
    if (!merged.length) return null; merged[0][0] = merged[0][0].replace(/^ +/, ''); const L = merged[merged.length - 1]; L[0] = L[0].replace(/ +$/, '');
    const full = merged.map(m => m[0]).join(''); if (!full.trim()) return null;
    // measure actual text box via Range
    const rg = document.createRange(); rg.selectNodeContents(el); const rr = rg.getBoundingClientRect();
    const rects = [...rg.getClientRects()].filter(r => r.width > 0);
    const lines = new Set(rects.map(r => Math.round(r.top))).size;
    const lh = cs.lineHeight === 'normal' ? null : rnd(parseFloat(cs.lineHeight));
    let al = cs.textAlign; if (al === 'start') al = 'left'; if (al === 'end') al = 'right';
    const x = rnd(rr.left - R0.left), y = rnd(rr.top - R0.top);
    return { k: 'T', x, y, w: rnd(rr.width), h: rnd(rr.height), bx: rnd(rect.left - R0.left), bw: rnd(rect.width), s: merged, lh, al, wrap: lines > 1 ? 1 : 0, ell: cs.textOverflow === 'ellipsis' ? 1 : 0 };
  }
  function svgNode(el, rect, cs) {
    const clone = el.cloneNode(true); const col = cs.color;
    clone.setAttribute('width', rnd(rect.width)); clone.setAttribute('height', rnd(rect.height));
    if (!clone.getAttribute('viewBox')) clone.setAttribute('viewBox', `0 0 ${el.getAttribute('width') || rect.width} ${el.getAttribute('height') || rect.height}`);
    // resolve use/currentColor + default fill from computed styles of original nodes
    const orig = [el, ...el.querySelectorAll('*')], cl = [clone, ...clone.querySelectorAll('*')];
    orig.forEach((o, i) => { const c = getComputedStyle(o); const n = cl[i]; if (!n.setAttribute) return; ['fill', 'stroke'].forEach(p => { const v = c[p]; if (v && v !== 'none') { const pc = parseCol(v); if (pc) { n.setAttribute(p, `rgb(${pc[0]},${pc[1]},${pc[2]})`); if (pc[3] < 1) n.setAttribute(p + '-opacity', pc[3]); } else n.setAttribute(p, 'none'); } else if (v === 'none') n.setAttribute(p, 'none'); }); const sw = c.strokeWidth; if (sw && c.stroke !== 'none') n.setAttribute('stroke-width', parseFloat(sw)); if (c.opacity !== '1') n.setAttribute('opacity', c.opacity); n.removeAttribute('class'); n.removeAttribute('style'); });
    let svg = clone.outerHTML.replace(/currentColor/g, col).replace(/\s+/g, ' ');
    if (!/xmlns=/.test(svg)) svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
    return { k: 'S', x: rnd(rect.left - R0.left), y: rnd(rect.top - R0.top), w: rnd(rect.width), h: rnd(rect.height), svg };
  }
  function nameOf(el) { const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/)[0] : ''; return (el.id ? '#' + el.id : '') + (c ? (el.id ? '.' : '') + c : '') || el.tagName.toLowerCase(); }
  function inView(r, clip) { return r.right > clip[0] && r.left < clip[2] && r.bottom > clip[1] && r.top < clip[3] && r.width > 0.5 && r.height > 0.5; }
  function walk(el, clip, out) {
    const cs = getComputedStyle(el); if (!vis(cs)) return;
    if (el.classList && el.classList.contains('skel') && false) return;
    const rect = el.getBoundingClientRect();
    const tag = el.tagName;
    if (tag === 'svg') { if (inView(rect, clip)) out.push(svgNode(el, rect, cs)); return; }
    if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'TEMPLATE') return;
    const plain = isPlain(el, cs);
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    // Element fully clipped / offscreen and not overflow-visible? still may have visible children (fixed). Skip only if plain & no rect & no children in view -- handled by children.
    let target = out, node = null;
    const dispBox = !plain && rect.width > 0.5 && rect.height > 0.5;
    if (dispBox) {
      if (!inView(rect, clip)) return; // offscreen / clipped away
      const rot = rotOf(cs);
      let x = rect.left - R0.left, y = rect.top - R0.top, w = rect.width, h = rect.height;
      if (rot) { w = el.offsetWidth; h = el.offsetHeight; const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2; x = cx - w / 2 - R0.left; y = cy - h / 2 - R0.top; const sc = cs.transform.match(/matrix\(([^)]+)\)/); if (sc) { const [a, b] = sc[1].split(',').map(parseFloat); const s = Math.hypot(a, b); w *= s; h *= s; x = cx - w / 2 - R0.left; y = cy - h / 2 - R0.top; } }
      node = { k: 'F', n: nameOf(el), x: rnd(x), y: rnd(y), w: rnd(w), h: rnd(h), c: [] };
      if (rot) node.rot = rot;
      const bg = parseCol(cs.backgroundColor); if (bg) node.bg = bg;
      if (cs.backgroundImage && cs.backgroundImage !== 'none') {
        const um = cs.backgroundImage.match(/url\("?([^")]+)"?\)/); if (um && !/\.svg|svg\+xml/.test(um[1])) node.img = [keyFor(um[1]), cs.backgroundSize === 'contain' ? 'FIT' : 'FILL'];
        const g = parseGrad(cs.backgroundImage); if (g) node.gr = g;
      }
      if (tag === 'IMG' && el.currentSrc && el.complete && el.naturalWidth) node.img = [keyFor(el.currentSrc), cs.objectFit === 'contain' ? 'FIT' : 'FILL'];
      const rr = [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius].map(v => Math.min(parseFloat(v) || 0, Math.min(w, h) / 2)).map(rnd);
      if (rr.some(v => v)) node.r = rr.every(v => v === rr[0]) ? rr[0] : rr;
      const bw = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseFloat(cs['border' + s + 'Width']) || 0);
      const bc = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseCol(cs['border' + s + 'Color']));
      const bi = bw.findIndex((v, i) => v > 0 && bc[i]);
      if (bi >= 0) node.st = [bw.map((v, i) => bc[i] ? v : 0), bc[bi], cs['border' + ['Top', 'Right', 'Bottom', 'Left'][bi] + 'Style'] === 'dashed' ? 1 : 0];
      const sh = shadow(cs); if (sh) node.sh = sh;
      if (cs.backdropFilter && cs.backdropFilter !== 'none') { const m = cs.backdropFilter.match(/blur\(([\d.]+)px/); if (m) node.bl = +m[1]; }
      const op = parseFloat(cs.opacity); if (op < 0.99) node.op = rnd(op * 100) / 100;
      if (cs.overflow !== 'visible' || cs.overflowX !== 'visible' || cs.overflowY !== 'visible') node.clip = 1;
      if (tag === 'INPUT' || tag === 'TEXTAREA') { const v = el.value || el.placeholder; if (v) { const ph = !el.value; const pl = parseFloat(cs.paddingLeft) || 0; const col = ph ? (parseCol(getComputedStyle(el, '::placeholder').color) || [0, 0, 0, .4]) : (parseCol(cs.color) || [0, 0, 0, 1]); node.c.push({ k: 'T', x: rnd(rect.left - R0.left + pl), y: rnd(rect.top - R0.top), w: rnd(rect.width - pl - (parseFloat(cs.paddingRight) || 0)), h: rnd(rect.height), s: [[v, rnd(parseFloat(cs.fontSize)), +cs.fontWeight, 0, col, 0, /Tight/.test(cs.fontFamily) ? 'D' : 'B', 0]], lh: null, al: 'left', wrap: 0, vc: 1 }); } }
      out.push(node); target = node.c;
    }
    let nclip = clip;
    if (node && node.clip) nclip = [Math.max(clip[0], rect.left), Math.max(clip[1], rect.top), Math.min(clip[2], rect.right), Math.min(clip[3], rect.bottom)];
    if (hasText && inlineOnly(el)) { const t = textNode(el, cs, rect); if (t && inView({ left: t.x + R0.left, top: t.y + R0.top, right: t.x + t.w + R0.left, bottom: t.y + t.h + R0.top, width: t.w, height: t.h }, nclip)) target.push(t); return; }
    // mixed content: children elements + loose text nodes
    const kids = [...el.childNodes];
    const order = kids.map((k, i) => { if (k.nodeType !== 1) return [k, 0, i]; const c = getComputedStyle(k); const z = (c.position !== 'static' && c.zIndex !== 'auto') ? +c.zIndex : 0; return [k, z, i]; }).sort((a, b) => a[1] - b[1] || a[2] - b[2]);
    for (const [k] of order) {
      if (k.nodeType === 3) { const t = k.textContent; if (!t.trim()) continue; const span = document.createElement('span'); k.parentNode.insertBefore(span, k); span.appendChild(k); const r = span.getBoundingClientRect(); const tn = textNode(span, getComputedStyle(span), r); span.parentNode.insertBefore(k, span); span.remove(); if (tn) target.push(tn); }
      else if (k.nodeType === 1) walk(k, nclip, target);
    }
  }
  const out = []; walk(ROOT, [R0.left, R0.top, R0.left + VW, R0.top + VH], out);
  return { tree: out[0], imgs };
})()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build index.html and anki.csv from data.json (single source of truth).

Usage: python3 build.py
Expected location: <lesson folder>/_tools/build.py, with data.json, prepositions.svg,
timeline.svg and the pronunciation PNGs one level up (or in ./assets).
"""
import base64
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def find(rel, *candidates):
    for c in candidates:
        p = HERE / c
        if p.exists():
            return p
    raise SystemExit("missing file: " + rel)


ROOT = HERE.parent if (HERE.parent / "data.json").exists() else HERE
SRC = ROOT / "_src" if (ROOT / "_src").exists() else ROOT

data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
svg_prep = (ROOT / "prepositions.svg").read_text(encoding="utf-8")
svg_time = (ROOT / "timeline.svg").read_text(encoding="utf-8")
img1 = base64.b64encode(find("pron-000.png", "assets/pron-000.png", "_src/pron-000.png", "pron-000.png").read_bytes()).decode("ascii")
img2 = base64.b64encode(find("pron-001.png", "assets/pron-001.png", "_src/pron-001.png", "pron-001.png").read_bytes()).decode("ascii")

css_vars = "\n".join(
    [f"      --t-{k}: {v['hex']};" for k, v in data["colors"]["tense"].items()]
    + [f"      --p-{k}: {v['hex']};" for k, v in data["colors"]["prep"].items()]
)

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Lesson 22 study page - My Daughter Jane and the Drift Bottle</title>
<style>
  :root{
      --bg:#f6f7f9; --card:#ffffff; --line:#e5e7eb; --ink:#0f172a; --muted:#64748b;
      --soft:#f1f5f9; --accent:#0f172a; --radius:14px;
__CSSVARS__
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:var(--bg);color:var(--ink);font:15px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-text-size-adjust:100%}
  .wrap{max-width:1040px;margin:0 auto;padding:0 14px 60px}
  header.top{position:sticky;top:0;z-index:20;background:var(--accent);color:#fff;padding:10px 0 12px;box-shadow:0 2px 12px rgba(15,23,42,.18)}
  header.top .wrap{padding-bottom:0;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
  .lesson{background:#1e293b;border:1px solid #334155;border-radius:999px;padding:2px 10px;font-size:12.5px;letter-spacing:.5px}
  header.top h1{font-size:16px;margin:0;font-weight:650;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .prog{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#cbd5e1;white-space:nowrap}
  .prog .bar{width:96px;height:7px;background:#334155;border-radius:99px;overflow:hidden}
  .prog .bar i{display:block;height:100%;width:0;background:#38bdf8;transition:width .25s}
  nav.tabs{position:sticky;top:52px;z-index:19;background:rgba(246,247,249,.96);backdrop-filter:blur(6px);border-bottom:1px solid var(--line);margin-bottom:16px}
  nav.tabs .inner{max-width:1040px;margin:0 auto;display:flex;gap:6px;overflow-x:auto;padding:8px 14px;scrollbar-width:none}
  nav.tabs .inner::-webkit-scrollbar{display:none}
  nav.tabs button{flex:0 0 auto;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:6px 14px;font-size:13.5px;cursor:pointer}
  nav.tabs button[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
  .card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:14px 15px;margin-bottom:12px}
  .card h2{font-size:15.5px;margin:0 0 10px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
  .card h3{font-size:14px;margin:14px 0 6px;color:#334155}
  .muted{color:var(--muted)}
  .small{font-size:12.5px}
  .pg{display:inline-block;background:var(--soft);color:var(--muted);border-radius:6px;padding:0 6px;font-size:11.5px;margin-left:6px;vertical-align:1px;white-space:nowrap}
  .chip{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:2px 10px;font-size:12.5px;color:#fff}
  .grid{display:grid;gap:10px}
  @media(min-width:720px){.grid.two{grid-template-columns:1fr 1fr}.grid.three{grid-template-columns:repeat(3,1fr)}}
  .kv{display:grid;grid-template-columns:150px 1fr;gap:6px 10px;font-size:13.5px}
  .kv dt{color:var(--muted)}
  .kv dd{margin:0}
  ul.tight{margin:6px 0 0;padding-left:18px}
  ul.tight li{margin:3px 0}
  .ex{border-left:2px solid var(--line);padding:2px 0 2px 10px;margin:8px 0}
  .ex .en{font-weight:520}
  .ex .sub{color:var(--muted);font-size:13.5px}
  .word{font-size:20px;font-weight:700}
  .phon{color:var(--muted);margin-left:6px}
  .pos{background:var(--soft);border-radius:6px;padding:0 6px;font-size:12px;color:#475569;margin-left:6px}
  .sent{border-left:4px solid var(--line);padding:6px 0 6px 12px;margin:10px 0}
  .sent .en{font-size:15.5px}
  .sent .sub{color:var(--muted);font-size:13.5px;margin-top:2px}
  .svgwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:12px;background:#fff;padding:6px}
  .svgwrap svg{width:100%;min-width:900px;max-width:none;height:auto;display:block}
  .svgwrap img{width:100%;min-width:860px;max-width:none;height:auto;display:block}
  .scrollhint{font-size:12px;color:var(--muted);margin:4px 0 0}
  @media(min-width:1040px){.scrollhint{display:none}}
  .q{border-top:1px dashed var(--line);padding:12px 0 4px}
  .q:first-of-type{border-top:0}
  .q .qt{font-size:14.5px}
  .q .meta{font-size:12px;color:var(--muted);margin-top:2px}
  button.ansbtn{margin-top:8px;border:1px solid var(--line);background:#fff;border-radius:8px;padding:5px 12px;font-size:13px;cursor:pointer}
  button.ansbtn:hover{background:var(--soft)}
  .ans{display:none;margin-top:8px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:9px 11px;font-size:13.8px}
  .ans.show{display:block}
  .ans b{color:#15803d}
  .steps label{display:flex;gap:8px;align-items:flex-start;padding:7px 0;border-top:1px dashed var(--line);font-size:14px;cursor:pointer}
  .steps label:first-child{border-top:0}
  .steps input{margin-top:4px;width:16px;height:16px;flex:0 0 auto}
  .legend{display:flex;flex-wrap:wrap;gap:8px}
  .legend .item{border:1px solid var(--line);border-radius:10px;padding:6px 10px;font-size:12.5px;display:flex;align-items:center;gap:7px}
  .dot{width:11px;height:11px;border-radius:50%;flex:0 0 auto}
  table.files{width:100%;border-collapse:collapse;font-size:13px}
  table.files td{border-top:1px solid var(--line);padding:5px 4px;vertical-align:top}
  table.files code{background:var(--soft);border-radius:5px;padding:1px 5px;font-size:12.2px}
  /* --- interactive practice --- */
  .opts{display:grid;gap:6px;margin-top:8px}
  .opt{text-align:left;border:1px solid var(--line);background:#fff;border-radius:10px;padding:8px 11px;font-size:14px;cursor:pointer;display:flex;gap:9px;align-items:flex-start;font-family:inherit}
  .opt:hover{background:var(--soft)}
  .opt .k{font-weight:700;color:var(--muted);flex:0 0 auto}
  .opt.ok{border-color:#86efac;background:#f0fdf4}
  .opt.bad{border-color:#fca5a5;background:#fef2f2}
  .fb{margin-top:8px;font-size:13.5px;border-radius:10px;padding:8px 10px;display:none}
  .fb.show{display:block}
  .fb.ok{background:#f0fdf4;border:1px solid #bbf7d0;color:#166534}
  .fb.bad{background:#fef2f2;border:1px solid #fecaca;color:#991b1b}
  .fb b{font-weight:700}
  input.gin{border:1px solid var(--line);border-radius:8px;padding:5px 8px;font-size:14px;min-width:120px;font-family:inherit}
  input.gin.ok{border-color:#86efac;background:#f0fdf4}
  input.gin.bad{border-color:#fca5a5;background:#fef2f2}
  .row{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-top:8px}
  .tok{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 12px;font-size:13.5px;cursor:pointer;font-family:inherit}
  .tok:hover{background:var(--soft)}
  .bank,.line{display:flex;gap:6px;flex-wrap:wrap;min-height:40px;border:1px dashed var(--line);border-radius:10px;padding:6px;align-items:center}
  .line{background:#f8fafc;margin-top:8px}
  .bank{margin-top:6px}
  .mt{display:grid;gap:10px;margin-top:8px}
  @media(min-width:660px){.mt{grid-template-columns:1fr 1fr}}
  .mcol{display:grid;gap:6px}
  .mitem{border:1px solid var(--line);background:#fff;border-radius:10px;padding:7px 10px;font-size:13.5px;cursor:pointer;text-align:left;font-family:inherit}
  .mitem:hover{background:var(--soft)}
  .mitem.sel{border-color:#0f172a;background:#0f172a;color:#fff}
  .mitem.ok{border-color:#86efac;background:#f0fdf4}
  .mitem.bad{border-color:#fca5a5;background:#fef2f2}
  .frame{font-size:15px;line-height:2.4;margin-top:6px}
  .chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
  .chip-w{border:1px solid #cbd5e1;background:#f8fafc;border-radius:999px;padding:3px 10px;font-size:12.5px;cursor:pointer;font-family:inherit}
  .chip-w:hover{background:#e2e8f0}
  .scorebar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:13.5px;margin-top:6px}
  .scorebar b{font-size:16px}
  textarea.gtx{width:100%;min-height:70px;border:1px solid var(--line);border-radius:10px;padding:8px;font-family:inherit;font-size:14px;margin-top:6px}
  .solved{display:inline-block;background:#dcfce7;color:#166534;border-radius:6px;padding:0 6px;font-size:11.5px;margin-left:6px}
  footer{color:var(--muted);font-size:12.5px;text-align:center;padding:10px 0 0}
  .warn{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:8px 10px;font-size:13px;color:#92400e}
</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <span class="lesson">Lesson 22</span>
    <h1>My Daughter Jane and the Drift Bottle</h1>
    <div class="prog"><span id="ptext">0 / 6</span><span class="bar"><i id="pbar"></i></span></div>
  </div>
</header>
<nav class="tabs"><div class="inner" id="tabs" role="tablist"></div></nav>
<main class="wrap" id="view"></main>
<footer class="wrap" id="foot"></footer>

<template id="tpl-prep">__SVG_PREP__</template>
<template id="tpl-time">__SVG_TIME__</template>
<template id="tpl-pron">
  <div class="svgwrap"><img alt="Pronunciation image 1" src="data:image/png;base64,__IMG1__"></div>
  <p class="scrollhint">Swipe left and right to see the whole image on a phone.</p>
  <div class="svgwrap" style="margin-top:10px"><img alt="Pronunciation image 2" src="data:image/png;base64,__IMG2__"></div>
  <p class="scrollhint">Swipe left and right to see the whole image on a phone.</p>
</template>

<script id="lesson-data" type="application/json">__DATA__</script>
<script>
(function(){
  "use strict";
  var D = JSON.parse(document.getElementById('lesson-data').textContent);
  var TN = D.colors.tense, PR = D.colors.prep;
  var SVG_PREP = document.getElementById('tpl-prep').innerHTML;
  var SVG_TIME = document.getElementById('tpl-time').innerHTML;
  var PRON_HTML = document.getElementById('tpl-pron').innerHTML;
  var esc = function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};
  var pg = function(p){return p?'<span class="pg">'+esc(p)+'</span>':'';};
  var exLine = function(e){return '<div class="ex"><div class="en">'+esc(e.en)+'</div><div class="sub">'+esc(e.gloss)+'</div>'+pg(e.page)+'</div>';};

  var TABS = [['overview','Overview'],['vocab','Vocabulary'],['grammar','Grammar'],['text','Text'],['pron','Pronunciation'],['ex','Practice'],['writing','Writing']];
  var current = 'overview';
  var hashTab = (location.hash || '').replace('#','');
  if(TABS.some(function(t){ return t[0] === hashTab; })){ current = hashTab; }

  /* ---------- Progress: six study steps kept in localStorage ---------- */
  var STEPS = [
    'Look at the diagrams: match the colours in prepositions.svg and timeline.svg to the ideas',
    'Read the examples aloud: every pattern on the Vocabulary tab, with its page number',
    'Do the practice: every interactive item, then go back to the page of anything you missed',
    'Write your own text: seven sentences on the Writing tab template, with a new topic',
    'Retell the text in five sentences, keeping the tense chain in order',
    'Review the Anki deck: import anki.csv and work through the 40 cards'
  ];
  var PKEY = 'dsh-L22-progress-en';
  function loadProg(){ try{ return JSON.parse(localStorage.getItem(PKEY)) || []; }catch(e){ return []; } }
  function saveProg(a){ try{ localStorage.setItem(PKEY, JSON.stringify(a)); }catch(e){} }
  function paintProg(){
    var done = loadProg().length, pct = Math.round(done/STEPS.length*100);
    document.getElementById('ptext').textContent = done + ' / ' + STEPS.length;
    document.getElementById('pbar').style.width = pct + '%';
  }

  /* ---------- Tabs ---------- */
  function renderOverview(){
    var h = '';
    h += '<section class="card"><h2>Lesson facts</h2><dl class="kv">';
    h += '<dt>Lesson</dt><dd>'+esc(D.lesson)+' - '+esc(D.title)+'</dd>';
    h += '<dt>Title note</dt><dd class="muted">'+esc(D.titleNote)+'</dd>';
    h += '<dt>Source</dt><dd>'+esc(D.source)+'<div class="muted small">'+esc(D.sourcePath)+'</div></dd>';
    h += '<dt>Target level</dt><dd>'+esc(D.targetLevel)+'</dd>';
    h += '<dt>Page convention</dt><dd class="muted">'+esc(D.pageConvention)+'</dd>';
    h += '<dt>Language</dt><dd class="muted">'+esc(D.localisationNote)+'</dd>';
    h += '</dl></section>';

    h += '<section class="card"><h2>How the handout is organised</h2><div class="grid two">';
    D.structure.forEach(function(s){
      h += '<div class="ex"><div class="en">'+esc(s.part)+pg(s.pages)+'</div><div class="sub">'+esc(s.content)+'</div></div>';
    });
    h += '</div></section>';

    h += '<section class="card"><h2>Colour conventions (two palettes, never mixed)</h2>'
      +  '<h3>Tense colours - used only in timeline.svg and on the tense tags of the Text tab</h3><div class="legend">';
    Object.keys(TN).forEach(function(k){
      h += '<span class="item"><i class="dot" style="background:'+TN[k].hex+'"></i><b>'+esc(TN[k].name)+'</b><span class="muted">'+esc(TN[k].hint)+'</span></span>';
    });
    h += '</div><h3>Preposition colours - used only in prepositions.svg</h3><div class="legend">';
    Object.keys(PR).forEach(function(k){
      h += '<span class="item"><i class="dot" style="background:'+PR[k].hex+'"></i><b>'+esc(PR[k].name)+'</b><span class="muted">'+esc(PR[k].core)+'</span></span>';
    });
    h += '</div><p class="small muted" style="margin-top:8px">'+esc(D.colors.note)+'</p></section>';

    h += '<section class="card"><h2>Study steps and progress</h2><div class="steps" id="steps">';
    var prog = loadProg();
    STEPS.forEach(function(s,i){
      h += '<label><input type="checkbox" data-i="'+i+'"'+(prog.indexOf(i)>=0?' checked':'')+'><span>'+esc(s)+'</span></label>';
    });
    h += '</div></section>';

    h += '<section class="card"><h2>Files in this package</h2><table class="files">';
    [['data.json','The single source of truth: vocabulary, grammar, text, pronunciation, writing, practice'],
     ['mindmap.mmd','Mermaid mind map (vocabulary, grammar, text, pronunciation, writing, practice)'],
     ['concept-map.mmd','Mermaid concept map (pattern network, confusables, tense contrast, text logic)'],
     ['prepositions.svg','Image schemas for in / on / from / of (the same drawing is embedded in the Grammar tab)'],
     ['timeline.svg','The five-tense timeline (the same drawing is embedded in the Text tab)'],
     ['index.html','This file: a single offline study page, no external dependencies'],
     ['anki.csv','Anki cards, UTF-8, fields Front,Back,Tags,Examples,Image'],
     ['README.md','How to use the package and a suggested study routine']].forEach(function(r){
      h += '<tr><td><code>'+esc(r[0])+'</code></td><td>'+esc(r[1])+'</td></tr>';
    });
    h += '</table></section>';

    h += '<section class="card"><h2>Quality check</h2><ul class="tight">';
    D.checklist.forEach(function(c){ h += '<li><b>'+esc(c.item)+'</b>: '+esc(c.result)+'</li>'; });
    h += '</ul><p class="small muted" style="margin-top:8px">Pronunciation note: '+esc(D.pronunciation.sourceNote)+'</p></section>';
    return h;
  }

  function renderVocab(){
    var h = '';
    D.vocab.forEach(function(v){
      h += '<section class="card"><h2><span class="word">'+esc(v.word)+'</span><span class="phon">'+esc(v.phonetic)+'</span><span class="pos">'+esc(v.pos)+'</span>'+pg(v.pages)+'</h2>';
      h += '<dl class="kv"><dt>Core meaning</dt><dd>'+esc(v.coreMeaning)+'</dd><dt>Extended meaning</dt><dd>'+esc(v.extendedMeaning)+'</dd></dl>';
      h += '<h3>Patterns</h3><ul class="tight">';
      v.patterns.forEach(function(p){ h += '<li>'+esc(p)+'</li>'; });
      h += '</ul><h3>Examples (quoted from the handout)</h3>';
      v.examples.forEach(function(e){ h += exLine(e); });
      h += '<h3>Watch out</h3><ul class="tight">';
      v.confusions.forEach(function(c){ h += '<li>'+esc(c)+'</li>'; });
      h += '</ul>';
      if(v.notes){ h += '<p class="small muted" style="margin-top:8px">'+esc(v.notes)+'</p>'; }
      h += '</section>';
    });
    return h;
  }

  function renderGrammar(){
    var h = '<section class="card"><h2>Preposition image schemas<span class="pg">prepositions.svg</span></h2>'
      + '<div class="svgwrap">'+SVG_PREP+'</div><p class="scrollhint">Swipe left and right to see the whole diagram on a phone.</p>'
      + '<p class="small muted">in blue, on green, from orange, of purple. All examples come from the handout, p8-p9.</p></section>';
    D.grammar.forEach(function(g){
      h += '<section class="card"><h2>'+esc(g.point)+pg(g.page);
      ['of','from','in','on'].forEach(function(k){
        if(new RegExp('\\b'+k+'\\b').test(g.point)){ h += '<span class="chip" style="background:'+PR[k].hex+'">'+k+'</span>'; }
      });
      h += '</h2><p>'+esc(g.coreIdea)+'</p>';
      h += '<h3>Rules</h3><ul class="tight">';
      g.rules.forEach(function(r){ h += '<li>'+esc(r)+'</li>'; });
      h += '</ul><h3>Examples</h3>';
      g.examples.forEach(function(e){ h += exLine(e); });
      if(g.commonMistakes && g.commonMistakes.length){
        h += '<h3>Common mistakes</h3><ul class="tight">';
        g.commonMistakes.forEach(function(m){ h += '<li>'+esc(m)+'</li>'; });
        h += '</ul>';
      }
      if(g.reviewNote){ h += '<p class="small muted" style="margin-top:8px">'+esc(g.reviewNote)+'</p>'; }
      h += '</section>';
    });
    return h;
  }

  function renderText(){
    var h = '<section class="card"><h2>The text<span class="pg">p4-p7</span></h2><p>'+esc(D.text.original)+'</p>'
      + '<h3>Plain-English gloss</h3><p class="muted">'+esc(D.text.gloss)+'</p></section>';
    h += '<section class="card"><h2>Sentence by sentence, with its tense</h2>';
    D.text.sentences.forEach(function(s){
      var t = TN[s.tenseKey];
      h += '<div class="sent" style="border-left-color:'+t.hex+'"><div class="en">'+esc(s.en)+'</div><div class="sub">'+esc(s.gloss)+'</div>'
        +  '<div style="margin-top:4px"><span class="chip" style="background:'+t.hex+'">'+esc(t.name)+'</span>'+pg(s.page)+'</div></div>';
    });
    h += '</section>';
    h += '<section class="card"><h2>Tense timeline<span class="pg">timeline.svg</span></h2>'
      + '<div class="svgwrap">'+SVG_TIME+'</div><p class="scrollhint">Swipe left and right to see the whole diagram on a phone.</p></section>';
    h += '<section class="card"><h2>Teaching points, sentence by sentence</h2>';
    D.text.points.forEach(function(p){
      h += '<div class="ex"><div class="en">'+esc(p.target)+pg(p.page)+'</div><div class="sub">'+esc(p.detail)+'</div></div>';
    });
    h += '</section>';
    h += '<section class="card"><h2>Linking words</h2><ul class="tight">';
    D.text.logic.forEach(function(l){ h += '<li><b>'+esc(l.marker)+'</b> ('+esc(l.page)+'): '+esc(l.relation)+'</li>'; });
    h += '</ul><h3>Review</h3><ul class="tight">';
    D.text.reviews.forEach(function(r){ h += '<li><b>'+esc(r.source)+'</b> ('+esc(r.page)+'): '+esc(r.en)+' - '+esc(r.gloss)+'</li>'; });
    h += '</ul></section>';
    return h;
  }

  function renderPron(){
    var p = D.pronunciation;
    var h = '<section class="card"><h2>The handout\'s pronunciation page<span class="pg">p7</span></h2><div class="warn">'+esc(p.sourceNote)+'</div>';
    h += PRON_HTML;
    p.images.forEach(function(im){ h += '<p class="small muted" style="margin-top:8px">'+esc(im.caption)+'</p>'; });
    h += '</section>';
    h += '<section class="card"><h2>Transcriptions and words</h2><ul class="tight">';
    p.words.forEach(function(w){ h += '<li><b>'+esc(w.word)+'</b>'+(w.phonetic?' <span class="phon">'+esc(w.phonetic)+'</span>':'')+': '+esc(w.note)+pg(w.page)+'</li>'; });
    h += '</ul></section>';
    h += '<section class="card"><h2>Linking points (blue arcs)</h2><ul class="tight">';
    p.linking.forEach(function(l){ h += '<li><b>'+esc(l.pair)+'</b>: '+esc(l.detail)+pg(l.page)+'</li>'; });
    h += '</ul></section>';
    h += '<section class="card"><h2>Special marks</h2><ul class="tight">';
    p.specialMarks.forEach(function(m){ h += '<li><b>'+esc(m.mark)+'</b>: '+esc(m.detail)+pg(m.page)+'</li>'; });
    h += '</ul></section>';
    h += '<section class="card"><h2>Stress</h2><ul class="tight">';
    p.stress.forEach(function(s){ h += '<li><b>'+esc(s.item)+'</b>: '+esc(s.detail)+pg(s.page)+'</li>'; });
    h += '</ul></section>';
    return h;
  }

  /* ---------- Interactive practice engine ---------- */
  var SPKEY = 'dsh-L22-score-en-v2', FPKEY = 'dsh-L22-free-en-v2';
  var LOOK = {};
  ['mcq','gap','tf','order','match'].forEach(function(k){
    (D.practice[k]||[]).forEach(function(it){ LOOK[it.id] = it; });
  });
  var WFRAMES = D.practice.write.frames;
  WFRAMES.forEach(function(f){ if(f.scored !== false){ LOOK[f.id] = f; } });
  var PKEYS = Object.keys(LOOK);
  function loadScore(){ try{ return JSON.parse(localStorage.getItem(SPKEY)) || {}; }catch(e){ return {}; } }
  function saveScore(o){ try{ localStorage.setItem(SPKEY, JSON.stringify(o)); }catch(e){} }
  function setScore(id, ok){ var s = loadScore(); s[id] = ok ? 1 : 0; saveScore(s); paintScore(); }
  function paintScore(){
    var s = loadScore(), n = 0;
    PKEYS.forEach(function(k){ if(s[k] === 1){ n++; } });
    var el = document.getElementById('score');
    if(el){ el.innerHTML = '<b>'+n+'</b> / '+PKEYS.length+' solved'; }
  }
  function norm(x){
    return String(x==null?'':x).toLowerCase()
      .replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"')
      .replace(/[^a-z0-9' ]+/g, ' ').replace(/\s+/g, ' ').trim()
      .replace(/^(a|an|the) /, '');
  }
  function okAns(given, accepts){
    var g = norm(given);
    if(!g){ return false; }
    for(var i=0;i<accepts.length;i++){ if(norm(accepts[i]) === g){ return true; } }
    return false;
  }
  function fb(id, kind, html){
    var el = document.getElementById('fb-'+id);
    if(!el){ return; }
    el.className = 'fb show ' + (kind === 'bad' ? 'bad' : 'ok');
    el.innerHTML = html;
  }
  function shuffle(arr, seed){
    var a = arr.slice(), s = seed || 7;
    for(var i=a.length-1;i>0;i--){ s = (s*9301 + 49297) % 233280; var j = Math.floor(s/233280*(i+1)); var t=a[i]; a[i]=a[j]; a[j]=t; }
    return a;
  }
  function seedOf(id){ var n=0; for(var i=0;i<id.length;i++){ n = (n*31 + id.charCodeAt(i)) % 99991; } return n+7; }
  function solvedBadge(id){ return (loadScore()[id] === 1) ? '<span class="solved">solved</span>' : ''; }

  function renderPractice(){
    var P = D.practice, h = '';
    h += '<section class="card"><h2>Interactive practice</h2><p>'+esc(P.intro)+'</p>'
      +  '<div class="scorebar"><span id="score"></span>'
      +  '<button class="ansbtn" id="resetScore">Reset score</button>'
      +  '<button class="ansbtn" id="revealAll">Show every answer</button></div>'
      +  '<p class="small muted" style="margin-top:6px">'+esc(P.note)+'</p></section>';

    h += '<section class="card"><h2>1 &#183; Multiple choice<span class="pg">'+P.mcq.length+' items</span></h2>';
    P.mcq.forEach(function(it,i){
      h += '<div class="q"><div class="qt">'+(i+1)+'. '+esc(it.prompt)+pg(it.page)+solvedBadge(it.id)+'</div><div class="opts">';
      it.options.forEach(function(o,j){
        h += '<button class="opt" data-mcq="'+it.id+'" data-j="'+j+'"><span class="k">'+'ABCD'[j]+'</span><span>'+esc(o)+'</span></button>';
      });
      h += '</div><div class="fb" id="fb-'+it.id+'"></div></div>';
    });
    h += '</section>';

    h += '<section class="card"><h2>2 &#183; Gap fill: type the missing word<span class="pg">'+P.gap.length+' items</span></h2>';
    P.gap.forEach(function(it,i){
      h += '<div class="q"><div class="qt">'+(i+1)+'. '+esc(it.prompt)+pg(it.page)+solvedBadge(it.id)+'</div>'
        +  '<div class="row"><input class="gin" data-gap="'+it.id+'" placeholder="missing word" autocomplete="off" autocapitalize="off" spellcheck="false">'
        +  '<button class="ansbtn" data-checkgap="'+it.id+'">Check</button>'
        +  '<button class="ansbtn" data-showgap="'+it.id+'">Show answer</button></div>'
        +  '<div class="fb" id="fb-'+it.id+'"></div></div>';
    });
    h += '</section>';

    h += '<section class="card"><h2>3 &#183; True or false<span class="pg">'+P.tf.length+' items</span></h2>';
    P.tf.forEach(function(it,i){
      h += '<div class="q"><div class="qt">'+(i+1)+'. '+esc(it.statement)+pg(it.page)+solvedBadge(it.id)+'</div>'
        +  '<div class="row"><button class="ansbtn" data-tf="'+it.id+'" data-v="true">True</button>'
        +  '<button class="ansbtn" data-tf="'+it.id+'" data-v="false">False</button></div>'
        +  '<div class="fb" id="fb-'+it.id+'"></div></div>';
    });
    h += '</section>';

    h += '<section class="card"><h2>4 &#183; Word order: click the words in the right order<span class="pg">'+P.order.length+' items</span></h2>';
    P.order.forEach(function(it,i){
      h += '<div class="q"><div class="qt">'+(i+1)+'. '+esc(it.hint)+pg(it.page)+solvedBadge(it.id)+'</div>'
        +  '<div class="line" id="line-'+it.id+'"></div><div class="bank" id="bank-'+it.id+'"></div>'
        +  '<div class="row"><button class="ansbtn" data-checkorder="'+it.id+'">Check</button>'
        +  '<button class="ansbtn" data-resetorder="'+it.id+'">Clear</button></div>'
        +  '<div class="fb" id="fb-'+it.id+'"></div></div>';
    });
    h += '</section>';

    h += '<section class="card"><h2>5 &#183; Matching: click a left item, then its partner<span class="pg">'+P.match.length+' tasks</span></h2>';
    P.match.forEach(function(it,i){
      var L = shuffle(it.left.map(function(t,j){ return {t:t,j:j}; }), seedOf(it.id));
      var R = shuffle(it.right.map(function(t,j){ return {t:t,j:j}; }), seedOf(it.id+'r'));
      h += '<div class="q"><div class="qt">'+(i+1)+'. '+esc(it.title)+pg(it.page)+solvedBadge(it.id)+'</div><div class="mt">'
        +  '<div class="mcol">'+L.map(function(o){ return '<button class="mitem" data-match="'+it.id+'" data-side="l" data-j="'+o.j+'">'+esc(o.t)+'</button>'; }).join('')+'</div>'
        +  '<div class="mcol">'+R.map(function(o){ return '<button class="mitem" data-match="'+it.id+'" data-side="r" data-j="'+o.j+'">'+esc(o.t)+'</button>'; }).join('')+'</div>'
        +  '</div><div class="row"><button class="ansbtn" data-resetmatch="'+it.id+'">Clear</button></div>'
        +  '<div class="fb" id="fb-'+it.id+'"></div></div>';
    });
    h += '</section>';

    var W = P.write;
    h += '<section class="card"><h2>6 &#183; Guided imitation writing, one sentence at a time</h2><p>'+esc(W.intro)+'</p>'
      +  '<p class="small muted">'+esc(W.modelNote)+'</p>';
    W.frames.forEach(function(f){
      h += '<div class="q"><div class="qt">'+esc(f.label)+pg(f.page)+solvedBadge(f.id)+'</div>';
      if(f.free){
        h += '<p class="small muted">'+esc(f.prompt)+'</p>'
          +  '<textarea class="gtx" id="free-'+f.id+'" placeholder="Your own last sentence, with will ..."></textarea>'
          +  '<div class="chips">'+f.bank.map(function(w){ return '<button class="chip-w" data-free="'+f.id+'" data-w="'+esc(w)+'">'+esc(w)+'</button>'; }).join('')+'</div>'
          +  '<div class="row"><button class="ansbtn" data-showmodel="'+f.id+'">Compare with the model</button></div>'
          +  '<div class="fb" id="fb-'+f.id+'"></div>';
      } else {
        h += '<div class="frame">';
        f.parts.forEach(function(pt){
          if(pt.t !== undefined){ h += esc(pt.t); }
          else {
            var bl = f.blanks[pt.b];
            h += '<input class="gin" data-w="'+f.id+'" data-b="'+pt.b+'" placeholder="'+esc(bl.hint)+'" autocomplete="off" autocapitalize="off" spellcheck="false">';
          }
        });
        h += '</div>';
        f.blanks.forEach(function(b,k){
          if(b.bank){
            h += '<div class="chips">'+b.bank.map(function(w){ return '<button class="chip-w" data-wbank="'+f.id+'" data-b="'+k+'" data-w="'+esc(w)+'">'+esc(w)+'</button>'; }).join('')+'</div>';
          }
        });
        h += '<div class="row"><button class="ansbtn" data-checkwrite="'+f.id+'">Check this sentence</button>'
          +  '<button class="ansbtn" data-showmodel="'+f.id+'">Show model sentence</button></div>'
          +  '<div class="fb" id="fb-'+f.id+'"></div>';
      }
      h += '</div>';
    });
    h += '</section>';
    return h;
  }

  function paintOrder(it){
    var bank = document.getElementById('bank-'+it.id), line = document.getElementById('line-'+it.id);
    if(!bank || !line){ return; }
    var toks = shuffle(it.tokens.map(function(t,i){ return {t:t,i:i}; }), seedOf(it.id));
    bank.innerHTML = toks.map(function(o){ return '<button class="tok" data-tok="'+it.id+'" data-i="'+o.i+'">'+esc(o.t)+'</button>'; }).join('');
    line.innerHTML = '';
  }
  function orderLine(it){
    var line = document.getElementById('line-'+it.id);
    return Array.prototype.map.call(line.querySelectorAll('.tok'), function(b){ return b.textContent; }).join(' ');
  }
  function selectMatch(btn){
    var id = btn.dataset.match, side = btn.dataset.side;
    var box = btn.closest('.q');
    if(side === 'l'){
      Array.prototype.forEach.call(box.querySelectorAll('[data-side="l"]'), function(b){ b.classList.remove('sel'); });
      btn.classList.add('sel');
      return;
    }
    var sel = box.querySelector('[data-side="l"].sel');
    if(!sel){ fb(id, 'bad', '<b>Pick a left-hand item first.</b>'); return; }
    if(sel.dataset.j === btn.dataset.j){
      sel.classList.remove('sel'); sel.classList.add('ok'); btn.classList.add('ok');
      sel.disabled = true; btn.disabled = true;
      var left = box.querySelectorAll('[data-side="l"].ok').length;
      var total = box.querySelectorAll('[data-side="l"]').length;
      if(left === total){ setScore(id, true); fb(id, 'ok', '<b>All pairs matched.</b>'); }
      else { fb(id, 'ok', '<b>Correct pair. </b>' + left + ' of ' + total + ' matched.'); }
    } else {
      btn.classList.add('bad'); sel.classList.remove('sel');
      var self = btn;
      setTimeout(function(){ self.classList.remove('bad'); }, 700);
      fb(id, 'bad', '<b>Not this one.</b> Try again: click a left item, then its partner.');
    }
  }
  function checkWrite(f){
    var allOk = true, wrong = [];
    f.blanks.forEach(function(b,k){
      var inp = document.querySelector('input[data-w="'+f.id+'"][data-b="'+k+'"]');
      if(!inp){ return; }
      var val = inp.value, ok;
      if(b.anyNonEmpty){ ok = norm(val).length > 0; }
      else { ok = okAns(val, b.accepts); }
      inp.classList.toggle('ok', ok); inp.classList.toggle('bad', !ok);
      if(!ok){ allOk = false; wrong.push(b.hint); }
    });
    setScore(f.id, allOk);
    if(allOk){ fb(f.id, 'ok', '<b>Good - this sentence is correct.</b> Model: ' + esc(f.model)); }
    else { fb(f.id, 'bad', '<b>Check these parts:</b> ' + esc(wrong.join(' / ')) + '<br><b>Model: </b>' + esc(f.model)); }
  }
  function revealAll(){
    D.practice.mcq.forEach(function(it){
      var box = document.querySelector('[data-mcq="'+it.id+'"]');
      if(!box){ return; }
      Array.prototype.forEach.call(box.querySelectorAll('.opt'), function(o,k){
        o.disabled = true;
        if(k === it.answer){ o.classList.add('ok'); }
      });
      fb(it.id, 'ok', '<b>Answer: </b>'+esc(it.options[it.answer])+'. '+esc(it.explain));
    });
    D.practice.gap.forEach(function(it){
      var inp = document.querySelector('input[data-gap="'+it.id+'"]');
      if(!inp){ return; }
      inp.value = it.answer; inp.classList.add('ok'); inp.classList.remove('bad');
      fb(it.id, 'ok', '<b>Answer: </b>'+esc(it.answer)+'. '+esc(it.explain));
    });
    D.practice.tf.forEach(function(it){
      fb(it.id, 'ok', '<b>Answer: </b>'+(it.answer ? 'True' : 'False')+'. '+esc(it.explain));
    });
    D.practice.order.forEach(function(it){
      var bank = document.getElementById('bank-'+it.id), line = document.getElementById('line-'+it.id);
      if(!bank || !line){ return; }
      bank.innerHTML = '';
      line.innerHTML = it.tokens.map(function(t){ return '<button class="tok" disabled>'+esc(t)+'</button>'; }).join('');
      fb(it.id, 'ok', '<b>Answer: </b>'+esc(it.target));
    });
    D.practice.match.forEach(function(it){
      var box = document.querySelector('[data-match="'+it.id+'"]');
      if(!box){ return; }
      var q = box.closest('.q');
      Array.prototype.forEach.call(q.querySelectorAll('.mitem'), function(b){ b.classList.add('ok'); b.disabled = true; b.classList.remove('sel'); });
      fb(it.id, 'ok', '<b>Answers are matched in the order shown.</b>');
    });
    WFRAMES.forEach(function(f){
      if(f.free){
        fb(f.id, 'ok', '<b>Model: </b>'+esc(f.model));
        return;
      }
      f.blanks.forEach(function(b,k){
        var inp = document.querySelector('input[data-w="'+f.id+'"][data-b="'+k+'"]');
        if(!inp){ return; }
        inp.value = b.anyNonEmpty ? (b.bank ? b.bank[0] : '') : b.accepts[0];
        inp.classList.add('ok'); inp.classList.remove('bad');
      });
      fb(f.id, 'ok', '<b>Model: </b>'+esc(f.model));
    });
  }
  function onPracticeClick(ev){
    var el = ev.target;
    if(!el || !el.closest){ return; }
    var b = el.closest('[data-mcq],[data-checkgap],[data-showgap],[data-tf],[data-tok],[data-checkorder],[data-resetorder],[data-match],[data-resetmatch],[data-checkwrite],[data-showmodel],[data-wbank],[data-free],[id="resetScore"],[id="revealAll"]');
    if(!b){ return; }
    if(b.id === 'resetScore'){ saveScore({}); paint(); return; }
    if(b.id === 'revealAll'){ revealAll(); return; }
    if(b.dataset.mcq){
      var it = LOOK[b.dataset.mcq], j = parseInt(b.dataset.j,10), ok = (j === it.answer);
      Array.prototype.forEach.call(b.parentNode.querySelectorAll('.opt'), function(o,k){
        o.disabled = true;
        if(k === it.answer){ o.classList.add('ok'); } else if(k === j){ o.classList.add('bad'); }
      });
      setScore(it.id, ok);
      fb(it.id, ok?'ok':'bad', (ok?'<b>Correct. </b>':'<b>Not quite. </b>')+esc(it.explain));
      return;
    }
    if(b.dataset.checkgap){
      var g = LOOK[b.dataset.checkgap], inp = document.querySelector('input[data-gap="'+g.id+'"]');
      var good = okAns(inp.value, g.accepts);
      inp.classList.toggle('ok', good); inp.classList.toggle('bad', !good);
      setScore(g.id, good);
      fb(g.id, good?'ok':'bad', (good?'<b>Correct. </b>':'<b>Not quite. Answer: </b>'+esc(g.answer)+'. ')+esc(g.explain));
      return;
    }
    if(b.dataset.showgap){
      var g2 = LOOK[b.dataset.showgap], inp2 = document.querySelector('input[data-gap="'+g2.id+'"]');
      inp2.value = g2.answer; inp2.classList.add('ok'); inp2.classList.remove('bad');
      fb(g2.id, 'ok', '<b>Answer: </b>'+esc(g2.answer)+'. '+esc(g2.explain));
      return;
    }
    if(b.dataset.tf){
      var t = LOOK[b.dataset.tf], val = (b.dataset.v === 'true'), ok2 = (val === t.answer);
      setScore(t.id, ok2);
      fb(t.id, ok2?'ok':'bad', (ok2?'<b>Correct. </b>':'<b>Not quite. </b>')+esc(t.explain));
      return;
    }
    if(b.dataset.tok){
      var o2 = LOOK[b.dataset.tok], line = document.getElementById('line-'+o2.id);
      if(b.parentNode.classList.contains('bank')){ line.appendChild(b); } else { document.getElementById('bank-'+o2.id).appendChild(b); }
      return;
    }
    if(b.dataset.checkorder){
      var o3 = LOOK[b.dataset.checkorder], given = orderLine(o3), ok3 = (norm(given) === norm(o3.target));
      setScore(o3.id, ok3);
      fb(o3.id, ok3?'ok':'bad', (ok3?'<b>Correct. </b>':'<b>Not quite. </b>')+esc(o3.hint));
      return;
    }
    if(b.dataset.resetorder){ paintOrder(LOOK[b.dataset.resetorder]); return; }
    if(b.dataset.match){ selectMatch(b); return; }
    if(b.dataset.resetmatch){
      var m = LOOK[b.dataset.resetmatch];
      var q = document.querySelector('[data-match="'+m.id+'"]').closest('.q');
      Array.prototype.forEach.call(q.querySelectorAll('.mitem'), function(x){ x.classList.remove('ok','bad','sel'); x.disabled = false; });
      document.getElementById('fb-'+m.id).className = 'fb';
      return;
    }
    if(b.dataset.wbank){
      var fid = b.dataset.wbank, bidx = b.dataset.b, word = b.dataset.w;
      var inputs = document.querySelectorAll('input[data-w="'+fid+'"][data-b="'+bidx+'"]');
      var target = null;
      Array.prototype.forEach.call(inputs, function(x){ if(target === null && !x.value){ target = x; } });
      if(target === null){ target = inputs[inputs.length-1]; }
      if(target){ target.value = word; target.classList.remove('bad'); }
      return;
    }
    if(b.dataset.free){
      var ta = document.getElementById('free-'+b.dataset.free);
      ta.value = (ta.value ? ta.value + ' ' : '') + b.dataset.w;
      try{ localStorage.setItem(FPKEY, ta.value); }catch(e){}
      return;
    }
    if(b.dataset.checkwrite){ checkWrite(LOOK[b.dataset.checkwrite]); return; }
    if(b.dataset.showmodel){
      var mf = WFRAMES.filter(function(x){ return x.id === b.dataset.showmodel; })[0];
      if(mf){ fb(mf.id, 'ok', '<b>Model: </b>'+esc(mf.model)); }
      return;
    }
  }

  function renderWriting(){
    var w = D.writing;
    var h = '<section class="card"><h2>'+esc(w.topic)+pg(w.page)+'</h2>';
    h += '<h3>Story plan (the handout gives this plan as well)</h3><p>'+esc(w.storyPlan)+'</p>';
    h += '<h3>Model text (the handout\'s English model)</h3><p>'+esc(w.model)+'</p>';
    h += '</section>';
    h += '<section class="card"><h2>Imitation template, seven steps</h2><ul class="tight">';
    w.template.forEach(function(t){ h += '<li>'+esc(t)+'</li>'; });
    h += '</ul><h3>Useful patterns</h3><ul class="tight">';
    w.usefulPatterns.forEach(function(t){ h += '<li>'+esc(t)+'</li>'; });
    h += '</ul><p class="small muted" style="margin-top:8px">'+esc(w.notes)+'</p></section>';
    return h;
  }

  var RENDER = {overview:renderOverview,vocab:renderVocab,grammar:renderGrammar,text:renderText,pron:renderPron,ex:renderPractice,writing:renderWriting};

  function paint(){
    document.getElementById('view').innerHTML = RENDER[current]();
    Array.prototype.forEach.call(document.querySelectorAll('#tabs button'),function(b){
      b.setAttribute('aria-selected', b.dataset.tab===current ? 'true':'false');
    });
    document.getElementById('foot').innerHTML = 'Data source: data.json &#183; handout: '+esc(D.source)+' &#183; page numbers p1-p10 match the PDF footers 1/10-10/10<br>Tense colours and preposition colours belong to two different diagrams and are never mixed.';
    bind();
    paintScore();
    window.scrollTo(0,0);
  }

  function bind(){
    Array.prototype.forEach.call(document.querySelectorAll('button.ansbtn[data-target]'),function(b){
      b.addEventListener('click',function(){
        var el = document.getElementById(b.dataset.target);
        var on = el.classList.toggle('show');
        b.textContent = on ? 'Hide answer' : 'Show answer';
      });
    });
    if(current === 'ex'){
      D.practice.order.forEach(paintOrder);
      var free = document.getElementById('free-w7');
      if(free){ try{ free.value = localStorage.getItem(FPKEY) || ''; }catch(e){} free.addEventListener('input', function(){ try{ localStorage.setItem(FPKEY, free.value); }catch(e){} }); }
    }
    var steps = document.getElementById('steps');
    if(steps){
      Array.prototype.forEach.call(steps.querySelectorAll('input'),function(cb){
        cb.addEventListener('change',function(){
          var arr = loadProg(), i = parseInt(cb.dataset.i,10), k = arr.indexOf(i);
          if(cb.checked && k<0){ arr.push(i); } else if(!cb.checked && k>=0){ arr.splice(k,1); }
          saveProg(arr); paintProg();
        });
      });
    }
  }

  document.addEventListener('click', onPracticeClick);
  var tabsEl = document.getElementById('tabs');
  TABS.forEach(function(t){
    var b = document.createElement('button');
    b.textContent = t[1]; b.dataset.tab = t[0]; b.setAttribute('role','tab');
    b.addEventListener('click',function(){ current = t[0]; location.hash = t[0]; paint(); });
    tabsEl.appendChild(b);
  });
  window.addEventListener('hashchange',function(){
    var k = (location.hash || '').replace('#','');
    if(RENDER[k] && k !== current){ current = k; paint(); }
  });
  paintProg(); paint();
})();
</script>
</body>
</html>
"""

html_out = (TEMPLATE
            .replace("__CSSVARS__", css_vars)
            .replace("__SVG_PREP__", svg_prep)
            .replace("__SVG_TIME__", svg_time)
            .replace("__IMG1__", img1)
            .replace("__IMG2__", img2)
            .replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":"))))
(ROOT / "index.html").write_text(html_out, encoding="utf-8")

# ------------------------------------------------------------------ Anki CSV
# Tags are separated by spaces (Anki splits tags on spaces, not commas).
CARDS = [
    ("dream: transcription, part of speech, core meaning?",
     "dream /driːm/ n./v. Noun: a dream, an ambition. Verb: to dream, to have an ambition. The handout says context tells you which sense is meant.",
     "Lesson22 vocab",
     "Goodnight. Sweet dreams. | A bedtime wish: sleep well and have pleasant dreams.",
     ""),
    ("What can follow dream of / dream about?",
     "sb/sth (to dream about somebody or something) or doing sth (to dream or hope to do something).",
     "Lesson22 vocab preposition",
     "She dreamed of/about becoming a chef. | Her ambition was to become a chef.",
     "prepositions.svg"),
    ("How is dream that used?",
     "dream that + clause. The word that can be left out: I dreamt (that) I got the job.",
     "Lesson22 vocab grammar",
     "She dreamed that one day she would be famous. | She hoped that one day she would be famous.",
     ""),
    ("What does daydream about mean?",
     "To let your mind wander in the daytime, to fantasise. Keep it apart from the ambition sense of dream.",
     "Lesson22 vocab",
     "daydream about | to daydream, to fantasise (p1)",
     ""),
    ("Three ways to ask about somebody's age?",
     "How old is ...? / What's ... age? / What age is ...? Answer with ... is <number> years old. or His age is <number>.",
     "Lesson22 vocab",
     "He is eight (years old). / His age is eight. | He is eight years old.",
     ""),
    ("How do you say 'at the age of ...'?",
     "at the age of + number, or at age + number.",
     "Lesson22 vocab preposition",
     "In Britain, schooling starts at age 5. | In Britain children start school at the age of five.",
     "prepositions.svg"),
    ("How does the handout express 'friends the same age'?",
     "noun + of one's own age, for example friends of their own age.",
     "Lesson22 vocab preposition",
     "Kids need friends of their own age to play with. | Children need friends of the same age to play with.",
     "prepositions.svg"),
    ("The two extended meanings of age?",
     "A historical era or period, and a very long time (for ages).",
     "Lesson22 vocab",
     "We are living in the age of technology. | We live in the age of technology. / I've been waiting for ages. | I have been waiting for a very long time.",
     ""),
    ("channel: core meaning and the capital-letter rule?",
     "A sea channel. the Channel = the English Channel, and the capital C is obligatory. Lower-case channel is just the ordinary noun.",
     "Lesson22 vocab",
     "the Channel = the English Channel | The sea between England and France (p2)",
     ""),
    ("Four extended meanings of channel?",
     "Duct or waterway (drainage/irrigation channels), fairway (narrow channel), customs lane (the green channel), TV channel (the Disney Channel).",
     "Lesson22 vocab",
     "If you have nothing to declare, go through the green channel. | At customs, use the green lane if you have nothing to declare.",
     ""),
    ("Which word is channel easily confused with?",
     "Chanel, the luxury brand. The two words are one letter apart, so watch the spelling.",
     "Lesson22 vocab",
     "Chanel vs channel | one letter apart (p3)",
     ""),
    ("The past forms of throw?",
     "threw - thrown, never 'throwed'.",
     "Lesson22 vocab grammar",
     "She threw the bottle into the sea. | She tossed the bottle into the sea.",
     "timeline.svg"),
    ("throw sth to sb or throw sth at sb?",
     "to stresses the direction, at stresses the target. throw sb sth is the double-object pattern.",
     "Lesson22 vocab preposition",
     "He threw his shirt to me. = He threw me his shirt. | He tossed his shirt in my direction.",
     "prepositions.svg"),
    ("Which preposition goes with throw to mean 'into'?",
     "throw sth into ...; into stresses the idea of 'going in'.",
     "Lesson22 vocab preposition",
     "She threw the bottle into the sea. | She tossed the bottle into the sea.",
     "prepositions.svg"),
    ("What is the core idea of of?",
     "A link between two things - not simply the Chinese possessive word.",
     "Lesson22 grammar preposition",
     "He'd been dreaming of her. | He kept dreaming about her.",
     "prepositions.svg"),
    ("What is the core idea of from?",
     "Leaving a starting point and setting off, away from.",
     "Lesson22 grammar preposition",
     "She began to walk away from him. | She started to walk away from him.",
     "prepositions.svg"),
    ("What is the core idea of in?",
     "Inside, within a frame or a container.",
     "Lesson22 grammar preposition",
     "I got stuck in a traffic jam for half an hour. | I was stuck in a traffic jam for half an hour.",
     "prepositions.svg"),
    ("What is the core idea of on?",
     "On top of, making contact with a surface.",
     "Lesson22 grammar preposition",
     "Be quiet – let me concentrate on my homework. | Be quiet, let me give my full attention to my homework.",
     "prepositions.svg"),
    ("What is a verb + preposition called and how does it behave?",
     "A phrasal verb. The unit works like a transitive verb, so an object can follow directly, and a verb after a preposition takes -ing.",
     "Lesson22 grammar",
     "She dreamed of becoming an actress. | Her ambition was to become an actress.",
     ""),
    ("What does consist of mean?",
     "To be made up of.",
     "Lesson22 grammar preposition",
     "Breakfast consists of bread and milk. | Breakfast is made up of bread and milk.",
     "prepositions.svg"),
    ("What does hear of mean?",
     "To hear about, to know of somebody.",
     "Lesson22 grammar preposition",
     "Have you heard of her? | Do you know about her?",
     "prepositions.svg"),
    ("Two frequent verb + from patterns?",
     "benefit from (to gain from) and suffer from (to be troubled by an illness or pain).",
     "Lesson22 grammar preposition",
     "Many thousands have benefited from the new treatment. | Tens of thousands have gained from it. / She's suffering from back pain. | She is troubled by back pain.",
     "prepositions.svg"),
    ("believe in and fill in - what do they mean?",
     "believe in: to trust, to have faith in. fill in: to complete a form.",
     "Lesson22 grammar preposition",
     "My son believes in Santa Claus. | My son has faith in Father Christmas. / Please fill in this application form. | Please complete this application form.",
     "prepositions.svg"),
    ("call on and focus on - what do they mean?",
     "call on: to visit somebody. focus on: to concentrate on something.",
     "Lesson22 grammar preposition",
     "Let's call on Kate on the way home. | Let's visit Kate on our way home. / Focus on your own problems. | Give your attention to your own problems.",
     "prepositions.svg"),
    ("Give an example where the verb means the same with or without the preposition.",
     "He fought the enemy. = He fought against the enemy.",
     "Lesson22 grammar preposition",
     "He fought the enemy. | He fought against the enemy.",
     "prepositions.svg"),
    ("What pattern is pay attention to?",
     "Verb + noun + preposition. An adjective can be added before the noun: pay close attention to, pay scant attention to.",
     "Lesson22 grammar preposition",
     "Pay attention to what the teacher says. | Listen carefully to what the teacher says.",
     "prepositions.svg"),
    ("How do the tenses divide around 'and' in the text?",
     "Before and: the background action in progress, past continuous. After and: the point of the sentence, a single finished action, past simple.",
     "Lesson22 grammar tense",
     "Last year, we were travelling across the Channel and Jane put a piece of paper into a bottle.",
     "timeline.svg"),
    ("Which sentence of the text is past continuous, and why?",
     "we were travelling across the Channel - it sets the background and shows an action in progress.",
     "Lesson22 tense",
     "Last year, we were travelling across the Channel. | We were crossing the English Channel.",
     "timeline.svg"),
    ("Why does 'Both girls write to each other regularly now.' take the present simple?",
     "The time markers now and regularly point to a present habit; both takes a plural noun and a plural verb.",
     "Lesson22 tense",
     "Both girls write to each other regularly now. | The two girls now write to each other at regular intervals.",
     "timeline.svg"),
    ("Why is 'However, they have decided to use the post office.' in the present perfect?",
     "It stresses the effect on the present: they no longer send letters in bottles.",
     "Lesson22 tense",
     "However, they have decided to use the post office. | Even so, they have made up their minds to use it.",
     "timeline.svg"),
    ("Which sentence of the text uses the future simple?",
     "Letters will cost a little more, but they will certainly travel faster. - it states what is very likely to happen.",
     "Lesson22 tense",
     "Letters will cost a little more, but they will certainly travel faster. | A little dearer, but certainly faster.",
     "timeline.svg"),
    ("What is special about cost?",
     "Its subject is a thing: sth cost sb + money. a little more and faster are the comparatives of much and fast.",
     "Lesson22 vocab grammar",
     "Letters will cost a little more. | Letters will cost slightly more.",
     ""),
    ("What is Jane in 'My daughter, Jane, never dreamed ...'?",
     "An appositive to My daughter: it gives the daughter's name and is set off by commas.",
     "Lesson22 grammar text",
     "My daughter, Jane, never dreamed of receiving a letter from a girl of her own age in Holland.",
     ""),
    ("What is the synonym of receive a letter from?",
     "hear from - to get a letter from somebody.",
     "Lesson22 vocab text",
     "I used to hear from my best friend. | I used to get letters from my best friend.",
     ""),
    ("Official name of Holland, its adjective and its words for the people?",
     "The official name is the Netherlands (Holland is the everyday name). Adjective: Dutch. One person: a Dutchwoman / a Dutchman. The people as a whole: the Dutch.",
     "Lesson22 vocab",
     "The Netherlands / Holland | the official name is the Netherlands (p4-p5)",
     ""),
    ("What does the handout mark on letter, bottle and little?",
     "/flap t/ - between two vowels the t / tt becomes a light American flap. The same image gives /ˈdɔːtər/ for daughter.",
     "Lesson22 pronunciation",
     "letter / bottle / little | all marked /flap t/ (p7)",
     ""),
    ("What is the (w) between into and a?",
     "An intrusive sound: a light /w/ is inserted, so into a bottle is read into-(w)-a bottle.",
     "Lesson22 pronunciation",
     "... address on it // into a bottle | p7 pronunciation image",
     ""),
    ("What does // mean in the handout's pronunciation images?",
     "A sense-group pause: ... address on it // into a bottle. Break the breath there.",
     "Lesson22 pronunciation",
     "address on it // into a bottle | p7 pronunciation image",
     ""),
    ("Transcription and stress of daughter?",
     "/ˈdɔːtər/ - the stress falls on the first syllable, daugh-.",
     "Lesson22 pronunciation",
     "My daughter, Jane, ... | p7 pronunciation image",
     ""),
    ("First line of the imitation template?",
     "My best friend, ___ (name), never dreamed of receiving a ___ (object) from a ___ (person) of his/her own age.",
     "Lesson22 writing",
     "My best friend, Mary, never dreamed of receiving an email from a boy of her own age.",
     ""),
]

with (ROOT / "anki.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    w.writerow(["Front", "Back", "Tags", "Examples", "Image"])
    for c in CARDS:
        w.writerow(list(c))

print("index.html %.1f KB" % ((ROOT / "index.html").stat().st_size / 1024))
print("anki.csv cards:", len(CARDS))

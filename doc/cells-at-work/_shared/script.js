(function(){
  'use strict';
  function $(sel, root){ return (root || document).querySelector(sel); }
  function $all(sel, root){ return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function initActiveTopNav(){
    var page = document.body.getAttribute('data-page') || '';
    var target = page;
    if(page.indexOf('vol-') === 0) target = 'vol-01-basic-defense.html';
    if(page.indexOf('spin-offs-') === 0) target = 'spin-offs-microbiome.html';
    $all('.lablinks a').forEach(function(a){
      a.classList.toggle('active', a.getAttribute('href') === target);
    });
  }
  function initMenus(){
    var btn = $('.bench-toggle'); var nav = $('#lablinks'); var rail = $('.slide-rail');
    if(!btn || !nav) return;
    btn.addEventListener('click', function(){
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      if(rail) rail.classList.toggle('is-open', !open);
    });
  }


  function initPageOutline(){
    var main = $('.workbench');
    if(!main || document.querySelector('.page-outline')) return;
    var selectors = [
      '.workbench > section > h2',
      '.workbench .section-head > h2',
      '.workbench .mechanism-section > h2',
      '.workbench .chapter-card h3',
      '.workbench .series-panel h3',
      '.workbench .special-card h3',
      '.workbench .guide-card h3',
      '.workbench .glossary-block h3'
    ].join(',');
    var seen = {};
    var items = [];
    function cleanLabel(el){
      var clone = el.cloneNode(true);
      $all('small', clone).forEach(function(s){ s.remove(); });
      return clone.textContent.replace(/\s+/g,' ').trim();
    }
    function getTarget(el, index){
      var holder = el.closest('article[id], section[id]');
      if(holder && holder.id) return holder;
      if(!el.id) el.id = 'outline-' + (document.body.getAttribute('data-page') || 'page').replace(/[^a-z0-9]+/gi,'-') + '-' + index;
      return el;
    }
    $all(selectors, main).forEach(function(el, index){
      if(el.closest('.page-outline')) return;
      var label = cleanLabel(el);
      if(!label || label.length < 2) return;
      var target = getTarget(el, index + 1);
      if(seen[target.id]) return;
      seen[target.id] = true;
      items.push({ id: target.id, label: label, level: el.tagName.toLowerCase() === 'h3' ? 3 : 2 });
    });
    if(items.length < 2) return;
    var aside = document.createElement('aside');
    aside.className = 'page-outline';
    aside.setAttribute('aria-label','本页大纲目录');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'outline-toggle';
    btn.setAttribute('aria-expanded','false');
    btn.innerHTML = '<span aria-hidden="true">☰</span><b>本页大纲</b><em class="outline-count" aria-hidden="true">' + items.length + '</em>';
    var panel = document.createElement('nav');
    panel.className = 'outline-panel';
    panel.setAttribute('aria-label','本页目录');
    var title = document.createElement('div');
    title.className = 'outline-title';
    title.textContent = '本页目录';
    panel.appendChild(title);
    items.forEach(function(item){
      var a = document.createElement('a');
      a.href = '#' + item.id;
      a.className = 'outline-link level-' + item.level;
      a.textContent = item.label;
      a.addEventListener('click', function(){
        aside.classList.remove('is-open');
        btn.setAttribute('aria-expanded','false');
      });
      panel.appendChild(a);
    });
    aside.appendChild(btn);
    aside.appendChild(panel);
    aside.classList.add('is-attention');
    document.body.appendChild(aside);
    var attentionTimer = window.setTimeout(function(){ aside.classList.remove('is-attention'); }, 6500);
    btn.addEventListener('click', function(){
      window.clearTimeout(attentionTimer);
      aside.classList.remove('is-attention');
      var open = aside.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape'){
        aside.classList.remove('is-open');
        btn.setAttribute('aria-expanded','false');
      }
    });
    if('IntersectionObserver' in window){
      var links = {};
      $all('.outline-link', panel).forEach(function(a){ links[a.getAttribute('href').slice(1)] = a; });
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            $all('.outline-link.is-active', panel).forEach(function(a){ a.classList.remove('is-active'); });
            var active = links[entry.target.id];
            if(active) active.classList.add('is-active');
          }
        });
      }, { rootMargin: '-18% 0px -68% 0px', threshold: 0.01 });
      items.forEach(function(item){
        var target = document.getElementById(item.id);
        if(target) observer.observe(target);
      });
    }
  }

  function initProgressBar(){
    if (document.getElementById('flow-progress')) return;
    var bar = document.createElement('div');
    bar.id = 'flow-progress';
    bar.className = 'flow-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);
    var ticking = false;
    function update(){
      var doc = document.documentElement;
      var max = Math.max(1, doc.scrollHeight - window.innerHeight);
      var ratio = Math.min(1, Math.max(0, window.scrollY / max));
      bar.style.transform = 'scaleX(' + ratio.toFixed(4) + ')';
      ticking = false;
    }
    function requestUpdate(){
      if(!ticking){
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }
    update();
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);
  }
  function initChapterSearch(){
    $all('.chapter-search').forEach(function(input){
      input.addEventListener('input', function(){
        var q = input.value.trim().toLowerCase();
        $all('.chapter-card').forEach(function(card){
          var txt = (card.textContent + ' ' + (card.dataset.keywords || '')).toLowerCase();
          card.classList.toggle('is-hidden', q && txt.indexOf(q) === -1);
        });
      });
    });
  }
  function initGlossarySearch(){
    var input = $('#glossarySearch'); if(!input) return;
    input.addEventListener('input', function(){
      var q = input.value.trim().toLowerCase();
      $all('.glossary-block').forEach(function(block){
        block.classList.toggle('is-hidden', q && block.textContent.toLowerCase().indexOf(q) === -1);
      });
    });
  }
  function initChart(){
    var el = $('#domainChart'); if(!el) return;
    if(!window.echarts){ el.innerHTML = '<p>领域分布：免疫学、微生物/病毒、血液循环、皮肤屏障、肿瘤与药物、公共卫生、发育/生殖/动物。</p>'; return; }
    var chart = echarts.init(el);
    chart.setOption({
      color:['#0F766E','#14B8A6','#FFB000','#E85D75','#7C3AED','#2563EB','#84CC16'],
      tooltip:{trigger:'item'},
      radar:{indicator:[
        {name:'免疫学',max:20},{name:'微生物/病毒',max:20},{name:'血液循环',max:14},{name:'皮肤屏障',max:10},{name:'肿瘤/药物',max:14},{name:'公共卫生',max:14},{name:'发育/物种',max:12}
      ],radius:'62%',axisName:{color:'#102A2A'}},
      series:[{type:'radar',areaStyle:{opacity:.18},data:[{name:'知识覆盖',value:[18,19,10,7,12,11,9]}]}]
    });
    window.addEventListener('resize', function(){ chart.resize(); });
  }
  function initSvg(){
    var el = $('#cellSvg'); if(!el || !window.SVG) return;
    el.innerHTML = '';
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var draw = SVG().addTo(el).viewbox(0,0,360,280).size('100%','100%');
    draw.rect(360,280).radius(28).fill('#F8FEFC');
    draw.circle(242).center(180,126).fill('none').stroke({color:'#0F766E',width:10,opacity:.18});
    var scope = draw.circle(224).center(180,126).fill('#D9FFF8').stroke({color:'#0F766E',width:3});
    var clip = draw.clip().add(draw.circle(224).center(180,126));
    var g = draw.group().clipWith(clip);
    g.path('M35 158 C92 82 150 209 233 121 C278 75 318 109 350 76').fill('none').stroke({color:'#76D5CC',width:34,opacity:.7});
    g.path('M36 158 C92 82 150 209 233 121 C278 75 318 109 350 76').fill('none').stroke({color:'#0F766E',width:4,dasharray:'10 8',opacity:.9});
    function red(x,y,rx,ry,rot){ return g.ellipse(rx*2,ry*2).center(x,y).fill('#F87171').opacity(.86).rotate(rot,x,y); }
    function platelet(x,y,r){ return g.circle(r*2).center(x,y).fill('#FFB000').opacity(.95); }
    function pathogen(x,y){
      var pg = g.group().translate(x,y);
      pg.circle(32).center(0,0).fill('#E85D75');
      [[0,-25,0,-18],[0,18,0,25],[-25,0,-18,0],[18,0,25,0],[-18,-18,-13,-13],[18,18,13,13],[-18,18,-13,13],[18,-18,13,-13]].forEach(function(a){ pg.line(a[0],a[1],a[2],a[3]).stroke({color:'#E85D75',width:4,linecap:'round'}); });
      return pg;
    }
    var moving = [red(86,132,23,16,-20), red(135,180,19,13,24), red(251,106,21,14,-18)];
    var white = g.group();
    white.circle(56).center(202,91).fill('#fff').stroke({color:'#14B8A6',width:4});
    white.path('M192 87 C202 72 221 83 211 98 C206 108 187 103 192 87Z').fill('#BFEDE6').stroke({color:'#0F766E',width:2});
    [platelet(112,91,7), platelet(125,84,5), platelet(132,98,6)];
    var bad = pathogen(276,158);
    var labels = draw.group().font({family:'Noto Sans SC, sans-serif',size:12,weight:700});
    function label(x,y,w,txt,bg,fg){ labels.rect(w,26).move(x,y).radius(13).fill(bg); labels.text(txt).center(x+w/2,y+13).fill(fg); }
    label(28,28,76,'运输','#FEE2E2','#DC2626'); label(238,30,76,'免疫','#DCFCE7','#0F766E'); label(28,222,76,'止血','#FEF3C7','#B45309'); label(238,222,76,'病原','#FFE4E6','#E85D75');
    draw.text('Body city under lens').font({family:'Noto Serif SC',size:16,weight:700}).fill('#0F766E').move(98,250);
    if(!reduce){
      moving.forEach(function(c,i){ c.animate(3200+i*350,0,'now').dmove(i%2?7:-6,i%2?-5:5).loop(true,true); });
      white.animate(4200,0,'now').dmove(5,-4).loop(true,true);
      bad.animate(2600,0,'now').scale(1.08,1.08).loop(true,true);
    }
  }
  document.addEventListener('DOMContentLoaded', function(){ initActiveTopNav(); initMenus(); initPageOutline(); initProgressBar(); initChapterSearch(); initGlossarySearch(); initChart(); initSvg(); });
})();

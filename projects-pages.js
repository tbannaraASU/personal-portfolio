/* V12 public static projects archive and individually linkable project case studies. */
'use strict';
(() => {
  const root=document.documentElement;
  const btn=document.getElementById('theme-toggle');
  let theme='light';try{theme=localStorage.getItem('portfolio-theme')||'light';}catch(_){}
  const apply=t=>{root.dataset.theme=t==='dark'?'dark':'light';btn.textContent=t==='dark'?'☀ Light mode':'☾ Dark mode';btn.setAttribute('aria-pressed',String(t==='dark'));};
  apply(theme);
  btn.addEventListener('click',()=>{const next=root.dataset.theme==='dark'?'light':'dark';apply(next);try{localStorage.setItem('portfolio-theme',next);}catch(_){}});
  document.getElementById('year').textContent=new Date().getFullYear();
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const text=value=>esc(value||'');
  const visible=window.PORTFOLIO_CONTENT?.sections?.find(s=>s.kind==='projects')?.items?.filter(x=>x.enabled!==false)||[];
  const tags=value=>String(value||'').trim().toLowerCase().split(/[\s,]+/).filter(Boolean);
  const imagePaths=value=>String(value||'').split(/\r?\n/).map(t=>t.trim()).filter(t=>/^project-images\/[a-zA-Z0-9_-]+\.(?:webp|jpg|jpeg|png)$/i.test(t)).slice(0,16);
  const lines=value=>String(value||'').split(/\r?\n/).map(t=>t.trim().replace(/^[-•*]\s*/, '')).filter(Boolean);
  const url=value=>{
    const v=String(value||'').trim();
    if(!v)return '';
    try{const parsed=new URL(v,location.href);return ['http:','https:'].includes(parsed.protocol)?parsed.href:'';}catch(_){return '';}
  };
  const links=project=>{
    const vals=[[project.github_url,'View code on GitHub'],[project.demo_url,'Live demo'],[project.link,project.link_label||'Project link']];
    const used=new Set();
    return vals.map(([raw,label])=>{const href=url(raw);if(!href||used.has(href))return '';used.add(href);return `<a class="button button-secondary" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${text(label)} ↗</a>`;}).filter(Boolean).join('');
  };
  const detailUrl=p=>/^item-[a-z0-9]+$/i.test(String(p.id||''))?'project.html?id='+encodeURIComponent(p.id):'projects.html';
  const allowedTheme=p=>['peach','violet','sage','blue','cream','gray'].includes(p.theme)?p.theme:'peach';
  function renderArchive(){
    const list=document.getElementById('projects-list');
    const filters=document.getElementById('projects-filters');
    const status=document.getElementById('projects-status');
    const categories=[...new Set(visible.flatMap(p=>tags(p.tags)))];
    filters.innerHTML='<button class="filter-button" type="button" data-category="all" aria-pressed="true">All projects</button>'+categories.map(c=>`<button class="filter-button" type="button" data-category="${esc(c)}" aria-pressed="false">${text(c.replace(/-/g,' '))}</button>`).join('');
    list.innerHTML=visible.map(p=>`<article class="project-card" data-categories="${esc(tags(p.tags).join(' '))}">
      <div class="project-banner ${allowedTheme(p)}" aria-hidden="true">${text(p.banner||p.title)}</div>
      <div class="project-body"><span class="status">${text(p.status||'Project')}</span>
        <h3>${text(p.title)}</h3><p class="multiline">${text(p.summary)}</p>
        <div class="project-meta">${text(p.period)}</div>
        <a class="project-link" href="${esc(detailUrl(p))}" aria-label="Read case study: ${text(p.title)}">Read case study →</a>
      </div></article>`).join('');
    const cards=[...list.querySelectorAll('.project-card')];
    function update(cat){
      let found=0;
      cards.forEach(c=>{const show=cat==='all'||tags(c.dataset.categories).includes(cat);c.hidden=!show;if(show)found++;});
      filters.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.category===cat)));
      status.textContent=`Showing ${found} of ${visible.length} projects${cat==='all'?'.':' tagged '+cat+'.'}`;
    }
    filters.addEventListener('click',e=>{const b=e.target.closest('button[data-category]');if(b)update(b.dataset.category);});
    update('all');
  }
  function renderCase(){
    const target=document.getElementById('case-root');
    const id=new URLSearchParams(location.search).get('id');
    const project=/^item-[a-z0-9]+$/i.test(id||'')?visible.find(p=>p.id===id):undefined;
    if(!project){
      target.innerHTML='<div class="case-empty"><h1>Project not found</h1><p>This project is unavailable or no longer published.</p><a class="button button-primary" href="projects.html">Browse projects →</a></div>';
      document.title='Project Not Found — Than Bannarat';return;
    }
    document.title=`${project.title||'Project'} — Than Bannarat`;
    document.getElementById('breadcrumb-project').textContent=project.title||'Case study';
    const meta=document.querySelector('meta[name="description"]');if(meta)meta.content=String(project.summary||'Project case study').slice(0,160);
    const facts=[['Timeline',project.period],['Duration',project.duration],['Role / team',project.role]].filter(([,v])=>v);
    const images=imagePaths(project.images);
    const captions=String(project.image_captions||'').split(/\r?\n/).map(t=>t.trim());
    const achievements=lines(project.outcomes);
    const skills=String(project.skills||'').split(/[\n,]+/).map(t=>t.trim()).filter(Boolean);
    const topics=tags(project.tags);
    const section=(heading,body)=>body?`<section class="case-block"><h2>${heading}</h2><p class="multiline">${text(body)}</p></section>`:'';
    const bullets=achievements.length?`<section class="case-block"><h2>Key contributions &amp; highlights</h2><ul class="case-bullets">${achievements.map(t=>`<li>${text(t)}</li>`).join('')}</ul></section>`:'';
    const imageSection=images.length?`<section class="case-block" aria-label="Project screenshots"><h2>Project screenshots</h2>
      <div class="case-photo-stage"><img class="case-photo" id="case-photo" src="${esc(images[0])}" alt="${esc(captions[0]||'Project screenshot 1')}" decoding="async"></div>
      <p class="case-photo-caption" id="case-photo-caption">${text(captions[0]||'Project screenshot')}</p>
      ${images.length>1?`<div class="case-photo-controls"><button id="case-photo-prev" type="button">← Previous</button><span id="case-photo-count">1 / ${images.length}</span><button id="case-photo-next" type="button">Next →</button></div>`:''}
    </section>`:'';
    const sidebarLinks=links(project);
    const skillsHtml=skills.length?`<h2>Technologies</h2><div class="skill-list">${skills.map(s=>`<span class="skill">${text(s)}</span>`).join('')}</div>`:'';
    const topicsHtml=topics.length?`<h2>Topics</h2><div class="skill-list">${topics.map(s=>`<span class="skill">${text(s)}</span>`).join('')}</div>`:'';
    target.innerHTML=`<header class="case-hero"><div class="eyebrow">Project / Case study</div><span class="status">${text(project.status||'Project')}</span>
      <h1 class="case-title">${text(project.title)}</h1><p class="lead multiline">${text(project.summary)}</p>
      ${facts.length?`<div class="case-meta">${facts.map(([k,v])=>`<div><small>${k}</small><strong>${text(v)}</strong></div>`).join('')}</div>`:''}
    </header><div class="case-layout"><article class="case-article">
      ${imageSection}${section('Overview',project.details||project.summary)}${section('Problem / challenge',project.challenge)}
      ${section('Approach / solution',project.approach)}${section('Results / impact',project.results)}${bullets}
      <p><a class="project-link" href="projects.html">← Back to all projects</a></p>
    </article><aside class="case-sidebar" aria-label="Project information">
      ${skillsHtml}${topicsHtml}${sidebarLinks?`<h2>Project links</h2><div>${sidebarLinks}</div>`:''}
      <a class="project-link" href="projects.html">Browse all projects →</a>
    </aside></div>`;
    if(images.length>1){
      let n=0;
      const photo=document.getElementById('case-photo');
      const count=document.getElementById('case-photo-count');
      const caption=document.getElementById('case-photo-caption');
      const show=i=>{n=(i+images.length)%images.length;photo.src=images[n];photo.alt=captions[n]||`Project screenshot ${n+1}`;count.textContent=`${n+1} / ${images.length}`;caption.textContent=captions[n]||'Project screenshot';};
      document.getElementById('case-photo-prev').addEventListener('click',()=>show(n-1));
      document.getElementById('case-photo-next').addEventListener('click',()=>show(n+1));
      document.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key)||/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName||''))return;e.preventDefault();show(n+(e.key==='ArrowRight'?1:-1));});
      let touch=null;photo.addEventListener('touchstart',e=>{if(e.touches.length===1)touch=[e.touches[0].clientX,e.touches[0].clientY];},{passive:true});
      photo.addEventListener('touchend',e=>{if(!touch||!e.changedTouches.length)return;const dx=e.changedTouches[0].clientX-touch[0],dy=e.changedTouches[0].clientY-touch[1];touch=null;if(Math.abs(dx)>55&&Math.abs(dx)>1.25*Math.abs(dy))show(n+(dx<0?1:-1));},{passive:true});
    }
  }
  if(document.getElementById('main').dataset.page==='projects')renderArchive();else renderCase();
})();

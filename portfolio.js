/* Static portfolio renderer. All content comes from data/portfolio-data.js,
   generated from local SQLite by the Admin. No visitor editing privileges. */
'use strict';
(() => {
  const data=window.PORTFOLIO_CONTENT?.sections || [];
  const host=document.getElementById('main');
  const nav=document.getElementById('main-nav');
  const modal=document.getElementById('project-modal');
  const modalBody=document.getElementById('project-modal-content');
  const escapeHtml=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const safeUrl=value=>{
    const v=String(value||'').trim();
    if (/^#[a-z][\w-]*$/i.test(v))return v;
    if (/^(?:[a-z\w-]+\.html)(?:\?[^<>"']*)?$/i.test(v))return v;
    try { const u=new URL(v,location.href); if (['https:','http:','mailto:'].includes(u.protocol))return v; } catch(_){}
    return '';
  };
  const link=(url,label,cls='button button-secondary')=>{
    const href=safeUrl(url);if(!href)return '';
    const ext=/^https?:/.test(href), mail=href.startsWith('mailto:');
    return `<a class="${cls}" href="${escapeHtml(href)}" ${ext?'target="_blank" rel="noopener noreferrer"':''}>${escapeHtml(label||'Visit link')} ${ext||mail?'↗':''}</a>`;
  };
  const visible=items=>(items||[]).filter(i=>i.enabled!==false);
  const line=x=>escapeHtml(x||'');
  const tags=x=>String(x||'').toLowerCase().split(/[\s,]+/).filter(Boolean);
  const projects=[];
  function hero(sec){
    const c=visible(sec.items)[0];if(!c)return '';
    const badges=[c.badge1,c.badge2].filter(Boolean).map(t=>`<span class="mini-pill">${line(t)}</span>`).join('');
    const brand=document.querySelector('.brand');if(brand){brand.textContent=c.nav_brand||'than.';}
    return `<header class="shell hero" id="hero"><div><div class="eyebrow">${line(c.eyebrow)}</div><h1>${line(c.headline)} <em>${line(c.highlight)}</em></h1><p class="lead">${line(c.intro)}</p><div class="mini-row">${badges}</div><div class="actions">${link(c.action_url||'#projects',c.action_label,'button button-primary')}${link(c.secondary_url,c.secondary_label)}</div></div><div class="hero-card"><div class="profile-art" role="img" aria-label="Personal initials on a peach gradient">${line(c.profile_initials||'TB ✳')}</div><p class="card-label">${line(c.card_label)}</p><h2>${line(c.card_title)}</h2><p>${line(c.card_body)}</p></div></header>`;
  }
  function intro(sec){return `<div class="section-head"><div class="eyebrow">${line(sec.eyebrow)}</div><h2>${line(sec.title)}</h2>${sec.description?`<p class="section-description">${line(sec.description)}</p>`:''}</div>`;}
  function content(sec){
    let inner='';const items=visible(sec.items);
    if(sec.kind==='about'){
      const para=items.filter(i=>i.type!=='fact');const facts=items.filter(i=>i.type==='fact');
      inner=`<div class="about-grid"><div class="panel">${para.map(i=>`<p class="multiline">${line(i.body)}</p>`).join('')}</div><aside class="quick-facts" aria-label="Quick facts">${facts.map(i=>`<div class="fact"><small>${line(i.title)}</small><strong>${line(i.body)}</strong></div>`).join('')}</aside></div>`;
    }else if(sec.kind==='skills'){
      inner=`<div class="skill-grid">${items.map(i=>`<div class="skill-group"><h3>${line(i.title)}</h3><div class="skill-list">${String(i.skills||'').split(',').map(x=>x.trim()).filter(Boolean).map(t=>`<span class="skill">${line(t)}</span>`).join('')}</div></div>`).join('')}</div>`;
    }else if(sec.kind==='projects'){
      projects.length=0;projects.push(...items);
      const categories=[...new Set(items.flatMap(i=>tags(i.tags)))];
      inner=`<div class="filters" role="group" aria-label="Filter projects"><button class="filter-button" type="button" data-filter="all" aria-pressed="true">All projects</button>${categories.map(t=>`<button class="filter-button" type="button" data-filter="${escapeHtml(t)}" aria-pressed="false">${line(t.replace(/-/g,' '))}</button>`).join('')}</div><p id="filter-summary" class="section-description" role="status" aria-live="polite">Showing all ${items.length} projects.</p><div class="projects-grid">${items.map((i,idx)=>{
        const theme=['violet','sage','blue','cream','peach','gray'].includes(i.theme)?i.theme:'peach';
        return `<article class="project-card" data-project="${idx}" data-category="${escapeHtml(tags(i.tags).join(' '))}"><div class="project-banner ${theme}" aria-hidden="true">${line(i.banner||i.title)}</div><div class="project-body"><span class="status">${line(i.status)}</span><h3>${line(i.title)}</h3><p class="multiline">${line(i.summary)}</p><div class="project-meta">${line(i.period)}</div><button type="button" class="project-open" data-project="${idx}" aria-label="View details for ${line(i.title)}">View project details ↗</button></div></article>`;
      }).join('')}</div>`;
    }else if(sec.kind==='experience'){
      inner=`<div class="timeline">${items.map(i=>`<article class="timeline-item"><small>${line(i.label)}</small><h3>${line(i.title)}</h3><div class="date">${line(i.period)}</div><p class="multiline">${line(i.body)}</p></article>`).join('')}</div>`;
    }else if(sec.kind==='photography'){
      inner=`${items.map(i=>`<div class="panel interests-panel"><div class="camera-icon" aria-hidden="true">📷</div><div class="photography-intro"><h3>${line(i.title)}</h3><p class="multiline">${line(i.body)}</p>${link(i.link||'photography.html',i.link_label||'View photography gallery','button button-primary photography-cta')}</div></div>`).join('')}`;
    }else if(sec.kind==='contact'){
      const introductory=items.filter(x=>x.type==='intro');const links=items.filter(x=>x.type!=='intro');
      inner=`<div class="panel contact-panel"><div>${introductory.map(i=>`<h3>${line(i.title)}</h3><p class="multiline">${line(i.body)}</p>`).join('')}</div><div class="actions">${links.map(i=>link(i.link,i.title)).join('')}</div></div>`;
    }else{
      inner=`<div class="timeline">${items.map(i=>`<article class="timeline-item"><h3>${line(i.title)}</h3><p class="multiline">${line(i.body)}</p>${link(i.link,i.link_label,'project-link')}</article>`).join('')}</div>`;
    }
    return `<section class="shell section" id="${escapeHtml(sec.id)}">${intro(sec)}${inner}</section>`;
  }
  host.innerHTML=data.filter(s=>s.enabled&&s.kind!=='footer').map(s=>s.kind==='hero'?hero(s):content(s)).join('') || '<div class="shell section"><p>No published content yet.</p></div>';
  const names={about:'About',skills:'Skills',projects:'Projects',experience:'Experience',photography:'Photography',contact:'Contact'};
  nav.innerHTML=data.filter(s=>s.enabled&&!['hero','footer'].includes(s.kind)).map(s=>`<a href="#${escapeHtml(s.id)}">${line(names[s.kind]||s.title)}</a>`).join('');
  if(!data.some(s=>s.kind==='photography'&&s.enabled))nav.insertAdjacentHTML('beforeend','<a href="photography.html">Photography ↗</a>');
  const filterButtons=[...host.querySelectorAll('[data-filter]')];
  const cards=[...host.querySelectorAll('.project-card[data-category]')];
  filterButtons.forEach(button=>button.addEventListener('click',()=>{
    const val=button.dataset.filter;let count=0;
    filterButtons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    cards.forEach(card=>{const show=val==='all'||tags(card.dataset.category).includes(val);card.hidden=!show;if(show)count++;});
    const status=document.getElementById('filter-summary');if(status)status.textContent=`Showing ${count} ${count===1?'project':'projects'}${val==='all'?'.':' in '+val+'.'}`;
  }));
  function showProject(i){
    const p=projects[i];if(!p)return;
    modalBody.innerHTML=`<span class="status">${line(p.status)}</span><h2 id="project-dialog-title">${line(p.title)}</h2><p class="project-dialog-sub">${line(p.period)}</p><p class="multiline">${line(p.details||p.summary)}</p>${p.outcomes?`<h3>Highlights</h3><p class="multiline">${line(p.outcomes)}</p>`:''}${p.tags?`<div class="skill-list">${tags(p.tags).map(t=>`<span class="skill">${line(t)}</span>`).join('')}</div>`:''}<div class="actions">${link(p.link,p.link_label||'See project')}</div>`;
    modal.showModal();
  }
  host.addEventListener('click',ev=>{if(ev.target.closest('a'))return;const trigger=ev.target.closest('[data-project]');if(trigger)showProject(Number(trigger.dataset.project));});
  document.getElementById('project-close').addEventListener('click',()=>modal.close());
  modal.addEventListener('click',ev=>{if(ev.target===modal)modal.close();});
  const root=document.documentElement,theme=document.getElementById('theme-toggle');
  let t='light';try{t=localStorage.getItem('portfolio-theme')||'light';}catch(_){}
  function apply(x){root.dataset.theme=x==='dark'?'dark':'light';theme.textContent=x==='dark'?'☀ Light mode':'☾ Dark mode';theme.setAttribute('aria-pressed',String(x==='dark'));}
  apply(t);
  theme.onclick=()=>{const next=root.dataset.theme==='dark'?'light':'dark';apply(next);try{localStorage.setItem('portfolio-theme',next);}catch(_){}};
  const footerSection=data.find(s=>s.kind==='footer');const footer=document.getElementById('site-footer');
  if(footerSection&&footerSection.enabled){
    const item=visible(footerSection.items)[0];
    if(item){document.getElementById('footer-left').textContent=String(item.left||'').replace('{year}',new Date().getFullYear());document.getElementById('footer-right').textContent=item.right||'';}
    else footer.hidden=true;
  }else footer.hidden=true;
})();

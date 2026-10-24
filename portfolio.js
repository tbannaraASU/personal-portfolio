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
    if (/^(?:[a-z\w-]+\/)*[a-z\w-]+\.html(?:\?[^<>"']*)?$/i.test(v))return v;
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
      // The admin's Featured flag wins. Older SQLite content uses a curated, non-AI fallback.
      const flagged=items.filter(i=>i.featured==='Featured');
      const prefer=['Personal Portfolio Website','Student Discussion Application','Studio XE'];
      const fallback=prefer.map(name=>items.find(i=>String(i.title||'').includes(name))).filter(Boolean);
      const featured=(flagged.length?flagged:[...fallback,...items.filter(i=>!fallback.includes(i)&&!String(i.title||'').toLowerCase().includes('personal ai'))]).slice(0,3);
      inner=`<div class="projects-grid featured-grid">${featured.map(i=>{
        const idx=items.indexOf(i);
        const theme=['violet','sage','blue','cream','peach','gray'].includes(i.theme)?i.theme:'peach';
        const detailUrl=/^item-[a-z0-9]+$/i.test(i.id||'')?`project.html?id=${encodeURIComponent(i.id)}`:'projects.html';
        return `<article class="project-card" data-project="${idx}"><div class="project-banner ${theme}" aria-hidden="true">${line(i.banner||i.title)}</div><div class="project-body"><span class="status">${line(i.status)}</span><h3>${line(i.title)}</h3><p class="multiline">${line(i.summary)}</p><div class="project-meta">${line(i.period)}</div><div class="project-card-actions"><button type="button" class="project-open" data-project="${idx}" aria-label="Quick view ${line(i.title)}">Quick view</button><a class="project-link" href="${escapeHtml(detailUrl)}">Read case study →</a></div></div></article>`;
      }).join('')}</div><div class="view-all-projects"><a class="button button-primary" href="projects.html">View all projects →</a><span>${items.length} published projects · Filter by topic on the next page</span></div>`;
    }else if(sec.kind==='experience'){
      inner=`<div class="timeline">${items.map(i=>`<article class="timeline-item"><small>${line(i.label)}</small><h3>${line(i.title)}</h3><div class="date">${line(i.period)}</div><p class="multiline">${line(i.body)}</p></article>`).join('')}</div>`;
    }else if(sec.kind==='photography'){
      // Show just the Admin-selected photographs above a gallery link.
      // No content or Featured Photo selections are changed in Local Admin.
      const featuredPhotos=(window.PORTFOLIO_GALLERY?.featured_photos||[]).slice(0,3);
      const imgUrl=src=>/^photos\/[a-zA-Z0-9_-]+\.(?:jpg|jpeg|png|webp)$/i.test(src||'')||/^photos\/thumbs\/[a-zA-Z0-9_-]+\.webp$/i.test(src||'')?src:'';
      const cards=featuredPhotos.map(p=>{
        const thumb=imgUrl(p.thumb)||imgUrl(p.src),original=imgUrl(p.src);
        if(!thumb||!original)return '';
        return `<a class="featured-photo" href="photography.html" aria-label="Explore photography: ${line(p.title)}"><img src="${escapeHtml(thumb)}" data-full-src="${escapeHtml(original)}" alt="${line(p.alt)}" loading="lazy" decoding="async" width="640" height="640"><span>${line(p.title)}</span></a>`;
      }).filter(Boolean).join('');
      inner=`${cards?`<div class="featured-photo-grid" aria-label="Featured photographs">${cards}</div>`:''}<div class="photography-view-more"><a class="button button-primary" href="photography.html">See More Photos →</a></div>`;
    }else if(sec.kind==='contact'){
      const introductory=items.filter(x=>x.type==='intro');const links=items.filter(x=>x.type!=='intro');
      inner=`<div class="panel contact-panel"><div>${introductory.map(i=>`<h3>${line(i.title)}</h3><p class="multiline">${line(i.body)}</p>`).join('')}</div><div class="actions">${links.map(i=>link(i.link,i.title)).join('')}</div></div>`;
    }else{
      inner=`<div class="timeline">${items.map(i=>`<article class="timeline-item"><h3>${line(i.title)}</h3><p class="multiline">${line(i.body)}</p>${link(i.link,i.link_label,'project-link')}</article>`).join('')}</div>`;
    }
    return `<section class="shell section" id="${escapeHtml(sec.id)}">${intro(sec)}${inner}</section>`;
  }
  host.addEventListener('error',event=>{
    const img=event.target;
    if(img?.tagName==='IMG'&&img.dataset.fullSrc&&img.src!==new URL(img.dataset.fullSrc,location.href).href){
      img.src=img.dataset.fullSrc;
    }
  },true);
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
  const projectImages=value=>String(value||'').split(/\r?\n/).map(v=>v.trim()).filter(v=>/^project-images\/[a-zA-Z0-9_-]+\.(?:webp|jpg|jpeg|png)$/i.test(v)).slice(0,16);
  let currentGallery=[], galleryIndex=0, opener=null;
  function setGalleryImage(index){
    if(!currentGallery.length)return;
    galleryIndex=(index+currentGallery.length)%currentGallery.length;
    const img=modalBody.querySelector('#project-detail-photo');
    const caption=modalBody.querySelector('#project-image-caption');
    const count=modalBody.querySelector('#project-image-count');
    if(img){img.src=currentGallery[galleryIndex].src;img.alt=currentGallery[galleryIndex].caption||`Project screenshot ${galleryIndex+1}`;}
    if(caption)caption.textContent=currentGallery[galleryIndex].caption||'Project image';
    if(count)count.textContent=`${galleryIndex+1} / ${currentGallery.length}`;
    modalBody.querySelectorAll('[data-photo-index]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.photoIndex)===galleryIndex)));
  }
  function showProject(i){
    const p=projects[i];if(!p)return;
    opener=document.activeElement;
    const skills=String(p.skills||'').split(/[,\n]+/).map(x=>x.trim()).filter(Boolean);
    const images=projectImages(p.images);
    const captions=String(p.image_captions||'').split(/\r?\n/).map(x=>x.trim());
    currentGallery=images.map((src,i)=>({src,caption:captions[i]||''})); galleryIndex=0;
    const periodLabel=/(?:20\d{2}|spring|summer|fall|winter|present|month|year)/i.test(String(p.period||''))?'Project timeline':'Project context';
    const metadata=[[periodLabel,p.period],['Duration',p.duration],['Role / team',p.role]].filter(x=>x[1]);
    const metadataHtml=metadata.length?`<div class="project-facts">${metadata.map(([key,value])=>`<div><small>${line(key)}</small><strong>${line(value)}</strong></div>`).join('')}</div>`:'';
    const galleryHtml=currentGallery.length?`<div class="project-media"><div class="project-image-stage"><img id="project-detail-photo" src="${escapeHtml(currentGallery[0].src)}" alt="${escapeHtml(currentGallery[0].caption||'Project screenshot')}" decoding="async"></div><div class="project-image-toolbar"><span id="project-image-caption">${line(currentGallery[0].caption||'Project image')}</span><span id="project-image-count">1 / ${currentGallery.length}</span></div>${currentGallery.length>1?`<div class="project-gallery-controls"><button type="button" id="project-image-prev" aria-label="Previous image">← Previous</button><div class="project-image-dots">${currentGallery.map((x,i)=>`<button type="button" data-photo-index="${i}" aria-pressed="${i===0}" aria-label="Show image ${i+1}">${i+1}</button>`).join('')}</div><button type="button" id="project-image-next" aria-label="Next image">Next →</button></div>`:''}</div>`:'';
    const highlights=String(p.outcomes||'').split(/\r?\n/).map(t=>t.trim().replace(/^[-•*]\s*/, '')).filter(Boolean);
    const highlightsHtml=highlights.length?`<section class="project-block"><h3>Highlights</h3><ul class="project-highlights">${highlights.map(t=>`<li>${line(t)}</li>`).join('')}</ul></section>`:'';
    const skillHtml=skills.length?`<section class="project-block"><h3>Skills & technologies</h3><div class="skill-list">${skills.map(t=>`<span class="skill">${line(t)}</span>`).join('')}</div></section>`:'';
    const urls=[];
    if(p.github_url)urls.push([p.github_url,'View on GitHub']);
    if(p.demo_url)urls.push([p.demo_url,'Live demo']);
    if(p.link&&!urls.some(x=>x[0]===p.link))urls.push([p.link,p.link_label||'Project link']);
    const links=urls.map(([url,label])=>link(url,label,'button button-secondary')).filter(Boolean).join('');
    const caseStudyLink=/^item-[a-z0-9]+$/i.test(p.id||'')?`<a class="button button-primary" href="project.html?id=${encodeURIComponent(p.id)}">Read full case study →</a>`:'';
    modalBody.innerHTML=`<div class="project-header"><span class="status">${line(p.status||'Project')}</span><h2 id="project-dialog-title">${line(p.title)}</h2><p class="project-dialog-intro multiline">${line(p.summary)}</p></div>${galleryHtml}${metadataHtml}<section class="project-block"><h3>About this project</h3><p class="multiline">${line(p.details||p.summary)}</p></section>${highlightsHtml}${skillHtml}${links||caseStudyLink?`<div class="actions project-links">${caseStudyLink}${links}</div>`:''}`;
    modal.showModal();
    const prev=modalBody.querySelector('#project-image-prev'),next=modalBody.querySelector('#project-image-next');
    if(prev)prev.onclick=()=>setGalleryImage(galleryIndex-1);
    if(next)next.onclick=()=>setGalleryImage(galleryIndex+1);
    modalBody.querySelectorAll('[data-photo-index]').forEach(b=>b.onclick=()=>setGalleryImage(Number(b.dataset.photoIndex)));
  }
  // Swipe between screenshots on touch devices, in addition to buttons and arrow keys.
  let touchStart=null;
  modal.addEventListener('touchstart',event=>{
    if(!event.target.closest('.project-image-stage')||event.touches.length!==1)return;
    touchStart={x:event.touches[0].clientX,y:event.touches[0].clientY};
  },{passive:true});
  modal.addEventListener('touchend',event=>{
    if(!touchStart||!event.changedTouches.length){touchStart=null;return;}
    const dx=event.changedTouches[0].clientX-touchStart.x;
    const dy=event.changedTouches[0].clientY-touchStart.y;
    touchStart=null;
    if(currentGallery.length>1&&Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.25){setGalleryImage(galleryIndex+(dx<0?1:-1));}
  },{passive:true});
  modal.addEventListener('keydown',ev=>{
    if(!currentGallery.length||!modal.open||!['ArrowLeft','ArrowRight'].includes(ev.key))return;
    if(/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName||''))return;
    ev.preventDefault();setGalleryImage(galleryIndex+(ev.key==='ArrowRight'?1:-1));
  });
  modal.addEventListener('close',()=>{currentGallery=[];if(opener?.isConnected)opener.focus();});
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

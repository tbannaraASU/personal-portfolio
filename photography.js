'use strict';
/* Same static data works on GitHub Pages; URLs provide a dedicated page per tag or album. */
(() => {
  const $ = s => document.querySelector(s);
  const page = document.body.dataset.page || 'home';
  const gallery = window.PORTFOLIO_GALLERY || {posts:[],albums:[]};
  const posts = (gallery.posts || []).filter(p => p.photos?.length);
  const albums = gallery.albums || [];
  const postMap = new Map(posts.map(p => [p.id,p]));
  const el = (name, cls='', label) => {const n=document.createElement(name);if(cls)n.className=cls;if(label!==undefined)n.textContent=label;return n;};
  const norm = s=>String(s||'').toLocaleLowerCase();
  const tagsFor = p => (p.hashtags || []).length ? p.hashtags : ['Untagged'];
  const tagMap = new Map();
  for (const post of posts) for (const tag of new Set(tagsFor(post))) {
    if (!tagMap.has(tag)) tagMap.set(tag,[]);
    tagMap.get(tag).push(post);
  }
  const tagList = [...tagMap.keys()].sort((a,b)=>tagMap.get(b).length-tagMap.get(a).length || a.localeCompare(b));
  $('#year').textContent = new Date().getFullYear();
  const themeBtn = $('#theme-toggle');
  let pref='light'; try {pref=localStorage.getItem('portfolio-theme')||'light';}catch(_){}
  function setTheme(t){const dark=t==='dark';document.documentElement.dataset.theme=dark?'dark':'light';themeBtn.textContent=dark?'☀ Light mode':'☾ Dark mode';themeBtn.setAttribute('aria-pressed',String(dark));}
  setTheme(pref);themeBtn.addEventListener('click',()=>{const t=document.documentElement.dataset.theme==='dark'?'light':'dark';setTheme(t);try{localStorage.setItem('portfolio-theme',t)}catch(_){}});
  if (location.hostname==='127.0.0.1' && location.port==='8765') {
    const link=el('a','','＋ Manage albums & tags');link.href='/admin';$('header nav').append(link);
  }
  const area = $('#gallery-content');const input=$('#search');const counter=$('#gallery-count');
  const searchMatch = p => norm([p.title,p.caption,...tagsFor(p)].join(' ')).includes(norm(input.value.trim()));
  const cover = p => p?.photos?.[0]?.src || '';
  const tagUrl = t=>`tag.html?tag=${encodeURIComponent(t)}`;
  const albumUrl = a=>`album.html?id=${encodeURIComponent(a.id)}`;
  function categoryCard({title,subtitle,photo,link,pill}) {
    const a=el('a','category-card');a.href=link;
    const image=el('div','category-cover');if(photo){const img=el('img');img.src=thumbSrc(photo);img.loading='lazy';img.decoding='async';img.width=640;img.height=480;img.onerror=()=>{img.onerror=null;img.src=photo};img.alt=`Preview of ${title}`;image.append(img);}image.append(el('span','category-label',pill));
    const copy=el('div','category-copy');copy.append(el('h3','',title),el('p','',subtitle||'Explore this collection'),el('span','go','View collection →'));
    a.append(image,copy);return a;
  }
  function empty(title,msg) {const box=el('div','empty-state');box.append(el('h3','',title),el('p','',msg));return box;}
  function renderCategories(items) {area.replaceChildren();if (!items.length) {area.append(empty('Nothing found','Try another keyword, or create an album in the local admin.'));return;}const grid=el('div','categories-grid');for(const x of items)grid.append(categoryCard(x));area.append(grid);}
  let homeView='tags';
  function setTab(tag, active){const btn=$(tag);if(btn){btn.classList.toggle('active',active);btn.setAttribute('aria-selected',String(active));}}
  function homeRender(){const q=norm(input.value.trim());const isTags=homeView==='tags';
    setTab('#tabs-tags',isTags);setTab('#tabs-albums',!isTags);
    const categories=isTags?tagList.filter(t=>norm(t).includes(q)).map(tag=>({title:tag,subtitle:`${tagMap.get(tag).length} photo sets`,photo:cover(tagMap.get(tag)[0]),link:tagUrl(tag),pill:'Hashtag'})):
      albums.filter(a=>norm(a.title+' '+a.description).includes(q)).map(a=>({title:a.title,subtitle:a.description||`${a.post_ids.length} photo sets`,photo:cover(postMap.get(a.cover_post_id)||postMap.get(a.post_ids[0])),link:albumUrl(a),pill:`${a.post_ids.length} sets`}));
    counter.textContent=`${isTags?tagList.length:albums.length} ${isTags?'hashtags':'albums'}`;renderCategories(categories);
  }
  // Gallery navigation: browse every photo in the currently filtered tag or album.
  // Previous/Next are intentionally NOT restricted to one Instagram post.
  const dialog=$('#photo-dialog');
  let playlist=[], imageIndex=0, opener=null;
  const totalImages = ()=>playlist.length;
  const thumbSrc = src => /^photos\/[a-zA-Z0-9_-]+\.(?:jpg|jpeg|png|webp)$/i.test(src)
    ? 'photos/thumbs/'+src.split('/').pop().replace(/\.[^.]+$/,'.webp') : src;
  const setStatus=(id,value)=>{const node=$(id);if(node)node.textContent=value;};
  function showImage() {
    if(!dialog||!playlist.length)return;
    imageIndex=(imageIndex+playlist.length)%playlist.length;
    const shot=playlist[imageIndex],p=shot.post,im=p.photos[shot.photoIndex];
    const img=$('#viewer-image');
    img.src=im.src; img.alt=im.alt||p.title||'Photograph';
    setStatus('#viewer-title',p.title||'Photo set');
    setStatus('#viewer-caption',p.caption||'');
    setStatus('#viewer-count',`${imageIndex+1} / ${totalImages()} · Image ${shot.photoIndex+1} of ${p.photos.length} in this set`);
    $('#viewer-prev').disabled=$('#viewer-next').disabled=totalImages()<2;
    $('#viewer-post-link').href=p.permalink||'https://www.instagram.com/foto_4th/';
    $('#viewer-post-link').textContent=p.permalink?'View post on Instagram ↗':'View @foto_4th ↗';
    // Preload neighbor to make navigation feel responsive.
    if(playlist.length>1){const near=new Image();const n=playlist[(imageIndex+1)%playlist.length];near.src=n.post.photos[n.photoIndex].src;}
  }
  function openPhoto(p,node){
    opener=node;
    const current=window.__visiblePhotoSets || [p];
    playlist=current.flatMap(post=>post.photos.map((photo,photoIndex)=>({post,photoIndex})));
    imageIndex=Math.max(0,playlist.findIndex(s=>s.post.id===p.id));
    if(!playlist.length)return;
    showImage(); dialog.showModal();
  }
  function navigate(delta){if(!playlist.length)return;imageIndex+=delta;showImage();}
  if(dialog) {
    $('#viewer-close').onclick=()=>dialog.close();
    $('#viewer-prev').onclick=()=>navigate(-1);
    $('#viewer-next').onclick=()=>navigate(1);
    dialog.addEventListener('close',()=>{playlist=[];opener?.focus();});
    dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
    document.addEventListener('keydown',e=>{
      if(!dialog.open||e.target?.matches('input,textarea,select'))return;
      if(e.key==='ArrowRight'||e.key==='ArrowLeft') {e.preventDefault();navigate(e.key==='ArrowRight'?1:-1);}
    });
    let startX=null,startY=null;
    const stage=$('#viewer-image');
    stage.addEventListener('touchstart',e=>{if(e.touches.length!==1)return;startX=e.touches[0].clientX;startY=e.touches[0].clientY;},{passive:true});
    stage.addEventListener('touchend',e=>{
      if(startX===null||!e.changedTouches.length)return;
      const dx=e.changedTouches[0].clientX-startX,dy=e.changedTouches[0].clientY-startY;
      startX=startY=null;
      if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.25)navigate(dx<0?1:-1);
    },{passive:true});
  }
  function photoCard(p) {
    const figure=el('figure','card');const btn=el('button','card-image');btn.type='button';btn.setAttribute('aria-label',`Open ${p.title||'photo set'}`);
    const img=el('img');img.src=thumbSrc(cover(p));img.loading='lazy';img.decoding='async';img.width=640;img.height=480;
    img.alt=p.photos[0].alt||p.title||'Original photo';btn.append(img);
    // Fallback if thumbnails have not been built yet.
    img.onerror=()=>{if(img.dataset.fallback!=='yes'){img.dataset.fallback='yes';img.src=cover(p);}};
    if(p.photos.length>1)btn.append(el('span','carousel-pill',`${p.photos.length} photos`));
    btn.addEventListener('click',()=>openPhoto(p,btn));
    const text=el('figcaption','card-text');text.append(el('h4','',p.title||'Photo set'));
    if(p.caption)text.append(el('p','',p.caption));const tags=el('div','tag-row');for(const t of tagsFor(p).slice(0,8)){const a=el('a','tag',t);a.href=tagUrl(t);tags.append(a)}text.append(tags);
    figure.append(btn,text);return figure;
  }
  function renderPhotoSets(sets){const filtered=sets.filter(searchMatch);counter.textContent=`${filtered.length} photo sets`;
    window.__visiblePhotoSets=filtered;
    area.replaceChildren();if(!filtered.length){area.append(empty('No matching photos','Try another search term or choose a different collection.'));return;}
    const grid=el('div','grid');for(const p of filtered)grid.append(photoCard(p));area.append(grid);
  }
  if(page==='home') {
    $('#tabs-tags').onclick=()=>{homeView='tags';homeRender()};$('#tabs-albums').onclick=()=>{homeView='albums';homeRender()};
    input.addEventListener('input',homeRender);homeRender();return;
  }
  const query=new URLSearchParams(location.search);
  if(page==='tag') {
    const slug=query.get('tag')||'';const sets=tagMap.get(slug);
    if(!sets) {$('#detail-title').textContent='Hashtag not found';area.replaceChildren(empty('No collection for this hashtag','Return to the collections page to choose another tag.'));counter.textContent='0 photo sets';return;}
    document.title=`${slug} | Than Photography`;
    $('#detail-title').textContent=slug;
    $('#detail-description').textContent=`${sets.length} photo sets with ${slug}. Open an image to browse the full set, or switch to related albums.`;
    let mode='sets';const ids=new Set(sets.map(p=>p.id));
    function renderTag(){const isSets=mode==='sets';setTab('#tabs-sets',isSets);setTab('#tabs-albums',!isSets);$('#section-title').textContent=isSets?'Photo sets':'Related albums';
      if(isSets){renderPhotoSets(sets);return;}
      const related=albums.filter(a=>a.post_ids.some(id=>ids.has(id)));
      const q=norm(input.value.trim());const items=related.filter(a=>norm(a.title+' '+a.description).includes(q)).map(a=>({title:a.title,subtitle:a.description||`${a.post_ids.length} photo sets`,photo:cover(postMap.get(a.cover_post_id)||postMap.get(a.post_ids[0])),link:albumUrl(a),pill:`${a.post_ids.filter(id=>ids.has(id)).length} matching`}));
      counter.textContent=`${items.length} related albums`;renderCategories(items);
    }
    $('#tabs-sets').onclick=()=>{mode='sets';renderTag()};$('#tabs-albums').onclick=()=>{mode='albums';renderTag()};input.addEventListener('input',renderTag);renderTag();return;
  }
  if(page==='album') {
    const id=query.get('id')||'';const album=albums.find(a=>a.id===id);
    if(!album){$('#detail-title').textContent='Album not found';counter.textContent='0 photo sets';area.replaceChildren(empty('This album was not found','It may have been renamed or deleted. Return to all collections.'));return;}
    document.title=`${album.title} | Than Photography`;$('#detail-title').textContent=album.title;
    $('#detail-description').textContent=album.description||'A curated photography album.';
    const sets=album.post_ids.map(id=>postMap.get(id)).filter(Boolean);input.addEventListener('input',()=>renderPhotoSets(sets));renderPhotoSets(sets);
  }
})();

/* Responsive navigation shared by Portfolio and Photography pages. */
'use strict';
(()=>{
  const bar=document.querySelector('.topbar .nav-inner');
  if(!bar)return;
  const menu=bar.querySelector(':scope > nav');
  const toggle=document.getElementById('nav-toggle');
  if(!menu||!toggle)return;
  const close=()=>{menu.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');toggle.textContent='☰ Menu';};
  toggle.addEventListener('click',()=>{
    const expanded=toggle.getAttribute('aria-expanded')==='true';
    if(expanded)close();
    else{menu.classList.add('is-open');toggle.setAttribute('aria-expanded','true');toggle.textContent='✕ Close';}
  });
  menu.addEventListener('click',event=>{if(event.target.closest('a'))close();});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&toggle.getAttribute('aria-expanded')==='true'){close();toggle.focus();}});
  window.addEventListener('resize',()=>{if(window.innerWidth>760)close();});
})();

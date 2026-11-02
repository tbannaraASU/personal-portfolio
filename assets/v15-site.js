/* Portfolio V15: progressive enhancement; no dependency on a server or API. */
'use strict';
(() => {
  const base = 'https://tbannaraasu.github.io/personal-portfolio/';
  const name = location.pathname.split('/').pop() || 'index.html';
  const canonicalPaths = new Set(['index.html', 'projects.html', 'photography.html', 'project.html', 'tag.html', 'album.html']);
  if (canonicalPaths.has(name)) {
    const url = new URL(name, base);
    const params = new URLSearchParams(location.search);
    const key = name === 'project.html' || name === 'album.html' ? 'id' : name === 'tag.html' ? 'tag' : '';
    if (key && params.has(key)) url.searchParams.set(key, params.get(key));
    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) { canonical = document.createElement('link'); canonical.rel = 'canonical'; document.head.appendChild(canonical); }
    canonical.href = url.toString();
  }
  // Add async decoding / native lazy loading only to gallery thumbnails, not the active lightbox photo.
  const enhanceImages = parent => {
    if (!parent.querySelectorAll) return;
    parent.querySelectorAll('.featured-photo img, #gallery-content img, .collection-card img').forEach(img => {
      if (!img.hasAttribute('loading')) img.loading = 'lazy';
      if (!img.hasAttribute('decoding')) img.decoding = 'async';
    });
  };
  enhanceImages(document);
  if (window.MutationObserver) {
    const gallery = document.getElementById('gallery-content');
    if (gallery) new MutationObserver(() => enhanceImages(gallery)).observe(gallery, {childList: true, subtree: true});
  }
  // Linkable case studies: copy the actual URL without adding new data to the public page.
  const caseHero = document.querySelector('#case-root .case-hero');
  if (name === 'project.html' && caseHero && new URLSearchParams(location.search).has('id')) {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'v15-copy-link'; button.textContent = 'Copy case study link';
    const status = document.createElement('span');
    status.className = 'v15-share-status'; status.setAttribute('role', 'status');
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(location.href);
        status.textContent = 'Link copied';
      } catch (_) { status.textContent = 'Copy the URL from your browser address bar.'; }
    });
    caseHero.append(button, status);
  }
  // Analytics is opt-in. A blank public config never loads Cloudflare's beacon.
  const token = String(window.PORTFOLIO_V15_CF_TOKEN || '').trim();
  if (/^[a-f0-9]{32}$/i.test(token)) {
    const beacon = document.createElement('script');
    beacon.type = 'module';
    beacon.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    beacon.setAttribute('data-cf-beacon', JSON.stringify({token}));
    document.head.appendChild(beacon);
  }
})();

(() => {
  const root = document.documentElement;
  const body = document.body;

  // Loader
  const loader = document.getElementById('loader');
  const finishLoad = () => { loader?.classList.add('is-done'); body.classList.add('is-loaded'); };
  if (loader) {
    window.addEventListener('load', () => setTimeout(finishLoad, 1500));
    setTimeout(finishLoad, 3500); // fallback
  } else {
    requestAnimationFrame(() => requestAnimationFrame(finishLoad));
  }

  // Header / fixbar / pagetop on scroll
  const header = document.getElementById('header');
  const fixbar = document.getElementById('fixbar');
  const pagetop = document.getElementById('pagetop');
  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 40);
    fixbar?.classList.toggle('is-show', y > window.innerHeight * .6);
    pagetop?.classList.toggle('is-show', y > window.innerHeight);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Drawer
  const toggle = document.getElementById('menuToggle');
  const drawer = document.getElementById('drawer');
  const setMenu = (open) => {
    body.classList.toggle('is-menu-open', open);
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
    drawer.setAttribute('aria-hidden', !open);
    body.style.overflow = open ? 'hidden' : '';
  };
  toggle.addEventListener('click', () => setMenu(!body.classList.contains('is-menu-open')));
  drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));

  // Scroll reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { threshold: .15, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal, .reveal-mask').forEach(el => io.observe(el));

  // Menu tabs
  const tabs = document.querySelectorAll('.menu-tab');
  tabs.forEach(tab => tab.addEventListener('click', () => {
    tabs.forEach(t => t.setAttribute('aria-selected', t === tab));
    document.querySelectorAll('.menu-panel').forEach(p => p.classList.toggle('is-active', p.id === tab.getAttribute('aria-controls')));
  }));

  // FAQ accordion
  document.querySelectorAll('.faq__q').forEach(q => q.addEventListener('click', () => {
    const item = q.parentElement;
    const open = !item.classList.contains('is-open');
    item.classList.toggle('is-open', open);
    q.setAttribute('aria-expanded', open);
  }));

  // Cursor follower
  const cursor = document.getElementById('cursor');
  if (cursor && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    let x = 0, y = 0, cx = 0, cy = 0;
    window.addEventListener('mousemove', e => { x = e.clientX; y = e.clientY; });
    const loop = () => { cx += (x - cx) * .18; cy += (y - cy) * .18; cursor.style.transform = `translate(${cx}px,${cy}px) translate(-50%,-50%)`; requestAnimationFrame(loop); };
    loop();
    document.querySelectorAll('a, button').forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('is-hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-hover'));
    });
  }

  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();

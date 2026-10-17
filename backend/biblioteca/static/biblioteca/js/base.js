(() => {
  const navButton = document.querySelector('.navbar-toggler');
  const navMenu = document.querySelector('#navbarNav');
  if (navButton && navMenu && !window.bootstrap) navButton.addEventListener('click', () => { const open = navMenu.classList.toggle('show'); navButton.setAttribute('aria-expanded', String(open)); });
  if (navMenu) navMenu.querySelectorAll('a.nav-link').forEach(link => link.addEventListener('click', () => {
    if (window.matchMedia('(max-width: 991px)').matches) {
      if (window.bootstrap && window.bootstrap.Collapse) { const instance = window.bootstrap.Collapse.getOrCreateInstance(navMenu, {toggle:false}); instance.hide(); }
      else { navMenu.classList.remove('show'); navButton?.setAttribute('aria-expanded','false'); }
    }
  }));
  document.querySelectorAll('.btn, .nav-link, .calendar-trigger').forEach(el => {
    el.classList.add('ripple-host');
    el.addEventListener('pointerdown', ev => {
      if (ev.pointerType === 'mouse' && ev.button !== 0) return;
      const rect = el.getBoundingClientRect(); const size = Math.max(rect.width, rect.height) * 1.35;
      const ripple = document.createElement('span'); ripple.className = 'ui-ripple';
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = (ev.clientX - rect.left - size/2) + 'px'; ripple.style.top = (ev.clientY - rect.top - size/2) + 'px';
      el.appendChild(ripple); window.setTimeout(() => ripple.remove(), 600);
    });
  });
  const items = document.querySelectorAll('.card, .page-heading, .table-responsive');
  items.forEach(item => item.classList.add('reveal'));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } }), {threshold: 0.04});
    items.forEach(item => observer.observe(item));
  } else items.forEach(item => item.classList.add('is-visible'));
})();
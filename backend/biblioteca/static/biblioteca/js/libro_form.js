
(() => {
  const year = document.getElementById('id_anio');
  const date = document.getElementById('id_anio_calendario');
  const calendarButton = document.getElementById('open-year-calendar');

  if (date) {
    date.setAttribute('aria-label', 'Fecha de publicación');
    date.setAttribute('autocomplete', 'off');
  }

  if (calendarButton && date) {
    calendarButton.addEventListener('click', () => {
      try {
        if (typeof date.showPicker === 'function') {
          date.showPicker();
        } else {
          date.focus();
          date.click();
        }
      } catch (e) {
        date.focus();
        date.click();
      }
    });
  }

  if (date && year) {
    date.addEventListener('change', () => {
      if (date.value) {
        year.value = String(new Date(date.value + 'T12:00:00').getFullYear());
        year.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  }

  function toggle(selectId, wrapId, expected) {
    const sel = document.getElementById(selectId);
    const wrap = document.getElementById(wrapId);
    if (!sel || !wrap) return;
    const input = wrap.querySelector('input');
    function update() {
      const show = sel.value === expected;
      wrap.classList.toggle('d-none', !show);
      if (input) {
        input.required = show;
        if (!show) input.value = '';
      }
    }
    sel.addEventListener('change', update);
    update();
  }

  toggle('id_editorial', 'wrap-editorial_otra', 'Otra');
  toggle('id_categoria', 'wrap-categoria_otra', 'Otros');

  const fileInput = document.getElementById('id_portada');
  const preview = document.getElementById('cover-preview');

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      const file = fileInput.files && fileInput.files[0];
      if (!file) return;
      if (!file.type.startsWith('image/')) return;
      const url = URL.createObjectURL(file);
      if (preview.tagName === 'IMG') {
        preview.src = url;
      } else {
        const img = document.createElement('img');
        img.id = 'cover-preview';
        img.className = 'book-preview';
        img.alt = 'Vista previa de la nueva portada';
        img.src = url;
        preview.replaceWith(img);
      }
    });
  }
})();
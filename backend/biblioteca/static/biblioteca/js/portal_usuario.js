// portal_usuario.js - Biblioteca Córdoba - 2026
(() => {
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');
  const list = document.getElementById('chatMessages');
  const status = document.getElementById('chatStatus');
  const humanButton = document.getElementById('humanButton');

  if (!form) return;

  const token = form.querySelector('[name=csrfmiddlewaretoken]').value;
  let sending = false;
  let handoff = form.dataset.handoff === 'true';

  if (handoff) {
    status.textContent = 'Caso abierto: podés seguir escribiendo y agregar mensajes al mismo caso. El chat automático está pausado hasta que se cierre.';
  }

  function bubble(text, kind) {
    const el = document.createElement('div');
    el.className = 'chat-bubble ' + (kind === 'user' ? 'user-bubble' : 'bot-bubble');
    el.textContent = text;
    list.appendChild(el);
    list.scrollTop = list.scrollHeight;
  }

  async function send(message, human = false) {
    if (sending || (handoff && human)) return;
    sending = true;
    form.querySelector('button[type=submit]').disabled = true;
    humanButton.disabled = true;
    if (message) bubble(message, 'user');
    status.textContent = human ? 'Derivando la consulta…' : 'BiblioBot está pensando…';

    try {
      const r = await fetch(form.dataset.chatUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': token
        },
        body: JSON.stringify({ message: message, human: human })
      });
      const data = await r.json();
      if (!r.ok) throw new Error(data.error || 'No se pudo enviar.');
      bubble(data.reply || 'Listo.', 'bot');
      if (data.human) {
        handoff = true;
        status.textContent = 'Caso abierto: el mensaje quedó asociado al caso. El bibliotecario lo verá y el caso no se cierra automáticamente.';
        humanButton.disabled = true;
      } else {
        status.textContent = '';
        humanButton.disabled = false;
      }
    } catch (e) {
      status.textContent = e.message || 'No se pudo conectar. Probá de nuevo.';
      humanButton.disabled = false;
    } finally {
      sending = false;
      form.querySelector('button[type=submit]').disabled = false;
    }
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const value = input.value.trim();
    if (!value) return;
    input.value = '';
    send(value);
  });

  humanButton.addEventListener('click', () => send('Quiero que me ayude una persona del equipo.', true));
})();
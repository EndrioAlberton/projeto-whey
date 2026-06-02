document.addEventListener('DOMContentLoaded', function () {
  var btn    = document.getElementById('buscar-btn');
  var input  = document.getElementById('buscar-url-input');
  var status = document.getElementById('buscar-status');

  if (!btn || !input || !status) return;

  btn.addEventListener('click', function () {
    var url = input.value.trim();
    if (!url) {
      status.style.color = '#c0392b';
      status.textContent = 'Cole um link antes de buscar.';
      return;
    }

    status.style.color = '#417690';
    status.textContent = 'Buscando...';
    btn.disabled = true;

    var csrf = '';
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    if (match) csrf = match[1];

    var fetchUrl = window.BUSCAR_LINK_URL || '/admin/catalog/produto/buscar-link/';

    fetch(fetchUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
      },
      body: JSON.stringify({ url: url }),
    })
    .then(function (res) { return res.json(); })
    .then(function (data) {
      if (data.erro) {
        status.style.color = '#c0392b';
        status.textContent = '✗ ' + data.erro;
        return;
      }

      if (data.name)      setVal('id_nome',       data.name);
      if (data.price !== null && data.price !== undefined) setVal('id_preco', data.price);
      if (data.image_url) setVal('id_url_imagem',  data.image_url);
      setVal('id_url_produto', url);

      if (data.tamanho_id)    setDropdown('id_tamanho',    data.tamanho_id);
      if (data.marca_id)      setDropdown('id_marca',      data.marca_id);
      if (data.sabor_id)      setDropdown('id_sabor',      data.sabor_id);
      if (data.plataforma_id) setDropdown('id_plataforma', data.plataforma_id);

      status.style.color = '#27ae60';
      status.textContent = '✓ Dados preenchidos! Preencha a proteína por dose e salve.';
    })
    .catch(function () {
      status.style.color = '#c0392b';
      status.textContent = '✗ Erro de conexão.';
    })
    .finally(function () {
      btn.disabled = false;
    });
  });

  function setVal(id, val) {
    var el = document.getElementById(id);
    if (el) el.value = val;
  }

  function setDropdown(id, val) {
    var el = document.getElementById(id);
    if (el) el.value = String(val);
  }
});

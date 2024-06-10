function tooEsile(rowId) {
    var row = document.querySelector('[data-row-id="' + rowId + '"]');
    row.classList.toggle('hidden-row');
  }
  
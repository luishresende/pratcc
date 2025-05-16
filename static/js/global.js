const deleteConfirmationModalEl = document.getElementById('delete-confirmation-modal');
const deleteConfirmationModal = new bootstrap.Modal(deleteConfirmationModalEl);
const deleteConfirmationBtn = document.getElementById('delete-confirmation-btn');
const deleteConfirmationMsg = document.getElementById('delete-confirmation-msg');
const toastMessageElem = document.getElementById("toastMessage");

// Exemplo de uso:
// openDeleteConfirmation('Deseja excluir?', () => deleteItem('id123', true));
function openDeleteConfirmation(msg, action) {
    deleteConfirmationMsg.innerText = msg;
    deleteConfirmationBtn.onclick = action;
    deleteConfirmationModal.show();
}

function validateRequired(input) {
    if (input.value.trim() === '') {
        input.classList.add('is-invalid'); // Ex: Bootstrap estilo
    } else {
        input.classList.remove('is-invalid');
    }
}

function toggleError(className) {
    const targetDiv = document.getElementById(className).value;
    if (!email) {
        targetDiv.style.display = 'block';
    } else {
        targetDiv.style.display = 'none';
    }
}

function addTableRows(tableElement, objects, keys, include_value = false, onClickAction = null, onDblClickAction = null) {
    const tbody = tableElement.tagName === 'TBODY' ? tableElement : tableElement.querySelector('tbody');

    objects.forEach(obj => {
        const idKey = keys[0];
        const existingRow = tbody.querySelector(`tr[data-id="${obj[idKey]}"]`);

        const newRow = document.createElement('tr');
        newRow.dataset.id = obj[idKey];

        const keysToUse = include_value ? keys : keys.slice(1);

        keysToUse.forEach(key => {
            const cell = document.createElement('td');
            cell.textContent = obj[key];
            newRow.appendChild(cell);
        });

        if (onClickAction !== null) {
            newRow.onclick = () => onClickAction(newRow);
        }

        if (onDblClickAction !== null) {
            newRow.ondblclick = () => onDblClickAction();
        }

        // Substitui linha se já existir, senão adiciona
        if (existingRow) {
            tbody.replaceChild(newRow, existingRow);
        } else {
            tbody.appendChild(newRow);
        }
    });
}

function toastMessage(message, isSuccess) {
    let icon = document.createElement('i');
    icon.classList.add('toast-icon');

    // Define o ícone baseado no sucesso ou erro
    if (isSuccess) {
        icon.classList.add('fas', 'fa-check', 'success-icon');
    } else {
        icon.classList.add('fas', 'fa-exclamation', 'error-icon');
    }

    toastMessageElem.innerHTML = '';
    toastMessageElem.appendChild(icon);
    toastMessageElem.appendChild(document.createTextNode(message));

    toastMessageElem.className = "show";
    setTimeout(function () { toastMessageElem.className = toastMessageElem.className.replace("show", ""); }, 3000);
}

function handleFormWithFetch(formSelector, afterSuccess=null) {
    const form = document.querySelector(formSelector);

    if (!form) return;

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        // Converte FormData em objeto (chave/valor)
        const formValues = getFormValuesWithSelectText(form);
        formValues.id = form.getAttribute('data-id') || null;

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                toastMessage(data.message || 'Salvo com sucesso!', true);

                if (afterSuccess != null){
                    if (data.id)
                        formValues.id = data.id;
                    // Passa os dados digitados para afterSuccess
                    afterSuccess(formValues);
                }

                form.reset();
            } else {
                handleApiErrors(data);
            }
        })
        .catch((e) => {
            toastMessage('Erro ao enviar o formulário.', false);
        });
    });
}

function getFormValuesWithSelectText(form) {
  const formData = new FormData(form);
  const values = Object.fromEntries(formData.entries());

  // Para cada <select>, adiciona também o texto da opção selecionada
  form.querySelectorAll('select').forEach(select => {
    const selectedOption = select.options[select.selectedIndex];
    if (selectedOption) {
      values[`${select.name}_text`] = selectedOption.textContent;
    }
  });

  return values;
}

function clearForm(formSelector) {
    const form = document.querySelector(formSelector);
    const inputs = form.querySelectorAll('input, select, textarea');  // Seleciona todos os inputs, selects e textareas

    inputs.forEach(input => {
        // Pula o csrfmiddlewaretoken
        if (input.name === 'csrfmiddlewaretoken') {
            return;
        }

        if (input.type === 'checkbox' || input.type === 'radio') {
            input.checked = false;  // Limpa os checkboxes e radios
        } else {
            input.value = '';  // Limpa os outros tipos de input
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function getCsrfTokenFromForm(form) {
    const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfInput ? csrfInput.value : null;
}

function openModal(modal, modalTitle, title, saveBtn, deleteBtn, isEdit, deleteMsg=null, deleteAction=null) {
    if (deleteMsg == null && deleteAction == null){
        deleteBtn.disabled = true;
    } else {
        deleteBtn.onclick = () => openDeleteConfirmation(deleteMsg, deleteAction);
    }

    if (isEdit) {
        modalTitle.innerText = title;
        saveBtn.innerText = 'Editar';
        deleteBtn.disabled = false;
    } else {
        modalTitle.innerText = title;
        saveBtn.innerText = 'Salvar';
    }
    modal.show(); // Chama o método show() no objeto Modal
}

function handleApiErrors(data) {
    if (data.errors) {
        for (const [field, messages] of Object.entries(data.errors)) {
            const errorList = Array.isArray(messages) ? messages : [messages];
            const errorText = errorList.join(', ');
            toastMessage(`${field}: ${errorText}`, false);
        }
    } else if (data.message) {
        toastMessage(data.message, false);
    }
}

function injectSelectValue(form, selectId, value, text) {
  const sel = form.querySelector(`#${selectId}`);
  if (!sel) {
    console.warn(`Select com id="${selectId}" não encontrado.`);
    return;
  }

  // Tenta encontrar option existente
  let opt = sel.querySelector(`option[value="${value}"]`);
  if (!opt) {
    // Se não existir, cria uma nova no final
    opt = document.createElement('option');
    opt.value = value;
    opt.textContent = text;
    sel.appendChild(opt);
  }

  // Desmarca todas e marca a desejada
  Array.from(sel.options).forEach(o => o.selected = (o.value === String(value)));
  opt.selected = true;
}

function unlockIcon(iconElem) {
    iconElem.classList.remove('fa-lock');
    iconElem.classList.add('fa-chevron-down');
}

function lockIcon(iconElem){
    iconElem.classList.remove('fa-chevron-down');
    iconElem.classList.add('fa-lock');
}

function searchTable(tableId, searchInputId) {
  const input = document.getElementById(searchInputId);
  const filter = input.value.toLowerCase();
  const table = document.getElementById(tableId);
  const tr = table.getElementsByTagName('tr');

  for (let i = 1; i < tr.length; i++) { // começa do 1 para pular o cabeçalho
    const tds = tr[i].getElementsByTagName('td');
    let found = false;

    for (let j = 0; j < tds.length; j++) {
      if (tds[j].textContent.toLowerCase().indexOf(filter) > -1) {
        found = true;
        break;
      }
    }

    tr[i].style.display = found ? '' : 'none';
  }
}
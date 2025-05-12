const deleteConfirmationModalEl = document.getElementById('delete-confirmation-modal');
const deleteConfirmationModal = new bootstrap.Modal(deleteConfirmationModalEl);
const deleteConfirmationBtn = document.getElementById('delete-confirmation-btn');
const deleteConfirmationMsg = document.getElementById('delete-confirmation-msg');

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

function addTableRows(tableElement, objects, onClickAction=null, onDblClickAction=null) {
    const tbody = tableElement.tagName === 'TBODY' ? tableElement : tableElement.querySelector('tbody');

    objects.forEach(obj => {
        const row = document.createElement('tr');

        const keys = Object.keys(obj);
        if (keys.length === 0) return; // ignora objetos vazios

        // Assume que a primeira chave é o ID
        const idKey = keys[0];
        row.dataset.id = obj[idKey];

        // Cria células para as demais chaves (exclui a primeira)
        keys.slice(1).forEach(key => {
            const cell = document.createElement('td');
            cell.textContent = obj[key];
            row.appendChild(cell);
        });

        if (onClickAction !== null)
            row.onclick = () => onClickAction(row);

        if (onDblClickAction !== null)
            row.ondblclick = () => onDblClickAction();

        tbody.appendChild(row);
    });
}
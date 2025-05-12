const registerPersonModalEl = document.getElementById('register-person-modal');
const registerPersonModal = new bootstrap.Modal(registerPersonModalEl);
const collapseEl = document.getElementById('teacher-universities-collapse');
const bsCollapse = new bootstrap.Collapse(collapseEl, { toggle: false });
const deletePersonBtn = document.getElementById('delete-person-btn');
const savePersonBtn = document.getElementById('save-person-btn');
const teacherAfilliationsTable = document.getElementById('teacher-affiliations-table');

function handleRadioChange(teacherCourses=null) {
  const isTeacher = document.getElementById('teacher-radio').checked;
  isTeacher ? bsCollapse.show() : bsCollapse.hide();
  registerPersonModal.show();
}

function selectRadioAndHandle(radioId, permanent, deleteMsg=null, deleteAction=null) {
  const radio = document.getElementById(radioId);

  if (!radio) return;

  // Setando mensagem e função de deletar
  if (deleteMsg == null && deleteAction == null){
    deletePersonBtn.disabled = true;
  } else {
    deletePersonBtn.onclick = () => openDeleteConfirmation(deleteMsg, deleteAction);
  }

  radio.checked = true;
  radio.dispatchEvent(new Event('change')); // Garante que handleRadioChange seja executada

  let registerPersonModalTitle = document.getElementById('register-person-modal-title');

  if (permanent) {
    savePersonBtn.innerText = 'Editar';
    registerPersonModalTitle.innerText = 'Editar pessoa';
    deletePersonBtn.disabled = false;
  } else {
    registerPersonModalTitle.innerText = 'Cadastrar pessoa';
    registerPersonModalEl.querySelectorAll('input, select').forEach(el => {
      if (el.tagName === 'SELECT') {
        el.selectedIndex = 0;
      } else {
        el.value = '';
      }
    });
    savePersonBtn.innerText = 'Salvar';
    savePersonBtn.onclick = () => {
      // TODO: Adicionar regra para depois de salvar
      savePersonBtn.innerText = 'Editar';
      deletePersonBtn.disabled = false;
    }
    registerPersonModalTitle.innerText = 'Cadastrar pessoa';
  }

  // Sempre atualiza os outros radios do mesmo grupo
  document.querySelectorAll(`input[name="${radio.name}"]`).forEach(r => {
    if (r !== radio) {
      r.disabled = permanent;
    }
  });
}

document.querySelectorAll('input[name="tipo"]').forEach(radio => {
  radio.addEventListener('change', handleRadioChange);
});

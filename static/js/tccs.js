const tccModalEl = document.getElementById('tcc-modal');
const tccModal = new bootstrap.Modal(document.getElementById('tcc-modal')); // Cria o objeto Modal
const tccTable = document.getElementById('tccs-table')
const tccModalTitle = document.getElementById('tcc-modal-title');
const registerTccBtn = document.getElementById('register-tcc-btn');
const deleteTccBtn = document.getElementById('delete-tcc-btn');
const saveTccBtn = document.getElementById('save-tcc-btn');

const bancaCollapse = document.getElementById('banca-collapse');
const bancaIcon = document.getElementById('banca-icon');

const documentsCollapse = document.getElementById('documents-collapse');
const documentsIcon = document.getElementById('documents-icon');

const bancaBsCollapse = bootstrap.Collapse.getOrCreateInstance(bancaCollapse);
const documentsBsCollapse = bootstrap.Collapse.getOrCreateInstance(documentsCollapse);

const registerStudentBtn = document.getElementById('register-tcc-btn');

const deleteMsgTcc = 'Você realmente deseja excluir este TCC?';

let podeAbrir = false;

documentsCollapse.addEventListener('show.bs.collapse', function (event) {
  if (!podeAbrir) {
    event.preventDefault();
  }
});

function loadTccsTable() {
  tccs = [
    {
      id: 1,
      name: "Kauan",
      title: "RegL: aisdhaihsda",
      supervisor: "Thiago",
      fase: 1
    },
    {
      id: 2,
      name: "Iuri",
      title: "NeRF: Comparação de Técnicas",
      supervisor: "Thiago",
      fase: 1
    },
    {
      id: 3,
      name: "Luis",
      title: "Back-end para NeRFs - Computação Distribuída",
      supervisor: "Thiago",
      fase: 1
    },
    {
      id: 4,
      name: "Guilherme",
      title: "Segmentção de placas",
      supervisor: "Thiago",
      fase: 1
    },
  ]

  addTableRows(tccTable, 
    tccs, 
    () => openTccModal(
      true, 
      deleteMsgTcc,
      null, 
      () => console.log('TCC apagado.'))
    );

}

loadTccsTable();

function openTccModal(edit, deleteMsg=null, deleteAction=null) {
  if (deleteMsg == null && deleteAction == null){
    deleteTccBtn.disabled = true;
  } else {
    deleteTccBtn.onclick = () => openDeleteConfirmation(deleteMsg, deleteAction);
  }

  if (edit) {
    tccModalTitle.innerText = 'Editar TCC'
    saveTccBtn.innerText = 'Editar';
    deleteTccBtn.disabled = false;
  } else {
    tccModalTitle.innerText = 'Cadastrar TCC'
    saveTccBtn.innerText = 'Salvar';
  }
  tccModal.show(); // Chama o método show() no objeto Modal
}

registerTccBtn.onclick = () => openTccModal(false);

documentsCollapse.addEventListener('shown.bs.collapse', () => {
  documentsIcon.classList.add('rotated');
});

documentsCollapse.addEventListener('hidden.bs.collapse', () => {
  documentsIcon.classList.remove('rotated');
});

bancaCollapse.addEventListener('shown.bs.collapse', () => {
  bancaIcon.classList.add('rotated');
});

bancaCollapse.addEventListener('hidden.bs.collapse', () => {
  bancaIcon.classList.remove('rotated');
});

tccModalEl.addEventListener('show.bs.modal', () => {
  // Limpar campos de input
  tccModalEl.querySelectorAll('input').forEach(el => el.value = '');

  // Remover classes de validação
  tccModalEl.querySelectorAll('.is-valid, .is-invalid').forEach(el =>
    el.classList.remove('is-valid', 'is-invalid')
  );

  // Resetar selects, se houver
  tccModalEl.querySelectorAll('select').forEach(select => select.selectedIndex = 0);

  bancaBsCollapse.hide();
  documentsBsCollapse.hide();

  // Resetar elementos customizados, mensagens, etc., se necessário
});

function onBlur(validateFunc) {
  const requiredInputs = document.getElementsByClassName('required-input');
  Array.from(requiredInputs).forEach(input => {
    input.addEventListener('blur', () => {
      validateFunc(input);
    });
  });
}



onBlur(validateRequired);




// function validateSelect(select) {
//     const isValid = select.value !== "";
//     select.classList.toggle('is-valid', isValid);
//     select.classList.toggle('is-invalid', !isValid);
// }

// const selects = document.querySelectorAll('select.required-input');

// selects.forEach(select => {
//     select.addEventListener('blur', () => validateSelect(select));
// });

// Example starter JavaScript for disabling form submissions if there are invalid fields

// (function () {
//     'use strict'

//     // Fetch all the forms we want to apply custom Bootstrap validation styles to
//     var forms = document.querySelectorAll('.needs-validation')

//     // Loop over them and prevent submission
//     Array.prototype.slice.call(forms)
//       .forEach(function (form) {
//         form.addEventListener('submit', function (event) {
//           if (!form.checkValidity()) {
//             event.preventDefault()
//             event.stopPropagation()
//           }

//           form.classList.add('was-validated')
//         }, false)
//       })
//   })()

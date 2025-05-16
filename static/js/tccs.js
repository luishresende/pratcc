const tccModalEl = document.getElementById('tcc-modal');
const tccModal = new bootstrap.Modal(document.getElementById('tcc-modal')); // Cria o objeto Modal
const tccTable = document.getElementById('tccs-table')
const tccModalTitle = document.getElementById('tcc-modal-title');
const registerTccBtn = document.getElementById('register-tcc-btn');
const deleteTccBtn = document.getElementById('delete-tcc-btn');
const saveTccBtn = document.getElementById('save-tcc-btn');
const tccWorkForm = document.getElementById('tcc-work-form');
const tccComitteForm = document.getElementById('tcc-committe-form');
const tccDocumentsForm = document.getElementById('tcc-documents-form');
const bancaCollapse = document.getElementById('banca-collapse');
const bancaIcon = document.getElementById('banca-icon');
const defenseBtn = document.getElementById('defense-btn');
const yearInput = document.getElementById('id_year');
const semesterSelect = document.getElementById('id_semester');
let tccWorkState = null;
let tccCommitteState = null;
let tccDocumentsState = null;

const documentsCollapse = document.getElementById('documents-collapse');
const documentsIcon = document.getElementById('documents-icon');

const bancaBsCollapse = bootstrap.Collapse.getOrCreateInstance(bancaCollapse);
const documentsBsCollapse = bootstrap.Collapse.getOrCreateInstance(documentsCollapse);
let selectedTccRow = null;

const deleteMsgTcc = 'Você realmente deseja excluir este TCC?';

let documentCanOpen = false;
let bancaCanOpen = false;

const title = tccWorkForm.querySelector('input[name="title"]');
const year = tccWorkForm.querySelector('input[name="year"]');
const semester = tccWorkForm.querySelector('select[name="semester"]');
const fase = tccWorkForm.querySelector('select[name="tcc_num"]');
const student = tccWorkForm.querySelector('select[name="student_ra"]');
const advisor = tccWorkForm.querySelector('select[name="teacher_advisor_ma"]');
const cosupervisor = tccWorkForm.querySelector('select[name="teacher_cosupervisor_ma"]');

const full_member_1 = tccComitteForm.querySelector('select[name="full_member_1_ma"]');
const full_member_2 = tccComitteForm.querySelector('select[name="full_member_2_ma"]');
const alternate_member = tccComitteForm.querySelector('select[name="alternate_member_ma"]');
const defense_location = tccComitteForm.querySelector('input[name="defense_location"]');
const defense_date = tccComitteForm.querySelector('input[name="defense_date"]');
const autorization_letter = tccComitteForm.querySelector('input[name="authorization_letter_submitted"]');

const fm1_evaluation_form = tccDocumentsForm.querySelector('input[name="fm1_evaluation_form"]');
const fm2_evaluation_form = tccDocumentsForm.querySelector('input[name="fm2_evaluation_form"]');
const fm3_evaluation_form = tccDocumentsForm.querySelector('input[name="fm3_evaluation_form"]');
const end_monograph = tccDocumentsForm.querySelector('input[name="end_monograph"]');
const end_monograph_in_lib = tccDocumentsForm.querySelector('input[name="end_monograph_in_lib"]');
const approvation_term = tccDocumentsForm.querySelector('input[name="approvation_term"]');
const recorded_data = tccDocumentsForm.querySelector('input[name="recorded_data"]');

documentsCollapse.addEventListener('show.bs.collapse', function (event) {
  if (!documentCanOpen) {
    event.preventDefault();
  }
});

bancaCollapse.addEventListener('show.bs.collapse', function (event) {
    if (!bancaCanOpen) {
        event.preventDefault();
    }
})

function loadTccsTable() {
    const tbody = tccTable.querySelector('tbody');

    // Remove todas as linhas do tbody
    tbody.innerHTML = '';

    fetch(`/tccs/get/`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableRows(
            tccTable,
            data.data,
            ['tcc_id', 'student_name', 'title', 'advisor_name', 'tcc_num'],
            false,
            (row) => selectedTccController(row),
            () => openEditTccModal()
        )
    })
    .catch(error => {
        console.error('Erro ao carregar campus:', error);
    });
}

loadTccsTable();

function openEditTccModal() {
  fetch('/tccs/get?tcc_id=' + selectedTccRow.dataset.id)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
            clearForm("#tcc-work-form");
            clearForm("#tcc-committe-form");

            let tcc_work_data = data.data.tcc_work;
            title.value = tcc_work_data.title;
            year.value = tcc_work_data.year;
            semester.value = tcc_work_data.semester;
            fase.value = tcc_work_data.tcc_num;

            year.disabled = true;
            semester.disabled = true;
            fase.disabled = true;

            student.value = tcc_work_data.student_ra;
            student.disabled = true;

            let supervisor_data = data.data.advisor;
            advisor.value = supervisor_data.ma;
            advisor.disabled = true;

            let cosupervisor_data = data.data.cosupervisor;
            cosupervisor.value = cosupervisor_data.ma || '';
            cosupervisor.disabled = true;

            let removeTccUrl = '/tccs/delete/' + tcc_work_data.tcc_id + '/';
            tccWorkForm.action = '/tccs/tcc_work/edit/' + tcc_work_data.tcc_id + '/';
            tccWorkForm.dataset.id = tcc_work_data.tcc_id;
            let tccw_hidden = tccComitteForm.querySelector('#id_tccw');
            tccw_hidden.value = tcc_work_data.tcc_id;

            let documents_data = data.data.documents;

            let committe_data = data.data.committe;

            bancaCanOpen = true;
            bancaBsCollapse.show();
            unlockIcon(bancaIcon);

            autorization_letter.checked = false;
            autorization_letter.disabled = false;
            full_member_1.disabled = false;
            full_member_2.disabled = false;
            alternate_member.disabled = false;
            defense_location.disabled = false;
            defense_date.disabled = false;
            lockIcon(documentsIcon);
            documentCanOpen = false;

            if (committe_data) {
                tccComitteForm.action = '/tccs/tcc_committe/edit/' + tcc_work_data.tcc_id + '/';

                full_member_1.value = committe_data.full_member_1.ma;
                full_member_2.value = committe_data.full_member_2.ma;
                alternate_member.value = committe_data.alternate_member.ma;
                defense_location.value = committe_data.defense_location;
                defense_date.value = committe_data.defense_date;

                if (committe_data.autorization_letter == true) {
                    autorization_letter.checked = true;
                    autorization_letter.disabled = true;
                    full_member_1.disabled = true;
                    full_member_2.disabled = true;
                    alternate_member.disabled = true;
                    defense_location.disabled = true;
                    defense_date.disabled = true;

                    if (documents_data != null){
                        defenseBtn.disabled = true;
                        unlockIcon(documentsIcon);
                        documentsBsCollapse.show();
                        documentCanOpen = true;
                        tccDocumentsForm.action = "/tccs/tcc_documents/edit/" + tcc_work_data.tcc_id + '/';
                        tccDocumentsState = [
                            {
                                elem: fm1_evaluation_form,
                                value: documents_data.fm1_evaluation_form,
                            },
                            {
                                elem: fm2_evaluation_form,
                                value: documents_data.fm2_evaluation_form,
                            },
                            {
                                elem: fm3_evaluation_form,
                                value: documents_data.fm3_evaluation_form,
                            },
                            {
                                elem: end_monograph,
                                value: documents_data.end_monograph,
                            },
                            {
                                elem: end_monograph_in_lib,
                                value: documents_data.end_monograph_in_lib,
                            },
                            {
                                elem: approvation_term,
                                value: documents_data.approvation_term,
                            },
                            {
                                elem: recorded_data,
                                value: documents_data.recorded_data,
                            },
                        ]

                    } else {
                        defenseBtn.disabled = true;
                        defenseBtn.onclick = () => defenseRegister(tcc_work_data.tcc_id);
                        tccDocumentsState = null;
                        lockIcon(documentsIcon);
                        documentsBsCollapse.hide();
                    }
                }

                if (tccDocumentsState != null) {
                    tccDocumentsState.forEach(item => {
                            item.elem.checked = item.value;
                            item.elem.disabled = item.value;
                        })
                }else {
                    defenseBtn.disabled = false;
                        defenseBtn.onclick = () => defenseRegister(tcc_work_data.tcc_id);
                        tccDocumentsState = null;
                        lockIcon(documentsIcon);
                        documentsBsCollapse.hide();
                }
                tccCommitteState = [
                    {
                        elem: full_member_1,
                        originalValue: full_member_1.value
                    },
                    {
                        elem: full_member_2,
                        originalValue: full_member_2.value
                    },
                    {
                        elem: alternate_member,
                        originalValue: alternate_member.value
                    },
                    {
                        elem: defense_location,
                        originalValue: defense_location.value
                    },
                    {
                        elem: defense_date,
                        originalValue: defense_date.value
                    },
                    {
                        elem: autorization_letter,
                        originalValue: autorization_letter.checked
                    }
                ]


                bancaBsCollapse.show();

            } else {
                tccComitteForm.action = '/tccs/tcc_committe/register/';
                bancaBsCollapse.hide();
                documentsBsCollapse.hide();
            }



            tccWorkState = [
                {
                    elem: title,
                    originalValue: title.value
                }
            ];

            if (tcc_work_data.tcc_num == 2)
                approvation_term.disabled = true;
            else
                end_monograph_in_lib.disabled = true;

            openModal(
                tccModal,
                tccModalTitle,
                'Editar TCC',
                saveTccBtn,
                deleteTccBtn,
                true,
                'Você tem certeza que deseja excluir este registro?',
                () => {
                    fetch(removeTccUrl, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                toastMessage(data.message || 'Salvo com sucesso!', true);
                                tccWorkForm.reset();
                                selectedTccRow.remove();
                                tccModal.hide();
                                selectedTccRow = null;
                            } else {
                                handleApiErrors(data);
                            }
                            deleteConfirmationModal.hide();
                        })
                }
            )
        } else {
          console.warn(data.message);
        }
      });
}

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


function onBlur(validateFunc) {
  const requiredInputs = document.getElementsByClassName('required-input');
  Array.from(requiredInputs).forEach(input => {
    input.addEventListener('blur', () => {
      validateFunc(input);
    });
  });
}



//onBlur(validateRequired);

document.getElementById('save-tcc-btn').addEventListener('click', async () => {
  const forms = [
    { form: document.getElementById('tcc-work-form'), state: tccWorkState , active: true},
    { form: document.getElementById('tcc-committe-form'), state: tccCommitteState, active: bancaCanOpen },
    { form: document.getElementById('tcc-documents-form'), state: tccDocumentsState, active: documentCanOpen },
  ];

  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  for (const { form, state, active } of forms) {
    if (!form) continue;

    if (!form.checkValidity()) {
      form.reportValidity();
      continue;
    }

    if (!active)
        continue;

    let changed = true;

    if (state) {
      changed = state.some(field => {
        const elem = field.elem;
        return elem.type === 'checkbox'
          ? elem.checked !== field.originalValue
          : elem.value !== field.originalValue;
      });
    }

    if (changed) {
      form.requestSubmit();
      await sleep(500); // espera meio segundo antes de continuar
    }
  }
});

function selectedTccController(newRow) {
    // Remove 'table-active' de todas as linhas da tabela de cursos
    tccTable.querySelectorAll('tbody tr').forEach(row => {
        row.classList.remove('table-active');
    });

    selectedTccRow = newRow;
    selectedTccRow.classList.add('table-active');
}

registerTccBtn.addEventListener('click', () => {
    tccWorkState = null;
    tccCommitteState = null;
    bancaBsCollapse.hide();
    documentsBsCollapse.hide();
    documentCanOpen = false;
    bancaCanOpen = false;
    lockIcon(documentsIcon);
    lockIcon(bancaIcon);
    tccWorkForm.action = '/tccs/tcc_work/register/';
    tccComitteForm.action = '/tccs/tcc_committe/register/';
    clearForm("#tcc-work-form");
    clearForm("#tcc-committe-form");

    year.disabled = false;
    semester.disabled = false;
    fase.disabled = false;
    student.disabled = false;
    advisor.disabled = false;
    cosupervisor.disabled = false;
    defenseBtn.disabled = true;

    full_member_1.disabled = false;
    full_member_2.disabled = false;
    alternate_member.disabled = false;
    defense_location.disabled = false;
    defense_date.disabled = false;
    autorization_letter.disabled = false;

    if (yearInput && !yearInput.value) {
        yearInput.value = new Date().getFullYear();
    }

    if (semesterSelect && !semesterSelect.value) {
        const currentMonth = new Date().getMonth() + 1; // janeiro = 0
        semesterSelect.value = currentMonth <= 6 ? '1' : '2';
    }

    tccWorkForm.dataset.id = '';
    openModal(
        tccModal,
        tccModalTitle,
        'Cadastrar TCC',
        saveTccBtn,
        deleteTccBtn,
        false
    )
});

function defenseRegister(tcc_id) {
    fetch('tcc_documents/register/' + tcc_id + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // necessário se estiver usando Django com CSRF
        },
        body: JSON.stringify({})  // corpo vazio, se não precisa enviar dados
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            toastMessage(data.message, true);
            defenseBtn.disabled = true;
            unlockIcon(documentsIcon);
            documentsBsCollapse.show();
            documentCanOpen = true;
            tccModal.hide();
            tccDocumentsState = [
                {
                    elem: fm1_evaluation_form,
                    value: false,
                },
                {
                    elem: fm2_evaluation_form,
                    value: false,
                },
                {
                    elem: fm3_evaluation_form,
                    value: false,
                },
                {
                    elem: end_monograph,
                    value: false,
                },
                {
                    elem: end_monograph_in_lib,
                    value: false,
                },
                {
                    elem: approvation_term,
                    value: false,
                },
                {
                    elem: recorded_data,
                    value: false,
                },
            ]
        } else {
            handleApiErrors(data);
        }
    })
    .catch(error => {
        console.error('Erro ao registrar defesa:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    handleFormWithFetch('#tcc-work-form', (obj) => {
            let tccw_hidden = tccComitteForm.querySelector('#id_tccw');
            tccw_hidden.value = obj.id;
            addTableRows(
            tccTable,
            [obj],
            ['id', 'student_ra_text', 'title', 'teacher_advisor_ma_text', 'tcc_num_text'],
            false,
            (row) => selectedTccController(row),
                () => openEditTccModal()
        );
            tccModal.hide();
    });

    handleFormWithFetch('#tcc-committe-form', () => {
        tccModal.hide();
    });

    handleFormWithFetch('#tcc-documents-form', () => {
        tccModal.hide();
    });
});

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

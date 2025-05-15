const registerStudentBtn = document.getElementById(`register-${personTypeEnglish}-btn`);
const studentTable = document.getElementById(`${personTypeEnglish}-table`);

const studentsModal = document.getElementById('register-student-modal');
const studentBsModal = new bootstrap.Modal(studentsModal);
const studentRemoveBtn = document.getElementById('delete-student-btn');
const studentSaveBtn = document.getElementById('save-student-btn');
const studentModalTitle = document.getElementById('register-student-modal-title');
const studentForm = document.getElementById('student-form');
let selectedStudentRow = null;

function loadStudentsTable() {
    const tbody = studentTable.querySelector('tbody');

    // Remove todas as linhas do tbody
    tbody.innerHTML = '';

    fetch(getUrl, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableRows(
            studentTable,
            data.data,
            editKeys,
            true,
            (row) => selectedStudentController(row),
            () => openEditStudentModal()
        )
    });
}
loadStudentsTable();

registerStudentBtn.addEventListener('click', () => {
  clearForm('#student-form');
  studentForm.action = registerUrl;
  const inputRa = document.querySelector(`input[name="${idName}"]`);
  inputRa.readOnly = false;
  openModal(
      studentBsModal,
      studentModalTitle,
      `Cadastrar ${personType}`,
      studentSaveBtn,
      studentRemoveBtn,
      false
  );
});

function openEditStudentModal() {
    fetch(getByIdUrl + selectedStudentRow.dataset.id)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
            const form = document.querySelector('#student-form');
            const inputRa = document.querySelector(`input[name="${idName}"]`);
            const inputName = document.querySelector('input[name="name"]');

            let ra = data.data.person.ra;

            inputRa.value = data.data.person.ra;
            inputRa.readOnly = true;
            let removeStudentUrl = removeUrl + ra + '/';
            form.action = editUrl + ra + '/';
            form.dataset.id = ra;
            inputName.value = data.data.person.name;

            injectSelectValue(studentForm, 'university_select',  data.data.university.acronym, data.data.university.name);
            injectSelectValue(studentForm, 'campus_select', data.data.campus.id, data.data.campus.name);
            injectSelectValue(studentForm, 'course_select', data.data.course.id, data.data.course.name);

            openModal(
                studentBsModal,
                studentModalTitle,
                `Editar ${personType}`,
                studentSaveBtn,
                studentRemoveBtn,
                true,
                'Você tem certeza que deseja excluir este registro?',
                () => {
                    fetch(removeStudentUrl)
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                toastMessage(data.message || 'Salvo com sucesso!', true);
                                form.reset();
                                selectedStudentRow.remove();
                                studentBsModal.hide();
                                selectedStudentRow = null;
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

function selectedStudentController(newRow) {
    // Remove 'table-active' de todas as linhas da tabela de campi
    studentTable.querySelectorAll('tbody tr').forEach(row => {
        row.classList.remove('table-active');
    });

    selectedStudentRow = newRow;
    selectedStudentRow.classList.add('table-active');
}

document.addEventListener('DOMContentLoaded', function () {
    handleFormWithFetch('#student-form', (obj) => {
            registerZeroItens.forEach(key => {
              obj[key] = 0;
            });
            addTableRows(
            studentTable,
            [obj],
            registerKeys,
            true,
            (row) => selectedStudentController(row),
                () => openEditStudentModal()
        );
            studentBsModal.hide();
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const universitySelect = document.querySelector('select[name="university"]');
    const campusSelect = document.querySelector('select[name="campus"]');
    const courseSelect = document.querySelector('select[name="course"]');

    universitySelect.addEventListener('change', function () {
        const universityId = this.value;

        campusSelect.innerHTML = '<option value="">Selecione um campus</option>';
        courseSelect.innerHTML = '<option value="">Selecione um curso</option>';

        if (!universityId) return;

        fetch(`/campus/get?acronym=${universityId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    data.data.forEach(campus => {
                        const option = document.createElement('option');
                        option.value = campus.id;
                        option.textContent = campus.name;
                        campusSelect.appendChild(option);
                    });
                } else {
                    handleApiErrors(data);
                }
            });
    });

    campusSelect.addEventListener('change', function () {
        const campusId = this.value;

        courseSelect.innerHTML = '<option value="">Selecione um curso</option>';

        if (!campusId) return;

        fetch(`/courses/get?campus_id=${campusId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    data.data.forEach(course => {
                        const option = document.createElement('option');
                        option.value = course.id;
                        option.textContent = course.name;
                        courseSelect.appendChild(option);
                    });
                } else {
                    handleApiErrors(data);
                }
            });
    });
});

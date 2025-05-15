const universityCollapse = document.getElementById('university-collapse');
const universityBsCollapse = bootstrap.Collapse.getOrCreateInstance(universityCollapse, { toggle: false });
const universityIcon = document.getElementById('university-icon');
const universityTable = document.getElementById('university-table');
const universityRegisterBtn = document.getElementById('university-register-btn')
const universityModal = document.getElementById('university-register-modal');
const universityBsModal = new bootstrap.Modal(universityModal);
const deleteUniversityBtn = document.getElementById('university-delete-btn');
const saveUniversityBtn = document.getElementById('university-save-btn');
const universityModalTitle = document.getElementById('university-register-modal-title');
let removeUniversityUrl;
let removeCampusUrl;

const campusCollapse = document.getElementById('campus-collapse');
const campusBsCollapse = bootstrap.Collapse.getOrCreateInstance(campusCollapse, { toggle: false });
const campusIcon = document.getElementById('campus-icon');
const campusTable = document.getElementById('campus-table');
const campusRegisterBtn = document.getElementById('campus-register-btn')
const campusModal = document.getElementById('campus-register-modal');
const campusBsModal = new bootstrap.Modal(campusModal);
const deleteCampusBtn = document.getElementById('campus-delete-btn');
const saveCampusBtn = document.getElementById('campus-save-btn');
const campusModalTitle = document.getElementById('campus-register-modal-title');
const campusCollapseTitle = document.getElementById('campus-collapse-title');
const campusForm = document.getElementById('campus-form');
let lastUniversityCampusQuery = null;

const coursesCollapse = document.getElementById('courses-collapse');
const coursesBsCollapse = bootstrap.Collapse.getOrCreateInstance(coursesCollapse, { toggle: false });
const coursesIcon = document.getElementById('courses-icon');
const coursesTable = document.getElementById('courses-table');
const coursesRegisterBtn = document.getElementById('courses-register-btn')
const coursesModal = document.getElementById('courses-register-modal');
const coursesBsModal = new bootstrap.Modal(coursesModal);
const deleteCourseBtn = document.getElementById('course-delete-btn');
const saveCourseBtn = document.getElementById('course-save-btn');
const coursesModalTitle = document.getElementById('course-register-modal-title');
const coursesCollapseTitle = document.getElementById('courses-collapse-title');
const courseForm = document.getElementById('course-form');
let lastCourseCampusQuery = null;

var selectedCourseRow = null;
var selectedUniversityRow = null;
var selectedCampusRow = null;

// UNIVERSIDADE
universityCollapse.addEventListener('show.bs.collapse', (event) => {
    if (coursesCollapse.classList.contains('show')){
        coursesBsCollapse.hide();
    }
    campusBsCollapse.hide();
    universityIcon.classList.add('rotated');
});

universityCollapse.addEventListener('hidden.bs.collapse', () => {
    universityIcon.classList.remove('rotated');
});


//CAMPUS
campusCollapse.addEventListener('show.bs.collapse', (event) => {
    console.log(selectedUniversityRow);
    if (selectedUniversityRow === null) {
        event.preventDefault();
        return;
    } else {
        if (selectedUniversityRow.dataset.id != lastUniversityCampusQuery) {
            loadCampusTable(selectedUniversityRow.dataset.id);
            lastUniversityCampusQuery = selectedUniversityRow.dataset.id;
        }
        campusCollapseTitle.innerText = selectedUniversityRow.dataset.id;
        universityBsCollapse.hide();
    }
    coursesBsCollapse.hide();
    campusIcon.classList.add('rotated');
});

campusCollapse.addEventListener('hide.bs.collapse', () => {
    campusIcon.classList.remove('rotated');
    if (coursesCollapse.classList.contains('show')) {
        universityBsCollapse.show();
    }
});

//CURSOS
coursesCollapse.addEventListener('show.bs.collapse', (event) => {
    if (selectedCampusRow === null) {
        event.preventDefault();
        return;
    } else {
        if (selectedCampusRow.dataset.id != lastCourseCampusQuery) {
            loadCoursesTable();
            lastCourseCampusQuery = selectedCampusRow.dataset.id;
        }
        coursesCollapseTitle.innerText = selectedCampusRow.querySelector('td')?.textContent.trim();
        campusBsCollapse.hide();
        universityBsCollapse.hide();
    }
    coursesIcon.classList.add('rotated');
});

coursesCollapse.addEventListener('hide.bs.collapse', (event) => {
    coursesIcon.classList.remove('rotated');
    if (universityCollapse.classList.contains('hide')){
        campusBsCollapse.show();
    }
});


function unlockIcon(iconElem) {
    iconElem.classList.remove('fa-lock');
    iconElem.classList.add('fa-chevron-down');
}

function lockIcon(iconElem){
    iconElem.classList.remove('fa-chevron-down');
    iconElem.classList.add('fa-lock');
}

function loadUniversitiesTable(universities){
    let keys = ['acronym', 'name']

    addTableRows(
        universityTable,
        universities,
        keys,
        true,
        (row) => selectedUniversityController(row),
        () => openEditUniversityModal()
    );
    
}

function selectedUniversityController(newRow) {
    // Remove 'table-active' de todas as linhas da tabela de universidades
    universityTable.querySelectorAll('tbody tr').forEach(row => {
        row.classList.remove('table-active');
    });

    selectedUniversityRow = newRow;
    selectedUniversityRow.classList.add('table-active');
    unlockIcon(campusIcon);
}

function selectedCourseController(newRow) {
    // Remove 'table-active' de todas as linhas da tabela de cursos
    coursesTable.querySelectorAll('tbody tr').forEach(row => {
        row.classList.remove('table-active');
    });

    selectedCourseRow = newRow;
    selectedCourseRow.classList.add('table-active');
}

function selectedCampusController(newRow) {
    // Remove 'table-active' de todas as linhas da tabela de campi
    campusTable.querySelectorAll('tbody tr').forEach(row => {
        row.classList.remove('table-active');
    });

    selectedCampusRow = newRow;
    selectedCampusRow.classList.add('table-active');
    unlockIcon(coursesIcon);
}

function loadCampusTable() {
    const tbody = campusTable.querySelector('tbody');

    // Remove todas as linhas do tbody
    tbody.innerHTML = '';

    const universityId = selectedUniversityRow.dataset.id;
    fetch(`/campus/get?acronym=${universityId}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableRows(
            campusTable,
            data.data,
            ['id', 'name', 'course_count'],
            false,
            (row) => selectedCampusController(row),
            () => openEditCampusModal()
        )


        lastUniversityCampusQuery = universityId;
    })
    .catch(error => {
        console.error('Erro ao carregar campus:', error);
    });
}

function loadCoursesTable() {
    const tbody = coursesTable.querySelector('tbody');

    // Remove todas as linhas do tbody
    tbody.innerHTML = '';

    const campusId = selectedCampusRow.dataset.id;
    fetch(`/courses/get?campus_id=${campusId}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableRows(
            coursesTable,
            data.data,
            ['id', 'name'],
            false,
            (row) => selectedCourseController(row),
            () => openEditCourseModal()
        )


        lastCourseCampusQuery = campusId;
    })
    .catch(error => {
        console.error('Erro ao carregar campus:', error);
    });
}

function openEditUniversityModal() {
    fetch('/universities/get?acronym=' + selectedUniversityRow.dataset.id)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
            const form = document.querySelector('#university-form');
            const inputAcronym = document.querySelector('input[name="acronym"]');
            const inputName = document.querySelector('input[name="name"]');

            inputAcronym.value = data.university.acronym;
            inputAcronym.readOnly = true;
            removeUniversityUrl = '/universities/delete/' + data.university.acronym + '/';
            form.action = '/universities/edit/' + data.university.acronym + '/';
            form.dataset.id = data.university.acronym;
            inputName.value = data.university.name;
            openModal(
                universityBsModal,
                universityModalTitle,
                'Editar universidade',
                saveUniversityBtn,
                deleteUniversityBtn,
                true,
                'Você tem certeza que deseja excluir este registro?',
                () => {
                    fetch(removeUniversityUrl, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            body: JSON.stringify({
                                university_id: selectedUniversityRow?.dataset?.id // ou outro identificador necessário
                            })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                toastMessage(data.message || 'Salvo com sucesso!', true);
                                form.reset();
                                selectedUniversityRow.remove();
                                universityBsModal.hide();
                                selectedUniversityRow = null;
                                lockIcon(campusIcon);
                                lockIcon(coursesIcon);
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

universityRegisterBtn.addEventListener('click', () => {
    clearForm('#university-form');
    const form = document.querySelector('#university-form');
    form.action = registerUniversityUrl;

    const inputAcronym = document.querySelector('input[name="acronym"]');
    inputAcronym.readOnly = false;
    openModal(
        universityBsModal,
        universityModalTitle,
        'Cadastrar universidade',
        saveUniversityBtn,
        deleteUniversityBtn,
        false
    )    
});

function openEditCampusModal() {
    fetch('/campus/get?id=' + selectedCampusRow.dataset.id)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
            const form = document.querySelector('#campus-form');
            const inputAcronym = form.querySelector('input[name="university"]');
            const inputName = form.querySelector('input[name="name"]');
            const inputCity = form.querySelector('select[name="city"]');
            const inputState = form.querySelector('select[name="state"]');

            inputAcronym.value = data.data.university;
            inputAcronym.readOnly = true;
            removeCampusUrl = '/campus/delete/' + data.data.id + '/';
            form.action = '/campus/edit/' + data.data.id + '/';
            form.dataset.id = data.data.id;
            inputName.value = data.data.name;
            inputState.value = data.data.state;
            inputState.dispatchEvent(new Event('change'));
            setTimeout(() => {
                    inputCity.value = data.data.city;
                }, 100); // espera o carregamento das cidades
            openModal(
                campusBsModal,
                campusModalTitle,
                'Editar campus',
                saveCampusBtn,
                deleteCampusBtn,
                true,
                'Você tem certeza que deseja excluir este registro?',
                () => {
                    fetch(removeCampusUrl)
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                toastMessage(data.message || 'Salvo com sucesso!', true);
                                form.reset();
                                selectedCampusRow.remove();
                                campusBsModal.hide();
                                selectedCampusRow = null;
                                lockIcon(coursesIcon);
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

function openEditCourseModal() {
    fetch('/courses/get?course_id=' + selectedCourseRow.dataset.id)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
            const form = document.querySelector('#course-form');
            const inputName = form.querySelector('input[name="name"]');

            let acronymCourseInput = courseForm.querySelector('#id_university');
            acronymCourseInput.value = data.data.university;

            const campusSelect = courseForm.querySelector('#id_campus');
            campusSelect.innerHTML = ''; // limpa as opções

            const option = document.createElement('option');
            option.value = data.data.campus_id;
            option.textContent = data.data.campus_name;
            option.selected = true;

            campusSelect.appendChild(option);

            let hiddenInput = courseForm.querySelector('#id_hidden_campus');
            if (!hiddenInput) {
                hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'campus';
                hiddenInput.id = 'id_hidden_campus';
                courseForm.appendChild(hiddenInput);
            }
            hiddenInput.value = data.data.campus_id;

            removeCampusUrl = '/courses/delete/' + data.data.id + '/';
            form.action = '/courses/edit/' + data.data.id + '/';
            form.dataset.id = data.data.id;
            inputName.value = data.data.name;
            openModal(
                coursesBsModal,
                coursesModalTitle,
                'Editar curso',
                saveCourseBtn,
                deleteCourseBtn,
                true,
                'Você tem certeza que deseja excluir este registro?',
                () => {
                    fetch('delete/' + data.data.id + '/')
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                toastMessage(data.message || 'Salvo com sucesso!', true);
                                form.reset();
                                selectedCourseRow.remove();
                                coursesBsModal.hide();
                                selectedCourseRow = null;
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

campusRegisterBtn.addEventListener('click', () => {
    campusForm.action = '/campus/register/';
    clearForm("#campus-form");
    let acronymCampusInput = campusForm.querySelector('#id_university');
    acronymCampusInput.value = selectedUniversityRow.dataset.id;
    acronymCampusInput.readOnly = true;

    campusForm.dataset.id = '';
    openModal(
        campusBsModal,
        campusModalTitle,
        'Cadastrar campus',
        saveCampusBtn,
        deleteCampusBtn,
        false
    )    
});

coursesRegisterBtn.addEventListener('click', () => {
    courseForm.action = '/courses/register/';
    clearForm("#course-form");
    let acronymCourseInput = courseForm.querySelector('#id_university');
    acronymCourseInput.value = selectedUniversityRow.dataset.id;

    const campusSelect = courseForm.querySelector('#id_campus');
    campusSelect.innerHTML = ''; // limpa as opções

    const option = document.createElement('option');
    option.value = selectedCampusRow.dataset.id;
    option.textContent = coursesCollapseTitle.innerText;
    option.selected = true;

    campusSelect.appendChild(option);

    let hiddenInput = courseForm.querySelector('#id_hidden_campus');
    if (!hiddenInput) {
        hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'campus';
        hiddenInput.id = 'id_hidden_campus';
        courseForm.appendChild(hiddenInput);
    }
    hiddenInput.value = selectedCampusRow.dataset.id;

    openModal(
        coursesBsModal,
        coursesModalTitle,
        'Cadastrar curso',
        saveCourseBtn,
        deleteCourseBtn,
        false
    )    
});


loadUniversitiesTable(universities);

document.addEventListener('DOMContentLoaded', function () {
    handleFormWithFetch('#university-form', (obj) => {
            addTableRows(
            universityTable,
            [obj],
            ['acronym', 'name'],
            true,
            (row) => selectedUniversityController(row),
            () => openEditUniversityModal()
        );
            universityBsModal.hide();
    });
    handleFormWithFetch('#campus-form', (obj) => {
        if (!obj.hasOwnProperty('id')) {
            obj.id = campusForm.dataset.id;
        }

        obj.course_count = 0;
            addTableRows(
            campusTable,
            [obj],
            ['id', 'name', 'course_count'],
            false,
            (row) => selectedCampusController(row),
            () => openEditCampusModal()
        );
            campusBsModal.hide();
    });

    handleFormWithFetch('#course-form', (obj) => {
        if (!obj.hasOwnProperty('id')) {
            obj.id = campusForm.dataset.id;
        }

            addTableRows(
            coursesTable,
            [obj],
            ['id', 'name'],
            false,
            (row) => selectedCourseController(row),
            () => openEditCourseModal()
        );
            coursesBsModal.hide();
    });
});
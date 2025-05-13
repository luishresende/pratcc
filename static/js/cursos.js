const universityCollapse = document.getElementById('university-collapse');
const universityBsCollapse = bootstrap.Collapse.getOrCreateInstance(universityCollapse, { toggle: false });
const universityIcon = document.getElementById('university-icon');
const univesityTable = document.getElementById('university-table');

const campusCollapse = document.getElementById('campus-collapse');
const campusBsCollapse = bootstrap.Collapse.getOrCreateInstance(campusCollapse, { toggle: false });
const campusIcon = document.getElementById('campus-icon');
const campusTable = document.getElementById('campus-table');

const coursesCollapse = document.getElementById('courses-collapse');
const coursesBsCollapse = bootstrap.Collapse.getOrCreateInstance(coursesCollapse, { toggle: false });
const coursesIcon = document.getElementById('courses-icon');
const coursesTable = document.getElementById('courses-table');

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
        console.log('Não abrindo.');
        event.preventDefault();
        return;
    } else {
        universityBsCollapse.hide();
    }
    console.log('continuei');
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
    iconElem.classList.remove('fas fa-chevron-down');
    iconElem.classList.add('fas fa-lock');
}

function loadUniversitiesTable(){
    universities = [
        {
            id: 1,
            name: 'Universidade Tecnológica Federal do Paraná',
            uf: 'PR'
        },
        {
            id: 2,
            name: 'Universidade Federal do Paraná',
            uf: 'PR'
        },
    ]

    addTableRows(
        univesityTable, 
        universities, 
        (row) => selectedUniversityController(row),
        null
    );
    
}
loadUniversitiesTable();

function selectedUniversityController(newRow) {
    if (selectedUniversityRow != null){
        selectedUniversityRow.classList.remove('table-active');
    }

    selectedUniversityRow = newRow;
    selectedUniversityRow.classList.add('table-active');
    unlockIcon(campusIcon);
}

function selectedCampusController(newRow) {
    if (selectedCampusRow != null){
        selectedCampusRow.classList.remove('table-active');
    }

    selectedCampusRow = newRow;
    selectedCampusRow.classList.add('table-active');
    unlockIcon(coursesIcon);
}

function loadCampusTable(){
    campus = [
        {
            id: 1,
            name: 'Santa Helena',
            courses: 3
        },
        {
            id: 2,
            name: 'Curitiba',
            courses: 13
        },
    ]

    addTableRows(
        campusTable, 
        campus, 
        (row) => selectedCampusController(row),
        null
    );
    
}
loadCampusTable();




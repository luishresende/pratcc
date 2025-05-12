const registerTeacherBtn = document.getElementById('register-teacher-btn');
const teacherTable = document.getElementById('teacher-table');


function loadTeachersTable() {
  teachers = [
    {
      id: 1,
      name: "Thiago",
      registration: 2457733,
      supervisors: 4,
      cosupervisors: 1,
      committes: 3
    },
    {
      id: 2,
      name: "Debora",
      registration: 2457733,
      supervisors: 2,
      cosupervisors: 5,
      committes: 1
    },
    {
      id: 3,
      name: "Fulano",
      registration: 2457733,
      supervisors: 41,
      cosupervisors: 13,
      committes: 39
    },
    {
      id: 4,
      name: "Ciclano",
      registration: 2457733,
      supervisors: 44,
      cosupervisors: 11,
      committes: 32
    }
  ]

  addTableRows(
    teacherTable, 
    teachers, 
    null,
    () => selectRadioAndHandle(
      'teacher-radio', 
      true, 
      'Você tem certeza que deseja excluir este professor?', 
      () => console.log('Professor deletado.'))
    );

}

loadTeachersTable();

function addTeacherCourses(courses, removeAll=false) {
  addTableRow(teacherAfilliationsTable, courses);
}

registerTeacherBtn.addEventListener('click', () => {
  selectRadioAndHandle('teacher-radio', false);
});

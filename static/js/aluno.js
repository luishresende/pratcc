const registerStudentBtn = document.getElementById('register-students-btn');
const studentTable = document.getElementById('student-table');

function loadStudentsTable() {
  students = [
    {
      id: 1,
      name: "Gilso",
      registration: 2457733,
      tccs: 4
    },
    {
      id: 2,
      name: "Alana",
      registration: 2457733,
      tccs: 4
    },
    {
      id: 3,
      name: "Luis",
      registration: 2457733,
      tccs: 4
    },
    {
      id: 4,
      name: "Cicluano",
      registration: 2457733,
      tccs: 4
    }
  ]

  addTableRows(
    studentTable, 
    students, 
    null, 
    onDblClickAction= () => selectRadioAndHandle(
      'students-radio',
      true, 
      'Você tem certeza que deseja excluir este aluno?', 
      () => console.log('Aluno deletado.'))
    );

}
loadStudentsTable();

registerStudentBtn.addEventListener('click', () => {
  selectRadioAndHandle('students-radio', false, null, null);
});

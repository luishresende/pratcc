PRAGMA foreign_keys = ON;

-- Tabela state
CREATE TABLE IF NOT EXISTS state (
  acronym TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

-- Tabela city
CREATE TABLE IF NOT EXISTS city (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  state_acronym TEXT NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY (state_acronym) REFERENCES state(acronym)
);

-- Tabela university
CREATE TABLE IF NOT EXISTS university (
  acronym TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

-- Tabela campus
CREATE TABLE IF NOT EXISTS campus (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  university_acronym TEXT NOT NULL,
  city_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY (university_acronym) REFERENCES university(acronym),
  FOREIGN KEY (city_id) REFERENCES city(id)
);

-- Tabela course
CREATE TABLE IF NOT EXISTS course (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  campus_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY (campus_id) REFERENCES campus(id)
);

-- Tabela student
CREATE TABLE IF NOT EXISTS student (
  ra TEXT PRIMARY KEY,
  course_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY (course_id) REFERENCES course(id)
);

-- Tabela teacher
CREATE TABLE IF NOT EXISTS teacher (
  teacher_ma TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  course_id INTEGER NOT NULL,
  FOREIGN KEY (course_id) REFERENCES course(id)
);

-- Tabela tcc_work
CREATE TABLE IF NOT EXISTS tcc_work (
  tcc_id INTEGER PRIMARY KEY AUTOINCREMENT,
  year INTEGER NOT NULL,
  semester INTEGER NOT NULL,
  tcc_num INTEGER NOT NULL,
  student_ra TEXT NOT NULL,
  teacher_advisor_ma TEXT NOT NULL,
  teacher_cosupervisor_ma TEXT,
  title TEXT NOT NULL,
  FOREIGN KEY (student_ra) REFERENCES student(ra),
  FOREIGN KEY (teacher_advisor_ma) REFERENCES teacher(teacher_ma),
  FOREIGN KEY (teacher_cosupervisor_ma) REFERENCES teacher(teacher_ma)
);

-- Tabela tcc_committee
CREATE TABLE IF NOT EXISTS tcc_committee (
  tccw_id INTEGER PRIMARY KEY,
  full_member_1_ma TEXT NOT NULL,
  full_member_2_ma TEXT NOT NULL,
  alternate_member_ma TEXT NOT NULL,
  defense_date TEXT NOT NULL,
  defense_location TEXT NOT NULL,
  authorization_letter_submitted INTEGER NOT NULL,
  FOREIGN KEY (tccw_id) REFERENCES tcc_work(tcc_id),
  FOREIGN KEY (full_member_1_ma) REFERENCES teacher(teacher_ma),
  FOREIGN KEY (full_member_2_ma) REFERENCES teacher(teacher_ma),
  FOREIGN KEY (alternate_member_ma) REFERENCES teacher(teacher_ma)
);

-- Tabela user
CREATE TABLE IF NOT EXISTS user (
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  teacher_ma TEXT NOT NULL UNIQUE,
  FOREIGN KEY (teacher_ma) REFERENCES teacher(teacher_ma)
);

-- Tabela tcc_documents
CREATE TABLE IF NOT EXISTS tcc_documents (
  tccw_id INTEGER PRIMARY KEY,
  fm1_evaluation_form INTEGER NOT NULL,
  fm2_evaluation_form INTEGER NOT NULL,
  fm3_evaluation_form INTEGER NOT NULL,
  approvation_term INTEGER NOT NULL,
  end_monograph INTEGER NOT NULL,
  end_monograph_in_lib INTEGER NOT NULL,
  recorded_data INTEGER NOT NULL,
  FOREIGN KEY (tccw_id) REFERENCES tcc_work(tcc_id)
);
BEGIN TRANSACTION;

-- Миграция данных из таблицы addresses в addresses_copy, её удаление и переименование

CREATE TABLE addresses_copy (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255), 
	addresses TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO addresses_copy (id, view, addresses, created, person_id) SELECT id, view, addresses, created, person_id FROM addresses WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE addresses;

ALTER TABLE addresses_copy RENAME TO addresses;

-- Миграция данных из таблицы affilations в affilations_copy, её удаление и переименование

CREATE TABLE affilations_copy (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255), 
	organization TEXT, 
	inn VARCHAR(255), 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO affilations_copy (id, view, organization, inn, created, person_id) SELECT id, view, organization, inn, created, person_id FROM affilations WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE affilations;

ALTER TABLE affilations_copy RENAME TO affilations;

-- Миграция данных из таблицы contacts в contacts_copy, её удаление и переименование

CREATE TABLE contacts_copy (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255), 
	contact VARCHAR(255), 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO contacts_copy (id, view, contact, created, person_id) SELECT id, view, contact, created, person_id FROM contacts WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE contacts;

ALTER TABLE contacts_copy RENAME TO contacts;

-- Миграция данных из таблицы documents в documents_copy, её удаление и переименование

CREATE TABLE documents_copy (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255), 
	series VARCHAR(255), 
	digits VARCHAR(255), 
	agency TEXT, 
	issue DATE, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO documents_copy (id, view, series, digits, agency, issue, created, person_id) SELECT id, view, series, digits, agency, issue, created, person_id FROM documents WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE documents;

ALTER TABLE documents_copy RENAME TO documents;

-- Миграция данных из таблицы educations в educations_copy, её удаление и переименование

CREATE TABLE educations_copy (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255), 
	institution TEXT, 
	finished INTEGER, 
	specialty TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO educations_copy (id, view, institution, finished, specialty, created, person_id) SELECT id, view, institution, finished, specialty, created, person_id FROM educations WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE educations;

ALTER TABLE educations_copy RENAME TO educations;


-- Миграция данных из таблицы previous в previous_copy, её удаление и переименование

CREATE TABLE previous_copy (
	id INTEGER NOT NULL, 
	surname VARCHAR(255), 
	firstname VARCHAR(255), 
	patronymic VARCHAR(255), 
	changed VARCHAR(255), 
	reason TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO previous_copy (id, surname, firstname, patronymic, changed, reason, created, person_id) SELECT id, surname, firstname, patronymic, changed, reason, created, person_id FROM previous WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE previous;

ALTER TABLE previous_copy RENAME TO previous;

-- Миграция данных из таблицы staffs в staffs_copy, её удаление и переименование

CREATE TABLE staffs_copy (
	id INTEGER NOT NULL, 
	position TEXT, 
	department TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO staffs_copy (id, position, department, created, person_id) SELECT id, position, department, created, person_id FROM staffs WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE staffs;

ALTER TABLE staffs_copy RENAME TO staffs;

-- Миграция данных из таблицы workplaces в workplaces_copy, её удаление и переименование

CREATE TABLE workplaces_copy (
	id INTEGER NOT NULL, 
	now_work BOOLEAN, 
	starts DATE, 
	finished DATE, 
	workplace VARCHAR(255), 
	addresses TEXT, 
	position TEXT, 
	reason TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO workplaces_copy (id, now_work, starts, finished, workplace, addresses, position, reason, created, person_id) SELECT id, now_work, starts, finished, workplace, addresses, position, reason, created, person_id FROM workplaces WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE workplaces;

ALTER TABLE workplaces_copy RENAME TO workplaces;

-- Миграция данных из таблицы checks в checks_copy, её удаление и переименование

CREATE TABLE checks_copy (
	id INTEGER NOT NULL, 
	workplace TEXT, 
	document TEXT, 
	inn TEXT, 
	debt TEXT, 
	bankruptcy TEXT, 
	bki TEXT, 
	courts TEXT, 
	affilation TEXT, 
	terrorist TEXT, 
	mvd TEXT, 
	internet TEXT, 
	cronos TEXT, 
	cros TEXT, 
	addition TEXT, 
	comment TEXT, 
	conclusion TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
    username TEXT,
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO checks_copy (id, workplace, document, inn, debt, bankruptcy, bki, courts, affilation, terrorist, mvd, internet, cronos, cros, addition, comment, conclusion, created, person_id) SELECT id, workplace, document, inn, debt, bankruptcy, bki, courts, affilation, terrorist, mvd, internet, cronos, cros, addition, comment, conclusion, created, person_id FROM checks WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE checks;

ALTER TABLE checks_copy RENAME TO checks;

-- Миграция данных из таблицы inquiries в inquiries_copy, её удаление и переименование

CREATE TABLE inquiries_copy (
	id INTEGER NOT NULL, 
	info TEXT, 
	initiator VARCHAR(255), 
	origins VARCHAR(255), 
	created DATETIME NOT NULL,
	person_id INTEGER NOT NULL, 
    username TEXT,
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO inquiries_copy (id, info, initiator, origins, created, person_id) SELECT id, info, initiator, origins, created, person_id FROM inquiries WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE inquiries;

ALTER TABLE inquiries_copy RENAME TO inquiries;

-- Миграция данных из таблицы investigations в investigations_copy, её удаление и переименование

CREATE TABLE investigations_copy (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	info TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
    username TEXT,
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO investigations_copy (id, theme, info, created, person_id) SELECT id, theme, info, created, person_id FROM investigations WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE investigations;

ALTER TABLE investigations_copy RENAME TO investigations;

-- Миграция данных из таблицы poligrafs в poligrafs_copy, её удаление и переименование

CREATE TABLE poligrafs_copy (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	results TEXT, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
    conclusion TEXT, 
    username TEXT,
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
);

INSERT INTO poligrafs_copy (id, theme, results, created, person_id, conclusion) SELECT id, theme, results, created, person_id, conclusion FROM poligrafs WHERE person_id IS NOT NULL AND person_id IN (SELECT id FROM persons);

DROP TABLE poligrafs;

ALTER TABLE poligrafs_copy RENAME TO poligrafs;

COMMIT;
CREATE TABLE users (
	id INTEGER NOT NULL, 
	fullname VARCHAR(255) NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	password VARCHAR NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	pswd_create DATETIME DEFAULT (DATETIME('now')), 
	change_pswd BOOLEAN DEFAULT 1, 
	last_login DATETIME, 
	blocked BOOLEAN DEFAULT 0,
	deleted BOOLEAN DEFAULT 0,
	attempt INTEGER DEFAULT 0,
	has_admin BOOLEAN DEFAULT 0,
	created DATETIME DEFAULT (DATETIME('now')), 
	updated DATETIME, 
	region VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (username), 
	UNIQUE (email)
)
;
CREATE TABLE persons (
	id INTEGER NOT NULL, 
	surname VARCHAR(255) NOT NULL, 
	firstname VARCHAR(255) NOT NULL, 
	patronymic VARCHAR(255), 
	birthday DATE NOT NULL, 
	birthplace TEXT, 
	country VARCHAR(255), 
	ext_country VARCHAR(255), 
    snils VARCHAR(11) CHECK(LENGTH(snils) = 11),
	inn VARCHAR(12) CHECK(LENGTH(inn) = 12), 
	marital VARCHAR(255), 
	addition TEXT, 
	path TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	updated DATETIME, 
	region VARCHAR(255) NOT NULL, 
	status VARCHAR(255) NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
)
;
CREATE TABLE previous (
	id INTEGER NOT NULL, 
	surname VARCHAR(255), 
	firstname VARCHAR(255), 
	patronymic VARCHAR(255), 
	date_change INTEGER, 
	reason TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE educations (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	name TEXT, 
	finish INTEGER, 
	speciality TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE staffs (
	id INTEGER NOT NULL, 
	position TEXT, 
	department TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE documents (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	series VARCHAR(255), 
	number VARCHAR(255), 
	agency TEXT, 
	issue DATE, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE addresses (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	address TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE contacts (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	contact VARCHAR(255), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE workplaces (
	id INTEGER NOT NULL, 
	now_work BOOLEAN DEFAULT 0, 
	start_date DATE, 
	end_date DATE, 
	workplace VARCHAR(255), 
	address TEXT, 
	position TEXT, 
	reason TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE affilations (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	name TEXT, 
	inn VARCHAR(255), 
	position TEXT, 
	data INTEGER, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE relations (
	id INTEGER NOT NULL, 
	relation VARCHAR(255) NOT NULL, 
	relation_id INTEGER NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(relation_id) REFERENCES persons (id) ON DELETE CASCADE,
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE checks (
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
	pfo BOOLEAN, 
	comments TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	updated DATETIME,
	conclusion VARCHAR(255) NOT NULL, 
	person_id INTEGER NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
)
;
CREATE TABLE poligrafs (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	results TEXT, 
	user_id INTEGER, 
	created DATETIME DEFAULT (DATETIME('now')), 
	updated DATETIME,
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE investigations (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	info TEXT, 
	user_id INTEGER, 
	created DATETIME DEFAULT (DATETIME('now')), 
	updated DATETIME,
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE inquiries (
	id INTEGER NOT NULL, 
	info TEXT, 
	initiator VARCHAR(255), 
	source VARCHAR(255), 
	user_id INTEGER, 
	created DATETIME DEFAULT (DATETIME('now')), 
	updated DATETIME,
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE connects (
	id INTEGER NOT NULL, 
	name VARCHAR(255), 
	company VARCHAR(255), 
	city VARCHAR(255), 
	fullname VARCHAR(255), 
	phone VARCHAR(255), 
	adding VARCHAR(255), 
	mobile VARCHAR(255), 
	mail VARCHAR(255), 
	comment TEXT, 
	updated DATETIME DEFAULT (DATETIME('now')), 
	PRIMARY KEY (id), 
	UNIQUE (id)
)


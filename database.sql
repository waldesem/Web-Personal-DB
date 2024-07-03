CREATE TABLE IF NOT EXISTS users (
	id INTEGER NOT NULL, 
	fullname VARCHAR(255) NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	passhash VARCHAR (255),
	pswd_create DATETIME DEFAULT (DATETIME('now')), 
	change_pswd BOOLEAN DEFAULT 1, 
	last_login DATETIME, 
	blocked BOOLEAN DEFAULT 0,
	deleted BOOLEAN DEFAULT 0,
	attempt INTEGER DEFAULT 0,
	has_admin BOOLEAN DEFAULT 0,
	created DATETIME DEFAULT (DATETIME('now')), 
	region VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (username), 
	UNIQUE (email)
)
;
CREATE TABLE IF NOT EXISTS persons (
	id INTEGER NOT NULL, 
	surname VARCHAR(255) NOT NULL, 
	firstname VARCHAR(255) NOT NULL, 
	patronymic VARCHAR(255), 
	birthday DATE NOT NULL, 
	birthplace TEXT, 
	citizenship VARCHAR(255), 
	dual VARCHAR(255), 
    snils VARCHAR(255),
	inn VARCHAR(255), 
	marital VARCHAR(255), 
	addition TEXT, 
	destination TEXT,
	created DATETIME DEFAULT (DATETIME('now')), 
	region VARCHAR(255) NOT NULL, 
	standing VARCHAR(255) NOT NULL,
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE IF NOT EXISTS previous (
	id INTEGER NOT NULL, 
	surname VARCHAR(255), 
	firstname VARCHAR(255), 
	patronymic VARCHAR(255), 
	changed INTEGER, 
	reason TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS educations (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	institution TEXT,
	finished INTEGER, 
	speciality TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS staffs (
	id INTEGER NOT NULL, 
	position TEXT, 
	department TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS documents (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	series VARCHAR(255), 
	digits VARCHAR(255), 
	agency TEXT, 
	issue DATE, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS addresses (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	addresses TEXT,
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS contacts (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	contact VARCHAR(255), 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS workplaces (
	id INTEGER NOT NULL, 
	now_work BOOLEAN DEFAULT 0, 
	starts DATE,
	finished DATE, 
	workplace VARCHAR(255), 
	addresses TEXT,
	position TEXT, 
	reason TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS affilations (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	organization TEXT,
	inn VARCHAR(255), 
	position TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS relations (
	id INTEGER NOT NULL, 
	relation VARCHAR(255) NOT NULL, 
	created DATETIME DEFAULT (DATETIME('now')), 
	relation_id INTEGER NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(relation_id) REFERENCES persons (id) ON DELETE CASCADE,
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS checks (
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
	comment TEXT, 
	created DATETIME DEFAULT (DATETIME('now')), 
	conclusion VARCHAR(255), 
	person_id INTEGER NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE IF NOT EXISTS poligrafs (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	results TEXT, 
	user_id INTEGER, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS investigations (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	info TEXT, 
	user_id INTEGER, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
CREATE TABLE IF NOT EXISTS inquiries (
	id INTEGER NOT NULL, 
	info TEXT, 
	origins VARCHAR(255),
	user_id INTEGER, 
	created DATETIME DEFAULT (DATETIME('now')), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
)
;
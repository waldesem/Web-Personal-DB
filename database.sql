
CREATE TABLE user_roles (
	user_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id, role_id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
)
;
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	role VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (role)
)
;
CREATE TABLE regions (
	id INTEGER NOT NULL, 
	region VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id)
)
;
CREATE TABLE users (
	id INTEGER NOT NULL, 
	fullname VARCHAR(255), 
	username VARCHAR(255) NOT NULL, 
	password VARCHAR, 
	email VARCHAR(255), 
	pswd_create DATETIME, 
	pswd_change DATETIME, 
	last_login DATETIME, 
	blocked BOOLEAN NOT NULL, 
	deleted BOOLEAN NOT NULL, 
	attempt INTEGER, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	region_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (username), 
	UNIQUE (email), 
	FOREIGN KEY(region_id) REFERENCES regions (id)
)
;
CREATE TABLE messages (
	id INTEGER NOT NULL, 
	message TEXT, 
	created DATETIME, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE statuses (
	id INTEGER NOT NULL, 
	status VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (id)
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
	snils VARCHAR(11), 
	inn VARCHAR(12), 
	marital VARCHAR(255), 
	addition TEXT, 
	path TEXT, 
	created DATETIME, 
	updated DATETIME, 
	region_id INTEGER, 
	status_id INTEGER, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(region_id) REFERENCES regions (id), 
	FOREIGN KEY(status_id) REFERENCES statuses (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE previous (
	id INTEGER NOT NULL, 
	surname VARCHAR(255), 
	firstname VARCHAR(255), 
	patronymic VARCHAR(255), 
	date_change DATE, 
	reason TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE educations (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	name TEXT, 
	"end" INTEGER, 
	specialty TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE staffs (
	id INTEGER NOT NULL, 
	position TEXT, 
	department TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
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
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE addresses (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	address TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE contacts (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	contact VARCHAR(255), 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE workplaces (
	id INTEGER NOT NULL, 
	now_work BOOLEAN, 
	start_date DATE, 
	end_date DATE, 
	workplace VARCHAR(255), 
	address TEXT, 
	position TEXT, 
	reason TEXT, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE affilations (
	id INTEGER NOT NULL, 
	view VARCHAR(255), 
	name TEXT, 
	inn VARCHAR(255), 
	position TEXT, 
	deadline DATE, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE relations (
	id INTEGER NOT NULL, 
	relation VARCHAR(255), 
	relation_id INTEGER, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
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
	deadline DATE, 
	conclusion_id INTEGER, 
	person_id INTEGER NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(conclusion_id) REFERENCES conclusions (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE conclusions (
	id INTEGER NOT NULL, 
	conclusion VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (id)
)
;
CREATE TABLE poligrafs (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	results TEXT, 
	user_id INTEGER, 
	deadline DATE, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE investigations (
	id INTEGER NOT NULL, 
	theme VARCHAR(255), 
	info TEXT, 
	user_id INTEGER, 
	deadline DATE, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
)
;
CREATE TABLE inquiries (
	id INTEGER NOT NULL, 
	info TEXT, 
	initiator VARCHAR(255), 
	source VARCHAR(255), 
	user_id INTEGER, 
	deadline DATE, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id)
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
	data DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (id)
)


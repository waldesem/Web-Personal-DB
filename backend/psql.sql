CREATE TABLE
	IF NOT EXISTS users (
		id SERIAL,
		fullname VARCHAR(255) NOT NULL,
		username VARCHAR(255) NOT NULL,
		passhash VARCHAR(255),
		pswd_create TIMESTAMP DEFAULT now(),
		change_pswd BOOLEAN DEFAULT TRUE,
		blocked BOOLEAN DEFAULT FALSE,
		deleted BOOLEAN DEFAULT FALSE,
		attempt INTEGER DEFAULT 0,
		has_admin BOOLEAN DEFAULT FALSE,
		created TIMESTAMP DEFAULT now(),
		region VARCHAR(255) NOT NULL,
		PRIMARY KEY (id),
		UNIQUE (id),
		UNIQUE (username)
	);

CREATE TABLE
	IF NOT EXISTS persons (
		id SERIAL,
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
		created TIMESTAMP DEFAULT now(),
		region VARCHAR(255) NOT NULL,
		standing BOOLEAN DEFAULT FALSE,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS previous (
		id SERIAL,
		surname VARCHAR(255),
		firstname VARCHAR(255),
		patronymic VARCHAR(255),
		changed INTEGER,
		reason TEXT,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS educations (
		id SERIAL,
		view VARCHAR(255),
		institution TEXT,
		finished INTEGER,
		speciality TEXT,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS staffs (
		id SERIAL,
		position TEXT,
		department TEXT,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS documents (
		id SERIAL,
		view VARCHAR(255),
		series VARCHAR(255),
		digits VARCHAR(255),
		agency TEXT,
		issue DATE,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS addresses (
		id SERIAL,
		view VARCHAR(255),
		addresses TEXT,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS contacts (
		id SERIAL,
		view VARCHAR(255),
		contact VARCHAR(255),
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS workplaces (
		id SERIAL,
		now_work BOOLEAN DEFAULT FALSE,
		starts DATE,
		finished DATE,
		workplace VARCHAR(255),
		addresses TEXT,
		position TEXT,
		reason TEXT,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS affilations (
		id SERIAL,
		view VARCHAR(255),
		organization TEXT,
		inn VARCHAR(255),
		position TEXT,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS relations (
		id SERIAL,
		relation VARCHAR(255) NOT NULL,
		created TIMESTAMP DEFAULT now(),
		relation_id SERIAL,
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (relation_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS checks (
		id SERIAL,
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
		created TIMESTAMP DEFAULT now(),
		conclusion VARCHAR(255),
		person_id SERIAL,
		user_id INTEGER,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
		FOREIGN KEY (user_id) REFERENCES users (id)
	);

CREATE TABLE
	IF NOT EXISTS poligrafs (
		id SERIAL,
		theme VARCHAR(255),
		results TEXT,
		user_id INTEGER,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (user_id) REFERENCES users (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
	);

CREATE TABLE
	IF NOT EXISTS investigations (
		id SERIAL,
		theme VARCHAR(255),
		info TEXT,
		user_id INTEGER,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (user_id) REFERENCES users (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
	);

CREATE TABLE
	IF NOT EXISTS inquiries (
		id SERIAL,
		info TEXT,
		origins VARCHAR(255),
		user_id INTEGER,
		created TIMESTAMP DEFAULT now(),
		person_id SERIAL,
		PRIMARY KEY (id),
		UNIQUE (id),
		FOREIGN KEY (user_id) REFERENCES users (id),
		FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
	);
James Telzrow
2025-02-25

# Database Schema

This document will be expanded as we develop the system.

## Users Table
This table represents a list of all users.
```
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	email TEXT UNIQUE NOT NULL,
	password_hash TEXT NOT NULL,
	user_role TEXT NOT NULL,
	CHECK (user_role in ('student', 'faculty'))
);
```

## Department Table
This table represents a list of all available departments.
```
CREATE TABLE departments (
	id SERIAL PRIMARY KEY,
	code TEXT UNIQUE NOT NULL,
	name TEXT UNIQUE NOT NULL
)
```

## Course Table
```
CREATE TABLE courses (
	id SERIAL PRIMARY KEY,
	department_id INTEGER NOT NULL REFERENCES departments(id),
	code TEXT UNIQUE NOT NULL,
	name TEXT UNIQUE NOT NULL,
	UNIQUE (department_id, code)
)
```

## Section Table
```
CREATE TABLE sections (
	id SERIAL PRIMARY KEY,
	course_id INTEGER NOT NULL REFERENCES courses(id),
	instructor INTEGER REFERENCES users(id),
	year INTEGER NOT NULL,
	semester TEXT NOT NULL,
	CHECK (semester in ('spring', 'summer', 'fall'))
)
```

## Note Table
```
CREATE TABLE notes (
	id SERIAL PRIMARY KEY,
	section_id INTEGER NOT NULL REFERENCES sections(id),
	owner_id INTEGER NOT NULL REFERENCES users(id),
	content TEXT NOT NULL
)
```

## Ratings Table
```
CREATE TABLE note_ratings (
	id SERIAL PRIMARY KEY,
	note_id INTEGER NOT NULL REFERENCES notes(id),
	rater INTEGER NOT NULL REFERENCES users(id),
	rating INTEGER NOT NULL,
	CHECK (rating >= 1 AND rating <= 10)
)
```

## Comments Table
```
CREATE TABLE comments (
	id SERIAL PRIMARY KEY,
	note_id INTEGER NOT NULL REFERENCES notes(id),
	parent_comment_id INTEGER REFERENCES comments(id),
	commenter_id INTEGER NOT NULL REFERENCES users(id),
	content TEXT NOT NULL
)
```
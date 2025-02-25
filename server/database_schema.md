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
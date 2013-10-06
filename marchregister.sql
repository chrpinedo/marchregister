drop table if exists entries;
create table entries (
	number integer primary key autoincrement,
	name text not null,
	first_lastname text not null,
	second_lastname text not null,
	id_number text not null unique,
	settlement text not null,
	province text not null,
	sex text not null,
	federated integer not null,
	club text,
	email text,
	born_date text not null,
	registry_date text not null default CURRENT_DATE,
	registry_time text not null default CURRENT_TIME
);

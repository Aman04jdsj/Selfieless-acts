CREATE DATABASE selfielessacts;
use selfielessacts
create table users (usn varchar(1000),pwd varchar (1000));
create table categories (category varchar(1000));
create table acts (actId varchar(1000), username varchar(1000), time_stamp timestamp, caption varchar(1000), category varchar(1000)
	, imgB64 MEDIUMTEXT(1000), likes int);

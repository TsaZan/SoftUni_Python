create table minions(
    id int primary key ,
    name varchar(30),
    age integer
);

alter table minions rename to minions_info ;


alter table minions_info
add column code   char(4),
add column task   text,
    add column salary numeric(8, 3);


alter table minions_info
    rename column salary to banana;

alter table minions_info
    add column email    varchar(20),
    add column equipped boolean not null;


create type type_mood as enum ('happy', 'relaxed', 'stressed', 'sad');
alter table minions_info
    add column mood type_mood;

alter table minions_info
alter column age set default 0,
    alter column name set default ' ',
    alter column code set default ' ';


alter table minions_info
add constraint unique_containt
unique (id, email),
    add constraint banana_check
check ( banana > 0 );


alter table minions_info
alter column task type varchar(150);






create table jockey(
  jockey_code varchar(8) not null,
  kana varchar(32)  null,
  name varchar(32)  null,
  bday datetime null,
  license_year int null,
  sozoku varchar(16) null
)
;
create unique index idx_jockey on jockey(jockey_code)
;


create table trainer(
  trainer_code varchar(8) not null,
  kana varchar(32) null,
  name varchar(32) null,
  bday datetime null,
  license_year int null,
  syozoku varchar(16) null
)
;
create unique index idx_trainer on trainer(trainer_code)
;

 


create table jockey(
  jockey_code varchar(5) not null,
  kana varchar(16)  null,
  name varchar(16)  null,
  bday datetime null,
  license_year int null,
  sozoku varchar(8) null
)
;
create unique index idx_jockey on jockey(jockey_code)
;


create table trainer(
  trainer_code varchar(5) not null,
  kana varchar(16) null,
  name varchar(16) null,
  bday datetime null,
  license_year int null,
  syozoku varchar(8) null
)
;
create unique index idx_trainer on trainer(trainer_code)
;

create table race(
  race_code varchar(10) not null,
  date datetime null,
  raceno int null,
  basyo varchar(8) null,
  hasso varchar(5) null,
  grade varchar(2) null,
  baba varchar(8) null,
  mawari varchar(4) null,
  kyori int null,
  sarakei varchar(16) null,
  racetype varchar(32) null,
  racekinryo varchar(8) null,
  syokin1 int null,
  syokin2 int null,
  syokin3 int null,
  syokin4 int null,
  syokin5 int null,
  tenki varchar(8) null,
  turf varchar(8) null
)
; 
create unique index idx_race on race(race_code)
;

create table seiseki(
  race_code varchar(10) not null,
  cyakujun int null,
  wakuban int null,
  umaban int null,
  uma_code varchar(10) null,
  sei varchar(4) null,
  rei int null,
  jockey_code varchar(5) null,
  racetime float null,
  cyakusa varchar(16) null,
  tuka1 int null,
  tuka2 int null,
  tuka3 int null,
  tuka4 int null,
  agari float null,
  kinryo float null,
  bataiju float null,
  zogen float null,
  ninki int null,
  odds float null,
  blinker varchar(4) null,
  trainer_code varchar(5) null
)
;
create unique index idx_seiseki on seiseki(race_code)
;

create table harai(
  race_code varchar(10) not null,
  syubetsu varchar(8) not null,
  umaban1 int null,
  umaban2 int null,
  umaban3 int null,
  harai int null,
  ninki int null
)
;
create unique index idx_harai on harai(race_code,syubetsu)
;
;





create table odds_tanfuku(
  race_code varchar(10) not null,
  wakuban int null,
  umaban int not null,
  uma_code varchar(10) null,
  tan float null,
  fuku_low float null,
  fuku_upp float null
)
;
create unique index idx_odds_tanfuku on odds_tanfuku(race_code,umaban)
;

create table odds_waku(
  race_code varchar(10) not null,
  wakuban1 int not null,
  wakuban2 int not null,
  odds float null
)
;
create unique index idx_odds_waku on odds_waku(race_code,wakuban1,wakuban2)
;


create table odds_umaren(
  race_code varchar(10) not null,
  umaban1 int not null,
  umaban2 int not null,
  odds float null
)
;
create unique index idx_odds_umaren on odds_umaren(race_code,umaban1,umaban2)
;



create table odds_umatan(
  race_code varchar(10) not null,
  umaban1 int not null,
  umaban2 int not null,
  odds float null
)
;
create unique index idx_odds_umatan on odds_umatan(race_code,umaban1,umaban2)
;


















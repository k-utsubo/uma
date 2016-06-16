#!/bin/sh


mysql -ukeiba -hlocalhost --local-infile=1 keiba << Eof
load data local infile "data/harai_data.txt" into table harai
;
load data local infile "data/jockey.txt" into table jockey
;
load data local infile "data/race_data.txt" into table race
;
load data local infile "data/seiseki_data.txt" into table seiseki
;
load data local infile "data/trainer.txt" into table trainer
;
Eof


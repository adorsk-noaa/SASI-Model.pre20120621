#!/bin/bash

tmp_sql_file="$$.tmp.sql"

cat raw_vtr_for_year.sql | sed "s/{{YEAR}}/$1/g" > $tmp_sql_file;

sqldump -u $2/$3 -d 'YYYY-MM-DD HH:MI:SS' -v -c -f $tmp_sql_file -o raw_vtr_$1 

rm $tmp_sql_file;

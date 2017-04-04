CREATE TEMP TABLE tmp_table AS SELECT * FROM patho.tbl_labpat WITH NO DATA;
COPY tmp_table FROM '/home/registro/Escritorio/RAMELLI/scripts/texto_plano/registro.csv' DELIMITER '|' CSV HEADER;
INSERT INTO patho.tbl_labpat SELECT * FROM tmp_table t1
where not exists
(select id_tblpat from patho.tbl_labpat t2 
where t2.id_tblpat=t1.id_tblpat);
DROP TABLE tmp_table;
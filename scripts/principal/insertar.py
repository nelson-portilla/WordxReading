# -*- coding: utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf8')
import extraccion as extraer
import getempty as getempty
import progressBar as progress
import docx
global matriz 
import glob
from time import time
matriz=[]

##METODO QUE CARGA EL ARCHIVO.SQL QUE CONTIENE EL COPY EL CUAL INSERTA DATOS A UNA TABLA DESDE UN SCV
def insertar(main_folder):
	try:
		csv=os.popen("echo | psql -U postgres -h 192.168.216.21 -d RegistroCancerBD -f "+main_folder+"/scripts/sql_scripts/insertarFROMcsv.sql").read()
	except Exception, e:
		print "Ha fallado la insercion: error general",str(e)
		sys.exit(1)

def consultar_secuencia(main_folder):
	csv=os.popen("echo | psql -U postgres -h 192.168.216.21 -d RegistroCancerBD -f "+main_folder+"/scripts/sql_scripts/query_sequence.sql").read()
	return csv.split('\n')[2].strip()

##METODO PARA ESCRIBIR LA MATRIZ EN UN ARCHIVO SCV
def escribirCSV(main_folder):
	global matriz
	# print "MATRIZ: ",len (matriz)
	
	reg=open(main_folder+"/scripts/texto_plano/registro.csv", 'w')	
	for idx, linea in enumerate(matriz):
		if idx==len(matriz)-1:
			if(isinstance(linea, basestring)):
				reg.write("|".join(linea))
			else:
				#print "Entro: ", linea
				#print "index", idx
				#print "Tamanno", len(matriz)
				reg.write("|".join(linea))				
		else:
			#print "index: ", idx
			reg.write("|".join(linea))
			reg.write("\n")
	

	reg.close()
	
	
	# print "==> Creando Archivo CSV ..OK"


##METODO PARA CREAR EL ARCHIVO SQL QUE CARGA EL CSV A LA BASE DE DATOS
def crearSQL(main_folder):
	archivo_csv=main_folder+"/scripts/texto_plano/registro.csv"
	ruta=main_folder+"/scripts/sql_scripts/insertarFROMcsv.sql"
	sql=open(ruta, 'w')
	texto="\COPY patho.tbl_labpat FROM '"+archivo_csv+"' DELIMITER '|' CSV HEADER;"
	
	##SE CREA LA CONSULTA
	# texto=("CREATE TEMP TABLE tmp_table AS SELECT * FROM patho.tbl_labpat WITH NO DATA;")
	# texto+="\n\COPY tmp_table FROM '"+archivo_csv+"' DELIMITER '|' CSV HEADER;"
	# # texto+="\nINSERT INTO muestra_html SELECT DISTINCT ON numeroregistro * FROM tmp_table;"
	# texto+=("\nINSERT INTO patho.tbl_labpat SELECT * FROM tmp_table t1"
	# 			"\nwhere not exists"
	# 			"\n(select id_tblpat from patho.tbl_labpat t2 "
	# 				"\nwhere t2.id_tblpat=t1.id_tblpat);")
	# texto+="\nDROP TABLE tmp_table;"
	sql.write (texto)
	texto=""



##CLASE PRINCIPAL
if __name__ == '__main__':
	matriz=[]
	##SE RECIBE LA RUTA DEL folder principal de los documentos en word
	folder_principal=str(sys.argv[1])
	##SE RECIBE LA RUTA DEL folder principal contenedor del folder scripts
	folder_main=sys.argv[2]

	# ##SE CREA UNA LISTA CON LOS SUBFILES
	subfiles_name=glob.glob(folder_principal+'/*')   
	tiempo_inicial = time()
	number=0
	totalArchivos=len(subfiles_name)
	objextraer = extraer.LecturaDOCX()
	val_sequence=int(consultar_secuencia(folder_main))+2
	for file in subfiles_name:
		#Se Lee el archivo
		if (sys.argv[3]=="0"):
			objextraer.extraerEntidades(file, int(val_sequence))
		else:
			objextraer.extraerEntidadesCito(file, int(val_sequence))
		val_sequence=objextraer.getUpdateValSequence()
		matriz=objextraer.getMatriz()

		escribirCSV(folder_main)
		##CREA EL ARCHIVO SQL CON LA CONSULTA PARA INSERTAR A TABLA IGNORANDO DUPLICADOS	
		crearSQL(folder_main)
		##EJECUTA LLAMADO AL SISTEMA PARA CARGAR ARCHIVO SQL CON CONSULTA DE INSERTAR
		insertar(folder_main)
		number+=1
	tiempo_final = time()
	tiempo_ejecucion = tiempo_final - tiempo_inicial
	print '\n- - El tiempo de ejecucion en segundos fue: - - > ',str(tiempo_ejecucion)+" seg" #En segundos
# -*- coding: utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf8')
import codecs
import docx
import re
import unicodedata
global jsonDatos, matriz, last_sequence
matriz=[]

pat = re.compile(r'\s+')
flag_acumular_diagnostico=False
count_lineas=0
jsonDatos= {'id_tblpat':"",
			'nobio':"",
			'fechabx':"",
			'cedula':"",
			'ape1':"",
			'ape2':"",
			'apec':"",
			'nom1':"",
			'nom2':"",
			'labbio':"",
			'recolector_':"",
			'link':"",
			'datesys':"",
			'fuente_recoleccion':"",
			'estado':"",
			'bdrpcc':"",
			'anexado':"",
			'recolector':"",
			'sexo':"",
			'edad':"",
			'cedula1':"",
			'cedula2':"",
			'fechainfo':"",
			'entidad':"",
			'diagnostico':""
			}



#Clase para leer el html, se obtienen solo el Data, se limpia y se arma la lista.
class LecturaDOCX():
	

	def inicializar(self):
		global jsonDatos		
		count_lineas=0
		jsonDatos= {'id_tblpat':"",
				'nobio':"",
				'fechabx':"",
				'cedula':"",
				'ape1':"",
				'ape2':"",
				'apec':"",
				'nom1':"",
				'nom2':"",
				'labbio':"",
				'recolector_':"",
				'link':"",
				'datesys':"",
				'fuente_recoleccion':"",
				'estado':"",
				'bdrpcc':"",
				'anexado':"",
				'recolector':"",
				'sexo':"",
				'edad':"",
				'cedula1':"",
				'cedula2':"",
				'fechainfo':"",
				'entidad':"",
				'diagnostico':""
				}

	def crearMatriz(self):		
		global matriz
		matriz=[[None] * 25 for i in range(1)]
		matriz[0][0]="id_tblpat"
		matriz[0][1]="nobio"
		matriz[0][2]="fechabx"
		matriz[0][3]="cedula"
		matriz[0][4]="ape1"
		matriz[0][5]="ape2"
		matriz[0][6]="apec"
		matriz[0][7]="nom1"
		matriz[0][8]="nom2"
		matriz[0][9]="labbio"
		matriz[0][10]="recolector_"
		matriz[0][11]="link"
		matriz[0][12]="datesys"
		matriz[0][13]="fuente_recoleccion"
		matriz[0][14]="estado"
		matriz[0][15]="bdrpcc"
		matriz[0][16]="anexado"
		matriz[0][17]="recolector"
		matriz[0][18]="sexo"
		matriz[0][19]="edad"
		matriz[0][20]="cedula1"
		matriz[0][21]="cedula2"
		matriz[0][22]="fechainfo"
		matriz[0][23]="entidad"
		matriz[0][24]="diagnostico"
		# print matriz
		self.crearFila()

	def crearFila(self):
		global matriz, jsonDatos
		if jsonDatos["nobio"]!='':
			fila=[]
			for item in matriz[0]:
				fila.append(jsonDatos[item])		
			matriz.append(fila)

	def extraerEntidades(self,ruta_archivo, val_sequence):
		global jsonDatos, last_sequence
		last_sequence=val_sequence
		doc = docx.Document(ruta_archivo)
		fullText = []
		nombres=[]
		count_lineas=0
		numero_parrafos=len(doc.paragraphs)
		self.crearMatriz()
		for i in range(0,numero_parrafos):
			if doc.paragraphs[i].text=="":
				# print "**",jsonDatos				
				last_sequence+=1
				self.crearFila()
				self.inicializar()
				count_lineas=0

			elif(count_lineas<4):				
				count_lineas+=1
				linea=doc.paragraphs[i].text.strip().split(":")
				if linea[0].strip()=="NOMBRE":
					jsonDatos['id_tblpat']=str(last_sequence)
					self.extraerNombre_Documento(linea)
				elif linea[0].strip()=="REF.":
					self.extraer_ref_edad_sexo_codigo(linea)
				elif linea[0].strip()=="MEDICO":
					self.extraer_medico_fechrecibido(linea)
				elif linea[0].strip()=="ENTIDAD":
					count_lineas=4
					self.extraer_entidad_fechinfo(linea)

			elif (count_lineas==4):
				self.extraer_diagnostico(doc.paragraphs[i].text.strip())


			

	def extraerNombre_Documento(self, listanombre):
		lista_palabras=pat.sub(' ', listanombre[1]).split(" ")
		if len(lista_palabras)==5:
			jsonDatos['nom1']=lista_palabras[0]
			jsonDatos['nom2']=lista_palabras[1]
			jsonDatos['ape1']=lista_palabras[2]
			jsonDatos['ape2']=lista_palabras[3]
		elif len(lista_palabras)==4:
			jsonDatos['nom1']=lista_palabras[0]
			jsonDatos['ape1']=lista_palabras[1]
			jsonDatos['ape2']=lista_palabras[2]
		elif len(lista_palabras)==3:
			jsonDatos['nom1']=lista_palabras[0]
			jsonDatos['ape1']=lista_palabras[1]
		elif len(lista_palabras)>5:
			jsonDatos['nom1']=lista_palabras[0]
			jsonDatos['nom2']=lista_palabras[1]
			jsonDatos['ape1']=lista_palabras[2]
			jsonDatos['apec']=lista_palabras[3]
			jsonDatos['ape2']=lista_palabras[4]
		jsonDatos['cedula']=listanombre[2]
		

	def extraer_ref_edad_sexo_codigo(self, listaref):	
		jsonDatos['nobio']=pat.sub(' ', listaref[1].strip()).split(" ")[0]
		jsonDatos['edad']=pat.sub(' ', listaref[2].strip()).split(" ")[0]
		sexo=pat.sub(' ', listaref[3].strip()).split(" ")[0]
		if sexo=="M":
			jsonDatos['sexo']=str(1)
		else:
			jsonDatos['sexo']=str(2)

			
		
	def extraer_medico_fechrecibido(self, listamedico):
		jsonDatos['fechabx']=pat.sub(' ', listamedico[2].strip()).split(" ")[0]
	
	def extraer_entidad_fechinfo(self, listaentidad):		
		jsonDatos['entidad']=pat.sub(' ', listaentidad[1].strip()).replace('FECH.INFO','').replace('FECHA','').strip()
		jsonDatos['fechainfo']=pat.sub(' ', listaentidad[2].strip()).split(" ")[0]

	def extraer_diagnostico(self, listadiag):
		jsonDatos['diagnostico']+=self.elimina_tildes(str(listadiag).strip())

	def getMatriz(self):
		return matriz

	def getUpdateValSequence(self):
		global last_sequence
		return last_sequence

	def elimina_tildes(self, cadena):
		s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
		return s.decode()

if __name__ == '__main__':
	None
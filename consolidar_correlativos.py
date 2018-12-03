import pandas as pd
import glob
import os
import os.path
import tkinter.filedialog, re

pasos=7

#AGREGARLE UN BUSCADOR DE CARPETA DONDE ESTARÁN LOS ARCHIVOS.
root = tkinter.Tk()
root.withdraw()
file_path = tkinter.filedialog.askdirectory()


print('')
print('Paso 1 de '+str(pasos)+'- Borrando consolidado anterior')
if os.path.isfile("consolidado_correlativos.csv"):
    os.remove("consolidado_correlativos.csv")

archivostxt=[]

os.chdir(file_path)
for file in glob.glob("*.txt"):
    archivostxt.append(file)

#archivostxt=glob.glob("*.txt")

print('Paso 2 de '+str(pasos)+'- Leyendo archivos')

archivos_correlativos=[]
for i in archivostxt:
	archivos_correlativos.append(pd.read_csv(i,encoding='latin1',sep=';', low_memory=False))

print ('             Hay un total de '+str(len(archivos_correlativos))+' archivos')
#extraer los primeros 3 caracteres del nombre
print('Paso 3 de '+str(pasos)+'- Extrayendo codigos')
codigos=[]
for i in range(0,len(archivostxt)):
	codigos.append(str(archivostxt[i][0:3]))

#pegar los primeros 3 caracteres del nombre en la ultima columna de cada archivo

print('Paso 4 de '+str(pasos)+'- Escribiendo codigos')
for j in range(0,len(archivos_correlativos)):
    archivos_correlativos[j].loc[0,"SERVICIO"]=""
    print('             Servicio: '+str(codigos[j]))
    for i in range(0, len(archivos_correlativos[j])):
        archivos_correlativos[j].loc[i,"SERVICIO"]=codigos[j]


print('Paso 5 de '+str(pasos)+'- Concatenando archivos')

#consolid a
consolidado=pd.concat(archivos_correlativos)
consolidado=pd.concat(archivos_correlativos).reset_index(drop = True)


#creo que aca pongo la ultima columna en la primera posicion
cols = [consolidado.columns[-1]] + [col for col in consolidado if col != consolidado.columns[-1]]
consolidado = consolidado[cols]

print ('Paso 6 de '+str(pasos)+'- Grabando Archivo')
consolidado.to_csv('consolidado_correlativos.csv', encoding='latin1',index=False)

print('Paso 7 de '+str(pasos)+'- Archivo listo')


input()

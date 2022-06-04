import pyperclip
import os

def es_funcion(palabras_clave, instruccion):
    for i in palabras_clave:
        if i in instruccion:
            return True
            break

#archivo = open('test.TXT','r')
#contenido = archivo.read()
#archivo.close()

salida = ''

def tabular():

    global salida

    pyperclip.waitForNewPaste()
    contenido = pyperclip.paste()

    if contenido != salida:
                    
        caracter_asignacion = str(' := ') # Esto es un comentario
        caracter_comentario = str(' // ') # Comentarios
        contenido_con_comentarios = list()
        asignaciones_tabuladas = list()
        contenido_partido = list()
        contenido_sin_comentarios = list()
        contenido_tabulado_comentarios = ''
        lista_caracteres1 = list() 
        lista_caracteres2 = list()
        caracteres_1 = 0
        caracteres_2 = 0
        salida = ""
        aux = 0
        palabras_reservadas = ('IF', 'ELSE', 'FOR', 'WHILE', 'END_IF', 'END_FOR', 'END_WHILE')

        contenido = contenido.splitlines()

        for i in contenido:

            contenido_con_comentarios.append(i.partition(caracter_comentario))

        for i in contenido:

            contenido_sin_comentarios.append(i.partition(caracter_comentario)[0])

        for i in contenido_sin_comentarios:  

            contenido_partido.append(i.partition(caracter_asignacion))  

        for i in contenido_partido:  

            if i[1] != '':

                if (len(i[0]) > caracteres_1):
                    caracteres_1 = len(i[0])

            else:

                lista_caracteres1.append(caracteres_1)
                caracteres_1 = 0

        lista_caracteres1.append(caracteres_1)

        for i in contenido_partido:

            if i[1] != '':

                if len(i[2]) > caracteres_2:

                    caracteres_2 = len(i[2])

            else:

                lista_caracteres2.append(caracteres_2)
                caracteres_2 = 0

        lista_caracteres2.append(caracteres_2)

        for i in contenido_partido:

            if i[1] != '' or es_funcion(palabras_reservadas, i[0]):

                asignaciones_tabuladas.append(str(i[0]).ljust(lista_caracteres1[aux]) + str(i[1]).center(len(str(i[1]))+0) + (str(i[2]).lstrip()).rjust(lista_caracteres2[aux]))

            else:

                asignaciones_tabuladas.append(str(i[0]) + "\n")
                aux += 1

        for i in range(len(contenido_con_comentarios)):

            contenido_tabulado_comentarios = contenido_tabulado_comentarios + (asignaciones_tabuladas[i]+contenido_con_comentarios[i][1]+contenido_con_comentarios[i][2]) + "\n"

        '''---------------------------------------------------'''

        contenido = contenido_tabulado_comentarios.splitlines()

        contenido_partido = list()

        for index,i in enumerate(contenido):

            tmp = i.partition(caracter_comentario)
            
            if len(tmp[1]) > 0 and tmp[0] == '' :

                siguiente_linea = contenido[index+1]

                for j, letra in enumerate(siguiente_linea):
                    if letra != ' ':
                        break

                contenido_partido.append((j*' ' + tmp[1][1:len(tmp[1])-1] + ' ' + tmp[2], '', ''))
            else:
                contenido_partido.append(tmp)  

        for i in contenido_partido:

            if (len(i[0]) > caracteres_1):
                caracteres_1 = len(i[0])

        lista_caracteres1.append(caracteres_1)

        for i in contenido_partido:

            if len(i[2]) > caracteres_2:

                caracteres_2 = len(i[2])

        for index,i in enumerate(contenido_partido):

            if (i[1] != ''):

                if index != len(contenido_partido)-1:
                    salida = salida + (str(i[0]).ljust(caracteres_1) + str(i[1]).center(len(str(i[1]))+4) + (str(i[2]).lstrip()).ljust(caracteres_2) + "\r\n")
                else:
                    salida = salida + (str(i[0]).ljust(caracteres_1) + str(i[1]).center(len(str(i[1]))+4) + (str(i[2]).lstrip()).ljust(caracteres_2))

            else:

                if index < len(contenido_partido)-1:
                    salida = salida + str(i[0]) + "\r\n"
                else:
                    salida = salida + str(i[0])

                aux += 1
        
        pyperclip.copy(salida)

def formato_codigo():

    pyperclip.waitForNewPaste()
    txt = pyperclip.paste()

    # Quito espacios innecesarios
    txt = " ".join(txt.split())

    nots = txt.count("NOT")
    espacio_not = 0

    if nots > 0:
        espacio_not = 4

    # Añado ; al final de la instrucción, en el caso de que no la tenga y compruebo que el string donde se pone la instrucción no esté vacia
    try:
        if (txt[-1]) != ";":
            txt += ";"
    except IndexError:
        print("La cadena de caracteres donde se introduce la instrucción está vacía")
    exit

    # Separo operación en líneas.

    txt = txt.replace(")","\n)")
    txt = txt.replace("AND","\nAND")
    txt = txt.replace("OR","\nOR ")
    txt = txt.splitlines()

    # Tabulo los parentesis

    aux = list()
    aux.append(0)
    nParentesis = 0

    for i in range(len(txt)):
        txt[i] = aux[(len(aux)-1)-nParentesis]*" " + txt[i]
        if txt[i].find("(") != -1:
            aux.append(txt[i].find("("))
        if txt[i].find(")") != -1:
            nParentesis += 1

    # Extraigo variables del texto inicial

    split = list()

    for i in txt:

        if i.find("(") != -1:
            i = i.replace("OR", "  ")
            i = i.replace("AND ", "   ")
            txt_split = i.split("(")
            split.append(txt_split)
        else:
            if i.find("AND") != -1:
                txt_split = i.split("AND")
                split.append(txt_split)
            else:
                if i.find("OR") != -1:
                    txt_split = i.split("OR")
                    split.append(txt_split)


    variables = list()

    for i in split:
        variables.append(i[1].strip())

    # Obtengo posición desde la cual tiene que empezar el nombre de la variable para 

    PosInicio = 0

    for linea in txt:
        for variable in variables:
            if linea.find(variable) != -1:
                if (linea.find(variable)) > PosInicio:
                    PosInicio = linea.find(variable)

    # Tabulo las variables

    for i, linea in enumerate(txt):
        for variable in variables:
            if linea.find(variable) != -1:
                if not("NOT" in linea):
                    txt[i] = (linea.replace(variable, ((PosInicio - linea.find(variable)+espacio_not))*" "+variable))
                else:
                    txt[i] = (linea.replace(variable, (PosInicio - linea.find(variable))*" "+variable))

    # Uno todas las lineas para obtener la operación con el formato deseado

    res = "\r\n".join(txt)
       
    pyperclip.copy(res)

def main():

    descripcion = ""

    print("Seleccione la acción que quiera realizar")
    accion = int(input("1: Tabular código\n2: Dar formato operación lógica\nAcción: "))
    print("Copie el texto a modificar")

    if accion == 1:
        tabular()
        descripcion = "tabulado"
    
    if accion == 2:
        formato_codigo()
        descripcion = "formateado"

    os.system("cls") # Limpia consola

    print(f'El texto {descripcion} ha sido copiado al clipboar')
    input()

if __name__ == "__main__":

    main()

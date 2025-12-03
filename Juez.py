import re

#Regex:
DIGITOS = r"[0-9]"
VOCAL = r"[AEIOUaeiou]"
VOCAL_ACENTUADA = r"[ÁÉÍÓÚáéíóú]"
VOCALES = rf"(?:{VOCAL}|{VOCAL_ACENTUADA})"
LETRAS = r"[A-Za-zÑñ]"
GUION = r"-"
STRING = rf"(?:{VOCALES}|{LETRAS}|{GUION})+"
CARACTERES_PERMITIDOS = r"[¿?¡!,.; '\-\(\):\"]"
PALABRA = rf"(?:{STRING}|{CARACTERES_PERMITIDOS}|{DIGITOS})+"


#Funciones: 
def validacion_sintax(estrofa, n, narchivo):    
    """"
    flag: booleano
    Retorna booleano
    Esta función hace match por cada verso de una estrofa con la regex PALABRA, retorna False en caso de que haya un caracter no permitido
    n es la n-ésima estrofa que está siendo evaluada en un archivo (será ocupado más adelante)
    """
    flag = True
    for verso in estrofa:
        valido = re.fullmatch(PALABRA, verso)
        if not valido:
            narchivo.write(f"Estrofa {n}: Inválida"+"\n")
            flag = False
            break
    return flag

def validacion_largo(listadeestrofa, n, narchivo):
    """
    Se entrega una lista que contiene los versos de una estrofa y si el largo de ésta es distinto de 4 retorna False
    n es la n-ésima estrofa que está siendo evaluada en un archivo (será ocupado mas adelante)
    """
    flag =  True
    if len(listadeestrofa) !=4:
            narchivo.write(f"Estrofa {n}: Inválida"+"\n")
            flag = False
    return flag
def quitar_tilde(palabra):
    palabra = palabra.lower()
    if re.search("á", palabra):
        palabra = re.sub("á", "a", palabra)
    if re.search("é", palabra):
        palabra = re.sub("é", "e", palabra)
    if re.search("í", palabra):
        palabra = re.sub("í", "i", palabra)
    if re.search("ó", palabra):
        palabra = re.sub("ó", "o", palabra)
    if re.search("ú", palabra):
        palabra = re.sub("ú", "u", palabra)
    if re.search("-", palabra):
        palabra = re.sub("-", "", palabra)
    return palabra

def extraerpalabras(listaversos):
    """
    Extrae la ultima palabra de cada verso, pero solo su parte string. Si contiene algun carácter como "?", lo quita del substring.
    """
    listpalabras=[]
    for verso in listaversos:
        palabras = re.findall(STRING, verso)
        if re.search(VOCAL_ACENTUADA, palabras[-1]) or re.search(GUION, palabras[-1]):
            listpalabras.append(quitar_tilde(palabras[-1]))
        else:
            listpalabras.append(palabras[-1])
    return listpalabras
    
def sufijocomun(p1, p2):
    """
    Extrae el máximo sufijo en común entre 2 palabras. Retorna string vacío en caso de que no haya.
    Se hace un while que vaya extrayendo el sufijo máximo de derecha a izquierda.
    """
    i = 0
    coincidencia = ""
    while i < min(len(p1),len(p2)):
        sufijo = p1[len(p1)-(i+1):]
        regex = re.compile(sufijo + r"$")  #el $ hace que se haga match al final del string, fuente: https://docs.python.org/es/3.13/library/re.html
        if re.search(regex, p2):
            coincidencia = sufijo
        else:
            break
        i += 1
    return coincidencia
            
def es_asonante(palabra1,palabra2):
    """
    Calcula los puntos que obtendria una rima asonante entre dos palabras.
    Retorna None en caso de que no exista rima asonante.
    """  
    vocales1 = "".join(re.findall(VOCALES, palabra1)).lower()      #evita que no se reconocan mayusculas
    vocales2 = "".join(re.findall(VOCALES, palabra2)).lower()      #Es cierto que se pudo verificar si hay mayusculas con regex también, por ejemplo un search con alguna regex de Mayusculas, pero .lower() era más compacto.
    puntos = 0
    if len(sufijocomun(vocales1, vocales2))>0:
        sufijo = sufijocomun(vocales1, vocales2)
        vocalescomunes = len(sufijo)
        if vocalescomunes == 1:
                puntos = 3
        elif vocalescomunes ==2:
                puntos = 4
        elif 3<=vocalescomunes and sufijocomun(palabra1,palabra2)!= palabra1:     #evita el caso que sean iguales
                puntos = 8
        return puntos
    
def es_consonante(palabra1, palabra2):
    """
    Calcula los puntos que obtendria una rima consonante entre dos palabras.
    Retorna None en caso de que no exista rima consonante.
    """  
    puntos = 0
    comun = sufijocomun(palabra1,palabra2) or ""                   #Se debió agregar el "or" debido a errores con None
    if comun:
        if 3<=len(comun)<=4:
            puntos = 5
        elif 5<= len(comun) and sufijocomun(palabra1,palabra2)!= palabra1:     #evita el caso que sean iguales:
            puntos = 8
    return puntos
def es_gemela(palabra1, palabra2):
    """
    Calcula los puntos de una rima gemela entre dos palabras.
    """
    regex = re.compile(palabra1)
    puntos = 0
    if re.fullmatch(regex, palabra2):
        puntos = 1
    return puntos
def es_mismaterminacion(palabra1, palabra2):
    """
    Calcula los puntos de una rima con misma terminación entre dos palabras.
    """
    comun = sufijocomun(palabra1,palabra2)
    puntos = 0
    if len(comun) == 2:
        puntos = 2
    return puntos

def validacion_(estrofas, regexb, archivo2):
    """
    Función principal que calcula la calificación de cada estrofa y sus rimas correspondientes.
    Se hace un ciclo anidado para por cada palabra final, se recorren las siguientes que falten.
    """
    for k , estrofa in enumerate(estrofas):
        rimasEncontradas = []
        puntaje = 0
        flag1 = True
        flag2 = True
        nohayrimas = False
        for verso in estrofa:
            flag1 = validacion_sintax(verso,k+1, archivo2)
            if flag1 == False:
                break
            flag2 = validacion_largo(estrofa,k+1,archivo2)
            if flag2 == False:
                break
        if flag1 and flag2:
            palabras = extraerpalabras(estrofa)

            i=0
            while i<4:
                j = i+1
                while j<4:
                    pGemelas = es_gemela(palabras[i], palabras[j]) or 0
                    pMismaterminacion = es_mismaterminacion(palabras[i], palabras[j]) or 0         #tuve que usar or 0, porque retornaba None en vez de 0 en los casos en que no encontraba alguna de estas rimas.
                    pAsonante = es_asonante(palabras[i], palabras[j]) or 0
                    pConsonante =es_consonante(palabras[i], palabras[j]) or 0
                    if pGemelas >0:
                        if "gemela" not in rimasEncontradas:
                            rimasEncontradas.append("gemela")
                        puntaje += pGemelas
                    elif max(pAsonante,pConsonante, pGemelas, pMismaterminacion) == pAsonante and pAsonante>0:
                        if "asonante" not in rimasEncontradas:
                            rimasEncontradas.append("asonante")
                        puntaje += pAsonante
                    elif max(pAsonante,pConsonante, pGemelas, pMismaterminacion) == pConsonante and pAsonante>0:
                        if "consonante" not in rimasEncontradas:
                            rimasEncontradas.append("consonante")  
                        puntaje += pConsonante   
                    elif max(pAsonante,pConsonante, pGemelas, pMismaterminacion) == pMismaterminacion and pMismaterminacion>0:
                        if "misma terminación" not in rimasEncontradas:
                            rimasEncontradas.append("misma terminación")
                        puntaje += pMismaterminacion
                    else:
                        nohayrimas = True
                    j+=1
                i+=1
            if nohayrimas:
                puntaje-=2
            flag_bonus = False
            for palabra in palabras:
                if re.search(regexb, palabra):
                    flag_bonus = True
            if flag_bonus:
                puntaje +=2
            score = round(puntaje/5 , 1)
            if flag_bonus:
                escrito = "Estrofa "+f"{k+1}: "+str(score)+"/10 (BONUS)"
                archivo2.write(escrito+"\n")
                archivo2.write("Rimas: ")
                result= ", ".join(rimasEncontradas)
                archivo2.write(result)
            else:
                escrito = "Estrofa "+f"{k+1}: "+str(score)+"/10"
                archivo2.write(escrito+"\n" )
                archivo2.write("Rimas: ")
                result= ", ".join(rimasEncontradas)
                archivo2.write(result)
                #print(rimasEncontradas)
            archivo2.write("\n")

def main():
    archivo = open("estrofas.txt", "r", encoding="utf-8")
    lista_estrofas =[]
    lista_versos =[]
    palabras_bonus = []
    CONTADOR_LINEA = 0

    for linea in archivo:
        if CONTADOR_LINEA == 0:
            palabras_bonus = linea.strip().split(", ")
        elif linea.strip() != "":
            lista_versos.append(linea.strip(",\n"))
        else:
            if CONTADOR_LINEA>2:
                lista_estrofas.append(lista_versos)
                lista_versos = []
        CONTADOR_LINEA +=1
    lista_estrofas.append(lista_versos)  #agrega la ultima estrofa que falta
    archivo.close() 
    
    regexBonus = r"(" + "|".join(palabras_bonus) + r")"
    decisiones = open("decision.txt","w", encoding="utf-8")
    validacion_(lista_estrofas, regexBonus, decisiones)
    decisiones.close()

if __name__ == "__main__":
    main()
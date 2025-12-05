import re

DIGITOS = r"[0-9]"
VOCAL = r"[AEIOUaeiou]"
VOCAL_ACENTUADA = r"[ÁÉÍÓÚáéíóú]"
VOCALES = rf"(?:{VOCAL}|{VOCAL_ACENTUADA})"
LETRAS = r"[A-Za-zÑñ]"
GUION = r"-"
STRING = rf"(?:{VOCALES}|{LETRAS}|{GUION})+"
CARACTERES_PERMITIDOS = r"[¿?¡!,.; '\-\(\):\"]"
PALABRA = rf"(?:{STRING}|{CARACTERES_PERMITIDOS}|{DIGITOS})+"

"""
Funcion: es_vacia (bool)
Parametros: string 
Funcionamiento: retorna true si la linea es "\n", si no, false.
"""
def es_vacia(linea):
    if linea == "\n":
        return True
    else:
        return False
"""
Funcion: guardar (lista de strings)
Parametros: archivo txt 
Funcionamiento: Va guardando cada linea no vacía excepto las palabras especiales 
"""
def guardar(archivo):
    lineas = archivo.readlines() 
    listlineas = []
    for linea in lineas: 
        if (not es_vacia(linea)):
            listlineas.append(re.sub("\n","",linea))
    return listlineas
"""
Funcion: makeEstrofas(lista de listas)
Parametros: lista de strings (versos) 
Funcionamiento: va agrupando los la palabra final de cada verso de cada estrofa 
    en sublistas de a 4 (estrofas) 
    - si encuentro una coma en la palabra final se la quito en la parte if re.search(",")
"""
def makeEstrofas(listaVersos):
    cont = 1 
    listaEstrofas = []
    estrofaActual = []
    while cont < len(listaVersos):  
        estrofaActual.append(listaVersos[cont])
        if (cont)%4 == 0:
            listaEstrofas.append(estrofaActual)
            estrofaActual = []
        cont += 1
    return listaEstrofas
"""
Funcion: extraerPalabras
Parámetros: lista de strings
Funcionamiento: saca las palabras finales
"""
def extraerPalabras(estrofaActual):
    j = 0
    listaPalabras = []
    while j < len(estrofaActual):
        versoActual = estrofaActual[j]
        versoSeparado = versoActual.split()
        palabraFinal = versoSeparado[-1]
        if re.search("," , palabraFinal):
            palabraFinal = re.sub("," , "", palabraFinal)
        if re.search("á", palabraFinal):
            palabraFinal = re.sub("á", "a", palabraFinal)
        if re.search("é", palabraFinal):
            palabraFinal = re.sub("é", "e", palabraFinal)
        if re.search("í", palabraFinal):
            palabraFinal = re.sub("í", "i", palabraFinal)
        if re.search("ó", palabraFinal):
            palabraFinal = re.sub("ó", "o", palabraFinal)
        if re.search("ú", palabraFinal):
            palabraFinal = re.sub("ú", "u", palabraFinal)
        if re.search("-", palabraFinal):
            palabraFinal = re.sub("-", "", palabraFinal)
        if re.search(CARACTERES_PERMITIDOS, palabraFinal):
            lis = re.findall(STRING, palabraFinal)
            palabraFinal = ""
            for sub in lis:
                palabraFinal += sub
        
        listaPalabras.append(palabraFinal)
        j += 1
    return listaPalabras
"""
Funcion: palabrasBonus
Parametros: lista de strings
Funcionamiento: es como makeEstrofas pero solo saca la 0
"""
def palabrasBonus(listaVersos):
    strPalabras = listaVersos[0]
    lista = []
    listaPalabras = strPalabras.split()
    for palabraFinal in listaPalabras:
        if re.search("," , palabraFinal):
            palabraFinal = re.sub("," , "", palabraFinal)
        if re.search("á", palabraFinal):
            palabraFinal = re.sub("á", "a", palabraFinal)
        if re.search("é", palabraFinal):
            palabraFinal = re.sub("é", "e", palabraFinal)
        if re.search("í", palabraFinal):
            palabraFinal = re.sub("í", "i", palabraFinal)
        if re.search("ó", palabraFinal):
            palabraFinal = re.sub("ó", "o", palabraFinal)
        if re.search("ú", palabraFinal):
            palabraFinal = re.sub("ú", "u", palabraFinal)
        if re.search("-", palabraFinal):
            palabraFinal = re.sub("-", "", palabraFinal)
        lista.append(palabraFinal)
    return lista

"""
Funcion: validarEstrofas
Parametros: estrofa (lista de strings) 
Funcionamiento: valida si caracteres invalidos 
"""
def validarEstrofas(estrofa):
    for verso in estrofa:
        if not re.fullmatch(PALABRA, verso) :
            return False
    return True
"""
Funcion: sufijoComun 
Parametros: 2 palabras  
Funcionamiento: retorna el sufijo maximo entre dos palabras
"""
def sufijoComun(palabra1, palabra2):
    i = 0
    coincidencia = ""
    while i < min(len(palabra1), len(palabra2)):
        sufijo1 = palabra1[(len(palabra1)-1)-i : ]
        sufijo2 = palabra2[(len(palabra2)-1)-i : ]
        regex = re.compile(sufijo1)
        if regex.fullmatch(sufijo2):
            coincidencia = sufijo1 
        else:
            break
        i += 1
    return coincidencia
"""    
Funcion: vocales 
Parametros: 1 palabra 
Funcionaminto: para "cancion " retornaria "aio"
"""
def vocales(palabra):
    i = 0
    soloVocales = ""
    while i < len(palabra):
        car = palabra[i]
        if re.match(VOCALES, car):
            soloVocales += car
        i += 1
    return soloVocales
"""
Funcion: rimas
ID's
11 = consonante, 3 a 4 letras, 5pts
12 = consonante, 5 o más letras, 8pts
21 = asonante, 1 letra, 3pts
22 = asonante, 2 letra, 4pts
3 = asonante, 3 letras o más, 8pts
3 = misma terminacion, 2 letras, 2pts
4 = palabra igual, 1pt
0 = no rima
"""
def rimas(palabra1, palabra2):
    palabra1def = palabra1.lower()
    palabra2def = palabra2.lower()
    if palabra1def == palabra2def:
        print("+1pts")
        return 4
    sufComun = sufijoComun(palabra1def,palabra2def) 
    vocales1 = vocales(palabra1def)
    vocales2 = vocales(palabra2def)
    vocalesComun = sufijoComun(vocales1, vocales2) 
    if 3 <= len(sufComun) <= 4 and re.search(VOCALES, sufComun) and re.search(LETRAS, sufComun) and len(vocalesComun) <= 2:
        print("+5pts")
        return 11
    elif 5 <= len(sufComun) and re.search(VOCALES, sufComun) and re.search(LETRAS, sufComun) :
        print("+8pts")
        return 12
    elif len(vocalesComun) == 1:
        print("+3pts")
        return 21
    elif len(vocalesComun) == 2:
        print("+4pts")
        return 22
    elif 3 <= len(vocalesComun):
        print("+8pts")
        return 23
    elif 2 <= len(sufComun):
        print("+2pts")
        return 3
    else:
        print("+0pts")
        return 0


def main():
    archivo = open("rimas.txt", "r", encoding="utf-8")
    versos = guardar(archivo)
    estrofas = makeEstrofas(versos)
    bonus = palabrasBonus(versos)
    e = 0
    while e < len(estrofas):
        valida = validarEstrofas(estrofas[e])
        puntos = 0
        rimasEncontradas = []
        if not valida:
            print("Estrofa "+str(e)+": Inválida")
        else:
            palabrasFinales = extraerPalabras(estrofas[e])
            for pal in palabrasFinales:
                if pal in bonus:
                    puntos += 2
                    print("BONUS en estrofa "+str(e+1))
                    break
            i = 0
            while i < 4:
                j = i + 1
                while j < 4:
                    categoria = rimas(palabrasFinales[i],palabrasFinales[j])
                    if categoria == 11:
                        puntos += 5
                        if "consonante" not in rimasEncontradas:
                            rimasEncontradas.append("consonante")
                    elif categoria == 12:
                        puntos += 8
                        if "consonante" not in rimasEncontradas:
                            rimasEncontradas.append("consonante")
                    elif categoria == 21:
                        puntos += 3
                        if "asonante" not in rimasEncontradas:
                            rimasEncontradas.append("asonante")
                    elif categoria == 22:
                        puntos += 4
                        if "asonante" not in rimasEncontradas:
                            rimasEncontradas.append("asonante")
                    elif categoria == 23:
                        puntos += 8
                        if "asonante" not in rimasEncontradas:
                            rimasEncontradas.append("asonante")
                    elif categoria == 3:
                        puntos += 2
                        if "misma terminacion" not in rimasEncontradas:
                            rimasEncontradas.append("misma terminacion")
                    elif categoria == 4:
                        puntos += 1
                        if "gemela" not in rimasEncontradas:
                            rimasEncontradas.append("gemela")
                    j += 1
                i += 1
        e+=1
        calificacion = puntos/5 
        print("Estrofa "+str(e)+": "+str(calificacion))
        for ri in rimasEncontradas:
            print(ri)
    archivo.close()
    
if __name__ == "__main__":
    main()
    

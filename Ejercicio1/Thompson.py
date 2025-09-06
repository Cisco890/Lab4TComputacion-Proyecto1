#####################################################################################################
# Joel Antonio Jaquez López - 23369  y Juan Francisco Martínez - 2361                               #
# Laboratorio 4, Ejercicio 1 Algoritmo de Shunting Yard con arbol sintactico e implementación de AFN#
#####################################################################################################

import sys
import graphviz

# Defino una clase llamada NodoAST que sera la estructura basica de arbol
class NodoAST:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

# Clase que sirve para representar un estado del AFN
class Estado:
    def __init__(self, id_estado):
        self.id = id_estado
        self.es_final = False
        self.transiciones = {}
    
    # Con esta funcion puedo decir con que letra moverme a otro estado
    def agregar_transicion(self, simbolo, estado_destino):
        if simbolo not in self.transiciones:
            self.transiciones[simbolo] = []
        self.transiciones[simbolo].append(estado_destino)

# Caja principal donde guardo todo un autómata
class AFN:
    def __init__(self):
        self.estado_inicial = None
        self.estados_finales = []
        self.estados = []
        self.alfabeto = set()
        self.contador_estados = 0
    
    # Funcion que me permite crear nuevos estados
    def nuevo_estado(self):
        estado = Estado(self.contador_estados)
        self.contador_estados += 1
        self.estados.append(estado)
        return estado
    
    # Funcion que me permite agregar simbolos al alfabeto, a excepción de epsilon
    def agregar_simbolo(self, simbolo):
        if simbolo != 'ε' and simbolo != '𝜀':
            self.alfabeto.add(simbolo)

# Clase para representar el estado del AFD
class EstadoAFD:
    def __init__(self, id_estado, conjunto_estados_afn):
        self.id = id_estado
        # Para comparar IDs
        self.conjunto_afn = frozenset(estado.id for estado in conjunto_estados_afn)
        self.estados_afn = conjunto_estados_afn
        self.es_final = any(estado.es_final for estado in conjunto_estados_afn)
        self.transiciones = {}
    
    def agregar_transicion(self, simbolo, estado_destino):
        self.transiciones[simbolo] = estado_destino
    
    def __repr__(self):
        return f"q{self.id}({sorted(self.conjunto_afn)})"

# Clase principal para el AFD
class AFD:
    def __init__(self):
        self.estado_inicial = None
        self.estados_finales = []
        self.estados = []
        self.alfabeto = set()
        self.contador_estados = 0
    
    def nuevo_estado(self, conjunto_estados_afn):
        estado = EstadoAFD(self.contador_estados, conjunto_estados_afn)
        self.contador_estados += 1
        self.estados.append(estado)

        if estado.es_final:
            self.estados_finales.append(estado)
        
        return estado

# La clase fragmento, permite definir el estado inicial y final del AFN
class FragmentoAFN:
    def __init__(self, estado_inicial, estado_final):
        self.inicio = estado_inicial
        self.fin = estado_final

# Funcion que permite leer un AST y contruir el AFN
def construir_thompson_afn(ast):
    if not ast:
        return None
        
    afn = AFN()

    def construir_fragmento(nodo):
        if not nodo:
            return None
            
        if nodo.valor not in ['|', '.', '*', '+', '?', '^']:
            inicio = afn.nuevo_estado()
            fin = afn.nuevo_estado()

            simbolo = nodo.valor
            if simbolo.startswith('\\'):
                simbolo = simbolo[1:]
                
            # Si es epsilon, crear transición vacía
            if simbolo == '𝜀' or simbolo == 'ε':
                inicio.agregar_transicion('ε', fin)
            else:
                afn.agregar_simbolo(simbolo)
                inicio.agregar_transicion(simbolo, fin)

            return FragmentoAFN(inicio, fin)
            
        elif nodo.valor == '.':
            frag_izq = construir_fragmento(nodo.izq)
            frag_der = construir_fragmento(nodo.der)

            frag_izq.fin.agregar_transicion('ε', frag_der.inicio)

            return FragmentoAFN(frag_izq.inicio, frag_der.fin)
            
        elif nodo.valor == '|':
            frag_izq = construir_fragmento(nodo.izq)
            frag_der = construir_fragmento(nodo.der)

            inicio = afn.nuevo_estado()
            fin = afn.nuevo_estado()

            inicio.agregar_transicion('ε', frag_izq.inicio)
            inicio.agregar_transicion('ε', frag_der.inicio)

            frag_izq.fin.agregar_transicion('ε', fin)
            frag_der.fin.agregar_transicion('ε', fin)

            return FragmentoAFN(inicio, fin)
            
        elif nodo.valor == '*':
            frag = construir_fragmento(nodo.izq)
            inicio = afn.nuevo_estado()
            fin = afn.nuevo_estado()

            # Transiciones epsilon
            inicio.agregar_transicion('ε', frag.inicio)
            inicio.agregar_transicion('ε', fin) 
            frag.fin.agregar_transicion('ε', frag.inicio) # Repetir
            frag.fin.agregar_transicion('ε', fin)        # Terminar
            
            return FragmentoAFN(inicio, fin)
            
        elif nodo.valor ==  '+':
            frag = construir_fragmento(nodo.izq)

            inicio = afn.nuevo_estado()
            fin = afn.nuevo_estado()

            # Para +, debe ejecutarse al menos una vez
            inicio.agregar_transicion('ε', frag.inicio)
            frag.fin.agregar_transicion('ε', frag.inicio) # Repetir
            frag.fin.agregar_transicion('ε', fin)        # Terminar
            
            return FragmentoAFN(inicio, fin)
            
        elif nodo.valor == '?':
            frag = construir_fragmento(nodo.izq)

            inicio = afn.nuevo_estado()
            fin = afn.nuevo_estado()

            inicio.agregar_transicion('ε', frag.inicio)  # Entrar al fragmento
            inicio.agregar_transicion('ε', fin)          # Saltar
            frag.fin.agregar_transicion('ε', fin)        # Terminar
            
            return FragmentoAFN(inicio, fin)
        
    fragmento_principal = construir_fragmento(ast)

    if fragmento_principal:
        afn.estado_inicial = fragmento_principal.inicio
        fragmento_principal.fin.es_final = True
        afn.estados_finales = [fragmento_principal.fin]
        
    return afn

def clausura_epsilon(estados, afn):
    clausura = set(estados)
    pila = list(estados)

    while pila:
        estado_actual = pila.pop()


        if 'ε' in estado_actual.transiciones:
            for estado_destino in estado_actual.transiciones['ε']:
                if estado_destino not in clausura:
                    clausura.add(estado_destino)
                    pila.append(estado_destino)
    return clausura

# Funcion para construccion de Subconjuntos
# Esta funcion implementa el algoritmo de construccion de subconjuntos para pasar de AFN a AFD
def construir_afd_subconjuntos(afn):
    if not afn or not afn.estado_inicial:
        return None
    
    print("\n=== CONSTRUCCIÓN DE SUBCONJUNTOS (AFN -> AFD) ===")
    afd = AFD()
    afd.alfabeto = afn.alfabeto.copy()

    # Paso 1: Estado inicial
    clausura_inicial = clausura_epsilon([afn.estado_inicial], afn)
    estado_inicial_afd = afd.nuevo_estado(clausura_inicial)
    afd.estado_inicial = estado_inicial_afd

    print (f"Estado Inicial del AFD: {estado_inicial_afd}")

    # Estructuras para el algoritmo
    estados_por_procesar = [estado_inicial_afd]
    conjuntos_visitados = {estado_inicial_afd.conjunto_afn: estado_inicial_afd}

    # Paso 2: Procesar cada estado el AFD
    while estados_por_procesar:
        estado_actual = estados_por_procesar.pop(0)
        print(f"\nProcesando estado: {estado_actual}")

        # Para cada simbolo del alfabeto
        for simbolo in afd.alfabeto:
            # Paso 3: Calcular el conjunto de estados alcanzables
            estados_destino = set()

            for estado_afn in estado_actual.estados_afn:
                if simbolo in estado_afn.transiciones:
                    for destino in estado_afn.transiciones[simbolo]:
                        estados_destino.add(destino)
            
            
            if estados_destino:
                # Paso 4: Calcular clausura epsilon del conjunto destino
                clausura_destino = clausura_epsilon(list(estados_destino), afn)
                conjunto_ids = frozenset(estado.id for estado in clausura_destino)

                # Verificar si este conjunto ya existe
                if conjunto_ids in conjuntos_visitados:
                    estado_destino_afd = conjuntos_visitados[conjunto_ids]
                
                else:
                    # Crear nuevo estado del AFD
                    estado_destino_afd = afd.nuevo_estado(clausura_destino)
                    conjuntos_visitados[conjunto_ids] = estado_destino_afd
                    estados_por_procesar.append(estado_destino_afd)
                    print(f"  Nuevo estado creado: {estado_destino_afd}")
                
                # Agregar transicion
                estado_actual.agregar_transicion(simbolo, estado_destino_afd)
                print(f"  Transición: {estado_actual} --{simbolo}--> {estado_destino_afd}")
        
    print(f"\n=== AFD CONSTRUIDO ===")
    print(f"Estados totales: {len(afd.estados)}")
    print(f"Estados finales: {len(afd.estados_finales)}")
    print(f"Alfabeto: {afd.alfabeto}")
    
    return afd

# Funcion de simulacion del AFD
def simular_afd(afd, cadena):
    if not afd or not afd.estado_inicial:
        return False
    
    estado_actual = afd.estado_inicial
    print(f"Estado inicial AFD: {estado_actual}")

    for i, simbolo in enumerate(cadena):
        if simbolo in estado_actual.transiciones:
            estado_actual = estado_actual.transiciones[simbolo]
            print(f"Después de '{simbolo}': {estado_actual}")
        else:
            print(f"No hay transición con '{simbolo}' desde {estado_actual}")
            return False
    
    # Verificar si el estado final es de aceptacion
    return estado_actual.es_final


def simular_afn(afn, cadena):
    if not afn or not afn.estado_inicial:
        return False
    
    estados_actuales = clausura_epsilon([afn.estado_inicial], afn)

    print(f"Estado inicial: {[e.id for e in estados_actuales]}")

    for i, simbolo in enumerate(cadena):
        nuevos_estados = set()

        for estado in estados_actuales:
            if simbolo in estado.transiciones:
                for estado_destino in estado.transiciones[simbolo]:
                    nuevos_estados.add(estado_destino)
        
        if nuevos_estados:
            estados_actuales = clausura_epsilon(list(nuevos_estados), afn)
        else:
            estados_actuales = set()
        print(f"Despues de '{simbolo}': {[e.id for e in estados_actuales]}")

        if not estados_actuales:
            return False
    
    for estado in estados_actuales:
        if estado.es_final:
            return True
        
    return False
    
def dibujar_afn(afn, nombre_archivo):
    if not afn:
        return
        
    dot = graphviz.Digraph(comment='AFN Thompson')
    dot.attr(rankdir='LR')
    dot.attr(ranksep='1.0')

    for estado in afn.estados:
        if estado.es_final:
            dot.node(str(estado.id), str(estado.id), shape='doublecircle')
        else:
            dot.node(str(estado.id), str(estado.id), shape='circle')

            # Marcar estado inicial con una flecha
    if afn.estado_inicial:
        dot.node('inicio', '', shape='none', width='0', height='0')
        dot.edge('inicio', str(afn.estado_inicial.id))
            
    # Agregar las transiciones
    for estado in afn.estados:
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                etiqueta = 'ε' if simbolo == 'ε' else simbolo
                dot.edge(str(estado.id), str(destino.id), label=etiqueta)

    dot.render(nombre_archivo, format='png', cleanup=True)
    print(f"AFN guardado como: {nombre_archivo}.png")

# Funcion para dibujar el AFD con Graphviz
def dibujar_afd(afd, nombre_archivo):
    if not afd:
        return
    
    dot = graphviz.Digraph(comment='AFD (Construcción de Subconjuntos)')
    dot.attr(rankdir='LR')
    dot.attr(ranksep='1.5')

    # Agregar los nodos
    for estado in afd.estados:
        # Etiqueta con el ID del estado AFD y los estados AFN que contiene
        etiqueta = f"q{estado.id}\\n{{{','.join(map(str, sorted(estado.conjunto_afn)))}}}"

        if estado.es_final:
            dot.node(str(estado.id), etiqueta, shape='doublecircle')
        else:
            dot.node(str(estado.id), etiqueta, shape='circle')

    # Marcar el estado inicial
    if afd.estado_inicial:
        dot.node('inicio_afd', '', shape='none', width='0', height='0')
        dot.edge('inicio_afd', str(afd.estado_inicial.id))
    
    # Agregar transiciones
    for estado in afd.estados:
        for simbolo, estado_destino in estado.transiciones.items():
            dot.edge(str(estado.id), str(estado_destino.id), label=simbolo)

    dot.render(nombre_archivo, format='png', cleanup=True)
    print(f"AFD guardado como: {nombre_archivo}.png")

# Funcion que se encargará de convertir el postfix en un árbol
def construir_AST(postfix):
    tokens = postfix.split()
    pila = []
    
    for token in tokens:
        # Para operadores binarios
        if token in ['|', '.', '^']:
            if len(pila) < 2:
                break
            der = pila.pop()
            izq = pila.pop()
            nodo = NodoAST(token, izq, der)
            pila.append(nodo)
        # Para operadores unarios
        elif token in ['*', '+', '?']:
            if len(pila) < 1:
                break
            hijo = pila.pop()
            nodo = NodoAST(token, hijo)
            pila.append(nodo)
        # Para los literales
        else:
            nodo = NodoAST(token)
            pila.append(nodo)
    
    # Solución para manejar pilas con múltiples elementos
    if len(pila) == 1:
        return pila[0]
    elif len(pila) > 1:
        # Si quedan múltiples elementos, crear un árbol con concatenación
        while len(pila) > 1:
            der = pila.pop()
            izq = pila.pop()
            nodo = NodoAST('.', izq, der)
            pila.append(nodo)
        return pila[0]
    else:
        return None

# Funcion para dibujar el arbol desde arriba hacia abajo 
def dibujar_ast(raiz, nombre_archivo):
    dot = graphviz.Digraph(comment='AST')
    dot.attr(rankdir='TB')
    dot.attr(ranksep='1.0')

    # Funcion recursiva para agregar los nodos empezando desde la raiz y comprobando si cada nodo tiene hijo izquierdo y derecho
    def agregar_nodos(nodo, contador=[0]):
        if not nodo:
            return None
        
        nodo_id = str(contador[0])
        contador[0] += 1

        etiqueta = 'ε' if nodo.valor == 'ε' else nodo.valor
        dot.node(nodo_id, etiqueta)

        if nodo.izq:
            izq_id = agregar_nodos(nodo.izq, contador)
            dot.edge(nodo_id, izq_id)

        if nodo.der:
            der_id = agregar_nodos(nodo.der, contador)
            dot.edge(nodo_id, der_id)

        return nodo_id

    agregar_nodos(raiz)
    dot.render(nombre_archivo, format='png', cleanup=True)
    print(f"Árbol guardado como: {nombre_archivo}.png")


# Primero defino una función que explica la precedencia de los opereadores
# Los más importantes son los que tienen un número mayor (es decir los de abajo)
def get_precedencia(c):
    if c == '(':
        return 1
    if c == '|':
        return 2
    if c == '.':
        return 3
    if c in ('?', '*', "+"):
        return 4
    if c == '^':
        return 5
    return 0

# Nueva función para transformar a + y ? en su forma basica
def transform_extension(regex):
    return regex



# Luego defino una función que se encarga de detectar y preservar los escapes para evitar confusiones
def format_regex(regex):
    # res corresponde a la nueva versión de la expresión con los puntos de concatenación
    res = []
    i = 0
    # Con este ciclo while se recorre la expresión caracter por caracter
    while i < len(regex):
        # Aquí tomo el carcter actual
        c1 = regex[i]
        # Y verifico si es una barra invertida y que este no sea el ultimo caracter de la cadena
        if c1 == '\\' and i + 1 < len(regex):
            # Añade los 2 caracteres como un único elemento
            res.append(regex[i:i+2])
            # Y se mueve 2 posiciones para saltar el escapado
            i += 2
            continue

        # Convertir operadores Unicode a ASCII
        if c1 == '∗':  # Unicode asterisk
            c1 = '*'
        elif c1 == '？':  # Unicode question mark
            c1 = '?'
        elif c1 == '＋':  # Unicode plus
            c1 = '+'

        # Y agrego c1 a res
        res.append(c1)
        # Luego compruebo que no estoy en lo último
        if i + 1 < len(regex):
            # Y sigo leyendo el caracter que viene
            c2 = regex[i+1]

             # Convertir c2 también si es Unicode
            if c2 == '∗':
                c2 = '*'
            elif c2 == '？':
                c2 = '?'
            elif c2 == '＋':
                c2 = '+'

            # Luego compruebo que c1 y c2 no estén entre lo definido para así concatenar bien separado por punto, sino solo lo agrego normal
            if (c1 not in {'(', '|'} and
                c2 not in {')', '|', '?', '*', '+', '^'} and
                c1 not in {'?', '*', '+'}):
                res.append('.')
        i += 1

    return ''.join(res)  

def infix_to_postfix(regex):
    # Lista output donde se guardarán los tokens en orden postfix
    output = []
    # Lista stack para guardar operadores
    stack = []

    # Primero transformar las extensiones (+ y ?) a su forma básica
    transformed = transform_extension(regex)
    # Luego formatear con puntos de concatenación
    formatted = format_regex(transformed)
    print(f"Infix original: {regex}")
    print(f"Transformado: {transformed}")
    print(f"Infix formateado: {formatted}\n") 

    # Con este ciclo for se recorre cada token de la cadena formateada y la va a mostrar
    for token in formatted:
        # Si es un literal lo mete directamente en el output
        if token.startswith('\\') or (token not in '|.()?*+^'):
            output.append(token)
            print(f" Salida ← {token} Pila: {stack}")
            continue
        
        # Operadores unarios postfix deben ir directo al output para atarse al operando previo
        if token in ('*', '+', '?'):
            output.append(token)
            print(f" Salida ← {token} (postfix) Pila: {stack}")
            continue
    
        # Si tengo un '(' lo apilo
        if token == '(':
            stack.append(token)
            print(f" Push '('  Pila: {stack}")
            continue
    
        # Si es ')' desapilo hasta llegar a '('
        if token == ')':
            while stack and stack[-1] != '(':
                op = stack.pop()
                output.append(op)
                print(f"Pop {op} →  Pila:  {stack}")
            stack.pop()
            print(f"Se descarta '('  Pila: {stack}")
            continue

        # Si es operador genérico calcula la precedencia del operador actual
        prec = get_precedencia(token)
        while stack and get_precedencia(stack[-1]) >= prec:
            op = stack.pop()
            output.append(op)
            print(f"Pop {op} (prec) →  Pila: {stack}")
        stack.append(token)
        print(f"Push '{token}'  Pila: {stack}")


    # Al final hay que vaciar la pila entera
    while stack:
        op = stack.pop()
        output.append(op)
        print(f"Pop final {op} → Pila: {stack}")
    
    postfix = ' '.join(output)
    print(f"\n Postfix resultante: {postfix}\n")

    print("Construyendo AST")
    ast = construir_AST(postfix)
    if ast:
        nombre_archivo = f"ast_linea_{regex.replace('*','_').replace('|','_').replace('(','').replace(')','').replace('?','_').replace('+','_')}"
        dibujar_ast(ast, nombre_archivo)

        print("Construyendo AFN con el algoritmo de Thompson...")
        afn = construir_thompson_afn(ast)

        if afn:
            nombre_afn = f"afn_linea_{regex.replace('*','_').replace('|','_').replace('(','').replace(')','').replace('?','_').replace('+','_')}"
            dibujar_afn(afn, nombre_afn)
            print(f"AFN construido con {len(afn.estados)} estados")
            print(f"Alfabeto: {afn.alfabeto}")

            # Contruccion de AFD con la construccion de subconjuntos
            print("Construyendo AFD con algoritmo de subconjuntos...")
            afd = construir_afd_subconjuntos(afn)

            if afd:
                nombre_afd = f"afd_linea_{regex.replace('*','_').replace('|','_').replace('(','').replace(')','').replace('?','_').replace('+','_')}"
                dibujar_afd(afd, nombre_afd)

            return afn, afd

    print()
    return None, None


# Funcion main que se encarga de verificar que se haya pasado el nombre del archivo como argumento
# También se encarga de comprobar que el archivo exista y que se pueda abrir
# Y lee línea por línea numerandolas y evitando lineas vacías, y para cada línea llama a procesar_linea()
def main():
    if len(sys.argv) != 2:
        print("Usar expresiones.txt")
        sys.exit(1)
    
    archivo = sys.argv[1]
    afns_generados = []
    afds_generados = []
    expresiones = []

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for idx, linea in enumerate(f, start=1):
                linea = linea.rstrip('\n')
                if not linea:
                    continue
                print(f"=== Línea {idx} ===")
                afn, afd =infix_to_postfix(linea)
                if afn:
                    afns_generados.append(afn)
                    afds_generados.append(afd)
                    expresiones.append(linea)
        
        if afns_generados:
            print("================")
            print("SIMULACION DE AUTOMATAS")
            print("================")

            while True:
                print("===== AUTOMATAS Disponibles ====")
                for i, expr in enumerate(expresiones, 1):
                    print(f"{i}. {expr}")
                print("0. Salir")

                try:
                    opcion = int(input("Selecciona el autómata a usar (numero): "))

                    if opcion == 0:
                        print("Gracias por probar la simulacion")
                        break
                    elif 1 <= opcion <= len(afns_generados):
                        afn_seleccionado = afns_generados[opcion - 1]
                        afd_seleccionado = afds_generados[opcion - 1]
                        expresion_seleccionada = expresiones[opcion - 1]

                        print(f"Simulando autómatas de {expresion_seleccionada}")
                        cadena = input("Escribe la cadena a evaluar: ")

                        #Simulacion del AFN
                        print("\n--- SIMULACIÓN AFN ---")
                        resultado_afn = simular_afn(afn_seleccionado, cadena)
                        respuesta_afn = "SI" if resultado_afn else "NO"
                        print(f"AFN: ¿'{cadena}' ∈ L({expresion_seleccionada})? {respuesta_afn}")


                        # SIMULACIÓN AFD
                        if afd_seleccionado:
                            print("\n--- SIMULACIÓN AFD ---")
                            resultado_afd = simular_afd(afd_seleccionado, cadena)
                            respuesta_afd = "SI" if resultado_afd else "NO"
                            print(f"AFD: ¿'{cadena}' ∈ L({expresion_seleccionada})? {respuesta_afd}")
                            
                            # Verificar que ambos dan el mismo resultado
                            if resultado_afn == resultado_afd:
                                print("✓ AFN y AFD dan el mismo resultado")
                            else:
                                print("✗ ERROR: AFN y AFD dan resultados diferentes")
                        
                    else:
                        print("Opción no válida. Intenta de nuevo")
                
                except ValueError:
                    print("Ingresa un numero valido")
                except KeyboardInterrupt:
                    print("\nSaliendo de la simulación")
                    break
        else:
            print("No se generaron AFNs validos.")

    except FileNotFoundError:
        print("No se encontro el archivo")
        sys.exit(1)

# Punto de entrada para correr el programa
if __name__ == "__main__":
    main()
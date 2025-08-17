# Lab4TComputacion

**Autores:** Joel Antonio Jaquez López (23369) y Juan Francisco Martínez (2361)  
**Curso:** Teoría de la Computación - UVG

## Descripción del Ejercicio 1

Implementación del **algoritmo de Thompson** para construir y simular Autómatas Finitos No deterministas (AFN) a partir de expresiones regulares.

## Funcionalidades Clave

### Construcción de AFN
- **Algoritmo de Thompson**: Construcción compositiva desde AST
- **Operadores soportados**: `*`, `+`, `?`, `|`, `.`, símbolos básicos
- **Fragmentos AFN**: Bloques reutilizables para cada operador
- **Transiciones epsilon**: Manejo automático del no-determinismo

### Simulación
- **Clausura epsilon**: Cálculo de estados alcanzables por ε
- **Simulación paso a paso**: Seguimiento de conjuntos de estados
- **Verificación**: Pertenencia de cadenas al lenguaje L(r)

### Visualización
- **Diagramas AFN**: Generación automática con Graphviz
- **Estados finales**: Marcados con doble círculo
- **Transiciones claras**: Símbolos y epsilon identificados

## Uso
Verificar instalaciones
```bash
pip install graphviz
```
Cómo correrlo
```bash
python Thompson.py expresiones.txt
```

**Ejemplo de simulación:**
```
Simulando AFN de (a*|b*)+
Escribe la cadena a evaluar: aab
Estado inicial: [0, 2]
Despues de 'a': [1, 3, 9, 11]
Despues de 'a': [1, 3, 9, 11]  
Despues de 'b': [5, 7, 9, 11]
¿'aab' ∈ L((a*|b*)+)? SI
```

## Algoritmo de Thompson

### Casos Básicos
- **Símbolo**: `inicio --'a'--> fin`
- **Epsilon**: `inicio --ε--> fin`

### Operadores
- **Unión (A|B)**: Estados inicial/final conectan ambas ramas
- **Concatenación (A.B)**: Final de A conecta con inicial de B
- **Kleene (A*)**: Permite cero o más repeticiones con ε
- **Positiva (A+)**: Una o más repeticiones (sin ε directo al final)
- **Opcional (A?)**: Puede saltarse con ε

## Expresiones del archivo .txt

1. `(a*|b*)+` - Una o más secuencias de a's o b's
2. `(ε|a)|b*)*` - Patrones con epsilon  
3. `(a|b)*abb(a|b)*` - Contiene subcadena "abb"
4. `0?(1?)?0*` - Secuencias numéricas opcionales

## Descripción del Ejercicio 2

Demostrar que el lenguaje A = {yy | y ∈ {0,1}*} NO es regular usando el Pumping Lemma.


## Enlace al video de Youtube

## Imágenes de los AFN por expresión regular
- (a∗|b∗)+: <img width="1298" height="383" alt="Image" src="https://github.com/user-attachments/assets/c38b10bf-8166-4911-96a1-2f4fbe46b844" />
- ((ε|a)|b∗)∗: <img width="1298" height="345" alt="Image" src="https://github.com/user-attachments/assets/cd2b19dc-7fa1-42e5-8e9e-cd8ae4adcf15" />
- (a|b)∗abb(a|b)∗: <img width="2410" height="248" alt="Image" src="https://github.com/user-attachments/assets/7bf48c9d-d773-48fa-827f-3d2d6bad5f69" />
- 0?(1?)?0∗: <img width="2169" height="164" alt="Image" src="https://github.com/user-attachments/assets/54f2beb6-e51a-4a04-b97a-74cabada2e14" />

---
**Universidad del Valle de Guatemala - 2025**

# Lab4TComputacion-Proyecto1
 Joel Antonio Jaquez López - 23369  y Juan Francisco Martínez - 23617                                          

## Librerías utilizadas

- **graphviz**: Para la visualización y generación de imágenes de los autómatas y árboles sintácticos.
- **sys**: Para la gestión de argumentos y entrada/salida estándar.


## Descripción

Este proyecto implementa la construcción y simulación de autómatas finitos a partir de expresiones regulares. Se incluyen los siguientes algoritmos y funcionalidades:

- **Shunting Yard**: Convierte expresiones regulares infix a postfix.
- **Thompson**: Construye un AFN (Autómata Finito No Determinista) desde el árbol sintáctico.
- **Subconjuntos**: Convierte el AFN en un AFD (Autómata Finito Determinista).
- **Minimización**: Reduce el AFD a su forma mínima.
- **Simulación**: Permite evaluar cadenas en los autómatas generados.


## Flujo del programa

1. **Lectura de expresiones**: El programa lee expresiones regulares desde un archivo (`expresiones.txt`).
2. **Conversión a postfix**: Utiliza el algoritmo Shunting Yard para convertir la expresión a notación postfix.
3. **Construcción del AST**: Genera el árbol sintáctico de la expresión.
4. **Construcción de AFN**: Aplica el algoritmo de Thompson para crear el AFN.
5. **Construcción de AFD**: Utiliza el método de subconjuntos para obtener el AFD.
6. **Minimización de AFD**: Aplica el algoritmo de particionamiento para minimizar el AFD.
7. **Visualización**: Genera imágenes PNG de los autómatas y el AST usando Graphviz.
8. **Simulación**: Permite al usuario seleccionar un autómata y evaluar cadenas para verificar si son aceptadas.

## Ejemplo de expresión

### Expresión: `0?(1|ε)?0*`

#### 1. Árbol Sintáctico (AST)

Se genera un árbol que representa la estructura de la expresión, mostrando la precedencia y agrupación de los operadores.

#### 2. AFN (Thompson)

El AFN resultante tiene transiciones epsilon y permite aceptar cadenas que cumplen con la expresión regular.

#### 3. AFD (Subconjuntos)

El AFD elimina las transiciones epsilon y representa el autómata de manera determinista.

#### 4. AFD Minimizado

El AFD minimizado reduce el número de estados, manteniendo el mismo lenguaje aceptado.

#### 5. Visualizaciones

El programa genera los siguientes archivos PNG:

-  Árbol sintáctico de la expresión.
- <img width="316" height="733" alt="image" src="https://github.com/user-attachments/assets/8cda8115-e4af-4514-a4f5-44bb1587703d" />

-  AFN construido.
- <img width="1687" height="137" alt="image" src="https://github.com/user-attachments/assets/f305fa37-074b-46ff-82ad-2be70d11f1ad" />

-  AFD generado.
-  <img width="1678" height="586" alt="image" src="https://github.com/user-attachments/assets/688775e9-86e1-45bd-97ca-e3ac5f59eacf" />

-  AFD minimizado.
-  <img width="827" height="203" alt="image" src="https://github.com/user-attachments/assets/92f8ad13-3bc3-45fa-8ad3-79874f002cd3" />


#### 6. Simulación

Puedes simular cadenas como:

- `"0"` → Aceptada
- `"01"` → Aceptada
- `"1"` → Aceptada
- `"000"` → Aceptada
- `"10"` → No aceptada

El programa muestra si la cadena pertenece al lenguaje definido por la expresión y compara los resultados entre AFN, AFD y AFD minimizado.

---

## Ejecución

1. Coloca tus expresiones regulares en `expresiones.txt`, una por línea.
2. Ejecuta el programa principal:

```powershell
python Ejercicio1/Proyecto1.py Ejercicio1/expresiones.txt
```

3. Sigue las instrucciones en pantalla para simular cadenas y visualizar los autómatas.

---

## Enlace al video de Youtube
https://youtu.be/d124eMaWTfY

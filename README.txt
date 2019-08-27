# fichador_amaimon
A partir de verbos dados, recupera fichas automáticamente de los corpus de la RAE: CORDE y CREA.

AMAIMON 2.0
Software para la recuperación automática de datos.

El objetivo de este programa es recuperar fichas de manera automática desde los corpus de la RAE: el CORDE y el CREA. El proceso se lleva a cabo a partir de verbos, es decir, el programa recupera oraciones en las que los verbos pedidos aparecen.

Amaimon fue creado con el propósito de facilitar la tarea de recolección de datos a los lingüistas, para que puedan dedicar más tiempo al análisis. Asismimo, permite recuperar grandes cantidades de datos rápidamente, y obtener muestras más pequeñas de los mismos, con lo que facilita la realización de estudios tanto cuantitativos como cualitativos.

Requerimientos:
Selenium
Requests
Chrome Driver

Proceso:

El programa solicita al usuario que introduzca verbos en infinitivo, separados por coma.

Cada verbo es buscado dentro del DLE para obtener su paradigma verbal.

Con los paradigmas verbales se crea un diccionario que vincula un lema con un paradigma flexivo.

Posteriormente, cada palabra flexionada es buscada en el corpus. Con el objetivo de que la búsqueda sea completa, se buscan tanto las formas con minúsculas (pensé) como aquellas con la primera letra capitalizada (Pensé).

Dado que el programa fue creado en el marco del proyecto de la Base de Datos de Construcciones Verbales en el Español Mexicano (UNAM / IIFL), el programa busca de manera predeterminada los datos en el CREA, solo para México, en el periodo comprendido entre 1980 y 2004, y tomando en cuenta solo medios impresos: Libros, Revistas y Periódicos. Estos parámetros pueden ser modificados en Amaimon como parte de la función Páginas (Ver abajo).

Si la búsqueda arroja más de 1000 datos, estos son filtrados con el filtro DOCUMENTOS que ofrece la RAE.

Posteriormente, el programa colecta los URLs de las distintas páginas de resultados.

Con la ayuda de expresiones regulares, Amaimon identifica las palabras buscadas dentro del código fuente de las páginas de resultados, y recolecta la oración en la que se encuentran (a través de la identificación de puntos), así como tres oraciones antes y tres oraciones después.

Además del contexto, el programa recolecta toda la meta-información que ofrece el corpus: año de publicación, autor, título, país, tema y publicación.

Cuando todos los datos están recolectados, si son menos de 2000, se aleatorizan y se impren en un archivo CSV. Cuando son más de 2000 datos, se toma una muestra aleatoria de 2000 datos.

La aleatorización tiene como objetivo que el investigador pueda trabajar solo con una parte de los datos reduciendo el sesgo de tener más ejemplos de una forma verbal que de otra. Por su parte, obtener una muestra cuando hay más de 2000 datos, tiene como propósito que el investigador cuente con una cantidad de datos más manejable de la que puede, a su vez, obtener muestras más pequeñas.

PARÁMETROS DE LA FUNCIÓN PÁGINAS

Valores posibles en Corpus:
corpus = 
"0"> CREA
"1"> CORDE

Valores posibles en Medio:
medio = 
"1000">(Todos)
"0"> Libros
"1"> Periódicos
"2"> Revistas
"3"> Miscelánea
"4"> Oral

Valores posibles en País:
pais = 
"1000">(Todos)
"0">Argentina
"1">Bolivia
"2">Chile
"3">Colombia
"4">Costa Rica
"5">Cuba
"6">Ecuador
"7">El Salvador
"8">EE.UU.
"9">España
"10">Filipinas
"11">Guatemala
"12">Honduras
"13">México
"14">Nicaragua
"15">Panamá
"16">Paraguay
"17">Perú
"19">Puerto Rico
"20">Rep. Dominicana
"21">Uruguay
"22">Venezuela

Los valores numéricos se pueden introducir solos o entre comillas:

pais = 0
pais = "0"

Para hacer búsquedas con múltiples valores en País o Medio (SIEMPRE ENTRECOMILLADO):

medio = "0&medio=1&medio=2" > Selecciona los valores 0 (Libros), 1 (Periódicos) y 2 (Revistas) en Medio.

Los parámetros de año (ano1 y ano2) son AMBOS NECESARIOS, y deben corresponder con el tipo de corpus. CORDE: desde el s. XII hasta el año 1974. CREA: desde 1975 hasta 2004.

Para recuperar ejemplos de un lapso diferente al comprendido entre 1980 y 2004:

ano1 = 1700, ano2 = 1850 

Para recuperar ejemplos de UN SOLO AÑO en específico:

ano1 = 1982, ano2 = "" 

Para NO seleccionar NINGÚN AÑO en específico ambos valores deben aparecer como:

ano1 = "", ano2 = ""

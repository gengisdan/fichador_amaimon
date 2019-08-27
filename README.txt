# fichador_amaimon
A partir de verbos dados, recupera fichas automáticamente de los corpus de la RAE: CORDE y CREA.

Amaimon 2.0
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

Dado que el programa fue creado en el marco del proyecto de la Base de Datos de Construcciones Verbales en el Español Mexicano (UNAM / IIFL), el programa busca de manera predeterminada los datos en el CREA, solo para México, en el periodo comprendido entre 1980 y 2004, y tomando en cuenta solo medios impresos: Libros, Revistas y Periódicos. Estos parámetros pueden ser modificados como parte de la función Páginas.

Si la búsqueda arroja más de 1000 datos, estos son filtrados con el filtro DOCUMENTOS que ofrece la RAE.

Posteriormente, el programa colecta los URLs de las distintas páginas de resultados.

Con la ayuda de expresiones regulares, Amaimon identifica las palabras buscadas dentro del código fuente de las páginas de resultados, y recolecta la oración en la que se encuentran (a través de la identificación de puntos), así como tres oraciones antes y tres oraciones después.

Además del contexto, el programa recolecta toda la meta-información que ofrece el corpus: año de publicación, autor, título, país, tema y publicación.

Cuando todos los datos están recolectados, si son menos de 2000, se aleatorizan y se impren en un archivo CSV. Cuando son más de 2000 datos, se toma una muestra aleatoria de 2000 datos.

La aleatorización tiene como objetivo que el investigador pueda trabajar solo con una parte de los datos reduciendo el sesgo de tener más ejemplos de una forma verbal que de otra. Por su parte, obtener una muestra cuando hay más de 2000 datos, tiene como propósito que el investigador cuente con una cantidad de datos más manejable de la que puede, a su vez, obtener muestras más pequeñas.

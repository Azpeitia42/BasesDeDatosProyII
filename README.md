# Proyecto Bases de Datos P. II

## Descripción

Esta aplicación gráfica en Python permite administrar un blog utilizando MongoDB como base de datos. Facilita la gestión de artículos, usuarios, comentarios, categorías y etiquetas, proporcionando una interfaz intuitiva para realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar).

## Esquema de la Base de Datos

La base de datos sigue un esquema que organiza la información del blog en las siguientes colecciones:

- **users**: Almacena información de los usuarios del blog, como nombre y correo electrónico.
- **articles**: Contiene los artículos del blog, incluyendo el título, la fecha y el contenido del texto.
- **comments**: Representa los comentarios en los artículos, almacenando el nombre del comentarista y una URL opcional.
- **tags**: Etiquetas asociadas a los artículos, con campos de nombre y URL.
- **categories**: Categorías de los artículos, también con campos de nombre y URL.

Cada artículo puede tener múltiples categorías y etiquetas, mientras que los comentarios están asociados a artículos específicos y los usuarios pueden ser autores de varios artículos.

## Uso de la Aplicación

1. **Conexión a MongoDB**: Configura la conexión a la base de datos en el archivo de configuración o en el código fuente, especificando la URL y el nombre de la base de datos.
2. **Interfaz de Usuario**: Al iniciar la aplicación, aparecerá una ventana gráfica donde puedes realizar las siguientes acciones:
   - **Crear**: Agrega nuevos usuarios, artículos, comentarios, etiquetas o categorías.
   - **Leer**: Consulta y visualiza el contenido existente en la base de datos.
   - **Actualizar**: Modifica la información existente, como el contenido de un artículo o los detalles de un usuario.
   - **Eliminar**: Elimina entradas específicas de la base de datos.

3. **Operaciones CRUD**: La aplicación permite realizar todas las operaciones CRUD sobre cada colección del esquema, con una interfaz fácil de usar.

## Autores

Oswaldo Valles Azpeitia 358430
Emily Abril Vazquez Moreno 357623
Angelica Torres Velderrein 359628

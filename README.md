## Estructura del proyecto

El proyecto está organizado en **tres carpetas principales**:

- **`src/`**
  Contiene la API que provee las alertas originales (fuente de datos). Se le agrego una carpeta .env para no exponer la api-key.

- **`ingestor/`**  
  Implementa la lógica para obtener los datos desde `src` y almacenarlos en la base de datos. También contiene un archivo .env con la api-key y credenciales de la bbdd.
  Incluye dos modelos principales:  
  - **Users**: almacena los usuarios y su `score`.  
  - **Alerts**: almacena el historial de alertas, se le agrego la columna user_id.  

- **`web/`**  
  Expone APIs y pequeños frontends para consultar la información persistida en la base de datos.  
  También incluye un archivo `.env` con las credenciales de conexión a la base de datos.  

## Endpoints disponibles

- **`http://localhost:8000/`**  
  Front simple donde se ingresa un email y devuelve el **score** del usuario.  

- **`http://localhost:8000/user-alerts`**  
  Front donde se ingresa un email y devuelve todas las **alertas asociadas** a ese usuario.  

- **`http://localhost:8000/api/users`**  
  Endpoint sin frontend, devuelve un **JSON con la lista de usuarios** de la tabla `Users`.  

## Importante
Las tres carpestas (scr, ingestor y web) necesitan un archivo .env para poder levantar las credenciales segun corresponda,
dejo env.dist en cada carpeta para tener de referencia.
Las credenciales de la bbdd tambien deben completarse en el docker-compose.

## Instrucciones de ejecucion 
Entrar en la carpeta principal y ejecutar docker-compose up --build, esto va a levantar la bbdd y todos los servicios (ingestor, web y src) en 4 contenedores distintos.

## Notas
Lo ideal es dejar que termine de ejcutar **`ingestor`** para obtener toda la data y luego usar **`http://localhost:8000/api/users`** para obtener algun email.
Con ese email pueden usar cualquiera de las dos apis

Cree la segunda tabla (Alerts) para poder obtener info relacionada con las alertas, ya que se podria estudiar el tipo de alerta. De ser necesario se podria hacer un foreing key en la columna user_id y asi poder tener relacionadas las dos.


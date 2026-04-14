# Tarea 1 Bases de Datos - Grupo 22
## Integrantes: 
  * Diego Álvarez - 23645318
  * Sofía Guzmán - 24641367
  * Joaquín Toro - 24641316

## Instrucciones para levantar la aplicación
1. Instalar las variables de entorno mencionadas a continuación
2. Levantar la base de datos en pgAdmin4 corriendo el archivo schema.sql y luego data.sql
3. Navegar en la terminal hasta la carpeta app de la carpeta tarea1
4. Correr el comando py app.py (o su equivalente en otros sistemas operativos)


## Variables de entorno necesarias
* 'DB_HOST' = 'localhost'
* 'DB_PORT' = 5432
* 'DB_USER' = 'postgres'
* 'DB_PASSWORD' = 'postgres'
* 'DB_NAME' = 'tarea1'

## Suposiciones
* En el punto 3.7 del enunciado (Requerimientos del cliente en relación a sponsors), asumimos que el enunciado se refiere a que el monto que un sponsor aporta a c/torneo es un valor constante del sponsor. Es decir, un sponsor x siempre aportará un monto idéntico x$ a cada torneo que auspicie. Esto se ve en el atributo monto de la tabla sponsors.

# PyPactia
Paquete para el cosumo de información de CRM y Ecosistema de Datos de Pactia

# Instalación
Antes de poder instalar **PyPactia** también es necesario contar con *GIT* qué es un software para el manejo de versiones en el desarrollo de software y similares. En el siguiente link se puede descargar:

[Descarga GIT](https://github.com/git-for-windows/git/releases/download/v2.36.1.windows.1/Git-2.36.1-64-bit.exe)

Para la instalación se debe correr el siguiente comando en python:
```python
pip install git+https://github.com/Pactia/PyPactia
```

# CRM
_____________________________________________________________________

## Loggin a la plataforma

Para poder traer información del CRM es necesario ingresar usuario y contraseña, para eso es necesario utilizar la función **inicio_crm()** cómo se muestra a continuación, la función le pedirá que ingrese las credenciales de acceso:

```python
from ayudantes.crm import crm_ayudantes

con = crm_ayudantes.inicio_crm()
```

También mediante la función de la siguiente manera:

```python
from ayudantes.crm import crm_ayudantes

con = crm_ayudantes.inicio_crm(usuario, contraseña)
```

Otra opción para hacer el loggin a la plataforma CRM es generar una tupla que contenga las variables de la siguiente manera:

```python
con = (usuario,contraseña)
```

## Acceder a información

**crm_tables(con):** Esta función lista las tablas del CRM disponibles para utilizar. Esta permite identificar los nombres para poder ser utilizadas en las dos funciones posteriores dónde la tabla es un parametro. 

```python
from ayudantes.crm import crm_ayudantes

crm_ayudantes.crm_tables(con=con)
```

**read_crm(tabla, página, con):** Con esta función es posible realizar la consulta de los registros en una de las tablas del CRM en una página específica, su principal uso podría ser para realizar un primer acercamiento a la información sin consumir memoria cargando la tabla completa con la información.

```python
from ayudantes.crm import crm_ayudantes

crm_ayudantes.read_crm(tabla, página, con=con)
```

**complete_crm(tabla, con):** Esta función se encarga de traer a python la totalidad de los registros de la tabla que se le especifique.

```python
from ayudantes.crm import crm_ayudantes

crm_ayudantes.complete_crm(tabla, con=con)
```

# Ecosistema de Datos
_____________________________________________________________________

Para poder conectarse al **Ecosistema de Datos** es necesario previamente tener instalado en el computador los drivers, si no los ha instalado se puede hacer en el siguiente link:

[Descarga Drivers](https://go.microsoft.com/fwlink/?linkid=2186919)


## Loggin a la plataforma

Para poder establecer la conexión entre el Ecosistema y el notebook de python es necesario hacer el loggeo a la plataforma, esto se realiza de la siguiente manera:

```python
from ayudantes.ecosistema import eco_ayudantes as eco

eco.conection_eco()
```

Otra opción es:

```python
from ayudantes.ecosistema import eco_ayudantes as eco

eco.conection_eco(usuario,contraseña)
```

## Acceder a información

**complete_eco()** Esta función genera la tabla completa con la información de rentas contenida en el ecosistema, no requiere ningún argumento, solo con llamarla se genera la tabla de información.

```python
from ayudantes.ecosistema import eco_ayudantes as eco

eco.complete_eco()
```


**filtered_eco(year=años, month=meses)** Con esta función se cargará la tabla de rentas del ecosistema pero filtrada por un periodo de tiempo especificado, usando cualquiera de los dos parametros (ambos o solo uno) **year** o **month** se puede seleccionar el periodo de tiempo deseado para el análisis. Pueden especificarse varios años o meses, a continuación se presenta en los ejemplos:

#### Solo un periodo de tiempo

```python
from ayudantes.ecosistema import eco_ayudantes as eco

#Solo arrojará los resultados de enero de 2021
eco.filtered_eco(year='2021', month='1')
```

#### Periodos de tiempo más amplios

```python
from ayudantes.ecosistema import eco_ayudantes as eco

#Arrojará la información de los 4 primeros meses de 2021
eco.filtered_eco(year='2021', month='1, 2, 3, 4')
```

```python
from ayudantes.ecosistema import eco_ayudantes as eco

#Arrojará la información de los años 2021 y 2022 para todos los meses
eco.filtered_eco(year='2021,2022')
```

```python
from ayudantes.ecosistema import eco_ayudantes as eco

#Arrojará la información de enero en todos los años disponibles
eco.filtered_eco(month='1')
```

# PyPactia
Paquete para el cosumo de información de CRM y Ecosistema de Datos de Pactia

# Instalación
Para la instalación se debe correr el siguiente comando en python:
```python
pip install git+https://github.com/Pactia/PyPactia
```

## CRM

Para poder traer información del CRM es necesario ingresar usuario y contraseña, para eso es necesario utilizar la función **inicio_crm()** cómo se muestra a continuación, la función le pedirá que ingrese las credenciales de acceso:

```python
from ayudantes.crm import crm_ayudantes

user, key = crm_ayudantes.inicio_crm()
```

**crm_tables():** Esta función lista las tablas del CRM disponibles para utilizar. Esta permite identificar los nombres para poder ser utilizadas en las dos funciones posteriores dónde la tabla es un parametro. 

```python
from ayudantes.crm import crm_ayudantes

crm_ayudantes.crm_tables()
```

**read_crm(tabla, página):** Con esta función es posible realizar la consulta de los registros en una de las tablas del CRM en una página específica, su principal uso podría ser para realizar un primer acercamiento a la información sin consumir memoria cargando la tabla completa con la información.

```python
from ayudantes.crm import crm_ayudantes

crm_ayudantes.read_crm(tabla, página)
```

**complete_crm(tabla):** Esta función se encarga de traer a python la totalidad de los registros de la tabla que se le especifique.

```python
from ayudantes.crm import crm_ayudantes

crm_ayudantes.complete_crm(tabla)
```

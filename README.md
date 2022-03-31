# PyPactia
Paquete para el cosumo de información de CRM y Ecosistema de Datos de Pactia

# Instalación
Para la instalación se debe correr el siguiente comando en python:
```python
pip install git+https://github.com/Pactia/PyPactia
```
#Ayudantes disponibles
## CRM
**odata_tables():** Esta función lista las tablas del CRM disponibles para utilizar. Esta permite identificar los nombres para poder ser utilizadas en las dos funciones posteriores dónde la tabla es un parametro. 

```python
pip install git+https://github.com/Pactia/PyPactia
```

**read_odata(tabla, página):** Con esta función es posible realizar la consulta de los registros en una de las tablas del CRM en una página específica, su principal uso podría ser para realizar un primer acercamiento a la información sin consumir memoria cargando la tabla completa con la información.

```python
pip install git+https://github.com/Pactia/PyPactia
```

**complete_odata(tabla):** Esta función se encarga de traer a python la totalidad de los registros de la tabla que se le especifique.

```python
pip install git+https://github.com/Pactia/PyPactia
```

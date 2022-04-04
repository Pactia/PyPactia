import pyodbc
import pandas as pd
import getpass

class eco_ayudantes:

    consulta="""
    
    """
    
    
    consulta_filtro= """

    """


    estructura="""WITH CTE AS (SELECT * ,CAST(SkEstructuraProductoPadre AS VARCHAR(MAX))  + ',' + CAST(CAST(SkEstructuraProducto AS VARCHAR(MAX)) AS VARCHAR(MAX)) AS IdListTopDown ,CAST(Linea AS varchar(MAX)) AS NameList 
    FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto]     
    WHERE SkEstructuraProductoPadre IS NULL UNION ALL SELECT t.* ,CAST(c.IdListTopDown AS VARCHAR(MAX)) + ',' + CAST(CAST(t.SkEstructuraProducto AS VARCHAR(MAX)) AS VARCHAR(MAX)) ,CAST(c.NameList + ' | ' + t.Linea AS varchar(MAX)) 
    FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto] AS t JOIN CTE c ON c.SkEstructuraProducto = t.SkEstructuraProductoPadre ) SELECT  CTE.SkEstructuraProducto, CTE.NameList FROM  CTE 
    WHERE NOT EXISTS(SELECT * FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto] WHERE SkEstructuraProductoPadre=CTE.SkEstructuraProducto) 
    ORDER BY CTE.IdListTopDown
    """
    
    
    ingreso="""WITH CTE AS (SELECT * ,CAST(SkTipoIngresoPadre AS VARCHAR(MAX))  + ',' + CAST(CAST(SkTipoIngreso AS VARCHAR(MAX)) AS VARCHAR(MAX)) AS IdListTopDown ,CAST(TipoIngreso AS varchar(MAX)) AS NameList     
    FROM [BodegaPactia].[Rentas].[vDimTipoIngreso]     
    WHERE SkTipoIngresoPadre IS NULL UNION ALL SELECT t.* ,CAST(c.IdListTopDown AS VARCHAR(MAX)) + ',' + CAST(CAST(t.TipoIngreso AS VARCHAR(MAX)) AS VARCHAR(MAX)) ,CAST(c.NameList + ' | ' + t.TipoIngreso AS varchar(MAX))       
    FROM [BodegaPactia].[Rentas].[vDimTipoIngreso] AS t JOIN CTE c ON c.SkTipoIngreso = t.SkTipoIngresoPadre ) SELECT  CTE.SKTipoIngreso, CTE.NameList FROM  CTE 
    WHERE NOT EXISTS(SELECT * FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto] WHERE SkTipoIngresoPadre=CTE.SkTipoIngreso) 
    ORDER BY CTE.IdListTopDown
    """

    def conection_eco():
        server = 'srvprodsqlcubo.eastus.cloudapp.azure.com'
        database = 'BodegaPactia'
        user = input('Usuario:')
        key = getpass.getpass('Contraseña:')
        return server, database, user, key
    
    def complete_eco():
        
        #Genera una tabla con toda la información disponible de rentas
        pass

    def filter_eco(year, month):
        #Genera una tabla filtrada de acuerdo con el año y el mes, con toda la información disponible de rentas
        year = str(year)
        month = str(month)
        pass
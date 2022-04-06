import pyodbc
import pandas as pd
import getpass

class eco_ayudantes:

    __con = None

    consulta="""
    SELECT DT.Fecha,
    DOA.NumeroActivo,
    DOA.NombreActivo, 
    DOA.NumeroObjetoAlquiler, 
    DOA.NombreObjetoAlquiler, 
    DOA.DescripcionClaseUso,
    DOA.DescripcionUsoActual,
    DMC.NombreMarca,
    DC.DescripcionCategoria,
    DC.CodigoContrato,
    DC.FechaInicioContrato,
    DC.FechaPrimerFinContrato,
    DEP.CodigoSociedad,
    DEP.CodigoUnidadEconomica,
    DOA.CodigoActivo,
    DTI.TipoIngreso,
    SUM(CASE WHEN DE.Escenario = 'REAL' THEN FI.ValorIngreso END) AS IngresoReal ,
    SUM(CASE WHEN DE.Escenario = 'PRESUPUESTO' THEN FI.ValorIngreso END) AS IngresoPlaneado,
    SUM(CASE WHEN DE.Escenario = 'PROYECCION' THEN FI.ValorIngreso END) AS IngresoProyectado ,
    SUM(CASE WHEN DE.Escenario = 'REAL' THEN FI.ValorIngresoPorcentajeParticipacionReal END) AS IngresoRealPorcentajeParticipacion,
    SUM(CASE WHEN DE.Escenario = 'PRESUPUESTO' THEN FI.ValorIngresoPorcentajeParticipacionReal END) AS IngresoPlaneadoPorcentajeParticipacion,
    SUM(CASE WHEN DE.Escenario = 'PROYECCION' THEN FI.ValorIngresoPorcentajeParticipacionReal END) AS IngresoProyectadoPortentajeParticipacion,
    FI.SkEstructuraProducto, 
    FI.SKTipoIngreso 
    FROM BodegaPactia.Rentas.vFactIngresos FI 
    LEFT JOIN BodegaPactia.Rentas.vDimTiempo DT ON DT.SkTiempo = FI.SkTiempo 
    LEFT JOIN BodegaPactia.Rentas.vDimContratos DC ON DC.SkContrato = FI.SkContrato 
    LEFT JOIN BodegaPactia.Rentas.vDimMarcaClientes DMC ON DMC.SkMarcaCliente = FI.SkMarcaCliente 
    LEFT JOIN BodegaPactia.Rentas.vDimObjetoAlquiler DOA ON DOA.SkObjetoAlquiler = FI.SkObjetoAlquiler 
    LEFT JOIN [BodegaPactia].[Rentas].[vDimTipoIngreso] DTI ON DTI.SkTipoIngreso = FI.SkTipoIngreso 
    LEFT JOIN [BodegaPactia].[Rentas].[vDimEscenario] DE ON DE.SkEscenario = FI.Escenario 
    LEFT JOIN [BodegaPactia].[Rentas].[vDimEstructuraProducto] DEP ON DEP.SkEstructuraProducto = FI.SkEstructuraProducto 
    WHERE 1=1 AND DE.Escenario IN ('REAL', 'PRESUPUESTO', 'PROYECCION')     
    GROUP BY DT.Fecha, FI.SkEstructuraProducto,FI.SkTipoIngreso, DOA.NumeroActivo, DOA.NombreActivo, DOA.NumeroObjetoAlquiler, DMC.NombreMarca, DC.DescripcionCategoria, DOA.NombreObjetoAlquiler, DOA.DescripcionClaseUso, DOA.DescripcionUsoActual, DC.CodigoContrato, DC.FechaInicioContrato, DC.FechaPrimerFinContrato, DEP.CodigoSociedad, DEP.CodigoUnidadEconomica, DOA.CodigoActivo, DTI.TipoIngreso
    """


    estructura="""WITH CTE AS (SELECT * ,CAST(SkEstructuraProductoPadre AS VARCHAR(MAX))  + ',' + 
    CAST(CAST(SkEstructuraProducto AS VARCHAR(MAX)) AS VARCHAR(MAX)) AS IdListTopDown,
    CAST(Linea AS varchar(MAX)) AS NameList     
    FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto]     
    WHERE SkEstructuraProductoPadre IS NULL UNION ALL
    SELECT t.* ,
    CAST(c.IdListTopDown AS VARCHAR(MAX)) + ',' + CAST(CAST(t.SkEstructuraProducto AS VARCHAR(MAX)) AS VARCHAR(MAX)),
    CAST(c.NameList + ' | ' + t.Linea AS varchar(MAX))        
    FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto] AS t 
    JOIN CTE c ON c.SkEstructuraProducto = t.SkEstructuraProductoPadre ) 
    SELECT  CTE.SkEstructuraProducto, CTE.NameList FROM  CTE 
    WHERE NOT EXISTS(SELECT * FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto]  
    WHERE SkEstructuraProductoPadre=CTE.SkEstructuraProducto) 
    ORDER BY CTE.IdListTopDown
    """
    
    
    ingreso="""
    WITH CTE AS (SELECT * ,CAST(SkTipoIngresoPadre AS VARCHAR(MAX))  + ',' + 
    CAST(CAST(SkTipoIngreso AS VARCHAR(MAX)) AS VARCHAR(MAX)) AS IdListTopDown         ,
    CAST(TipoIngreso AS varchar(MAX)) AS NameList 
    FROM [BodegaPactia].[Rentas].[vDimTipoIngreso]     
    WHERE SkTipoIngresoPadre IS NULL UNION ALL 
    SELECT t.* ,
    CAST(c.IdListTopDown AS VARCHAR(MAX)) + ',' + 
    CAST(CAST(t.TipoIngreso AS VARCHAR(MAX)) AS VARCHAR(MAX)),
    CAST(c.NameList + ' | ' + t.TipoIngreso AS varchar(MAX)) 
    FROM [BodegaPactia].[Rentas].[vDimTipoIngreso] AS t        
    JOIN CTE c ON c.SkTipoIngreso = t.SkTipoIngresoPadre ) 
    SELECT  CTE.SKTipoIngreso, CTE.NameList FROM  CTE 
    WHERE NOT EXISTS(SELECT * FROM [BodegaPactia].[Rentas].[vDimEstructuraProducto] 
    WHERE SkTipoIngresoPadre=CTE.SkTipoIngreso) 
    ORDER BY CTE.IdListTopDown
    """

    def conection_eco():
        server = 'srvprodsqlcubo.eastus.cloudapp.azure.com'
        database = 'BodegaPactia'
        user = input('Usuario:')
        key = getpass.getpass('Contraseña:')
        eco_ayudantes.__con = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+ key+';TrustServerCertificate=YES;') 
        return True
    
    def clean_estructura():
        df = pd.read_sql_query(eco_ayudantes.estructura, con = eco_ayudantes.__con)
        df[['Estructura', 'Linea', 'UnidadEconomica', 'Activo','ObjetoAlquiler']] =df.NameList.str.split('|', expand=True)
        df.drop(columns='NameList', inplace=True)
        return df

    def clean_ingreso():
        df = pd.read_sql_query(eco_ayudantes.ingreso, con = eco_ayudantes.__con)
        df[['borrar', 'TipoIngreso1', 
            'TipoIngreso2', 'TipoIngreso3', 
            'TipoIngreso4', 'TipoIngreso5']] = df.NameList.str.split('|', expand=True)
        df.drop(columns= ['borrar', 'NameList'], inplace=True)
        return df


    def table_join():
        consulta = pd.read_sql_query(eco_ayudantes.consulta, con = eco_ayudantes.__con)
        # print(consulta.head() )
        estructura = eco_ayudantes.clean_estructura()
        # print(estructura.head() )
        ingreso = eco_ayudantes.clean_ingreso()
        consulta = consulta.merge(estructura, on='SkEstructuraProducto', how='left')
        consulta = consulta.merge(ingreso, on='SKTipoIngreso', how='left')
        return consulta
    
    def complete_eco():
        #Genera una tabla con toda la información disponible de rentas
        df = eco_ayudantes.table_join()
        return df

    def filtered_eco(year, month):
        #Genera una tabla filtrada de acuerdo con el año y el mes, con toda la información disponible de rentas
        year = str(year)
        month = str(month)

        if bool(month)==True & bool(year)==True:
            pass
        elif bool(month)==True & bool(year)==False:
            pass
        elif bool(month)==False & bool(year)==True:
            pass
        else:
            print('Debe especificar el valor de año o de mes, si no desea aplicar filtros utilice la función complete_eco')
        return 
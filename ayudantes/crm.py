import requests
import xmltodict
import json
import pandas as pd
import getpass

class crm_ayudantes:

    def inicio_crm():

        user = input('Usuario:')
        key = getpass.getpass('Contraseña')
        return user, key

    def crm_tables(user=user, key=key):

        api_url = "https://pactia.od2.vtiger.com/restapi/V1/OData/Pull/odata.svc/Entity"
        response = requests.get(api_url, auth=(user, key))
        if response.status_code==200:
            print('Conexión exitosa a OData')
        else:
            print('No se pudo realizar la conexión con OData')
        dict_data = response.content
        dict_data = xmltodict.parse(response.content)
        json_data = json.loads(json.dumps(dict_data))
        final_json = pd.DataFrame.from_dict(json_data).service['workspace']
        print('Las tablas disponibles en el CRM son:\n\n')
        print(pd.json_normalize(pd.json_normalize(final_json).collection[0])['atom:title'])
    
    def read_crm(table, page, user=user, key=key):
    #Parametro tabla: Tabla de la cuál se va a extraer la información
    #Parametro page: Página de registros, cada página tiene 5000 registros
    
    #Llamado de información por API
        if page < 0:
            print('Debe especificar una página')
        elif page == 1:
            skip=(page-1)*5000
            api_url = "https://pactia.od2.vtiger.com/restapi/V1/OData/Pull/odata.svc/"
            request = api_url+table
            response = requests.get(request, auth=(user, key))
            print(request)
            if response.status_code==200:
                print('Conexión exitosa a OData en tabla ', table, ' para la página ', page)
            else:
                print('No se pudo realizar la conexión con OData, revisar nombre de tabla')
        else:
            skip=(page-1)*5000
            api_url = "https://pactia.od2.vtiger.com/restapi/V1/OData/Pull/odata.svc/"
            request = api_url+table+'?$skip='+str(skip)
            response = requests.get(request, auth=(user, key))
            print(request)
            if response.status_code==200:
                print('Conexión exitosa a OData en tabla ', table, ' para la página ', page)
            else:
                print('No se pudo realizar la conexión con OData, revisar nombre de tabla')

        #Conversión a DataFrame
        dict_data = xmltodict.parse(response.content)
        json_data = json.loads(json.dumps(dict_data))
        final_json = pd.DataFrame.from_dict(json_data).feed[4]
        data = pd.json_normalize(final_json)
        
        #Limpieza columnas
        data = data[data.columns.drop(list(data.filter(regex='@m:type')))]
        data = data[data.columns.drop(list(data.filter(regex='@scheme')))]
        data = data[data.columns.drop(list(data.filter(regex='@null')))]
        data = data[data.columns.drop(list(data.filter(regex='@m:null')))]
        
        data.columns = data.columns.str.replace('content.m:properties.d:', '')
        data.columns = data.columns.str.replace('.#text','')
        
        data = data.iloc[:,7:]
        
        return data

    def complete_crm(table, user=user, key=key):

    #Se ingresa la tabla qué se quiere leer completamente, es el único parametro y debe ser en formato string
    
    #Se inicializan valores para entrar a ciclo
        df = pd.DataFrame()
        shape = 0
        count = 0
        #Cada llamado entrega máximo 5001 registros sí tiene hojas adicionales
        while shape%5001 == 0 or shape%5000 == 0:
            count+=1
            page_table = read_crm(table, count)
            df = df.append(page_table)
            shape = len(df)
            
        print('Total de registros de tabla ', table,' fue ',shape)
        return df


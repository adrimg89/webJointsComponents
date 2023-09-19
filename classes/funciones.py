import requests
import mysql.connector
from passwords import *

def airtable_url(table_name):
    base_id=joints_base_id
    
    url=f'https://api.airtable.com/v0/{base_id}/{table_name}'
    return url

def configure_headers():
    api_key=adri_api_key
    
    headers={'Authorization': f'Bearer {api_key}'}
    
    return headers

def rt_connection():
    config = {
        'user': user_rt,
        'password': password_rt,
        'host': host_rt,
        'database': database_components,
        'port': port,        
    }
    connection = mysql.connector.connect(**config)
    #print (config)
    return connection
    
def get_joints():
    
    url=airtable_url(joints_table)
    headers=configure_headers()
    
    # Variables para controlar la paginación y contar registros
    params = {
        'pageSize': 100,  # Tamaño máximo de una página (ajústalo según tus necesidades)
    }
    
    records_list = []  # Lista para almacenar los datos que se devolverán como respuesta

    try:
        offset = None
        while True:
            # Configurar el offset para obtener la siguiente página
            if offset:
                params['offset'] = offset

            # Realizar una petición GET a la tabla de Airtable
            response = requests.get(url, headers=headers, params=params)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la página actual en formato JSON
                data = response.json()

                # Acceder a los registros de la página actual
                records = data['records']

                # Si no hay más registros, salir del bucle
                if not records:
                    break

                # Procesar los registros que cumplen la condición y agregarlos a records_list
                for record in records:
                    # Cada registro tiene un campo 'fields' con los datos reales
                    fields = record['fields']

                    # Obtener el valor de la columna 'joint_type_id'
                    joint_type_id = fields.get('joint_type_id')
                    joints3_type = fields.get('JointType_api')
                    cgt = fields.get('api_ConnectionGroup_type')
                    components = fields.get('Components_api')
                    Project = fields.get('project_export')
                    

                    # Agregar el valor a records_list
                    records_list.append({
                        'joint_type_id': joint_type_id,
                        'joints3_type': joints3_type,
                        'api_ConnectionGroup_type': cgt,
                        'Components_api': components,
                        'project_export': Project,                        
                    })
                    
                    #print(records_list)

                # Obtener el offset para la siguiente página, si no hay más, el valor será None y salimos del bucle
                offset = data.get('offset')
                if not offset:
                    break
            else:
                # Si la petición no fue exitosa, imprimir el mensaje de error
                records_list = [f"Error al obtener datos: {response.status_code} - {response.text}"]
                break

        # Ordenar registros
        records_list = sorted(records_list, key=lambda x: x['joint_type_id'])
        

    except requests.exceptions.RequestException as e:
        # Manejar excepciones de conexión
        records_list = [f"Error de conexión: {e}"]

    return records_list

def get_joint_layers(joint):
    
    url=airtable_url(jointlayers_table)
    headers=configure_headers()
    
    # Variables para controlar la paginación y contar registros
    params = {
        'filterByFormula': "SEARCH('"+joint+"', {joint_type_code})",
        'pageSize': 100,  # Tamaño máximo de una página (ajústalo según tus necesidades)
    }
    
    records_list = []  # Lista para almacenar los datos que se devolverán como respuesta

    try:
        offset = None
        while True:
            # Configurar el offset para obtener la siguiente página
            if offset:
                params['offset'] = offset

            # Realizar una petición GET a la tabla de Airtable
            response = requests.get(url, headers=headers, params=params)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la página actual en formato JSON
                data = response.json()

                # Acceder a los registros de la página actual
                records = data['records']

                # Si no hay más registros, salir del bucle
                if not records:
                    break

                # Procesar los registros que cumplen la condición y agregarlos a records_list
                for record in records:
                    # Cada registro tiene un campo 'fields' con los datos reales
                    fields = record['fields']

                    # Obtener el valor de las columnas
                    material_id = fields.get('material_id')
                    description = fields.get('Long_Name (from Material)')
                    formula = fields.get('Calculation Formula')
                    performance = fields.get('Performance')

                    # Agregar el valor a records_list
                    records_list.append({
                        'material_id': material_id,
                        'Long_Name': description,
                        'formula': formula,
                        'performance': performance,                                               
                    })
                    
                    #print(records_list)

                # Obtener el offset para la siguiente página, si no hay más, el valor será None y salimos del bucle
                offset = data.get('offset')
                if not offset:
                    break
            else:
                # Si la petición no fue exitosa, imprimir el mensaje de error
                records_list = [f"Error al obtener datos: {response.status_code} - {response.text}"]
                break

    except requests.exceptions.RequestException as e:
        # Manejar excepciones de conexión
        records_list = [f"Error de conexión: {e}"]

    return records_list    
    
def get_connectiontype(cgt):
    
    url=airtable_url(connectiontype_table)
    headers=configure_headers()
    
    # Variables para controlar la paginación y contar registros
    params = {
        'filterByFormula': "SEARCH('"+cgt+"', {connectiongroup_type_id})",
        'pageSize': 100,  # Tamaño máximo de una página (ajústalo según tus necesidades)
    }
    
    records_list = []  # Lista para almacenar los datos que se devolverán como respuesta

    try:
        offset = None
        while True:
            # Configurar el offset para obtener la siguiente página
            if offset:
                params['offset'] = offset

            # Realizar una petición GET a la tabla de Airtable
            response = requests.get(url, headers=headers, params=params)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la página actual en formato JSON
                data = response.json()

                # Acceder a los registros de la página actual
                records = data['records']

                # Si no hay más registros, salir del bucle
                if not records:
                    break
                
                # Procesar los registros que cumplen la condición y agregarlos a records_list
                for record in records:
                    # Cada registro tiene un campo 'fields' con los datos reales
                    fields = record['fields']

                    # Obtener el valor de las columnas
                    connection_type_id = fields.get('connection_type')
                    description = fields.get('description (from connection_type_id)')
                    formula = fields.get('Calculation Formula')
                    performance = fields.get('Performance')
                    cgtdesc = fields.get('CGT_description')

                    # Agregar el valor a records_list
                    records_list.append({
                        'connection_type_id': connection_type_id,
                        'description': description,
                        'formula': formula,
                        'performance': performance,
                        'CGtype_description':cgtdesc                                               
                    })
                    
                    
                # Obtener el offset para la siguiente página, si no hay más, el valor será None y salimos del bucle
                offset = data.get('offset')
                if not offset:
                    break
            else:
                # Si la petición no fue exitosa, imprimir el mensaje de error
                records_list = [f"Error al obtener datos: {response.status_code} - {response.text}"]
                break

    except requests.exceptions.RequestException as e:
        # Manejar excepciones de conexión
        records_list = [f"Error de conexión: {e}"]

    return records_list

def getcomp():
    connection=rt_connection()
    cursor= connection.cursor()
    
    query = "select code, status from component_type where status <> 'deprecated' order by code"

    cursor.execute(query)
    
    results = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return results

def getExecutionUnits(component_type):
    connection=rt_connection()
    cursor= connection.cursor()
    
    query = "select execution_unit_type.code, execution_unit_type.description, execution_unit_type.thickness "\
      "from execution_unit_type "\
      "inner join component_type_execution_unit_type on execution_unit_type.id=component_type_execution_unit_type.execution_unit_type_id "\
      "inner join component_type on component_type_execution_unit_type.component_type_id=component_type.id "\
      f"where component_type.code='{component_type}'"
      
    cursor.execute(query)
    
    results = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return results

def getLayerGroups(EU):
    connection=rt_connection()
    cursor= connection.cursor()
    
    query = "select layer_group_type.code, layer_group_type.description "\
      "from execution_unit_type "\
      "inner join execution_unit_type_layer_group_type on execution_unit_type.id=execution_unit_type_layer_group_type.execution_unit_type_id "\
      "inner join layer_group_type on execution_unit_type_layer_group_type.layer_group_type_id=layer_group_type.id "\
      f"where execution_unit_type.code='{EU}'"
      
    cursor.execute(query)
    
    results = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return results

def getcgclass():
    
    url=airtable_url(cgclass_table)
    headers=configure_headers()
    
    # Variables para controlar la paginación y contar registros
    params = {
        'pageSize': 100,  # Tamaño máximo de una página (ajústalo según tus necesidades)
    }
    
    records_list = []  # Lista para almacenar los datos que se devolverán como respuesta

    try:
        offset = None
        while True:
            # Configurar el offset para obtener la siguiente página
            if offset:
                params['offset'] = offset

            # Realizar una petición GET a la tabla de Airtable
            response = requests.get(url, headers=headers, params=params)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la página actual en formato JSON
                data = response.json()

                # Acceder a los registros de la página actual
                records = data['records']

                # Si no hay más registros, salir del bucle
                if not records:
                    break

                # Procesar los registros que cumplen la condición y agregarlos a records_list
                for record in records:
                    # Cada registro tiene un campo 'fields' con los datos reales
                    fields = record['fields']

                    # Obtener el valor de la columna 'joint_type_id'
                    connectiongroup_class = fields.get('connectiongroup_class')
                    Description_CGClass = fields.get('Description_CGClass')
                    planilla = fields.get('Planilla PDF')
                    box_type = fields.get('box_type (from boxtype_id)')
                                 
                    # Agregar el valor a records_list
                    records_list.append({
                        'connectiongroup_class': connectiongroup_class,
                        'Description_CGClass': Description_CGClass,
                        'planilla': planilla,  
                        'box_type': box_type,                                           
                    })
                    
                    #print(records_list)

                # Obtener el offset para la siguiente página, si no hay más, el valor será None y salimos del bucle
                offset = data.get('offset')
                if not offset:
                    break
            else:
                # Si la petición no fue exitosa, imprimir el mensaje de error
                records_list = [f"Error al obtener datos: {response.status_code} - {response.text}"]
                break

        # Ordenar registros
        records_list = sorted(records_list, key=lambda x: x['box_type'], reverse=True)
        

    except requests.exceptions.RequestException as e:
        # Manejar excepciones de conexión
        records_list = [f"Error de conexión: {e}"]

    return records_list

def getcgtype(cgclass):
    url=airtable_url(cgtype_table)
    headers=configure_headers()
    
    params = {
        'filterByFormula': "SEARCH('"+cgclass+"', {api_ConnectionGroup_Class})",
        'pageSize': 100,  # Tamaño máximo de una página (ajústalo según tus necesidades)
    }
    
    records_list = []  # Lista para almacenar los datos que se devolverán como respuesta

    try:
        offset = None
        while True:
            # Configurar el offset para obtener la siguiente página
            if offset:
                params['offset'] = offset

            # Realizar una petición GET a la tabla de Airtable
            response = requests.get(url, headers=headers, params=params)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la página actual en formato JSON
                data = response.json()

                # Acceder a los registros de la página actual
                records = data['records']

                # Si no hay más registros, salir del bucle
                if not records:
                    break

                # Procesar los registros que cumplen la condición y agregarlos a records_list
                for record in records:
                    # Cada registro tiene un campo 'fields' con los datos reales
                    fields = record['fields']

                    # Obtener el valor de la columna 'joint_type_id'
                    cgtype_id = fields.get('cgtype_id')
                    connectiongroup_class = fields.get('api_ConnectionGroup_Class')
                    cgclass_description = fields.get('CG_Class_api')
                    description = fields.get('Description')
                    connectiontype = fields.get('RL_cgtype_ctype (from ConnectionGroup_type)')
                                 
                    # Agregar el valor a records_list
                    records_list.append({
                        'cgtype_id': cgtype_id,
                        'connectiongroup_class': connectiongroup_class,
                        'cgclass_description': cgclass_description,  
                        'description': description,  
                        'connectiontype': connectiontype                                         
                    })
                                        
                # Obtener el offset para la siguiente página, si no hay más, el valor será None y salimos del bucle
                offset = data.get('offset')
                if not offset:
                    break
            else:
                # Si la petición no fue exitosa, imprimir el mensaje de error
                records_list = [f"Error al obtener datos: {response.status_code} - {response.text}"]
                break

        # Ordenar registros
        records_list = sorted(records_list, key=lambda x: x['cgtype_id'])
        

    except requests.exceptions.RequestException as e:
        # Manejar excepciones de conexión
        records_list = [f"Error de conexión: {e}"]

    return records_list

def get_clayers(cgt):
    ct_info=get_connectiontype(cgt)
    
    ct=[]
    
    for i in ct_info:
        ct.append(i['connection_type_id'])
    
    url=airtable_url(clayers_table)
    headers=configure_headers()
    
    records_list = []  # Lista para almacenar los datos que se devolverán como respuesta
    
    for i in ct:
        params = {
            'filterByFormula': "SEARCH('"+i+"', {connection_type_code})",
            'pageSize': 100,  # Tamaño máximo de una página (ajústalo según tus necesidades)
        }      

        try:
            offset = None
            while True:
                # Configurar el offset para obtener la siguiente página
                if offset:
                    params['offset'] = offset

                # Realizar una petición GET a la tabla de Airtable
                response = requests.get(url, headers=headers, params=params)

                # Verificar si la petición fue exitosa (código de estado 200)
                if response.status_code == 200:
                    # Obtener los datos de la página actual en formato JSON
                    data = response.json()

                    # Acceder a los registros de la página actual
                    records = data['records']

                    # Si no hay más registros, salir del bucle
                    if not records:
                        break

                    # Procesar los registros que cumplen la condición y agregarlos a records_list
                    for record in records:
                        # Cada registro tiene un campo 'fields' con los datos reales
                        fields = record['fields']

                        # Obtener el valor de la columna 'joint_type_id'
                        connectiontype_id = fields.get('connection_type_code')
                        material = fields.get('material_id')
                        description = fields.get('Long name (from Material)')
                        performance = fields.get('Performance')
                        formula = fields.get('Calculation Formula')
                        fase=fields.get('Fase')
                                    
                        # Agregar el valor a records_list
                        records_list.append({
                            'connectiontype_id': connectiontype_id,
                            'material': material,
                            'description': description, 
                            'performance': performance,  
                            'formula': formula,  
                            'fase': fase                                         
                        })
                                            
                    # Obtener el offset para la siguiente página, si no hay más, el valor será None y salimos del bucle
                    offset = data.get('offset')
                    if not offset:
                        break
                else:
                    # Si la petición no fue exitosa, imprimir el mensaje de error
                    records_list = [f"Error al obtener datos: {response.status_code} - {response.text}"]
                    break      
            
        except requests.exceptions.RequestException as e:
            # Manejar excepciones de conexión
            records_list = [f"Error de conexión: {e}"]

    # Ordenar registros
    records_list = sorted(records_list, key=lambda x: x['connectiontype_id'])

    #return records_list
    return records_list

"""
def get_cgclass_cgt():
    info=getcgclass()
    for i in info: print (i['connectiongroup_class'])
"""
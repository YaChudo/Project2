import xml.etree.ElementTree as ET
import pandas as pd
import datetime
import os
import shutil
from pathlib import Path
import numpy as np

def date_now():  # определение текущей даты и часа
    now = datetime.datetime.now().strftime("%Y%m%d%H")
    return now

def copy_doc(folder_from, folder_to, folder_user_list):  # копирование xml файлов в папку ггггммддчч
    try:
        for f in os.listdir(folder_from):
            for folder_user in folder_user_list:
                if os.path.isfile(os.path.join(folder_from, f)):
                    shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, folder_user, f))
                if os.path.isdir(os.path.join(folder_from, f)):
                    shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, folder_user, f))
        return
    except:
        pass

def search_unit(XML_doc, file):  # поиск тегов в xml документах - eDIMessage, receivingAdvice и deliveryContact, создание list
    try:
        tree = ET.parse(XML_doc)
        root = tree.getroot()
        for elem in root.iter(tag='receivingAdvice'):
            MX_number = int(elem.attrib['number'][2])
        for elem1 in root.iter(tag="deliveryContact"):
            contact_name = elem1.find('name').text
        for elem2 in root.iter(tag='eDIMessage'):
            id_number = elem2.attrib['id']
        file_number = file

        #my_file.write(x, contact_name, '\n')
        print (file_number, id_number, MX_number, contact_name)
        return file_number, id_number, MX_number, contact_name

    except:
        pass

def GroupingTagsIntoList (paths): # объединение пути и тегов документа в общий список 
    try:
        all_name = [] #создание списка
        for file in paths:
            lol = search_unit(file, str(file))
            r = all_name.append(lol)
        return all_name
    except:
        pass

def TablePartitioning():
    try:
        df = pd.DataFrame(list_with_teg, columns=['name_doc', 'id_number', 'MX_number', 'contact_name']) #общая таблица из всех xml документов
        df_duplicate = df[df.duplicated(['MX_number', 'contact_name'])]
        df_duplicate = df_duplicate.rename_axis('index').reset_index()
        df_duplicate = df_duplicate.drop(['index'], axis=1)
        df6 = pd.DataFrame()
        df4 = pd.DataFrame()
        for i in range(len(df)):
            for x in range(len(df_duplicate)):
                if df['MX_number'][i] == df_duplicate['MX_number'][x] and df['contact_name'][i] == df_duplicate['contact_name'][x]:
                    new_row = {'index': i, 'name_doc': df['name_doc'][i], 'id_number': df['id_number'][i],
                               'MX_number': df['MX_number'][i], 'contact_name': df['contact_name'][i]}
                    df6 = df6.append(new_row, ignore_index=True)
        df6 = df6.sort_values(by=['contact_name', 'MX_number'])
        print(df6)
        # for i in range(len(df6)):
        #     for x in range(len(df_duplicate)):
        #         if df['MX_number'][i] == df_duplicate['MX_number'][x] and df['contact_name'][i] ==df_duplicate['contact_name'][x]:

        df4 = df.drop_duplicates(subset=['MX_number', 'contact_name'],
                                 keep=False)  #таблица строки, которые не повторяются
        list_without_duplicates = df4['name_doc'].tolist() #список xml, которые не имеют дубликат
        print(df6)
        print(df4)
        return list_without_duplicates
    except:
        pass

now = date_now()
way_from = r'C:\Users\pered\OneDrive\Рабочий стол\EDI\Inbox' #каталог, в котором расположены xml документы
# way_to = r'C:\Users\kr.perederina\Desktop\EDI\OUT' #каталог, в который будут копироваться текущие документы
# user_list = ([now])

# copy_doc(way_from, way_to, user_list) #копирование файлов

paths = sorted(Path(way_from).glob('*.xml')) #найти все xml документы в каталоге
paths_2 = list(map(str, paths)) #приведение к строке 

list_with_teg = GroupingTagsIntoList(paths_2)

getting_tables = TablePartitioning()

# df.to_csv(r'C:\Users\pered\OneDrive\Рабочий стол\EDI\csv\df.csv', encoding= 'utf-8', header=True, index=False, sep=';')
# df2.to_csv(r'C:\Users\pered\OneDrive\Рабочий стол\EDI\csv\df2.csv', encoding= 'utf-8', header=True, index=False, sep=';')





# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 19:14:42 2018

@author: Actiview
"""

import os
import xlwt
import json
import zipfile
import pandas as pd
from openpyxl import load_workbook
import a1_ShelfScoreAccuracy as a1
import a2_timeObjDelta as a2
import a3_tcomp_final as a3
import a4_r_nItemsReplaced as a4
import a5_nObjGazedPreGrab as a5

path_to_zipped = 'C:/Users/VORTEX/Desktop/py_assense/analogies/zipped'
path_to_excel = 'C:/Users/VORTEX/Desktop/py_assense/analogies/csv/analogies.xlsx'
#path_to_json = 'C:/Temp/analogies_files/analogies.xls'

indices = ['ShelfScoreAccuracy','tCompletionToDone', 'tCompletion', 'tDone',
           'tObjDelta', 'tObjDeltaSum','tObjDeltaSumDivCount', 'r_nObjSelectedPerShelf',
           'r_t1stSolution', 'r_t1stSolutionToDone','r_nObjGazedPreGrab', 'r_nObjGazedPreSolution' ]

def save_json(list_dfs, json_path, indices):
    dicts_merged_dfs = {}
    try:
        for indice, list_df in zip(indices, list_dfs):
            merged_df = pd.concat(list_df)
            dicts_merged_df = merged_df.to_dict('index')
            dicts_merged_dfs[indice] = dicts_merged_df  
                 
        with open(json_path, 'w') as jf:
            json.dump(dicts_merged_dfs, jf, ensure_ascii=True, sort_keys = True, indent=4, allow_nan=True, separators=(',', ': '))
    except ValueError:
        pass

def creat_empty_xls(xls_path):
    if not os.path.exists(xls_path):
        print("creating file...")
        writer = pd.ExcelWriter(xls_path, engine='xlsxwriter')
        writer.save()
    else:
        print("file exists...")


def save_xls(list_dfs, xls_path, indices):

    book = load_workbook(xls_path)        
    writer = pd.ExcelWriter(xls_path, engine = 'openpyxl')
    writer.book = book
    writer.sheets = {x.title: x for x in book.worksheets}
    for n, df_list in enumerate(list_dfs):
        x = indices[n]
        start_row = - 1
        for df in df_list:
            start_row += 1
            df.to_excel(writer, sheet_name = '%s' %x, startrow = start_row, header = False)
    writer.save()

creat_empty_xls(path_to_excel)
zipped_files = [pos_zip for pos_zip in os.listdir(path_to_zipped) if pos_zip.endswith('.zip')]
pwd = '123456'
b_pwd = str(pwd).encode('ascii')
dn0, dn1, dn2, dn3, dn4, dn5, dn6, dn8, dn9, dn10, dn11, dn12 = [], [], [], [], [], [], [], [], [], [], [], []
print('Unzipping')
for file_name in zipped_files:
    with zipfile.ZipFile(path_to_zipped + "/" + file_name, 'r') as z:
        for filename in z.namelist():
            if filename == "Settings.json" or filename == "EventSeries.json":
                with z.open(filename ,pwd=b_pwd) as f:
                    data = f.read()
                    d = json.loads(data.decode("utf-8"))
                    if filename == "Settings.json":
                        user_id = d.get("userID")
                    a1.main(d, filename, dn0)
                    a2.main(d, filename, dn4, dn5, dn6)
                    a3.main(d, filename, dn1, dn2, dn3)
                    a4.main(d, filename, dn8, dn9, dn10)
                    a5.main(d, filename, dn11, dn12)
         
        save_xls([dn0, dn1, dn2, dn3, dn4, dn5, dn6, dn8, dn9, dn10, dn11, dn12], path_to_excel, indices)
        print(user_id)
print('Analogies Done')


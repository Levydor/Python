# -*- coding: utf-8 -*-
"""
Created on Sun Nov  18 11:32:59 2018

@author: Actiview
"""
import numpy as np
import pandas as pd
from openpyxl import load_workbook

path_to_excel = 'C:/Users/VORTEX/Desktop/analogies/csv/analogies.xlsx'

def save_xls(list_df, xls_path, indexes):
    book = load_workbook(xls_path)
    writer = pd.ExcelWriter(xls_path, engine = 'openpyxl')
    writer.book = book
    writer.sheets = {x.title: x for x in book.worksheets}
    start_r = 0
    for df in list_df:
        x = indexes
        df.to_excel(writer, sheet_name = '%s' %x, startrow = start_r, header = False )
        start_r += 1
    writer.save()
    writer.close()

def t_delta(t1, t2):
    delta = t1- t2
    t_delta = round(delta, 4)
    return t_delta

def mili_delt(t1, t2):
    ind = False
    if t_delta(t1, t2) >= 0.2:
        ind = True
    return ind

def untype(l1):
    c = 0
    for i in l1:
        try:
            if type(i) == str:
                c += 1
        except TypeError:
            pass
    for i in range(20 - c):
        l1.pop()
    return l1


dn11 = []
def main(d, filename):
    global user_id
    flow, obj, ugazed = [], [], []
    ugazed = np.full((7,20), str)
    if filename == "Settings.json":
        user_id = d.get("userID")
        #print(user_id)
    elif filename == "EventSeries.json":
        for event in d:
            if event.get('$type') == 'Actiview.Logger.Events.FlowEvent, Actiview.Logger' :
                name = event.get ('name')
                level = event.get('level')
                state = event.get('state')
                #time = event.get('Time')
                if (level == 3 and state == 0):
                    etype = 'round'
                    flow.append([etype, name])
                    obj.append([etype, name])
            elif event.get('$type') == 'Actiview.Logger.Events.ObjectGrabEvent, AssenseObjects':
                grab_time = event.get('Time')
                ob = event.get('o')
                ob_name = ob.get('name')
                #ob_uid = ob.get('uid')
                flow.append(['gr: {0}'.format(ob_name), grab_time])
                obj.append(['gr: {0}'.format(ob_name), grab_time])
            elif event.get('$type') == 'Actiview.Logger.Events.PlayerEvent, Actiview.Logger' :
                gtime = event.get('Time')
                gaze = event.get('gaze')
                for key, value in gaze.items():
                    if key == 'lookAtObject' and value.get('uid') != '':
                        obj.append([value.get('uid'), gtime])

        #r_nObjGazedPreGrab
        p = []
        for n, (o, t) in enumerate(obj):
            if o[:2] == 'gr':
                p.append(['g', n])
            elif o == 'round':
                p.append(['r', n])
        #creating relevant position list
        pn = []
        for x, y in zip(p,p[1:]):
            if x[0] == 'r' and y[0] == 'g':
                pn.append([x[0], x[1]])
                pn.append([y[0], y[1]])
            elif x[0] == 'r'  and y[0] == 'r':
                pn.append([x[0], x[1]])
                pn.append([y[0], y[1]])
            elif x[0] == 'g'  and y[0] == 'g':
                pass
            elif x[0] == 'g' and y[0] == 'r':
                pass
        #run on obj list and check if obj time delta >= 0.3
        p1, n, objn1 = 0, 0, ''
        for i, r in enumerate(pn):
            if i < 12  and i % 2 == 0:
                print(i,n)
                for n1, n2 in zip(obj[pn[i][1]:pn[i+1][1]], obj[pn[i][1]+1:pn[i+1][1]]):
                    if n1[0] == 'round' and n2[0] != 'round':
                        objt1 = n2[1]
                        objn1 = n2[0]
                    elif n1[0] != 'round' and n2[0] != 'round' and n1[0] != n2[0]:
                        if n2[0][:2] == 'gr':
                            break                                        
                        elif mili_delt(n1[1], objt1):
                            try:
                                ugazed[n][p1] = n1[0]
                                p1 += 1
                                objt1 = n2[1]
                                objn1 = n2[0]
                            except IndexError:
                                pass
                        elif objn1 != n2[0]:
                            objt1 = n2[1]
                            objn1 = n2[0]                                    
                    elif n1[0] == n2[0] or (n1[0] == 'round' and n2[0] == 'round') :
                        pass
                n += 1
                p1 = 0
                    
            elif i == 12:
                n = 6
                print(i,n)
                for n1, n2 in zip(obj[pn[i][1]:], obj[pn[i][1]+1:]):
                    if n1[0] == 'round':
                        pass
                    elif n1[0] != 'round' and n1[0] != n2[0]:
                        if n2[0][:2] == 'gr':
                            break
                        elif mili_delt(n1[1], objt1):
                            try:
                                ugazed[n][p1] = objn1
                                p1 += 1
                                objt1 = n2[1]
                                objn1 = n2[0]
                            except IndexError:
                                pass
                        elif objn1 != n2[0]:
                            objt1 = n2[1]
                            objn1 = n2[0]  
                    elif n1[0] == n2[0]:
                        pass
        # poping out ierelevant data from ugazed            
        def c_uni(l1,i):
            l1 = list(ugazed[i])
            l1 = untype(l1)
            l1 = np.unique(l1)
            return l1
        
        # creating count list
        rnd = np.full(7,np.nan)
        for i in range(7):
            x = c_uni('a' + str(i), int(i))
            rnd[i] = len(x)
        rnd = list(rnd)
                                                            
        d11 = pd.DataFrame([rnd], index = [user_id])
        dn11.append(d11)
        
    indexes = 'r_nObjGazedPreGrab'   
    save_xls((dn11), path_to_excel,indexes)
                                      
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
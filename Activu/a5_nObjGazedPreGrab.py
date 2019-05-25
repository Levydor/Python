# -*- coding: utf-8 -*-
"""
Created on Sun Nov  18 11:32:59 2018

@author: Actiview
"""
import numpy as np
import pandas as pd
import re

#indices = ['r_nObjGazedPreGrab', 'r_nObjGazedPreSolution'] 

def t_delta(t1, t2):
    delta = t1- t2
    t_delta = round(delta, 4)
    return t_delta

def mili_delt(t1, t2):
    ind = False
    if t_delta(t1, t2) >= 0.2:
        ind = True
    return ind

def c_uni(l1, i, gazed):
    l1 = list(gazed[i])
    l1 = untype(l1)
    l1 = np.unique(l1)
    return l1

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

uid_to_ex = ['Main-Timer-a1120929-ab03-4ea0-89d1-4ffc81b074e8', \
             'Main-StartBtn-e8b17f8f-4b4d-4181-a4ec-9eccb98a5bf4',\
             '']

def ex_list(a):
    status = True
    for i in uid_to_ex:
        if a == i:
            status = False
    return status

dn11, dn12 = [], []
def main(d, filename, dn11, dn12):
    global user_id
    obj, obj1, flow = [], [], []
    ugazed = np.full((7,20), str)
    ugazed1 = np.full((7,20), str)
    if filename == "Settings.json":
        user_id = d.get("userID")
    elif filename == "EventSeries.json":
        for event in d:
            if event.get('$type') == 'Actiview.Logger.Events.FlowEvent, Actiview.Logger' :
                name = event.get ('name')
                level = event.get('level')
                state = event.get('state')
                if (level == 3 and state == 0):
                    etype = 'round'
                    obj.append([etype, name])
                    obj1.append([etype, name])
                    flow.append(name)
            elif event.get('$type') == 'Actiview.Logger.Events.ObjectGrabEvent, AssenseObjects':
                grab_time = event.get('Time')
                ob = event.get('o')
                ob_name = ob.get('name')
                obj.append(['gr: {0}'.format(ob_name), grab_time])
            elif event.get('$type') == 'Actiview.Logger.Events.ContainerFilledEvent, AssenseObjects':
                con_time = event.get('Time')
                ob = event.get('o')
                ob_name = ob.get('name')
                obj1.append(['co: {0}'.format(ob_name), con_time])
            elif event.get('$type') == 'Actiview.Logger.Events.PlayerEvent, Actiview.Logger' :
                gtime = event.get('Time')
                gaze = event.get('gaze')
                for key, value in gaze.items():
                    if key == 'lookAtObject' and ex_list(value.get('uid')) == True and re.search('Slot*',value.get('name')) == None:
                        obj.append([value.get('uid'), gtime])
                        obj1.append([value.get('uid'), gtime])

#r_nObjGazedPreGrab
        p = []
        for n, (o, t) in enumerate(obj):
            if o[:2] == 'gr':
                p.append(['g', n])
            elif o == 'round':
                p.append(['r', n])
        
        po = []
        for n, (o, t) in enumerate(obj1):
                if o[:2] == 'co':
                    po.append(['c', n])
                elif o == 'round':
                    po.append(['r', n])            
                
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
                      
        pn1, i = [], 0
        for x, y in zip(po,po[1:]):
            if x[0] == 'r' and y[0] == 'c':
                pn1.append([x[0], x[1]])
                pn1.append([y[0], y[1]])
            elif x[0] == 'r'  and y[0] == 'r':
                pn1.append([x[0], x[1]])
                pn1.append([y[0], y[1]])
            elif x[0] == 'c'  and y[0] == 'c' and i < 1:
                i += 1
                pn1.append([y[0], y[1]])
            elif x[0] == 'c' and y[0] == 'r':
                i = 0
                pass
        pn1.append(['end',0])
            
        #run on obj list and check if obj time delta >= 0.2
        p1, n, objn1 = 0, 0, ''
        for i, r in enumerate(pn):
            if i < 12  and i % 2 == 0:
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
        # creating count list
        i = 0
        rnd = np.full(7,np.nan)
        for i in range(7):
            x = c_uni('a' + str(i), int(i), ugazed)
            rnd[i] = len(x)
        rnd = list(rnd)
        
# r_nObjGazedPreSolution         
        #run on obj list and check if obj time delta >= 0.2
        ri, p1, n, objn1 = 0, 0, 0, ''
        for i, r in enumerate(pn1):
            if i < 6  and i % 2 == 0:
                for n1, n2 in zip(obj1[pn1[i][1]:pn1[i+1][1]], obj1[pn1[i][1]+1:pn1[i+1][1]]):
                    if n1[0] == 'round' and n2[0] != 'round':
                        objt1 = n2[1]
                        objn1 = n2[0]
                    elif n1[0] != 'round' and n2[0] != 'round' and n1[0] != n2[0]:
                        if n2[0][:2] == 'co':
                            break                                        
                        elif mili_delt(n1[1], objt1):
                            try:
                                ugazed1[n][p1] = n1[0]
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
            elif i > 5 and i < 15 and i % 3 == 0:
                for n1, n2 in zip(obj1[pn1[i][1]:pn1[i+3][1]], obj1[pn1[i][1]+1:pn1[i+3][1]]):
                    if n1[0] == 'round' and n2[0] != 'round':
                        objt1 = n2[1]
                        objn1 = n2[0]
                    elif n1[0] != 'round' and n2[0] != 'round' and n1[0] != n2[0]:
                        if n2[0][:2] == 'co':
                            ri += 1
                            if ri > 1:
                                ri = 0
                                break
                        elif mili_delt(n1[1], objt1):
                            try:
                                ugazed1[n][p1] = n1[0]
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
            elif i > 14:
                n = 6
                for n1, n2 in zip(obj[pn1[i][1]:], obj[pn1[i][1]+1:]):
                    if n1[0] == 'round' and n2[0] != 'round':
                        objt1 = n2[1]
                        objn1 = n2[0]
                    elif n1[0] != 'round' and n2[0] != 'round' and n1[0] != n2[0]:
                        if n2[0][:2] == 'co':
                            ri += 1
                            if ri > 1:
                                ri = 0
                                break
                        elif mili_delt(n1[1], objt1):
                            try:
                                ugazed1[n][p1] = n1[0]
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

        # creating count list
        i = 0
        rnds = np.full(7,np.nan)
        for i in range(7):
            x = c_uni('a' + str(i), int(i), ugazed1)
            rnds[i] = len(x)
        rnds = list(rnds)
                                                            
        d11 = pd.DataFrame([rnd], index = [user_id])
        d12 = pd.DataFrame([rnds], index = [user_id])
        dn11.append(d11)
        dn12.append(d12)
          
    #save_json([dn11, dn12], path_to_json, indices)
                                      
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
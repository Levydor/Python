# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:48:59 2018

@author: Actiview
"""
import pandas as pd
import numpy as np

#indices = ["tCompletionToDone", "tCompletion", "tDone"]
            
def t_delta(t1, t2):
    t_delta = round((t1 -t2), 3)
    return t_delta

def mis_aspot(l1):
    c = len(l1)
    if c < 7:
        for i in range(7 - c):
            l1.append(0)
    else:
        return l1
    return l1 

dn1, dn2 ,dn3 = [], [], []
def main(d, filename, dn1, dn2, dn3):
    global user_id
    flow_l, comp_l = [], []
    if filename == "Settings.json":
        user_id = d.get("userID")
    elif filename == "EventSeries.json":
        for event in d:
            if event.get('$type') == 'Actiview.Logger.Events.FlowEvent, Actiview.Logger':
                level = event.get('level')
                state = event.get('state')
                time1 = event.get('Time')
                if (level == 3 and state == 1):
                    etype = 'endFlow'
                    flow_l.append([etype, time1])
                    comp_l.append([etype, time1])
                elif(level == 3 and state == 0):
                    etype = 'startFlow'
                    comp_l.append([etype, time1])                   
            elif event.get('$type') == 'Actiview.Logger.Events.ContainerFilledEvent, AssenseObjects':
                etype = 'shelf'
                time2 = event.get('Time')
                flow_l.append([etype, time2])
    #tCompletionToDone      
        dif_end = []
        t1, t2 = 0.0, 0.0
        for i, (item, time) in enumerate(flow_l):
            if item == 'endFlow':
                t1 = time
                i2 = i - 1
                t2 = flow_l[i2]
                if t2[0] == 'shelf':
                    delta = t_delta(t1, t2[1])
                elif t2[0] == 'endFlow':
                    continue
                dif_end.append(delta)
        
        try:
            if dif_end[6]:
                pass
        except IndexError:
            mis_aspot(dif_end)
        finally:
            pass
        
    #tCompletion
        dif_full, dif_done = [], []
        for ci, (cItem, cTime) in enumerate(comp_l):
            if item == 'endFlow':
                t_end = cTime
                i_start = ci - 1
                t_start = comp_l[i_start]
                delta_full = t_delta(t_end, t_start[1])
            if delta_full > 0.0 : dif_full.append(delta_full)
        dif_d = np.subtract(dif_full, dif_end)
        dif_done = list(dif_d)
        d1 = pd.DataFrame([dif_end], index = [user_id], columns = [1, 2, 3, 4, 5, 6, 7])
        d2 = pd.DataFrame([dif_done], index = [user_id], columns = [1, 2, 3, 4, 5, 6, 7])
        d3 = pd.DataFrame([dif_full], index = [user_id], columns = [1, 2, 3, 4, 5, 6, 7])
        dn1.append(d1)
        dn2.append(d2)
        dn3.append(d3)                        
      
        #save_json([dn1, dn2, dn3], path_to_json, indices)

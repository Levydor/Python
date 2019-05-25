# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:48:59 2018

@author: Actiview
"""
import numpy as np
import pandas as pd
import warnings

#indices = ["tObjDelta", "tObjDeltaSum", "tObjDeltaSumDivCount"]

def t_delta(t1, t2):
    t_delta = round((t1 -t2), 3)
    return t_delta

dn4, dn5, dn6 = [], [], []
def main(d, filename, dn4, dn5, dn6):
    global user_id
    slot = []
    if filename == "Settings.json":
        user_id = d.get("userID")
    elif filename == "EventSeries.json":
        for event in d:
            if event.get('$type') == 'Actiview.Logger.Events.FlowEvent, Actiview.Logger':
                name = event.get ('name')
                level = event.get('level')
                state = event.get('state')
                time = event.get('Time')
                if (any(c in name for c in ('3', '4', '5', '6')) and level == 3 and state == 0):
                    etype = 'startFlow'
                    slot.append([etype, time])                   
            elif event.get('$type') == 'Actiview.Logger.Events.ContainerFilledEvent, AssenseObjects':
                c_time = event.get('Time')
                container = event.get('container')
                c_name = container['name']
                if c_name == 'Slot_0X0' : slot.append(['s00', c_time])
                elif c_name == 'Slot_0X1' : slot.append(['s01', c_time])
                elif c_name == 'Slot_1X0' : slot.append(['s10', c_time])
                elif c_name == 'Slot_1X1' : slot.append(['s11', c_time])
                elif c_name == 'Slot_2X0' : slot.append(['s20', c_time])
                elif c_name == 'Slot_2X1' : slot.append(['s21', c_time])
                elif c_name == 'Slot_0X2' : slot.append(['s02', c_time])
                elif c_name == 'Slot_0X3' : slot.append(['s03', c_time])
                elif c_name == 'Slot_1X2' : slot.append(['s12', c_time])
                elif c_name == 'Slot_1X3' : slot.append(['s13', c_time])
                elif c_name == 'Slot_2X2' : slot.append(['s22', c_time])
                elif c_name == 'Slot_2X3' : slot.append(['s23', c_time])
                elif c_name == 'Slot_0X4' : slot.append(['s04', c_time])
                elif c_name == 'Slot_0X5' : slot.append(['s05', c_time])
                elif c_name == 'Slot_1X4' : slot.append(['s14', c_time])
                elif c_name == 'Slot_1X5' : slot.append(['s15', c_time])
                elif c_name == 'Slot_2X4' : slot.append(['s24', c_time])
                elif c_name == 'Slot_2X5' : slot.append(['s25', c_time])
        
        #deleting rounds [1-3] data
        pos_d, p = [], []
        l, i = 0, 0
        for n, (o, t) in enumerate(slot):
            if o == 'startFlow':
                pos_d.append(n)                        
        if len(pos_d) > 0:
            del(slot[:pos_d[0]])
            l = len(pos_d)
            p = list(np.subtract(pos_d, [pos_d[0]]*l))
        
        obj_total_delta = []
        matrix_rnd4 = np.full((1,9),np.nan)
        matrix_rnd5 = np.full((1,9),np.nan)
        matrix_rnd6 = np.full((3,9),np.nan)
        matrix_rnd7 = np.full((9,9),np.nan)
        for i, (s,t) in enumerate(slot):
            #round 4
            if i < p[1]:
                a1 = 0
                for x, y in zip(slot[p[0]:p[1]], slot[p[0]+1:p[1]]):
                    if x[0] == 's02' and y[0] == 's03' or x[0] == 's03' and y[0] == 's02':
                        matrix_rnd4[0][a1] = (t_delta(y[1], x[1]))
                        a1 += 1
            #round 5
            if i > p[1] and i < p[2]:
                a2 = 0
                for x, y in zip(slot[p[1]:p[2]], slot[p[1]+1:p[2]]):
                    if x[0] == 's02' and y[0] == 's03' or x[0] == 's03' and y[0] == 's02':
                        matrix_rnd5[0][a2] = (t_delta(y[1], x[1]))
                        a2 += 1
            #round 6
            elif i > p[2] and i < p[3]:
                e1, e2, e3 = 0, 0, 0
                for x, y in zip(slot[p[2]:p[3]], slot[1+p[2]:1+p[3]]):
                    if x[0] == 's00' and y[0] == 's01' or x[0] == 's01' and y[0] == 's00':
                        matrix_rnd6[0][e1] = (t_delta(y[1], x[1]))
                        e1 += 1
                    elif x[0] == 's10' and y[0] == 's11' or x[0] == 's11' and y[0] == 's10':
                        matrix_rnd6[1][e2] = (t_delta(y[1], x[1]))
                        e2 += 1
                    elif x[0] == 's20' and y[0] == 's21' or x[0] == 's21' and y[0] == 's20':
                        matrix_rnd6[2][e3] = (t_delta(y[1], x[1]))
                        e3 += 1
                        
            #round 7
            elif i > p[3]:
                i1, i2, i3, i4, i5, i6, i7, i8, i9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
                for x, y in zip(slot[p[3]:], slot[1+p[3]:]):
                    if x[0] == 's00' and y[0] == 's01' or x[0] == 's01' and y[0] == 's00':
                        matrix_rnd7[0][i1] = (t_delta(y[1], x[1]))
                        i1 += 1
                    elif x[0] == 's10' and y[0] == 's11' or x[0] == 's11' and y[0] == 's10':
                        matrix_rnd7[1][i2] = (t_delta(y[1], x[1]))
                        i2 += 1
                    elif x[0] == 's20' and y[0] == 's21' or x[0] == 's21' and y[0] == 's20':
                        matrix_rnd7[2][i3] = (t_delta(y[1], x[1]))
                        i3 += 1
                    elif x[0] == 's02' and y[0] == 's03' or x[0] == 's03' and y[0] == 's02':
                        matrix_rnd7[3][i4] = (t_delta(y[1], x[1]))
                        i4 += 1
                    elif x[0] == 's12' and y[0] == 's13' or x[0] == 's13' and y[0] == 's12':
                        matrix_rnd7[4][i5] = (t_delta(y[1], x[1]))
                        i5 += 1
                    elif x[0] == 's22' and y[0] == 's23' or x[0] == 's23' and y[0] == 's22':
                        matrix_rnd7[5][i6] = (t_delta(y[1], x[1]))
                        i6 += 1
                    elif x[0] == 's04' and y[0] == 's05' or x[0] == 's05' and y[0] == 's04':
                        matrix_rnd7[6][i7] = (t_delta(y[1], x[1]))
                        i7 += 1
                    elif x[0] == 's14' and y[0] == 's15' or x[0] == 's15' and y[0] == 's14':
                        matrix_rnd7[7][i8] = (t_delta(y[1], x[1]))
                        i8 += 1
                    elif x[0] == 's24' and y[0] == 's25' or x[0] == 's25' and y[0] == 's24':
                        matrix_rnd7[8][i9] = (t_delta(y[1], x[1]))
                        i9 += 1
        

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            try:
                obj_r4_delta = np.nanmean(matrix_rnd4, axis = 1)
            except RuntimeWarning:
                obj_r4_delta=np.NaN
            try:
                obj_r5_delta = np.nanmean(matrix_rnd5, axis = 1)
            except RuntimeWarning:
                obj_r5_delta=np.NaN
            try:
                obj_r6_delta = np.nanmean(matrix_rnd6, axis = 1)
            except RuntimeWarning:
                obj_r6_delta=np.NaN
            try:
                obj_r7_delta = np.nanmean(matrix_rnd7, axis = 1)
            except RuntimeWarning:
                obj_r7_delta=np.NaN
        
        obj_total_delta = np.append(obj_total_delta, obj_r4_delta, axis=0)
        obj_total_delta = np.append(obj_total_delta, obj_r5_delta, axis=0)
        obj_total_delta = np.append(obj_total_delta, obj_r6_delta, axis=0)
        obj_total_delta = np.append(obj_total_delta, obj_r7_delta, axis=0)
        obj_delta_sum ,obj_delta_avg = 0.0, 0.0
        obj_delta_sum = np.nansum(obj_total_delta)
        obj_delta_avg = np.nanmean(obj_total_delta)

        d4 = pd.DataFrame([obj_total_delta], index = [user_id])
        d5 = pd.DataFrame([obj_delta_sum], index = [user_id])
        d6 = pd.DataFrame([obj_delta_avg], index = [user_id])
        dn4.append(d4)
        dn5.append(d5)
        dn6.append(d6)
   
    #save_json([dn4, dn5, dn6], path_to_json, indices)
            


                  
                    

                            
                                



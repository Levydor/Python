# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:48:59 2018

@author: Actiview
"""
import numpy as np
import pandas as pd

#indices = ['r_nObjSelectedPerShelf', 'r_t1stSolution', 'r_t1stSolutionToDone']

def t_delta(t1, t2):
    delta = round(t1, 4) - round(t2, 4)
    t_delta = round(delta, 4)
    return t_delta

def side(s1):
    if int(s1[-1:]) % 2 == 0:
        return 'l'
    else:
        return 'r'
    
def offside(l1, l2):
    if side(l1) != side(l2):
        return True
    else:
        return False

dn8, dn9, dn10 = [], [], []
def main(d, filename, dn8, dn9, dn10):
    global user_id
    ans, cont, arpl, rprnd, nitem, sol1 = [], [], [], [], [], []
    if filename == "Settings.json":
        user_id = d.get("userID")
        #print(user_id)
    elif filename == "EventSeries.json":
        for event in d:
            if event.get('$type') == 'Actiview.Logger.Events.FlowEvent, Actiview.Logger':
                name = event.get ('name')
                level = event.get('level')
                state = event.get('state')
                time = event.get('Time')
                if (level == 3 and state == 0):
                    etype = 'round'
                    cont.append([etype, name])
                    ans.append([etype, name])
                    arpl.append([etype, time])
            elif event.get('$type') == 'Actiview.Logger.Events.ContainerFilledEvent, AssenseObjects':
                c_time = event.get('Time')
                container = event.get('container')
                c_name = container['name']
                cont.append(['cont', c_name])
                arpl.append([c_name, c_time])
            elif event.get('$type') == 'Actiview.Logger.Events.AnalogiesRoundResultEvent, AssenseObjects':
                answer = event.get('Answer')
                obj_set = answer['ObjectSets']
                for o in obj_set:
                    left_o = (o.get('LeftObject'))['uid']
                    right_o = (o.get('RightObject'))['uid']
                    if not((o.get('LeftObject'))['name'][:3]=='Ref' and (o.get('RightObject'))['name'][:3]=='Ref') and not(right_o =='NAN/NoAnswer'):
                        ans.append(['r',right_o])
                        if left_o.find('Ref') < 0 and left_o.find('NAN/NoAnswer') < 0:
                            ans.append(['l',left_o])
        
        sard1_3 = np.full((3,1), 0.0)
        sard4_5 = np.full((2,1), 0.0)
        ard1_3 = np.full((3,1), 0.0)
        ard4_5 = np.full((2,1), 0.0)
        rnd = np.full(7, 0.0)
        ornd = np.full(7, 0.0)

        cont.append(['round', 'end'])
        
#r_nObjSelectedPerShelf
        #container
        r, count = -1, 0.0
        for t, c in cont:
            if t != 'round':
                count += 1.0
            elif t == 'round':
                r += 1
                if r>0:
                    rnd[r-1] = count
                    count = 0.0
                    
        ans.append(['round', 'end'])
        #round result
        r, count = -1, 0.0
        for t, c in ans:
            if t != 'round':
                count += 1.0
            elif t == 'round':
                r += 1
                if r > 0:
                    ornd[r-1] = count
                    count = 0.0
        
        nitem = list(np.round(np.divide(rnd, ornd), 2))

        apos = []
        for n, (o, t) in enumerate(arpl):
            if o == 'round':
                apos.append(n)
                
# 1st Solution
        # round 1-3
        n, rnd_t = 0, 0.0
        for i, (co, t) in enumerate(arpl):
            if i < apos[3]:
                if co == 'round':
                    rnt = arpl[i][1]
                elif co[:1] == 'S':
                    if arpl[i-1][0][:1] == 'S':
                        pass
                    elif arpl[i-1][0] == 'round':
                        sard1_3[n] = t_delta(arpl[i][1],rnt)
                        rnt = 0.0
                        n += 1
                    
        # round 4-5
        n, rnd_t = 0, 0.0
        for x, y in zip(arpl[apos[3]:apos[5]], arpl[1+apos[3]:apos[5]]):
            if x[0] == 'round' and y[0][:1] == 'S':
                rnd_t = x[1]
            elif x[0][:1] == 'S' and y[0][:1] == 'S':
                if n < 2 and rnd_t > 0:
                    if offside(x[0], y[0]):
                        sard4_5[n] = t_delta(y[1], rnd_t)
                        rnd_t = 0.0
                else:
                    pass
            elif x[0][:1] == 'S' and y[0] == 'round':
                n += 1
                pass
            elif x[0] == 'round' and y[0] == 'round':
                sard4_5[n] = 0
                n += 1
        
        sol1 = np.append(sol1, sard1_3)
        sol1 = np.append(sol1, sard4_5)
        
# 1st Solution To Done
        # round 1-3
        n, st = 0, 0.0
        for i, (co, t) in enumerate(arpl):
            if i < (apos[3] + 1) and i > 0:
                if co[:1] == 'S':
                    st = arpl[i][1]
                elif co == 'round':
                    ard1_3[n] = t_delta(arpl[i][1], st)
                    n += 1
                    st = 0.0
                    
        # round 4-5
        n, var = 0, 0.0 
        for x, y in zip(arpl[1+apos[3]:apos[5]], arpl[2+apos[3]:1+apos[5]]):
            if x[0] == 'round' and y[0][:1] == 'S':
                n += 1
                pass
            elif x[0][:1] == 'S' and y[0][:1] == 'S':
                if offside(x[0], y[0]):
                    var = y[1]
            elif x[0][:1] == 'S' and y[0] == 'round':
                if  n < 2:
                    if var > 0:
                        ard4_5[n] = t_delta(y[1], var)
                        var = 0.0
                    else:
                        ard4_5[n] = 0.0
            elif x[0] == 'round' and y[0] == 'round':
                ard4_5[n] = 0
                n += 1
        
        rprnd = np.append(rprnd, ard1_3)
        rprnd = np.append(rprnd, ard4_5)
        
        d8 = pd.DataFrame([nitem], index = [user_id])
        d9 = pd.DataFrame([sol1], index = [user_id])
        d10 = pd.DataFrame([rprnd], index = [user_id])

        dn8.append(d8)
        dn9.append(d9)
        dn10.append(d10)
        
    #save_json([dn8, dn9, dn10], path_to_json, indices)

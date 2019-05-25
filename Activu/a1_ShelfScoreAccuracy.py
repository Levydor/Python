# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:48:59 2018

@author: Actiview
"""
import numpy as np
import pandas as pd

#indices = ['ShelfScoreAccuracy']

def is_equal(ans, usr):
    for o, u in ans:
        equal = False
        if o != 'round' and o == 'r':
            for ob, uid in usr:
                if ob != 'startFlow' and ob == 'u_r':
                    if u == uid:
                        equal = True
                    elif pd.isnull(uid):
                        return None
            if not equal:
                return False
    return True

def shelf_equal(l_ans, l_user):
    c1, c2, c3, c4 = False ,False, False, False
    c = None
    for o, u in l_ans:
        if not (c1 and c2) and not (c3 and c4):
            if o != 'round' and o == 'r':
                for ob, uid in l_user:
                    if ob != 'startFlow':
                        if ob == 'u_r':
                            if u == uid:
                                c1 = True
                                break
                            else:
                                c1 = False
                        elif ob == 'u_l':
                            if u == uid:
                                c3 = True
                                break
                            else:
                                c3 = False
            elif o != 'round' and o == 'l':
                for ob, uid in l_user:
                    if ob != 'startFlow':
                        if ob == 'u_l':
                            if u == uid:
                                c2 = True
                                break
                            else:
                                c2 = False
                        elif ob == 'u_r':
                            if u == uid:
                                c4 = True
                                break
                            else:
                                c4 = False
        else:
            break                        
    if c1 and c2:
        c = 1
    elif c3 and c4:
        c = 0.5
    else:
        c = 0
    return c

# main feature program
def main(d, filename, dn0):
    global user_id
    ans_u, ans = [], []
    if filename == "Settings.json":
        user_id = d.get("userID")
    elif filename == "EventSeries.json":
        for event in d:
            if event.get('$type') == 'Actiview.Logger.Events.FlowEvent, Actiview.Logger':
                name = event.get ('name')
                level = event.get('level')
                state = event.get('state')
                if (level == 3 and state == 0):
                    etype = 'startFlow'
                    ans_u.append([etype, name])
            elif event.get('$type') == 'Actiview.Logger.Events.AnalogiesRoundResultEvent, AssenseObjects':
                answer = event.get('Answer')
                object_set = answer['ObjectSets']
                for ui in object_set:
                    try:
                        left_o = (ui.get('LeftObject'))['name']
                        right_o = (ui.get('RightObject'))['name']
                        ans_u.append(['u_r',right_o])
                        ans_u.append(['u_l',left_o])
                    except KeyError:
                        pass
            elif event.get('$type') == 'Actiview.Logger.Events.InitAnalogiesEvent, AssenseObjects':      
                answers = event.get('Answers')
                for i, obj_s in enumerate(answers):
                    obj_set = obj_s.get('ObjectSets')
                    ans.append(['round',i])
                    for uid in obj_set:
                        left_o = (uid.get('LeftObject'))['name']
                        right_o = (uid.get('RightObject'))['name']
                        if not((uid.get('LeftObject'))['name'][:3]=='Ref' and (uid.get('RightObject'))['name'][:3]=='Ref'):
                            ans.append(['r',right_o])
                            ans.append(['l',left_o])
      
        matrix_total, p = [], []
        for n, (o, t) in enumerate(ans_u):
            if o == 'startFlow':
                p.append(n)
    
        ans_u6 = ans_u[p[5]+1:p[6]]
        ans_u7 = ans_u[p[6]:]
        matrix_rnd1_3 = np.full((3,1), np.nan)
        matrix_rnd4_5 = np.full((2,1), np.nan)
        matrix_rnd6 = np.full((3,1), np.nan)
        matrix_rnd71 = np.full((3,1), np.nan)
        matrix_rnd72 = np.full((3,1), np.nan)
        matrix_rnd73 = np.full((3,1), np.nan)
        
        #round 1-3
        i, n, d = 0, 0, 0
        c = None
        while i < 3:
            if is_equal(ans[p[i]:p[i+1]], ans_u[p[i]:p[i+1]]):
                c = 1
            else:
                c = 0
            matrix_rnd1_3[i] = c
            i += 1
    
        #round 4_5
        c = None
        e = 0
        for e in range(2):
            matrix_rnd4_5[e] = (shelf_equal(ans[p[i]:p[i+1]], ans_u[p[i]:p[i+1]]))
            i += 1
            
        #round 6
        e = 0
        for n in range(0,len(ans_u6),2):
            matrix_rnd6[e] = (shelf_equal(ans[p[i]:p[i+1]],ans_u6[n:n+2]))
            e += 1
        
        #round 7
        sp = p[6]+1
        ans71 = ans[sp:sp+6]
        ans72 = ans[sp+6:sp+12]
        ans73 = ans[sp+12:]
        i += 1
        n = 0
        for d in range(len(ans_u7)):
            if n < 9:
                if n < 3 and d % 2 == 0:
                    matrix_rnd71[n] = (shelf_equal(ans71[d:d+2], ans_u7[1:7]))
                    n += 1
                elif n > 2 and n < 6 and d % 2 == 0:
                    matrix_rnd72[n - 3] = (shelf_equal(ans72[d-6:d-4], ans_u7[7:13]))
                    n += 1
                elif n > 5 and d % 2 == 0:
                    matrix_rnd73[n - 6] = (shelf_equal(ans73[d-12:d-10], ans_u7[13:]))
                    n += 1
        
        matrix_total = np.append(matrix_total, matrix_rnd1_3)
        matrix_total = np.append(matrix_total, matrix_rnd4_5)
        matrix_total = np.append(matrix_total, (matrix_rnd6, matrix_rnd71, matrix_rnd72, matrix_rnd73 ))
        d0 = pd.DataFrame([matrix_total], index = [user_id])
        dn0.append(d0)
        
    #save_json([dn0], path_to_json, indices)
        
                           



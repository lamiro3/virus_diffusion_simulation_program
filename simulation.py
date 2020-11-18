import turtle as t
from random import *
import numpy as np
from graph import *
import matplotlib.pylab as plt

#start = time.time() # 시뮬레이션 시작할 때 시간
# code: 0 = S, 1 = I, 2 = R
cnt = 0 # 날짜수 (일)
case_code = []
distance = []
x_input = []
t_input = []
beta = 0

def begin_simulation(x, y, num, INUM): # 시뮬레이션 시작
    global cnt
    global case_code
    global distance
    global S
    global I
    global R
    global x_input
    global t_input
    global beta

    if cnt == 0:
        distance = [0]*num
        case_code = [0]*num
        S = 0
        I = 0
        R = 0
        x_input = [0]*3

    if R == num: # 시뮬레이션 종료
        t.exitonclick()
        print(f'모두가 회복되기까지 총 {cnt}일이 소요되었습니다.')
        return
    
    t.setup(width = 1000, height = 1000)
    t.ht()
    t.penup()
    t.speed(0)

    for i in range(num):
        if i+1 == INUM:
            if case_code[INUM-1] != 2:
                case_code[INUM-1] = 1
            else:
                case_code[INUM-1] = 2
            continue
        t.goto(x[f'cx{i+1}'], y[f'cy{i+1}']) # 최초 감염자 외의 위치

        if case_code[i] == 0:
            t.dot(20,'blue')
        elif case_code[i] == 1:
            t.dot(20,'red')
        elif case_code[i] == 2:
            t.dot(20, 'green')

    t.goto(x[f'cx{INUM}'], y[f'cy{INUM}']) # 최초 감염자 위치
    t.dot(20,'red')
    i_pos = t.position() # 최초 감염자 위치

    if cnt >= 1:
        case_code, beta = activation_infect(x, y, num, distance, i_pos, case_code)
    if I >= num*(3/5) or S <= num*(2/5):
        case_code = activation_recover(x, y, num, case_code)

    S, I, R = countSIR(num, case_code)
    print(f'{S},{I},{R}')

    x_input[0] = S
    x_input[1] = I
    x_input[2] = R
    t_input = np.linspace(0, cnt)
    plot_(SIR, x_input, t_input, beta, 1/14, num)

    t.clear()
    cnt = cnt + 1
    moving(x, y, num, INUM)

def moving(x, y, num, INUM): # 위치 변경
    for i in range(num):
        x[f'cx{i+1}'] = randint(-400, 400)
        y[f'cy{i+1}'] = randint(-400, 400)
    begin_simulation(x, y, num, INUM)

def activation_infect(x, y, num, dis, pos, code): # 감염 활성화 함수
    S = 0

    for i in range(num):
        if code[i] == 0: 
            S+=1
    if S > 0:
        beta = (1/14)*5/S # 감염률(한국 기준)
    else:
        beta = 0

    S = 0

    for k in range(num):
        dis[k] = t.distance(pos)
    
    for j in range(num):
        if dis[j] <= 100 and beta >= uniform(0, 1):
            code[j] = 1
    
    return code, beta

def activation_recover(x, y, num, code): # 회복 활성화 함수
    GAMMA = 1/14
    for i in range(num):
        if code[i] == 1 and GAMMA >= uniform(0, 1):
            code[i] = 2
    
    return code

def countSIR(num, code):
    S = 0
    I = 0
    R = 0
    for i in range(num):
        if code[i] == 0:
            S+=1
        elif code[i] == 1:
            I+=1
        elif code[i] == 2:
            R+=1
    
    return S, I, R
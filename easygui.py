#!/usr/bin/env python
# coding: utf-8

# # 最优化方法课程作业
# 
# * 使用方法：依次运行以下文件，会弹出运行主窗口，通过点击相应的按钮进行操作
# * 注意事项：单纯形法仅能输入约束条件为等式的矩阵，输入矩阵时注意使用空格与换行对数据进行划分

# ## 文件1：单纯形法实现

# In[29]:


import numpy as np
import decimal

# 一组测试数据
obj = np.array([-4, -1, 0, 0, 0])
st = np.array([[-1, 2, 1, 0, 0, 4],[2, 3, 0, 1, 0, 12],[1, -1, 0, 0, 1, 3]])

def simplex(obj, st):
    # 输出在控制台上的字符串
    res = ''
    obj = np.array(obj)
    st = np.array(st)
    row, column = st.shape
    A = np.delete(st, column-1, 1)
    b = st[:,column-1]
    p = np.array([example for example in A.T])
    # 取后几个数字的索引
    index = [e for e in range(len(p))][-row:]
    while(True):
        B = p[index].T

        # B矩阵求逆
        B_inv = np.linalg.inv(B)
        xb = np.matmul(B_inv,b)

        # 得到的一个目标值
        cb = obj[index]
        # 使用近似值，解决浮点运算不准确的问题
        f = np.around(cb@xb)
        res+= '基本可行解{}\n'.format(f)

        # 单纯形乘子
        w = cb@B_inv

        # 计算判别数，存储在字典中
        judge = {}
        for i,_ in enumerate(p):
            if i not in index:
                judge[i] = w@p[i]-obj[i]

        # 所有判别数都小于0，停止迭代
        if(max(judge.values())<=0):
            print("找到最优解的值为{}".format(f))
            res+='最优解为{}'.format(f)
            return log_issue(obj,st) + res
#         else:
#             print("继续迭代")

        # 获取最大值的索引, xk为进基变量
        k = max(judge, key=judge.get)

        yk = B_inv@p[k]

        # 判断yk>0中是否有True。使用in直接判断有逻辑错误，因此将所有布尔值相或
        bo = False
        for e in yk>0:
            bo = bo|e
        if(not bo):
            print("该问题不存在最优解")
            return np.nan

        # 选择下标r，xr为离基变量
        dic = {}
        for i,_ in enumerate(yk):
            if(yk[i]>0):
                dic[i]=b[i]/yk[i]
        r = min(dic, key=dic.get)
        # 由index确定p变量
        index[r] = k

def log_issue(obj, st):
    variable = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']
    # 返回的字符串，打印在控制台上
    res = ''
    # 打印目标函数
    print("min\t", end='')
    res+="min\t"
    for i,num in enumerate(obj):
        if(num<0):
            print('{num}*{var}'.format(num=num, var=variable[i]), end='')
            res+='{num}*{var}'.format(num=num, var=variable[i])
        elif(num>0 and i!=0):
            print('+{num}*{var}'.format(num=num, var=variable[i]), end='')
            res+='+{num}*{var}'.format(num=num, var=variable[i])
        elif(num>0 and i==0):
            print('{num}*{var}'.format(num=num, var=variable[i]), end='')
            res+='{num}*{var}'.format(num=num, var=variable[i])
    print()
    res+='\n'
    # 打印约束条件
    row, column = st.shape
    print("s.t.\t", end='')
    res+=("s.t.\t")
    for j in range(row):
        for i,num in enumerate(st[j]):
            if(i==(len(st[j])-1)):
                print('={num}'.format(num=num))
                res+='={num}'.format(num=num)
            else:
                if(num<0):
                    print('{num}*{var}'.format(num=num, var=variable[i]), end='')
                    res+='{num}*{var}'.format(num=num, var=variable[i])
                elif(num>0 and i!=0):
                    print('+{num}*{var}'.format(num=num, var=variable[i]), end='')
                    res+='+{num}*{var}'.format(num=num, var=variable[i])
                elif(num>0 and i==0):
                    print('{num}*{var}'.format(num=num, var=variable[i]), end='')
                    res+='{num}*{var}'.format(num=num, var=variable[i])
        print("\t", end='')
        res+="\n\t"
    res+="\n"    
    return res
        
log_issue(obj, st)
print(simplex(obj, st))


# ## 文件2：运输问题实现

# In[2]:


import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

def find_initial_solution(costs, demand, supply):
    C = np.copy(costs)
    d = np.copy(demand)
    s = np.copy(supply)

    # Get the shape of costs-matrix
    n, m = C.shape

    # Create the matrix of basic values and convert cost to one-dim array
    X = np.zeros((n, m))
    indices = [(i, j) for i in range(n) for j in range(m)]
    xs = sorted(zip(indices, C.flatten()), key=lambda kv: kv[1])

    # Find initial solution
    for (i, j), _ in xs:
        if d[j] == 0:
            continue
        else:
            # Reserving supplies in a greedy way
            remains = s[i] - d[j] if s[i] >= d[j] else 0
            grabbed = s[i] - remains
            X[i, j] = grabbed
            s[i] = remains
            d[j] -= grabbed
    return X


def find_potential(X, C):
    n, m = X.shape

    u = np.array([np.nan] * n)
    v = np.array([np.nan] * m)

    _x, _y = np.where(X > 0)
    nonzero = list(zip(_x, _y))
    f = nonzero[0][0]
    u[f] = 0

    while any(np.isnan(u)) or any(np.isnan(v)):
        for i, j in nonzero:
            if np.isnan(u[i]) and not np.isnan(v[j]):
                u[i] = C[i, j] - v[j]
            elif not np.isnan(u[i]) and np.isnan(v[j]):
                v[j] = C[i, j] - u[i]
            else:
                continue
    return u, v


def transport(costs, demand, supply):
    # Get initials solution
    n, m = costs.shape
    X = find_initial_solution(costs, demand, supply)
    
    # 打印在控制台上的值
    res = ''
    print("基本可行解:", np.sum(X * costs))
    res += "基本可行解：{}\n".format(np.sum(X * costs))


    while True:
        S = np.zeros((n, m))

        # Find potentials
        u, v = find_potential(X, costs)

        # Find S - matrix
        for i in range(n):
            for j in range(m):
                S[i, j] = costs[i, j] - u[i] - v[j]

        # Condition to break
        s = np.min(S)
        if s >= 0:
            print("求得的最优解为：", np.sum(X * costs))
            res += "求得的最优解为：{}\n".format(np.sum(X * costs))

            break

        i, j = np.argwhere(S == s)[0]
        start = (i, j)

        # print(start)
        # Find cycle elements

        T = np.copy(X)
        T[start] = 1
        while True:
            _xs, _ys = np.nonzero(T)
            xcount, ycount = Counter(_xs), Counter(_ys)

            for x, count in xcount.items():
                if count <= 1:
                    T[x, :] = 0
            for y, count in ycount.items():
                if count <= 1:
                    T[:, y] = 0

            if all(x > 1 for x in xcount.values())                     and all(y > 1 for y in ycount.values()):
                break
        # print(T)

        # Finding cycle order
        dist = lambda kv1, kv2: abs(kv1[0] - kv2[0]) + abs(kv1[1] - kv2[1])
        fringe = [tuple(p) for p in np.argwhere(T > 0)]
        # print(fringe)

        size = len(fringe)

        path = [start]
        while len(path) < size:
            last = path[-1]
            if last in fringe:
                fringe.remove(last)
            next = min(fringe, key=lambda kv: dist(last, (kv[0], kv[1])))
            path.append(next)

        # Improving solution on cycle elements
        neg = path[1::2]
        pos = path[::2]
        q = min(X[list(zip(*neg))])

        # Print optimal solution
        if q == 0:
            print("基本可行解:", np.sum(X * costs))
            res += "基本可行解{}\n".format(np.sum(X * costs))

        # Improve solution
        X[list(zip(*neg))] -= q
        X[list(zip(*pos))] += q

        # Print table after improving
        print("基本可行解:", np.sum(X * costs))
        res += "基本可行解{}\n".format(np.sum(X * costs))
    
    return res


# ## 文件3 工具类
# 打印时间

# In[3]:


import time
# 获取时间，打印在控制台上
def get_current_time():
    time_stamp = time.time()  # 当前时间的时间戳
    local_time = time.localtime(time_stamp)  #
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return str_time

get_current_time()


# ## 文件四 UI界面实现
# 借助于TKinker实现

# In[40]:


from tkinter import *
from tkinter import scrolledtext
from PIL import Image, ImageTk


# 打印出信息到下方文本区域
def log(str='--------'*10):
    text.insert('end',str)
    text.insert('end','\n')
    text.see('end')

def log_clear():
    text.delete('1.0','end')
    init()
    
def solve_simplex():
    log("单纯形法求解")

# 弹出一个新窗口
def create_sim():
    global top
    top = Toplevel()
    top.title('simplex')
    
    top.geometry('600x350')
#     v1 = StringVar()
#     e1 = Entry(top,textvariable=v1,width=10)
#     e1.grid(row=1,column=0,padx=1,pady=1)

#     Button(top, text='出现2级').grid(row=1,column=1,padx=1,pady=1)
   
    
     # 一个简单的提示标签，可以修改一些字体之类
    label = Label(top, text="请在此输入系数矩阵")
    label.pack()

    btn = Button(top, text="使用默认值", command=default_simplex)
    btn.pack()
    
    confirm = Button(top, text="输入完毕", command=count_sim)
    confirm.pack()
    
    # 创建一个文本框放在frame上，经常报错text_top not found，因此使用global修饰符
    global text_top 
    text_top = scrolledtext.ScrolledText(top)
    text_top.pack()
    
#     text = Entry(window, width=500, height=200)
#     text.pack()

# 弹出运输窗口
def create_tran():
    global top
    top = Toplevel()
    top.title('transport')
    
    top.geometry('600x350')
#     v1 = StringVar()
#     e1 = Entry(top,textvariable=v1,width=10)
#     e1.grid(row=1,column=0,padx=1,pady=1)

#     Button(top, text='出现2级').grid(row=1,column=1,padx=1,pady=1)
   
    
     # 一个简单的提示标签，可以修改一些字体之类
    label = Label(top, text="请在此输入系数矩阵")
    label.pack()

    btn = Button(top, text="使用默认值", command=default_transport)
    btn.pack()
    
    confirm = Button(top, text="输入完毕", command=count_tran)
    confirm.pack()
    
    # 创建一个文本框放在frame上，经常报错text_top not found，因此使用global修饰符
    global text_top 
    text_top = scrolledtext.ScrolledText(top)
    text_top.pack()

# 弹出框中，使用默认的参数矩阵
def default_simplex():
    arr = '-4 -1 0 0 0\n-1 2 1 0 0 4\n2 3 0 1 0 12\n1 -1 0 0 1 3\n'
    text_top.delete('1.0', 'end')
    text_top.insert('end', arr)

# 弹出框中，使用默认的参数矩阵
def default_transport():
    arr = '23 25 12 30\n18 18 18 18 18\n3 25 11 22 12\n9 15 4 26 12\n13 22 15 12 27\n6 19 8 11 8'
    text_top.delete('1.0', 'end')
    text_top.insert('end', arr)
    
# 单纯形法运算，并销毁弹出框，将结果输出到控制台
def count_sim():
    param = text_top.get('0.0','end')
    print(param)
    top.destroy()
    # 进行运算
    arr = param.strip().split('\n')
    obj = [float(f) for f in arr[0].strip().split()]
    
    st = []
    # 使用filter去除空的列表
    for str in filter(None,arr[1:]):
        st.append([float(f) for f in str.strip().split()])
    print(obj, st)
    res = simplex(obj, st)
    log('\n')
    log('='*30+get_current_time()+'='*30)
    log(res)
    log('\n')
    
def count_tran():
    param = text_top.get('0.0','end')
    print(param)
    top.destroy()
    # cost demand sumply
    # 进行运算
    arr = param.strip().split('\n')
    sumply = np.array([float(f) for f in arr[0].strip().split()])
    demand = np.array([float(f) for f in arr[1].strip().split()])
    
    costs = []
    # 使用filter去除空的列表
    for str in filter(None,arr[2:]):
        costs.append([float(f) for f in str.strip().split()])
    costs = np.array(costs)
    print(costs, demand, sumply)
    res = transport(costs, demand, sumply)
    log('\n')
    log('='*30+get_current_time()+'='*30)
    log(res)
    log('\n')
    
# 初始化，目前仅初始化打印区
def init():
    time = get_current_time()
    log('='*30+time+'='*30)
    log()
    log('''\t _____   _       ___  ___   _____   _       _____  __    __ 
\t/  ___/ | |     /   |/   | |  _  \ | |     | ____| \ \  / / 
\t| |___  | |    / /|   /| | | |_| | | |     | |__    \ \/ /  
\t\___  \ | |   / / |__/ | | |  ___/ | |     |  __|    }  {   
\t ___| | | |  / /       | | | |     | |___  | |___   / /\ \  
\t/_____/ |_| /_/        |_| |_|     |_____| |_____| /_/  \_\ ''')
    log('\n')
    log('\t\t\tAuthor:wangdong\t\tID:2020317041')
    log("\t\t\tHello, program is ready to work")
    log("\t\t\tPlease click the button to setup program")
    log('\n')
    log()
    
def about():
    top = Toplevel()
    top.title('About')
    top.geometry('600x400')
   
    text_top = scrolledtext.ScrolledText(top, height=60)
    text_top.pack()
    str = '''
             created by Wang Dong, Dec 6, 2020.
             Copyright (c) 2020, dong1024mail@163.com All Rights Reserved.

             #####################################################
             #                                                   #
             #                       _oo0oo_                     #
             #                      o8888888o                    #
             #                      88" . "88                    #
             #                      (| -_- |)                    #
             #                      0\  =  /0                    #
             #                    ___/`---'\___                  #
             #                  .' \\|     |# '.                  #
             #                 / \\|||  :  |||# \                 #
             #                / _||||| -:- |||||- \              #
             #               |   | \\\  -  #/ |   |               #
             #               | \_|  ''\---/''  |_/ |             #
             #               \  .-\__  '-'  ___/-. /             #
             #             ___'. .'  /--.--\  `. .'___           #
             #          ."" '<  `.___\_<|>_/___.' >' "".         #
             #         | | :  `- \`.;`\ _ /`;.`/ - ` : | |       #
             #         \  \ `_.   \_ __\ /__ _/   .-` /  /       #
             #     =====`-.____`.___ \_____/___.-`___.-'=====    #
             #                       `=---='                     #
             #     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   #
             #                                                   #
             #               佛祖保佑         高分飘过           #
             #                                                   #
             #####################################################
 
'''
    text_top.insert('end', str)
    
def main():

    # 用于保存参数矩阵
    global param
    param=''

    window = Tk()
    window.title("最优化方法")
    # 禁止缩放
    window.resizable(False, False)

    # 创建一个顶级菜单
    menubar = Menu(window)
    menubar.add_command(label="about", command=about)
    menubar.add_command(label="clear", command=log_clear)
    window.config(menu = menubar)

    # 创建frame容器
    #  must be flat, groove, raised, ridge, solid, or sunken
    frameLT = Frame(width=500, height=200, bg='#D3D3D3', relief="ridge", bd=4)
    frameLC = Frame(width=500, height=150, bg='red')

    # 创建一个文本框放在上面frame
    global text
    text = scrolledtext.ScrolledText(frameLC)
    text.pack()

    # 尝试使用背景图片
    # image = Image.open(r'./bg.jpg')
    # bg_img = ImageTk.PhotoImage(image)
    # bg_label = Label(window, image=bg_img)
    # bg_label.place(x=0, y=0)


    frameLT.grid(row=0, column=0,padx=5, pady=10)
    frameLC.grid(row=1, column=0,padx=10, pady=10)
    frameLT.pack_propagate(0)
    frameLT.pack_propagate(0)

    # 创建两个按钮，分别表示单纯形法与运输问题
    # 用两个无意义的标签控制间距
    l1 = Label(frameLT, text="",heigh=1, bg="#d3d3d3")
    btn1 = Button(frameLT, text="Simplex solution", command=create_sim, width=30, heigh=3)
    l2 = Label(frameLT, text="",heigh=1, bg="#d3d3d3")
    btn2 = Button(frameLT, text="Transport problem", command=create_tran, width=30, heigh=3)
    l1.pack()
    btn1.pack()
    l2.pack()
    btn2.pack()

    init()

    mainloop()
    
main()


# In[ ]:





# P_pagerank by Huajie Shao
import numpy as np
import operator

# -------author index-----
num_name = {}
index_name = {}
f_author = open('author.txt', 'r')
for name in f_author.readlines():
    nam = name.split()  # whitespace
    num_name[nam[0]] = ' '.join(nam[1: len(nam)])  # joint the names
    index_name[num_name[nam[0]]] = nam[0]  # search name
f_author.close()
n = len(num_name)
#  ----get the authors--
key = sorted(num_name.keys())
i = 0
d_key = {}  # dictionary
re_key = {}
for ky in key:
    d_key[ky] = i   # get the rows of matrix
    re_key[i] = ky
    i += 1

# -----get the dict for authors and neighbors---

def read_folder(ids):
    dic_nm = {}
    id = int(ids)
    if id == 68855 or id == 51360:
        fv = open('APVPA.txt', 'r')  # Christos Faloutsos 68855, AnHai Doan: 51360
    else:
        fv = open('APTPA.txt', 'r')
    for line in fv.readlines():
        a_id = line.split()
        dic_nm.setdefault(a_id[0], []).append(a_id[1])
        # d_name.setdefault(a_id[1], []).append(a_id[0])  # second column
    fv.close()
    return dic_nm



# ------define the A matrix-----
def get_amtx(dic_name):
    a_mtx = np.zeros([n, n])
    dic_nm = dic_name
    for kn in dic_nm.keys():  # the 1st column
        nbs = dic_nm[kn]      # get the list of neighbors
        clm = d_key[kn]
        #if len(nbs) >= 1:
        for nb in nbs:
            r = d_key[nb]   # get the row or column of A matrix
            a_mtx[r][clm] = 1
            a_mtx[clm][r] = 1
    # normalized A matrix
    for j in range(0, n):
        sm = np.sum(a_mtx[:, j])
        a_mtx[:, j] = a_mtx[:, j]/sm
    return a_mtx



# ----define the u matrix------
def u_matrix(m, pid):
    u_mtx = np.zeros(m)
    k = d_key[pid]
    u_mtx[k] = 1
    return u_mtx


# ---solve the v matrix
def page_rank(names):
    x_name = names
    pid1 = index_name[names]
    dic_name1 = read_folder(pid1)   #get the list of neighbors
    u_arr = u_matrix(n, pid1)
    amtx = get_amtx(dic_name1)  #get the dict
    c = 0.15
    t = 10
    v_mtx = np.zeros(n)
    v_mtx[:] = 1/n
    vt = np.zeros(n)
    while t > 0:
        vt = (1-c)*np.dot(amtx, v_mtx) + c*u_arr  #get the A matrix
        v_mtx = vt
        t -= 1
    rst = {}
    for ki in range(0, n):
        gn = num_name[re_key[ki]]     # get the name
        rst[gn] = vt[ki]

    result = sorted(rst.items(), key=operator.itemgetter(1), reverse=True)
    for jm in result[0:10]:
        print(jm)

# ------This is the result for APVPA------
page_rank('Christos Faloutsos')
print('----------------------------\n')
page_rank('AnHai Doan')



#------The following result is for APTPA------

'''
print('\n-----Notice: The following result is for APTPA------\n')
page_rank('Xifeng Yan')
print('----------------------------')
page_rank('Jamie Callan')
'''







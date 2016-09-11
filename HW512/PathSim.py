# Huajie Shao, Fun: PathSim algorithm @ 512 data mining
import operator
# output_file ="rank_author.txt"
num_name = {}
s_name = {} #dictionary
f_author = open('author.txt', 'r')
for name in f_author.readlines():
    nam = name.split()  # whitespace
    num_name[nam[0]] = ' '.join(nam[1: len(nam)])  # joint the names
    s_name[num_name[nam[0]]] = nam[0]  # search name
f_author.close()

# please replace the venue with term
def read_folder_dic(ids):
    vlist = []
    id = int(ids)
    if id == 68855 or id == 51360:
        fv = open('venue.txt', 'r')  # Christos Faloutsos 68855, AnHai Doan: 51360
    else:
        fv = open('term.txt', 'r')
    for venue in fv.readlines():
        vnu = venue.split()
        vlist.append(vnu[0])
    fv.close()
    return vlist


# find the dictionary, important
def count_paper(k_list):
    v_list = k_list
    ven = {}
    author = {}
    fr = open('relation.txt', 'r')
    for line in fr.readlines():
        txt = line.split()
        if txt[1] in v_list:  # here is the difference to read data
            ven.setdefault(txt[0], []).append(txt[1])  # {paper id, term}
        elif txt[1] in num_name.keys():
            author.setdefault(txt[0], []).append(txt[1])  # multiple authors {paper id, author}
    fr.close()
    # give all the lists, it has repeated values
    pv_list = []
    for key in author.keys():  # paper id
        au_id = author[key]  # get author ids
        terms = ven[key]
        for au in au_id:
            for term in terms:
                pv_list.extend([(au, term)])  # {author, venues}
    # create dict to count the total number
    pv_count = {}  # dict
    for pv in pv_list:
        if pv in pv_count:
            pv_count[pv] += 1
        else:
            pv_count[pv] = 1
    return pv_count


def pathsim_fun(names):
    num = s_name[names]
    v_list = read_folder_dic(num)  # get the name id
    pv_count = count_paper(v_list)
    cnt = []
    for ve in v_list:
        num_v = (num, ve)  # key
        if num_v in pv_count.keys():  # get the number of paper for author
            cnt.append(pv_count[num_v])
        else:
            cnt.append(0)
    dic = {}
    for nm in num_name.keys():  # get the id of author
        sim = []
        sum3 = 0
        sum1 = 0
        sum2 = 0
        for ve in v_list:
            nv = (nm, ve)
            if nv in pv_count.keys():
                sim.append(pv_count[nv])
            else:
                sim.append(0)
        # calculate the results based on pathsim
        for i in range(0, len(v_list)):
            sum1 += int(cnt[i]) ** 2
            sum2 += int(sim[i]) ** 2
            sum3 += int(cnt[i]) * int(sim[i])
        val = round(2 * 10000000000 * sum3 / (sum2 + sum1)) / 10000000000
        fm = num_name[nm]
        dic[fm] = val

    rst = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
    # file_out=open(output_file,'w')
    for j in rst[0:10]:
        print (j)     
        # file_out.write(str(j)+'\n')

    # file_out.close()

        

pathsim_fun('Christos Faloutsos')
print('-------------------------------')
pathsim_fun('AnHai Doan')


# ---------the following is APTPA-------------

'''
print('\n-----Notice: The following result for APTPA------\n')
pathsim_fun('Xifeng Yan')
print('-------Please continue to wait for 3 minutes----------')
pathsim_fun('Jamie Callan')
'''

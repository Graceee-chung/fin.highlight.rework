import os
import shutil


def find_sic(filename):
    with open('/home/intern/Dyna/data/sel4_cmp_info_2.txt') as fh:
        data = [line[:-1] for line in fh.readlines()]
        
    lines = [cmp.split(' ~~~') for cmp in data]
    sic_codes = [i[0] for i in lines]
    files = [i[2].split(' | ')[1:] for i in lines]
    for i in files:
        i[0] = i[0][:-1]; i[1] = i[1][:-1]; i[2] = i[2][:-1]; i[3] = i[3][:-1]
    
    dic = [(i, v)  for i, v in zip(sic_codes, files)]
    for item in dic:
        for i in item:
            if filename in i:
                return int(item[0])
                

def cat_file(year):
    path = f'/home/intern/Dyna/data/sel4_10k/{year}/'
    for name in os.listdir(path):
        if len(name) > 5:
            des_path = f'/home/intern/Dyna/data/sel4_10k/{year}/{find_sic(name)}/'
            shutil.copy2(path + name, des_path)

for year in range(2016, 2021):
    cat_file(year)






















#!/usr/bin/python
#import pandas
import subprocess
import matplotlib.pyplot as plt
#import pandas as pd
from matplotlib import pyplot
import itertools
import sys
import argparse
from datetime import *

cluster_dic={'Allocated': 0,'Down': 0, 'Down PLND': 0,'Idle': 0,'Reserved': 0}

def get_all_report(var1,var2,var3):
    ''' cette foction premet de recupere les resultat d'un sreport clustre utilisation par gpu dans un periode de temps fixer par
        l'utilisateut
    '''
    cmd="sreport  " +  var1  +   "   utilisation -n --tres=gres/gpu -t percent start="+var2 +"  end="+var3
    cmd2=cmd +  "| awk -F \" \" '{print $3,$4,$5,$6,$7}'"
    cluster_raw = subprocess.Popen( cmd2, stdout=subprocess.PIPE, shell=True).communicate()[0].strip().split('\n')
    cluster_raw = cluster_raw[0].split()
    print(cluster_raw)
    for i in range(0,len(cluster_raw)):
              cluster_raw[i] = cluster_raw[i].replace('%', ' ').strip()
              cluster_raw[i] = float(cluster_raw[i])
    i = 0
    for key, value in cluster_dic.items():
        if key == "Allocated":
            cluster_dic[key] = cluster_raw[0]
        elif key == "Down":
            cluster_dic[key] = cluster_raw[1]
        elif key == "Down PLND":
            cluster_dic[key] = cluster_raw[2]
        elif key == "Idle":
            cluster_dic[key] = cluster_raw[3]
        elif key == "Reserved":
            cluster_dic[key] = cluster_raw[4]
    return cluster_dic
def get_raw(var1,var2,var3):
    ''' cette foction premet de recupere les resultat d'un sreport clustre utilisation par gpu dans un periode de temps fixer par
            l'utilisateut
        '''
    cmd = "sreport  " + var1 + "   TopUsage --tres=gres/gpu -t percent  TopCount=1000 start=" + var2 + "  end=" + var3
    cmd2 = cmd + "| awk -F \" \" '{print $3,$4,$5,$6,$7}'"
    cluster_raw = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    return cluster_raw

if __name__ == "__main__":

#    if  len(sys.argv) <= 2 and (sys.argv[2] == 0 and sys.argv[3] == 0):
#        print("Precisez une action en parametre")
#        sys.exit(1)
    parser = argparse.ArgumentParser(description='Process sreport MILA')
    parser.add_argument('argument', choices=['cluster','user'],  help='donner un argument valide cluster ou user')
    parser.add_argument('start', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help='donner une froma valide de date YYYY-MM-DD')
    parser.add_argument('end', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help='donner une forma  valide de date YYYY-MM-DD')
    args = parser.parse_args()
#    print(parser.args)


    arg = args.argument
    start = str(args.start)
    end  =  str(args.end)
    print(arg)
    print(args.start)
    print(args.end)
    if arg == 'cluster':
         vstat= get_all_report(arg,start,end)
   	 data = []
   	 for value in vstat.values():
             data.append(value)
             name = vstat.keys()
         explode = (0, 0.15, 0, 0, 0)
         colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'red']
         plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, colors=colors, shadow=True)
         plt.axis('equal')
         plt.title("LA Periode entre  "+ start+ " et  "+ end) 
         plt.show()
    elif arg == 'user':
         vstat = get_raw(arg, start, end)
         print(vstat)
    else:
	 print("erreur")

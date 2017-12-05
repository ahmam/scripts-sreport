#!/usr/bin/python
import matplotlib.pyplot as plt
import subprocess
from datetime import *
from calendar import *
from calendar import monthrange
import calendar


def get_all_report():
    cluster_list=[]
    for i in range(1, 13):
        start = datetime(2017, i, 1).date()
        res = calendar.monthrange(2017, i)
        end = start + timedelta(days=(res[1] - 1))
        var1 = str(start)
        var2 = str(end)
        cmd = " sreport cluster utilisation  -n  --tres=gres/gpu  -t percent start=" + var1 + "  end=" + var2
        cmd2 = cmd + "| awk -F \" \" '{print $3,$4,$5,$6,$7}'"
        cluster_raw = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True).communicate()[0].strip().split('\n')
        cluster_raw = cluster_raw[0].split(' ')
        if len(cluster_raw) > 1:
           cluster_list.append(cluster_raw)
        else:
           cluster_list.append(['0.0%'])
    #cluster_raw = subprocess.Popen(['sh /u/mamlouka/sreport3.sh'], stdout=subprocess.PIPE, shell=True).communicate()[0].strip().split('\n')
    #while i < len(cluster_list):
     #     cluster_list[i] = cluster_list[i].split()
     #     i=i+1
    i=0
    j=0
    for i in range(0,len(cluster_list)):
        for j in range(0,len(cluster_list[i])):
                cluster_list[i][j] = cluster_list[i][j].replace('%', ' ').strip()
                cluster_list[i][j] = float(cluster_list[i][j])
    return cluster_list



print(get_all_report())
stat=get_all_report()
state = ('Allo', 'Down', 'DownP', 'Idle', 'Resd')
mois=['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
j=1
n=1
print(len(stat))
for i in range(0,(len(stat)-4)):
    if len(stat[i]) > 1:
        plt.subplot(2, 3, n)
        explode = (0, 0.15, 0, 0, 0)
        plt.title(mois[i])
        plt.pie(stat[i], explode=explode, labels=state, autopct='%1.1f%%', startangle=90, shadow=True)
        plt.axis('equal')
        n+=1
    #else:
        #plt.subplot(2, 3, n)
        #explode = (0, 0, 0, 0, 0)
        #plt.title(mois[i])
        #circle=plt.Circle((0,0),2)
        #plt.pie(1 , explode=explode, labels=state, autopct='%1.1f%%', startangle=90, shadow=True)
        #plt.axis('equal')
plt.tight_layout()
plt.show()
for i in range(8,len(stat)):
    if len(stat[i]) > 1:
       plt.subplot(2, 3, j)
       explode = (0, 0.15, 0, 0, 0)
       plt.title(mois[i])
       plt.pie(stat[i], explode=explode, labels=state, autopct='%1.1f%%', startangle=90, shadow=True)
       plt.axis('equal')
       j+=1
plt.tight_layout()
plt.show()

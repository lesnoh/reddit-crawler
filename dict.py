#!/usr/bin/env python3
import time;
import datetime;
from collections import defaultdict

sub_start = int(time.mktime(time.strptime('2017-11-30 10:00:00', '%Y-%m-%d %H:%M:%S')))
sub_end   = int(time.mktime(time.strptime('2017-11-30 11:59:59', '%Y-%m-%d %H:%M:%S')))
directory = 'output/' + str(sub_start) + '-' + str(sub_end)
dictAuthoren = defaultdict(int)

dictAuthoren["bla"] += 1
dictAuthoren["bla"] += 1
dictAuthoren["bla"] += 1
dictAuthoren["bla"] += 1
dictAuthoren["bla"] += 1
dictAuthoren["bla"] += 1
dictAuthoren["bla"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["michon"] += 1
dictAuthoren["blubb"] += 1
dictAuthoren["blubb"] += 1

#for keys,values in dictAuthoren.items():
#    print(keys),
#    print(values)

print ('\nAuthoren:')
s = [(k, dictAuthoren[k]) for k in sorted(dictAuthoren, key=dictAuthoren.get, reverse=True)]
file = open(directory + '/' + str('00-Authoren.txt'), 'w')
for k, v in s:
    print (k,v)
    file.write('{} {} {}'.format(
                    k,
                    v,
                    '\n'
                    ))
file.close()

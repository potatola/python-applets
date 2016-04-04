# coding: UTF-8

import os 
import sys

if len(sys.argv) == 3:
    fname = sys.argv[1]
    out_dir = sys.argv[2]
else:
    print "usage: vcf_spliter <input file> <output dir>"
    exit()

count = 0
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with open(fname, 'r') as f:
    for l in f:
        if l.strip() == "BEGIN:VCARD":
            count += 1
            fw = open(os.path.join(out_dir, str(count)+'.vcf'), 'w')
            fw.write(l)
        elif l.strip() == "END:VCARD":
            fw.write(l)
            fw.close()
        else:
            fw.write(l)
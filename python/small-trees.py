# Computing polymorphisms of small trees

import datetime
import os


def generate_trees(n, outfile):
    # command = f"gentreeg -q {n} | directg -o -T > {outfile}"
    command = f"gentreeg -q {n} | watercluster2 S T > {outfile}"        
    os.system(command)


def generate_triads(n, outfile):
    command = f"gentreeg -q -D3 {n} | pickg -q -D3 -M1 | watercluster2 S T > {outfile}"
    os.system(command)


def main():
    for n in range(1, 22):
        print(f"size {n}")        
        generate_trees(n, f"tmp{n}.txt")


main()
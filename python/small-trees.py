# Computing polymorphisms of small trees

import datetime
import os


def generate_trees(n):
    # generate oriented trees of size {n} using nauty
    command = f"gentreeg -q {n} | watercluster2 S T"
    print(os.system(command))


def generate_triads(n):
    # generate oriented triads of size {n} using nauty
    command = f"gentreeg -q -D3 {n} | pickg -D3 -M3 | watercluster2 S T"
    os.system(command)


def main():
    for n in range(1, 10):
        generate_trees(n)


main()
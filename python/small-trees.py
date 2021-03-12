# Computing polymorphisms of small trees

import minizinc
import os
from pathlib import Path


def generate_trees(n, outfile):
    # command = f"gentreeg -q {n} | directg -o -T > {outfile}"
    command = f"gentreeg -q {n} | watercluster2 S T > {outfile}"        
    os.system(command)


def generate_triads(n, outfile):
    command = f"gentreeg -q -D3 {n} | pickg -q -D3 -M1 | watercluster2 S T > {outfile}"
    os.system(command)    


def convert_to_dzn(infile):
    # convert digraphs in nauty's simple text format (nv ne edges) to minizinc instances
    with open(infile, 'r') as file:
        trees = []
        for line in file:
            input_list = line.strip().split(' ')
            edgelist = '[|'+ '|'.join(','.join(edge) for edge in zip(input_list[2::2], input_list[3::2])) + '|]'        
            output = f"n={input_list[0]};m={input_list[1]};edgelist={edgelist};"            
            trees.append(output)
    return trees


def convert_to_python(infile):
    # convert digraphs in nauty's simple text format (nv ne edges) to python dictionary
    with open(infile, 'r') as file:
        trees = []
        for line in file:
            tree = {}
            numbers = [int(x) for x in line.strip().split(' ')]
            tree["n"] = numbers[0]
            tree["m"] = numbers[1]
            tree["edgelist"] = list(zip(numbers[2::2], numbers[3::2]))          
            trees.append(tree)
    return trees


def count_core_triads2(n):
    generate_triads(n, f"./tmp/triads{n}.trees")    
    trees = convert_to_python(f"./tmp/triads{n}.trees")

    gecode = minizinc.Solver.lookup("gecode")
    
    # model for computing height and levels of vertices
    model_levels = minizinc.Model("./minizinc/models/levels.mzn") 
    inst_levels = minizinc.Instance(gecode, model_levels)
    inst_levels["n"] = n
    inst_levels["m"] = n - 1
    
    # better model to test non-cores that requires height and levels
    model_not_core_levels = minizinc.Model("./minizinc/models/not-core-levels.mzn") 
    inst_not_core_levels = minizinc.Instance(gecode, model_not_core_levels)
    inst_not_core_levels["n"] = n
    inst_not_core_levels["m"] = n - 1
        
    num_cores = 0
    for tree in trees:
        
        with inst_levels.branch() as inst_levels_branch:
            inst_levels_branch["edgelist"] = tree["edgelist"]
            result = inst_levels_branch.solve() 

            # triads of height <= 3 cannot be cores
            if result["height"] > 3:
                with inst_not_core_levels.branch() as inst_not_core_levels_branch:
                    inst_not_core_levels_branch["edgelist"] = tree["edgelist"]
                    inst_not_core_levels_branch["height"] = result["height"]
                    inst_not_core_levels_branch["levels"] = result["levels"]
                    inst_not_core_levels_branch["edge_levels"] = [result["levels"][e[1]] for e in tree["edgelist"]]
                    result = inst_not_core_levels_branch.solve()
                    if not result:
                        num_cores += 1           
    
    print(f"Core triads of size {n}: {num_cores}")


def main():
    for i in range(8, 8 + 1):
        count_core_triads2(i)


main()


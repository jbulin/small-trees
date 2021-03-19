## 
# Computing polymorphisms of small trees
##

import minizinc
import os
import sys
from pathlib import Path


def generate_trees(size, outfile):
    # also works but seems slower: `command = f"gentreeg -q {size} | directg -o -T > {outfile}`"
    command = f"gentreeg -q {size} | watercluster2 S T > {outfile}"        
    os.system(command)
    return True


def generate_triads(size, outfile):
    command = f"gentreeg -q -D3 {size} | pickg -q -D3 -M1 | watercluster2 S T > {outfile}"
    os.system(command)   
    return True 


def graph_text_to_list(graph_text):
    # Nauty's simple text format (nv ne edges) to list of int
    return [int(x) for x in graph_text.strip().split(' ')]


def graph_list_to_dict(graph_list):
    # from list of int to dict
    graph_dict = {}    
    graph_dict["n"] = graph_list[0]
    graph_dict["m"] = graph_list[1]
    graph_dict["E"] = list(zip(graph_list[2::2], graph_list[3::2]))
    return graph_dict         


def all_graphs_to_dicts(infile):
    # convert all graphs in the input file from text (nv ne edges) to list of dict
    with open(infile, 'r') as file:
        graphs = []
        for line in file:
            graph_dict = graph_list_to_dict(graph_text_to_list(line))
            graphs.append(graph_dict)    
    return graphs


def core_triads(size, outfile):
    # Compute all core triads of size {size} up to reversing edges (requires that the outdegree of the root is >= 2)
    Path("./tmp").mkdir(exist_ok=True)
    generate_triads(size, f"./tmp/all_triads{size}.trees")    
    triads = all_graphs_to_dicts(f"./tmp/all_triads{size}.trees")

    gecode = minizinc.Solver.lookup("gecode")
    
    # model for computing height and levels of vertices
    model = minizinc.Model("./models/triad-core.mzn") 
    inst = minizinc.Instance(gecode, model)
    inst["n"] = size 
    inst["m"] = size - 1    
    
    num_cores = 0
    with open(outfile, 'w') as file:
        for triad in triads:
            edgelist_flat = [v for e in triad["E"] for v in e]
            # sources = set(edgelist_flat[::2])
            # sinks = set(edgelist_flat[1::2])
            degrees = [edgelist_flat.count(v) for v in range(size)]
            outdegrees = [edgelist_flat[::2].count(v) for v in range(size)]
            # indegrees = [edgelist_flat[1::2].count(v) for v in range(n)]        
            root = degrees.index(3)
            
            # symmetry: require that the root has more outgoing edges than incoming edges
            if outdegrees[root] <= 1:
                continue 

            with inst.branch() as branch:
                branch["E"] = triad["E"]
                result = branch.solve() 
                if not result:
                    num_cores += 1
                    file.write(str(edgelist_flat) + "\n")         
    
    print(f"Done. There are {num_cores} core triads of size {size} up to edge reversal.")


if __name__ == "__main__":
    if sys.argv[1] == "core-triads":
        core_triads(int(sys.argv[2]), sys.argv[3])


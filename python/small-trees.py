## 
# Computing polymorphisms of small trees
##

import minizinc
import os
import sys
from pathlib import Path


class Nauty:
    # Using Nauty to generate graphs

    @staticmethod
    def generate_trees(size, outfile):
        # also works but seems slower: `command = f"gentreeg -q {size} | directg -o -T > {outfile}`"
        command = f"gentreeg -q {size} | watercluster2 S T > {outfile}"        
        os.system(command)
        return True

    @staticmethod
    def generate_triads(size, outfile):
        command = f"gentreeg -q -D3 {size} | pickg -q -D3 -M1 | watercluster2 S T > {outfile}"
        os.system(command)   
        return True 


class Graph:
    # Convert between various graph formats

    @staticmethod
    def text_to_list(graph_text):
        # Nauty's simple text format (nv ne edges) to list of int
        return [int(x) for x in graph_text.strip().split(' ')]

    @staticmethod
    def list_to_dict(graph_list):
        # from list of int to dict
        graph_dict = {}    
        graph_dict["n"] = graph_list[0]
        graph_dict["m"] = graph_list[1]
        graph_dict["E"] = list(zip(graph_list[2::2], graph_list[3::2]))
        return graph_dict         

    @staticmethod
    def all_to_dicts(infile):
        # convert all graphs in the input file from text (nv ne edges) to list of dict
        with open(infile, 'r') as file:
            graphs = []
            for line in file:
                graph_dict = Graph.list_to_dict(Graph.text_to_list(line))
                graphs.append(graph_dict)    
        return graphs


class Triad:
    
    @staticmethod
    def core_triads(size, outfile):
        # Compute all core triads of size {size} up to reversing edges (requires that the outdegree of the root is >= 2)
        Path("./tmp").mkdir(exist_ok=True)
        
        all_triads_file = Path(f"./tmp/all_triads{size}.trees")        
        if not all_triads_file.is_file():        
            # generate all triads if not already done
            Nauty.generate_triads(size, f"./tmp/all_triads{size}.trees")    
        triads = Graph.all_to_dicts(all_triads_file)
        

        gecode = minizinc.Solver.lookup("gecode")
        
        # model for computing height and levels of vertices
        model = minizinc.Model("./models/triad-core.mzn") 
        inst = minizinc.Instance(gecode, model)
        inst["n"] = size
        
        num_cores = 0
        num_triads = len(triads)
        print(f"Tesing {num_triads} triads for being a core.") 
        with open(outfile, 'w') as file:
            for i, triad in enumerate(triads):                
                # find the root and compute its outdegree
                edgelist_flat = [v for e in triad["E"] for v in e]
                degrees = [edgelist_flat.count(v) for v in range(size)]
                root = degrees.index(3)
                outdegrees = [edgelist_flat[::2].count(v) for v in range(size)]
                                
                # symmetry: require that the root has more outgoing edges than incoming edges
                if outdegrees[root] <= 1:
                    continue 

                with inst.branch() as branch:
                    branch["E"] = triad["E"]
                    result = branch.solve() 
                    if not result:
                        num_cores += 1
                        file.write(str(edgelist_flat) + "\n") 

                print(f"{(i + 1) / num_triads:.2%}", end="\r")
        
        print(f"\nDone. There are {num_cores} core triads of size {size} up to edge reversal.\n")
        return True   


if __name__ == "__main__":
    
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        print("Compute core triads: `python ./python/smalltrees.py core-triads <size> <output-file>`\n")
    
    elif sys.argv[1] == "core-triads":
        Triad.core_triads(int(sys.argv[2]), sys.argv[3])
        


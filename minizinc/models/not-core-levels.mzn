% Test if the input digraph with levels is a non-core
int: n;
int: m;    
int: height;
set of int: vertices = 0..n-1;
set of int: edges = 1..m;
array[1..n] of 0..height: levels;
array[1..m] of 1..height: edge_levels;
    
array[edges, 1..2] of vertices: edgelist;

array[vertices] of var vertices: f;

constraint forall(e1 in edges)(exists(e2 in edges where edge_levels[e1] = edge_levels[e2])(    
    f[edgelist[e1, 1]] = edgelist[e2, 1] /\
    f[edgelist[e1, 2]] = edgelist[e2, 2]
));

constraint exists(u, v in vertices where levels[u+1] = levels[v+1] /\ u < v)(f[u] = f[v]);
    
solve satisfy;

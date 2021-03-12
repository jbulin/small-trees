% Test if the input digraph is a non-core
int: n;
int: m;    
int: max_height = m;
set of int: vertices = 0..n-1;
set of int: edges = 1..m;    
array[edges, 1..2] of vertices: edgelist;

array[vertices] of var vertices: f;

constraint forall(e1 in edges)(exists(e2 in edges)(
    f[edgelist[e1, 1]] = edgelist[e2, 1] /\
    f[edgelist[e1, 2]] = edgelist[e2, 2]
));

constraint exists(u, v in vertices where u < v)(f[u] == f[v]);
    
solve satisfy;

% Test if the input digraph has a 2-wnu
int: n;
int: m;    
set of int: vertices = 0..n-1;
set of int: edges = 1..m;    
array[edges, 1..2] of vertices: edgelist;

array[vertices, vertices] of var vertices: f;

constraint forall(e1, e2 in edges)(exists(e3 in edges)(
    f[edgelist[e1, 1], edgelist[e2, 1]] = edgelist[e3, 1] /\
    f[edgelist[e1, 2], edgelist[e2, 2]] = edgelist[e3, 2]
));

constraint forall(x in vertices)(f[x, x] = x);
constraint forall(x, y in vertices)(f[x, y] = f[y, x]);
    
solve satisfy;

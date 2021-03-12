% Test if the input digraph with levels has a 2-wnue
int: n;
int: m;
int: height;
set of int: vertices = 0..n-1;
set of int: edges = 1..m;    
array[edges, 1..2] of vertices: edgelist;
array[1..n] of 0..height: levels;
array[1..m] of 1..height: edge_levels;

array[vertices, vertices] of var vertices: f;

constraint forall(e1, e2 in edges where edge_levels[e1] = edge_levels[e2])(exists(e3 in edges where edge_levels[e1] = edge_levels[e3])(
    f[edgelist[e1, 1], edgelist[e2, 1]] = edgelist[e3, 1] /\
    f[edgelist[e1, 2], edgelist[e2, 2]] = edgelist[e3, 2]
));

constraint forall(x in vertices)(f[x, x] = x);
constraint forall(x, y in vertices where levels[x+1] = levels[y+1])(f[x, y] = f[y, x]);
    
solve satisfy;


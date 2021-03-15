
int: n; 
set of vertices: nonsources;
set of vertices: nonsinks;

set of int: edges = 1..n-1;    
array[edges, 1..2] of vertices: edgelist;


array[vertices] of var vertices: f;

constraint forall(u in nonsources)(f[u] in nonsources);
constraint forall(u in nonsinks)(f[u] in nonsinks);

constraint forall(e1 in edges)(exists(e2 in edges)(
    f[edgelist[e1, 1]] = edgelist[e2, 1] /\
    f[edgelist[e1, 2]] = edgelist[e2, 2]
));

include "alldifferent.mzn";
constraint not alldifferent(f);
    
solve satisfy;

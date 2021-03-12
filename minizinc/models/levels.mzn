% Compute levels and height of the input digraph
int: n;
int: m;    
int: max_height = m;
set of int: vertices = 0..n-1;
set of int: edges = 1..m;    
array[edges, 1..2] of vertices: edgelist;

array[vertices] of var 0..max_height: levels;
var 0..max_height: height;

constraint min(levels) = 0;
constraint height = max(levels);

constraint forall(e in edges)(levels[edgelist[e, 2]] = levels[edgelist[e, 1]] + 1);

solve satisfy;

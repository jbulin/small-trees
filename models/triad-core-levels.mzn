
int: n;   
int: h;
array[0..n-1] of 0..h:lvl;
array[1..n-1, 1..2] of 0..n-1: E;
array[0..n-1] of var 0..n-1: f;

constraint forall(v in 0..n-1)(lvl(f[v])=lvl(v));
constraint forall(e in 1..n-1)(exists(e2 in 1..n-1)(f[E[e,1]]=E[e2,1] /\ f[E[e,2]]=E[e2,2]));
include "alldifferent.mzn";
constraint not alldifferent(f);    
solve satisfy;

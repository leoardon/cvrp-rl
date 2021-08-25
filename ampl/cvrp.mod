param n > 0,integer;
param Q > 0 integer;

set V := 0..n;
set VC := 1..n;

param c{V,V} >= 0;
param d{VC} >= 0;

var x{V,V} binary;
var u{VC};

minimize total_dist : 
	sum{i in V, j in V} x[i,j]*c[i,j];

subject to leaveOnce {i in VC}: 
	sum{j in V: i != j} x[i,j] = 1;
	
subject to enteredOnce {j in VC}: 
	sum{i in V: i != j} x[i,j] = 1;

# subject to subTour {i in VC, j in VC}:
#	x[i,j] == 1 ==> u[i] + d[j] = u[j];

subject to subTour {i in VC, j in VC}:
	u[i] - u[j] + Q * x[i,j] <= Q - d[j];
	
subject to capacity {i in VC}:
	u[i] >= d[i];
	
subject to totalCapacity {i in VC}:
	u[i] <= Q;
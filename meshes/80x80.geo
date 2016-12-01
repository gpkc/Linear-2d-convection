cl = 0.1;
n = 80;
progr = 1;

Point(1) = {0,0,0,cl};
Point(2) = {1,0,0,cl};
Point(3) = {1,1,0,cl};
Point(4) = {0,1,0,cl};
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Line Loop(5) = {1,2,3,4};
Plane Surface(6) = {5};

Transfinite Line {1, 2, 3, 4} = n Using Progression progr;
Transfinite Surface "*";
Recombine Surface "*";

Physical Surface(100) = {6};

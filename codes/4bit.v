`include "FullAdder.v"
module fbit(a,b,cin,sum,cout);
	output [3:0] sum;
	output cout;
	input [3:0] a,b;
	input cin;
	wire c1,c2,c3,c4;
	Full_Adder1 fa1(a[0],b[0],cin,sum[0],c1);
	Full_Adder1 fa2(a[1],b[1],c1,sum[1],c2);
	Full_Adder1 fa3(a[2],b[2],c2,sum[2],c3);
	Full_Adder1 fa4(a[3],b[3],c3,sum[3],cout);
endmodule
	
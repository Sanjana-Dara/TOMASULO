`include "32bit.v"
module sibit(a,b,cin,sum,cout);
	output [63:0] sum;
	output cout;
	input [63:0] a,b;
	input cin;
	wire c1,c2,c3,c4;
	tbit fa1(a[31:0],~b[31:0],cin,sum[31:0],c1);
	tbit fa2(a[63:32],~b[63:32],c1,sum[63:32],cout);
	
endmodule
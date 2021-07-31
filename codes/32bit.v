`include "16bit.v"
module tbit(a,b,cin,sum,cout);
	output [31:0] sum;
	output cout;
	input [31:0] a,b;
	input cin;
	wire c1,c2,c3,c4;
	sbit fa1(a[15:0],b[15:0],cin,sum[15:0],c1);
	sbit fa2(a[31:16],b[31:16],c1,sum[31:16],cout);
	
endmodule
	
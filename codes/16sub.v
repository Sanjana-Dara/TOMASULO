`include "8bit.v"
module sbit(a,b,cin,sum,cout);
	output [15:0] sum;
	output cout;
	input [15:0] a,b;
	input cin;
	wire c1,c2,c3,c4;
	ebit fa1(a[7:0],~b[7:0],cin,sum[7:0],c1);
	ebit fa2(a[15:8],~b[15:8],c1,sum[15:8],cout);
	
endmodule
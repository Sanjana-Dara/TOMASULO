`include "4bit.v"
module ebit(a,b,cin,sum,cout);
	output [7:0] sum;
	output cout;
	input [7:0] a,b;
	input cin;
	wire c1,c2,c3,c4;
	fbit fa1(a[3:0],b[3:0],cin,sum[3:0],c1);
	fbit fa2(a[7:4],b[7:4],c1,sum[7:4],cout);
	
endmodule
	
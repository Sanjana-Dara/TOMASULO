`include "64sub.v"
module siibit;
	reg [63:0] a,b;
	reg cin;
	wire [63:0] sum;
	wire c1,c2;
	sibit fa1 (a[63:0],b[63:0],cin,sum[63:0],c1);
	
	
	initial begin
		if($value$plusargs("a=%b",a));
        if($value$plusargs("b=%b",b));
        if($value$plusargs("cin=%b",cin));
	end
		initial begin
			$monitor($time,"vlaue = %d",sum);
			
		end
endmodule
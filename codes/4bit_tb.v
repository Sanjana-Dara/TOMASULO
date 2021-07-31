`include "8bit.v"
module siibit;
	reg [3:0] a,b;
	reg cin;
	wire [4:0] sum;
	wire c1,c2;
	fbit fa1 (a[3:0],b[3:0],cin,sum[3:0],sum[4]);
	
	
	initial begin
        if($value$plusargs("a=%b",a));
        if($value$plusargs("b=%b",b));
        if($value$plusargs("cin=%b",cin));
	end
    
		initial begin
			$monitor($time,"value = %d",sum);
		end
endmodule
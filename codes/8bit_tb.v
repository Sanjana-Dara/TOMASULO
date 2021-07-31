`include "8bit.v"
module siibit;
	reg [7:0] a,b;
	reg cin;
	wire [8:0] sum;
	wire c1,c2;
	ebit fa1 (a[7:0],b[7:0],cin,sum[7:0],sum[8]);
	
	
	initial begin
        if($value$plusargs("a=%b",a));
        if($value$plusargs("b=%b",b));
        if($value$plusargs("cin=%b",cin));
	end
    
		initial begin
			$monitor($time,"value = %d",sum);
		end
endmodule
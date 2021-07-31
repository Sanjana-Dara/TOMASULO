`include "Wallace16bit.v"
module top1;

    reg [15:0] A, B;

    wire [31:0] out;

   Wallace16bit w(A, B, out);

    initial begin
        if($value$plusargs("a=%b",A));
        if($value$plusargs("b=%b",B));
    end
      
    initial
        $monitor($time,"Output=%d",out);

endmodule
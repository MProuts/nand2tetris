## sp--
@SP
M=M-1
## D = *sp
@SP
A=M
D=M
## if D != 0: goto <label>
@${symbol}
D;JNE

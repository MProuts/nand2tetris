## push return address
@${return_addr}
D=A
@SP
A=M
M=D
@SP
M=M+1
## push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
## push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
## push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
## push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
## ARG = SP - 5 - n_args
@SP
D=M
@5
D=D-A
@${n_args}
D=D-A
@ARG
M=D
## LCL = SP
@SP
D=M
@LCL
M=D
## goto functionName
@${symbol}
0;JMP
## output return address label
(${return_addr})

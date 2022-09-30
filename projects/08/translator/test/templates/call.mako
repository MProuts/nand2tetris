## push return address
@Foo.bar$ret.47
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
@2
D=D-A
@ARG
M=D
## LCL = SP
@SP
D=M
@LCL
M=D
## goto functionName
@Foo.bar
0;JMP
## output return address label
(Foo.bar$ret.47)

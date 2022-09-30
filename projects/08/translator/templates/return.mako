## save end of frame:
## R13 = LCL
@LCL
D=M
@R13
M=D
## save caller's return address:
## R14 = *(LCL - 5)
@LCL
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
## copy over return value:
## *ARG = pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
## reset stack pointer:
## SP = ARG + 1
@ARG
D=M+1
@SP
M=D
## reset THAT pointer:
## THAT = end_frame - 1
@R13
D=M-1
A=D
D=M
@THAT
M=D
## reset THIS pointer:
## THIS = *(end_frame - 2)
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
## reset ARG pointer:
## ARG = *(end_frame - 3)
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
## reset LCL pointer:
## LCL = *(end_frame - 4)
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
## goto caller's return address:
@R14
A=M
0;JMP

(${symbol})
% for i in range(nvars):
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
% endfor

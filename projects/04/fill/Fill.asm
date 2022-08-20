// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// if KBD == 0, GOTO WHITE
(START)
  @KBD
  D=M
  @WHITE
  D;JEQ

  // else set the substitution value to -1
  @sub
  M=-1
  @REFRESH
  0;JMP

  (WHITE)
    // set the substitution value to 0
    @sub
    M=0
    @REFRESH
    0;JMP

  (REFRESH)
  // set up loop variables
  @i
  M=0
  @8159
  D=A
  @words
  M=D

  (LOOP)
    // if i >= words jump to start
    @words
    D=M
    @i
    D=D-M
    @START
    D;JLE

    // set screen address to manipulate
    @SCREEN
    D=A
    @i
    D=D+M
    @addr
    M=D

    // set screen address to substitution value
    @sub
    D=M
    @addr
    A=M
    M=D

    // increment loop index
    @i
    M=M+1

    @LOOP
    0;JMP

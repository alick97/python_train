#!/usr/bin/env python3
from lex import *
from parse import *
from emit import *
import sys


def main():
    print("Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    # Initialize the lexer and parser.
    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()  # Start the parser.
    emitter.writeFile()  # Write the output to file.
    print("Compiling completed.")

main()

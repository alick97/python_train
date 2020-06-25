#### tinycompiler
---

This is a small compiler to demonstrate how compilers work.

Read the tutorial: [Let's make a Teeny Tiny compiler, part 1](http://web.eecs.utk.edu/~azh/blog/teenytinycompiler1.html)

> Note: Most Code from https://github.com/AZHenley/teenytinycompiler.

It supports:

- Numerical variables
- Basic arithmetic
- If statements
- While loops
- Print text and numbers
- Input numbers
- Labels and goto
- Comments

Example code:
```
PRINT "How many fibonacci numbers do you want?"
INPUT nums

LET a = 0
LET b = 1
WHILE nums > 0 REPEAT
    PRINT a
    LET c = a + b
    LET a = b
    LET b = c
ENDWHILE
```
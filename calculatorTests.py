from calculator import calculate

def testCalculate():
    # Test for no string input
    assert calculate("")=="No input was entered." 

    # Tests for basic computations
    assert calculate("1+2+3+4")=="10"
    assert calculate("1*2*3*4")=="24"
    assert calculate("6-5-4-3")=="-6"

    # Tests for precedence of combined operations
    assert calculate("6*2-7+4")=="9"
    assert calculate("8+1*1-9")=="0"
    assert calculate("99-24+9*4")=="111"

    # Tests for invalid numbers
    assert calculate("x+1")== "Not a valid input"
    assert calculate("p-1")== "Not a valid input"
    assert calculate("a*1")== "Not a valid input"

    # Tests for invalid operations
    assert calculate("1/2")=="Not a valid input"
    assert calculate("1x2")=="Not a valid input"
    assert calculate("1=2")=="Not a valid input"

    # Tests for strings beginning and ending with an operation
    assert calculate("1+2+3+")=="Expression cannot end with an operation"
    assert calculate("1+2+3*")=="Expression cannot end with an operation"
    assert calculate("1+2+3-")=="Expression cannot end with an operation"
    assert calculate("+1+2+3")=="Expression cannot begin with an operation"
    assert calculate("*1+2+3")=="Expression cannot begin with an operation"
    assert calculate("--1+2+3")=="Expression cannot begin with an operation"
    assert calculate("+-1+2+3")=="Expression cannot begin with an operation"
    assert calculate("*-1+2+3")=="Expression cannot begin with an operation"
    
    # Tests for negative numbers
    assert calculate("-2+1")=="-1"
    assert calculate("-2-1")=="-3"
    assert calculate("-2+-1")=="-3"
    assert calculate("-2*-2")=="4"
    assert calculate("2*-2")=="-4"
    assert calculate("-2*3")=="-6"

    # Tests for consecutive operators
    assert calculate("2+++2")=="Invalid string, contains consecutive operators"
    assert calculate("2---2")=="Invalid string, contains consecutive operators"
    assert calculate("2**2")=="Invalid string, contains consecutive operators"
    assert calculate("2-*2")=="Invalid string, contains consecutive operators"
    assert calculate("2+*2")=="Invalid string, contains consecutive operators"
    assert calculate("2-+2")=="Invalid string, contains consecutive operators"
    assert calculate("2*+2")=="Invalid string, contains consecutive operators"
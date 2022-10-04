from calculator import calculate

def testCalculate():
    # Tests for string of 0s
    assert calculate("0+0+0+0")=="0"
    assert calculate("0-0-0-0")=="0"
    assert calculate("0*0*0*0")=="0" 
    
    # Tests for addition
    assert calculate("1+2+3+4")=="10"
    
    # Tests for multiplication
    assert calculate("1*2*3*4")=="24"
    
    # Tests for subtraction
    assert calculate("6-5-4-3")=="-6"

    # Tests for precedence of combined operations
    assert calculate("6*2-7+4")="9"
    assert calculate("8+1*1-9")="0"
    assert calculate("99-24+9*4")="111"

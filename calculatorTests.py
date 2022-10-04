from calculator import calculate

def testCalculate():
    # Tests for addition
    assert calculate("1+2+3+4")=="10"
    
    # Tests for multiplication
    assert calculate("1*2*3*4")=="24"
    
    # Tests for subtraction
    assert calculate("30-5-4-3")=="18"

    

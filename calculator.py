import re

CONSECUTIVE_OPERATORS ="Invalid string, contains consecutive operators"


def calculate(exp):
    answer=""
    if exp:
        # checks for any non operators or digits
        if not re.search(r"[^\d\+\-\*]",exp):
            # checks for expressions beginning only with a single minus or not
            if re.search(r"^\-?\d",exp):
                # checks for expressions ending with only digits 
                if re.search(r"\d$", exp):
                    ############# ACTUAL OPERATIONS #############
                    validExpression = re.findall(r"\d+|[\+\-\*]", exp)
                    ############# Here at the moment
                    if validExpression[0] =="-":
                        validExpression[0:2]=["".join(validExpression[0:2])]

                    while (validExpression.count("*") > 0):
                        opIndex = validExpression.index("*")
                        if validExpression[opIndex-1]=="+" or validExpression[opIndex-1]=="-": 
	                        return CONSECUTIVE_OPERATORS
                        if (validExpression[opIndex+1]=="+" or validExpression[opIndex+1]=="*"):
                            return CONSECUTIVE_OPERATORS
                        if (validExpression[opIndex+1]=="+" or validExpression[opIndex+1]=="*") and (validExpression[opIndex+2]=="+" or validExpression[opIndex+2]=="-" or validExpression[opIndex+2]=="*"): 
	                        return CONSECUTIVE_OPERATORS
                        if validExpression[opIndex+1] =="-" and (validExpression[opIndex+2]=="+" or validExpression[opIndex+2]=="-" or validExpression[opIndex+2]=="*"): 
	                        return CONSECUTIVE_OPERATORS
                        if validExpression[opIndex+1] =="-":
                            validExpression[opIndex+1:opIndex+3] = ["".join(validExpression[opIndex+1:opIndex+3])]
                        computedValue = int(validExpression[opIndex-1])*int(validExpression[opIndex+1])
                        validExpression[opIndex-1] = computedValue
                        validExpression.pop(opIndex+1)
                        validExpression.pop(opIndex)

                    while (validExpression.count("-") > 0):
                        opIndex = validExpression.index("-")
                        if validExpression[opIndex+1]=="-" or validExpression[opIndex+1]=="+":
                            return CONSECUTIVE_OPERATORS
                        if validExpression[opIndex-1]=="+":
                            validExpression.pop(opIndex-1)
                        else:
                            computedValue = int(validExpression[opIndex-1])-int(validExpression[opIndex+1])
                            validExpression[opIndex-1] = computedValue
                            validExpression.pop(opIndex+1)
                            validExpression.pop(opIndex)
                    
                    while (validExpression.count("+") > 0):
                        opIndex = validExpression.index("+")
                        if validExpression[opIndex+1]=="+":
                            return CONSECUTIVE_OPERATORS
                        computedValue = int(validExpression[opIndex-1])+int(validExpression[opIndex+1])
                        validExpression[opIndex-1] = computedValue
                        validExpression.pop(opIndex+1)
                        validExpression.pop(opIndex)

                    answer=str(validExpression[0])

                else:
                    answer="Expression cannot end with an operation"
            else:
                answer="Expression cannot begin with an operation"
        else:
            answer="Not a valid input"
    else:
        answer="No input was entered."
    return answer

print("Enter an expression")

answer = calculate(input())

print(answer)
def calcAndReplace(destiList, index):
    if destiList[index] == '+':
        destiList[index] = str(
            float(destiList[index - 1]) + float(destiList[index + 1]))
        destiList.pop(index - 1)
        destiList.pop(index)
        return destiList
    elif destiList[index] == '-':
        destiList[index] = str(
            float(destiList[index - 1]) - float(destiList[index + 1]))
        destiList.pop(index - 1)
        destiList.pop(index)
        return destiList
    elif destiList[index] == '*':
        destiList[index] = str(
            float(destiList[index - 1]) * float(destiList[index + 1]))
        destiList.pop(index - 1)
        destiList.pop(index)
        return destiList
    elif destiList[index] == '/':
        try:
            destiList[index] = str(
                float(destiList[index - 1]) / float(destiList[index + 1]))
            destiList.pop(index - 1)
            destiList.pop(index)
            return destiList
        except ZeroDivisionError:
            pass


# Calculate arithmetic expressions, without parentheses
def calcFourFunction(exprList):
    i = 0
    while True:
        if exprList[i] == '*' or exprList[i] == '/':
            exprList = calcAndReplace(exprList, exprList.index(exprList[i]))
            i = 0
        if i + 1 == len(exprList):
            break
        i = i + 1

    i = 0
    while True:
        if exprList[i] == '+' or exprList[i] == '-':
            exprList = calcAndReplace(exprList, exprList.index(exprList[i]))
            i = 0
        if i + 1 == len(exprList):
            break
        i = i + 1

    return (exprList[0])


def calcParentheses(exprList):
    for i in range(0, len(exprList)):
        if type(exprList[i]) == type([]):
            exprList[i] = calcParentheses(exprList[i])
    return calcFourFunction(exprList)


# Method for
def calc(expr):
    # Remove spaces
    try:
        while True:
            expr.remove(' ')
    except ValueError:
        pass

    # Convert expression to list 'exprList'
    exprList = []
    temp = ''
    for i in expr:
        try:
            if i == '.':
                pass
            else:
                int(i)
            temp = temp + i
        except ValueError:
            if temp != '':
                exprList.append(temp)
            exprList.append(i)
            temp = ''
    exprList.append(temp)
    
    # Handle parentheses
    leftParenthesesCount = 0
    rightParenthesesCount = 0
    for i in range(0, len(exprList)):
        if exprList[i] == '(':
            leftParenthesesCount = leftParenthesesCount + 1
        elif exprList[i] == ')':
            rightParenthesesCount = rightParenthesesCount + 1
    if leftParenthesesCount >= rightParenthesesCount:
        for i in range(0,leftParenthesesCount-rightParenthesesCount):
            exprList.append(')')
    elif leftParenthesesCount <= rightParenthesesCount:
        return 'Syntax Error'

    change = True
    while change == True:
        temp = []
        indexIndicator = 0
        change = False
        for i in range(0, len(exprList)):
            temp.append(exprList[i])
            if exprList[i] == '(':
                indexIndicator = i
                temp = []
                change = True
            elif exprList[i] == ')':
                temp.pop()
                for x in range(len(temp) + 2):
                    del exprList[indexIndicator]
                exprList.insert(indexIndicator, temp)
                break

    # Calculate
    return calcParentheses(exprList)

# EXECUTE
if __name__ == "__main__":
    while True:
        expr = list(input('>'))
        if expr == []:
            continue
        elif expr == ['q']:
            break
        print(calc(expr))
        print()

def calc_and_replace(desti_list, index):
    if desti_list[index] == '+':
        desti_list[index] = str(
            float(desti_list[index - 1]) + float(desti_list[index + 1]))
        desti_list.pop(index - 1)
        desti_list.pop(index)
        return desti_list
    elif desti_list[index] == '-':
        desti_list[index] = str(
            float(desti_list[index - 1]) - float(desti_list[index + 1]))
        desti_list.pop(index - 1)
        desti_list.pop(index)
        return desti_list
    elif desti_list[index] == '*':
        desti_list[index] = str(
            float(desti_list[index - 1]) * float(desti_list[index + 1]))
        desti_list.pop(index - 1)
        desti_list.pop(index)
        return desti_list
    elif desti_list[index] == '/':
        try:
            desti_list[index] = str(
                float(desti_list[index - 1]) / float(desti_list[index + 1]))
            desti_list.pop(index - 1)
            desti_list.pop(index)
            return desti_list
        except ZeroDivisionError:
            pass


# Calculate arithmetic expressions, without parentheses
def calc_four_function(expr_list):
    i = 0
    while True:
        if expr_list[i] == '*' or expr_list[i] == '/':
            expr_list = calc_and_replace(expr_list, expr_list.index(expr_list[i]))
            i = 0
        if i + 1 == len(expr_list):
            break
        i = i + 1

    i = 0
    while True:
        if expr_list[i] == '+' or expr_list[i] == '-':
            expr_list = calc_and_replace(expr_list, expr_list.index(expr_list[i]))
            i = 0
        if i + 1 == len(expr_list):
            break
        i = i + 1

    return (expr_list[0])


def calc_parentheses(expr_list):
    for i in range(0, len(expr_list)):
        if type(expr_list[i]) == type([]):
            expr_list[i] = calc_parentheses(expr_list[i])
    return calc_four_function(expr_list)


# Method for
def calc(expr):
    # Remove spaces
    try:
        while True:
            expr.remove(' ')
    except ValueError:
        pass

    # Convert expression to list 'expr_list'
    expr_list = []
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
                expr_list.append(temp)
            expr_list.append(i)
            temp = ''
    expr_list.append(temp)
    
    # Handle parentheses
    left_parentheses_count = 0
    right_parentheses_count = 0
    for i in range(0, len(expr_list)):
        if expr_list[i] == '(':
            left_parentheses_count = left_parentheses_count + 1
        elif expr_list[i] == ')':
            right_parentheses_count = right_parentheses_count + 1
    if left_parentheses_count >= right_parentheses_count:
        for i in range(0,left_parentheses_count-right_parentheses_count):
            expr_list.append(')')
    elif left_parentheses_count <= right_parentheses_count:
        return 'Syntax Error'

    change = True
    while change == True:
        temp = []
        index_indicator = 0
        change = False
        for i in range(0, len(expr_list)):
            temp.append(expr_list[i])
            if expr_list[i] == '(':
                index_indicator = i
                temp = []
                change = True
            elif expr_list[i] == ')':
                temp.pop()
                for x in range(len(temp) + 2):
                    del expr_list[index_indicator]
                expr_list.insert(index_indicator, temp)
                break

    # Calculate
    return calc_parentheses(expr_list)

# EXECUTE
if __name__ == "__main__":
    while True:
        expr = list(input('> '))
        if expr == []:
            continue
        elif expr == ['q']:
            break
        print(calc(expr))
        print()

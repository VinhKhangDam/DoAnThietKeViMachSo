import networkx as nx

#Độ ưu tiên toán tử:* có độ ưu tiên cao hơn +
def OperatorPrecedence (op):
    if op == '+':
        return 1
    elif op == '*':
        return 2
    else:
        return 0

#Giữ nguyên toán tử 
def OperatorProcessing(operand1, operand2, operator, q: list = None) -> str:
    #Lưu q mặc định là None khi không cần sử dụng
    expression = f"{operand1}{operator}{operand2}"
    if q is not None:
        q.append(expression)
    return expression
#Đảo ng ược toán tử
def OperatorProcessing_inv(operand1, operand2, operator,q: list = None) -> str:
    new_op = '*' if operator == '+' else '+'
    expression = f"{operand1}{new_op}{operand2}"
    if q is not None:
        q.append(expression)
    return expression
    
def EvaluateExpression_inv(expression, q):
    operand_stack = []
    operator_stack = []
    index = 0
    n = len(expression)

    while index < n:
        token = expression[index]
        #Xu li khoang trang
        if token.isspace():
            index += 1
        #Xu li ki tu
        elif token.isalpha():
            operand_stack.append(token)
            index += 1
        elif token.isdigit():
            num = token
            while index + 1 < n and expression[index+1].isdigit():
                num += expression[index+1]
                index += 1
            operand_stack.append(num)
            index += 1
        elif token in '+-*/^':
            while (operator_stack and operator_stack[-1] != '(' and
                   OperatorPrecedence(operator_stack[-1]) >= OperatorPrecedence(token)):
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                operand_stack.append(OperatorProcessing(operand1, operand2, operator))
            operator_stack.append(token)
            index += 1
        elif token == '(':
            operator_stack.appen(token)
            index += 1
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                operand_stack.append(OperatorProcessing(operand1, operand2, operator))
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
            else :
                raise ValueError("Mismatched parentheses")
            index += 1
        else:
            raise ValueError(f"Invalid token: '{token}")
    
    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        operand_stack.append(OperatorProcessing(operand1, operand2, operator))

    if len(operand_stack) != 1:
        raise ValueError("Invalid expression")

    return operand_stack.pop()

def EvaluateExpression(expression, q):
    operand_stack = []
    operator_stack = []
    index = 0

    while index < len(expression):
        token = expression[index]
        if token.isalpha():
            operand_stack.append((token))
            index += 1
        elif token in '+-*/^':
            while (len(operator_stack) != 0 and OperatorPrecedence(operator_stack[-1]) >= OperatorPrecedence(token)):
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = OperatorProcessing(operand1, operand2, operator, q)
                q.append(result)
                operand_stack.append(result)
            operator_stack.append(token)
            index += 1
        elif token == '(':
            operator_stack.append(token)
            index += 1
        elif token == ')':
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = OperatorProcessing(operand1, operand2, operator, q)
                q.append(result)
                operand_stack.append(result)
            operator_stack.pop()  
            index += 1
        else:
            
            index += 1

    while len(operator_stack) != 0:
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = OperatorProcessing(operand1, operand2, operator, q)
        q.append(result)
        operand_stack.append(result)

    return operand_stack.pop()

def SubtractExpression(expression1, expression2):
    #loai bo ki tu giong nhau
    str1 = str(expression1)
    str2 = str(expression2)

    if str1.startswith(str2):
        return str1[len(str2):]
    return str1

def IntersectionExpression(expression1, expression2):
    #Tim phan giao giua 2 bieu thuc
    i = 0
    j = 0
    result = ''
    while i < len(expression1):
        if (expression1[i] == expression2[j]):
            result += expression1[i]
            i += 1
            j += 1
        else: i += 1
        if j == len(expression2):break
        
    return result
                             
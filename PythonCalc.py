def calc(operator, num1, num2=None):
    if not isinstance(num1, (int, float)):
        raise ValueError(f'Invalid number "{num1}"')
    if num2 is not None and not isinstance(num2, (int, float)):
        raise ValueError(f'Invalid number "{num2}"')

    if operator == '+' or operator == 'add':
        if num2 is None:
            answer = +num1
        else:
            answer = num1 + num2
    elif operator == '-' or operator == 'sub':
        if num2 is None:
            answer = -num1
        else:
            answer = num1 - num2
    elif operator == '*' or operator == 'mul':
        answer = num1 * num2
    elif operator == '/' or operator == 'div':
        if num2 == 0:
            raise ValueError("Division by zero")
        else:
            answer = num1 / num2
    elif operator == '%' or operator == 'mod':
        if num2 == 0:
            raise ValueError("Division by zero")
        else:
            answer = num1 % num2
    elif operator == '^' or operator == 'pow':
        answer = num1 ** num2
    else:
        raise ValueError(f'Invalid operator "{operator}"')
    
    return answer

def eval(expression):
    if not isinstance(expression, list):
        raise ValueError(f'Failed to evaluate "{expression}"')
    if len(expression) < 2:
        raise ValueError(f'Failed to evaluate "{expression}"')
    if len(expression) > 3:
        raise ValueError(f'Failed to evaluate "{expression}"')

    if len(expression) == 2:
        operator = expression[0]
        num1 = expression[1]
        num2 = None
        if isinstance(num1, list):
            num1 = eval(num1)
        else:
            return calc(operator, num1, num2)
    elif len(expression) == 3:
        operator = expression[0]
        num1 = expression[1]
        num2 = expression[2]
        if isinstance(num1, list):
            num1 = eval(num1)
        if isinstance(num2, list):
            num2 = eval(num2)

    return calc(operator, num1, num2)

def struct(expression):
    i = 0
    function_operators = {'^', 'pow'}
    high_priority_operators = {'*', '/', '%', 'mul', 'div', 'mod'}
    low_priority_operators = {'+', '-', 'add', 'sub'}

    if not isinstance(expression, list):
        raise TypeError(f'Failed to structure "{expression}"')
    elif len(expression) == 1 and any(expression[0] in operator_set for operator_set in [function_operators, high_priority_operators, low_priority_operators]):
        raise TypeError(f'Failed to structure "{expression}"')
    elif len(expression) % 2 == 0 and not isinstance(expression[-1], (int, float, list)):
        raise TypeError(f'Failed to structure "{expression}"')

    if len(expression) == 2:
        return expression

    while i < len(expression):
        if i + 2 < len(expression) and isinstance(expression[i + 1], str) and expression[i + 1] in function_operators:
            nested_expr = [expression[i + 1], expression[i], expression[i + 2]]
            expression[i:i + 3] = [nested_expr]
            i -= 1
        i += 1

    i = 0
    while i < len(expression):
        if i + 2 < len(expression) and isinstance(expression[i + 1], str) and expression[i + 1] in high_priority_operators:
            nested_expr = [expression[i + 1], expression[i], expression[i + 2]]
            expression[i:i + 3] = [nested_expr]
            i -= 1
        i += 1

    i = 0  
    while i < len(expression):
        if i + 2 < len(expression) and isinstance(expression[i + 1], str) and expression[i + 1] in low_priority_operators: 
            nested_expr = [expression[i + 1], expression[i], expression[i + 2]]
            expression[i:i + 3] = [nested_expr]
            i -= 1
        i += 1
    
    i = 0  
    while i < len(expression):
        if i + 2 < len(expression) and expression[i + 1] not in (high_priority_operators, function_operators, low_priority_operators) and not isinstance(expression[i + 1], (int, float)) and expression[i + 1] != 'list':
            nested_expr = [expression[i + 1], expression[i], expression[i + 2]]
            expression[i:i + 3] = [nested_expr]
            i -= 1
        i += 1
    
    if isinstance(expression, list) and len(expression) == 1 and isinstance(expression[0], list):
        expression = expression[0]

    return expression

def get_next(s, start_index):
    if start_index >= len(s):
        raise ValueError('End of string')
    if not s:
        raise ValueError('End of string')

    current_char = s[start_index]
    if not current_char.isdigit() and current_char != '.':
        result = current_char
        while start_index + 1 < len(s):
            next_char = s[start_index + 1]
            if next_char.isalpha() or (not next_char.isdigit() and next_char != '('):
                start_index += 1
                result += next_char
            else:
                break
        return result

    result = current_char
    while start_index + 1 < len(s):
        next_char = s[start_index + 1]
        if next_char.isdigit() or next_char == '.':
            start_index += 1
            result += next_char
        elif not next_char.isdigit() and next_char != '.':
            break

    return int(result) if result.isdigit() else float(result)

def pre_parse(s):
    pfcount = s.count('(')
    plcount = s.count(')')
    if pfcount != plcount:
        raise TypeError(f'Not matching parenthesis')

def parse(s):
    pre_parse(s)
    s = s.replace(' ', '')
    plist = []
    index = 0
    while index < len(s):
        current_char = s[index]
        if current_char == '(':
            closing_index = index + 1
            count_open = 1
            while closing_index < len(s) and count_open > 0:
                if s[closing_index] == '(':
                    count_open += 1
                if s[closing_index] == ')':
                    count_open -= 1
                closing_index += 1
            nested_expression = parse(s[index + 1 : closing_index - 1])
            plist.append(nested_expression)

            index = closing_index
        else:
            a = get_next(s, index)
            plist.append(a)
            index += len(str(a))

    plist = struct(plist)
    return plist

def coordinate(s):
    try:
        parsed_func = parse(s)
        answer = eval(parsed_func)
        return answer
    except Exception as e:
        return f'Error: {e}'

def main():
    while True:
        user_input = input()
        if user_input.lower() in {'q', 'quit'}:
            break
        result = coordinate(user_input)
        print(result)

if __name__ == '__main__':
    main()
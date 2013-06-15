"""Evaluates mathematical expressions with addition, subtraction,
   division, and multiplication using order of operations. The
   Shunting-Yard algorithm is used to evaluate these expressions
   in a clean and simple way."""
import shlex


def main():
    """"Evaluates expressions until nothing is returned from the user."""
    while True:
        expression = raw_input('>> ')
        if not expression:
            break
        result = evaluate(expression)
        print(result)


def evaluate(expression):
    """Evaluates the given expression and returns the result."""
    tokens = get_tokens_from(expression)
    result = evaluate_from(tokens)
    return result


def get_tokens_from(expression):
    """Returns a list of tokens in string form."""
    return list(shlex.shlex(expression))


def evaluate_from(tokens):
    """Uses the Shunting-Yard algorithm to evaluate the expression from the
       given tokens. Returns the mathematical result of the expression."""
    operands = []
    operators = []

    for token in tokens:
        if is_operator(token):
            # Evaluate all higher precedence operators before pushing next
            # operator onto the operators stack.
            while operators and is_operator(operators[-1]) and \
                    precedence(token) <= precedence(operators[-1]):
                perform_next_operation(operands, operators)

            operators.append(token)

        elif token == '(':
            operators.append(token)
        # If we hit the closing parentheses...
        elif token == ')':
            # Evaluate the entire expression within these parentheses.
            while operators[-1] != '(':
                perform_next_operation(operands, operators)

            # Pop off the matching opening parentheses.
            operators.pop()

        # Otherwise token is a number, so just append it to the operands stack.
        else:
            operands.append(token)

    # Done processing tokens. Finish evaluating them.
    while operators:
        perform_next_operation(operands, operators)

    return operands.pop()


def is_operator(token):
    """Returns whether the specified token is an operator."""
    return token == '+' or token == '-' or \
        token == '*' or token == '/' or token == '^'


def precedence(operator):
    """Returns the precedence of the specified operator."""
    if operator == '+' or operator == '-':
        return 0
    elif operator == '*' or operator == '/':
        return 1
    elif operator == '^':
        return 2


def perform_next_operation(operands, operators):
    """Given a stack of operands and operators, pops two numbers off the
       operands stack and applies the next operator on the operators stack.
       Finally, pushes this result to the operands stack."""
    rhs = convert_to_float(operands.pop())
    lhs = convert_to_float(operands.pop())
    operator = operators.pop()
    result = perform_operation(lhs, rhs, operator)
    operands.append(result)


def convert_to_float(token):
    """Returns the float representation of token if token is a number.
       If token is some other type, an exception is raised."""
    try:
        return float(token)
    except ValueError:
        print('ValueError: ' + token + ' is an invalid real number')
        raise


def perform_operation(lhs, rhs, operator):
    """Performs the operation 'lhs operator rhs', where lhs and rhs are numbers
       and operator is a string holding '+', '-', '*', or '/'."""
    if operator == '+':
        return lhs + rhs
    elif operator == '-':
        return lhs - rhs
    elif operator == '*':
        return lhs * rhs
    elif operator == '/':
        return lhs / rhs
    elif operator == '^':
        return lhs**rhs

if __name__ == '__main__':
    main()

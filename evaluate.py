"""Evaluates mathematical expressions with addition, subtraction,
   division, and multiplication using order of operations. The
   Shunting-Yard algorithm is used to evaluate these expressions
   in a simple and clean way."""
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
    """Returns a list of tokens (numbers and operator strings)."""
    tokens = list(shlex.shlex(expression))
    tokens = [convert(token) for token in tokens]
    return tokens

def convert(token):
    """Returns the integer representation of token if token is a number.
       Otherwise, returns the original token."""
    try:
        return int(token)
    except ValueError:
        return token

def evaluate_from(tokens):
    """Uses the Shunting-Yard algorithm to evaluate the expression from the
       given tokens. Returns the mathematical result of the expression."""
    operands = []
    operators = []

    for token in tokens:
        if type(token) == int:
            operands.append(token)
        else:
            # Evaluate all higher precedence operators before pushing next 
            # operator.
            while operators and precedence(token) <= precedence(operators[-1]):
                perform_next_operation(operands, operators)
            
            operators.append(token)

    # Done processing tokens. Now finish evaluating tokens.
    while operators:
        perform_next_operation(operands, operators)

    return operands.pop()

def precedence(operator):
    """Returns 0 for addition and subtraction and 1 for multiplcation and 
       division. Used to compare precedence of operators."""
    if operator == '+' or operator == '-':
        return 0
    else:
        return 1

def perform_next_operation(operands, operators):
    """Given a stack of operands and operators, pops two numbers off the 
       operands stack and applies the next operator on the operators stack.
       Finally, pushes this result to the operands stack."""
    rhs = operands.pop()
    lhs = operands.pop()
    operator = operators.pop()
    result = perform_operation(lhs, rhs, operator)
    operands.append(result)

def perform_operation(lhs, rhs, operator):
    """Performs the operation 'lhs operator rhs', where lhs and rhs are numbers
       and operator is a string holding '+', '-', '*', or '/'."""
    if operator == '+':
        return lhs + rhs
    elif operator == '-':
        return lhs - rhs
    elif operator == '*':
        return float(lhs) * float(rhs)
    elif operator == '/':
        return float(lhs) / float(rhs)

if __name__ == '__main__':
    main()

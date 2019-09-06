import re

add = lambda a,b: a+b
mult = lambda a,b: a*b
sub = lambda a,b: a-b
def div(a, b):
   if b == 0:
      raise ValueError('divide by 0 not allowed')
   return a / b

op_map = {'*': mult, '+': add, '-':sub, '/':div}

def simple_calculator(calculation):
   """Receives 'calculation' and returns the calculated result,

      Examples - input -> output:
      '2 * 3' -> 6
      '2 + 6' -> 8

      Support +, -, * and /, use "true" division (so 2/3 is .66
      rather than 0)

      Make sure you convert both numbers to ints.
      If bad data is passed in, raise a ValueError.
   """
   expr_match = re.match(r'([+-]*\d+)\s*([*|+|/|-])\s*([+-]*\d+)', calculation.strip())
   if expr_match:
      a = int(expr_match.groups()[0])
      b = int(expr_match.groups()[2])
      op = expr_match.groups()[1]
      return op_map[op](a,b)
   else:
      raise ValueError()
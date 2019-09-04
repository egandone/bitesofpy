STAR = '*'

def gen_rhombus(width):
    """Create a generator that yields the rows of a rhombus row
       by row. So if width = 5 it should generate the following
       rows one by one:

       gen = gen_rhombus(5)
       for row in gen:
           print(row)

        output:
          *
         ***
        *****
         ***
          *
    """
    for i in range(-(width - 1), width, 2):
      star_count = width - abs(i)
      stars = '*' * star_count
      yield stars.center(width)

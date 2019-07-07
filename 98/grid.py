from collections import namedtuple
DOWN, UP, LEFT, RIGHT = '⇓', '⇑', '⇐', '⇒'
START_VALUE = 1

Edge = namedtuple('Edge', 'p1 direction p2')

def tokenize_grid(grid):
    lines = grid.strip().splitlines()
    # Assume the first line is the maximum length.  Need this
    # to pad every line to the correct length so when it is
    # tokenized we end up with a token at every position
    line_length = len(lines[0])
    token_grid = []
    for line in lines:
       padded_line = line.ljust(line_length)
       p = 0
       tokens = []
       while p < line_length:
          number = padded_line[p:p+3].strip()
          tokens.append(number)
          if p + 5 < line_length:
             join = padded_line[p+3:p+5].strip()
             tokens.append(join)
          p = p + 5
       token_grid.append(tokens)
    return token_grid

def build_edges(token_grid):
   edges = []
   for y in range(len(token_grid)):
      for x in range(len(token_grid[y])):
         #print(f'[{y}][{x}] = {token_grid[y][x]}')
         if token_grid[y][x] == '-':
            #print(f'    [{y}][{x-1}] = {token_grid[y][x-1]} - [{y}][{x+1}] = {token_grid[y][x+1]}')
            p1 = int(token_grid[y][x-1])
            p2 = int(token_grid[y][x+1])
            if p1 < p2:
               edge = Edge(p1, RIGHT, p2)
            else:
               edge = Edge(p2, LEFT, p1)
            edges.append(edge)
         elif token_grid[y][x] == '|':
            #print(f'    [{y-1}][{x}] = {token_grid[y-1][x]} | [{y+1}][{x}] = {token_grid[y+1][x]}')
            p1 = int(token_grid[y-1][x])
            p2 = int(token_grid[y+1][x])
            if p1 < p2:
               edge = Edge(p1, DOWN, p2)
            else:
               edge = Edge(p2, UP, p1)
            edges.append(edge)
   return edges

def print_sequence_route(grid, start_coordinates=START_VALUE):
   """Receive grid string, convert to 2D matrix of ints, find the
       START_VALUE coordinates and move through the numbers in order printing
       them.  Each time you turn append the grid with its corresponding symbol
       (DOWN / UP / LEFT / RIGHT). See the TESTS for more info."""
   token_grid = tokenize_grid(grid)
   edges = build_edges(token_grid)
   # Filter out and edges with a start before our starting point
   edges = [edge for edge in edges if edge.p1 >= start_coordinates]
   # Now sort the list so we can just walk through the list in order
   edges = sorted(edges, key = lambda e: e.p1)
   current_direction = None
   out_list = []
   for edge in edges:
      if not current_direction:
         # Print out the starting point at set initial direction
         out_list.append(str(edge.p1))
         current_direction = edge.direction
      # Always print out the detination point
      out_list.append(str(edge.p2))
      # Check if this was a change in direction.  If
      # so then print out new direction
      if current_direction != edge.direction:
         out_list.append(edge.direction)
         current_direction = edge.direction   
   return out_list
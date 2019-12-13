STAR = "+"
LEAF = "*"
TRUNK = "|"


def generate_improved_xmas_tree(rows=10):
    """Generate a xmas tree with a star (+), leafs (*) and a trunk (|)
       for given rows of leafs (default 10).
       For more information see the test and the bite description"""
    width = rows * 2 - 1
    lines = [STAR.center(width, ' ')]
    for row in range(1, rows+1):
        leaves = LEAF * (row*2 - 1)
        lines.append(leaves.center(width, ' '))
    trunk = TRUNK * rows
    if rows % 2 == 0:
        trunk += TRUNK
    lines.append(trunk.center(width, ' '))
    lines.append(trunk.center(width, ' '))
    return '\n'.join(lines)

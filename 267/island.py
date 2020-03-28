# Hint:
# You can define a helper funtion: get_others(map, row, col) to assist you.
# Then in the main island_size function just call it when traversing the map.


def count_outside_edges(map_, r, c):
    """Go through the map and check the size of the island
       (= summing up all the 1s that are part of the island)

       Input - the map, row, column position
       Output - return the total numbe)
    """
    nums = 0
    if map_[r][c] == 1:
        if c == 0 or map_[r][c-1] == 0:
            nums += 1
        if c == (len(map_[r]) - 1) or map_[r][c+1] == 0:
            nums += 1
        if r == 0 or map_[r-1][c] == 0:
            nums += 1
        if r == (len(map_) - 1) or map_[r+1][c] == 0:
            nums += 1
    return nums


def island_size(map_):
    """Hint: use the get_others helper

    Input: the map
    Output: the perimeter of the island
    """
    perimeter = 0
    for r in range(len(map_)):
        for c in range(len(map_[r])):
            perimeter += count_outside_edges(map_, r, c)

    return perimeter

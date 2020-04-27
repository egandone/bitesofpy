value_map = dict()

old_sequence_map = set([1])
for i in range(1, 50):
    print(f'doing len={i}, {len(old_sequence_map)*2} additions')
    new_sequence_map = set()
    for value in old_sequence_map:
        new_value = value * 2
        new_sequence_map.add(new_value)
        if new_value not in value_map:
            value_map[new_value] = i

        new_value = value // 3
        new_sequence_map.add(new_value)
        if new_value not in value_map:
            value_map[new_value] = i
    old_sequence_map = new_sequence_map

for i in [10, 12, 15, 33, 55, 102, 1985, 2020, 3012]:
    if i in value_map:
        print(f'{i} -> {value_map[i]}')

# for i in range(20):
#     if i in value_map:
#         print(f'{i} -> {value_map[i]}')

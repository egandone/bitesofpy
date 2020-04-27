from array import array

value_map = dict()

value_map[1] = len('223')
value_map[2] = len('2')
value_map[4] = len('22')
value_map[8] = len('222')
value_map[16] = len('2222')
value_map[32] = len('22222')
value_map[64] = len('222222')

old_sequence_map = array('i', [8])
for i in range(4, 30):
    print(f'doing len={i}, {len(old_sequence_map)*2} additions')
    new_sequence_map = array('i')
    for value in old_sequence_map:
        new_value = value * 2
        # if new_value == 10:
        #     print(f'10 --> {new_key}')
        new_sequence_map.extend([new_value])
        if new_value not in value_map:
            value_map[new_value] = i

        new_value = value // 3
        # if new_value == 10:
        #     print(f'10 --> {new_key}')
        new_sequence_map.extend([new_value])
        if new_value not in value_map:
            value_map[new_value] = i
    old_sequence_map = new_sequence_map

# if sequence_map[new_key] not in value_map:
#     value_map[sequence_map[new_key]] = new_key

# if sequence_map[new_key] not in value_map:
#     value_map[sequence_map[new_key]] = new_key

for i in [10, 12, 15, 33, 55, 102, 1985, 2020, 3012]:
    if i in value_map:
        print(f'{i} -> {value_map[i]}')

# for i in range(20):
#     if i in value_map:
#         print(f'{i} -> {value_map[i]}')

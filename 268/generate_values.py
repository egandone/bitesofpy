from itertools import product


value_map = dict()
sequence_map = dict()


def analyze(tuples):
    for t in tuples:
        if t[0:3] != (2, 2, 2):
            computed_value = 0
        elif t[:-1] in sequence_map:
            computed_value = sequence_map[t[:-1]]
            if t[-1] == 2:
                computed_value = computed_value * 2
            else:
                computed_value = computed_value // 3
        else:
            print(f'computing {t}')
            computed_value = 1
            for v in t:
                if computed_value > 0:
                    if v == 2:
                        computed_value = computed_value * 2
                    else:
                        computed_value = computed_value // 3
                else:
                    break
        sequence_map[t] = computed_value
        if (computed_value > 0) and (computed_value not in value_map):
            value_map[computed_value] = len(t)


analyze([(2, 2, 2)])
for i in range(4, 30):
    analyze(product([2, 3], repeat=i))

for i in [10, 12, 15, 33, 55, 102, 1985, 2020, 3012]:
    if i in value_map:
        print(f'{i} -> {value_map[i]}')

for i in range(20):
    if i in value_map:
        print(f'{i} -> {value_map[i]}')

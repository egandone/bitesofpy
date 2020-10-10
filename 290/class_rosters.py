import csv
import re


def class_rosters(input_file):
    ''' Read the input_file and modify the data
        according to the Bite description.
        Return a list holding one item per student
        per class, correctly formatted.'''
    course_map = {}
    with open(input_file) as f:
        input_data = f.read()
    for line in input_data.split('\n'):
        if line.strip():
            (id, first, last, *courses) = line.replace('"', '').split(',')
            for course in courses:
                if course:
                    if course not in course_map:
                        course_map[course] = []
#                    if id not in course_map[course]:
                    course_map[course].append(id)
    result = []
    for key, ids in course_map.items():
        course = re.sub('\s-\s\S+$', '', key)
        ids_str = ','.join(ids)
        result.append(f'{course},2020,{ids_str}')
    return result

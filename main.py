from generator.generation_methods import *

for i in range(10):
    student = random.choice([True, False])
    i1, i2, n = generate_names_and_surname(Sex.MALE)
    title = generate_scientific_title(student)
    print('student?: ', student, ' - ', i1, i2, n, ' [', title, ']')

for i in range(10):
    student = random.choice([True, False])
    i1, i2, n = generate_names_and_surname(Sex.FEMALE)
    title = generate_scientific_title(student)
    print('student?: ', student, ' - ', i1, i2, n, ' [', title, ']')

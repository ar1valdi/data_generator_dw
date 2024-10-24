from generator.generation_methods import *

for i in range(10):
    i1, i2, n = generate_names_and_surname(Sex.MALE)
    print(i1, i2, n)

for i in range(10):
    i1, i2, n = generate_names_and_surname(Sex.FEMALE)
    print(i1, i2, n)

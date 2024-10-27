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

cl = CourseLexicon()
sl = StudyLexicon()
for _ in range(20):
    s = generate_study(sl, 2017, 2024)
    print(s.nazwa, s.rok_rozpoczecia)

for _ in range(20):
    c = generate_course(cl, datetime.date(2017,1,1), datetime.date(2024,10,1))
    print(c.nazwa, c.data_utworzenia, c.ilosc_godzin, c.liczba_ects)

if False:
    names = set()
    for _ in range(10000000):
        names.add(generate_course_name(cl))

    print(len(names))

    names = set()
    for _ in range(5000000):
        names.add(generate_study_name(sl))

    print(len(names))

nums = []
for _ in range(1000):
    count = 0
    result = ""
    while result != "Hipertekst i Hipermedia":
        result = generate_course_name(cl)
        count += 1
    print(count)
    nums.append(count)
    
import matplotlib.pyplot as plt
plt.hist(nums)
plt.show()

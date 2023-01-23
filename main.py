class Student:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.sum_grades = 0
        self.count_grades = 0

    def __str__(self):
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}\n' \
              f'Средняя оценка за домашние задания: {self.sum_grades / self.count_grades if self.count_grades != 0 else 0}\n' \
              f'Курсы в процессе изучения: {courses_in_progress}\n' \
              f'Завершенные курсы: {finished_courses}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Не студент!')
            return
        return (self.sum_grades / self.count_grades) < (other.sum_grades / other.count_grades)

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
            lecturer.sum_grades += grade
            lecturer.count_grades += 1
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.sum_grades = 0
        self.count_grades = 0

    def __str__(self):
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}\n' \
              f'Средняя оценка за лекции: {self.sum_grades / self.count_grades if self.count_grades != 0 else 0}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Не лектор!')
            return
        return (self.sum_grades / self.count_grades) < (other.sum_grades / other.count_grades)


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\n '
        return res

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
            student.sum_grades += grade
            student.count_grades += 1
        else:
            return 'Ошибка'


# при таком решении (с одинаковыми названиями атрибутов внутри классов студентов и лекторов) можно обойтись одной
# функцией
def av_grade(persons, course):
    total = 0
    len_ = 0
    for person in persons:
        if course in person.grades:
            total += sum(person.grades[course]) / len(person.grades[course])
            len_ += 1
    return total / len_


# creating students
tor4ok = Student('Александр', 'Корчук')
tor4ok.courses_in_progress += ['Python', 'Java', 'БПЛА', 'Linux forever']
stranger = Student('Владислав', 'Розовский')
stranger.courses_in_progress += ['Python', 'Linux forever', 'Java']

# creating reviewers
belok = Reviewer('Александр', 'Белокопытов')
belok.courses_attached = ['БПЛА', 'Linux forever', 'Java']
ha4 = Reviewer('Артур', 'Хачатрян')
ha4.courses_attached = ['Python', 'Java', 'БПЛА', 'Linux forever']

# creating lecturers
lama = Lecturer('Лама', 'Далай')
lama.courses_attached = ['Python', 'Java']
inga = Lecturer('Ингиборге', 'Добкунайте')
inga.courses_attached = ['Python', 'Java', 'БПЛА', 'Linux forever']

# give grades
tor4ok.rate_hw(lama, 'Gfhf', 2)
belok.rate_hw(tor4ok, 'БПЛА', 2)
belok.rate_hw(tor4ok, 'Linux forever', 7)
belok.rate_hw(stranger, 'Java', 7)
belok.rate_hw(stranger, 'Linux forever', 6)
ha4.rate_hw(stranger, 'Python', 1)
stranger.rate_hw(lama, 'Python', 5)
stranger.rate_hw(lama, 'Python', 2)
stranger.rate_hw(inga, 'Python', 5)
stranger.rate_hw(inga, 'Java', 4)

# show results
print(tor4ok.grades)
print(stranger.grades)
print(av_grade([tor4ok, stranger], 'Linux forever'))

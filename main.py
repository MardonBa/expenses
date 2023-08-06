class Person:
    def __init__(self, age, hair_color, eye_color, school):
        self.age = age
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.school = school

    def grow_older(self):
        self.age = self.age + 1

    def change_school(self, new_school):
        self.school = new_school

class Teenager(Person):
    def __init__(self, age, hair_color, eye_color, school, smoking_status):
        super().__init__(age, hair_color, eye_color, school)
        self.smoking_status = smoking_status

    def change_smoking_status(self):
        if self.smoking_status == True:
            self.smoking_status = False
        else:
            self.smoking_status = True


person = Person(16, 'brown', 'green', 'GAC')
print(person.age)
person.grow_older()
print(person.age)

ellie = Teenager(16, 'brown', 'green', 'GAC', False)
print(ellie.age)
print(ellie.smoking_status)
ellie.change_smoking_status()
print(ellie.smoking_status)

ellie.change_school("College")
print(ellie.school)
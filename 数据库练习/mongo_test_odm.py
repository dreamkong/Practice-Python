from mongoengine import connect, Document, EmbeddedDocument, StringField, IntField, FloatField, ListField, EmbeddedDocumentField

connect('student')

SEX_CHOICES = (
    ('male', '男'),
    ('female', '女')
)


class Grade(EmbeddedDocument):
    '''成绩'''
    name = StringField(required=True)
    score = FloatField(required=True)


class Student(Document):
    name = StringField(max_length=20, required=True)
    sex = StringField(choices=SEX_CHOICES, requred=True)
    age = IntField(required=True)
    address = StringField()
    grades = ListField(EmbeddedDocumentField(Grade))

    meta = {
        'collection': 'students',
        # 以年龄倒序
        'ordering': ['-age']
    }


class MongonEngineTest():

    def add_one(self):
        math = Grade(
            name='张三',
            score=95.5
        )
        chinese = Grade(
            name='张三',
            score=98
        )
        english = Grade(
            name='张三',
            score=40
        )
        stu_obj = Student(
            name='张三',
            age=15,
            sex='male',
            grades=[math, chinese, english]
        )
        stu_obj.save()
        return stu_obj

    def get_one(self):
        '''查询一条数据'''
        return Student.objects.first()

    def get_more(self):
        return Student.objects.all()

    def get_from_oid(self, oid):
        return Student.objects.filter(pk=oid).first()

    def update_one(self):
        return Student.objects.filter(sex='male').update_one(inc__age=1)

    def update_more(self):
        return Student.objects.filter(sex='male').update(inc__age=1)

    def delete_one(self):
        rset = Student.objects.filter(sex='female').first()
        if rset:
            return rset.delete()
        return None

    def delete_more(self):
        return Student.objects.filter(sex='male').delete()


def main():
    obj = MongonEngineTest()
    # rest = obj.add_one()
    # print(rest.id)
    # rest = obj.get_one()
    # print(rest.id)
    # rest = obj.get_more()
    # for row in rest:
    #     print(row.name)
    # rest = obj.get_from_oid('5ac988aec3666e72258f2ee3')
    # rest = obj.update_one()
    # rest = obj.update_more()
    # rest = obj.delete_one()
    rest = obj.delete_more()
    print(rest)


if __name__ == '__main__':
    main()

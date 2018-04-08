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
    comments = ListField(EmbeddedDocumentField(Grade))

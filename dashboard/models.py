from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_lecture = models.BooleanField(default=False)

class EmailVerify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)



class HomeWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    finished = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


CLASS_CHOICE = (
    ('BCA', 'BCA'),
    ('MCA', 'MCA'),
    ('BBA', 'BBA'),
    ('MBA', 'MBA'),
    ('BCOM', 'BCOM'),
    ('MCOM', 'MCOM'),
    ('BA', 'BA'),
    ('MA', 'MA'),
    ('DIPLOMA', 'DIPLOMA'),
    ('ENGINEERING', 'ENGINEERING'),
)

class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=20)
    cls = models.CharField(choices=CLASS_CHOICE   ,max_length=50)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12)
    img = models.ImageField(upload_to="pro_img")

    def __str__(self):
        return str(self.id)


DEP_CHOICE = (
    ('Commerce', 'Commerce'),
    ('Computer Science', 'Computer Science'),
    ('Science', 'Science'),
    ('Arts', 'Arts'),
)

class LectureProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    department = models.CharField(choices=DEP_CHOICE, max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12)
    img = models.ImageField(upload_to="lec_img")

    def __str__(self):
        return str(self.full_name)
    

class Assignments(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecture = models.ForeignKey(LectureProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    document = models.FileField(upload_to="assignments", null=True, blank=True) 
    date = models.DateTimeField(auto_now_add=True)
    valued = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
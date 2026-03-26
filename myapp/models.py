from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Hier ist Model-Teil, da gibt es alle attributes fur Datenbankmanagment in dieser Django-Projekt.

class Branche(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Branche"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class Person(models.Model):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="person"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    branch = models.ForeignKey(Branche, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to="teachers/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"



# --------------------
# Student (student-only data)
# -------------------- 

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student"
    )
    address = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    grade_level = models.PositiveSmallIntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="students/", blank=True, null=True)

    def __str__(self):
        return self.user.username


# Lesson
class Lesson(models.Model):
    name = models.CharField(max_length=200)
    branch = models.ForeignKey(Branche, on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ManyToManyField(User, related_name="lessons", blank=True)

    def __str__(self):
        return self.name


# Enrollment
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student} - {self.lesson}"



# Grade
class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="grades")
    value = models.DecimalField(max_digits=5, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    given_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="given_grades")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.lesson}: {self.value}"

class Announcement(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.text
# Kalender    
class Event(models.Model):
    title = models.CharField(max_length=200)
    anfang = models.DateTimeField()
    ende = models.DateTimeField(null=True, blank=True)
    audience = models.CharField(
        choices=[("teacher","Teacher"),("student","Student"),("both","Both")],
        max_length=10
    )
class Kategorie(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.TextField(blank=True)
    gestaltet_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    kategorie = models.ForeignKey(Kategorie,on_delete=models.CASCADE,related_name="posts",null=False,blank=False)
    content = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def comment_count(self):
        return self.comments.count()

    def like_count(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    commentcontent = models.CharField(max_length=200)
    commentauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commentauthor.username} - {self.commentcontent[:20]}"

    class Meta:
        ordering = ["-submitted_at"]


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"



# Lunch

class Lunch(models.Model):
    lunchname = models.CharField(max_length=200)
    preis = models.DecimalField(max_digits=7, decimal_places=2)
    inhalte = models.CharField(max_length=200)
    allergiewarn = models.BooleanField()
    date = models.DateField()
# quiz
class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,null=True,blank=True, related_name="quiz")
    frage = models.CharField(max_length=200,null=True)
    antwort1= models.CharField(max_length=100,null=True)
    antwort2= models.CharField(max_length=100,null=True)
    antwort3= models.CharField(max_length=100,null=True)
    antwort4= models.CharField(max_length=100,null=True)
    richtigeantwort=models.CharField(max_length=100,null=True)      
     
    def __str__(self):
        return self.frage
    
class Quiz_Sammlung(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)   # quiz title
    questions = models.JSONField()             # json

    def __str__(self):
        return f"{self.title} ({self.lesson.name})"
    
class Quiz_Versuch(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="versuche")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_versuche")
    angefangen_at = models.DateTimeField(auto_now_add=True)
    beendet_at = models.DateTimeField(null=True, blank=True)
    ergebniss = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.frage} - {self.ergebniss}"
#material    
class File_Lernmaterial(models.Model):
        lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name="lernmaterials")
        title = models.CharField(max_length=200)
        file= models.FileField(upload_to=('learnmaterials/'))
        hochgeladen_um =models.DateTimeField(auto_now=True,blank=True)
        description = models.TextField(blank=True, null=True)
#news
class News(models.Model):
    titel = models.CharField(max_length=200)
    kurz_text = models.TextField()
    voll_text = models.TextField()
    bild = models.ImageField(upload_to="news/")
    kategorie = models.CharField(max_length=50)
    erstellt_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titel

class Schoolbilder(models.Model):
    bild= models.ImageField(upload_to="bilder/")
    titel =models.CharField(max_length=100)

    def __str__(self):
        return self.titel 
#karriere    
class Karriere(models.Model):
    jobtitel= models.CharField(max_length=100,blank=False)
    jobbeschreibung= models.CharField(max_length=1000)
    erstellt_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.jobtitel
#ai intergration
class Chat_ai(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message_ai(models.Model):
    chat = models.ForeignKey(Chat_ai, related_name="messages", on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # user / model
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
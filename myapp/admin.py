from django.contrib import admin
from .models import (
    Branche,
    Person,
    Student,
    Lesson,
    Enrollment,
    Grade,
    Announcement,
    Event,
    Quiz,
    Lunch,
    Quiz_Sammlung,
    File_Lernmaterial,
    News,
    Kategorie,
    Schoolbilder,
    Karriere
)

@admin.register(Branche)
class BrancheAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "branch")
    list_filter = ("role", "branch")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "grade_level")
    search_fields = ("user__username",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "branch")
    filter_horizontal = ("teachers",)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "enrolled_at")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "value", "given_by", "created_at")

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("text", "date")

@admin.register(Lunch)
class LunchAdmin(admin.ModelAdmin):
    list_display = ("lunchname", "preis","inhalte","allergiewarn")    


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title","anfang","ende","audience")

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("frage", "richtigeantwort")
  
@admin.register(Quiz_Sammlung)
class Quiz_SammlungAdmin(admin.ModelAdmin):
    list_display =["lesson","title"]
@admin.register(File_Lernmaterial)
class LernMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "hochgeladen_um")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("titel", "kategorie", "erstellt_at")
    search_fields = ("titel", "kurz_text")
    list_filter = ("kategorie", "erstellt_at")
    ordering = ("-erstellt_at",)

@admin.register(Kategorie)
class KategorieAdmin(admin.ModelAdmin):
    list_display = ("name","beschreibung","gestaltet_at")
    search_fields = ("name","beschreibung")

@admin.register(Schoolbilder)
class SchoolbilderAdmin(admin.ModelAdmin):
    list_display=("bild","titel")
   
@admin.register(Karriere)
class KarreireAdmin(admin.ModelAdmin):
    list_display=("jobtitel","jobbeschreibung","erstellt_at")
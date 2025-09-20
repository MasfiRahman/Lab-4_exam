from django.contrib import admin
from .models import Student, Instructor, Course, Enrollment


# Inline for Enrollment inside Course
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "department", "enrollment_date")
    search_fields = ("name",)
    list_filter = ("department",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "department", "hire_date", "course_count")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_code", "title", "credits", "instructor", "enrolled_students_count")
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrollment_date", "grade")
    list_filter = ("course", "grade")
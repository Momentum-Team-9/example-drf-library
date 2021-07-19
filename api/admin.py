from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Book, BookRecord, User

admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(BookRecord)

from django.contrib import admin
from JobPortalApp.models import *

# Register your models here.
admin.site.register([
  CustomUserModel,
  RecruiterProfileModel,
  SeekerProfileModel,
  CategoryModel,
  JobPostModel,
  ApplyJobModel,
])
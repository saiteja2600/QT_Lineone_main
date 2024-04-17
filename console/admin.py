from django.contrib import admin

from .models import *


class RegisterModelAdmin(admin.ModelAdmin):
    list_display = ('crn', 'full_name', 'email_id', 'phone_number', 'pin')
    search_fields = ('crn', 'full_name', 'email_id', 'phone_number')  
    readonly_fields = ('crn',)
    exclude = ('otp',)



admin.site.register(Register_model, RegisterModelAdmin)


# Training type 

class TrainingTypeAdmin(admin.ModelAdmin):
  list_display = ('TrainingTypeName', 'status')
  list_filter = ('TrainingTypeName', 'status')
  
  class Meta:
    model = TrainingType


admin.site.register(TrainingType, TrainingTypeAdmin)


class CourseAdmin(admin.ModelAdmin):
  list_display = ('course_name', 'status')
  list_filter = ('course_name', 'status')
  
  class Meta:
    model = Course


admin.site.register(Course, CourseAdmin)

class SpecializationAdmin(admin.ModelAdmin):
  list_display = ('specilalization_name', 'status')
  list_filter = ('specilalization_name', 'status')
  
  class Meta:
    model = Specialization


admin.site.register(Specialization, SpecializationAdmin)


class RegulationsAdmin(admin.ModelAdmin):
  list_display = ('batch_number', 'status')
  list_filter = ('batch_number', 'status')
  
  class Meta:
    model = Regulations


admin.site.register(Regulations, RegulationsAdmin)

class ComplaintsAdmin(admin.ModelAdmin):
  list_display = ('complaint_name', 'status')
  list_filter = ('complaint_name', 'status')
  
  class Meta:
    model = Complaints


admin.site.register(Complaints, ComplaintsAdmin)



class CourseManageAdmin(admin.ModelAdmin):
  list_display=('course_title','course_name','teaching_faculty')
  list_filter=('course_title','course_name','teaching_faculty')
   
  class Meta:
    model= CourseManage
admin.site.register(CourseManage,CourseManageAdmin)



class JobroleAdmin(admin.ModelAdmin):
  list_display=('jobrole_name','status')
  list_filter=('jobrole_name','status')
   
  class Meta:
    model= Jobrole
admin.site.register(Jobrole,JobroleAdmin)




# employee list

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('Employee_id', 'first_name', 'last_name', 'personal_number', 'status')
    list_filter = ('status', 'department_name', 'designation_name')
    search_fields = ('Employee_id', 'first_name', 'last_name', 'personal_number')

admin.site.register(Employee_model, EmployeeAdmin)
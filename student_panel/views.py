from django.shortcuts import render
def base(request):
    return render(request,'base.html')
def dash(request):
    return render(request,'dashbord.html')
def student_profile(request):
    return render(request,'student_profile.html')
def student_id(request):
    return render(request,'id.html')
def my_job(request):
    return render(request,'Myjob.html')
def project(request):
    return render(request,'profile_project.html')
def certification(request):
    return render(request,'profile_certification.html')
def student_login(request):
    return render(request,'student_login.html')
def reset_paasword(request):
    return render(request,'reset_password.html')
def internship(request):
    return render(request, 'internship.html')


def mycourse1(request):
    return render(request,"my_course1.html")
def mycourses(request):
    return render(request,"my_courses.html")
def my_course_As1(request):
    return render(request,"my_course_As1.html")
def my_course_As2(request):
    return render(request,"my_course_As2.html")
def my_course_video1(request):
    return render(request,"my_course_video1.html")
def Test_card(request):
    return render(request,"Test_card.html")
def matched_jobs(request):
    return render(request,'matched_jobs.html')

def applied_jobs(request):
    return render(request,'applied_jobs.html')

def qualified_jobs(s):
    return render(s,'qualified_jobs.html')

def job_details(s):
    return render(s,'job_details.html')
# Create your views here.
def student_attendance(request):
    return render(request,'student_attendance.html')

def calendar(request):
    return render(request,'calendar.html')
def CERTIFICATE(request):
    pass
    return render(request, 'certificates.html')
def payments(request):
    return render(request,'payments.html')
def Invoice(request):
    return render(request,'invoice.html')

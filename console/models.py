from django.db import models
from django.contrib.auth.models import AbstractUser
# from .manager import EmailAuthBackend
from datetime import datetime
from django.core.files import File
from PIL import Image, ImageDraw
from io import BytesIO
import random
import qrcode
from django.urls import reverse
from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.timezone import now



class Register_model(models.Model):
    crn = models.CharField(max_length=100, null=True, unique=True, editable=False)
    company_name = models.CharField(max_length=100)
    company_short_name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=255, null=True)
    email_id = models.EmailField( null=True)
    phone_number = models.CharField(max_length=10, null=True)
    pin = models.IntegerField(null=True)
    password = models.CharField(max_length=255, null=True)
    otp = models.CharField(max_length=6, null=True)
    terms_and_conditions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.crn}"

    def save(self, *args, **kwargs):
        if not self.crn:
            self.crn = self.generate_crn()
        super().save(*args, **kwargs)

    def generate_crn(self):
        prefix = f'{self.company_short_name}'
        today = datetime.now().date()
        year = today.year % 100
        month = today.month
        day = today.day
        last_crn = Register_model.objects.filter(crn__startswith=f'{prefix}{day:02d}{month:02d}{year:02d}').order_by('-id').first()
        if last_crn:
            last_number = int(last_crn.crn[-3:]) + 1
        else:
            last_number = 1
        return f'{prefix}{day:02d}{month:02d}{year:02d}{last_number:03d}'

    def __str__(self):
        return f"{self.crn}"

       


# department
class Department(models.Model):
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='departments')
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'))
    department_name=models.CharField(max_length=100)
    status = models.CharField(choices=choice_status,max_length=100, default='Active')
    def __str__(self) -> str:
        return self.department_name
class Department_import(models.Model):
    department_name=models.CharField(max_length=100)



# Designations
class Designation(models.Model):
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='designations')
    choice_status =(
        ('Active','Active'),
        ('Deactive','Deactive'),
    )
    department_name=models.ForeignKey(Department, on_delete=models.CASCADE)
    designation_name=models.CharField(max_length=100)
    status = models.CharField(choices=choice_status,max_length=100, default='Active')
    def __str__(self):
        return self.designation_name


# Plans
class Plan(models.Model):
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'),
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='plans')
    plan_name = models.CharField(max_length=100)
    status = models.CharField(choices=choice_status, max_length=100, default='Active')

    def __str__(self):
        return self.plan_name

    


# Training Type
class TrainingType(models.Model):
    status_Choices = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'),
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='training_types')
    TrainingTypeName = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=status_Choices, default='Active')

    def __str__(self):
        return self.TrainingTypeName
    

    

# Training type import
class Traning_type_import_form(models.Model):
  training_type_import=models.CharField(max_length=100)  

# Courses
class Course(models.Model):
    choice_status =(
        ('Active','Active'),
        ('Deactive','Deactive'),
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='courses')
    course_name=models.CharField(max_length=100)
    status = models.CharField(choices=choice_status,max_length=100, default='Active')
    def __str__(self):
        return self.course_name
class Course_import(models.Model):
    course_name=models.CharField(max_length=100)




# Specialization
class Specialization(models.Model):
    choice_status =(
        ('Active','Active'),
        ('Deactive','Deactive'),
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='specializations')
    course_name=models.ForeignKey(Course,on_delete=models.CASCADE)
    specilalization_name=models.CharField(max_length=100)
    status = models.CharField(choices=choice_status,max_length=100, default='Active')
    def __str__(self):
        return self.specilalization_name

class Specialization_import(models.Model):
    specialization_name=models.CharField(max_length=100)
    course_name=models.CharField(max_length=100)
    status=models.CharField(max_length=100)





# regulations
class Regulations(models.Model):
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='regulations')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    spec_id = models.ForeignKey(
        Specialization, on_delete=models.CASCADE,null=False)
    batch_number = models.CharField(max_length=100)
    
    status = models.CharField(
        max_length=100, choices=choice_status, default='Active')


    def __str__(self):
        return self.batch_number    


# branch 
class BranchModel(models.Model):
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=100)
    branch_qr = models.ImageField(upload_to='qrcode', null=False, blank=True)
    status = models.CharField(max_length=100, choices=choice_status, default='Active')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_qr_code()

    def generate_qr_code(self):
        if not self.id:
            return

        qr_url = f"http://192.168.219.156:8080/inquiry_form/{self.id}/{self.crn_number.crn}"
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_image = buffer.getvalue()
        self.branch_qr.save(f'branch_qr{self.crn_number}_{self.branch_name}_{random.randint(0, 9999)}.png', ContentFile(qr_image), save=False)
        super().save()

    def __str__(self):
        return self.branch_name
    
class Branchimportmodel(models.Model):
    branch_name_import=models.CharField(max_length=100)
    branch_qr_import=models.CharField(max_length=100)




class Demo(models.Model):
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='demo')
    choice_status = (
        ('Active','Active'),
        ('Deactive','Deactive'))
    demotitle=models.CharField(max_length=100)
    demosessiontype=models.ForeignKey(TrainingType,on_delete=models.CASCADE) 
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    specialization=models.ForeignKey(Specialization,on_delete=models.CASCADE)
    faculty=models.CharField(max_length=100,default='null')
    courseplan=models.ForeignKey(Plan,on_delete=models.CASCADE)
    branchlocation=models.ForeignKey(BranchModel,on_delete=models.CASCADE)
    batchno=models.ForeignKey(Regulations,on_delete=models.CASCADE)
    meetinglink=models.CharField(max_length=100)
    meetingid=models.CharField(max_length=100)
    passcode=models.CharField(max_length=100)
    datestartat=models.DateTimeField()
    dateendat=models.DateTimeField()
    demoimage=models.ImageField(upload_to='demo_image',null=True,default=True)
    demobannerimage=models.ImageField(upload_to='demo_banner',null=True,default=True)
    demodescription=models.TextField(max_length=100)
    status = models.CharField(max_length=100, choices=choice_status,default='Active')










# complaint 
class Complaints(models.Model):
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='complaints')
    complaint_name = models.CharField(max_length=100,unique=True)
    complaint_subject = models.CharField(max_length=100)
    complaint_discription = models.TextField()
    status = models.CharField(
        max_length=100, choices=choice_status, default='Active')
   

    def __str__(self):
        return self.complaint_name
class complaint_import_model(models.Model):
    complaint_import=models.CharField(max_length=100)
    complaint_subject = models.CharField(max_length=100)
    complaint_discription = models.TextField()




# calender
class CalenderModel(models.Model):
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='calenders')
    title = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    category=models.CharField(max_length=100)
    branch=models.ForeignKey(BranchModel,on_delete=models.CASCADE)
    message=models.TextField()
    status = models.CharField(
        max_length=100, choices=choice_status, default='Active')
   
    def __str__(self):
        return self.title    



# calender import
class Calender_import_model(models.Model):
    
    title = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    category=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    message=models.TextField()
    
    def __str__(self):
        return self.title    
    



# forum category
class Forumcategories_model(models.Model):
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='forumcategories')
    forum_category = models.CharField(max_length=40,unique=True)
    status = models.CharField(
        max_length=100, choices=choice_status, default='Active')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.forum_category

class Forumcategories_model_import(models.Model):
    forum_category_import=models.CharField(max_length=100)
    date_update=models.DateField(auto_now_add=True)
 


# prospect type


class ProspectType_model(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive')
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='prospect_types')
    prospect_type = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.prospect_type}"
class prospect_type_import_model(models.Model):
    prospect_type_import=models.CharField(max_length=100)
    date_update=models.DateField(auto_now_add=True)





# purpose of visit


class Purpose_of_visit_model(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive')
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='purpose')
    purpose = models.CharField(max_length=250,unique=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.purpose}"
    
class purpose_import_model(models.Model):
    purpose_type_import=models.CharField(max_length=100)
    date_update=models.DateField(auto_now_add=True)




class vendorModel(models.Model):
    choice_status = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='vendors')
    vendor_name = models.CharField(max_length=100,unique=True)
    status = models.CharField(
        max_length=100, choices=choice_status, default='Active')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.vendor_name}"
class vendor_import_model(models.Model):
    vendor_import=models.CharField(max_length=100)
    date_update=models.DateField(auto_now_add=True)



class EmployeeType_model(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive')
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='employee_types')
    employee_type = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.employee_type}"
    
class employee_type_import_model(models.Model):
    employee_type_import=models.CharField(max_length=100)
    date_update=models.DateField(auto_now_add=True)



class upipayments(models.Model):
    choice_status = (
        ('Active','Active'),
        ('Deactive','Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='upi')
    upipayments_name=models.CharField(max_length=100)
    mobilenumber=models.CharField(max_length=100)
    upiid=models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=choice_status, default='Active')

    def __str__(self):
        return self.upipayments_name
    


class UPIPayments_import(models.Model):
    upipayments_name=models.CharField(max_length=100)
    mobilenumber=models.CharField(max_length=100)
    upiid=models.CharField(max_length=100)




class netbanking(models.Model):
    choice_status = (
        ('Active','Active'),
        ('Deactive','Deactive'))
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='net_banking')
    netbanking_name=models.CharField(max_length=100)
    accountnumber=models.CharField(max_length=100) 
    ifscode=models.CharField(max_length=100)
    accounttype=models.CharField(max_length=100,default='null')
    bankname=models.CharField(max_length=100)
    branchname=models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=choice_status,default='Active')    


class NETBanking_import(models.Model):
    netbanking_name=models.CharField(max_length=100)
    accountnumber=models.CharField(max_length=100) 
    ifscode=models.CharField(max_length=100)
    accounttype=models.CharField(max_length=100,default='null')
    bankname=models.CharField(max_length=100)
    branchname=models.CharField(max_length=100)


class Batchtype(models.Model):
    choice_status = (
        ('Active','Active'),
        ('Deactive','Deactive'),)
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='batch_type')
    batchtype_name=models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=choice_status, default='Active')
    def __str__(self) ->str:
        return self.batchtype_name
class BatchType_import(models.Model):
    batchtype_name=models.CharField(max_length=100)






class LeadModel(models.Model):
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='leads')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=11)
    email = models.EmailField()
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)

    branch_name = models.ForeignKey(BranchModel, on_delete=models.CASCADE, editable=False)
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE)
    lead_type = models.ForeignKey(ProspectType_model, on_delete=models.CASCADE)

    token_id = models.CharField(max_length=100, unique=True, editable=False)
    token_generated_date = models.DateField(null=True, blank=True)
    prospect_taken = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        today = timezone.now()
        token_prefix = f"{self.crn_number.company_short_name}{today.day:02d}{today.month:02d}{today.year % 100:02d}"
        last_lead = LeadModel.objects.order_by('-id').first()
        if last_lead:
            last_token_id = last_lead.token_id
            last_count = int(last_token_id[len(token_prefix):])
            new_count = last_count + 1
            self.token_id = f"{token_prefix}{new_count:03d}"
        else:
            self.token_id = f"{token_prefix}001"
        self.token_generated_date = timezone.now().date()
        super().save(*args, **kwargs)



class Leadstage(models.Model):

    choice_status = (('Active','Active'),
        ('Deactive','Deactive'),)
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='leadstages')
    Leadstage_name=models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=choice_status, default='Active')
    def __str__(self) ->str:
        return self.Leadstage_name 

class Leadstage_import(models.Model):
    Leadstage_name=models.CharField(max_length=100)        




class Employee_model(models.Model):
    choice_status=(
        ('Active','Active'),
        ('Deactive','Deactive'),
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='employee')
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    personal_number= models.CharField(max_length=100)
    alternative_number= models.CharField(max_length=100,null=True,blank=True)
    personal_email= models.EmailField()
    professional_email= models.EmailField(null=True,blank=True)
    blood_group= models.CharField(max_length=100,null=True,blank=True)
    gender= models.CharField(max_length=100)
    date_of_birth= models.CharField(max_length=100)
    nationality= models.CharField(max_length=100,null=True,blank=True)
    religion= models.CharField(max_length=100,null=True,blank=True)
    caste= models.CharField(max_length=100,null=True,blank=True)
    Employee_id= models.CharField(max_length=100,unique=True,editable=False)
    employee_type=models.ForeignKey(EmployeeType_model,on_delete=models.CASCADE,null=True)
    department_name=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    designation_name=models.ForeignKey(Designation,on_delete=models.CASCADE,null=True)
    branch=models.ForeignKey(BranchModel,on_delete=models.CASCADE)
    profile_image= models.ImageField(upload_to='profile_image',null=True,blank=True)
    country= models.CharField(max_length=100,null=True,blank=True)
    state= models.CharField(max_length=100,null=True,blank=True)
    city= models.CharField(max_length=100,null=True,blank=True)
    pincode= models.CharField(max_length=100,null=True,blank=True)
    address= models.CharField(max_length=255,null=True,blank=True)
    aadhar_card= models.CharField(max_length=100,null=True,blank=True)
    pan_card= models.CharField(max_length=100,null=True,blank=True)
    aadhar_card_pdf= models.FileField(upload_to='aadhar_card_pdf',null=True,blank=True)
    pan_card_pdf= models.FileField(upload_to='pan_card_pdf',default=None,blank=True)
    status = models.CharField(max_length=20, choices=choice_status, default='Active')
    def save(self, *args, **kwargs):
        if not self.Employee_id:
            last_employee = Employee_model.objects.order_by('-Employee_id').first()
            if last_employee and last_employee.Employee_id:
                last_id = int(last_employee.Employee_id[3:])
                new_id = last_id + 1
                self.Employee_id = f"EMP{new_id}"
            else:
                self.Employee_id = f"EMP100"
        super().save(*args, **kwargs)

    def __str__(self) ->str:
        return self.first_name 



class CourseManage(models.Model):
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='course_manage')
    course_title=models.CharField(max_length=100)
    course_plan=models.ForeignKey(Plan, on_delete=models.CASCADE)
    course_name=models.ForeignKey(Course, on_delete=models.CASCADE)
    specialization=models.ForeignKey(Specialization,on_delete=models.CASCADE)
    teaching_faculty=models.ForeignKey(Employee_model,on_delete=models.CASCADE)
    batch_type=models.ForeignKey(Batchtype,on_delete=models.CASCADE)
    duration=models.CharField(max_length=50)
    course_fee=models.DecimalField(max_digits=8,decimal_places=2)
    discount=models.DecimalField(max_digits=6,decimal_places=0)
    final_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    branch=models.ForeignKey(BranchModel,on_delete=models.CASCADE)
    curriculum=models.FileField(upload_to='Curriculum',null=True,blank=True)
    course_image=models.ImageField(upload_to='course_image',null=True,blank=True)
    course_banner=models.ImageField(upload_to='course_banner',null=True,blank=True)
    hardware=models.CharField(max_length=100)
    software=models.CharField(max_length=100)
    short_description=models.TextField()
    long_description=models.TextField()
    def __str__(self) ->str:
        return self.course_title
    

class CourseManage_import(models.Model):
    course_title=models.CharField(max_length=100)
    course_plan=models.CharField(max_length=100)
    course_name=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100)
    teaching_faculty=models.CharField(max_length=100)
    batch_type=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    course_fee=models.DecimalField(max_digits=6,decimal_places=0)
    discount=models.DecimalField(max_digits=6,decimal_places=0)
    final_price=models.DecimalField(max_digits=6,decimal_places=0,default=0)
    branch=models.CharField(max_length=100)
    curriculum=models.FileField(default='null.pdf')
    course_image=models.ImageField(default='null.png')
    course_banner=models.ImageField(default='null.png')
    hardware=models.CharField(max_length=100)
    software=models.CharField(max_length=100)
    short_description=models.TextField()
    long_description=models.TextField()







                



class Jobtype(models.Model):
    choice_status = (('Active','Active'),
        ('Deactive','Deactive'),)
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='job_types')
    JobType_name=models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=choice_status, default='Active')

    def __str__(self) ->str:
        return self.JobType_name 

class Jobtype_import(models.Model):
    JobType_name=models.CharField(max_length=100)



class Job_Category(models.Model):
    choice_status = (('Active','Active'),
        ('Deactive','Deactive'),)
    crn= models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='job_category')
    Jobcategory_name=models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=choice_status, default='Active')

    def __str__(self) ->str:
        return self.Jobcategory_name 

class Job_Category_import(models.Model):
    Category_name=models.CharField(max_length=100)





class Jobrole(models.Model):
    choice_status=(
        ('Active','Active'),
        ('Deactive','Deactive'),
    )
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='jobrole')
    jobrole_name= models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=choice_status, default='Active')






class Qualification(models.Model):
    choice_status = (('Active','Active'),
        ('Deactive','Deactive'),)
    crn_number=models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='qualifications')
    qualification_name=models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=20, choices=choice_status, default='Active')
    def __str__(self):
        return self.qualification_name 




class Lead_generation(models.Model):
    # Assuming the Register_model, Course, BranchModel, and TrainingType are defined elsewhere
    # Basic Contact Information
    crn_number = models.ForeignKey(Register_model, on_delete=models.CASCADE, related_name='Register_model')
    token_id = models.CharField(max_length=255)
    token_generated_date = models.DateField(default=now)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    lead_source = models.CharField(max_length=255, null=True, blank=True)
    lead_stage = models.CharField(max_length=255, null=True, blank=True)
    # Relationships
    course_interested_in = models.ForeignKey(Course, on_delete=models.CASCADE)  # Assuming Course is a model
    Training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE)  # Assuming TrainingType is a model
    branch_name = models.ForeignKey(BranchModel, on_delete=models.CASCADE)  # Assuming BranchModel is a model
    enquiry_taken_by = models.ForeignKey(Register_model, on_delete=models.CASCADE)  # Assuming Register_model is a model

    # Lead process
    LEAD_POSITION = (
        ('LEAD', 'Lead'),
        ('ASSIGNED_DEMO', 'AssignedDemo'),
        ('ATTENDED_DEMO', 'AttendedDemo'),
        ('REQUEST_DISCOUNT', 'RequestDiscount'),
        ('OPPORTUNITY', 'Opportunity'),
        ('ADMITTED', 'Admitted'),
        ('SPAM', 'Spam'),
    )
    lead_position = models.CharField(max_length=100, choices=LEAD_POSITION)
    lead_type = models.CharField(max_length=255, null=True, blank=True)

    has_attended_demo = models.BooleanField(default=False)
    request_acceptance = models.BooleanField(default=False)

    # Course Information
    plan = models.CharField(max_length=255, null=True, blank=True)
    course_faculty = models.CharField(max_length=255, null=True, blank=True)
    course_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_fee = models.IntegerField(null=True, blank=True)
    Final_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remaining_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    demo_date = models.DateField(null=True, blank=True)
    batch_no = models.CharField(max_length=255, null=True, blank=True)
    paymentMode = models.CharField(max_length=255, null=True, blank=True)
    paymentid = models.CharField(max_length=255, null=True, blank=True)
    transactionid = models.CharField(max_length=255, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)

    # For description
    lead_description = models.TextField(null=True, blank=True)
    mql_description = models.TextField(null=True, blank=True)
    sql_description = models.TextField(null=True, blank=True)
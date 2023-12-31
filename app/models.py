from django.db import models
from django.contrib.auth.hashers import make_password

class Admin_Login(models.Model):
    Username = models.CharField(max_length=20)
    Password = models.CharField(max_length=20) 
    
    class Meta:  
        # managed = False
        db_table = "admin_Login"
        
# Create your models here.

class Addemployee(models.Model):
    Name = models.CharField(max_length=200)
    Contact = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    D_O_B = models.DateField(blank = True,null=True)
    Date_of_join = models.DateField(blank = True,null=True)
    department = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
    Reporting_Dept = models.CharField(max_length=200)
    Email = models.EmailField(max_length=70,blank=True,unique=True) 
    User_name = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)
    Confirm_Password = models.CharField(max_length=200)
    Emp_ID = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='images/')
    Emp_status = models.IntegerField(default=0,blank = True,null=True)
    
        
    Total_Paid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Total_Sick_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Total_HalfDay_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Total_Unpaid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    
    Pending_Paid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Pending_Sick_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Pending_HalfDay_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Pending_Unpaid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    
    class Meta:  
        db_table = "add_employee" 
         
    @staticmethod
    def get_customer_by_email(User_name):
        try:
            return Addemployee.objects.get(User_name=User_name)
        except:
            return False

    def isExists(self):
        if Addemployee.objects.filter(User_name = self.User_name):
            return True

        return  False
        
        
class Leave_App(models.Model):
    
    Category = models.CharField(max_length=200)          
    From = models.CharField(max_length=200) 
    to = models.CharField(max_length=200 )
    leavedayCategory_From = models.CharField(max_length=200)  
    leavedayCategory_to = models.CharField(max_length=200)  
    Reason = models.CharField(max_length=250)
    Emp_ID = models.CharField(max_length=200,blank = True,null=True) 
    Leave_count_Category = models.CharField(max_length=2,blank = True,null=True) 
    leave_status = models.IntegerField(default=0,blank = True,null=True)
    comments = models.CharField(max_length=500,blank = True,null=True)
    

    
    
    
    class Meta:  
        db_table = "leave"  


    


        
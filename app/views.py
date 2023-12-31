from django.shortcuts import render, redirect ,HttpResponse ,  HttpResponseRedirect
from django.contrib import messages
from .models import Addemployee  
from .forms import AddemployeeForm 
from .models import Admin_Login  
from .forms import Admin_LoginForm 
from .models import Leave_App  
from .forms import Leave_AppForm 
from django.conf import settings
from django.core.mail import send_mail
from .filters import ConsumerFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime
import os 
from django.db import connection
from django.db.models import Count 
from django.urls import reverse


def homePage(request):
    return render(request,"homePage.html")


def adminLogin(request):   
    if request.method == 'POST':
        form = Admin_LoginForm(request.POST)  
        Username = request.POST['Username']
        Password = request.POST['Password']
         
        try:
            salary = Admin_Login.objects.get(Username = Username,Password=Password)
            request.session['Username'] = Username
        except Admin_Login.DoesNotExist:
            salary = None


        if salary is not None:
            return redirect('/adminDashboard')                                           
        else:
            messages.error(request,"Invalid Username or Password")
            return render(request,"adminLogin.html")

    return render(request,"adminLogin.html")

def adminDashboard(request):
    # Username = request.session['Username']
    # print(Username)
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            admin_reg = Admin_Login.objects.get(Username=Username)
            print(admin_reg)
            
     
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            print(total_emp)
            
            total_Leave = Leave_App.objects.count()
            print(total_Leave)
            
            dic ={
                'admin_reg':admin_reg,
                'total_emp':total_emp,
                'total_Leave':total_Leave
            }
            
            return render(request,'adminDashboard.html',dic)   
    return render(request,"adminDashboard.html")

    
def addEmployee(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            admin_reg = Admin_Login.objects.get(Username=Username)
            print(admin_reg)
            
            return render(request,'addEmployee.html',{'admin_reg':admin_reg})
        
        
    if request.method == "POST":  
        form = AddemployeeForm(request.POST,request.FILES)  
        if form.is_valid():
                Emp_ID = form.cleaned_data.get('Emp_ID')
                Name = form.cleaned_data.get('Name')
                User_name = form.cleaned_data.get('User_name')
                Contact = form.cleaned_data.get('Contact')
                Email = form.cleaned_data.get('Email')
                Designation = form.cleaned_data.get('Designation')
                D_O_B = form.cleaned_data.get('D_O_B')
                Date_of_join = form.cleaned_data.get('Date_of_join')
                Reporting_Dept = form.cleaned_data.get('Reporting_Dept')
                Password = form.cleaned_data.get('Password')
                Confirm_Password = form.cleaned_data.get('Confirm_Password')
                Image = form.cleaned_data.get('Image')
                Address = form.cleaned_data.get('Address')
                department = form.cleaned_data.get('department')
                subject ="Your Account has been created" 
                send_mail(subject, f'User_name:{User_name}\n\nPassword :{Password}\n\n', 'settings.EMAIL_HOST_USER', [Email],fail_silently=False) 
                
                form.save()
                return redirect('/adminDashboard') 
        
    else:
        form = AddemployeeForm()  
    return render(request,'addEmployee.html',{'form':form})


def edit(request): 
       
    employees = Addemployee.objects.all()  
    paginator = Paginator(employees,5)

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'edit.html', {'employees': employees})


def show_Emp_ID(request):
        Emp_ID = request.POST['Emp_ID'] 
        employee = Addemployee.objects.filter(Emp_ID=Emp_ID)
        return render(request, 'edit.html',{'employees' : employee})
   
        

def editEmployee(request,id):

    employee = Addemployee.objects.get(id=id)  
    return render(request,'editEmployee.html', {'employee':employee}) 
    # return render(request,"editEmployee.html")

def update(request, id):  
   
    employee = Addemployee.objects.get(id=id)  
    if len(employee.Image) > 0:
        os.remove(employee.Image.path)
    form = AddemployeeForm(request.POST, instance = employee)  
    if form.is_valid(): 
        
        form.save()  
        return redirect("/edit")  
    # else:
        # print(form.errors) 
    return render(request, 'editEmployee.html', {'employee': employee})  


def employees(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            admin_reg = Admin_Login.objects.get(Username=Username)
            print(admin_reg)
            
            return render(request,'employees.html',{'admin_reg':admin_reg})
        
    return render(request,"employees.html")



def leaveApplicationDetails(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
        
            
            leaves = Leave_App.objects.raw("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."department" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID" ORDER BY leave."leave_status" ASC """)


            return render(request,'leaveApplicationDetails.html',{'leaves':leaves,'Username':Username})
        
    return render(request,"leaveApplicationDetails.html")


def removeEmployees(request):
    employees = Addemployee.objects.all()  
    paginator = Paginator(employees,5)

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
        
    return render(request,"removeEmployees.html",{'employees':employees})

def remove_Emp_ID(request):
    Emp_ID = request.POST['Emp_ID']
    employee = Addemployee.objects.filter(Emp_ID=Emp_ID)
    return render(request, 'removeEmployees.html',{'employees' : employee})

def destroy(request, id):
          
    employee = Addemployee.objects.get(id=id)  
    if len(employee.Image) > 0:
        os.remove(employee.Image.path)
    employee.delete()  
    return redirect("/removeEmployees") 



def reviewLeaveApplication(request,Emp_ID,id):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            
            dic = {
                'Emp_ID' : Emp_ID,
                'id':id
            }
            leaves = Leave_App.objects.raw("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."Contact",add_Employee."Address",add_Employee."D_O_B",add_Employee."Date_of_join",add_Employee."department",add_Employee."Designation",add_Employee."Reporting_Dept",add_Employee."Email",add_Employee."User_name",add_Employee."Password",add_Employee."Confirm_Password",add_Employee."Emp_ID",add_Employee."Image" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID" where leave."Emp_ID" = %(Emp_ID)s and leave."id" = %(id)s """, dic)

           
            return render(request,'reviewLeaveApplication.html',{'leaves':leaves})
        
    return render(request,"reviewLeaveApplication.html")


def Approve_leave(request,Emp_ID,id):
    
    leave=Leave_App.objects.get(Emp_ID=Emp_ID,id=id)
    leave.leave_status=1
    leave.save()


    for leave_Paid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_Paid_Leave','Pending_Sick_Leave','Pending_HalfDay_Leave','Pending_Unpaid_Leave'):
        print(leave_Paid1)
        
        leave_Paid2 = list(leave_Paid1)
        pending_leave_Paid = [eval(i) for i in leave_Paid2]
        print(pending_leave_Paid)
        
      
    for Paid_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Paid Leave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        Paid_leave1 = list(Paid_leave_days)
        # print(Paid_leave1)  
        Paidleave_list = [eval(i) for i in Paid_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in Paidleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_Paid, Paidleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_Paid_Leave = sum[0]
        print(pending_Paid_Leave)
        
        
        Paid_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        Paid_leave.Pending_Paid_Leave= pending_Paid_Leave
        Paid_leave.save()
        print(Paid_leave)

# # ===============sick leave ===============================


 
    for leave_sick1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_Sick_Leave'):
        print(leave_sick1)
        
        leave_sick2 = list(leave_sick1)
        pending_leave_sick = [eval(i) for i in leave_sick2]
        print(pending_leave_sick)
        
      
    for sick_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Sick Leave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        sick_leave1 = list(sick_leave_days)
        # print(Paid_leave1)  
        sickleave_list = [eval(i) for i in sick_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in sickleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_sick, sickleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_sick_Leave = sum[0]
        print(pending_sick_Leave)
        
        
        sick_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        sick_leave.Pending_Sick_Leave= pending_sick_Leave
        sick_leave.save()
        print(sick_leave)
        
# ================================================= HalfDay_Leave ==============================================
        
    for leave_HalfDay1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_HalfDay_Leave'):
        print(leave_HalfDay1)
        
        leave_HalfDay2 = list(leave_HalfDay1)
        pending_leave_HalfDay = [eval(i) for i in leave_HalfDay2]
        print(pending_leave_HalfDay)
        
      
    for HalfDay_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Half DayLeave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        HalfDay_leave1 = list(HalfDay_leave_days)
        # print(Paid_leave1)  
        HalfDayleave_list = [eval(i) for i in HalfDay_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in HalfDayleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_HalfDay, HalfDayleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_HalfDay_Leave = sum[0]
        print(pending_HalfDay_Leave)
        
        
        HalfDay_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        HalfDay_leave.Pending_HalfDay_Leave= pending_HalfDay_Leave
        HalfDay_leave.save()
        print(HalfDay_leave)


# ================================================= HalfDay_Leave ==============================================
        
    for leave_Unpaid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_Unpaid_Leave'):
        print(leave_Unpaid1)
        
        leave_Unpaid2 = list(leave_Unpaid1)
        pending_leave_Unpaid = [eval(i) for i in leave_Unpaid2]
        print(pending_leave_Unpaid)
        
      
    for Unpaid_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Unpaid Leave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        Unpaid_leave1 = list(Unpaid_leave_days)
        # print(Paid_leave1)  
        Unpaidleave_list = [eval(i) for i in Unpaid_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in Unpaidleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_Unpaid, Unpaidleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_Unpaid_Leave = sum[0]
        print(pending_Unpaid_Leave)
        
        
        Unpaid_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        Unpaid_leave.Pending_Unpaid_Leave= pending_Unpaid_Leave
        Unpaid_leave.save()
        print(Unpaid_leave)
    
    return redirect("/leaveApplicationDetails")
    
        


    

def Reject_leave(request,Emp_ID,id):
    comments = request.POST.get('comments')
    print(comments)
    leave=Leave_App.objects.get(Emp_ID=Emp_ID,id=id)
    leave.leave_status=2
    leave.comments = comments
    leave.save()

    return redirect("/leaveApplicationDetails")
            

def deactive_emp(request,Emp_ID,id):
    emp=Addemployee.objects.get(Emp_ID=Emp_ID,id=id)
    emp.Emp_status=1
    emp.save()

    return redirect("/removeEmployees")


def active_emp(request,Emp_ID,id):
    emp=Addemployee.objects.get(Emp_ID=Emp_ID,id=id)
    emp.Emp_status=0
    emp.save()
    return redirect("/removeEmployees")


def adminlogout(request):
    try:
      del request.session['Username']
    except:
      pass
    return render(request,"adminLogin.html")


#=============================================================================================








def employeeLogin(request):
    if request.method == 'POST':
        form = AddemployeeForm(request.POST)  
        User_name = request.POST['User_name']
        Password = request.POST['Password']
         
        try:
            emp = Addemployee.objects.get(User_name = User_name,Password=Password)
            print(emp.Emp_status)
            request.session['User_name'] = User_name
            
            
            for employee in Addemployee.objects.all().filter(User_name=User_name).values_list('id','Name','Emp_ID'):
                request.session['id'] = employee[0]
                request.session['Name'] = employee[1]
                request.session['Emp_ID'] = employee[2]
                
                # print(employee[0],employee[1],employee[2])

                if emp.Emp_status is not 1:
                    return redirect('/sidebar')                                           
                else:
                    messages.error(request,"Your Account is Deactivate")
                    return render(request,"employeeLogin.html")

        except Addemployee.DoesNotExist:
            emp = None


        if emp is not None:
            return redirect('/sidebar')                                           
        else:
            messages.error(request,"Invalid Username or Password")
            return render(request,"employeeLogin.html")

    return render(request,"employeeLogin.html")


def sidebar(request):   
    Name = request.session['Name']
    Emp_ID = request.session['Emp_ID']
    Paid_leave = Leave_App.objects.filter(Emp_ID=Emp_ID,Category='Paid Leave').count()
    # print(Paid_leave)
    
    for leave_paid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_Paid_Leave','Pending_Unpaid_Leave'):
        print(leave_paid1)
        x_paid=0
        x_paid = list(leave_paid1)
        print(x_paid)
        paidleave = [eval(i) for i in x_paid]
        print(paidleave)
        total_Paid_leave = int(paidleave[0])-int(paidleave[1])
        print(total_Paid_leave)
        
    for leave_sick1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_Sick_Leave','Pending_Sick_Leave'):
        print(leave_sick1)
        x_sick = 0
        x_sick = list(leave_sick1)
        print(x_sick)
        sickleave = [eval(i) for i in x_sick]
        print(sickleave)
        total_Sick_leave = int(sickleave[0])-int(sickleave[1])
        print(total_Sick_leave)
        
        
        
    for leave_halfday1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_HalfDay_Leave','Pending_HalfDay_Leave'):
        print(leave_halfday1)
        x_halfday = 0
        x_halfday = list(leave_halfday1)
        print(x_halfday)
        halfdayleave = [eval(i) for i in x_halfday]
        print(halfdayleave)
        total_halfday_leave = int(halfdayleave[0])-int(halfdayleave[1])
        print(total_halfday_leave)
        
        
        
    for leave_Unpaid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_Unpaid_Leave','Pending_Unpaid_Leave'):
        print(leave_Unpaid1)
        x_Unpaid = 0
        x_Unpaid = list(leave_Unpaid1)
        print(x_Unpaid)
        Unpaidleave = [eval(i) for i in x_Unpaid]
        print(Unpaidleave)
        total_Unpaid_leave = int(Unpaidleave[0])-int(Unpaidleave[1])
        print(total_Unpaid_leave)
   
    
    
        
    dic ={
        'total_Paid_leave':total_Paid_leave,
        'total_Sick_leave':total_Sick_leave,
        'total_halfday_leave':total_halfday_leave,
        'total_Unpaid_leave':total_Unpaid_leave,
    }
        

    return render(request,"sidebar.html",dic)







def profileSetting(request):
    if request.session.has_key('Name'):
        if request.method == 'GET':
            Name = request.session['Name']
            emp_reg = Addemployee.objects.get(Name=Name)
            print(emp_reg)
            
            return render(request,'profileSetting.html',{'emp_reg':emp_reg})        
    return render(request,"profileSetting.html",{'Name':Name})


def leaveSection(request):
    Name = request.session['Name']
    return render(request,"leaveSection.html",{'Name':Name})


def leaveApplication(request):
    Name = request.session['Name']
            
    if request.method == "POST": 
        
        form = Leave_AppForm(request.POST)  
        print(form)
        if form.is_valid():
            Category = form.cleaned_data.get('Category')
            From = form.cleaned_data.get('From')
            to = form.cleaned_data.get('to')
            leavedayCategory_From = form.cleaned_data.get('leavedayCategory_From')
            leavedayCategory_to = form.cleaned_data.get('leavedayCategory_to')
            Reason = form.cleaned_data.get('Reason')
            Emp_ID = form.cleaned_data.get('Emp_ID')
            Leave_count_Category = form.cleaned_data.get('Leave_count_Category')
            print(Leave_count_Category)
            
           
            
            try:  
                form.save()  
                return redirect('/approvalStatus')  
                
            except:  
                print(form.errors)
                pass  
        
    else:
        
        form = Leave_AppForm()  
        
    con ={
        'form':form,
        'Name':Name,

        
    }
    return render(request,'leaveApplication.html',con)



def leaveBasket(request): 
  
    if request.session.has_key('Name'):
            Name = request.session['Name']
            Emp_ID = request.session['Emp_ID']
            emp_reg = Addemployee.objects.get(Name=Name,Emp_ID=Emp_ID)
            print(emp_reg)
            return render(request, 'leaveBasket.html',{'emp_reg' : emp_reg})   

    else:
    
        return render(request,"leaveBasket.html")
    
    
def approvalStatus(request):
    if request.session.has_key('Name'):
        if request.method == 'GET':
            Name = request.session['Name']
            Emp_ID = request.session['Emp_ID']
            for employee in Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('department'):
                
                department = employee[0]
                
            leave = Leave_App.objects.filter(Emp_ID=Emp_ID).order_by('leave_status').values()
            print(leave)
           
            con = {
                'leaves':leave,
                'Name':Name,
                'Emp_ID':Emp_ID,
                'department':department,
                
            }
            
            return render(request,'approvalStatus.html',con)
    
    return render(request,'approvalStatus.html')


def reviewEmployeeApplication(request,Emp_ID,id):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Name = request.session['Name']
            
            dic = {
                'Emp_ID' : Emp_ID,
                'id':id
            }
            leaves = Leave_App.objects.raw("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."Contact",add_Employee."Address",add_Employee."D_O_B",add_Employee."Date_of_join",add_Employee."department",add_Employee."Designation",add_Employee."Reporting_Dept",add_Employee."Email",add_Employee."User_name",add_Employee."Password",add_Employee."Confirm_Password",add_Employee."Emp_ID",add_Employee."Image" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID" where leave."Emp_ID" = %(Emp_ID)s and leave."id" = %(id)s """, dic)

           
            # cursor = connection.cursor()    
            # cursor.execute("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."Contact",add_Employee."Address",add_Employee."D_O_B",add_Employee."Date_of_join",add_Employee."department",add_Employee."Designation",add_Employee."Reporting_Dept",add_Employee."Email",add_Employee."User_name",add_Employee."Password",add_Employee."Confirm_Password",add_Employee."Emp_ID",add_Employee."Image" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID"  """ )
            # row = cursor.fetchall()
            # print(row)
           
            return render(request,'reviewEmployeeApplication.html',{'leaves':leaves})
        
    return render(request,"reviewEmployeeApplication.html")
 
    # if request.session.has_key('Name'):
    #     if request.method == 'GET':
    #         Name = request.session['Name']
    #         Emp_ID = request.session['Emp_ID']
    #         for employee in Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('department'):
    
    #              department = employee[0]
    #              print(department)
    #         for leave in Leave_App.objects.all().filter(Emp_ID=Emp_ID).values_list('Category','From','to','leavedayCategory_From','leavedayCategory_to','Reason','Emp_ID','Leave_count_Category'):
    #             From = leave[1]
    #             to = leave[2]
    #             print(From,to)
    #             print(leave)
    #         # leave = Leave_App.objects.get(Emp_ID=Emp_ID)
    #         # print(leave)
    #         From_date = str(From)
    #         From_date = datetime.strptime(From_date, '%Y-%m-%d')
    #         From_date = From_date.strftime("%d")
            
    #         # # print(From_date)

    #         to_date = str(to)
    #         to_date = datetime.strptime(to_date, '%Y-%m-%d')
    #         to_date = to_date.strftime("%d")
            
    #         # # print(to_date) 

    #         date = int(to_date) - int(From_date)
    #         # print(date)
        
    #         con = {
    #             'leave':leave,
    #             'Name':Name,                            
    #             'From' : From,
    #             'Emp_ID':Emp_ID,
    #             'department':department,
    #             'date':date,
                
    #         }
            
    #         return render(request,'approvalStatus.html',con)
    
    # return render(request,'approvalStatus.html')

def employeelogout(request):
    try:
      del request.session['Name']
    except:
      pass
    return render(request,"employeeLogin.html")




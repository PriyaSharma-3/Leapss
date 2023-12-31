"""crud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homePage', views.homePage),
    path('adminLogin', views.adminLogin),
    path('adminDashboard',views.adminDashboard),
    path('employeeLogin', views.employeeLogin),
    path('addEmployee',views.addEmployee),
    path('sidebar', views.sidebar),
    path('profileSetting', views.profileSetting),
    path("approvalStatus",views.approvalStatus),
    path('leaveSection', views.leaveSection),
    path('leaveApplication', views.leaveApplication),
    path('leaveBasket', views.leaveBasket),
    path('edit', views.edit),
    path('show_Emp_ID', views.show_Emp_ID),
    path("editEmployee/<int:id>",views.editEmployee),
    path('update/<int:id>', views.update),
    path('delete/<int:id>', views.destroy),
    path('remove_Emp_ID', views.remove_Emp_ID),
    path('employees', views.employees),
    path('leaveApplicationDetails', views.leaveApplicationDetails),
    path('removeEmployees', views.removeEmployees),
    path('reviewLeaveApplication/<str:Emp_ID>/<int:id>', views.reviewLeaveApplication),
    path('reviewEmployeeApplication/<str:Emp_ID>/<int:id>', views.reviewEmployeeApplication),
    path('adminlogout', views.adminlogout),
    path('employeelogout', views.employeelogout),
    path('Approve_leave/<str:Emp_ID>/<int:id>',views.Approve_leave),
    path('Reject_leave/<str:Emp_ID>/<int:id>',views.Reject_leave),
    path('deactive_emp/<str:Emp_ID>/<int:id>',views.deactive_emp),
    path('active_emp/<str:Emp_ID>/<int:id>',views.active_emp),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
from django.urls import path

from FamilyLogin import views

app_name = "FamilyLogin"

urlpatterns = [
    path('', views.home),
    path('loginscreen', views.login_screen, name='LoginScreen'),
    path('Registerscreen', views.register_screen, name='RegisterScreen'),
    path('registeruser', views.register_user),
    path('loginuser', views.login_user, name='loginuser'),
    path('addfamilymembers', views.add_family, name='addfamily'),
    path('addingmember', views.adding_member, name="addingmember"),
    path('seefamily', views.see_family, name="seefamily"),
    path('gotohome', views.go_to_home, name="gotohome"),
    path('logoutuser', views.logout_user),
    path('updatemem/<int:id>', views.update_family_mem, name="update"),
    path('delmem/<int:id>', views.del_family_mem, name="delete"),
    path('addingexpenses', views.add_expenses, name="addexpenses"),
    path('saveexpensedata', views.save_expense_data, name="saveexpenses"),
    path('viewexpenses', views.view_expenses, name="viewexpenses"),
    path('seemonthlyreport', views.see_monthly_report, name="seemonthlyreport"),
    path('getmonthlyrecords', views.get_monthly_records),
    path('updateExpenses/<int:id>', views.update_expenses, name="updateExpenses"),
    path('deleteExpenses/<int:id>', views.delete_expenses, name="deleteExpenses"),
    path('seeyearlyreport', views.see_yearly_report, name="seeyearlyreport"),
    path('getyearlyrecords', views.get_yearly_records, name="getyearlyrecords"),
    path('seeconsolidatereport', views.see_consolidate_report, name="seeconsolidatereport"),
    path('getconsolidatedreport', views.get_consolidated_report, name='getconsolidatedreport')

]

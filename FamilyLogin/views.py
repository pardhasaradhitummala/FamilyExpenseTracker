from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from FamilyLogin.services import *
from FamilyLogin.models import FamilyMembers, Expenses


def home(request):
    return render(request, 'index.html')


def login_screen(request):
    return render(request, 'login.html', {'data': ''})


def register_screen(request):
    return render(request, 'register.html')


def register_user(request):
    email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    if User.objects.filter(username=username).exists():
        return render(request, 'register.html', {'user_available': True})
    elif User.objects.filter(email=email).exists():
        return render(request, 'register.html', {'email_available': True})
    else:
        user = User.objects.create_user(email=email, password=password, username=username)
        user.save()
        return render(request, 'login.html', {'data': ''})


def login_user(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return render(request, "family_person.html")
    else:
        return render(request, 'login.html', {'data': 'failed'})


def add_family(request):
    return render(request, 'add_members.html')


def adding_member(request):
    income = request.POST['income']
    if income == '':
        context = {
            'null': True
        }
        return render(request, 'add_members.html', context)
    else:
        income = float(income)
    family_mem = FamilyMembers()
    family_mem.firstname = request.POST['firstname']
    family_mem.lastname = request.POST['lastname']
    family_mem.income = income
    family_mem.familyLead = request.user
    family_mem.save()
    return render(request, 'add_members.html')


def see_family(request):
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request, 'see_family.html', {'data': redirect_data})


def go_to_home(request):
    return render(request, 'family_person.html')


def logout_user(request):
    logout(request)
    return render(request, 'index.html')


def update_family_mem(request, id):
    obj = FamilyMembers.objects.get(id=id)
    if request.method == "POST":
        obj.firstname = request.POST['firstname']
        obj.lastname = request.POST['lastname']
        obj.income = float(request.POST['income'])
        obj.save()
        redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
        return render(request, 'see_family.html', {'data': redirect_data})
    return render(request, 'update_mem.html', {'data': obj})


def del_family_mem(request, id):
    obj = FamilyMembers.objects.get(id=id)
    obj.delete()
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request, 'see_family.html', {'data': redirect_data})


def add_expenses(request):
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request, 'add_expense.html', {'data': redirect_data})


def save_expense_data(request):
    exp = Expenses()
    exp.familyLead = request.user
    exp.name = FamilyMembers.objects.get(firstname=request.POST['name'])
    exp.purpose = request.POST['purpose']
    exp.expense = float(request.POST['expense'])
    date_from_user = request.POST.get('date')
    exp.date = datetime.strptime(date_from_user, '%Y-%m-%d')
    exp.save()
    return render(request, 'add_expense.html', {'data': FamilyMembers.objects.filter(familyLead=request.user)})


def view_expenses(request):
    expenses_data = Expenses.objects.filter(familyLead=request.user, date__month=datetime.now().month)
    income_data = FamilyMembers.objects.filter(familyLead=request.user)
    total_income = 0
    if len(income_data) != 0:
        for i in income_data:
            total_income = total_income + float(i.income)
    total_expenses = 0
    if len(expenses_data) != 0:
        for i in expenses_data:
            total_expenses = total_expenses + float(i.expense)
    data = Expenses.objects.filter(familyLead=request.user, date__month=datetime.now().month,
                                   date__year=datetime.now().year)
    context = {
        'data': data, 'month': month_dict[str(datetime.now().month)], 'year': datetime.now().year,
        'income': total_income,
        'expense': total_expenses,
        'netincome': total_income - total_expenses

    }
    return render(request, 'show_expenses.html', context)


def see_monthly_report(request):
    list_years = list(range(2002, datetime.now().year + 1, 1))
    list_months = list(range(2, 13, 1))
    dict1 = {
        'years': list_years,
        'months': list_months,
        'records': "",
        'norecords': "",
        'start_month': 1,
        'start_year': 2001
    }
    return render(request, 'monthly_report.html', dict1)


def get_monthly_records(request):
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    data = Expenses.objects.filter(familyLead=request.user, date__year=year, date__month=month)
    if len(data) == 0:
        no_records = " oops!! No records on that particular month and year"
        records = ""
    else:
        records = data
        no_records = ""
    list_years = list(range(2001, datetime.now().year + 1, 1))
    list_months = list(range(1, 13, 1))
    dict1 = {
        'years': list_years,
        'months': list_months,
        'records': records,
        'norecords': no_records,
        'start_month': month,
        'start_year': year
    }
    return render(request, 'monthly_report.html', dict1)


def delete_expenses(request, id):
    obj = Expenses.objects.get(id=id)
    obj.delete()
    expenses_data = Expenses.objects.filter(familyLead=request.user, date__month=datetime.now().month)
    income_data = FamilyMembers.objects.filter(familyLead=request.user)
    data = get_income_and_expenses(income_data, expenses_data)
    context = expenses_context(request, data)
    return render(request, 'show_expenses.html', context)


def update_expenses(request, id):
    obj = Expenses.objects.get(id=id)
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    if request.method == "POST":
        obj.familyLead = request.user
        obj.name = (FamilyMembers.objects.get(firstname=request.POST['name']))
        obj.purpose = request.POST['purpose']
        obj.expense = float(request.POST['expense'])
        date_user = request.POST.get('date')
        obj.date = datetime.strptime(date_user, '%Y-%m-%d')
        obj.save()
        expenses_data = Expenses.objects.filter(familyLead=request.user, date__month=datetime.now().month)
        income_data = FamilyMembers.objects.filter(familyLead=request.user)
        data = get_income_and_expenses(income_data, expenses_data)
        context = expenses_context(request, data)
        return render(request, 'show_expenses.html', context)
    return render(request, 'update_expense.html', {'data': redirect_data, 'object': obj})


def see_yearly_report(request):
    list_years = list(range(2002, datetime.now().year + 1, 1))
    context = {
        'years': list_years,
        'records': "",
        'norecords': "",
        'start_year': 2001
    }
    return render(request, 'yearly_report.html', context)


def get_yearly_records(request):
    year = int(request.POST['year'])
    data = Expenses.objects.filter(familyLead=request.user, date__year=year)
    if len(data) == 0:
        no_records = " oops!! No records on that particular  year"
        records = ""
    else:
        records = data
        no_records = ""
    list_years = list(range(2001, datetime.now().year + 1, 1))
    context = {
        'years': list_years,
        'records': records,
        'norecords': no_records,
        'start_year': year
    }
    return render(request, 'yearly_report.html', context)


def see_consolidate_report(request):
    context = {"coming": False}
    return render(request, 'consolidate_report.html', context)


def get_consolidated_report(request):
    # today
    today_q = Expenses.objects.filter(familyLead=request.user, date__day=get_today_data()[0],
                                      date__month=get_today_data()[1], date__year=get_today_data()[2]).order_by(
        'name_id').annotate(t_s=Sum('expense'))
    # yesterday expenses
    yesterday_q = Expenses.objects.filter(familyLead=request.user, date__day=get_yesterday_data()[0],
                                          date__month=get_yesterday_data()[1],
                                          date__year=get_yesterday_data()[2]).order_by('name_id').annotate(
        t_s=Sum('expense'))
    # this month
    month_q = Expenses.objects.filter(familyLead=request.user, date__month=get_today_data()[1],
                                      date__year=get_today_data()[2]).order_by('name_id').annotate(t_s=Sum('expense'))
    # consolidated
    from_date = request.POST['fromdate']
    to_date = request.POST['todate']
    consolidated_data = get_consolidated_data(from_date, to_date)
    if consolidated_data[0] > consolidated_data[1]:
        context = {
            'date_failed': True
        }
        return render(request, 'consolidate_report.html', context)
    consolidated_q = Expenses.objects.filter(familyLead=request.user,
                                             date__range=[consolidated_data[0], consolidated_data[1]]).order_by(
        'name_id').annotate(t_s=Sum('expense'))
    context = {
        'coming': True,
        'data_today': query_to_dict(today_q, request),
        'data_yesterday': query_to_dict(yesterday_q, request),
        'data_month': query_to_dict(month_q, request),
        'data_consolidated': query_to_dict(consolidated_q, request),
        'today_total': find_total(query_to_dict(today_q, request)),
        'yesterday_total': find_total(query_to_dict(yesterday_q, request)),
        'month_total': find_total(query_to_dict(month_q, request)),
        'con_total': find_total(query_to_dict(consolidated_q, request))
    }
    return render(request, 'consolidate_report.html', context)

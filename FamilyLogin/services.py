from FamilyLogin.models import Expenses, FamilyMembers
from datetime import datetime, timedelta, date


def get_today_data():
    return datetime.now().day, datetime.now().month, datetime.now().year


def get_yesterday_data():
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    return yesterday.day, yesterday.month, yesterday.year


def get_consolidated_data(start_in, end_in):
    date_from = datetime.strptime(start_in, '%Y-%m-%d')
    date_to = datetime.strptime(end_in, '%Y-%m-%d')
    start = date(date_from.year, date_from.month, date_from.day)
    end = date(date_to.year, date_to.month, date_to.day) + timedelta(days=1)
    return start, end


def query_to_dict(q, req):
    sum_dict = {}
    for i in q:
        if i.name not in sum_dict:
            sum_dict[i.name] = i.expense
        else:
            sum_dict[i.name] = sum_dict[i.name] + i.expense
    family = FamilyMembers.objects.filter(familyLead=req.user)
    family_mem = []
    for i in family:
        family_mem.append(i)
    for i in family_mem:
        if i not in sum_dict.keys():
            sum_dict[i] = 0
    return sum_dict


def find_total(q_dict):
    total = 0
    for key, value in q_dict.items():
        total = total + value
    return total


month_dict = {'1': 'January',
              '2': 'February',
              '3': 'March',
              '4': 'April',
              '5': 'May',
              '6': 'June',
              '7': 'July',
              '8': 'August',
              '9': 'September',
              '10': 'October',
              '11': 'November',
              '12': 'December'}


def get_income_and_expenses(income_data, expenses_data):
    total_income = 0
    total_expenses = 0
    if len(income_data) != 0:
        for i in income_data:
            total_income = total_income + float(i.income)
    if len(expenses_data) != 0:
        for i in expenses_data:
            total_expenses = total_expenses + float(i.expense)
    return total_income, total_expenses


def expenses_context(request,data):
    return {
        'data': Expenses.objects.filter(familyLead=request.user, date__month=datetime.now().month,
                                        date__year=datetime.now().year),
        'month': month_dict[str(datetime.now().month)],
        'year': datetime.now().year,
        'income': data[0],
        'expense': data[1],
        'netincome': data[0] - data[1]

    }



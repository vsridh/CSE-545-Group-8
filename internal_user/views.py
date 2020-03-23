from django.shortcuts import render
from django.http import HttpResponse
from .forms import FundDepositForm

customers = [
    {
        'customerName': 'James Karen',
        'customerId': 1,
        'accountId': 1,
        'accountType': 'Savings'
    },
    {
        'customerName': 'Jane Doe',
        'customerId': 2,
        'accountId': 2,
        'accountType': 'Checking'
    }
]

def initFundDeposit(request):
    return render(request, 'init_fund_deposit.html')

def searchCustomer(request):
    context = {
        'customers' : customers,
        'customerSearchString' : request.POST['customerSearchString']
    }
    return render(request, 'init_fund_deposit.html', context)

def depositFund(request):
    form = FundDepositForm()
    return render(request, 'depositFund.html', {'form':form})

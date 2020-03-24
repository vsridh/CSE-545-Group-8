from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
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
    if request.method == 'POST':
        form = FundDepositForm(request.POST)
        if form.is_valid():
            depositAmount = form.cleaned_data.get('depositAmount')
            ## backend code goes here
            messages.success(request, f'Amount deposited successfully {depositAmount}')
            return redirect('./initFundDeposit')


def depositTemplate(request):
    form = FundDepositForm(initial={'customerName': request.POST['customerName'],
                                    'customerId': request.POST['customerId'],
                                    'accountId': request.POST['accountId'],
                                    'accountType': request.POST['accountType']
    })
    return render(request, 'depositFund.html', {'form':form})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FundDepositForm, IssueChequeForm, CustomerForm

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
        'customerSearchString' : request.POST['customerSearchString'],
    }
    if request.POST['context_page']=='deposit':
        return render(request, 'init_fund_deposit.html', context)
    elif request.POST['context_page']=='issue_cheque':
        return render(request, 'init_issue_cheque.html', context)
    elif request.POST['context_page']=='view_customer':
        return render(request, 'init_view_customer.html', context)

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

def initIssueCheque(request):
    return render(request, 'init_issue_cheque.html')

def issueCheque(request):
    if request.method == 'POST':
        form = IssueChequeForm(request.POST)
        if form.is_valid():
            chequeAmount = form.cleaned_data.get('chequeAmount')
            ## backend code goes here
            messages.success(request, f'Cheque Issued successfully {chequeAmount}')
            return redirect('./initIssueCheque')


def issueChequeTemplate(request):
    form = IssueChequeForm(initial={'customerName': request.POST['customerName'],
                                    'customerId': request.POST['customerId'],
                                    'accountId': request.POST['accountId'],
                                    'accountType': request.POST['accountType']
    })
    return render(request, 'issueCheque.html', {'form':form})

def initViewCustomer(request):
    return render(request, 'init_view_customer.html')

def viewCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(initial={'customerName': request.POST['customerName'],
                                    'customerId': request.POST['customerId'],
                                    'accountId': request.POST['accountId'],
                                    'accountType': request.POST['accountType']
        })
        ##Get all customer realted data from database and populate form
        return render(request, 'view_customer.html', {'form':form})
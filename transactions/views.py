from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FundTransferForm
from django.conf import settings

transactionList = [
    {
        'requesterName': 'James Karen',
        'requesterId': 1,
        'requestDate': '03/21/2020',
        'amount': 500,
        'transactionId': 111,
        'transactionType': 'customerRequest'
    },
    {
        'requesterName': 'Vijai Hari',
        'requesterId': 2,
        'requestDate': '03/19/2020',
        'amount': 1500,
        'transactionId': 211,
        'transactionType': 'customerRequest'
    },
    {
        'requesterName': 'Jane Doe',
        'requesterId': 3,
        'requestDate': '03/15/2020',
        'amount': 300,
        'transactionId': 311,
        'transactionType': 'tier1Request'
    }
]

def fundTransfer(request):
    if request.method == 'POST':
        print('inside')
        form = FundTransferForm(request.POST)
        if form.is_valid():
            print('inside2')
            transferAmount = form.cleaned_data.get('transferAmount')
            messages.success(request, f'Fund transfered successfully {transferAmount}')
            return redirect(settings.BASE_URL+'/user_home/home')
        else:
            messages.error(request, f'Form is not valid')
            return redirect(settings.BASE_URL+'/user_home/home')
    else:
        return render(request, 'fundTransfer.html')

def initfundTransfer(request):
    return render(request, 'fundTransfer.html')

def pendingTrans(request):
    context = {
        'pendingTransList' : transactionList
    }
    return render(request, 'pendingTransactions.html', context)

def updateTransaction(request):
    return HttpResponse({'value':'success'}, status=200)

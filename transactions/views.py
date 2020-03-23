from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'fundTransfer.html')

def pendingTrans(request):
    context = {
        'pendingTransList' : transactionList
    }
    return render(request, 'pendingTransactions.html', context)

def approveTransaction(request):
    return HttpResponse({'value':'success'}, status=200)

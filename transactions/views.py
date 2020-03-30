from django.shortcuts import render, redirect
from django.http import *
from django.contrib import messages
from .forms import *
from django.conf import settings

from home.models import *
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import cryptography.exceptions
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import rsa

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


def fund_deposit(request):
    """Deposits the given amount of money into the specified bank account"""
    if request.method == 'POST':
        form = FundDepositWithdrawForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data.get('depositAccount')
            amount = form.cleaned_data.get('depositAmount')
            account_object = Account.objects.get(pk=account)

            # Check that account was found
            if account_object is not None:
                account_object.account_balance += amount
                account_object.save()
                return render(request, 'success.html')
            else:
                return render(request, 'failed.html', {'failure': '500 Error: Account not found.'}, status=500)
    elif request.method == 'GET':
        return render(request, 'deposit.html')
    else:
        return render(request, 'failed.html', {'failure': '405 Error: Method not supported.'}, status=405)


def fund_withdraw(request):
    """Withdraws the given amount of money from the specified bank account"""
    if request.method == 'POST':
        form = FundDepositWithdrawForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data.get('withdrawAccount')
            amount = form.cleaned_data.get('withdrawAmount')
            account_object = Account.objects.get(pk=account)

            # Check that account was found
            if account_object is not None:
                # Check for adequate funds
                if account_object.account_balance >= amount:
                    account_object.account_balance -= amount
                    account_object.save()
                    return render(request, 'success.html')
                else:
                    return render(request, 'failed.html',  {'failure': '403 Error: Account balance too small.'},
                                  status=403)
            else:
                return render(request, 'failed.html', {'failure': '500 Error: Account not found.'}, status=500)
        else:
            return render(request, 'failed.html', {'failure': '400 Error: Bad request.'}, status=400)
    elif request.method == 'GET':
        return render(request, 'withdraw.html')
    else:
        return render(request, 'failed.html', {'failure': '405 Error: Method not supported.'}, status=405)


def fundTransfer(request):
    if request.method == 'POST':
        print('inside')
        form = FundTransferForm(request.POST)
        if form.is_valid():
            print('inside2')
            transferAmount = form.cleaned_data.get('transferAmount')
            messages.success(request, f'Fund transfered successfully {transferAmount}')
            return redirect(settings.BASE_URL + '/user_home/home')
        else:
            messages.error(request, f'Form is not valid')
            return redirect(settings.BASE_URL + '/user_home/home')
    else:
        return render(request, 'fundTransfer.html')


def initfundTransfer(request):
    return render(request, 'fundTransfer.html')


def pendingTrans(request):
    context = {
        'pendingTransList': transactionList
    }
    return render(request, 'pendingTransactions.html', context)


def updateTransaction(request):
    return HttpResponse({'value': 'success'}, status=200)


# generate key function
# generate private key and public key
def generate_key():
    # Generate the public/private key pair.
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend(),
    )

    # Save the private key to a file.
    with open('private.key', 'wb') as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save the public key to a file.
    with open('public.pem', 'wb') as f:
        f.write(
            private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
    return


# sign file function
# use private key to sign statement file
# generate sign file, it use to verificate
# The sign file and statement file is corresponding
# private_key---string of private_key file
# file_name ---- string of file should sign
def sign_file(private_key, file_name):
    # Load the private key.
    # private_key=private.key
    with open(private_key, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend(),
        )
    # Load the contents of the file to be signed.
    # file_name='statement.txt'
    with open(file_name, 'rb') as f:
        payload = f.read()

    # Sign the payload file.
    # genertae sign file, it should send to verification
    signature = base64.b64encode(
        private_key.sign(
            payload,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
    )
    with open('signature.sig', 'wb') as f:
        f.write(signature)
    return


# verificate_file function
# need statement file and sign file,  two file is corresponding
# public_key---string of private_key file
# file_name ---- string of file should verificate
# sign_file ----- string of sign file which generate by sign file function, use to verificate
def verificate_file(public_key, file_name, sign_file):
    # Load the public key.
    # public_key=public.pem
    with open(public_key, 'rb') as f:
        public_key = load_pem_public_key(f.read(), default_backend())

    # Load the statement contents and the signature.
    # file_name='statement.txt'
    with open(file_name, 'rb') as f:
        payload_contents = f.read()
    # sign_file='signature.sig'
    with open(sign_file, 'rb') as f:
        signature = base64.b64decode(f.read())

    # Perform the verification.
    try:
        public_key.verify(
            signature,
            payload_contents,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        # this file is pass verification
        # to do more
        ##############
    except cryptography.exceptions.InvalidSignature as e:
        # this file is fail
        # ERROR
        print('ERROR: Payload and/or signature files failed verification!')
    return

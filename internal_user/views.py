from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import FundDepositForm, IssueChequeForm, CustomerForm
from django.conf import settings
from internal_user.approvals import _viewRequests, _updateRequest, _view_updates, _approve_update, _view_open_accs,_approve_open_request,_view_close_accs,_approve_close_request,_viewInternalRequests,_updateInternalRequest
from internal_user.utils import render_to_pdf,verify_file

def initFundDeposit(request):
    return render(request, 'init_fund_deposit.html')

def depositTemplate(request):
    form = FundDepositForm(initial={'customerName': request.POST['customerName'],
                                    'customerId': request.POST['customerId'],
                                    'accountId': request.POST['accountId'],
                                    'accountType': request.POST['accountType']
    })
    return render(request, 'depositFund.html', {'form':form})

def depositFund(request):
    if request.method == 'POST':
        form = FundDepositForm(request.POST)
        if form.is_valid():
            depositAmount = form.cleaned_data.get('depositAmount')
            ## backend code goes here
            messages.success(request, f'Amount deposited successfully {depositAmount}')
            return redirect('./initFundDeposit')

def initIssueCheque(request):
    context = {'context_page' : 'issue_cheque'}
    return render(request, 'init_issue_cheque.html', context)

def issueChequeTemplate(request):
    form = IssueChequeForm(initial={'customerName': request.POST['customerName'],
                                    'customerId': request.POST['customerId'],
                                    'accountId': request.POST['accountId'],
                                    'accountType': request.POST['accountType']
    })
    return render(request, 'issueCheque.html', {'form':form})

def issueCheque(request):
    if request.method == 'POST':
        form = IssueChequeForm(request.POST)
        if form.is_valid():
            chequeAmount = form.cleaned_data.get('chequeAmount')
            ## backend code goes here
            messages.success(request, f'Cheque Issued successfully {chequeAmount}')
            cheque_id = 222
            data = {
                'pay_to':form.cleaned_data.get('recipientName'),
                'cheque_id': cheque_id,
                'amount': form.cleaned_data.get('chequeAmount'),
            }
            pdf = render_to_pdf('pdf_template.html', data)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Cheque_"+str(cheque_id)+".pdf"
                content = "attachment; filename=%s" % (filename)
                response['Content-Disposition'] = content
                return response

def verifyCheque(request):
    try:
        try:
            chequeId = request.FILES['cheque'].name.split('_')[-1].replace(settings.SIGNATURE_FILES_FORMAT,'')
        except:
            return HttpResponse("Invalid file name format, file name should be of form Cheque_CHEQUEID.pdf")
        status = verify_file('public.pem', request.FILES['cheque'], settings.SIGNATURE_FILES + str(chequeId) + settings.SIGNATURE_FILES_FORMAT)
        status = not status
        context = {'tampared': status}
    except:
        return HttpResponse("Error occured while verifying cheque")
    return render(request, 'verify_cheque.html', context)

def initVerifyCheque(request):
    return render(request, 'init_verify.html')

def searchCustomer(request):
    context = {
        'customers' : customers,
        'customerSearchString' : request.POST['customerSearchString']
    }
    if request.POST['context_page']=='deposit':
        return render(request, 'init_fund_deposit.html', context)
    elif request.POST['context_page']=='issue_cheque':
        return render(request, 'init_issue_cheque.html', context)
    elif request.POST['context_page']=='view_customer':
        return render(request, 'init_view_customer.html', context)
    elif request.POST['context_page']=='modify_customer':
        return render(request, 'init_modify_customer.html', context)
    elif request.POST['context_page']=='delete_customer':
        return render(request, 'delete_customer_account.html', context)

def initViewCustomer(request):
    context = {'context_page' : 'view_customer'}
    return render(request, 'init_view_customer.html', context)

def viewCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(initial={'customerName': request.POST['customerName'],
                                    'customerId': request.POST['customerId'],
                                    'accountId': request.POST['accountId'],
                                    'accountType': request.POST['accountType']
        })
        ##Get all customer realted data from database and populate form
        return render(request, 'view_customer.html', {'form':form})

def createCustomer(request):
    return redirect(settings.BASE_URL+'/create_account')

def initModifyCustomer(request):
    context = {'context_page' : 'modify_customer'}
    return render(request, 'init_modify_customer.html', context)

def modifyCustomerTemplate(request):
    if request.method == 'POST':
        # populate all customer related data here in the form
        form = CustomerForm(initial={'customerName': request.POST['customerName'],
                                    'customerId': request.POST['customerId'],
                                    'accountId': request.POST['accountId'],
                                    'accountType': request.POST['accountType']
        })
        return render(request, 'modify_customer_template.html',{'form':form})

def modifyCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        #backend code goes here, save modified form data to db
        return redirect('./initModifyCustomer')

def deleteCustomer(request):
    context = {'context_page' : 'delete_customer'}
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            ## backend code goes here. Code to delete/close customer account
            messages.success(request, f'Customer account deleted successfully')
            return redirect(settings.BASE_URL+'/user_home/home')
        else:
            messages.error(request, f'Failed to delete customer account')
            return redirect(settings.BASE_URL+'/user_home/home')
    else:
        form = CustomerForm()
        return render(request, 'delete_customer_account.html', context)

def viewRequests(request):
    return _viewRequests(request)

def updateRequest(request):
    return _updateRequest(request)

def viewInternalRequests(request):
    return _viewInternalRequests(request)

def view_updates(request):
    return _view_updates(request)

def view_open_accs(request):
    return _view_open_accs(request)

def view_close_accs(request):
    return _view_close_accs(request)

def updateInternalRequest(request):
    return _updateInternalRequest(request)

def approve_update(request):
    return _approve_update(request)

def approve_open_request(request):
    return _approve_open_request(request)

def approve_close_request(request):
    return _approve_close_request(request)

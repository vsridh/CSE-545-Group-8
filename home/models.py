from django.db import models

# Create your models here.
class Privilege(models.Model):
    view_transaction = models.BooleanField()
    create_transaction = models.BooleanField()
    authorize_transaction = models.BooleanField()
    transaction_type = models.CharField(max_length=20)
    issue_check = models.BooleanField()
    fund_transfer = models.BooleanField()
    view_account = models.BooleanField()
    create_account = models.BooleanField()
    modify_account = models.BooleanField()
    close_account = models.BooleanField()
    delete_account = models.BooleanField()
    account_type = models.CharField(max_length=20)
    request_type = models.CharField(max_length=20)
    access_logs = models.BooleanField()
    user_type = models.CharField(max_length=10)

    def __str__(self):
        return self.user_id
        
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    business_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.IntegerField()
    mobile_number = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    birthdate = models.DateTimeField()
    ssn = models.CharField(max_length=9)
    user_type = models.CharField(max_length=10)
    joining_date = models.DateTimeField()
    password = models.CharField(max_length=200)
    privilege_id = models.ForeignKey(Privilege, on_delete=models.CASCADE)

    def __str__(self):
        if self.first_name:
            return self.first_name
        else:
            return self.business_name

class Account(models.Model):
    account_type = models.CharField(max_length=20)
    account_balance = models.BigIntegerField()
    creation_date = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_type

class Transaction(models.Model):
    from_account = models.IntegerField()
    to_account = models.IntegerField()
    transaction_value = models.BigIntegerField()
    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=20)
    transaction_status = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id

class Appointment(models.Model):
    appointment_date = models.DateTimeField()
    appointment_subject = models.TextField()
    appointment_assigned_to = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id

class Requests(models.Model):
    request_date = models.DateTimeField()
    request_subject = models.TextField()
    request_assigned_to = models.IntegerField()
    request_type = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id
from django.db import models

# Create your models here.
class BankDetail(models.Model):

    def __str__(self):
        return self.ifsc_code

    ifsc_code = models.CharField(max_length=11, primary_key=True)
    branch_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    branch_address = models.CharField(max_length=250)    
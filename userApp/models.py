from django.db import models
from django.contrib.auth.models import User
from baseApp.models import tblFeeders, tblTariffs

class tblMeters(models.Model):
    user = models.ForeignKey(User, default=None, to_field='username', on_delete=models.CASCADE)
    feederName = models.ForeignKey(tblFeeders, default=None, to_field='name', on_delete=models.CASCADE)
    meterType = models.CharField(max_length=50)
    connectionType = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    installationDate = models.CharField(max_length=15, null=True)
    isActive = models.BooleanField(default=False)

    class Meta:
        db_table = "tbl_meters"

    def __str__(self):
        return str(self.id)

class tblBills(models.Model):
    meterID = models.ForeignKey(tblMeters, default=None, to_field='id', on_delete=models.CASCADE)
    tariffID = models.ForeignKey(tblTariffs,default=None, to_field='tariffID', on_delete=models.CASCADE)
    billingMonth = models.CharField(max_length=50, null=True)
    previousReading = models.FloatField(default=0)
    currentReading = models.FloatField(default=0)
    units = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=10)
    paidDate = models.CharField(max_length=20, null=True)
    dueDate = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "tbl_bills"

    def __str__(self):
        return str(self.id)
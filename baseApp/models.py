from django.db import models

# Create your models here.

class tblFeeders(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    div = models.CharField(max_length=50)
    subDiv = models.CharField(max_length=50)
    readingDate = models.CharField(max_length=20, null=True)
    issueDate = models.CharField(max_length=20, null=True)
    class Meta:
        db_table = "tbl_feeders"

    def __str__(self):
        return self.name

class tblTariffs(models.Model):
    tariffID = models.CharField(max_length=10, primary_key=True)
    slab1Rate = models.FloatField(default=0)
    slab2Rate = models.FloatField(default=0)
    slab3Rate = models.FloatField(default=0)
    singlePhMeterRent = models.FloatField(default=0)
    threePhMeterRent = models.FloatField(default=0)
    TVFee = models.FloatField(default=0)
    EDuty = models.FloatField(default=0)
    GST = models.FloatField(default=0)
    NJS = models.FloatField(default=0)
    FCS = models.FloatField(default=0)

    class Meta:
        db_table = "tbl_tariffs"

    def __str__(self):
        return self.tariffID

# class tblBillingMonths(models.Model):
#     name = models.CharField(max_length=15, primary_key=True)

#     class Meta:
#         db_table = "tbl_billingmonths"

#     def __str__(self):
#         return self.name

# class tblSchedules(models.Model):
#     feederName = models.ForeignKey(tblFeeders, default=None, to_field='name', on_delete=models.CASCADE)
#     monthName = models.ForeignKey(tblBillingMonths, default=None, to_field='name', on_delete=models.CASCADE)
#     readingDate = models.CharField(max_length=10, default='15')
#     issueDate = models.CharField(max_length=10, default='15')

#     class Meta:
#         db_table = "tbl_schedules"

#     def __str__(self):
#         return self.feederName + ' ' + self.monthName
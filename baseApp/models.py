from django.db import models

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
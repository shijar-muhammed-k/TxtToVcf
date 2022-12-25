from django.db import models

# Create your models here.
class txtfile(models.Model):
    id = models.IntegerField(primary_key=True)
    file = models.FileField(upload_to='Files')
    vcf = models.FileField(upload_to='Files')

    class Meta:
        db_table = "textfile"

class imagefile(models.Model):
    id = models.IntegerField(primary_key=True)
    file = models.FileField(upload_to='Files')
    txt = models.FileField(upload_to='Files')

    class Meta:
        db_table = "imagefiles"
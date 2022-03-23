from django.db import models


class Profession(models.Model):
    description = models.CharField(max_length=255)

    @property
    def status(self):
        return True

    def __str__(self):
        return self.description


class DataSheet(models.Model):
    description = models.CharField(max_length=50)
    historical_data = models.TextField()

    def __str__(self):
        return self.description


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    profession = models.ManyToManyField(Profession)
    data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    doc_num = models.CharField(max_length=50, unique=True, null=True, blank=True)

    @property
    def status_message(self):
        if self.active:
            return "Customer is active"
        else:
            return "Customer is not active"

    def num_professions(self):
        return self.profession.all().count()

    def __str__(self):
        return self.name


class Document(models.Model):
    PP = 'PP'
    ID = 'ID'
    OT = 'OT'

    DOC_TYPE = (
        (PP, 'Passport'),
        (ID, 'Identity Card'),
        (OT, 'Others')
    )

    dtype = models.CharField(choices=DOC_TYPE, max_length=2)
    doc_number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_number

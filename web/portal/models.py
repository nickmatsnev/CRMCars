from django.db import models
import sys
sys.path.append('../')
sys.path.append('../../')
from enum import Enum
from datetime import datetime
from core.lib.constants import BASE_DATE


class RawClientData(models.Model):
    payload = models.TextField()


class Client(models.Model):
    #individuals = models.ForeignKey(Individual, related_name='Individuals', on_delete=models.CASCADE)
    willz_external_id = models.IntegerField(default=0)
    #created_at = models.DateTimeField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    product = models.IntegerField(default=0)


class Individual(models.Model):
    client = models.ForeignKey(Client, related_name='individuals', on_delete=models.CASCADE)
    willz_external_id = models.IntegerField(default=0)
    primary = models.BooleanField(default=False)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender = models.IntegerField(default=0)
    # gender = models.CharField(max_length=100)
    #birthday = models.DateTimeField()
    birthday = models.DateField(default=datetime.strptime(BASE_DATE, "%m.%d.%Y").date(), blank=True)
    dadata_raw = models.TextField(null=True, blank=True)
    dadata_isready = models.BooleanField(default=False)
    dadata_birthplace_raw = models.TextField(null=True, blank=True)
    dadata_birthplace_isready = models.BooleanField(default=False)
    scorista_raw = models.TextField(null=True, blank=True)
    scorista_isready = models.BooleanField(default=False)


class Passport(models.Model):
    individual = models.OneToOneField(Individual, related_name='passport', on_delete=models.CASCADE)
    #number = models.CharField(max_length=100)
    SN_serial = models.IntegerField(default=0)
    SN_number = models.IntegerField(default=0)

    #issued_at = models.DateField()
    issued_at = models.DateField(default=datetime.strptime(BASE_DATE, "%m.%d.%Y").date(), blank=True)
    issued_by = models.TextField()
    division_code = models.CharField(max_length=100, null=True,blank=True)
    birthplace = models.CharField(max_length=100, null=True,blank=True)
    #birth_region = models.CharField(max_length=100, null=True, blank=True)
    #birth_city = models.CharField(max_length=100, null=True, blank=True)

    address_registration = models.CharField(max_length=100)
    #reg_index = models.IntegerField(default=0)
    #reg_obl = models.CharField(max_length=100)
    #reg_city = models.CharField(max_length=100)
    #reg_street = models.CharField(max_length=100, null=True,blank=True)
    #reg_house = models.CharField(max_length=100, null=True,blank=True)
    #reg_building = models.CharField(max_length=100, null=True,blank=True)
    #reg_flat = models.CharField(max_length=100, null=True,blank=True)
    #reg_kladrID = models.CharField(max_length=100, null=True,blank=True)

class DriverLicense(models.Model):
    individual = models.OneToOneField(Individual, related_name='driver_license', on_delete=models.CASCADE)

    number = models.CharField(max_length=100, default="")
    #issued_at = models.DateField(null=True)
    issued_at = models.DateField(default=datetime.strptime(BASE_DATE, "%m.%d.%Y").date(), blank=True)


class PassportImage(models.Model):
    passport = models.ForeignKey(Passport,  related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100,null=True,blank=True)


class DriverLicenseImage(models.Model):
    driver_license = models.ForeignKey(DriverLicense,  related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100,null=True,blank=True)


#class ClientTask(models.Model):
#    task = models.OneToOneField(Task, on_delete=models.CASCADE,null=False)
#    raw_client_data = models.OneToOneField(RawClientData, on_delete=models.CASCADE,null=True)
#    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Source(models.Model):
    source_name = models.IntegerField(default=0)
    source_processor = models.CharField(max_length=100)
    source_processor_start_message = models.CharField(max_length=100)
    source_processor_finish_message = models.CharField(max_length=100)


class SourceRawData(models.Model):
    payload = models.TextField
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)


#class SourceTask(models.Model):
#    task = models.OneToOneField(Task, on_delete=models.CASCADE,null=False)
#    source_raw_data = models.OneToOneField(SourceRawData, on_delete=models.CASCADE)
#    individual = models.OneToOneField(Individual, on_delete=models.CASCADE)


class CheckModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    score_model = models.ForeignKey


class ScoreModel(models.Model):
    check_models = models.ManyToManyField(CheckModel)


class Score(models.Model):
    score = models.IntegerField(default=0)


# class ChecksTask(models.Model):
#     task = models.ForeignKey(Task, related_name='tasks', on_delete=models.CASCADE)
#     individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
#     score_model = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)
#
#
# class ScoringTask(models.Model):
#     task = models.ForeignKey(Task, related_name='tasks', on_delete=models.CASCADE)
#     individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
#     score_model = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)
#

class Check(models.Model):
    checkModel = models.ForeignKey(CheckModel, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


class CheckModelSource(models.Model):
    check_model = models.ForeignKey(CheckModel, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)


class ConcreteScore(models.Model):
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    payload = models.TextField
    score_model = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)
    score_task = models.IntegerField(default=0)


class Generation(models.Model):
    individual = models.ForeignKey(Individual, related_name='generations', on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    create_time = models.DateTimeField()
    is_archive = models.BooleanField()
    #scoring_task = models.OneToOneField(Task, on_delete=models.CASCADE, null=True)
    #source_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    #checks_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)


class Action(models.Model):
    generation = models.ForeignKey(Generation,related_name='actions', on_delete=models.CASCADE)
    create_time = models.DateTimeField()
    processor = models.CharField(max_length=200, null=True)
    action_type = models.CharField(max_length=50)
    payload = models.TextField(null=True)

class ModuleType(Enum):
    ImportModule = 'source'
    ParserModule = 'parser'
    ScoringModule = 'scoring'


class Module(models.Model):
    type = models.TextField(choices=[
        (ModuleType.ImportModule, 'source'),
        (ModuleType.ParserModule, 'parser'),
        (ModuleType.ScoringModule, 'scoring'),
    ])
    name = models.TextField()
    path = models.TextField()
    is_active = models.BooleanField()
    create_time = models.DateTimeField()
    credentials = models.TextField(null=True)


class Product(models.Model):
    name = models.TextField(unique=True)
    primary_scoring = models.IntegerField(default=0)
    other_scoring = models.IntegerField(default=0)


class ModuleData(models.Model):
    individual = models.IntegerField()
    generation = models.IntegerField()
    raw_data = models.TextField()
    name = models.TextField()
    create_time = models.DateTimeField()


class CacheData(models.Model):
    url = models.TextField()
    data = models.TextField(null=True,blank=True)
    headers = models.TextField(null=True,blank=True)
    crc = models.TextField()
    type_of_request = models.TextField(choices=[
        ('GET', 'GET'),
        ('POST', 'POST')])
    body = models.TextField(null=True,blank=True)
    create_time = models.DateTimeField()
    is_active = models.BooleanField()


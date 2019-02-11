from django.db import models
import sys
sys.path.append('../')
from enum import Enum


class RawClientData(models.Model):
    payload = models.TextField()


class Client(models.Model):
    #individuals = models.ForeignKey(Individual, related_name='Individuals', on_delete=models.CASCADE)
    willz = models.IntegerField(default=0)
    #created_at = models.DateTimeField()
    created_at = models.TextField(null=True)


class Individual(models.Model):
    client = models.ForeignKey(Client, related_name='individuals', on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender = models.IntegerField(default=0)
    # gender = models.CharField(max_length=100)
    #birthday = models.DateTimeField()
    birthday = models.TextField(null=True)


class Passport(models.Model):
    individual = models.OneToOneField(Individual, related_name='passport', on_delete=models.CASCADE)

    number = models.CharField(max_length=100)
    #issued_at = models.DateField()
    issued_at = models.TextField()
    issued_by = models.TextField()
    address_registration = models.CharField(max_length=100)
    division_code = models.CharField(max_length=100)
    birthplace = models.CharField(max_length=100)


class DriverLicense(models.Model):
    individual = models.OneToOneField(Individual, related_name='driver_license', on_delete=models.CASCADE)

    number = models.CharField(max_length=100, default="")
    #issued_at = models.DateField(null=True)
    issued_at = models.TextField(null=True)


class Image(models.Model):
    individual = models.ForeignKey(Individual, related_name='individual', on_delete=models.CASCADE)
    passport = models.ForeignKey(Passport, null=True, related_name='passport_images', on_delete=models.CASCADE)
    driver_license = models.ForeignKey(DriverLicense, null=True, related_name='driver_license_images', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True)


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
    individual = models.ForeignKey(Individual,on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    create_time = models.DateTimeField()
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
    ImportModule = 'Source'
    ParserModule = 'Parser'
    ScoringModule = 'Scoring'


class Module(models.Model):
    type = models.TextField(choices=[
        (ModuleType.ImportModule,'Source'),
        (ModuleType.ParserModule,'Parser'),
        (ModuleType.ScoringModule, 'Scoring'),
    ])
    name = models.TextField()
    path = models.TextField()
    is_active = models.BooleanField()
    create_time = models.DateTimeField()
    credentials = models.TextField(null=True)


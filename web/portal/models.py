from django.db import models
import sys
sys.path.append('../')


class Passport(models.Model):
    number = models.CharField(max_length=100)
    issued_at = models.DateField()
    issued_by = models.CharField(max_length=100)
    address_registration = models.CharField(max_length=100)
    division_code = models.CharField(max_length=100)
    birthplace = models.CharField(max_length=100)

    @property
    def images(self):
        ret_images = Image.objects.filter(passport=self.id)
        return ret_images


class DriverLicense(models.Model):
    number = models.CharField(default=0, max_length=100)
    issued_at = models.DateField(null=True)

    @property
    def images(self):
        ret_images = Image.objects.filter(driver_license=self.id)
        return ret_images


class Individual(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender = models.IntegerField(default=0)
    # gender = models.CharField(max_length=100)
    birthday = models.DateTimeField()

    passport = models.OneToOneField(Passport, on_delete=models.CASCADE, null=True)
    driver_license = models.OneToOneField(DriverLicense, on_delete=models.CASCADE, null=True)


class Image(models.Model):
    passport = models.ForeignKey(Passport, related_name='pass_images', on_delete=models.CASCADE, null=True)
    driver_license = models.ForeignKey(DriverLicense, related_name='drv_lcns_images', on_delete=models.CASCADE,
                                       null=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True)


class Task(models.Model):
    create_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    processor = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=50, null=True)
    task_type = models.CharField(max_length=5)


class RawClientData(models.Model):
    payload = models.TextField()


class Client(models.Model):
    #primary_individual = models.ForeignKey(Individual, related_name='clients', on_delete=models.CASCADE)
    willz_id = models.IntegerField(default=0)

    created_at = models.DateTimeField()


class ClientTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE,null=False)
    raw_client_data = models.OneToOneField(RawClientData, on_delete=models.CASCADE,null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Source(models.Model):
    source_name = models.IntegerField(default=0)
    source_processor = models.CharField(max_length=100)
    source_processor_start_message = models.CharField(max_length=100)
    source_processor_finish_message = models.CharField(max_length=100)


class SourceRawData(models.Model):
    payload = models.TextField
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)


class SourceTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE,null=False)
    source_raw_data = models.OneToOneField(SourceRawData, on_delete=models.CASCADE)
    individual = models.OneToOneField(Individual, on_delete=models.CASCADE)


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


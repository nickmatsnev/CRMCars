from django.db import models


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


class License(models.Model):
    number = models.CharField(default=0, max_length=100)
    issued_at = models.DateField(null=True)

    @property
    def images(self):
        ret_images = Image.objects.filter(license=self.id)
        return ret_images


class Individual(models.Model):
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender = models.IntegerField(default=0)
    gender = models.CharField(max_length=100)
    birthday = models.DateTimeField()
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, null=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE, null=True)


#  def license(self):
#     ret_license = License.objects.get(my=self.id)
#    return ret_license

# def passport(self):
#    ret_passport = Passport.objects.get(my=self.id)
#   return ret_passport

#k = Individual()
# sample
#k.passport.issued_at


class Image(models.Model):
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, null=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True)


class Task(models.Model):
    create_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    processor = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=50, null=True)


class RawClientData(models.Model):
    payload = models.aggregates


class Client(models.Model):
    primary_individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    willz_id = models.IntegerField(default=0)

    created_at = models.DateTimeField()


class ClientTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    raw_client_data = models.ForeignKey(RawClientData, on_delete=models.CASCADE)
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
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    source_raw_data = models.ForeignKey(SourceRawData, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)


class ScoreModel(models.Model):
    score = models.IntegerField(default=0)


class ChecksTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    score_model = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)


class ScoringTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    score_model = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)


class CheckRegistry(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Check(models.Model):
    checkRegistry = models.ForeignKey(CheckRegistry, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


class ScoreModelCheckRegistry(models.Model):
    score_model = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)
    check_registry = models.ForeignKey(CheckRegistry, on_delete=models.CASCADE)


class CheckRegistrySource(models.Model):
    check_registry = models.ForeignKey(CheckRegistry, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)


class ConcreteScore(models.Model):
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    payload = models.TextField
    score_model = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)
    score_task = models.IntegerField(default=0)

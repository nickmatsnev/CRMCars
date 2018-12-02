from django.db import models


class Client(models.Model):
    client_id = models.IntegerField(default=0)

    def phone(self):
        return self.driver.phone

    client_type_id = models.IntegerField(default=0)
    client_type = models.CharField(max_length=100)

    def lastname(self):
        return self.driver.lastname

    def firstname(self):
        return self.driver.firstname

    def midddlename(self):
        return self.driver.midddlename

    def email(self):
        return self.driver.email

    def gender_id(self):
        return self.driver.gender_id

    def gender(self):
        return self.driver.gender

    def birthdate(self):
        return self.driver.birthdate

    communication_id = models.IntegerField(default=0)
    communication = models.CharField(max_length=100)
    phone_confirm = models.BooleanField()
    welcome = models.BooleanField()
    amocrm_deal_id = models.IntegerField(default=0)
    ga_client_id = models.CharField(max_length=100)
    utm_source = models.CharField(max_length=100, null=True)
    utm_medium = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField()
    main_driver_id = models.IntegerField(default=0)

    def passport(self):
        return self.driver.passport

    def driver(self):
        return self.drivers.get(driver_id=self.main_driver_id)


class Driver(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    driver_id = models.IntegerField(default=0)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender_id = models.IntegerField(default=0)
    gender = models.CharField(max_length=100)
    birthday = models.DateTimeField()

    def passport(self):
        ret_passport = Passport.objects.get(driver=self.id)
        return ret_passport

    def license(self):
        ret_license = License.objects.get(driver=self.id)
        return ret_license


class Passport(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    issued_at = models.DateField()
    issued_by = models.CharField(max_length=100)
    address_registration = models.CharField(max_length=100)
    division_code = models.CharField(max_length=100)
    birthplace = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    def images(self):
        ret_images = Image.objects.filter(passport=self.id)
        return ret_images


class License(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    number = models.CharField(default=0, max_length=100)
    issued_at = models.DateField(null=True)
    finished_at = models.DateField(null=True)
    created_at = models.DateTimeField()

    def images(self):
        ret_images = Image.objects.filter(license=self.id)
        return ret_images


class Image(models.Model):
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, null=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True)
    confirm_id = models.CharField(max_length=100, null=True)
    confirm = models.CharField(max_length=100, null=True)

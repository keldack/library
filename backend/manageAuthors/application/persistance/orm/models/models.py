from django.db import models


class Author(models.Model):

    name = models.CharField(max_length=50)


class Notice(models.Model):

    id = models.CharField(max_length=20)
    title = models.CharField(max_length=200)


class Copy(models.Model):

    id = models.AutoField()
    notice = models.ForeignKey(Notice)

class Checkout(models.Model):

    copy = models.ForeignKey(Copy)
    on_date = models.DateField()


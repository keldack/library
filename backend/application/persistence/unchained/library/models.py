from django.db import models

# Create your models here.
class Author(models.Model):

    name = models.CharField(max_length=100)


class Book(models.Model):

    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name="books")
        

class Copy(models.Model):

    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    place = models.CharField(max_length=20)


class Checkout(models.Model):

    copy = models.ForeignKey(Copy, on_delete=models.PROTECT)
    on_date = models.DateField()
    return_date = models.DateField()
    borrower = models.CharField(max_length=80)

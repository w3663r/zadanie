from django.db import models

class Osoba(models.Model):

	imie = models.CharField(max_length=50)
	nazwisko = models.CharField(max_length=50)
	def __str__(self):
		return '{} {}'.format(self.imie, self.nazwisko)

class Telefon(models.Model):

	osoba = models.ForeignKey(Osoba,related_name='telefony', editable=False, on_delete=models.CASCADE)
	telefon = models.CharField(max_length=50)
	def __str__(self):
		return '{}'.format(self.telefon)

class Email(models.Model):

	osoba = models.ForeignKey(Osoba, editable=False,related_name='emaile', on_delete=models.CASCADE)
	email = models.EmailField()
	def __str__(self):
		return '{}'.format(self.email)


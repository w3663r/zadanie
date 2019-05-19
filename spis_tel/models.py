from django.db import models


class OsobaManager(models.Manager):
    '''nie wykorzystywane, zwraca listę obiektów typu Osoba z atrybutem telefon (lista telefonow w postaci str)'''

    def with_info(self):
        from django.db import connection
        results = []
        with connection.cursor() as cursor:
            for row in cursor.execute("""
                SELECT p.id, p.imie, p.nazwisko, t.telefon
                FROM spis_tel_osoba p,spis_tel_telefon t
                WHERE p.id = t.osoba_id 
		ORDER BY p.id"""):
                p = self.model(id=row[0], imie=row[1], nazwisko=row[2])
                if p in results:
                    results[results.index(p)].telefon.append(row[3])
                else:
                    p.telefon=[row[3]]
                    results.append(p)
                print(row)
        print(results)
        return results

           
class Osoba(models.Model):

	imie = models.CharField(max_length=50)
	nazwisko = models.CharField(max_length=50)
	def imieinazwisko(self):
		return '{} {}'.format(self.imie, self.nazwisko)
	objects = OsobaManager()

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


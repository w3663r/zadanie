from django.db import models


class OsobaManager(models.Manager):
    def with_info(self):
        from django.db import connection
        dic = {'osoba': 0, 'telefony':[]}
        results = []
        osoby = []
        sets = []
        with connection.cursor() as cursor:
            for row in cursor.execute("""
                SELECT p.id, p.imie, p.nazwisko, t.telefon, e.email
                FROM spis_tel_osoba p
                    LEFT JOIN spis_tel_telefon t
		                ON p.id = t.osoba_id 
                    LEFT JOIN spis_tel_email e
		                ON p.id = e.osoba_id 
		        ORDER BY p.id"""):
                osoby.append(row[0])
                p = self.model(id=row[0], imie=row[1], nazwisko=row[2])
                if p in results:
                    results[results.index(p)].telefon.append(row[3])
                else:
                    p.telefon=[row[3]]
                    results.append(p)
                print(row)
        print(results)
        return results
    def telephone(self):
        from django.db import connection
        results = []
        with connection.cursor() as cursor:
            for row in cursor.execute("""
                SELECT  *
                FROM spis_tel_osoba p, spis_tel_telefon t
				WHERE p.id = t.osoba_id
				GROUP BY p.id"""):
                print(row)
                '''p = self.model(id=row[0], imie=row[1], nazwisko=row[2])
                p.telefon = row[3]
                results.append(p)'''
        return results

    def has_data(self,id):
        from django.db import connection
        results = []
		
        with connection.cursor() as cursor:
            for row in cursor.execute("""
                SELECT t.telefon, e.email
                FROM spis_tel_email e, spis_tel_telefon t
				WHERE spis_tel_osoba.id = t.osoba_id
				AND spis_tel_osoba.id = e.osoba_id
									"""):
                results.append(row[0],row[1])
        if results != []:
            return True
        else: 
            return False
           
class Osoba(models.Model):

	imie = models.CharField(max_length=50)
	nazwisko = models.CharField(max_length=50)
	objects = OsobaManager()

	def __str__(self):
		return '{} {}'.format(self.imie, self.nazwisko)

class Telefon(models.Model):

	osoba = models.ForeignKey(Osoba,related_name='telefony', editable=True, on_delete=models.CASCADE)
	telefon = models.CharField(max_length=50)
	def __str__(self):
		return '{}'.format(self.telefon)

class Email(models.Model):

	osoba = models.ForeignKey(Osoba, editable=True,related_name='emaile', on_delete=models.CASCADE)
	email = models.EmailField()
	def __str__(self):
		return '{}'.format(self.email)


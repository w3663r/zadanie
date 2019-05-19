from . import models
from django.db.models import Q
from itertools import chain

def get_data_list():
    '''lista slownikow, takich że : {'osoba': Osoba, 'telefony': lista Telefon'ow, 'emaile': lista Email'i}'''
    from . import models
    os_obj = models.Osoba.objects
    tel_obj = models.Telefon.objects
    em_obj = models.Email.objects
    l = [{'osoba':o, 'telefony':[t for t in tel_obj.filter(osoba_id= o.id)], 'emaile':[e for e in em_obj.filter(osoba_id= o.id)]} for o in os_obj.all()]
    return l

def search(query):
	
	l = get_data_list()
	if query:
		if len(query.split(' ')) > 1:
			new_query = query.split(' ')
			#if ' ' in query as 'joanna ', new query contains '', and search returns all objects, not right
			osoba_qset = (Q(imie__icontains=new_query[0])|Q(nazwisko__icontains=new_query[1])|Q(imie__icontains=new_query[1])|Q(nazwisko__icontains=new_query[0]))
		else : osoba_qset = (Q(imie__icontains=query)|Q(nazwisko__icontains=query))
		osoby = models.Osoba.objects.filter(osoba_qset).distinct()
		telefony = models.Telefon.objects.filter(Q(telefon__icontains=query)).distinct()
		emaile = models.Email.objects.filter(Q(email__icontains=query)).distinct()
		results = []
		# add object from l list to results, avoid duplicates
		if osoby:
			lista_osob = [o.id for o in osoby]
			results += [i for i in l if i['osoba'].id in lista_osob and i not in results] 
		if telefony: 
			lista_osob = [o.osoba_id for o in telefony]
			results += [i for i in l if i['osoba'].id in lista_osob and i not in results] 
		if emaile:
			lista_osob = [o.osoba_id for o in emaile]
			results += [i for i in l if i['osoba'].id in lista_osob and i not in results] 

	else: results = []
	return results



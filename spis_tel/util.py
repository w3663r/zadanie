from . import models
from django.db.models import Q
from itertools import chain

def get_data_list():
    '''lista slownikow, takich że : {'osoba': Osoba, 'telefony': lista Telefon'ow, 'emaile': lista Email'i}'''
    os_obj = models.Osoba.objects.all
    tel_obj = models.Telefon.objects.filter
    em_obj = models.Email.objects.filter
    return ([{'osoba':o, 'telefony':list(tel_obj(osoba_id=o.id)), 'emaile':list(em_obj(osoba_id=o.id))} for o in os_obj()])
    

def search(query):
	'''lista wyników wyszukiwania, każdy jak słownik w get_data_list'''
	l = get_data_list()
	if query and query.strip():
		list_query = query.split(' ')
		if len(list_query) > 1:
			osoba_qset = (Q(imie__icontains=list_query[0])&Q(nazwisko__icontains=list_query[1])|Q(imie__icontains=list_query[1])&Q(nazwisko__icontains=list_query[0]))
		else : osoba_qset = (Q(imie__icontains=query)|Q(nazwisko__icontains=query))
		osoby = models.Osoba.objects.filter(osoba_qset).distinct()
		telefony = models.Telefon.objects.filter(Q(telefon__icontains=query)).distinct()
		emaile = models.Email.objects.filter(Q(email__icontains=query)).distinct()
		results = [i for i in l if i['osoba'] in osoby or set(i['telefony']).intersection(set(telefony)) or set(i['emaile']).intersection(set(emaile))]

	else: results = []
	return results

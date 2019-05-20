from . import models
from django.db.models import Q
from itertools import chain

def get_data_list():
    '''lista slownikow, takich że : {'osoba': Osoba, 'telefony': lista Telefon'ow, 'emaile': lista Email'i}'''
    from . import models
    os_obj = models.Osoba.objects
    tel_obj = models.Telefon.objects
    em_obj = models.Email.objects
    return ([{'osoba':o, 'telefony':list(tel_obj.filter(osoba_id=o.id)), 'emaile':list(em_obj.filter(osoba_id=o.id))} for o in os_obj.all()])
    

def search(query):
	'''lista wyników wyszukiwania, każdy jak słownik w get_data_list'''
	l = get_data_list()
	if query and query.strip():
		if len(query.split(' ')) > 1:
			list_query = query.split(' ')
			osoba_qset = (Q(imie__icontains=list_query[0])&Q(nazwisko__icontains=list_query[1])|Q(imie__icontains=list_query[1])&Q(nazwisko__icontains=list_query[0]))
		else : osoba_qset = (Q(imie__icontains=query)|Q(nazwisko__icontains=query))
		osoby = models.Osoba.objects.filter(osoba_qset).distinct()
		telefony = models.Telefon.objects.filter(Q(telefon__icontains=query)).distinct()
		emaile = models.Email.objects.filter(Q(email__icontains=query)).distinct()

		results = [i for i in l if i['osoba'] in osoby or set(i['telefony']).intersection(set(telefony)) or set(i['emaile']).intersection(set(emaile))]

	else: results = []
	return results

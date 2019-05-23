from . import models
from django.db.models import Q

def search(query):

	if query and query.strip():
		list_query = query.split(' ')
		if len(list_query) > 1:
			q = (Q(imie__icontains=list_query[0])&Q(nazwisko__icontains=list_query[1])|Q(imie__icontains=list_query[1])&Q(nazwisko__icontains=list_query[0]))
		else : q = Q(imie__icontains=query)|Q(nazwisko__icontains=query)|Q(telefony__telefon__icontains=query)|Q(emaile__email__icontains=query)
		osoby = models.Osoba.objects.filter(q).distinct()
		return osoby
	else: return []


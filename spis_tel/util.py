from . import models
def get_data_list():
    '''lista slownikow, takich że : {'osoba': obiekt, 'telefony': lista obiektów, 'emaile': lista obiektów}'''
    from . import models
    os_obj = models.Osoba.objects
    tel_obj = models.Telefon.objects
    em_obj = models.Email.objects
    l = [{'osoba':o, 'telefony':[t for t in tel_obj.filter(osoba_id= o.id)], 'emaile':[e for e in em_obj.filter(osoba_id= o.id)]} for o in os_obj.all()]
    return l



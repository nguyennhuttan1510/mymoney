def query_or_not(model, **params):
    try:
        return model.objects.get(**params)
    except:
        return None

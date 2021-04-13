import datetime as dt


def get_year(request):
    current_date = dt.date.today()
    return {'year': current_date.year}

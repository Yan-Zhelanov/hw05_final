import datetime as dt


def get_year(request):
    current_date = dt.date.today()
    return {'year': current_date.year}


def following(request):
    if request.user.is_authenticated:
        username = request.path.split('/')[1]
        if request.user.follower.filter(author__username=username).exists():
            return {'following': True}
    return {'following': False}

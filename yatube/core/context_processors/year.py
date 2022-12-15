from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    year = datetime.today().year
    return {
        'greeting': 'Ennyn Pronin: pedo mellon a minno.',
        'year': year,
    }

from datetime import date
from rest_framework.exceptions import ValidationError

MIN_AGE = 18

def validate_adult_creator(claims: dict):
    birthdate_str = claims.get('birthdate')
    
    if not birthdate_str:
        raise ValidationError(
            "Укажите дату рождения, чтобы создать продукт."
        )

    try:
        birthdate = date.fromisoformat(birthdate_str)
    except ValueError:
        
        raise ValidationError(
            "Некорректный формат даты рождения в токене."
        )

    today = date.today()
    
    age = today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

    if age < MIN_AGE:
        raise ValidationError(
            "Вам должно быть 18 лет, чтобы создать продукт."
        )
    
    
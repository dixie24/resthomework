from rest_framework.permissions import BasePermission
from datetime import date
from dateutil.relativedelta import relativedelta

class IsAdultProductCreator(BasePermission):
    message = "Проверка возраста не пройдена." 

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        token_birthdate_str = None

        if hasattr(request.user, 'birthdate') and request.user.birthdate:
            birthdate = request.user.birthdate
        else:

            try:

                token_birthdate_str = request.auth.payload.get('birthdate')
            except AttributeError:

                 pass
            
            if token_birthdate_str is None:
                self.message = "Укажите дату рождения, чтобы создать продукт."
                return False
            try:
                birthdate = date.fromisoformat(token_birthdate_str)
            except ValueError:
                self.message = "Некорректный формат даты рождения в токене."
                return False

        today = date.today()

        eighteen_years_ago = today - relativedelta(years=18)

        if birthdate > eighteen_years_ago:
            self.message = "Вам должно быть 18 лет, чтобы создать продукт."
            return False

        return True
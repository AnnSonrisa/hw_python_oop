import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = float(amount)
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, some_record):
        self.records.append(some_record)

    def get_today_stats(self):
        today = dt.date.today()
        today_amount = 0
        for record in self.records:
            if record.date == today:
                today_amount += record.amount
        return today_amount

    def get_week_stats(self):
        now = dt.date.today()
        then = now - dt.timedelta(days=7)
        week_amount = 0
        for record in self.records:
            if then <= record.date <= now:
                week_amount += record.amount
        return float(week_amount)

    def get_today_remained(self):
        today_amount = self.get_today_stats()
        remains = self.limit - today_amount
        return remains


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_remains = self.get_today_remained()
        if today_remains > 0:
            return f'Сегодня можно съесть что-нибудь ещё, ' \
                   f'но с общей калорийностью не более ' \
                   f'{int(today_remains)} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 72.56
    EURO_RATE = 85.46
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        currencies = {'eur': ('Euro', CashCalculator.EURO_RATE),
                      'usd': ('USD', CashCalculator.USD_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        today_remains = self.get_today_remained()
        currency_name, currency_rate = currencies[currency]
        today_remains_currency = abs(round(today_remains / currency_rate, 2))
        if not today_remains:
            return 'Денег нет, держись'
        if today_remains > 0:
            return f'На сегодня осталось {today_remains_currency} ' \
                   f'{currency_name}'
        else:
            return f'Денег нет, держись: твой долг - ' \
                   f'{today_remains_currency} {currency_name}'

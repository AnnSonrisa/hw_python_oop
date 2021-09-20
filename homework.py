import datetime as dt

NO_CASH = 'Денег нет, держись'
CASH_CURRENCY = '{today_remains_currency} {currency_name}'
CASH_REMAINS = 'На сегодня осталось ' + CASH_CURRENCY
CASH_CREDIT = 'Денег нет, держись: твой долг - ' + CASH_CURRENCY
FORMAT_OF_DATE = '%d.%m.%Y'
CALORIES_LIMIT = 'с общей калорийностью не более {today_remains} кКал'
CALORIES_REMAINS = 'Сегодня можно съесть что-нибудь ещё, но ' + CALORIES_LIMIT
NO_CALORIES = 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = float(amount)
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, FORMAT_OF_DATE).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, some_record) -> None:
        """ Добавление записи """
        self.records.append(some_record)

    def get_today_stats(self) -> float:
        """ Подсчет денег/калорий, потраченных сегодня """
        today = dt.date.today()
        today_amount = sum([record.amount
                            for record in self.records
                            if record.date == today])
        return today_amount

    def get_week_stats(self) -> float:
        """ Подсчет денег/калорий, потраченных за неделю """
        now = dt.date.today()
        then = now - dt.timedelta(days=7)
        week_amount = float(sum([record.amount
                            for record in self.records
                            if then <= record.date <= now]))
        return week_amount

    def get_today_remained(self) -> float:
        """ Подсчет денег/калорий, которые можно потратить/получить сегодня """
        today_amount = self.get_today_stats()
        remains = self.limit - today_amount
        return remains


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """ Подсчет калорий, которые можно получить сегодня """
        today_remains = self.get_today_remained()
        if today_remains > 0:
            return CALORIES_REMAINS.format(today_remains=int(today_remains))
        return NO_CALORIES


class CashCalculator(Calculator):
    USD_RATE = 72.56
    EURO_RATE = 85.46
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency) -> str:
        """ Подсчет денег, которые можно потратить сегодня """
        CURRENCIES = {'eur': ('Euro', CashCalculator.EURO_RATE),

                      'usd': ('USD', CashCalculator.USD_RATE),

                      'rub': ('руб', CashCalculator.RUB_RATE)}
        today_remains = self.get_today_remained()
        try:
            currency_name, currency_rate = CURRENCIES[currency]
        except Exception as exc:
            raise exc('Currency нет в словаре')
        today_remains_currency = abs(round(today_remains / currency_rate, 2))
        if not today_remains:
            return NO_CASH
        if today_remains > 0:
            return CASH_REMAINS.format(
                today_remains_currency=today_remains_currency,
                currency_name=currency_name)
        return CASH_CREDIT.format(
            today_remains_currency=today_remains_currency,
            currency_name=currency_name)

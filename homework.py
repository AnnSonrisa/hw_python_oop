import datetime as dt

FORMAT_OF_DATE = '%d.%m.%y'
CASH_BALANCE = '''На сегодня осталось {balance} 
{currency_name}'''
CASH_DEBT = '''Денег нет, держись: твой долг -  
            {today_remains_currency} {currency_name}'''
CASH_NO = 'Денег нет, держись'
EXCEPTION = 'Currency не существует в словаре'
CALORIES_BALANCE = '''Сегодня можно съесть что-нибудь ещё, 
но с общей калорийностью не более {int(today_remains)} кКал'''
CALORIES_STOP = 'Хватит есть!'


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
        today_amount = sum(record.amount for record in self.records if record.date == today)
        return today_amount

    def get_week_stats(self) -> float:
        """ Подсчет денег/калорий, потраченных за неделю """
        now = dt.date.today()
        then = now - dt.timedelta(days=7)
        week_amount = 0
        week_amount = sum(record.amount for record in self.records if then <= record.date <= now)
        return float(week_amount)

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
            return CALORIES_BALANCE.format(today_remains=today_remains)
        return CALORIES_STOP


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
            raise exc(EXCEPTION)

        today_remains_currency = abs(round(today_remains / currency_rate, 2))
        if not today_remains:
            return CASH_NO
        if today_remains > 0:
            return CASH_BALANCE.format(balance=today_remains_currency,
                                       currency_name=currency_name)
        return CASH_DEBT.format(today_remains_currency=today_remains_currency, currency_name=currency_name)
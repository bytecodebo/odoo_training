import math
from datetime import datetime, timedelta, date

import maya
import numpy as np
import pandas
import pendulum
from pytz import timezone, utc
from odoo import fields
import datetime
from dateutil.relativedelta import relativedelta, MO, TU,WE,FR,TH,SA,SU

DAYS_REL = {1:MO, 2: TU, 3: WE, 4: TH, 5: FR, 6: SA, 7: SU}

DAYS_OF_WEEK = [('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday')
                , ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')]


def datetime_to_string(dt):
    """ Convert the given datetime (converted in UTC) to a string value. """
    return fields.Datetime.to_string(dt.astimezone(utc))

def fn_date_to_string(value, format_date='%Y-%M-%d'):
    """ Convert the given datetime (converted in UTC) to a string value. """
    return value.strftime(format_date)

def to_fecha_literal(fecha):
    # current_date = datetime.strptime(fecha, "%Y-%m-%d")
    if fecha is False:
        fecha = fields.Datetime.now()
    str_fecha = fecha.strftime("%d") + " de "
    month = fecha.month
    if month == 1:
        str_fecha += " enero de "
    elif month == 2:
        str_fecha += " febrero de "
    elif month == 3:
        str_fecha += " marzo de "
    elif month == 4:
        str_fecha += " abril de "
    elif month == 5:
        str_fecha += " mayo de "
    elif month == 6:
        str_fecha += " junio de "
    elif month == 7:
        str_fecha += " julio de "
    elif month == 8:
        str_fecha += " agosto de "
    elif month == 9:
        str_fecha += " septiembre de "
    elif month == 10:
        str_fecha += " octubre de "
    elif month == 11:
        str_fecha += " noviembre de "
    elif month == 12:
        str_fecha += " diciembre de "
    str_fecha += str(fecha.year)
    return str_fecha


def to_month_literal(fecha):
    # current_date = datetime.strptime(fecha, "%Y-%m-%d")
    if fecha is False:
        fecha = datetime.now()
    str_fecha = ""
    month = fecha.month
    if month == 1:
        str_fecha += "Enero"
    elif month == 2:
        str_fecha += "Febrero"
    elif month == 3:
        str_fecha += "Marzo"
    elif month == 4:
        str_fecha += "Abril"
    elif month == 5:
        str_fecha += "Mayo"
    elif month == 6:
        str_fecha += "Junio"
    elif month == 7:
        str_fecha += "Julio"
    elif month == 8:
        str_fecha += "Agosto"
    elif month == 9:
        str_fecha += "Septiembre"
    elif month == 10:
        str_fecha += "Octubre"
    elif month == 11:
        str_fecha += "Noviembre"
    elif month == 12:
        str_fecha += "Diciembre"
    return str_fecha


def fn_to_day_literal(weekday, short=False, upper=True):
    literal = to_day_literal(weekday,short)
    return literal.upper() if upper else literal

def to_day_literal(weekday, short=False):
    # current_date = datetime.strptime(fecha, "%Y-%m-%d")
    str_fecha = ""
    month = int(weekday)
    if month == 0:
        str_fecha += "lunes" if not short else 'lu'
    elif month == 1:
        str_fecha += "martes" if not short else 'ma'
    elif month == 2:
        str_fecha += "miercoles" if not short else 'mi'
    elif month == 3:
        str_fecha += "jueves" if not short else 'ju'
    elif month == 4:
        str_fecha += "viernes" if not short else 'vi'
    elif month == 5:
        str_fecha += "sabado" if not short else 'sa'
    elif month == 6:
        str_fecha += "domingo"  if not short else 'do'
    return str_fecha

def fn_format_float_time(value):
    if not value:
        return 0,0
    pattern = '{:02}:{:02}'
    if value < 0:
        value = np.inf(value)
        pattern = '-' + pattern
    hour = math.floor(value)
    min = round((value % 1) * 60)
    if min == 60:
        min = 0
        hour = hour + 1
    # return pattern.format(hour, min)
    return hour, min


def fn_time_long(from_date=None, time=None, tz_str='UTC', to_format='%Y-%m-%d %H:%M', **kwargs):

    # time = self.fn_formatFloatTime(time)
    full_date = datetime.datetime.now()
    tz = timezone(tz_str)
    start_period = kwargs.get('start_period', None)
    slot_sequence = kwargs.get('slot_sequence', 0)
    slot_period = kwargs.get('slot_period', 0)
    slot_interval = kwargs.get('slot_interval', 'minutes')
    if not start_period:
        if time and isinstance(time, float):
            hour, min = fn_format_float_time(time)
            to_time = datetime.time(hour, min)
        else:
            to_time = time

        full_date = datetime.datetime.combine(from_date or full_date, to_time)
    else:
        if slot_interval == 'minutes':
            full_date = start_period + relativedelta(minutes=slot_period*slot_sequence)
        elif slot_interval == 'months':
            full_date = start_period + relativedelta(months=slot_period*slot_sequence)

    str_date = datetime.datetime.strftime(full_date, to_format)
    return maya.parse(str_date, timezone=tz).datetime(naive=True)


def fn_start_end_month(from_date, tz_str="UTC"):
    new_date = pendulum.datetime(from_date.year, from_date.month, from_date.day, tz=tz_str)
    start_date = new_date.start_of('month')
    end_date = new_date.end_of('month')
    return start_date.in_timezone(tz_str), end_date.in_timezone(tz_str)

#def time_long(date, time):
#    time = time.datetime.strptime('0130', '%H%M').time()
#     return datetime.datetime.combine(date, time)

def days360(start_date, end_date, method_eu=False, incl_end_date=True):
    start_day = start_date.day
    start_month = start_date.month
    start_year = start_date.year
    end_day = end_date.day
    end_month = end_date.month
    end_year = end_date.year

    if (
            start_day == 31 or
            (
                    method_eu is False and
                    start_month == 2 and (
                            start_day == 29 or (
                            start_day == 28 and
                            start_date.is_leap_year is False
                    )
                    )
            )
    ):
        start_day = 30

    if end_day == 31:
        if method_eu is False and start_day != 30:
            end_day = 1

            if end_month == 12:
                end_year += 1
                end_month = 1
            else:
                end_month += 1
        else:
            end_day = 30

    result_days = (end_day + end_month * 30 + end_year * 360 - start_day - start_month * 30 - start_year * 360)
    result_days += 1 if incl_end_date else 0
    return result_days



if __name__ == '__main__':
    d1 = pandas.to_datetime("2020-02-11")
    d2 = pandas.to_datetime("2021-01-11")
    # -print(days360(d1, d2, method_eu=False))


from dateutil import parser
from datetime import datetime, timezone

# Função para formatar a data
def format_date(iso_date, date_format="%d/%m/%Y %H:%M:%S"):
    date = parser.isoparse(iso_date)    
    return date.strftime(date_format)

# Função para calcular a quantidade de dias entre a data atual e a data recebida (cálculo da idade do repositório e cálculo do tempo de atualização)
def calculate_time_between_dates_in_days(iso_date):
    creation_date = parser.isoparse(iso_date)
    now = datetime.now(timezone.utc)
    age = (now - creation_date).days
    return age

# Função para calcular a porcentagem de issues fechadas
def calculate_closed_issues_percentage(closed_issues, total_issues):
    if total_issues == 0:
        return 0
    percentage = (closed_issues / total_issues) * 100
    return round(percentage, 2)
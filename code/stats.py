import csv
from enums.MostPopularLanguages import MostPopularLanguages

# Calcula o valor mediano da lista recebida
def calculate_median(list):
    number_of_elements = len(list)
    sorted_values = sorted(list)
    middle_element = number_of_elements // 2
    if number_of_elements % 2 == 0:
        return (sorted_values[middle_element - 1] + sorted_values[middle_element]) / 2
    else:
        return sorted_values[middle_element]

# Percorre o arquivo csv e coleta os dados para análise
def analyze_data_from_csv(file_path):
    # Inicializa variáveis para armazenar os valores necessários para cada RQ
    total_age_days = []
    total_pull_requests = []
    total_releases = []
    time_since_last_update = []
    primary_languages = []
    total_issues = []
    closed_issues = []

    language_count = {language.value: 0 for language in MostPopularLanguages}

    popular_languages_data = {
        'pull_requests': [],
        'releases': [],
        'time_since_last_update': []
    }

    other_languages_data = {
        'pull_requests': [],
        'releases': [],
        'time_since_last_update': []
    }

    # Lê o arquivo CSV
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Converte e coleta os dados necessários para a análise
            age_days = int(row["Idade do repositorio (dias)"])
            total_age_days.append(age_days)
            
            pull_requests = int(row["Total de Pull Requests"])
            total_pull_requests.append(pull_requests)
            
            releases = int(row["Total de Releases"])
            total_releases.append(releases)
            
            time_since_update_days = int(row["Data da ultima atualizacao"])
            time_since_last_update.append(time_since_update_days)

            primary_language = row["Linguagem primaria"]
            primary_languages.append(primary_language)

            closed_issue = int(row["Total de Issues Fechadas"])
            total_issue = int(row["Total de Issues"])

            closed_issues.append(closed_issue)
            total_issues.append(total_issue)

            if primary_language in language_count:
                language_count[primary_language] += 1
                popular_languages_data['pull_requests'].append(pull_requests)
                popular_languages_data['releases'].append(releases)
                popular_languages_data['time_since_last_update'].append(time_since_update_days)
            else:
                other_languages_data['pull_requests'].append(pull_requests)
                other_languages_data['releases'].append(releases)
                other_languages_data['time_since_last_update'].append(time_since_update_days)

    # Faz os cálculos e exibe os resultados para cada requisito
    results = {
        'RQ01_median_age': calculate_median(total_age_days),
        'RQ02_median_pull_requests': calculate_median(total_pull_requests),
        'RQ03_median_releases': calculate_median(total_releases),
        'RQ04_median_time_since_update': calculate_median(time_since_last_update),
        'RQ05_popular_languages_percentage': analyze_popular_languages(primary_languages),
        'RQ05_amount_of_repositories_per_language': language_count,
        'RQ06_closed_issues_percentage': calculate_closed_issues_percentage(calculate_median(closed_issues), calculate_median(total_issues)),
        'RQ07_analysis_by_language': analyze_data_by_language(popular_languages_data, other_languages_data)
    }

    return results

# Função para verificar se a linguagem recebida está presente no enum de linguagens mais populares
def is_popular_language(language):
    return any(language == popularLanguage.value for popularLanguage in MostPopularLanguages)

# REQ 05 - Função para calcular o percentual de repositórios escritos com as linguagens mais populares
def analyze_popular_languages(primary_languages):
    popular_language_count = 0

    for language in primary_languages:
        if is_popular_language(language):
            popular_language_count += 1

    quantity = len(primary_languages)

    return (popular_language_count / quantity) * 100

# REQ06 - Função para calcular o percentual de issues fechadas, através da razão dos valores medianos de issues fechadas e total de issues dos repositórios
def calculate_closed_issues_percentage(closed_issues, total_issues):
    closed_issues_percentage =(closed_issues / total_issues) * 100 if total_issues > 0 else 0
    return round(closed_issues_percentage, 2)

# REQ07 - Função para obter a mediana de pull requests, releases e tempo desde a última atualização para repositórios com linguagens populares e outras linguagens
def analyze_data_by_language(popular_data, other_data):
    analysis_results = {
        'popular_languages': {
            'median_pull_requests': calculate_median(popular_data['pull_requests']),
            'median_releases': calculate_median(popular_data['releases']),
            'median_time_since_last_update': calculate_median(popular_data['time_since_last_update'])
        },
        'other_languages': {
            'median_pull_requests': calculate_median(other_data['pull_requests']),
            'median_releases': calculate_median(other_data['releases']),
            'median_time_since_last_update': calculate_median(other_data['time_since_last_update'])
        }
    }
    return analysis_results

# Função principal para rodar o script e imprimir os resultados
if __name__ == "__main__":
    file_path = "./repos_info.csv"
    analysis_results = analyze_data_from_csv(file_path)

    # Exibe os resultados
    print("Resultado dos dados analisados:")
    print(f"• RQ01 - Mediana da Idade dos Repositórios (dias): {analysis_results['RQ01_median_age']}")
    print(f"\n• RQ02 - Mediana de Pull Requests Aceitos: {analysis_results['RQ02_median_pull_requests']}")
    print(f"\n• RQ03 - Mediana do Total de Releases: {analysis_results['RQ03_median_releases']}")
    print(f"\n• RQ04 - Mediana do Tempo desde a Última Atualização (dias): {analysis_results['RQ04_median_time_since_update']}")
    print(f"\n• RQ05 - Percentual de Repositórios escritos com as linguagens mais populares: {analysis_results['RQ05_popular_languages_percentage']}")
    
    print("       - Quantidade de Repositórios por Linguagem Popular:")
    for language, count in analysis_results['RQ05_amount_of_repositories_per_language'].items():
        print(f"          - {language.upper()}: {count} repositórios")

    print(f"\n• RQ06 - Percentual de Issues Fechadas: {analysis_results['RQ06_closed_issues_percentage']}")

    print("\n• RQ07 - Análise por Linguagem:")
    print("          - Linguagens Populares:")
    print(f"            - Mediana de Pull Requests: {analysis_results['RQ07_analysis_by_language']['popular_languages']['median_pull_requests']}")
    print(f"            - Mediana de Releases: {analysis_results['RQ07_analysis_by_language']['popular_languages']['median_releases']}")
    print(f"            - Mediana do Tempo desde a Última Atualização (dias): {analysis_results['RQ07_analysis_by_language']['popular_languages']['median_time_since_last_update']}")
    
    print("\n          - Outras Linguagens:")
    print(f"            - Mediana de Pull Requests: {analysis_results['RQ07_analysis_by_language']['other_languages']['median_pull_requests']}")
    print(f"            - Mediana de Releases: {analysis_results['RQ07_analysis_by_language']['other_languages']['median_releases']}")
    print(f"            - Mediana do Tempo desde a Última Atualização (dias): {analysis_results['RQ07_analysis_by_language']['other_languages']['median_time_since_last_update']}")

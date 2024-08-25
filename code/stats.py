import csv

def median(lst):
    n = len(lst)
    s = sorted(lst)
    mid = n // 2
    if n % 2 == 0:
        return (s[mid - 1] + s[mid]) / 2
    else:
        return s[mid]

def analyze_data_from_csv(file_path):
    # Inicializa variáveis para armazenar os valores necessários para cada RQ
    total_age_days = []
    total_pull_requests = []
    total_releases = []
    time_since_last_update = []

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

    # Calcula as medianas para as RQs
    results = {
        'RQ01_median_age': median(total_age_days),
        'RQ02_median_pull_requests': median(total_pull_requests),
        'RQ03_median_releases': median(total_releases),
        'RQ04_median_time_since_update': median(time_since_last_update)
    }

    return results

# Função principal para rodar o script e imprimir os resultados
if __name__ == "__main__":
    file_path = "C:\\Users\\samue\\OneDrive\\Documentos\\Faculdade\\experimentacao-data-extractor\\data-extractor-gitHub\\code\\repos_info.csv"
    analysis_results = analyze_data_from_csv(file_path)
    print(analysis_results)

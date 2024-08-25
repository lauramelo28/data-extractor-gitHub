import requests
import time
import os
import csv
from calculateRQ import format_date, calculate_time_between_dates_in_days, calculate_closed_issues_percentage
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv('.env')

# Obtém o token do GitHub
personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')

# Função para executar a consulta GraphQL
def run_graphql_query(query, variables=None):
    url = "https://api.github.com/graphql"

    headers = {
        "Authorization": f"Bearer {personal_access_token}",
        "Content-Type": "application/json"
    }

    json = {"query": query, "variables": variables}

    retry_attempts = 3
    for attempt in range(retry_attempts):
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if "errors" in result:
                raise Exception(f"Erro no GraphQL: {result['errors']}")
            return result["data"]
        elif response.status_code == 502 and attempt < retry_attempts - 1:
            print(f"Retrying due to 502 error (attempt {attempt + 1})...")
            time.sleep(3)  # Aguarda 3 segundos antes de tentar novamente
        else:
            raise Exception(f"Erro ao executar a query: {response.status_code}, {response.text}")

# Função para obter os repositórios mais populares com base no número de estrelas com paginação
def get_popular_repos(num_repos):
    query = """
    query($number_of_repos_per_request: Int!, $cursor: String) {
        search(query: "stars:>0", type: REPOSITORY, first: $number_of_repos_per_request, after: $cursor) {
            edges {
                node {
                    ... on Repository {
                        name
                        createdAt
                        url
                      
                        stargazers {
                            totalCount
                        }
                        
                        issues(states: CLOSED) {
                            totalCount
                        }
                        
                        pullRequests(states: [OPEN, CLOSED, MERGED]) {
                            totalCount
                        }
                        
                        releases {
                            totalCount
                        }
                        
                        primaryLanguage {
                            name
                        }
                       
                        closedIssues: issues(states: [CLOSED]) {
                            totalCount
                        }
                        
                        totalIssues: issues(states: [OPEN, CLOSED]) {
                            totalCount
                        }
                        
                        defaultBranchRef {
                            name
                            target {
                                ... on Commit {
                                    committedDate
                                }
                            }
                        }
                        
                    }
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """
    
    repos = []
    cursor = None

    while len(repos) < num_repos:
        variables = {"number_of_repos_per_request": 20, "cursor": cursor}
        result = run_graphql_query(query, variables)
        edges = result["search"]["edges"]
        repos.extend(edges)
        
        if not result["search"]["pageInfo"]["hasNextPage"]:
            break
        
        cursor = result["search"]["pageInfo"]["endCursor"]

    # Ordenar repositórios por número de estrelas (decrescente) após a recuperação dos dados
    sorted_repos = sorted(repos, key=lambda r: r["node"]["stargazers"]["totalCount"], reverse=True)

    return sorted_repos[:num_repos]

# Função para coletar e salvar informações dos repositórios em um arquivo .csv
def save_repo_info_to_csv(repos, filename):
    # Obtém o diretório onde o script está localizado
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, filename)
    
    # Define os cabeçalhos para o CSV
    headers = [
        "Index", "Nome do Repository", "URL", "Total de Estrelas", "Data da criacao", "Data da ultima atualizacao",
        "Total de Issues", "Total de Issues Fechadas", "Idade do repositorio (dias)", "Total de Pull Requests",
        "Total de Releases", "Data da ultima atualizacao", "Linguagem primaria", "Percentual de issues fechadas"
    ]

    # Abre o arquivo .csv para escrita
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Escreve os cabeçalhos no arquivo CSV

        # Escreve os dados dos repositórios no arquivo CSV
        for index, repo in enumerate(repos, start=1):
            repo_node = repo["node"]            
            repo_name = repo_node["name"]
            repo_creation_date = format_date(repo["node"]["createdAt"])
            repo_age = calculate_time_between_dates_in_days(repo["node"]["createdAt"])
            repo_number_of_pull_requests = repo["node"]["pullRequests"]["totalCount"]
            
            default_branch = repo_node.get("defaultBranchRef")
            repo_update_date = format_date(default_branch["target"]["committedDate"]) if default_branch else "No data"
            repo_time_since_last_update = calculate_time_between_dates_in_days(repo["node"]["defaultBranchRef"]["target"]["committedDate"])            

            closed_issues = repo["node"]["closedIssues"]["totalCount"]
            total_issues = repo["node"]["totalIssues"]["totalCount"]
            percent_issues_closed =  calculate_closed_issues_percentage(closed_issues, total_issues)
            
            writer.writerow([
                index, repo_name, repo_node['url'], repo_node['stargazers']['totalCount'],
                repo_creation_date, repo_update_date, total_issues, closed_issues,
                repo_age, repo_number_of_pull_requests, repo_node['releases']['totalCount'],
                repo_time_since_last_update,
                repo_node['primaryLanguage']['name'] if repo_node['primaryLanguage'] else 'No primary language',
                f"{percent_issues_closed}%"
            ])

# Main
if __name__ == "__main__":
    num_repos = 1000  # Número de repositórios a serem coletados
    try:
        popular_repos = get_popular_repos(num_repos)
        save_repo_info_to_csv(popular_repos, "repos_info.csv")
    except Exception as e:
        print(e)

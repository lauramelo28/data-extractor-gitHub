import requests
import time
import os
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
        variables = {"number_of_repos_per_request": 10, "cursor": cursor}
        result = run_graphql_query(query, variables)
        edges = result["search"]["edges"]
        repos.extend(edges)
        
        if not result["search"]["pageInfo"]["hasNextPage"]:
            break
        
        cursor = result["search"]["pageInfo"]["endCursor"]

    # Ordenar repositórios por número de estrelas (decrescente) após a recuperação dos dados
    sorted_repos = sorted(repos, key=lambda r: r["node"]["stargazers"]["totalCount"], reverse=True)

    return sorted_repos[:num_repos]

# Função para coletar e salvar informações dos repositórios em um arquivo .txt
def save_repo_info_to_file(repos, filename):
    # Obtém o diretório onde o script está localizado
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, filename)
    
    with open(file_path, "w") as file:
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
            
            file.write(f"#{index} Repositorio: {repo_name}\n")              
            file.write(f"- URL: {repo_node['url']}\n")
            file.write(f"- Total de Estrelas: {repo_node['stargazers']['totalCount']}\n")               
            file.write(f"- Data da criacao: {repo_creation_date}\n")
            file.write(f"- Data da ultima atualizacao: {repo_update_date}\n")
            file.write(f"- Total de Issues: {total_issues}\n")       
            file.write(f"- Total de Issues fechadas: {closed_issues}\n")
            file.write(f"[RQ 01] Idade do repositorio (em dias): {repo_age}\n")
            file.write(f"[RQ 02] Total de pull requests aceitas: {repo_number_of_pull_requests}\n")
            file.write(f"[RQ 03] Total de releases: {repo_node['releases']['totalCount']}\n")
            file.write(f"[RQ 04] Tempo ate a ultima atualizacao (em dias): {repo_time_since_last_update}\n")
            file.write(f"[RQ 05] Linguagem primaria: {repo_node['primaryLanguage']['name'] if repo_node['primaryLanguage'] else 'No primary language'}\n")
            file.write(f"[RQ 06] Percentual de Issues fechadas: {percent_issues_closed}%\n")                
            file.write("-" * 200 + "\n")

# Main
if __name__ == "__main__":
    num_repos = 100  # Número de repositórios a serem coletados
    try:
        popular_repos = get_popular_repos(num_repos)
        save_repo_info_to_file(popular_repos, "repos_info.txt")
    except Exception as e:
        print(e)

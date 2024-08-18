# 📈 Análise de repositorios populares no GitHub - [Lab01S01]

💻Laboratório de Experimentação de Software 

Esse projeto tem como objetivo estudar as principais características de sistemas populares open-source. 
Dessa forma, vamos analisar como eles são desenvolvidos, com que frequência recebem contribuição externa, com qual frequência lançam releases, entre outras características. 
Para tanto, serão coletados os dados indicados para os 1.000 repositórios com maior número de estrelas no GitHub e discuta os valores obtidos.

**Questões de Pesquisa:**

**RQ 01**. Sistemas populares são maduros/antigos?
Métrica: idade do repositório (calculado a partir da data de sua criação)

**RQ 02.** Sistemas populares recebem muita contribuição externa?
Métrica: total de pull requests aceitas

**RQ 03.** Sistemas populares lançam releases com frequência?
Métrica: total de releases

**RQ 04.** Sistemas populares são atualizados com frequência?
Métrica: tempo até a última atualização (calculado a partir da data de última
atualização)

**RQ 05.** Sistemas populares são escritos nas linguagens mais populares?
Métrica: linguagem primária de cada um desses repositórios

**RQ 06.** Sistemas populares possuem um alto percentual de issues fechadas?
Métrica: razão entre número de issues fechadas pelo total de issues Relatório Final:


## 👩🏻‍💻 Alunos:
* Bárbara Mattioly Andrade  
* Laura Enísia Rodrigues Melo
* Samuel Marques Sousa Leal 
 
## 👨‍🏫 Professor:
* João Paulo Carneiro Aramuni

## 💻 Para compilação e execução do sistema:
1. Clone o repositório do projeto;
2. Crie um arquivo .env com a mesma estrutura e no mesmo nível do .env.example. Em seguida gere um token de acesso do github e substitua o PERSONAL_ACCESS_TOKEN.
3. Instale as dependências das bibliotecas usadas como `pip install load_dotenv`, `pip install requests` e `pip install python-dateutil`.
4. Execute o arquivo `main.py`

## 📝 Sobre o projeto:
- O arquivo **main.py** possui as funções principais para executar a consulta em GraphQL, extrair os dados relevantes para o sistema e coletar as informações salvando no arquivo  'repos_info.txt'
- O arquivo **calculateRQ.py** possui funções auxiliares para realizarem cálculos dos RQ's como formatar a data, calcular quantidade de dias entre datas e também calcular a porcentagem de issues fechadas.

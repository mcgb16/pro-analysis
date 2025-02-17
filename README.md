# Análise e Armazenamento de Dados de Esports de League of Legends

Este projeto analisa dados de partidas de esports de League of Legends, calcula pontuações de desempenho do jogador e armazena os resultados em um banco de dados MongoDB. Ele usa dados do OraclesElixir (representados por um arquivo CSV). O objetivo é gerar um ranking dos 10 melhores jogadores das rodadas, por estatística, para posteriormente visualizar o desempenho dos players e das equipes no Power BI, utilizando filtros de Rodadas e Splits.

## Vídeo com a Demonstração do Projeto



## Estrutura do Projeto

O projeto é composto pelos seguintes módulos:

### `main.py`

**Descrição:** Orquestra todo o processo de ETL (Extração, Transformação e Carga).

**Etapas:**

1. **Extração:** Lê os dados das partidas de um arquivo CSV especificado em `extras/info.py`.
2. **Filtragem:** Filtra os dados por liga (CBLOL) e intervalo de datas definido em `extras/info.py`.
3. **Transformação:**
    - Cria DataFrames para análise, incluindo estatísticas individuais dos jogadores.
    - Calcula as classificações dos jogadores e atribui pontuações.
    - Calcula a pontuação de first bloods.
4. **Carga:** Armazena os dados de análise e o ranking dos 10 melhores em um banco de dados MongoDB.
5. **Exportação:** Recupera os dados do MongoDB e os exporta para arquivos CSV para visualização no Power BI.

### `analysis.py`

**Descrição:** Contém as funções principais para análise de dados.

- **`create_top10_dict_list(league_player_analysis_df)`**: 
    - Recebe o DataFrame com as estatísticas dos jogadores.
    - Calcula o ranking dos 10 melhores jogadores para cada métrica.
    - Atribui pontuações com base na classificação.
    - Atualiza a coluna `total_score` no DataFrame original.
    - Retorna uma lista de dicionários, onde cada dicionário representa uma entrada no ranking.

- **`insert_first_blood_score(league_player_analysis_df)`**:
    - Recebe o DataFrame com as estatísticas dos jogadores.
    - Calcula a pontuação de first blood (abate, assistência ou vítima).
    - Adiciona a pontuação à coluna `total_score` no DataFrame.

- **`create_player_analysis_dict_list(league_player_analysis_df)`**:
    - Recebe o DataFrame com as estatísticas dos jogadores.
    - Converte o DataFrame em uma lista de dicionários para facilitar a inserção no MongoDB.
    - Retorna a lista de dicionários.

### `df_generators.py`

**Descrição:** Responsável pela criação e manipulação de DataFrames.

- **`create_lol_dataframe(csv_path)`**: Lê o arquivo CSV e cria um DataFrame.
    - `csv_path`: Caminho para o arquivo CSV.

- **`create_league_dataframe(lol_df, league)`**: Filtra o DataFrame por liga e calcula métricas adicionais (geff, geff team, kp, kda).
    - `lol_df`: DataFrame original.
    - `league`: Nome da liga (ex: "CBLOL").

- **`filter_league_dataframe_by_date(league_df, date_filter)`**: Filtra o DataFrame por uma lista de datas usando expressões regulares.
    - `league_df`: DataFrame da liga.
    - `date_filter`: Lista de strings de data em formato regex.

- **`create_player_analysis_dataframe(league_date_filtered_df, date_filter, round_filter)`**: Cria um DataFrame com estatísticas agregadas por jogador.
    - `league_date_filtered_df`: DataFrame filtrado por data.
    - `date_filter`: Lista de strings de data em formato regex.
    - `round_filter`: String representando a rodada.


- **`create_dataframe_from_list(dict_list)`**: Converte uma lista de dicionários em um DataFrame.
    - `dict_list`: Lista de dicionários.

### `db_conn.py`

**Descrição:** Gerencia a conexão com o banco de dados MongoDB.

- **Conexão:** Usa as credenciais em `extras/info.py` para estabelecer a conexão.
- **`create_top10(top10_list)`**: Insere ou atualiza o ranking dos 10 melhores jogadores.
    - `top10_list`: Lista de dicionários com os dados do ranking.
- **`get_top10()`**:  Recupera o ranking dos 10 melhores jogadores do banco de dados.
- **`create_info_player_record(pl_list)`**: Insere ou atualiza as estatísticas individuais dos jogadores.
    - `pl_list`: Lista de dicionários com as estatísticas dos jogadores.
- **`get_info_player()`**: Recupera as estatísticas individuais dos jogadores do banco de dados.

### `extras/info.py`

**Descrição:** Arquivo de configuração com informações sensíveis (não versionado).

- `string_connection`: String de conexão com o MongoDB.
- `db`: Nome do banco de dados.
- `top10_collection`: Nome da coleção para o ranking dos 10 melhores.
- `player_info_collection`: Nome da coleção para as estatísticas individuais dos jogadores.
- `csv_path`: Caminho para o arquivo CSV contendo os dados das partidas.
- `date_filter_list_split1`: Lista de filtros de data em formato regex, organizados por split.
- `rounds_list`: Lista de rodadas correspondentes aos filtros de data.

## Instruções de Uso

1. Criar um arquivo extras/info.py: Crie um arquivo chamado info.py dentro da pasta extras. Copie o conteúdo abaixo e preencha com suas informações:

```python

string_connection = "SUA_STRING_DE_CONEXÃO_MONGODB"

db = "SEU_BANCO_DE_DADOS"

top10_collection = "SUA_COLECAO_TOP10"

player_info_collection = "SUA_COLECAO_INFO_JOGADOR"

csv_path = "CAMINHO_PARA_O_SEU_CSV"

date_filter_list = [
    ["YYYY-MM-DD"], #Exemplo - Substituir pelas datas relevantes
    ["YYYY-MM-DD", "YYYY-MM-DD", "YYYY-MM-DD"], #Exemplo - Substituir pelas datas relevantes
    ["YYYY-MM-DD", "YYYY-MM-DD"] #Exemplo - Substituir pelas datas relevantes
]

rounds_list = [
    "rodada1", "rodada2", "rodada3" #Exemplo - Substituir pelas rodadas relevantes. Obs: O tamanho dessa lista precisa ser identico ao das datas.
]

```

2. Instalar as Dependências:

``` bash
   pip install -r requirements.txt
# Análise e Armazenamento de Dados de Esports de League of Legends

Este projeto analisa dados de partidas de esports de League of Legends, calcula pontuações de desempenho do jogador e armazena os resultados em um banco de dados MongoDB. Ele usa dados do OraclesElixir (representados por um arquivo CSV). O objetivo é gerar um ranking dos 10 melhores jogadores da semana, por estatística, para posteriormente visualizar o desempenho dos players e das equipes no Power BI, utilizando filtros de Rodadas e Splits.

## Estrutura do Projeto

## Módulos

### `main.py`

O script principal orquestra todo o processo:

1. **Carregamento e Filtragem de Dados:** Carrega os dados da partida de LoL de um arquivo CSV, filtra-os por liga e intervalo de datas.
2. **Transformação de Dados:** Cria vários DataFrames para análise, incluindo estatísticas específicas do jogador.
3. **Análise:** Calcula as classificações dos jogadores com base em diferentes métricas (KDA, DPM, etc.) e atribui pontuações. Também calcula a pontuação de first bloods.
4. **Inserção no Banco de Dados:** Armazena os dados de análise do jogador calculados e as 10 melhores classificações em um banco de dados MongoDB.
5. **Recuperação e Exportação de Dados:** Recupera os dados armazenados do banco de dados e os exporta para arquivos CSV para uso no Power BI.

### `analysis.py`

Este módulo contém as principais funções de análise:

- `create_top10_dict_list()`: Calcula as 10 melhores classificações de jogadores para várias métricas e atribui pontuações com base na classificação. Atualiza o `total_score` no DataFrame.
- `insert_first_blood_score()`: Calcula e adiciona uma pontuação com base na participação no primeiro sangue (abate, assistência ou vítima).
- `create_player_analysis_dict_list()`: Converte o DataFrame de análise do jogador em uma lista de dicionários para inserção no banco de dados.

### `df_generators.py`

Este módulo lida com a criação e manipulação de DataFrame:

- `create_lol_dataframe()`: Carrega os dados CSV em um DataFrame do Pandas.
- `create_league_dataframe()`: Filtra o DataFrame por liga e calcula métricas adicionais (por exemplo, geff, geff team, kp, kda).
- `filter_league_dataframe_by_date()`: Filtra o DataFrame por uma lista de datas.
- `create_player_analysis_dataframe()`: Cria um DataFrame com estatísticas agregadas do jogador, pronto para análise. Solicita ao usuário o número da rodada.
- `create_dataframe_from_list()`: Cria um DataFrame a partir de uma lista de dicionários.


### `db_conn.py`

Este módulo gerencia a conexão e as operações do banco de dados:

- Estabelece uma conexão com um banco de dados MongoDB usando credenciais armazenadas em `extras/info.py`.
- `create_top10()`: Insere ou atualiza as 10 melhores classificações de jogadores no banco de dados.
- `get_top10()`: Recupera as 10 melhores classificações do banco de dados com base na divisão (split).
- `create_info_player_record()`: Insere ou atualiza os dados de análise do jogador no banco de dados.
- `get_info_player()`: Recupera os dados de análise do jogador do banco de dados com base na divisão (split).

### `extras/info.py`

Este arquivo (não incluído no repositório) contém informações confidenciais:

```python
string_connection = "sua_string_de_conexão_mongodb"
db = "seu_nome_do_banco_de_dados"
top10_collection = "seu_nome_da_coleção_top10"
player_info_collection = "seu_nome_da_coleção_player_info"
# Cofre Digital de Documentos Financeiros

Este projeto foi desenvolvido para a disciplina de **Desenvolvimento de Software para Persistência**.

A proposta foi criar um cofre digital capaz de armazenar e organizar documentos financeiros, mantendo tanto os arquivos quanto seus metadados de forma persistente.

## Equipe

- André Cayare
- Antonio Kaynandeson
- Iarly Batista

## Tema

**Tema 10 — Cofre de Documentos Financeiros**

O sistema foi pensado para trabalhar com documentos relacionados à área financeira, como:

- notas fiscais;
- recibos;
- comprovantes;
- relatórios financeiros;
- planilhas;
- documentos de pagamento.

## Objetivo

O objetivo do projeto é permitir o cadastro e gerenciamento de documentos financeiros por meio de uma API desenvolvida com FastAPI.

Além de armazenar os arquivos, o sistema também permite consultar documentos, realizar downloads, atualizar dados, excluir registros, verificar integridade, gerar estatísticas, exportar dados em CSV e criar backups.

## Requisitos

Para executar o projeto é necessário ter:

- Python instalado;
- pip;
- dependências do arquivo `requirements.txt`.

## Bibliotecas utilizadas

As principais bibliotecas utilizadas foram:

- FastAPI;
- Pydantic;
- Uvicorn;
- PyYAML;
- python-multipart.

O `python-multipart` é utilizado para permitir o envio de arquivos e dados de formulário pela API.

Também utilizamos módulos nativos do Python, como `json`, `csv`, `hashlib`, `logging`, `zipfile`, `pathlib` e `xml.etree.ElementTree`.

## Instalação

Dentro da pasta do projeto, execute:

```bash
pip install -r requirements.txt
```

## Execução

Para iniciar a aplicação:

```bash
uvicorn main:app --reload
```

Depois, acesse a documentação interativa da API em:

```text
http://127.0.0.1:8000/docs
```

## Estrutura do projeto

```text
core/            Configuração de logging
data/            Arquivos, metadados e exportações
models/          Modelo dos documentos
routes/          Rotas da API
services/        Funções de persistência, CSV e backup
storage/backups/ Backups gerados
logging.yaml     Configuração externa
main.py          Arquivo principal da aplicação
```

## Metadados

Cada documento possui informações gerais, como:

- ID;
- nome original;
- nome armazenado;
- extensão;
- tipo MIME;
- tamanho;
- categoria;
- descrição;
- data de upload;
- hash SHA-256.

Como o tema do projeto é financeiro, também foram adicionados:

- tipo do documento;
- competência;
- valor;
- centro de custo;
- responsável.

## Principais endpoints

| Método | Endpoint | Função |
|---|---|---|
| POST | `/documentos` | Cadastrar documento |
| GET | `/documentos` | Listar e filtrar documentos |
| GET | `/documentos/{id}` | Buscar documento por ID |
| GET | `/documentos/{id}/download` | Baixar arquivo |
| PUT | `/documentos/{id}` | Atualizar metadados |
| DELETE | `/documentos/{id}` | Excluir documento |
| GET | `/documentos/{id}/integridade` | Verificar integridade de um arquivo |
| GET | `/documentos/estatisticas` | Consultar estatísticas |
| GET | `/integridade` | Verificar integridade de todos os arquivos |
| GET | `/exportar/csv` | Exportar os dados para CSV |
| POST | `/backup` | Criar backup |
| GET | `/backups` | Listar backups |

## Exemplo de cadastro

Um documento pode ser cadastrado pelo endpoint:

```text
POST /documentos
```

Exemplo:

```text
arquivo: nota_fiscal.pdf
categoria: nota_fiscal
descricao: Nota fiscal referente à compra de equipamentos
tipo: Nota Fiscal
competencia: 2026-10
valor: 1500.00
centro_de_custo: TI
responsavel: Iarly Batista
```

O arquivo é salvo em `data/arquivos/` e seus metadados são armazenados em `data/documentos.json`.

## Filtros

Os documentos podem ser filtrados por:

- extensão;
- competência;
- centro de custo.

Exemplo:

```text
GET /documentos?extensao=.pdf&competencia=2026-10&centro_de_custo=TI
```

## Funcionalidade específica do tema

A funcionalidade específica do Tema 10 foi a geração de estatísticas dos documentos considerando:

- competência;
- categoria;
- centro de custo.

Essas informações podem ser consultadas em:

```text
GET /documentos/estatisticas
```

Além disso, o sistema também mostra dados como quantidade total de documentos, tamanho ocupado, quantidade por extensão e valor total.

## Integridade dos arquivos

No momento do upload, o sistema calcula o hash SHA-256 do arquivo.

Depois, pelo endpoint:

```text
GET /documentos/{id}/integridade
```

o sistema recalcula o hash e compara com o valor original.

Dessa forma, é possível identificar se o arquivo foi alterado depois de ser cadastrado.

## CSV, configuração e backup

Os dados podem ser exportados em CSV através de:

```text
GET /exportar/csv
```

O arquivo `logging.yaml` é utilizado para configurar o sistema de logs.

Os backups são gerados em formato ZIP através de:

```text
POST /backup
```

e ficam armazenados em:

```text
storage/backups/
```

Os backups existentes podem ser consultados por:

```text
GET /backups
```

## Tratamento de erros

A aplicação também trata situações como:

- documento inexistente;
- arquivo físico não encontrado;
- XML inválido;
- JSON inválido;
- upload inválido;
- configuração YAML inexistente ou inválida;
- dados inválidos.

Dependendo da situação, a API retorna códigos como `400`, `404`, `422` e `500`.
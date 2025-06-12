# PIIXtractor

Ferramenta simples para extração de informações pessoais de arquivos de texto,
PDF, planilhas ou documentos Word. Utiliza expressões regulares e, quando
necessário, a API da OpenAI para classificar trechos de texto.

### Requisitos

- Python 3.10 ou superior

### Instalação

Recomenda-se utilizar um ambiente virtual. Execute os comandos abaixo:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Uso

1. Coloque o arquivo ZIP contendo os documentos no mesmo diretório.
2. Defina a variável de ambiente `OPENAI_API_KEY` com sua chave.
3. Execute o script `extractor_drive.py` para processar o ZIP e salvar os dados
   ou utilize as funções diretamente em seu próprio código:

```bash
python extractor_drive.py
```

Exemplo de uso das funções programaticamente:

```python
from pii_extractor import extrair_e_processar_zip
from extractor.exporters import export_csv, export_json, export_sqlite

resultados = extrair_e_processar_zip("meu_arquivo.zip")
export_csv(resultados)
export_json(resultados)
export_sqlite(resultados)
```

Durante o processamento será exibida uma barra de progresso indicando o avanço.
Ao final, os resultados são exportados para arquivos CSV, JSON e SQLite. Todo o
conteúdo temporário é extraído no diretório `tmp/`, que é removido
automaticamente após a exportação.

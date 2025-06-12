# PIIXtractor

Ferramenta simples para extração de informações pessoais de arquivos de texto,
PDF, planilhas ou documentos Word. Utiliza expressões regulares e, quando
necessário, a API da OpenAI para classificar trechos de texto.

### Uso

1. Coloque o arquivo ZIP contendo os documentos no mesmo diretório.
2. Defina a variável de ambiente `OPENAI_API_KEY` com sua chave.
3. Execute o script `extractor_drive.py` para processar o ZIP e salvar os dados:

```bash
python extractor_drive.py
```

Durante o processamento será exibida uma barra de progresso indicando o avanço.
Ao final, os resultados são exportados para arquivos CSV, JSON e SQLite. Todo o
conteúdo temporário é extraído no diretório `tmp/`, que é removido
automaticamente após a exportação.

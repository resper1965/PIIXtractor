import os
import logging
import time
from typing import List

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_TEMPLATE = (
    "Extraia todos os dados pessoais (nome, CPF, CNPJ, e-mail, telefone, endereco, "
    "data de nascimento) do texto abaixo e retorne um JSON com os campos detectados "
    "e seus respectivos valores.\n\nTexto:\n\"\"\"{chunk}\"\"\""
)


def _classify_chunk(chunk: str, max_retries: int = 3) -> str:
    """Send a single chunk to the OpenAI API with retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(chunk=chunk)}],
                temperature=0.0,
                max_tokens=800,
            )
            return response.choices[0].message.content
        except Exception as exc:
            logging.warning("[OpenAI] tentativa %s falhou: %s", attempt, exc)
            if attempt < max_retries:
                wait = attempt * 2
                logging.info("Aguardando %ss para nova tentativa", wait)
                time.sleep(wait)
            else:
                logging.error("[OpenAI] Limite de tentativas atingido")
    return ""


def classify_text(text: str, chunk_size: int = 12000) -> str:
    """Break the text into chunks and classify each chunk."""
    results: List[str] = []
    for idx in range(0, len(text), chunk_size):
        chunk = text[idx:idx + chunk_size]
        logging.info("Classificando bloco %s", idx // chunk_size + 1)
        result = _classify_chunk(chunk)
        if result:
            results.append(result)
        time.sleep(1)
    return "\n".join(results)

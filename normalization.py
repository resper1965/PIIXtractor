"""Utilities for normalizing extracted PII results."""

from typing import Dict, Any


def normalize_results(resultados: Dict[str, Any]) -> Dict[str, Any]:
    """Return a new dict with duplicates removed and values sorted.

    Iterates over the nested results structure produced by ``processar_diretorio``
    and ensures each list of extracted values is converted to a ``set`` to remove
    duplicates and then sorted.
    """
    normalizados: Dict[str, Any] = {}
    for arquivo, dados in resultados.items():
        arquivo_dict: Dict[str, Any] = {}
        for origem, info in dados.items():
            if isinstance(info, dict):
                origem_dict: Dict[str, Any] = {}
                for tipo, valores in info.items():
                    if isinstance(valores, list):
                        origem_dict[tipo] = sorted(set(valores))
                    else:
                        origem_dict[tipo] = valores
                arquivo_dict[origem] = origem_dict
            else:
                arquivo_dict[origem] = info
        normalizados[arquivo] = arquivo_dict
    return normalizados

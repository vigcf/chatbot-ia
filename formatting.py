from typing import List

from sources.base import Documento


class FormatadorDeContexto:
    """Transforma uma lista de documentos em um único texto para o prompt."""

    @staticmethod
    def formatar(documentos: List[Documento]) -> str:
        blocos = (
            f"Arquivo: {doc.fonte}\n"
            f"Localização: {doc.localizacao}\n\n"
            f"{doc.conteudo}\n"
            for doc in documentos
        )
        return "\n".join(blocos)

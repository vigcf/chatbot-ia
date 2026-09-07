from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Documento:
    """Um trecho de conteúdo extraído de uma fonte (ex.: página de PDF, trecho de transcrição)."""
    fonte: str
    localizacao: str
    conteudo: str


class FonteDeDocumentos(ABC):
    """Interface para qualquer fonte capaz de fornecer documentos ao agente.

    Novas fontes (YouTube, site, etc.) devem implementar esta interface,
    sem exigir alterações em quem já consome FonteDeDocumentos.
    """

    @abstractmethod
    def carregar(self) -> List[Documento]:
        """Retorna a lista de documentos extraídos desta fonte."""
        raise NotImplementedError

import re
from typing import List, Optional

from youtube_transcript_api import YouTubeTranscriptApi

from sources.base import Documento, FonteDeDocumentos

_PADROES_ID_VIDEO = [
    r"(?:v=|/)([0-9A-Za-z_-]{11})",
    r"youtu\.be/([0-9A-Za-z_-]{11})",
]


class FonteYoutube(FonteDeDocumentos):
    """Carrega a transcrição de um vídeo do YouTube a partir da sua URL."""

    def __init__(self, url: str, idiomas: Optional[List[str]] = None):
        self._url = url
        self._idiomas = idiomas or ["pt", "pt-BR", "en"]

    def carregar(self) -> List[Documento]:
        print(f"Carregando transcrição: {self._url}")

        video_id = self._extrair_video_id(self._url)
        transcricao = YouTubeTranscriptApi().fetch(video_id, languages=self._idiomas)
        texto = " ".join(trecho.text for trecho in transcricao)

        if not texto.strip():
            raise RuntimeError(f"Não foi possível obter a transcrição do vídeo: {self._url}")

        return [
            Documento(
                fonte=self._url,
                localizacao="transcrição do vídeo",
                conteudo=texto,
            )
        ]

    @staticmethod
    def _extrair_video_id(url: str) -> str:
        for padrao in _PADROES_ID_VIDEO:
            correspondencia = re.search(padrao, url)
            if correspondencia:
                return correspondencia.group(1)
        raise ValueError(f"Não foi possível identificar o ID do vídeo na URL: {url}")

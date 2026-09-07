from typing import List

from langchain_community.document_loaders import WebBaseLoader

from sources.base import Documento, FonteDeDocumentos


class FonteSite(FonteDeDocumentos):
    """Carrega o conteúdo textual de uma página web a partir da sua URL."""

    def __init__(self, url: str):
        self._url = url

    def carregar(self) -> List[Documento]:
        print(f"Carregando site: {self._url}")

        paginas = WebBaseLoader(self._url).load()

        if not paginas:
            raise RuntimeError(f"Não foi possível carregar o conteúdo de: {self._url}")

        return [
            Documento(
                fonte=self._url,
                localizacao="conteúdo do site",
                conteudo=pagina.page_content,
            )
            for pagina in paginas
        ]

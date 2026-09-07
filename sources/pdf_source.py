from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader

from sources.base import Documento, FonteDeDocumentos


class FontePdf(FonteDeDocumentos):
    """Carrega todos os PDFs de uma pasta como documentos."""

    def __init__(self, pasta: Path):
        self._pasta = pasta

    def carregar(self) -> List[Documento]:
        arquivos_pdf = self._listar_pdfs()

        if not arquivos_pdf:
            raise RuntimeError(f"Nenhum PDF foi encontrado em: {self._pasta}")

        documentos: List[Documento] = []
        for arquivo in arquivos_pdf:
            print(f"Lendo: {arquivo.name}")
            documentos.extend(self._carregar_arquivo(arquivo))

        return documentos

    def _listar_pdfs(self) -> List[Path]:
        if not self._pasta.exists():
            raise RuntimeError(f"A pasta de PDFs não foi encontrada em: {self._pasta}")

        return sorted(
            arquivo
            for arquivo in self._pasta.iterdir()
            if arquivo.is_file() and arquivo.suffix.lower() == ".pdf"
        )

    @staticmethod
    def _carregar_arquivo(arquivo: Path) -> List[Documento]:
        paginas = PyPDFLoader(str(arquivo)).load()
        return [
            Documento(
                fonte=arquivo.name,
                localizacao=f"página {pagina.metadata.get('page', 0) + 1}",
                conteudo=pagina.page_content,
            )
            for pagina in paginas
        ]

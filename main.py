import sys
from pathlib import Path
from typing import List

from cli import SessaoDeChat
from formatting import FormatadorDeContexto
from modelo import criar_modelo_chat
from qa_agent import AgenteDeQA
from sources.base import Documento, FonteDeDocumentos
from sources.pdf_source import FontePdf
from sources.site_source import FonteSite
from sources.youtube_source import FonteYoutube

_TEXTO_SELECAO = """
Digite 1 se você quiser conversar com um site
Digite 2 se você quiser conversar com um PDF
Digite 3 se você quiser conversar com um vídeo do YouTube
"""


def configurar_encoding_console() -> None:
    """Evita erros ao exibir no console caracteres fora da codificação padrão do Windows."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")


def _criar_fonte_site() -> FonteDeDocumentos:
    url = input("Digite a URL do site: ").strip()
    return FonteSite(url)


def _criar_fonte_pdf() -> FonteDeDocumentos:
    pasta_projeto = Path(__file__).resolve().parent
    pasta_arquivos = pasta_projeto / "arquivos"
    return FontePdf(pasta_arquivos)


def _criar_fonte_youtube() -> FonteDeDocumentos:
    url = input("Digite a URL do vídeo: ").strip()
    return FonteYoutube(url)


_CRIADORES_DE_FONTE = {
    "1": _criar_fonte_site,
    "2": _criar_fonte_pdf,
    "3": _criar_fonte_youtube,
}


def montar_fontes() -> List[FonteDeDocumentos]:
    """Pergunta ao usuário com qual tipo de fonte ele quer conversar.

    Para adicionar uma nova opção, basta criar a classe implementando
    FonteDeDocumentos e registrá-la em _CRIADORES_DE_FONTE.
    """
    while True:
        selecao = input(_TEXTO_SELECAO).strip()
        criar_fonte = _CRIADORES_DE_FONTE.get(selecao)

        if criar_fonte:
            return [criar_fonte()]

        print("Digite um valor entre 1 e 3.")


def carregar_documentos(fontes: List[FonteDeDocumentos]) -> List[Documento]:
    documentos: List[Documento] = []
    for fonte in fontes:
        documentos.extend(fonte.carregar())
    return documentos


def main() -> None:
    configurar_encoding_console()

    fontes = montar_fontes()
    documentos = carregar_documentos(fontes)

    print()
    print(f"Documentos carregados: {len(documentos)}")

    contexto = FormatadorDeContexto.formatar(documentos)

    agente = AgenteDeQA(criar_modelo_chat())
    SessaoDeChat(agente, contexto).iniciar()


if __name__ == "__main__":
    main()

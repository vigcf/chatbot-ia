import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

_VARIAVEL_API_KEY = "GROQ_API_KEY"
_NOME_MODELO = "openai/gpt-oss-120b"


def _obter_api_key() -> str:
    api_key = os.environ.get(_VARIAVEL_API_KEY)

    if not api_key:
        raise RuntimeError(
            f"Variável de ambiente '{_VARIAVEL_API_KEY}' não foi definida. "
            "Crie um arquivo .env na raiz do projeto com "
            f"{_VARIAVEL_API_KEY}=<sua_chave>, ou defina a variável no sistema."
        )

    return api_key


def criar_modelo_chat() -> ChatGroq:
    return ChatGroq(model=_NOME_MODELO, api_key=_obter_api_key())

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

_PROMPT_SISTEMA = """
Você é um assistente amigável especializado em responder
perguntas sobre documentos.

Responda utilizando somente as informações fornecidas abaixo.

Se a resposta não estiver nas informações, responda:
"Não encontrei essa informação nos documentos."

Informações disponíveis:

{informacoes}
"""


class AgenteDeQA:
    """Responde perguntas com base em um contexto de documentos, usando um modelo de chat."""

    def __init__(self, modelo: BaseChatModel):
        template = ChatPromptTemplate.from_messages([
            ("system", _PROMPT_SISTEMA),
            ("user", "{input}"),
        ])
        self._chain = template | modelo

    def responder(self, pergunta: str, contexto: str) -> str:
        resposta = self._chain.invoke({
            "informacoes": contexto,
            "input": pergunta,
        })
        return resposta.content

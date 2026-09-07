from qa_agent import AgenteDeQA

_COMANDO_SAIR = "sair"


class SessaoDeChat:
    """Interface de linha de comando para conversar com um AgenteDeQA."""

    def __init__(self, agente: AgenteDeQA, contexto: str):
        self._agente = agente
        self._contexto = contexto

    def iniciar(self) -> None:
        while True:
            pergunta = self._ler_pergunta()

            if pergunta.lower() == _COMANDO_SAIR:
                print("Programa encerrado.")
                break

            if not pergunta:
                print("Digite uma pergunta.")
                continue

            self._responder(pergunta)

    @staticmethod
    def _ler_pergunta() -> str:
        return input(f"\nDigite uma pergunta ou digite '{_COMANDO_SAIR}': ").strip()

    def _responder(self, pergunta: str) -> None:
        try:
            resposta = self._agente.responder(pergunta, self._contexto)
            print("\nResposta:")
            print(resposta)
        except Exception as erro:
            print("\nNão foi possível consultar o modelo.")
            print(f"Erro: {erro}")

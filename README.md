# chatbot-ia

Agente de IA que responde perguntas sobre um **site**, um **PDF** ou a **transcrição de um vídeo do YouTube**, escolhidos pelo usuário no início da execução.

## Objetivo

Construir um chatbot de linha de comando que:

1. Carrega o conteúdo de uma fonte externa (site, PDF ou vídeo do YouTube);
2. Usa esse conteúdo como contexto para um LLM;
3. Responde perguntas do usuário **somente** com base nesse conteúdo — se a informação não estiver lá, o agente admite que não sabe, em vez de inventar (mitiga alucinação).

## Como funciona

O fluxo é sempre o mesmo, independentemente da fonte escolhida:

```
usuário escolhe a fonte (1-site / 2-PDF / 3-YouTube)
        │
        ▼
a fonte carrega o conteúdo e vira texto
        │
        ▼
o texto entra no prompt como contexto
        │
        ▼
loop: usuário pergunta → modelo responde com base no contexto
```

### Arquitetura do código

O projeto é dividido em módulos com responsabilidade única, seguindo os princípios **SOLID** — em especial o **Open/Closed**: para adicionar uma nova fonte de conteúdo (ex.: um arquivo `.docx`, uma planilha), basta criar uma nova classe, sem alterar o que já existe.

```
main.py                    → orquestra: menu → carregar fonte → montar agente → iniciar chat
modelo.py                  → cria o modelo de chat (ChatGroq), lê a chave do .env
qa_agent.py                → AgenteDeQA: monta o prompt e chama o modelo
formatting.py              → FormatadorDeContexto: transforma os documentos em texto único
cli.py                     → SessaoDeChat: loop de pergunta/resposta no terminal
sources/base.py            → Documento (dataclass) + interface FonteDeDocumentos
sources/pdf_source.py      → FontePdf     (usa PyPDFLoader)
sources/site_source.py     → FonteSite    (usa WebBaseLoader)
sources/youtube_source.py  → FonteYoutube (usa youtube_transcript_api)
```

Todas as fontes implementam a mesma interface (`FonteDeDocumentos.carregar()`), então `main.py` não precisa saber como cada uma funciona por dentro — ele só pede a lista de `Documento` e segue o fluxo.

## Tecnologias utilizadas

- **[Python 3.13](https://www.python.org/)**
- **[LangChain](https://www.langchain.com/)** (`langchain`, `langchain-community`) — orquestração do prompt e dos *document loaders*
- **[LangChain Groq](https://python.langchain.com/docs/integrations/chat/groq/)** (`langchain-groq`) — integração com o modelo de chat
- **[Groq](https://groq.com/)** — provedor de inferência do LLM (modelo `openai/gpt-oss-120b`)
- **[pypdf](https://pypdf.readthedocs.io/)** — extração de texto de PDFs
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** — parsing de HTML (usado pelo `WebBaseLoader`)
- **[youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)** — obtenção da transcrição de vídeos do YouTube
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — carregamento de variáveis de ambiente a partir de um `.env`

## LangChain

Conceitos centrais do LangChain utilizados no projeto:

**1. Document Loaders** — colocar conteúdo externo dentro de um prompt parece trivial (ler um texto e jogar numa string), mas cada fonte tem seu próprio formato: um PDF tem páginas e metadados, um site tem HTML cheio de ruído (menus, scripts, tags), um vídeo não tem texto nenhum, só uma legenda cronometrada. O LangChain padroniza tudo isso na mesma interface — um objeto `Document` com `page_content` e `metadata` — independentemente de a origem ser um PDF ou uma página web. Essa é a ideia por trás da interface `FonteDeDocumentos` deste projeto: a mesma abstração do LangChain, adaptada e simplificada para este caso de uso.

**2. Chains (correntes) e o operador `|`** — no LangChain, um "chain" é a composição de passos: prompt → modelo → (opcionalmente) parser de saída. A sintaxe `template | chat` (usada em `qa_agent.py`) vem do LangChain sobrecarregando o operador `|` (via **LCEL** — *LangChain Expression Language*) para encadear componentes, de forma análoga a um pipe do Unix. O prompt formatado vira a entrada do modelo, e o `.invoke()` executa a corrente inteira de uma vez.

Na prática, o motivo de usar LangChain em vez de chamar a API da Groq diretamente foi justamente esse: ele abstrai tanto a **origem do conteúdo** (document loaders) quanto o **provedor do modelo** (`ChatGroq`, `ChatOpenAI`, `ChatAnthropic`... todos com a mesma interface `BaseChatModel`). Trocar de Groq para outro provedor, por exemplo, seria alterar só o `modelo.py` — o resto do código (`qa_agent.py`, `cli.py`, `formatting.py`) não muda, porque depende da abstração (`BaseChatModel`), não da implementação concreta. É o mesmo princípio de inversão de dependência (SOLID) aplicado pela própria biblioteca.

## Como rodar

### Pré-requisitos

- Python 3.10+
- Uma chave de API da [Groq](https://console.groq.com/keys) (gratuita)

### Passo a passo

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd chatbot-ia

# 2. Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a chave da API
copy .env.example .env       # Windows
cp .env.example .env         # Linux/Mac
# depois edite o .env e coloque sua chave: GROQ_API_KEY=sua_chave_aqui

# 5. Rode o agente
python main.py
```

Ao rodar, escolha a fonte (site, PDF ou YouTube) e comece a fazer perguntas. Digite `sair` para encerrar.

> Para a opção de PDF, os arquivos devem estar na pasta `arquivos/` na raiz do projeto.

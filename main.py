import requests
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS para permitir todos os origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos os origens, você pode limitar para específicos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Substitua com seu token de acesso da API Autentique
ACCESS_TOKEN = "seu_token_de_acesso"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

API_URL = "https://api.autentique.com.br/v2/graphql"

# rota home
@app.get("/", tags=["Home"])
async def home():
    return {"message": "Bem-vindo à API do autentique usando Python"}

# endpoint de produção para criar documento
@app.post("/criar-documento/", tags=["Produção"])
async def criar_documento(
    nome_documento: str = Form(...), 
    mensagem_documento: str = Form(...), 
    email_signatario: str = Form(...), 
    file: UploadFile = File(...)
):
    operations = {
        "query": """
            mutation CreateDocumentMutation(
              $document: DocumentInput!,
              $signers: [SignerInput!]!,
              $file: Upload!
            ) {
              createDocument(
                document: $document,
                signers: $signers,
                file: $file
              ) {
                id
                name
                refusable
                sortable
                created_at
                signatures {
                  public_id
                  name
                  email
                  created_at
                  action { name }
                  link { short_link }
                  user { id name email }
                }
              }
            }
        """,
        "variables": {
            "document": {
                "name": nome_documento,
                "message": mensagem_documento,
                "ignore_cpf": True,
                "cc": [{"email": "etc.juca@gmail.com"}]
            },
            "signers": [{
                "email": email_signatario,
                "action": "SIGN",
            }],
            "file": None
        }
    }

    map = {"file": ["variables.file"]}

    files = {
        'operations': (None, json.dumps(operations), 'application/json'),
        'map': (None, json.dumps(map), 'application/json'),
        'file': (file.filename, file.file, file.content_type)
    }

    response = requests.post(API_URL, headers=HEADERS, files=files)

    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# endpoint de produção para resgatar documento
@app.post("/resgatar-documento/", tags=["Produção"])
async def resgatar_documento(id_documento: str = Form(...)):
    query = """
    query {
        document(id: \"ID_DO_DOCUMENTO\") {
            id name refusable sortable created_at
            files { original signed }
            signatures {
                public_id name email created_at action { name }
                link { short_link }
                user { id name email }
                email_events { sent opened delivered refused reason }
                viewed { ...event }
                signed { ...event }
                rejected { ...event }
            }
        }
    }
    fragment event on Event {
        ip port reason created_at
        geolocation { country countryISO state stateISO city zipcode latitude longitude }
    }
    """
    query = query.replace("ID_DO_DOCUMENTO", id_documento)
    response = requests.post(API_URL, headers=HEADERS, json={"query": query})

    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# endpoint de produção para listar documentos
@app.post("/listar-documentos/", tags=["Produção"])
async def listar_documentos():
    query = """
    query {
        documents(limit: 60, page: 1) {
            total data {
                id name refusable sortable created_at
                signatures {
                    public_id name email created_at action { name }
                    link { short_link }
                    user { id name email }
                    viewed { created_at }
                    signed { created_at }
                    rejected { created_at }
                }
                files { original signed }
            }
        }
    }
    """
    response = requests.post(API_URL, headers=HEADERS, json={"query": query})

    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# endpoint de produção para excluir documento
@app.post("/excluir-documento/", tags=["Produção"])
async def excluir_documento(id_documento: str = Form(...)):
    query = """
    mutation {
        deleteDocument(id: \"ID_DO_DOCUMENTO\")
    }
    """
    query = query.replace("ID_DO_DOCUMENTO", id_documento)
    response = requests.post(API_URL, headers=HEADERS, json={"query": query})

    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# endpoint de teste para criar documento em ambiente de sandbox
@app.post("/teste/criar-documento/", tags=["Testes"])
async def criar_documento_teste(
    nome_documento: str = Form(...), 
    mensagem_documento: str = Form(...), 
    email_signatario: str = Form(...), 
    file: UploadFile = File(...)
):
    operations = {
        "query": """
            mutation CreateDocumentMutation(
              $document: DocumentInput!,
              $signers: [SignerInput!]!,
              $file: Upload!
            ) {
              createDocument(
                document: $document,
                sandbox: true,
                signers: $signers,
                file: $file
              ) {
                id
                name
                refusable
                sortable
                created_at
                signatures {
                  public_id
                  name
                  email
                  created_at
                  action { name }
                  link { short_link }
                  user { id name email }
                }
              }
            }
        """,
        "variables": {
            "document": {
                "name": nome_documento,
                "message": mensagem_documento,
                "ignore_cpf": True,
            },
            "signers": [{
                "email": email_signatario,
                "action": "SIGN",
            }],
            "file": None
        }
    }

    map = {"file": ["variables.file"]}

    files = {
        'operations': (None, json.dumps(operations), 'application/json'),
        'map': (None, json.dumps(map), 'application/json'),
        'file': (file.filename, file.file, file.content_type)
    }

    response = requests.post(API_URL, headers=HEADERS, files=files)

    if response.status_code == 200:
        return JSONResponse(content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

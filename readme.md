# Documentação da API Autentique Python

## Introdução

Esta é a documentação da API Autentique usando python, que permite a criação, consulta, listagem e exclusão de documentos digitalmente assinados. Utilize esta API para integrar funcionalidades de assinatura digital em seus projetos.

## Autenticação

Para utilizar a API Autentique, você precisa de um token de acesso válido. Substitua `ACCESS_TOKEN` no cabeçalho `Authorization` com seu token obtido através do painel de administração da Autentique.

```python
import requests

ACCESS_TOKEN = "seu_token_de_acesso"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
```

## Endpoints Disponíveis

Você pode usar a documentação do FastAPI para testar ou Endpoint: http://localhost:8000/docs

### 1. Criar Documento

Endpoint para criar um novo documento no Autentique.

- **URL:** `/criar-documento/`
- **Método:** `POST`
- **Parâmetros:**
  - `nome_documento`: Nome do documento.
  - `mensagem_documento`: Mensagem associada ao documento.
  - `email_signatario`: E-mail do signatário.
  - `file`: Arquivo a ser assinado (upload).

Exemplo de uso via terminal:

```bash
curl -X POST \
  -F "nome_documento=Contrato de Serviços" \
  -F "mensagem_documento=Por favor, assine este contrato." \
  -F "email_signatario=exemplo@email.com" \
  -F "file=@/path/do/arquivo.pdf" \
  -H "Authorization: Bearer seu_token_de_acesso" \
  http://localhost:8000/criar-documento/
```

### 2. Resgatar Documento

Endpoint para consultar informações detalhadas de um documento existente.

- **URL:** `/resgatar-documento/`
- **Método:** `POST`
- **Parâmetros:**
  - `id_documento`: ID do documento a ser consultado.

Exemplo de uso via terminal:

```bash
curl -X POST \
  -F "id_documento=ID_DO_DOCUMENTO" \
  -H "Authorization: Bearer seu_token_de_acesso" \
  http://localhost:8000/resgatar-documento/
```

### 3. Listar Documentos

Endpoint para listar todos os documentos existentes.

- **URL:** `/listar-documentos/`
- **Método:** `POST`

Exemplo de uso via terminal:

```bash
curl -X POST \
  -H "Authorization: Bearer seu_token_de_acesso" \
  http://localhost:8000/listar-documentos/
```

### 4. Excluir Documento

Endpoint para excluir um documento existente.

- **URL:** `/excluir-documento/`
- **Método:** `POST`
- **Parâmetros:**
  - `id_documento`: ID do documento a ser excluído.

Exemplo de uso via terminal:

```bash
curl -X POST \
  -F "id_documento=ID_DO_DOCUMENTO" \
  -H "Authorization: Bearer seu_token_de_acesso" \
  http://localhost:8000/excluir-documento/
```

## Considerações Finais

Utilize os endpoints fornecidos para integrar facilmente a funcionalidade de assinatura digital do Autentique em seus sistemas. Certifique-se de gerenciar adequadamente seus tokens de acesso e tratar as respostas da API conforme necessário.

---

Esta documentação fornece uma visão geral dos endpoints disponíveis e como utilizá-los na integração com a API Autentique.

Em caso de duvidas sobre a API entre em contato pelo e-mail: etc.juca@gmail.com

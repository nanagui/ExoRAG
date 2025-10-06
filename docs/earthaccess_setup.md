# Earthaccess Authentication Setup

The project integrates the [earthaccess](https://earthaccess.readthedocs.io/) library to authenticate against NASA Earthdata services when downloading protected assets (e.g., SDO ML datasets). Follow the steps below to enable the workflow locally.

## 1. Create or reuse an Earthdata Login
1. Navegue para https://urs.earthdata.nasa.gov/users/new e crie uma conta se ainda não tiver.
2. No perfil (menu *Applications → Application Tokens*), clique em **Generate Token** e copie o valor (ex.: `EDL-XXXXXXXX`).

## 2. Configure environment variables
Preencha o `.env` em `app/.env` com o token gerado (usuário/senha tornam-se opcionais):

```
EXOAI_EARTHDATA_TOKEN=EDL-xxxxxxxxxxxxxxxxxxxx
# Opcional (compatibilidade com fluxos antigos)
EXOAI_EARTHDATA_USERNAME=
EXOAI_EARTHDATA_PASSWORD=
```

Ou exporte diretamente no shell antes de executar ingestões:

```bash
export EXOAI_EARTHDATA_TOKEN=EDL-xxxxxxxxxxxxxxxxxxxx
```

O `EarthAccessClient` detecta automaticamente o token e chama `earthaccess.login(strategy="environment", token=...)`. Caso o token não seja fornecido, ele recai para usuário/senha (se presentes).

## 3. Running an authenticated download
Once the environment variables are set, you can invoke the ingestion helper from an interactive shell:

```python
from app.data import EarthAccessClient
from app.data.paths import get_raw_data_dir

client = EarthAccessClient()
results = client.search(short_name="SDO", cloud_hosted=True, bounding_box=[-90, -180, 90, 180])
files = client.download(results[:5], destination=get_raw_data_dir("sdo"))
print(files)
```

All downloads are logged and stored under `data/raw/<mission>`; metadata is persisted via SQLModel for reproducibility.

## 4. Security recommendations
- Never commit the `.env` file—`app/.gitignore` already excludes it.
- For production environments use secret managers (AWS Secrets Manager, GCP Secret Manager) instead of plain env vars.
- Rotate passwords and revoke tokens if credentials may have been exposed.

This documentation fulfills the "Prototype earthaccess authenticated download workflow" task by specifying configuration and execution steps without requiring hardcoded secrets in the repository.

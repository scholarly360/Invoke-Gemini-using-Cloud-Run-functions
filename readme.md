
# From Zero to Vertex AI: Invoke Gemini using Cloud Run functions

Cloud Run Functions is essentially the evolution of what used to be called Cloud Functions, now unified under the Cloud Run infrastructure. In August 2024, Cloud Functions was officially rebranded as Cloud Run Functions, merging with Cloud Run to offer a unified serverless platform that delivers more control and flexibility.
You deploy function code directly (source-based), and Google handles containerization unlike Cloud Run.

Cloud Run Functions offers higher abstraction—focus on business logic, not infrastructure.

## Choose Cloud Run Functions if:

You need to respond to events or HTTP triggers quickly.

You want minimal configuration—all infrastructure handled for you.

You're working with concise functions rather than full-fledged services.

## Choose Cloud Run when:

You require full control over the runtime, libraries, or environment.

Your application is a multi-endpoint service, API, or requires customization.

You need advanced features like GPUs, custom networking, or domain mappings.

## Velox

Vellox is an adapter for running ASGI applications ((Asynchronous Server Gateway Interface) ) in GCP Cloud Functions.

## HTTPBearer

HTTPBearer in FastAPI is a security utility provided by the fastapi.security module. It is designed to handle Bearer token authentication, which is a common method for securing API endpoints.
HTTPBearer primarily handles the presence and extraction of the Bearer token.

## Steps 

### Dev Setup
Use devcontainer to install ( I am using so this is easy )
create main.py with fastapi and vellox

### Enable Services

>> gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com logging.googleapis.com aiplatform.googleapis.com

### IAM 
[In IAM give project role of 'roles/aiplatform.user' to current project](https://cloud.google.com/vertex-ai/generative-ai/docs/start/api-keys?usertype=existinguser) 

### Deploy with ENV, Variables

>> gcloud run deploy fastapi-func --source . --function handler --base-image python313 --region asia-south1 --set-env-vars API_TOKEN="damn-long-token",GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_LOCATION=global  --allow-unauthenticated


from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers.api import api_router
from app.middleware.metrics import PrometheusMiddleware, metrics_endpoint
from app.core.config import settings

# Désactivation de Swagger en production
# En production (ENVIRONMENT=production), /docs et /redoc sont désactivés
# pour ne pas exposer la structure de l'API publiquement.
_is_prod = settings.ENVIRONMENT == "production"
_docs_url = None if _is_prod else "/docs"
_redoc_url = None if _is_prod else "/redoc"
_openapi_url = None if _is_prod else "/openapi.json"

app = FastAPI(
    title="Prédi'lection API",
    version="1.0.0",
    description="API de prédiction politique — FastAPI + PostgreSQL",
    docs_url=_docs_url,
    redoc_url=_redoc_url,
    openapi_url=_openapi_url,
)

# Middleware Prometheus
app.add_middleware(PrometheusMiddleware)

# CORS — Origines autorisées
# En production : seul le domaine officiel est autorisé.
# En développement : localhost est autorisé.
if _is_prod:
    allowed_origins = [
        f"https://{settings.DOMAIN_NAME}",
        f"https://api.{settings.DOMAIN_NAME}",
    ]
else:
    allowed_origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limiter aux méthodes réellement utilisées
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(api_router)

# Endpoint métriques Prometheus (réseau interne uniquement)
# En production, /metrics ne doit être accessible que depuis le réseau Docker
# interne (par Prometheus). On filtre les requêtes extérieures par IP source.
async def _metrics_guard(request: Request) -> Response:
    """Restreint /metrics aux requêtes internes (réseau Docker 172.x.x.x)."""
    client_ip = request.client.host if request.client else ""
    # Autoriser : réseau Docker interne, localhost, et les runners CI
    allowed_prefixes = ("172.", "127.", "10.", "::1")
    if _is_prod and not any(client_ip.startswith(p) for p in allowed_prefixes):
        return Response(content="Forbidden", status_code=403)
    return await metrics_endpoint(request)

app.add_route("/metrics", _metrics_guard, include_in_schema=False)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de health check pour Uptime Kuma et les load balancers."""
    return {"status": "ok", "service": "predilection-api"}
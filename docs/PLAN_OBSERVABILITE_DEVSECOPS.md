# Plan d'Implémentation Observabilité & DevSecOps

## Contexte

Le projet dispose déjà :

* d'un dépôt GitHub
* d'une pipeline CI/CD GitHub Actions
* d'une application conteneurisée avec Docker
* d'un déploiement automatique sur VPS OVH (8 Go RAM)
* d'un reverse proxy Traefik
* d'un environnement de production fonctionnel

L'objectif est maintenant de renforcer :

1. La sécurité du pipeline (DevSecOps)
2. L'observabilité de l'infrastructure
3. La supervision de la disponibilité
4. La collecte et l'analyse des métriques

---

# Sprints d'Implémentation

## Sprint 1 — DevSecOps

1. `feature/gitleaks` (Détecter les secrets exposés)
2. `feature/codeql-security` (Analyse statique du code)
3. `feature/trivy-image-scan` (Scan d'images Docker)

## Sprint 2 — Monitoring Infrastructure

1. `feature/node-exporter` (Collecter métriques système VPS)
2. `feature/prometheus-monitoring` (Centraliser les métriques)
3. `feature/grafana-dashboard` (Visualiser les métriques)
4. `feature/cadvisor-monitoring` (Superviser conteneurs Docker)

## Sprint 3 — Supervision

1. `feature/uptime-kuma` (Surveiller disponibilité des services)

## Sprint 4 — Centralisation des Logs

1. `feature/loki-logging` (Stocker logs applicatifs)
2. `feature/promtail-logging` (Collecter logs Docker)

---

# Architecture Finale Recommandée

VPS OVH
│
├── Traefik
├── Django
├── FastAPI
├── PostgreSQL
│
├── Node Exporter
├── cAdvisor
├── Prometheus
├── Grafana
├── Uptime Kuma
├── Loki
└── Promtail

---

# Structure Docker Recommandée

## docker-compose.yml

Services métier :
* Application (Django, FastAPI)
* Base de données (PostgreSQL)
* Traefik

## docker-compose.monitoring.yml

Services d'observabilité :
* Prometheus
* Grafana
* Node Exporter
* cAdvisor
* Uptime Kuma
* Loki
* Promtail

---

# Résultat Final

Le projet disposera :

* d'une CI/CD automatisée
* d'un contrôle de sécurité du code
* d'un contrôle de sécurité des images Docker
* d'une détection de secrets
* d'un monitoring système
* d'un monitoring Docker
* d'une supervision de disponibilité
* d'une centralisation complète des logs
* d'une architecture DevSecOps moderne

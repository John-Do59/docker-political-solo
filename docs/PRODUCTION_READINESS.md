# Production Readiness — Plan de preuves

> Objectif : passer de « infra quasi prod » à **production-ready prouvé**.
> Chaque critère exige une **preuve documentée** (log, capture, mesure), pas seulement du code mergé.

## Seuils à valider

| # | Critère | Branche | Checklist |
|---|---------|---------|-----------|
| 1 | Alerte réelle (Discord + Telegram) | `ops/prove-alerting` | [01-prove-alerting.md](checklists/01-prove-alerting.md) |
| 2 | Backup restaurable | `ops/prove-backup-restore` | [02-prove-backup-restore.md](checklists/02-prove-backup-restore.md) |
| 3 | Charge max connue (k6) | `ops/k6-load-baseline` | [03-k6-load-baseline.md](checklists/03-k6-load-baseline.md) |
| 4 | Staging isolé | `feature/staging-environment` | [04-staging-environment.md](checklists/04-staging-environment.md) |

## Ordre recommandé

1. `ops/prove-alerting` — ~30 min, aucune infra supplémentaire
2. `ops/prove-backup-restore` — 1–2 h, validation VPS
3. `ops/k6-load-baseline` — ~1 h, exécution k6
4. `feature/staging-environment` — 1–2 jours, architecture

## Definition of Done (global)

- [ ] Les 4 checklists sont complétées avec preuves datées
- [ ] `docs/BACKUP.md`, `docs/MONITORING.md`, `docs/INCIDENT_RESPONSE.md` rédigés
- [ ] Résultats k6 archivés dans `k6/results/`
- [ ] Environnements GitHub `staging` et `prod` configurés

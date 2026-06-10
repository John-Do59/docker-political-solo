# Checklist — Établir la baseline de charge (critère 3/4)

**Branche :** `ops/k6-load-baseline`  
**Preuve attendue :** courbes de performance documentées, point de saturation identifié.

---

## Prérequis

```bash
brew install k6   # macOS
# ou voir k6/README.md pour Linux
export BASE_URL=https://api.<DOMAIN_NAME>
```

---

## Étape 1 — Smoke test

```bash
k6 run k6/smoke.js
```

| Métrique | Résultat | Seuil | OK |
|----------|----------|-------|-----|
| `http_req_failed` | | < 1% | [ ] |
| `http_req_duration p(95)` | | < 500ms | [ ] |

---

## Étape 2 — Load test (100 VUs)

```bash
k6 run --out json=k6/results/load_$(date +%Y%m%d).json k6/load.js
```

| Métrique | Résultat | Seuil | OK |
|----------|----------|-------|-----|
| `errors` rate | | < 1% | [ ] |
| `http_req_duration p(95)` | | < 1000ms | [ ] |
| `http_req_duration p(99)` | | < 2000ms | [ ] |
| Requêtes totales | | — | [ ] |
| Durée test | ~10 min | — | [ ] |

Observer pendant le test (VPS) :

```bash
docker stats --no-stream
# ou Grafana : CPU, RAM, latence API (http_request_duration_seconds)
```

- [ ] CPU max pendant load : ___________ %
- [ ] RAM max pendant load : ___________ %
- [ ] Latence p95 Grafana : ___________ ms

---

## Étape 3 — Stress test (500 VUs)

```bash
k6 run --out json=k6/results/stress_$(date +%Y%m%d).json k6/stress.js
```

| Question | Réponse |
|----------|---------|
| À combien de VUs les erreurs démarrent ? | ___ VUs |
| Premier goulot (CPU / RAM / DB / réseau) | ___ |
| Code HTTP dominant en échec | ___ |
| L'API reste-t-elle récupérable après ? | oui / non |

---

## Étape 4 — Documenter la baseline

Remplir `k6/results/BASELINE.md` avec :

- Date et `BASE_URL` utilisés
- Config VPS (CPU, RAM)
- Tableaux smoke / load / stress
- Recommandations (ex. « stable jusqu'à 100 VUs, DB sature à 300 »)

---

## Optionnel — Intégration CI

- [ ] Ajouter `k6 run k6/smoke.js` en post-deploy dans `deploy.yml`
- [ ] Seuils smoke bloquants en CI

---

## Critère validé quand

- [ ] 3 scénarios exécutés, résultats dans `k6/results/`
- [ ] Point de rupture identifié et documenté
- [ ] Date de validation : ___________

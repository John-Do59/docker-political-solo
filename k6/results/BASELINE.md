# k6 — Baseline de performance

> Remplir après exécution des tests (branche `ops/k6-load-baseline`).
> Ne pas committer de données sensibles (URLs internes OK).

## Contexte

| Champ | Valeur |
|-------|--------|
| Date | |
| Exécuteur | |
| `BASE_URL` | |
| VPS (CPU / RAM) | |
| Version déployée (`RELEASE_TAG`) | |

---

## Smoke test (`smoke.js`)

| Métrique | Valeur | Seuil | Pass |
|----------|--------|-------|------|
| `http_req_failed` | | < 1% | |
| `http_req_duration p(95)` | | < 500ms | |

---

## Load test (`load.js` — 100 VUs)

| Métrique | Valeur | Seuil | Pass |
|----------|--------|-------|------|
| `errors` rate | | < 1% | |
| `http_req_duration p(95)` | | < 1000ms | |
| `http_req_duration p(99)` | | < 2000ms | |
| CPU max observé | | — | |
| RAM max observée | | — | |

---

## Stress test (`stress.js` — 500 VUs)

| Question | Réponse |
|----------|---------|
| VUs avant première erreur | |
| Goulot identifié | |
| Récupération post-stress | |

---

## Conclusion

**Charge supportée en production (recommandation) :** ___ VUs / ___ req/s

**Actions correctives identifiées :**

- 

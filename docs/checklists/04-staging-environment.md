# Checklist — Mettre en place le staging (critère 4/4)

**Branche :** `feature/staging-environment`  
**Preuve attendue :** environnement staging isolé, déployable sans impact production.

---

## Architecture cible

```text
develop  →  staging  (staging.domain.com, DB staging)
main     →  prod     (app.domain.com, DB prod)
tag v*   →  prod     (release versionnée)
```

---

## Étape 1 — Environnements GitHub

Créer dans `Settings → Environments` :

| Environnement | Branche déclencheur | Secrets dédiés |
|---------------|---------------------|----------------|
| `dev` | `develop` | existant |
| `staging` | `main` | à créer |
| `prod` | tags `v*` | à créer |

- [ ] Environnement `staging` créé
- [ ] Environnement `prod` créé (protection rules optionnelles)
- [ ] `DOMAIN_NAME` différent par env (`staging.xxx` vs `xxx`)
- [ ] `DATABASE_URL` / credentials Postgres séparés

---

## Étape 2 — Infrastructure

**Option A — Second VPS (recommandé)**

- [ ] VPS staging provisionné
- [ ] DNS : `staging.<domaine>`, `api.staging.<domaine>`, etc.
- [ ] Secrets GitHub `VPS_HOST_STAGING` ou env-specific secrets

**Option B — Même VPS, stack isolée**

- [ ] `docker-compose.staging.yml` avec noms containers / réseau / volumes distincts
- [ ] Port ou sous-domaine Traefik dédié
- [ ] Base PostgreSQL séparée (`predilection_staging`)

---

## Étape 3 — Modifications code (cette branche)

- [ ] Adapter `deploy.yml` pour cibler le bon VPS/compose par environnement
- [ ] Variables `vars.DOMAIN_NAME` par environnement GitHub
- [ ] Documenter le flux dans `docs/DEPLOYMENT.md`

---

## Étape 4 — Validation

```bash
# Push sur develop → déploie dev (inchangé)
# Merge develop → main → déploie staging
# Tag v1.0.0 → déploie prod
```

- [ ] `https://staging.<domaine>/home/` répond 200
- [ ] `https://api.staging.<domaine>/health` répond 200
- [ ] Modification staging n'impacte pas prod (test : créer une donnée test en staging)
- [ ] Rollback staging testé

---

## Critère validé quand

- [ ] 3 environnements GitHub opérationnels
- [ ] Staging accessible et isolé de prod
- [ ] Date de validation : ___________

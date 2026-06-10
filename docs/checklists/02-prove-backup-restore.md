# Checklist — Prouver backup & restauration (critère 2/4)

**Branche :** `ops/prove-backup-restore`  
**Preuve attendue :** backup créé, vérifié, restauré sur DB de test en < 10 minutes.

---

## Prérequis

- [ ] Scripts déployés sur VPS : `scripts/backup.sh`, `scripts/verify_backup.sh`, `scripts/restore.sh`
- [ ] Workflow `backup.yml` accessible dans GitHub Actions

---

## Étape 1 — Lancer un backup manuel

```bash
gh workflow run backup.yml --repo John-Do59/docker-political-solo
```

Ou sur le VPS :

```bash
cd ~/docker-political
export POSTGRES_USER=... POSTGRES_PASSWORD=... POSTGRES_DB=...
export BACKUP_DIR=/var/backups/predilection BACKUP_RETENTION=7
bash scripts/backup.sh
bash scripts/verify_backup.sh
```

- [ ] Workflow GitHub terminé en **success**
- [ ] Fichier présent : `ls -lh /var/backups/predilection/backup_*.sql.gz`
- [ ] Taille backup : ___________ Mo
- [ ] `verify_backup.sh` : OK

---

## Étape 2 — Restauration sur base de test

> Ne pas restaurer sur la base de production. Utiliser une DB temporaire.

```bash
# Créer une base de test
docker compose -f docker-compose.prod.yml exec db \
  psql -U $POSTGRES_USER -c "CREATE DATABASE predilection_restore_test;"

# Restaurer (adapter POSTGRES_DB)
POSTGRES_DB=predilection_restore_test \
  bash scripts/restore.sh /var/backups/predilection/backup_<date>.sql.gz
```

- [ ] Restauration terminée sans erreur
- [ ] Tables présentes : `docker compose exec db psql -U $POSTGRES_USER -d predilection_restore_test -c '\dt'`
- [ ] Durée totale restore : ___________ min (< 10 min objectif)

```bash
# Nettoyage
docker compose -f docker-compose.prod.yml exec db \
  psql -U $POSTGRES_USER -c "DROP DATABASE predilection_restore_test;"
```

---

## Étape 3 — Backup hors-site (recommandé)

Choisir une option :

- [ ] **Option A** — `rsync` vers second VPS
- [ ] **Option B** — Object Storage (OVH, S3, Backblaze)
- [ ] **Option C** — Copie locale chiffrée hors serveur

Documenter la procédure dans `docs/BACKUP.md`.

---

## Étape 4 — Cron quotidien

- [ ] Attendre le cron 02h00 UTC ou vérifier le run planifié suivant
- [ ] 3 backups consécutifs réussis (dates : ___, ___, ___)
- [ ] Rotation 7 jours vérifiée : anciens backups supprimés

---

## Preuves à archiver

| Élément | Fichier / lien |
|---------|----------------|
| Log backup réussi | `docs/evidence/backup/backup-log-YYYY-MM-DD.txt` |
| Log restore réussi | `docs/evidence/backup/restore-log-YYYY-MM-DD.txt` |
| Durée mesurée | notée dans ce fichier |

---

## Critère validé quand

- [ ] Backup automatique OK + restore testé sur DB non-prod
- [ ] Date de validation : ___________

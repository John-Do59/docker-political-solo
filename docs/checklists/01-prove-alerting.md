# Checklist — Prouver l'alerting (critère 1/4)

**Branche :** `ops/prove-alerting`  
**Preuve attendue :** une alerte reçue sur Discord **et** Telegram en moins d'1 minute.

---

## Prérequis

- [x] PR #47 et #48 mergées, deploy réussi sur le VPS
- [x] Secrets GitHub configurés : `GRAFANA_DISCORD_WEBHOOK_URL`, `GRAFANA_TELEGRAM_BOT_TOKEN`, `GRAFANA_TELEGRAM_CHAT_ID`
- [x] Grafana container `Up` sur le VPS (corrections SMTP + email + chat ID appliquées le 2026-06-10)

---

## Étape 1 — Vérifier les contact points Grafana

```bash
# Sur le VPS
cd ~/docker-political
docker compose -f docker-compose.monitoring.yml logs grafana --tail=50 | grep -i "contact\|alert\|provisioning"
```

Dans Grafana UI → **Alerting** → **Contact points** :
- [x] `Discord Alerting` présent
- [x] `Telegram Alerting` présent
- [x] Test canaux via `bash scripts/test_alert_channels.sh` → Discord HTTP 204, Telegram OK (2026-06-10)

---

## Étape 2 — Déclencher une alerte réelle

**Option A — Alerte test Grafana**

1. Alerting → Alert rules → sélectionner une règle (ex. CPU)
2. **More** → **Evaluate** ou créer une règle test avec seuil très bas

**Option B — Simulation charge CPU (VPS)**

```bash
# Générer de la charge CPU temporaire (à arrêter après test)
stress-ng --cpu 4 --timeout 360s
```

- [ ] Alerte `CPU Usage > 80%` passe en **Firing** dans Grafana
- [ ] Notification Discord reçue (horodatage : ___________)
- [ ] Notification Telegram reçue (horodatage : ___________)
- [ ] Délai alerte → notification < 60 secondes

---

## Étape 3 — Uptime Kuma (complément)

```bash
# Depuis une machine avec accès au VPS
KUMA_URL=https://kuma.<DOMAIN_NAME> \
KUMA_USER=admin \
KUMA_PASSWORD=<secret> \
DOMAIN_NAME=<DOMAIN_NAME> \
python3 scripts/setup_uptime_kuma.py
```

- [ ] 4 monitors actifs : Frontend, API, Traefik, Grafana
- [ ] Notification Discord configurée dans Uptime Kuma
- [ ] Test de panne simulée (arrêt container `api` 2 min) → alerte reçue

---

## Preuves à archiver

| Élément | Fichier / lien |
|---------|----------------|
| Capture Discord | `docs/evidence/alerting/discord-YYYY-MM-DD.png` |
| Capture Telegram | `docs/evidence/alerting/telegram-YYYY-MM-DD.png` |
| État Grafana Firing | `docs/evidence/alerting/grafana-firing-YYYY-MM-DD.png` |

---

## Scripts de validation (VPS)

```bash
# Test direct des canaux Discord + Telegram
bash scripts/test_alert_channels.sh

# Liste des contact points Grafana (API interne)
bash scripts/test_grafana_contact_points.sh
```

## Critère validé quand

- [x] Discord + Telegram reçoivent un message de test (canaux opérationnels)
- [ ] Alerte **critical** Grafana en état Firing → Discord + Telegram (à valider via charge CPU ou règle test)
- [ ] Date de validation complète : ___________
- [ ] Validé par : ___________

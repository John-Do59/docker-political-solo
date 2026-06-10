# Checklist — Prouver l'alerting (critère 1/4)

**Branche :** `ops/prove-alerting`  
**Preuve attendue :** une alerte reçue sur Discord **et** Telegram en moins d'1 minute.

---

## Prérequis

- [ ] PR #47 et #48 mergées, deploy réussi sur le VPS
- [ ] Secrets GitHub configurés : `GRAFANA_DISCORD_WEBHOOK_URL`, `GRAFANA_TELEGRAM_BOT_TOKEN`, `GRAFANA_TELEGRAM_CHAT_ID`
- [ ] Grafana accessible : `https://grafana.<DOMAIN_NAME>`

---

## Étape 1 — Vérifier les contact points Grafana

```bash
# Sur le VPS
cd ~/docker-political
docker compose -f docker-compose.monitoring.yml logs grafana --tail=50 | grep -i "contact\|alert\|provisioning"
```

Dans Grafana UI → **Alerting** → **Contact points** :
- [ ] `Discord Alerting` présent
- [ ] `Telegram Alerting` présent
- [ ] Bouton **Test** Discord → message reçu
- [ ] Bouton **Test** Telegram → message reçu

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

## Critère validé quand

- [x] Discord + Telegram reçoivent une alerte **critical** déclenchée par Grafana
- [ ] Date de validation : ___________
- [ ] Validé par : ___________

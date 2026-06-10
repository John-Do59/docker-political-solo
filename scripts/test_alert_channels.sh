#!/usr/bin/env bash
# =============================================================================
# test_alert_channels.sh — Teste Discord et Telegram (canaux d'alerte)
# =============================================================================
# Usage (sur le VPS) :
#   bash scripts/test_alert_channels.sh
#
# Lit les variables depuis le container Grafana (aucun secret affiché).
# =============================================================================

set -euo pipefail

GRAFANA_CONTAINER="${GRAFANA_CONTAINER:-monitoring-grafana}"
MSG="${1:-Test alerting production-readiness — $(date -u +%Y-%m-%dT%H:%M:%SZ)}"

if ! docker ps --format '{{.Names}}' | grep -q "^${GRAFANA_CONTAINER}$"; then
    echo "❌ Container ${GRAFANA_CONTAINER} non démarré."
    exit 1
fi

echo "▶ Test Discord webhook..."
DISCORD_OK=$(docker exec "${GRAFANA_CONTAINER}" sh -c '
URL=$(printenv GRAFANA_DISCORD_WEBHOOK_URL)
if [ -z "$URL" ]; then echo "missing"; exit 0; fi
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "{\"content\":\"'"${MSG}"' — Discord\"}")
echo "$CODE"
')

case "${DISCORD_OK}" in
  204|200) echo "   ✅ Discord OK (HTTP ${DISCORD_OK})" ;;
  missing) echo "   ⚠️  GRAFANA_DISCORD_WEBHOOK_URL non défini" ; exit 1 ;;
  *) echo "   ❌ Discord échec (HTTP ${DISCORD_OK})" ; exit 1 ;;
esac

echo "▶ Test Telegram bot..."
TELEGRAM_RESULT=$(docker exec "${GRAFANA_CONTAINER}" sh -c '
TOKEN=$(printenv GRAFANA_TELEGRAM_BOT_TOKEN)
CHAT=$(printenv GRAFANA_TELEGRAM_CHAT_ID)
if [ -z "$TOKEN" ] || [ -z "$CHAT" ]; then echo "missing"; exit 0; fi
RESP=$(curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${CHAT}" \
  --data-urlencode "text='"${MSG}"' — Telegram")
echo "$RESP" | grep -q "\"ok\":true" && echo "ok" || echo "fail"
')

case "${TELEGRAM_RESULT}" in
  ok) echo "   ✅ Telegram OK" ;;
  missing) echo "   ⚠️  GRAFANA_TELEGRAM_* non défini" ; exit 1 ;;
  *) echo "   ❌ Telegram échec" ; exit 1 ;;
esac

echo ""
echo "✅ Canaux Discord et Telegram opérationnels — vérifier les messages reçus."

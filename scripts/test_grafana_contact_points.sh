#!/usr/bin/env bash
# =============================================================================
# test_grafana_contact_points.sh — Teste les contact points Grafana (Discord, Telegram)
# =============================================================================
# Usage (sur le VPS) :
#   bash scripts/test_grafana_contact_points.sh
#
# Prérequis : container monitoring-grafana en état Up
# =============================================================================

set -euo pipefail

GRAFANA_CONTAINER="${GRAFANA_CONTAINER:-monitoring-grafana}"
GRAFANA_USER="${GRAFANA_USER:-admin}"

if ! docker ps --format '{{.Names}}' | grep -q "^${GRAFANA_CONTAINER}$"; then
    echo "❌ Container ${GRAFANA_CONTAINER} non démarré."
    exit 1
fi

echo "▶ Vérification santé Grafana..."
docker exec "${GRAFANA_CONTAINER}" sh -c '
PASS=$(printenv GF_SECURITY_ADMIN_PASSWORD)
curl -sf -u "admin:${PASS}" http://localhost:3000/api/health
'

echo "▶ Contact points provisionnés :"
docker exec "${GRAFANA_CONTAINER}" sh -c '
PASS=$(printenv GF_SECURITY_ADMIN_PASSWORD)
curl -sf -u "admin:${PASS}" http://localhost:3000/api/v1/provisioning/contact-points \
  | grep -o "\"name\":\"[^\"]*\"" | cut -d\" -f4 | sed "s/^/  - /"
'

test_contact_point() {
    local encoded_name="$1"
    local label="$2"
    echo ""
    echo "▶ Test contact point : ${label}"
    docker exec "${GRAFANA_CONTAINER}" sh -c "
PASS=\$(printenv GF_SECURITY_ADMIN_PASSWORD)
HTTP_CODE=\$(curl -s -o /tmp/grafana-test-out.txt -w '%{http_code}' \
  -u \"admin:\${PASS}\" \
  -H 'Content-Type: application/json' \
  -X POST 'http://localhost:3000/api/v1/provisioning/contact-points/${encoded_name}/test' \
  -d '{\"message\":\"Test alerting production-readiness — ${label}\"}')
if echo \"\${HTTP_CODE}\" | grep -qE '^2'; then
  echo \"   ✅ Test envoyé (HTTP \${HTTP_CODE})\"
else
  echo \"   ❌ Échec (HTTP \${HTTP_CODE})\"
  cat /tmp/grafana-test-out.txt
  exit 1
fi
"
}

test_contact_point "Discord%20Alerting" "Discord"
test_contact_point "Telegram%20Alerting" "Telegram"

echo ""
echo "✅ Tests terminés — vérifier Discord et Telegram."

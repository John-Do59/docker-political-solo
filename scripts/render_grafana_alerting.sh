#!/usr/bin/env bash
# =============================================================================
# render_grafana_alerting.sh — Rend les contact points Grafana (chat ID en string)
# =============================================================================
# Appelé par deploy.sh sur le VPS. Les secrets restent dans l'environnement shell,
# le YAML rendu est écrit localement sur le VPS (requis par Grafana provisioning).
# =============================================================================

set -euo pipefail

ALERTING_DIR="${1:-monitoring/grafana/provisioning/alerting}"
CONTACT_FILE="${ALERTING_DIR}/contact_points.yml"

if [[ ! -f "${CONTACT_FILE}" ]]; then
    echo "⚠️  ${CONTACT_FILE} introuvable, skip render."
    exit 0
fi

if [[ -z "${GRAFANA_TELEGRAM_CHAT_ID:-}" ]]; then
    echo "⚠️  GRAFANA_TELEGRAM_CHAT_ID absent, skip render Telegram chatid."
    exit 0
fi

# Grafana 11 parse les chat ID numériques comme int si non quotés — forcer string YAML
python3 - "${CONTACT_FILE}" "${GRAFANA_TELEGRAM_CHAT_ID}" <<'PY'
import re, sys
path, chat_id = sys.argv[1], sys.argv[2]
text = open(path, encoding="utf-8").read()
text = re.sub(
    r"chatid:.*",
    f'chatid: "{chat_id}"',
    text,
    count=1,
)
open(path, "w", encoding="utf-8").write(text)
PY

echo "▶ contact_points.yml rendu (Telegram chatid quoté)."

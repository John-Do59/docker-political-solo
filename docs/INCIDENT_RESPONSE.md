# Plan de Réponse aux Incidents (Incident Response)

Ce document décrit la marche à suivre en cas d'alerte critique sur l'infrastructure de Predil'ection.

## 1. Réception de l'alerte
Les alertes sont configurées pour être envoyées automatiquement vers nos canaux de communication (Discord / Telegram) en cas de défaillance.

**Exemples de déclencheurs :**
- Conteneur arrêté (API, Front, Base de données).
- Consommation CPU anormale (> 80%).
- Uptime Kuma ne parvient pas à joindre l'application (Erreur HTTP).

## 2. Évaluation de l'incident (Triage)
Dès qu'une alerte est reçue :
1. **Confirmer la panne** : Accéder à l'interface Uptime Kuma ou Grafana pour confirmer que l'alerte est toujours active et non un faux positif.
2. **Identifier l'impact** : Est-ce que l'application entière est inaccessible (ex: Traefik down) ou seulement une partie (ex: API down) ?

## 3. Investigation
Se connecter au VPS en SSH pour inspecter les logs. Si Grafana/Loki sont accessibles, privilégier la lecture centralisée des logs via l'interface Grafana.

Commandes d'urgence si accès SSH :
```bash
# Voir l'état des conteneurs
cd ~/docker-political
docker compose -f docker-compose.prod.yml ps

# Regarder les logs du conteneur fautif (ex: api)
docker compose -f docker-compose.prod.yml logs --tail=100 -f api
```

## 4. Résolution (Playbooks)

### Cas 4.1 : Surcharge de trafic ou fuite mémoire
- **Symptôme** : CPU > 80% ou conteneur "OOM Killed".
- **Action** : Redémarrer le conteneur concerné. Si la charge persiste, envisager une augmentation des ressources (Scale up) du VPS.
  ```bash
  docker compose -f docker-compose.prod.yml restart api
  ```

### Cas 4.2 : Corruption de la base de données
- **Symptôme** : Erreurs 500 sur l'API, logs indiquant des erreurs PostgreSQL fatales.
- **Action** : Déclencher la procédure de restauration. Se référer à [BACKUP.md](./BACKUP.md).

### Cas 4.3 : Plus d'espace disque
- **Symptôme** : Les conteneurs refusent de démarrer, alertes système.
- **Action** : Nettoyer les ressources Docker non utilisées et vérifier les logs volumineux.
  ```bash
  docker system prune -af --volumes
  ```

## 5. Post-mortem
Après la résolution de l'incident :
- Consigner l'heure de début et de fin.
- Expliquer la cause (Root Cause Analysis).
- Définir des actions correctives (ex: ajouter une nouvelle alerte Grafana plus spécifique) pour éviter que cela ne se reproduise.

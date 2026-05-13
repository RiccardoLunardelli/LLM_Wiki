# Contratti messaggi ed esecuzione locale di PW-Airport

## Contratti Messaggi

### Unity -> Python

- `setup-init`
- `send-splines`
- `finish-send-splines`
- `send-prefabs`
- `finish-send-prefabs`
- payload spline `{ "type":"event", "event":"spline", "spline": {...} }`
- `path_completed`
- `plane_left_stand`
- `set_time_scale`
- `set_sim_time`

### Python -> Unity

- `spawn_plane`
- `start_path`
- `clock_sync`
- `welcome`

## Convenzioni di stato / vocabolario

- Stati volo: `Unscheduled`, `Scheduled`, `Ongoing`, `Landing`, `Disembarking`, `Completed`, `StandReserved`
- Stati aereo: `Parked`, `Reserved`, `InFlight`, `Disembarking`
- Stati stand: `Available`, `Reserved`, `Occupied`
- Tipi di volo: `Cargo`, `Passengers`
- Range: `Short`, `Medium`, `Long`

## Esecuzione locale / servizi

### Stack infrastrutturale

```bash
docker compose up -d

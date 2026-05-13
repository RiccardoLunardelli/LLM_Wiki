# Workflow backend PW-Airport

## Workflow End-to-End

### 1) Startup e handshake di setup (Unity -> Python)

1. Unity si connette a `ws://localhost:8765` (`UnityWSClient.cs`).
2. Unity `SplineRegistry` invia controllo + batch spline:
   - `setup-init`
   - `send-splines`
   - molti payload spline
   - `finish-send-splines`
3. Unity `PrefabRegistry` invia:
   - `send-prefabs`
   - lista prefab
   - `finish-send-prefabs`
4. Python `SetupBusHandler`:
   - bufferizza i batch
   - memorizza prefab e posizioni
   - costruisce i path tramite `InitGraph`
   - ricostruisce `Percorso` nel DB
   - marca `setup_completed=True`

### 2) Logica di generazione dei path

`src/init_graph.py` esegue:

- Caricamento dello schema nodi-collegamenti da `schema_nodi.json`
- Parsing dei knot della master spline
- Costruzione dei path di atterraggio
- Costruzione dei path di partenza
- Salvataggio dei record path nel DB

### 3) Bootstrap dello spawn iniziale

- `schedule_initial_spawns()` esegue `SpawnScheduler.plan_initial_spawns()`
- resetta stand e tabelle collegate
- seleziona stand disponibili e prefab casuali
- emette `spawn_plane`
- `ws_server.py` garantisce la riga aereo e registra `WorldState`

### 4) Scheduling del lifecycle dei voli

`flight_scheduler_loop()`:

- aspetta il setup
- genera i voli iniziali
- legge il tempo da `SimulationClock`
- recupera i voli nella finestra scorrevole
- applica le guardie di fase

Decisioni:
- scheduling partenze
- preparazione voli in ingresso
- prenotazione arrivi
- assegnazione stand/path/parking
- invio dei comandi di movimento

### 5) Gestione degli eventi runtime

Unity emette:
- `path_completed`
- `plane_left_stand`

`RuntimeBusHandler` aggiorna:
- stati aereo
- stati volo
- stati stand
- timer di sbarco
- gestione parking

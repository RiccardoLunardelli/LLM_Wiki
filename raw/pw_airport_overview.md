# PW-Airport

Simulazione aeroportuale in tempo reale con:

- Backend Python (scheduling autorevole, stato DB e clock di simulazione)
- Client Unity (setup della scena, spawning dei prefab, movimento su spline)
- Placement AR dello scenario aeroportuale in Unity AR Space
- Parcheggi circolari di holding sopra l'aeroporto per la gestione degli arrivi senza stand libero
- Servizi di terra per bus passeggeri e mezzi cargo/bagagli coordinati dal backend
- PostgreSQL + Metabase (persistenza dei dati e analisi)
- Dashboard FastAPI con viste live e dettaglio
- Servizio chatbot FastAPI che inoltra prompt verso un server LLM remoto

## Documentazione

La documentazione del progetto e organizzata in `src/docs` (cartelle tematiche, in ordine di lettura):

- `src/docs/README.md` (indice)

## Macro Architettura

### Componenti principali

- `src/server.py`: entrypoint del processo; inizializza lo stato condiviso (`PrefabStore`, `InitGraph`, `WorldState`) e avvia il server WebSocket.
- `src/transport/ws_server.py`: orchestratore del flusso di setup, del flusso runtime, degli scheduler, della sincronizzazione del clock e del dispatch dei comandi verso Unity.
- `src/transport/message_bus.py`: code async in ingresso/uscita tra il trasporto WebSocket e la logica backend.
- `src/handlers/setup_bus.py`: gestisce i payload di bootstrap di Unity (spline + prefab), costruisce i path e scrive la tabella `Percorso`.
- `src/handlers/runtime_bus.py`: gestisce gli eventi runtime di Unity (`path_completed`, `plane_left_stand`) e i timer di sbarco.
- `src/schedulers/spawn_scheduler.py`: pianifica gli spawn iniziali degli aerei parcheggiati dopo il setup.
- `src/schedulers/flight_scheduler.py`: motore decisionale a finestra scorrevole per il lifecycle di partenze/arrivi.
- `src/services/flight_generator.py`: crea voli casuali nel DB per la simulazione.
- `src/services/ground_vehicle_coordinator.py`: coordina bus passeggeri e mezzi cargo, assegna i path ai veicoli e gestisce i cicli di servizio.
- `src/db/db_functions.py`: transizioni DB a livello di dominio (assegnazione aerei, prenotazione stand, assegnazione path, transizioni di stato).
- `src/domain/sim_clock.py`: clock di simulazione autorevole con `time_scale` regolabile.
- `src/web/dashboard_app.py`: dashboard FastAPI con shell HTML, websocket live (`/ws/clock`, `/ws/window-flights`) e API di dettaglio per voli e aerei.
- `src/llm_service/app.py` + `src/llm_service/templates/index.html` + `src/llm_service/static/*`: servizio chatbot web che inoltra richieste a un endpoint LLM remoto.
- `Unity_Scripts/*`: lato Unity per client websocket, dispatcher, export/import spline, spawning, movimento lungo i path e controlli temporali.
- `Unity_Scripts/AirportSimulationBootstrap.cs` + `Unity_Scripts/AutoARPlacementController.cs`: placement AR, rebuild delle cache spline dopo il posizionamento e bootstrap della simulazione.

### Modello dati (alto livello)

Entita principali in `src/db/models.py`:

- `Flight` (`Viaggio`): pianificazione + stato operativo.
- `Airplane` (`Aereo`): stato dell'aeromobile e percorso corrente.
- `Stand` (`Piazzola`): disponibilita del parcheggio/stand e collegamento opzionale con un aereo.
- `Path` (`Percorso`): segmenti spline generati per il movimento.
- `ParkingSpot`: parcheggi circolari di attesa usati quando uno stand non e disponibile.
- `Vehicle`: mezzi di terra usati per trasferimento passeggeri, bagagli e cargo.
- Di supporto: `Airport`, `Airline`, `Terminal`, `Vehicle`, `Operation`, `Passenger`, `Cargo`, `ParkingSpot`.

Creazione/reset dello schema: `scripts/init_db.py`
Seed dei dati statici: `scripts/startup.py`

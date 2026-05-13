# Dashboard, chatbot e AR di PW-Airport

### 9) Workflow dashboard

`src/web/dashboard_app.py` espone:

- `GET /`
- `GET /flight/{flight_id}`
- `GET /plane/{airplane_id}`
- `GET /api/status`
- `GET /api/flight/{flight_id}`
- `GET /api/plane/{airplane_id}`
- `WS /ws/clock`
- `WS /ws/window-flights`
- `/static/*`

La dashboard usa:
- `src/web/dashboard_data.py`
- `src/web/dashboard_live.py`
- `src/web/dashboard_views.py`

### 10) Workflow chatbot

Il servizio chatbot (`src/llm_service/app.py`) espone:

- `GET /`
- `GET /health`
- `POST /api/prompt`

Supporta:
- risposta diretta
- recupero differito via `request_id`
- streaming backend con `REMOTE_STREAM = True`
- input vocale
- bridge Android (`Android.sendJsonData`, `window.setPromptFromNative`)

### 11) Unity AR Space e superfici web embeddabili

- `AutoARPlacementController` rileva un piano AR valido
- `AirportSimulationBootstrap` aspetta il placement e invia il setup a Python
- dashboard e chatbot possono essere mostrati dentro l’esperienza AR o su companion device
- la UI chatbot e orientata al mobile

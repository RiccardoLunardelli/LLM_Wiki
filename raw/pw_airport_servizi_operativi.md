# Servizi operativi PW-Airport

### 6) Holding nei parcheggi circolari sopra l'aeroporto

Il sistema supporta parcheggi circolari di attesa (`PARKING_SPLINES = (1, 2, 3)`).

- path di ingresso `Path_LandingRoute_<direction>_Parking<n>`
- path di uscita `Path_Parking<n>_<landing_id>_<stand_id>`
- uso del parking quando non ci sono stand liberi
- uscita coordinata quando uno stand torna disponibile

### 7) Servizi di terra: bus, bagagli e cargo

`src/services/ground_vehicle_coordinator.py` orchestra:

- voli passeggeri: `passenger_transfer` + `luggage_transfer`
- voli cargo: `cargo_transfer`

Nodi home:
- `BusHome_P`
- `BusHome_O`
- `CargoHome_P`
- `CargoHome_C`
- `CargoHome_O`

Il backend:
- risolve i path dei mezzi nel DB
- invia `start_vehicle_path`
- invia eventi di progresso come `start_service_progress` e `stop_service_progress`

### 8) Clock di simulazione e controllo del tempo

- `SimulationClock` Python e autorevole
- `clock_sync_loop()` invia `clock_sync` a Unity
- Unity consuma la sincronizzazione
- i controlli UI inviano `set_time_scale` e opzionalmente `set_sim_time`
- `handle_clock_control()` applica le modifiche

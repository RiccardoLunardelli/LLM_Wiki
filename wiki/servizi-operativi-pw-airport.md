---
title: "Servizi operativi PW-Airport"
date: "2026-05-13"
tags: ["PW-Airport", "Servizi Operativi"]
source: ["raw/pw_airport_servizi_operativi.md"]
---

# Servizi operativi PW-Airport

## Sintesi

Descrizione dei servizi operativi del progetto PW-Airport.

## Dettagli

- Il sistema supporta parcheggi circolari di attesa (`PARKING_SPLINES = (1, 2, 3)`).
- Il backend risolve i path dei mezzi nel DB e invia eventi di progresso come `start_service_progress` e `stop_service_progress`.
- La simulazione è sincronizzata con Unity tramite il `clock_sync_loop()`.

## Collegamenti

Nessuno.

## Fonti

- raw/pw_airport_servizi_operativi.md

## Contraddizioni

Nessuno.

## Note operative

Nessuno.

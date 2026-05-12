# Project Work ITS Alto Adriatico - LIAG

## Sintesi

Il progetto consiste nella simulazione di un aeroporto chiamato LIAG.

L'aeroporto simulato si trova ad Amaro, in Friuli Venezia Giulia.

Il progetto è stato realizzato come Project Work per ITS Alto Adriatico.

## Gruppo

I componenti del gruppo sono:

- Lunardelli Riccardo
- Esposito Nicholas
- Barzan Umberto
- Petrillo Giacomo

## Ruoli

I ruoli dei componenti del gruppo sono:

- Esposito Nicholas: Product Owner (PO)
- Barzan Umberto: Scrum Master
- Petrillo Giacomo: Developer
- Lunardelli Riccardo: Developer

## IoT

Nel progetto sono state implementate due funzionalità IoT.

### Rilevazione della luce

È stato utilizzato un fotoresistore per rilevare l'intensità luminosa.

Il fotoresistore invia il valore rilevato tramite MQTT.

Il valore ricevuto viene usato da Unreal Engine per decidere se nella simulazione deve essere giorno o notte.

### Notifiche di atterraggio e decollo

Unreal Engine invia una notifica quando un aereo sta atterrando o decollando.

In base alla notifica ricevuta, vengono accesi dei LED.

I LED rappresentano uno stato fisico collegato agli eventi della simulazione.

## Intelligenza artificiale

Nel progetto sono state implementate funzionalità di intelligenza artificiale.

### LLM Wiki

È stato realizzato un agente LLM Wiki.

L'agente LLM Wiki risponde alle domande dell'utente usando le informazioni salvate nella wiki locale.

L'agente usa il modello locale `llama3.1:8b`.

Il modello `llama3.1:8b` viene eseguito localmente tramite Ollama.

La wiki viene salvata in file Markdown.

Le fonti originali vengono salvate nella cartella `raw`.

Le pagine generate dall'agente vengono salvate nella cartella `wiki`.

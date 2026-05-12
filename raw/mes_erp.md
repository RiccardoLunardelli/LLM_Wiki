# MES e ERP - Documento di Studio Completo

## 1. Introduzione

Nel contesto industriale moderno, le aziende utilizzano sistemi software per gestire sia la parte amministrativa che quella produttiva. I due sistemi principali sono:

* ERP (Enterprise Resource Planning)
* MES (Manufacturing Execution System)

Questi sistemi non sono in competizione, ma **complementari**.

---

## 2. ERP - Enterprise Resource Planning

### Definizione

Un ERP è un sistema gestionale che coordina e pianifica tutte le risorse aziendali.

### Funzioni principali

* Gestione ordini clienti
* Acquisti fornitori
* Fatturazione
* Contabilità
* Gestione dipendenti
* Stipendi e ferie
* Magazzino (livello strategico)

### Obiettivo

Fornire una **visione globale e organizzativa** dell'azienda.

---

## 3. MES - Manufacturing Execution System

### Definizione

Un MES è il sistema che gestisce e monitora la produzione in tempo reale.

### Funzioni principali

* Monitoraggio macchine
* Avanzamento produzione
* Raccolta dati sensori
* Controllo qualità
* Tracciabilità lotti
* Gestione manutenzione
* Sicurezza operatori

### Obiettivo

Ottimizzare l'efficienza della produzione.

---

## 4. Differenza ERP vs MES

| ERP                | MES                 |
| ------------------ | ------------------- |
| Pianifica          | Esegue              |
| Gestione aziendale | Gestione produzione |
| Visione strategica | Controllo operativo |
| Dati aggregati     | Dati real-time      |

### Frase da esame

> L'ERP decide cosa produrre e quando, il MES esegue e monitora la produzione.

---

## 5. Classificazione dei processi

### ERP

* Ordini materiali
* Gestione ordini clienti
* Fatture
* Stipendi
* Ferie
* Gestione dipendenti

### MES

* Creazione mescole
* Monitoraggio produzione
* Manutenzione
* Sicurezza lavoratori
* Consumi macchine
* Task operativi

### Zona ibrida

* Magazzino
* Qualità
* Produzione ordini
* Manutenzione (costi + interventi)

---

## 6. Esempio azienda farmaceutica

### ERP

* Acquisto materie prime
* Gestione fornitori
* Fatturazione
* Pianificazione produzione
* Documentazione qualità

### MES

* Produzione lotti farmaci
* Miscelazione ingredienti
* Controllo temperatura
* Tracciabilità batch
* Monitoraggio impianti

---

## 7. Architettura moderna

Flusso tipico:

Sensori -> IoT -> Automazioni -> Ticket -> ERP

Componenti:

* IoT: raccolta dati
* Automazioni: gestione eventi
* Ticketing: gestione problemi
* ERP: gestione aziendale

---

## 8. n8n - Automazione

### Cos'è

Piattaforma low-code per creare workflow automatizzati.

### Funzioni

* Webhook (API)
* Integrazione sistemi
* Trigger automatici
* Manipolazione dati

### Esempio

Temperatura alta:

* webhook riceve dato
* workflow analizza
* crea ticket
* invia notifica

---

## 9. ThingsBoard - IoT

### Funzione

* Raccolta dati sensori
* Dashboard
* Telemetria
* Monitoraggio eventi

---

## 10. Zammad - Ticketing

### Funzione

* Gestione assistenza
* Creazione ticket
* Automazione supporto
* Integrazione con sistemi

---

## 11. LLM (AI)

### Utilizzo

* Interpretare dati
* Analizzare anomalie
* Generare report
* Automatizzare decisioni

### Esempio

Input:

> Temperatura troppo alta

Output:

> Possibile guasto sistema di raffreddamento

---

## 12. Selenium - Automazione browser

### Definizione

Selenium permette di automatizzare il browser simulando un utente.

### Quando usarlo

Quando NON ci sono:

* API
* accesso database
* integrazioni ufficiali

### Cosa fa

* apre pagine web
* compila form
* clicca bottoni
* invia dati

### Esempio

Creazione ordine:

1. login gestionale
2. compilazione form
3. selezione prodotto
4. submit ordine

### Frase da esame

> Selenium consente l'integrazione con sistemi legacy automatizzando l'interfaccia web.

---

## 13. Integrazione completa

Esempio reale:

1. Sensore rileva problema
2. ThingsBoard registra dato
3. n8n elabora evento
4. LLM interpreta problema
5. Zammad crea ticket
6. ERP registra costo/intervento

---

## 14. Concetti chiave da ricordare

* ERP = gestione aziendale
* MES = gestione produzione
* n8n = automazioni
* IoT = raccolta dati
* LLM = intelligenza
* Selenium = automazione browser

---

## 15. Risposta pronta da esame

> In un sistema industriale moderno, l'ERP gestisce le risorse aziendali mentre il MES controlla la produzione in tempo reale.
> I dati provenienti dai sensori IoT vengono elaborati da sistemi di automazione come n8n, che possono generare ticket e aggiornare l'ERP.
> In assenza di API, strumenti come Selenium permettono l'integrazione automatizzando l'interfaccia web dei gestionali.

---

## 16. Metodo per memorizzare

ERP -> ufficio  
MES -> fabbrica  
n8n -> automazioni  
IoT -> dati  
Selenium -> browser automation  
AI -> interpretazione

---

FINE DOCUMENTO

# M1 — Analisi mensile personale

[← PRD](../README.md) · Precedente: [M0](M0-foundation.md) · Successive: [M2](M2-import.md), [M3](M3-budgets.md)

## Esito

Un utente gestisce i propri conti, la propria tassonomia di categorie e
sottocategorie, registra entrate, uscite e giroconti e ottiene il report
mensile per categoria, senza doppi conteggi. È la priorità di prodotto
(obiettivo G-1) ed è funzionalmente autonoma per uso individuale; l'uso con
dati reali segue il [livello 1](../roadmap.md#livelli-di-rilascio).

## Dipendenze

- [M0](M0-foundation.md).
- Milestone tecnica M0.1, chiusa il 2026-11-03
  ([scheda](../../../architecture/household-hub-v1/M0.1-structural-refactoring.md)).
- Preparazione tecnica, decisioni e ordine dei task nella
  [scheda tecnica di M1](../../../architecture/household-hub-v1/M1-technical-preparation.md).

## Storie

| Ordine | Storia | Dipende da | DoR |
|---|---|---|---|
| 1 | [US-003 — Gestione dei conti personali](../stories/US-003-personal-accounts.md) | US-002 | READY |
| 1 | [US-004 — Categorie e sottocategorie personalizzabili](../stories/US-004-categories.md) | US-002 | READY |
| 2 | [US-005 — Movimenti manuali](../stories/US-005-manual-transactions.md) | US-003, US-004 | READY |
| 3 | [US-006 — Giroconti tra conti](../stories/US-006-transfers.md) | US-005 | READY |
| 4 | [US-007 — Report mensile per categoria](../stories/US-007-monthly-report.md) | US-005, US-006 | READY |

US-003 e US-004 sono indipendenti e possono procedere in parallelo.

## Criterio di completamento

- Criteri di accettazione di US-003 – US-007 soddisfatti, esclusi
  AC-US-007-05 se rinviato e i criteri completati nelle milestone
  successive (tabella sotto).
- Dataset di verifica dei report (giroconti, rimborsi, movimenti da
  categorizzare, importi frazionari) definito e superato sui punti di
  DR-012 verificabili in M1, inclusa la quadratura dei saldi con i
  giroconti (DR-012 punto 7; [delimitazione in US-007](../stories/US-007-monthly-report.md#verifica)):
  sarà riusato in M3 ed esteso in M4 con i trasferimenti tra spazi.
- NFR-004, NFR-005 e NFR-006 verificati per il report mensile.

### Criteri completati nelle milestone successive

Un criterio si considera soddisfatto solo quando tutte le sue condizioni
verificabili sono implementate e verificate. I criteri seguenti comprendono
condizioni che richiedono funzioni di milestone successive: le loro parti
realizzabili in M1 sono implementate e verificate in M1, ma il criterio è
dichiarato soddisfatto nella milestone indicata.

| Criterio | Condizione successiva | Completato in |
|---|---|---|
| AC-US-003-05 | Un conto archiviato non accetta importazioni | M2: TASK-024, TASK-026 |
| AC-US-005-06 | Filtro per la natura «trasferimento tra spazi» | M4: TASK-081 |
| AC-US-006-02 | Lo spostamento verso un altro spazio si registra come trasferimento tra spazi | M4: TASK-081 |
| AC-US-006-06 | Unione di movimenti attribuiti (conferma dei nuclei) e vincolati (rettifica contabile) | M4: TASK-056, TASK-085 |
| AC-US-006-08 | Trasferimenti tra spazi nello spazio personale | M4: TASK-081 |
| AC-US-007-02 | Invarianti di DR-012 su budget, trasferimenti tra spazi e attribuzioni | M4: TASK-061 |
| AC-US-007-09 | Quadratura dei saldi con i trasferimenti tra spazi | M4: TASK-061 |

## Rischi principali

- [RISK-002](../open-questions-and-risks.md#rischi): correttezza dei totali.

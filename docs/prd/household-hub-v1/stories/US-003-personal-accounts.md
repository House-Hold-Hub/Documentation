# US-003 — Gestione dei conti personali

| Campo | Valore |
|---|---|
| Milestone | [M1 — Analisi mensile personale](../milestones/M1-personal-monthly-analysis.md) |
| Requisiti | [FR-008](../requirements.md#fr-008--conti-e-tipologie), [FR-009](../requirements.md#fr-009--saldo-del-conto), [FR-010](../requirements.md#fr-010--archiviazione-dei-conti) |
| Regole | [DR-018](../domain-rules.md#dr-018--saldo-del-conto) |
| Dipende da | [US-002](US-002-space-isolation.md) |
| Questioni collegate | [Q-007](../open-questions-and-risks.md#q-007--carte-di-credito) (non bloccante) |
| DoR | READY |

## Storia

Come utente, voglio registrare i miei conti con il saldo di partenza, così
da vedere quanto ho su ciascuno.

## Esito atteso

L'utente ha l'elenco dei propri conti attivi e archiviati con saldi
corretti a qualsiasi data.

## Criteri di accettazione

- **AC-US-003-01** — Creo un conto indicando nome, tipologia (conto
  corrente, conto deposito, conto investimento, contanti), istituto
  facoltativo, saldo iniziale (anche negativo) e data di riferimento; il
  conto appare nell'elenco con il saldo odierno.
- **AC-US-003-02** — Il nome è obbligatorio e unico tra i conti attivi
  dello spazio; il saldo iniziale accetta al massimo due decimali.
- **AC-US-003-03** — Dato un saldo iniziale di 1.000,00 € al 31 gennaio, un
  movimento di uscita di 30,00 € il 20 gennaio, un'uscita di 50,00 € il
  5 febbraio e un'entrata di 200,00 € il 10 febbraio, il saldo è 1.030,00 €
  al 19 gennaio, 1.000,00 € al 31 gennaio e 1.150,00 € al 28 febbraio.
- **AC-US-003-04** — Modificare saldo iniziale o data di riferimento
  ricalcola subito i saldi a ogni data.
- **AC-US-003-05** — Un conto archiviato non accetta nuovi movimenti,
  giroconti né importazioni, resta nei report dei mesi in cui ha movimenti
  e compare tra i conti archiviati; può essere riattivato.
- **AC-US-003-06** — Un conto senza movimenti può essere eliminato; per un
  conto con movimenti l'eliminazione non è consentita e viene proposta
  l'archiviazione.

## Verifica

Test di accettazione automatizzati con i dati di AC-03; test negativi di
accesso estesi ai conti (US-002).

## Task

- **TASK-008** — Creazione, modifica ed elenco dei conti (AC-01, AC-02).
- **TASK-009** — Calcolo del saldo a una data secondo DR-018 (AC-03, AC-04).
- **TASK-010** — Archiviazione, riattivazione ed eliminazione dei conti
  senza movimenti (AC-05, AC-06).

## Definition of Ready

READY. Le posizioni dei conti investimento sono in
[US-024](US-024-investments-and-net-worth.md).

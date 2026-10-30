# US-010 — Lotti di importazione annullabili

| Campo | Valore |
|---|---|
| Milestone | [M2 — Importazione](../milestones/M2-import.md) |
| Requisiti | [FR-024](../requirements.md#fr-024--lotti-di-importazione), [FR-028](../requirements.md#fr-028--limite-delle-attribuzioni) |
| Regole | [DR-017](../domain-rules.md#dr-017--annullamento-di-un-lotto), [DR-010](../domain-rules.md#dr-010--modifica-di-movimenti-attribuiti), [DR-023](../domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo) |
| Dipende da | [US-008](US-008-file-import.md) |
| Questioni collegate | [Q-014](../open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro) (default adottato) |
| DoR | READY |

## Storia

Come utente, voglio poter annullare un'importazione sbagliata, così da
correggere un errore di file o di mappatura senza cancellare i movimenti
uno a uno.

## Esito atteso

Ogni importazione è tracciabile e reversibile, con conferma esplicita
quando l'annullamento tocca dati già lavorati.

## Criteri di accettazione

- **AC-US-010-01** — Dopo la conferma, l'importazione compare nello storico
  del conto con nome del file, data, numero di movimenti importati e di
  righe escluse.
- **AC-US-010-02** — Da un lotto vedo i suoi movimenti; da un movimento
  importato vedo il lotto di provenienza.
- **AC-US-010-03** — Annullando un lotto i cui movimenti non sono stati
  toccati, tutti i suoi movimenti sono eliminati e saldi e report tornano
  ai valori precedenti all'importazione.
- **AC-US-010-04** — Se alcuni movimenti del lotto sono stati modificati,
  categorizzati, attribuiti o abbinati in un giroconto, il sistema mostra
  quanti per ciascun caso e chiede conferma; confermando, le attribuzioni
  sono rimosse e i giroconti sciolti, con l'altro lato che torna movimento
  ordinario del tipo originale.
- **AC-US-010-05** — I movimenti del lotto già eliminati singolarmente sono
  ignorati senza errori.
- **AC-US-010-06** — Un lotto annullato resta nello storico con stato
  "annullato" e non può essere annullato di nuovo.
- **AC-US-010-07** — Dopo l'annullamento, reimportare lo stesso file non
  segnala come duplicati i movimenti eliminati.
- **AC-US-010-08** — I movimenti vincolati del lotto (DR-023) non sono
  eliminati: prima della conferma il sistema ne indica il numero; dopo
  l'annullamento restano nel conto con le loro quote nei nuclei lasciati e
  il lotto annullato ne riporta il conteggio; la loro correzione segue la
  rettifica contabile (DR-023 punto 6), bloccata finché le attribuzioni
  non sono riconciliate esplicitamente.

## Verifica

Test di accettazione automatizzati; confronto di saldi e report prima
dell'importazione e dopo l'annullamento. La parte di AC-04 relativa alle
attribuzioni è verificabile dopo [US-018](US-018-transaction-attribution.md),
AC-08 dopo [US-015](US-015-household-roles-and-members.md).

## Task

- **TASK-031** — Registrazione dei lotti e storico delle importazioni
  (AC-01, AC-02, AC-06).
- **TASK-032** — Annullamento con conferma e gestione di modifiche,
  attribuzioni, giroconti e movimenti vincolati (AC-03 – AC-05, AC-07,
  AC-08).

## Definition of Ready

READY. Il trattamento dei movimenti vincolati (AC-08) segue il default di
[Q-014](../open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro).

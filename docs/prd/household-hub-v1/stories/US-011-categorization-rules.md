# US-011 — Regole di categorizzazione

| Campo | Valore |
|---|---|
| Milestone | [M2 — Importazione](../milestones/M2-import.md) |
| Requisiti | [FR-019](../requirements.md#fr-019--regole-di-categorizzazione) |
| Regole | [DR-008](../domain-rules.md#dr-008--categorie) |
| Dipende da | [US-004](US-004-categories.md), [US-008](US-008-file-import.md) |
| DoR | READY |

## Storia

Come utente, voglio che i movimenti ricorrenti vengano categorizzati in
automatico, così da dedicare il mio tempo solo ai movimenti nuovi.

## Esito atteso

Le regole dello spazio categorizzano i movimenti importati e, su richiesta,
quelli ancora da categorizzare, senza mai sovrascrivere le scelte
dell'utente (metrica SM-02).

## Criteri di accettazione

- **AC-US-011-01** — Con la regola "la descrizione contiene TELEPASS →
  Trasporti › Telepass", le righe importate che contengono "Telepass"
  hanno quella sottocategoria già in anteprima, con indicata la regola
  applicata.
- **AC-US-011-02** — Il confronto ignora maiuscole, minuscole e spazi
  multipli.
- **AC-US-011-03** — Se più regole corrispondono si applica la prima
  nell'ordine definito dall'utente, che può riordinarle.
- **AC-US-011-04** — Su richiesta applico le regole ai movimenti esistenti
  "Da categorizzare": vedo prima quanti saranno categorizzati e i movimenti
  già categorizzati non sono mai modificati.
- **AC-US-011-05** — Posso cambiare la categoria proposta in anteprima o
  dopo l'importazione; la scelta manuale prevale.
- **AC-US-011-06** — Una regola che punta a una categoria archiviata non
  viene applicata ed è segnalata; eliminando una categoria con
  destinazione, le regole passano alla destinazione.
- **AC-US-011-07** — Le regole appartengono allo spazio in cui sono create
  e si applicano solo ai suoi movimenti.

## Verifica

Test di accettazione automatizzati; sui file di esempio di Q-008 misura
della quota di movimenti categorizzati automaticamente al secondo mese.

## Task

- **TASK-033** — Gestione delle regole con priorità (AC-02, AC-03, AC-07).
- **TASK-034** — Applicazione delle regole in anteprima e ai movimenti
  da categorizzare (AC-01, AC-04, AC-05).
- **TASK-035** — Coerenza delle regole con archiviazione ed eliminazione
  delle categorie (AC-06).

## Definition of Ready

READY.

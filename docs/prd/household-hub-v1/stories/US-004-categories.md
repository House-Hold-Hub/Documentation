# US-004 — Categorie e sottocategorie personalizzabili

| Campo | Valore |
|---|---|
| Milestone | [M1 — Analisi mensile personale](../milestones/M1-personal-monthly-analysis.md) |
| Requisiti | [FR-016](../requirements.md#fr-016--tassonomia-personalizzabile-a-due-livelli), [FR-017](../requirements.md#fr-017--tassonomia-iniziale-predefinita), [FR-018](../requirements.md#fr-018--eliminazione-e-unione-di-categorie) |
| Regole | [DR-008](../domain-rules.md#dr-008--categorie) |
| Dipende da | [US-002](US-002-space-isolation.md) |
| DoR | READY |

## Storia

Come utente, voglio organizzare le mie spese ed entrate in categorie e
sottocategorie mie (es. Ristorazione › Aperitivi, Pranzi, Cene; Trasporti ›
Carburante, Telepass), così che l'analisi mensile rifletta le mie abitudini.

## Esito atteso

Ogni spazio ha una tassonomia a due livelli che parte da un modello
predefinito e che l'utente può adattare senza perdere la coerenza dello
storico.

## Criteri di accettazione

- **AC-US-004-01** — Un nuovo spazio contiene la tassonomia predefinita di
  FR-017, con categorie di spesa e di entrata.
- **AC-US-004-02** — Posso creare una categoria indicandone il tipo (spesa
  o entrata) e creare sottocategorie al suo interno; non è possibile
  creare un terzo livello.
- **AC-US-004-03** — Un nome già usato allo stesso livello (tra le
  categorie, o tra le sottocategorie della stessa categoria) è rifiutato.
- **AC-US-004-04** — Rinominare una categoria aggiorna l'etichetta in tutti
  i movimenti e report, inclusi i mesi passati.
- **AC-US-004-05** — Spostare una sottocategoria sotto un'altra categoria
  dello stesso tipo sposta i relativi importi nei report di tutti i mesi; lo
  spostamento verso una categoria di tipo diverso è rifiutato.
- **AC-US-004-06** — Eliminare una categoria o sottocategoria in uso
  richiede di scegliere una destinazione dello stesso tipo; dopo
  l'eliminazione i movimenti puntano alla destinazione e i totali del mese
  restano invariati. Una categoria non in uso si elimina senza destinazione.
- **AC-US-004-07** — Una categoria con sottocategorie può essere eliminata
  solo dopo averle spostate o eliminate.
- **AC-US-004-08** — Una categoria archiviata non è proposta per nuove
  assegnazioni ma resta visibile nei movimenti e nei report esistenti; può
  essere riattivata.

## Verifica

Test di accettazione automatizzati; per AC-04 – AC-06 confronto dei totali
dei report prima e dopo l'operazione.

## Task

- **TASK-011** — Tassonomia predefinita creata con ogni nuovo spazio (AC-01).
- **TASK-012** — Creazione, rinomina, spostamento e archiviazione di
  categorie e sottocategorie (AC-02 – AC-05, AC-08).
- **TASK-013** — Eliminazione con riassegnazione a una destinazione
  (AC-06, AC-07). La riassegnazione di regole e budget è aggiunta da
  [US-011](US-011-categorization-rules.md) e [US-013](US-013-budgets.md).

## Definition of Ready

READY.

# US-016 — Conti, movimenti e categorie del nucleo

| Campo | Valore |
|---|---|
| Milestone | [M4 — Nuclei familiari](../milestones/M4-households.md) |
| Requisiti | [FR-011](../requirements.md#fr-011--conti-del-nucleo), [FR-014](../requirements.md#fr-014--giroconti), [FR-016](../requirements.md#fr-016--tassonomia-personalizzabile-a-due-livelli), NFR-001 |
| Regole | [DR-001](../domain-rules.md#dr-001--appartenenza-delle-risorse), [DR-006](../domain-rules.md#dr-006--giroconti), [DR-007](../domain-rules.md#dr-007--movimenti-tra-spazi-diversi), [Matrice dei permessi](../domain-rules.md#matrice-dei-permessi-del-nucleo) |
| Dipende da | [US-015](US-015-household-roles-and-members.md), [US-003](US-003-personal-accounts.md), [US-004](US-004-categories.md), [US-005](US-005-manual-transactions.md); per importazioni e regole del nucleo (AC-02, AC-03) [US-008](US-008-file-import.md), [US-011](US-011-categorization-rules.md) |
| DoR | READY |

## Storia

Come membro di un nucleo, voglio gestire il conto comune della famiglia con
categorie condivise, così che le spese comuni siano registrate una volta
sola e visibili a tutti i membri.

## Esito atteso

Il nucleo ha conti, movimenti, categorie e regole propri, gestiti secondo
la matrice dei permessi e separati dagli spazi personali.

## Criteri di accettazione

- **AC-US-016-01** — Un amministratore crea il conto del nucleo "Conto
  cointestato": è visibile a tutti i membri e non compare in alcuno spazio
  personale. Un Membro non può creare, archiviare o eliminare conti del
  nucleo.
- **AC-US-016-02** — Ogni membro registra, modifica ed elimina movimenti e
  importa file nei conti del nucleo, con le categorie del nucleo; ogni
  movimento indica il membro che lo ha registrato o importato.
- **AC-US-016-03** — Un amministratore gestisce categorie e regole del
  nucleo; un Membro può solo usarle. Rinominare una categoria del nucleo
  non cambia alcuna categoria personale, e viceversa.
- **AC-US-016-04** — Un giroconto tra due conti del nucleo è neutro nei
  report del nucleo; un conto personale non può essere scelto come
  contropartita di un giroconto del nucleo: un versamento dal conto
  personale al conto del nucleo si registra come trasferimento tra spazi
  in entrambi gli spazi, ciascun lato registrato da chi vi ha accesso (nel
  nucleo anche da un altro membro), neutro nei report di entrambi (DR-007).
- **AC-US-016-05** — Saldo, archiviazione ed eliminazione dei conti del
  nucleo seguono gli stessi criteri di [US-003](US-003-personal-accounts.md).
- **AC-US-016-06** — Chi non è membro non accede a conti, movimenti,
  categorie e regole del nucleo.
- **AC-US-016-07** — Il rimborso a un membro, dal conto del nucleo, di una
  spesa che il membro ha attribuito al nucleo si registra come trasferimento
  tra spazi, da qualsiasi membro e senza accedere al conto personale del
  destinatario: il nucleo conta la spesa una sola volta, tramite la quota
  attribuita, e il saldo del conto del nucleo diminuisce dell'importo
  rimborsato (dataset di [US-019](US-019-household-reports-and-budgets.md)).

## Verifica

Test di accettazione automatizzati con due membri di ruolo diverso e un
non membro; estensione della suite di test negativi.

## Task

- **TASK-048** — Conti del nucleo con permessi per ruolo (AC-01, AC-05, AC-06).
- **TASK-049** — Movimenti, importazioni, giroconti e trasferimenti tra
  spazi nei conti del nucleo con indicazione dell'autore (AC-02, AC-04,
  AC-07).
- **TASK-050** — Tassonomia e regole del nucleo (AC-03).

## Definition of Ready

READY. I conti del nucleo sono una proposta (P) di questo PRD. Le parti di
AC-02 e AC-03 su importazioni e regole richiedono M2.

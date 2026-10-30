# US-006 — Giroconti tra conti

| Campo | Valore |
|---|---|
| Milestone | [M1 — Analisi mensile personale](../milestones/M1-personal-monthly-analysis.md) |
| Requisiti | [FR-012](../requirements.md#fr-012--inserimento-manuale-dei-movimenti), [FR-014](../requirements.md#fr-014--giroconti) |
| Regole | [DR-006](../domain-rules.md#dr-006--giroconti), [DR-007](../domain-rules.md#dr-007--movimenti-tra-spazi-diversi), [DR-010](../domain-rules.md#dr-010--modifica-di-movimenti-attribuiti) |
| Dipende da | [US-005](US-005-manual-transactions.md) |
| DoR | READY |

## Storia

Come utente, voglio registrare gli spostamenti di denaro tra i miei conti
come giroconti, e quelli verso o da un nucleo come trasferimenti tra spazi,
così che non vengano contati come spese o entrate.

## Esito atteso

Giroconti e trasferimenti tra spazi modificano solo i saldi dei conti
coinvolti e non alterano mai i totali dei report.

## Criteri di accettazione

- **AC-US-006-01** — Registro un giroconto di 500,00 € dal conto corrente
  al conto deposito il 10 marzo: il saldo del conto corrente diminuisce di
  500,00 €, quello del conto deposito aumenta di 500,00 € e i totali di
  entrate e uscite di marzo restano invariati.
- **AC-US-006-02** — Non posso scegliere lo stesso conto come origine e
  destinazione, né un conto di un altro spazio: uno spostamento verso un
  altro spazio si registra come trasferimento tra spazi (AC-08).
- **AC-US-006-03** — Modificare importo o data aggiorna entrambi i lati;
  eliminare il giroconto rimuove entrambi i lati dopo conferma.
- **AC-US-006-04** — Un giroconto non ha categoria e non compare tra i
  movimenti "Da categorizzare".
- **AC-US-006-05** — Nell'elenco dei movimenti ogni lato del giroconto è
  riconoscibile e indica il conto di contropartita.
- **AC-US-006-06** — Posso unire un'uscita e un'entrata esistenti di pari
  importo su due conti dello stesso spazio in un giroconto: le loro
  categorie sono rimosse, le date restano quelle originali e, se uno dei
  due movimenti ha attribuzioni verso nuclei di cui sono membro attivo, il
  sistema chiede conferma indicando i nuclei coinvolti; un movimento
  vincolato (DR-023) si unisce solo con la rettifica contabile.
- **AC-US-006-07** — Posso sciogliere un giroconto: i due lati tornano
  movimenti ordinari "Da categorizzare".
- **AC-US-006-08** — Registro un'uscita di 300,00 € dal mio conto corrente
  come trasferimento tra spazi verso il nucleo A: il saldo del conto
  diminuisce di 300,00 €; il movimento non ha categoria, non compare tra le
  uscite, nei budget né tra i "Da categorizzare" e non può essere
  attribuito. Posso trasformare un movimento ordinario in trasferimento tra
  spazi e viceversa, con le conferme di DR-010; un movimento vincolato si
  trasforma solo con la rettifica contabile.

## Verifica

Test di accettazione automatizzati; il dataset di verifica dei report
([US-007](US-007-monthly-report.md)) include giroconti. AC-06 per i
movimenti attribuiti è verificabile dopo US-018 e per i movimenti
vincolati dopo US-015; AC-08 richiede un nucleo ed è verificato in M4, dopo
[US-014](US-014-household-creation-and-invitations.md).

## Task

- **TASK-017** — Registrazione, modifica ed eliminazione dei giroconti
  (AC-01 – AC-05).
- **TASK-018** — Unione di due movimenti in giroconto e scioglimento
  (AC-06, AC-07).
- **TASK-081** — Trasferimenti tra spazi: registrazione, trasformazione da
  e verso movimento ordinario ed esclusione dai totali (AC-02, AC-08).

## Definition of Ready

READY.

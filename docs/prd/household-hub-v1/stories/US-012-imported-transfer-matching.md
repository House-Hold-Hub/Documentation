# US-012 — Abbinamento dei giroconti importati

| Campo | Valore |
|---|---|
| Milestone | [M2 — Importazione](../milestones/M2-import.md) |
| Requisiti | [FR-025](../requirements.md#fr-025--abbinamento-dei-giroconti-importati) |
| Regole | [DR-006](../domain-rules.md#dr-006--giroconti), [DR-007](../domain-rules.md#dr-007--movimenti-tra-spazi-diversi) |
| Dipende da | [US-006](US-006-transfers.md), [US-008](US-008-file-import.md) |
| Questioni collegate | [Q-010](../open-questions-and-risks.md#q-010--criteri-dei-duplicati) (tolleranza sulle date, non bloccante) |
| DoR | READY |

## Storia

Come utente che importa gli estratti di più conti, voglio che gli
spostamenti tra i miei conti vengano riconosciuti come giroconti, così che
non risultino come spese ed entrate.

## Esito atteso

Le coppie uscita/entrata tra conti dello stesso spazio sono proposte come
giroconti e, dopo conferma, escono dai totali dei report.

## Criteri di accettazione

- **AC-US-012-01** — Importata un'uscita di 300,00 € il 3 aprile sul conto
  A e, anche in un'importazione successiva, un'entrata di 300,00 € il
  4 aprile sul conto B dello stesso spazio, il sistema propone di abbinarle.
  Sono candidate le coppie con stesso importo e date entro ±3 giorni.
- **AC-US-012-02** — Confermando, le due righe diventano un giroconto:
  spariscono dai totali di entrate e uscite, ogni lato mantiene la propria
  data e i saldi dei conti non cambiano.
- **AC-US-012-03** — Rifiutando, la stessa coppia non viene più proposta.
- **AC-US-012-04** — Non sono proposte coppie tra conti di spazi diversi,
  movimenti già parte di un giroconto, trasferimenti tra spazi o movimenti
  con attribuzioni, comprese quelle verso nuclei lasciati.
- **AC-US-012-05** — Se per un movimento esistono più candidati, scelgo io
  quale abbinare.
- **AC-US-012-06** — Le proposte compaiono nel riepilogo dell'importazione
  e in un elenco consultabile finché non sono confermate o rifiutate.

## Verifica

Test di accettazione automatizzati con due conti e importazioni separate;
verifica dei totali del report prima e dopo la conferma.

## Task

- **TASK-036** — Individuazione delle coppie candidate (AC-01, AC-04, AC-05).
- **TASK-037** — Conferma, rifiuto ed elenco delle proposte (AC-02, AC-03, AC-06).

## Definition of Ready

READY. Perimetro MVP: rinviabile; l'unione manuale di AC-US-006-06 copre il
caso ([roadmap](../roadmap.md#perimetro-dellmvp)).

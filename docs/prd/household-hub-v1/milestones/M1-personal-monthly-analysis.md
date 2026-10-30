# M1 — Analisi mensile personale

[← PRD](../README.md) · Precedente: [M0](M0-foundation.md) · Successive: [M2](M2-import.md), [M3](M3-budgets.md)

## Esito

Un utente gestisce i propri conti, la propria tassonomia di categorie e
sottocategorie, registra entrate, uscite e giroconti e ottiene il report
mensile per categoria, senza doppi conteggi. È la priorità di prodotto
(obiettivo G-1) ed è utilizzabile da sola per uso individuale.

## Dipendenze

- [M0](M0-foundation.md).

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

- Criteri di accettazione di US-003 – US-007 soddisfatti, escluso
  AC-US-007-05 se rinviato; AC-US-006-08 (trasferimenti tra spazi) è
  verificato in M4.
- Dataset di verifica dei report (giroconti, rimborsi, movimenti da
  categorizzare, importi frazionari) definito e superato, inclusa la
  quadratura dei saldi (DR-012 punto 7): sarà riusato in M3 ed esteso in
  M4 con i trasferimenti tra spazi.
- NFR-004, NFR-005 e NFR-006 verificati per il report mensile.

## Rischi principali

- [RISK-002](../open-questions-and-risks.md#rischi): correttezza dei totali.

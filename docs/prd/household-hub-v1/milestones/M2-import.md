# M2 — Importazione

[← PRD](../README.md) · Precedente: [M1](M1-personal-monthly-analysis.md)

## Esito

Un utente importa l'estratto conto CSV o Excel della propria banca, evita
i duplicati, può annullare un'importazione, ottiene la categorizzazione
automatica tramite regole e trasforma in giroconti le coppie di movimenti
tra propri conti. Riduce lo sforzo mensile (obiettivo G-4, metriche SM-01 e
SM-02).

## Dipendenze

- [M1](M1-personal-monthly-analysis.md). Indipendente da [M3](M3-budgets.md).
- File di esempio delle banche prioritarie per la verifica ([Q-008](../open-questions-and-risks.md#q-008--banche-prioritarie-e-file-di-esempio)).

## Storie

| Ordine | Storia | Dipende da | DoR |
|---|---|---|---|
| 1 | [US-008 — Importazione CSV/Excel](../stories/US-008-file-import.md) | US-005 | READY |
| 2 | [US-009 — Rilevamento duplicati](../stories/US-009-duplicate-detection.md) | US-008 | READY |
| 2 | [US-010 — Lotti di importazione annullabili](../stories/US-010-import-batches.md) | US-008 | READY |
| 2 | [US-011 — Regole di categorizzazione](../stories/US-011-categorization-rules.md) | US-004, US-008 | READY |
| 3 | [US-012 — Abbinamento dei giroconti importati](../stories/US-012-imported-transfer-matching.md) | US-006, US-008 | READY (rinviabile) |

US-009, US-010 e US-011 sono indipendenti tra loro dopo US-008.

## Criterio di completamento

- Criteri di accettazione di US-008 – US-012 soddisfatti con i file di
  esempio di Q-008, esclusi il formato .xls e US-012 se rinviati.
- NFR-006 (anteprima) e NFR-011 verificati.
- Abbinamento uno a uno dei duplicati verificato (AC-US-009-09);
  AC-US-010-08 sui movimenti vincolati è verificato dopo M4.
- US-012 è rinviabile ([perimetro](../roadmap.md#perimetro-dellmvp)): se
  rinviata non blocca il completamento.

## Rischi principali

- [RISK-003](../open-questions-and-risks.md#rischi) eterogeneità dei file,
  [RISK-004](../open-questions-and-risks.md#rischi) duplicati,
  [RISK-006](../open-questions-and-risks.md#rischi) annullamento dei lotti.

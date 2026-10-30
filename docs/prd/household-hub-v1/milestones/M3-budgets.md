# M3 — Budget

[← PRD](../README.md) · Precedente: [M1](M1-personal-monthly-analysis.md) · Successiva: [M4](M4-households.md)

## Esito

Un utente pianifica quanto spendere ogni mese per categoria o sottocategoria
e confronta previsto e consuntivo (obiettivo G-2). Le stesse regole saranno
riusate dai budget del nucleo in [US-019](../stories/US-019-household-reports-and-budgets.md).

## Dipendenze

- [M1](M1-personal-monthly-analysis.md) (report mensile come fonte del
  consuntivo). Indipendente da [M2](M2-import.md).

## Storie

| Ordine | Storia | Dipende da | DoR |
|---|---|---|---|
| 1 | [US-013 — Budget mensili](../stories/US-013-budgets.md) | US-007 | READY |

## Criterio di completamento

- Criteri di accettazione di US-013 soddisfatti.
- Dataset di verifica di M1 esteso con voci di budget su categorie e
  sottocategorie, incluso il caso con voci solo su sottocategorie
  (AC-US-013-10).

## Rischi principali

- [RISK-002](../open-questions-and-risks.md#rischi): doppio conteggio tra
  budget di categoria e di sottocategoria.

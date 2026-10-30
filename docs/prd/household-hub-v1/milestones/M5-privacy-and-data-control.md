# M5 — Privacy e controllo dei dati

[← PRD](../README.md) · Precedente: [M4](M4-households.md)

## Esito

Ogni utente può portare via i propri dati e quelli dei nuclei di cui è
membro, eliminare il proprio account e
vedere chi ha cambiato visibilità o appartenenza nei propri spazi. Chiude
l'MVP implementato; con il gate di Q-012 lo rende autorizzato all'uso reale
e apribile a utenti esterni ([livelli di rilascio](../roadmap.md#livelli-di-rilascio)).

## Dipendenze

- [M4](M4-households.md): esportazione, eliminazione e registro devono
  coprire anche nuclei, condivisioni e attribuzioni.

## Storie

| Ordine | Storia | Dipende da | DoR |
|---|---|---|---|
| 1 | [US-020 — Esportazione dei dati](../stories/US-020-data-export.md) | US-015, US-016, US-018 | READY |
| 1 | [US-022 — Registro attività di condivisione](../stories/US-022-activity-log.md) | US-015, US-017 (parti: US-020; registro completo: US-014, US-018) | READY; audit minimo indispensabile, registro completo rinviabile |
| 2 | [US-021 — Eliminazione dell'account](../stories/US-021-account-deletion.md) | US-015, US-016, US-018, US-020, US-022 | READY per la progettazione; implementazione definitiva e uso con dati reali dopo il gate di Q-012 |

## Criterio di completamento

- Criteri di accettazione di US-020 – US-022 soddisfatti, esclusi quelli del
  registro completo se rinviato (AC-US-022-02, AC-US-022-03,
  AC-US-022-07) e la voce di AC-US-022-01 sulle riconciliazioni di quote
  di ex membri finché Q-014 non le autorizza; verificate le parti di
  US-015 rinviate a M5 e le voci dell'audit minimo sulle azioni di M4.
- Accesso del personale (NFR-013) verificato.
- Revisione privacy (NFR-010) e prova di ripristino (NFR-012) completate,
  inclusa la riapplicazione delle eliminazioni di account.
- [gate di utilizzo](../open-questions-and-risks.md#gate-di-utilizzo) di [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione)
  superato prima di usare con dati reali i trattamenti interessati e quindi
  prima di autorizzare M4 e M5 all'uso reale (livello 2, [livelli di rilascio](../roadmap.md#livelli-di-rilascio));
  se la valutazione esclude la base
  giuridica proposta, US-021 adotta il ripiego di DR-024 e DR-023 va
  rivisto.

## Rischi principali

- [RISK-009](../open-questions-and-risks.md#rischi) riferimenti residui all'utente eliminato,
  [RISK-010](../open-questions-and-risks.md#rischi) ricalcolo dei report storici nel ripiego,
  [RISK-011](../open-questions-and-risks.md#rischi) esito negativo della valutazione legale,
  [RISK-012](../open-questions-and-risks.md#rischi) riconoscibilità delle quote storiche,
  [RISK-006](../open-questions-and-risks.md#rischi) perdita di dati,
  [RISK-005](../open-questions-and-risks.md#rischi) privacy delle attribuzioni,
  [RISK-014](../open-questions-and-risks.md#rischi) avvisi che rivelano un'opposizione,
  [RISK-017](../open-questions-and-risks.md#rischi) accessi del personale.

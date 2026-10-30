# M0 — Fondamenta

[← PRD](../README.md) · Successiva: [M1](M1-personal-monthly-analysis.md)

## Esito

Una persona si registra, accede in sicurezza e trova uno spazio personale
privato. Ogni accesso ai dati è vincolato allo spazio di appartenenza, base
di tutte le milestone successive.

## Dipendenze

- Nessuna milestone precedente.
- Prerequisito esterno: decisioni di architettura ([Q-011](../open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico)),
  soddisfatto: Q-011 è chiusa con l'approvazione di ADR-001 – ADR-006
  ([documento di architettura](../../../architecture/household-hub-v1/README.md)).

## Storie

| Ordine | Storia | DoR |
|---|---|---|
| 1 | [US-001 — Registrazione, accesso e spazio personale](../stories/US-001-registration-and-personal-space.md) | READY |
| 2 | [US-002 — Isolamento degli spazi](../stories/US-002-space-isolation.md) | READY |

## Criterio di completamento

- Criteri di accettazione di US-001 e US-002 soddisfatti.
- NFR-001, NFR-002 e NFR-003 verificati sulle funzioni della milestone; per
  NFR-003 la verifica in due passaggi degli utenti (AC-US-001-08) è esclusa
  se rinviata ([perimetro](../roadmap.md#perimetro-dellmvp)). La sezione
  sullo storico dei nuclei di AC-US-001-09 è verificata in M4.
- Verifiche architetturali da completare durante M0 chiuse
  ([elenco](../../../architecture/household-hub-v1/README.md#da-completare-durante-m0)),
  escluse le parti che dipendono dalla scelta dell'hosting.

## Rischi principali

- [RISK-001](../open-questions-and-risks.md#rischi): l'isolamento definito qui
  è riusato da ogni storia; un difetto si propaga ovunque.

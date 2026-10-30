# M4 — Nuclei familiari

[← PRD](../README.md) · Precedenti: [M1](M1-personal-monthly-analysis.md), [M2](M2-import.md), [M3](M3-budgets.md) · Successiva: [M5](M5-privacy-and-data-control.md)

## Esito

Gli utenti creano nuclei, invitano membri, gestiscono ruoli e conti comuni,
condividono in sola lettura i propri conti e attribuiscono al nucleo, anche
in parte, le spese pagate da conti personali. Il nucleo ottiene report e
budget propri senza doppi conteggi e senza esporre i conti personali
(obiettivo G-3).

## Dipendenze

- [M1](M1-personal-monthly-analysis.md) per conti, categorie, movimenti e report.
- [M3](M3-budgets.md) per la parte budget di US-019.
- [M2](M2-import.md) per importazioni e regole nei conti del nucleo
  (US-016).
- Autorizzazione all'uso reale (livello 2, [livelli di rilascio](../roadmap.md#livelli-di-rilascio)) solo insieme a
  [M5](M5-privacy-and-data-control.md)
  e dopo il [gate di utilizzo](../open-questions-and-risks.md#gate-di-utilizzo) di Q-012.

## Storie

| Ordine | Storia | Dipende da | DoR |
|---|---|---|---|
| 1 | [US-014 — Creazione del nucleo e inviti](../stories/US-014-household-creation-and-invitations.md) | US-002 | READY |
| 2 | [US-015 — Ruoli e gestione dei membri](../stories/US-015-household-roles-and-members.md) | US-014 (parti: US-017, US-018, US-020 – US-022) | READY per la progettazione; gate di Q-012 |
| 3 | [US-016 — Conti, movimenti e categorie del nucleo](../stories/US-016-household-accounts-and-categories.md) | US-015, US-003, US-004, US-005 (parti: US-008, US-011) | READY |
| 3 | [US-017 — Condivisione in sola lettura](../stories/US-017-read-only-sharing.md) | US-015, US-003 | READY |
| 4 | [US-018 — Attribuzione dei movimenti al nucleo](../stories/US-018-transaction-attribution.md) | US-016 (parti: US-015) | READY; AC-11 dopo il gate di Q-012 |
| 5 | [US-019 — Report e budget del nucleo](../stories/US-019-household-reports-and-budgets.md) | US-016, US-017, US-018, US-013 | READY |

US-016 e US-017 sono indipendenti tra loro.

## Criterio di completamento

- Criteri di accettazione di US-014 – US-019 soddisfatti, salvo le parti
  che dipendono da storie di M5 (AC-US-015-03 per le voci del registro
  completo, se realizzato; AC-US-015-07 e AC-US-015-13 per
  l'esportazione; AC-US-015-10), verificate al completamento di M5. Le
  voci dell'audit minimo sulle azioni di US-015 e US-017 sono verificate
  in M5 con AC-US-022-01.
- Revisione di sicurezza dell'isolamento tra spazi e nuclei (NFR-001)
  con esito positivo.
- Dataset di verifica esteso con un conto condiviso che ha anche movimenti
  attribuiti, attribuzioni parziali a due nuclei, giroconti, trasferimenti
  tra spazi, rimborso a un membro, uscita e rientro di un membro con
  movimento vincolato e rettifica contabile bloccata e poi riconciliata
  esplicitamente, senza riduzioni automatiche; capienza e quadratura dei
  saldi (DR-012 punti 7 e 8) verificate.
- AC-US-006-08 (trasferimenti tra spazi nello spazio personale) e
  AC-US-001-09 (sezione sullo storico dei nuclei) verificati.

## Rischi principali

- [RISK-001](../open-questions-and-risks.md#rischi) esposizione di dati,
  [RISK-002](../open-questions-and-risks.md#rischi) doppi conteggi,
  [RISK-005](../open-questions-and-risks.md#rischi) deduzioni dalle attribuzioni,
  [RISK-015](../open-questions-and-risks.md#rischi) movimenti vincolati,
  [RISK-016](../open-questions-and-risks.md#rischi) errori nei trasferimenti tra spazi,
  [RISK-018](../open-questions-and-risks.md#rischi) perdita di accesso ai dati comuni,
  [RISK-019](../open-questions-and-risks.md#rischi) rettifiche contabili senza errore reale,
  [RISK-020](../open-questions-and-risks.md#rischi) trasferimenti dichiarati impropriamente.

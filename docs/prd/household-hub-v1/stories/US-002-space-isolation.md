# US-002 — Isolamento degli spazi

| Campo | Valore |
|---|---|
| Milestone | [M0 — Fondamenta](../milestones/M0-foundation.md) |
| Requisiti | [FR-002](../requirements.md#fr-002--spazio-personale-privato), [FR-005](../requirements.md#fr-005--appartenenza-a-più-nuclei), NFR-001, NFR-002 |
| Regole | [DR-001](../domain-rules.md#dr-001--appartenenza-delle-risorse), [DR-002](../domain-rules.md#dr-002--privacy-per-default), [DR-003](../domain-rules.md#dr-003--isolamento-degli-spazi) |
| Dipende da | [US-001](US-001-registration-and-personal-space.md) |
| DoR | READY |

## Storia

Come utente, voglio che i miei dati siano accessibili solo a chi ne ha
diritto e sapere sempre in quale spazio sto lavorando, così da potermi
fidare del servizio.

## Esito atteso

Ogni risorsa appartiene a un solo spazio e ogni accesso è verificato
rispetto a quello spazio. Le storie successive ereditano questa regola e ne
estendono la verifica.

## Criteri di accettazione

- **AC-US-002-01** — Dati due utenti A e B, A non può leggere, modificare
  né eliminare alcuna risorsa dello spazio personale di B, neanche usando un
  riferimento diretto alla risorsa; l'esito è identico a quello di una
  risorsa inesistente.
- **AC-US-002-02** — Ogni risorsa creata è associata allo spazio attivo e
  nessuna modifica successiva può spostarla in un altro spazio.
- **AC-US-002-03** — L'interfaccia mostra sempre lo spazio attivo; il
  selettore elenca solo gli spazi a cui l'utente ha accesso (in M0 il solo
  spazio personale; i nuclei si aggiungono con US-014).
- **AC-US-002-04** — Elenchi, ricerche, report ed esportazioni restituiscono
  solo dati degli spazi autorizzati, anche quando i filtri sono manipolati.
- **AC-US-002-05** — Un utente non autenticato non accede ad alcun dato.

## Verifica

Una suite di test negativi riusabile (utente esterno, utente non
autenticato, riferimento diretto a risorse altrui) da estendere in ogni
storia successiva con le nuove funzioni e, da M4, con i casi ex membro e
membro di altro nucleo.

## Task

- **TASK-005** — Associare ogni risorsa a uno spazio e verificare il
  diritto sullo spazio a ogni lettura e scrittura (AC-01, AC-02, AC-04, AC-05).
- **TASK-006** — Indicazione dello spazio attivo e selettore degli spazi (AC-03).
- **TASK-007** — Suite di test negativi di accesso riusabile (tutti gli AC).

## Definition of Ready

READY.

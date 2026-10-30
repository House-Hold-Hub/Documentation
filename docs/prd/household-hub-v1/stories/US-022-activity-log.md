# US-022 — Registro attività di condivisione

| Campo | Valore |
|---|---|
| Milestone | [M5 — Privacy e controllo dei dati](../milestones/M5-privacy-and-data-control.md) |
| Requisiti | [FR-043](../requirements.md#fr-043--registro-attività), NFR-001 |
| Regole | [DR-004](../domain-rules.md#dr-004--condivisione-in-sola-lettura), [DR-009](../domain-rules.md#dr-009--attribuzioni), [DR-023](../domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo), [DR-025](../domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo), [DR-026](../domain-rules.md#dr-026--tutela-dei-dati-condivisi-del-nucleo) |
| Dipende da | Audit minimo: [US-015](US-015-household-roles-and-members.md), [US-017](US-017-read-only-sharing.md); per le esportazioni del nucleo [US-020](US-020-data-export.md). Registro completo: anche [US-014](US-014-household-creation-and-invitations.md) e [US-018](US-018-transaction-attribution.md) |
| Questioni collegate | [Q-004](../open-questions-and-risks.md#q-004--attribuzioni-di-un-membro-uscito) (decisa), [Q-014](../open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro) |
| DoR | READY |

## Storia

Come utente e come membro di un nucleo, voglio sapere chi ha cambiato
visibilità o composizione dei miei spazi, così da accorgermi di cambiamenti
inattesi.

## Esito atteso

Un audit minimo, indispensabile nell'MVP, consultabile e non modificabile,
delle azioni che cambiano chi accede ai dati comuni o li proteggono; il
registro completo delle altre azioni di visibilità è rinviabile.

## Criteri di accettazione

- **AC-US-022-01** — Audit minimo. Nell'audit minimo del nucleo compaiono,
  con data, ora e autore: ingressi, uscite e rimozioni; cambi di ruolo;
  condivisioni e revoche di conti verso il nucleo; avvio, annullamento,
  scadenza e decadenza dei preavvisi di rimozione o declassamento di
  amministratori e di eliminazione del nucleo; esportazioni dei dati del
  nucleo; riconciliazioni di quote di ex membri nelle rettifiche
  contabili, indicate come "ex membro", quando Q-014 le autorizza (DR-023,
  DR-026). Le voci su ingressi, uscite, rimozioni e cambi
  di ruolo riportano il nome del membro anche dopo la sua uscita (DR-023
  punto 2).
- **AC-US-022-02** — Registro completo (rinviabile). Nel registro del mio
  spazio personale compaiono le condivisioni e revoche dei miei conti e le
  attribuzioni che ho creato, modificato o rimosso, con il nucleo
  interessato.
- **AC-US-022-03** — Registro completo (rinviabile). Le voci relative alle
  attribuzioni non riportano più informazioni di quelle visibili secondo
  FR-029; dopo l'uscita dell'autore dal nucleo mostrano "ex membro" al posto
  del nome (DR-023).
- **AC-US-022-04** — Nessun utente, amministratori compresi, può modificare
  o eliminare le voci dell'audit minimo o del registro; le voci sono rimosse
  solo per effetto dell'eliminazione di un account
  ([DR-024](../domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo)).
- **AC-US-022-05** — Audit minimo e registro di un nucleo sono visibili solo
  ai suoi membri attivi; un ex membro non li vede più.
- **AC-US-022-06** — Opposizioni e decisioni sulle opposizioni non
  compaiono nei registri visibili ai membri: sono tracciate solo nel
  registro delle opposizioni, accessibile ai referenti autorizzati (DR-025).
- **AC-US-022-07** — Registro completo (rinviabile). Nel registro del nucleo
  compaiono inoltre inviti inviati, revocati, accettati e rifiutati,
  attribuzioni create, modificate e rimosse e rinomina del nucleo.

## Verifica

Test di accettazione automatizzati che eseguono ciascuna azione e
controllano la voce registrata; estensione della suite di test negativi.
Le azioni di M4 sono verificate qui, al completamento di M5; la voce sulle
riconciliazioni di quote di ex membri si verifica quando Q-014 le
autorizza.

## Task

- **TASK-067** — Audit minimo: registrazione delle azioni di AC-01.
- **TASK-068** — Consultazione dell'audit e del registro con permessi e
  immutabilità (AC-04 – AC-06).
- **TASK-086** — Registro completo: voci aggiuntive del nucleo e registro
  dello spazio personale (AC-02, AC-03, AC-07).

## Definition of Ready

READY. Perimetro MVP, confermato il 2026-10-28: l'audit minimo (AC-01,
AC-04 – AC-06) è indispensabile; il registro completo (AC-02, AC-03, AC-07) è rinviabile
([roadmap](../roadmap.md#perimetro-dellmvp)). Se rinviato, le parti di DR-023 e DR-024 sulle voci delle
attribuzioni si applicano quando viene realizzato.

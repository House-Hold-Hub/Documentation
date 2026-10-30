# US-014 — Creazione del nucleo e inviti

| Campo | Valore |
|---|---|
| Milestone | [M4 — Nuclei familiari](../milestones/M4-households.md) |
| Requisiti | [FR-003](../requirements.md#fr-003--creazione-di-un-nucleo-familiare), [FR-004](../requirements.md#fr-004--inviti-al-nucleo), [FR-005](../requirements.md#fr-005--appartenenza-a-più-nuclei), [FR-044](../requirements.md#fr-044--informativa-sullo-storico-del-nucleo), NFR-001 |
| Regole | [DR-003](../domain-rules.md#dr-003--isolamento-degli-spazi), [Matrice dei permessi](../domain-rules.md#matrice-dei-permessi-del-nucleo) |
| Dipende da | [US-002](US-002-space-isolation.md) |
| Questioni collegate | [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione) (sezione sullo storico del nucleo dell'informativa, gate di utilizzo) |
| DoR | READY |

## Storia

Come utente, voglio creare un nucleo familiare e invitarvi le persone con
cui condivido le spese, così da gestire insieme le finanze comuni.

## Esito atteso

Nuclei creati, membri entrati solo tramite inviti accettati, isolamento
netto tra nuclei e tra nucleo e spazi personali.

## Criteri di accettazione

- **AC-US-014-01** — Creo il nucleo "Famiglia Rossi": ne divento
  amministratore, compare nel selettore degli spazi e contiene la
  tassonomia predefinita e nessun conto.
- **AC-US-014-02** — Come amministratore invito un indirizzo email:
  l'invitato riceve un messaggio e io vedo l'invito in attesa con la data
  di scadenza.
- **AC-US-014-03** — Un utente che ha effettuato l'accesso con l'indirizzo
  invitato accetta l'invito e diventa membro con ruolo Membro; chi non ha
  ancora un account può registrarsi con quell'indirizzo e poi accettare.
- **AC-US-014-04** — Un invito non può essere accettato da un account con
  indirizzo diverso da quello invitato.
- **AC-US-014-05** — Un invito scaduto (oltre 7 giorni) o revocato
  dall'amministratore non è più accettabile; l'invitato può rifiutarlo
  esplicitamente.
- **AC-US-014-06** — Invitare un indirizzo che appartiene già a un membro
  è rifiutato; un Membro non può inviare inviti.
- **AC-US-014-07** — Un utente membro dei nuclei A e B passa dall'uno
  all'altro; nessuna risorsa di A è visibile o raggiungibile, anche con
  riferimento diretto, mentre lavora in B, e viceversa.
- **AC-US-014-08** — Entrare in un nucleo non rende visibile alcuna risorsa
  personale: gli altri membri vedono solo nome e indirizzo email del nuovo
  membro.
- **AC-US-014-09** — Prima di accettare un invito vedo l'informativa di
  FR-044 sullo storico del nucleo; non mi viene chiesto un consenso.

## Verifica

Test di accettazione automatizzati; estensione della suite di test negativi
di [US-002](US-002-space-isolation.md) con i casi "membro di altro nucleo"
e "invitato non ancora membro".

## Task

- **TASK-042** — Creazione del nucleo con tassonomia predefinita (AC-01).
- **TASK-043** — Inviti: invio, scadenza, revoca, accettazione e rifiuto
  (AC-02 – AC-06).
- **TASK-044** — Estensione dei test di isolamento ai nuclei (AC-07, AC-08).
- **TASK-082** — Informativa sullo storico del nucleo all'ingresso (AC-09).

## Definition of Ready

READY. La sezione sullo storico del nucleo (AC-09) va validata con Q-012 prima
dell'uso con utenti reali.

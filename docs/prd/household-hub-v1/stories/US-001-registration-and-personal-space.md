# US-001 — Registrazione, accesso e spazio personale

| Campo | Valore |
|---|---|
| Milestone | [M0 — Fondamenta](../milestones/M0-foundation.md) |
| Requisiti | [FR-001](../requirements.md#fr-001--registrazione-e-accesso), [FR-002](../requirements.md#fr-002--spazio-personale-privato), [FR-044](../requirements.md#fr-044--informativa-sullo-storico-del-nucleo), NFR-003, NFR-010 |
| Regole | [DR-002](../domain-rules.md#dr-002--privacy-per-default) |
| Dipende da | — |
| Questioni collegate | [Q-002](../open-questions-and-risks.md#q-002--registrazione-aperta-o-su-invito) (non bloccante); [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione) (sezione sullo storico dei nuclei dell'informativa, gate di utilizzo) |
| DoR | READY |

## Storia

Come persona che vuole gestire le proprie finanze, voglio registrarmi e
accedere in sicurezza, così da avere uno spazio personale privato.

## Esito atteso

Una persona registrata e verificata accede al proprio spazio personale;
nessun altro può farlo al suo posto.

## Criteri di accettazione

- **AC-US-001-01** — Dato un indirizzo email non registrato, quando completo
  la registrazione e confermo l'indirizzo tramite il messaggio ricevuto,
  allora posso accedere e trovo il mio spazio personale.
- **AC-US-001-02** — Finché l'indirizzo non è confermato non posso accedere
  allo spazio personale; posso richiedere un nuovo messaggio di conferma.
- **AC-US-001-03** — Quando provo a registrare un indirizzo già in uso, la
  risposta mostrata è identica a quella di una registrazione riuscita e il
  titolare dell'indirizzo riceve un avviso: non è possibile scoprire quali
  indirizzi sono registrati.
- **AC-US-001-04** — Una password che non rispetta i requisiti minimi di
  robustezza è rifiutata con l'indicazione del requisito mancante.
- **AC-US-001-05** — Dopo ripetuti tentativi di accesso falliti sullo
  stesso account, ulteriori tentativi sono temporaneamente limitati.
- **AC-US-001-06** — Il recupero dell'accesso invia un collegamento monouso
  con scadenza; dopo il cambio password tutte le altre sessioni attive
  sono chiuse. Un collegamento scaduto o già usato è rifiutato.
- **AC-US-001-07** — Una sessione inattiva per 30 minuti scade; l'uscita
  esplicita invalida la sessione corrente.
- **AC-US-001-08** — Posso attivare la verifica in due passaggi; quando è
  attiva, l'accesso la richiede sempre.
- **AC-US-001-09** — Durante la registrazione vedo l'informativa sul
  trattamento dei dati (NFR-010) e, quando i nuclei sono disponibili (M4),
  la sezione sullo storico dei nuclei di FR-044; entrambe restano
  consultabili e non mi viene chiesto un consenso. Se mi sono registrato
  prima di M4, vedo la sezione all'ingresso nel primo nucleo
  (AC-US-014-09).

## Verifica

Test di accettazione automatizzati per ciascun criterio, inclusi i casi di
errore; verifica manuale del flusso completo da desktop e smartphone
(NFR-007).

## Task

- **TASK-001** — Registrazione con conferma dell'email e creazione dello
  spazio personale (AC-01, AC-02, AC-03, AC-04).
- **TASK-002** — Accesso, uscita, scadenza per inattività e limitazione dei
  tentativi (AC-05, AC-07).
- **TASK-003** — Recupero dell'accesso con collegamento monouso (AC-06).
- **TASK-004** — Verifica in due passaggi opzionale (AC-08).
- **TASK-080** — Informativa sul trattamento e sezione sullo storico dei
  nuclei alla registrazione (AC-09).

## Definition of Ready

READY. La modalità di registrazione segue il default di Q-002 (aperta);
se il product owner sceglie la registrazione su invito cambiano AC-01 e
AC-03.
La sezione sullo storico dei nuclei di AC-09 va validata con Q-012 prima
dell'uso con utenti reali; l'informativa generale non dipende da Q-012 ed è
verificata con la revisione privacy di NFR-010. Perimetro MVP: AC-08 (verifica in due passaggi) è
rinviabile ([roadmap](../roadmap.md#perimetro-dellmvp)).

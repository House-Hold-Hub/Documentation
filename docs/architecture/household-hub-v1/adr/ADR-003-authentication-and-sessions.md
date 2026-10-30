# ADR-003 — Autenticazione e sessioni

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato** (2026-10-30) |
| Data | 2026-10-30 |
| Decisore | mdellapa (product owner) |
| Questione | [Q-011](../../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Requisiti | [FR-001](../../../prd/household-hub-v1/requirements.md#fr-001--registrazione-e-accesso), NFR-003, NFR-010, NFR-013; [US-001](../../../prd/household-hub-v1/stories/US-001-registration-and-personal-space.md); AC-US-020-05, AC-US-021-01, AC-US-021-04 |
| Correlati | [ADR-002](ADR-002-stack-and-server-rendered-ui.md), [ADR-004](ADR-004-space-isolation-and-authorization.md) |

## Contesto

US-001 richiede registrazione con email verificata, risposte che non rivelano
gli indirizzi registrati, password robuste, limitazione dei tentativi,
recupero con collegamento monouso, chiusura delle altre sessioni al cambio
password e scadenza dopo 30 minuti di inattività. M5 richiede una nuova
verifica dell'identità per esportazione ed eliminazione, e la chiusura
immediata di tutte le sessioni all'eliminazione dell'account. Il referente
(M5) deve usare la verifica in due passaggi.

## Decisione

### Libreria e perimetro

- Autenticazione nell'applicazione con **django-allauth** (versione in
  [ADR-002](ADR-002-stack-and-server-rendered-ui.md)), sopra il sistema di
  autenticazione di Django. Nessun identity provider esterno, nessun JWT.
- Accesso con email e password; email unica e verifica obbligatoria.
- Accesso tramite social non installato (`allauth.socialaccount` assente).
- Opzione "ricordami" disattivata: sarebbe in conflitto con il timeout di
  inattività.

### Corrispondenza con i criteri di US-001

| Criterio | Meccanismo |
|---|---|
| AC-US-001-01, 02 — verifica email | Verifica obbligatoria; reinvio del messaggio disponibile |
| AC-US-001-03 — nessuna enumerazione | Protezione dall'enumerazione di allauth: stessa risposta e messaggio al titolare dell'indirizzo già registrato |
| AC-US-001-04 — robustezza password | Validatori di Django (lunghezza minima iniziale 12, password comuni, solo numeri, somiglianza con i dati dell'utente), con messaggio sul requisito mancante |
| AC-US-001-05 — tentativi ripetuti | Limiti di allauth per IP e per account, su una cache condivisa da tutti i processi |
| AC-US-001-06 — recupero e altre sessioni | Collegamento con scadenza (valore iniziale: 1 ora) invalidato dal cambio password; le altre sessioni sono invalidate dal cambio dell'impronta della password nella sessione |
| AC-US-001-07 — inattività e uscita | Sessione con scadenza scorrevole di 30 minuti; l'uscita cancella la sessione |
| AC-US-001-08 — verifica in due passaggi (rinviabile) | TOTP con codici di recupero di `allauth.mfa`; esposizione agli utenti decisa con DEF-014 |

### Sessioni

- **Sessioni lato server** nel database. Il cookie contiene solo
  l'identificativo, con attributi `Secure`, `HttpOnly`, `SameSite=Lax`.
- **Timeout di inattività**: durata del cookie di 1.800 secondi, salvata a
  ogni richiesta, quindi scadenza scorrevole.
- **Durata massima assoluta**: parametro di configurazione non richiesto dal
  PRD, con valore iniziale di 12 ore dall'accesso; marca temporale salvata al
  login e verificata a ogni richiesta (VER-005).
- **Cambio di identificativo** della sessione al login. All'uscita la sessione
  viene cancellata.
- **Cambio password**: la sessione corrente resta valida, le altre decadono.
  **Recupero password**: decadono tutte (VER-006).
- **Disattivazione dell'account** (avvio dell'eliminazione, M5): l'utente
  disattivato non è più autenticato dalla richiesta successiva. Le sessioni
  vengono comunque cancellate esplicitamente (AC-US-021-04).
- **Contenuto della sessione**: solo dati di autenticazione e preferenze di
  interfaccia. Mai dati finanziari.
- **Richieste HTMX con sessione scaduta**: risposta con `HX-Redirect` verso
  l'accesso invece del frammento della pagina di login (VER-005).
- **Pulizia delle sessioni scadute**: il comando standard di Django,
  eseguito dalle attività periodiche quando saranno introdotte (DEF-003).
  Fino ad allora a mano: il volume è trascurabile.

### Password e segreti

- Hash delle password con Argon2id come algoritmo principale; gli altri
  algoritmi di Django restano solo per verificare hash esistenti.
- I segreti TOTP sono gestiti dalla libreria. Le chiavi dell'applicazione
  (`SECRET_KEY`) arrivano dall'ambiente, mai dal repository.

### Nuova verifica dell'identità

Esportazione dei dati, eliminazione dell'account e modifica della verifica in
due passaggi richiedono una verifica recente dell'identità, tramite la
ri-autenticazione di allauth. La finestra ha valore iniziale di 5 minuti, da
confermare con VER-004.

### Limitazione dei tentativi

- I contatori dei limiti usano la cache di Django con backend su database
  PostgreSQL, condivisa da tutti i processi. Nessun Redis.
- L'IP del client va rilevato correttamente dietro il proxy del fornitore di
  hosting, configurando il numero di proxy fidati o l'intestazione fidata.
  Senza questa configurazione i limiti per IP sono inefficaci o aggirabili
  (VER-004, completata con la scelta dell'hosting: DEF-001).

### Pannello di amministrazione

- L'admin di Django **non è esposto** in alcun ambiente ospitato: nessun
  operatore accede ai dati tramite il prodotto (NFR-013).
- Gli accessi tecnici (shell, database) sono regolati dall'ADR di hosting.
- Il back-office del referente sarà un'interfaccia dedicata, con verifica in
  due passaggi obbligatoria (DEF-010, M5).

### Email

- In M0 l'invio è sincrono tramite il backend email di Django; in sviluppo
  il backend è la console.
- Un invio fallito non blocca l'utente, che può richiedere un nuovo
  messaggio (AC-US-001-02).
- Le email non contengono dati finanziari.
- Il provider si sceglie con DEF-002.

## Da verificare

| ID | Verifica | Entro |
|---|---|---|
| VER-004 | Configurazione di allauth contro ogni criterio di US-001: testo e comportamento della protezione dall'enumerazione, chiavi e soglie dei limiti di tentativi, rilevamento dell'IP dietro proxy, finestra di ri-autenticazione e suo comportamento dopo le modifiche di 65.20 | Durante M0, con i test di US-001; la parte sul rilevamento dell'IP dietro proxy segue DEF-001 (prima del livello 1) |
| VER-005 | Durata massima assoluta della sessione; risposta alle richieste HTMX non autenticate | Durante M0 |
| VER-006 | Test: cambio password chiude le altre sessioni; recupero password le chiude tutte; collegamento di recupero scaduto o già usato rifiutato | Durante M0, con i test di accettazione di US-001 |

## Rinviato

- DEF-002: provider email.
- DEF-003: attività periodiche (pulizia delle sessioni).
- DEF-010: back-office del referente e account del personale.
- DEF-014: verifica in due passaggi esposta agli utenti; passkey.
- Elenco delle sessioni attive visibile all'utente: dopo l'MVP, non richiesto dal PRD.

## Alternative considerate

| Alternativa | Motivo dello scarto |
|---|---|
| Identity provider esterno (Keycloak, Auth0, Zitadel) | Componente in più, un ulteriore responsabile del trattamento e un altro luogo da cancellare (DR-024), senza bisogno di SSO |
| Token JWT | Revoca immediata (uscita, cambio password, eliminazione) difficile senza uno stato lato server |
| Autenticazione scritta da zero | Rischio di errori su flussi critici già coperti da una libreria matura |
| Sessioni nei cookie firmati | Revoca e cancellazione immediate non possibili |

## Conseguenze

- Gran parte di US-001 è configurazione e test, non codice nuovo.
- Revoca immediata delle sessioni in ogni caso richiesto dal PRD.
- Le versioni di allauth vanno seguite con attenzione: le correzioni di
  sicurezza recenti riguardano proprio la verifica in due passaggi e i limiti
  di tentativi.

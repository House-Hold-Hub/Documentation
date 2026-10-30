# Architettura software — House-Hold-Hub V1

| Campo | Valore |
|---|---|
| Documento | Architettura software, risposta a [Q-011](../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Versione | 0.2 (ADR indispensabili per M0 approvati) |
| Data | 2026-10-30 |
| Responsabile | mdellapa |
| Fonte dei requisiti | [PRD House-Hold-Hub V1](../../prd/household-hub-v1/README.md), versione 0.2.1 |
| Ambito | V1 (M0–M6), con il dettaglio delle decisioni necessarie prima di M0 |

## Navigazione

| Documento | Contenuto | Stato |
|---|---|---|
| [ADR-001](adr/ADR-001-modular-monolith.md) | Monolite modulare con app Django | Approvato |
| [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) | Stack, versioni e interfaccia renderizzata dal server | Approvato |
| [ADR-003](adr/ADR-003-authentication-and-sessions.md) | Autenticazione e sessioni | Approvato |
| [ADR-004](adr/ADR-004-space-isolation-and-authorization.md) | Isolamento degli spazi e autorizzazione applicativa, senza RLS | Approvato; meccanismo di accesso filtrato scelto durante M0 (VER-016) |
| [ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md) | Convenzioni di persistenza, importi e invarianti | Approvato nei principi; meccanismi di trigger e contatori da verificare |
| [ADR-006](adr/ADR-006-testing-and-continuous-integration.md) | Test e integrazione continua | Approvato |

## Convenzioni

**Stato delle decisioni**

- **Approvata**: decisa dal product owner. Si cambia solo con un nuovo ADR che la sostituisce.
- **Proposta**: principio raccomandato ma non ancora formalizzato in un ADR
  approvato; orienta la progettazione ma non va reso irreversibile prima
  dell'approvazione.
- **Da verificare** (`VER-nnn`): dettaglio che richiede una verifica tecnica
  (documentazione, prova, test di concorrenza) prima di essere adottato.
  Ogni voce indica quando va chiusa.
- **Rinviata** (`DEF-nnn`): scelta posticipata, con il momento o la
  condizione in cui va presa.

**Ciclo di vita di un ADR**: Proposto → Approvato → eventualmente Sostituito
da ADR-nnn. Un ADR approvato non si modifica nel merito: si sostituisce.

**Identificatori stabili**: `ADR-nnn`, `VER-nnn`, `DEF-nnn`, `RA-nnn`. Come
nel PRD, gli identificatori non vengono riutilizzati.

**Rapporto con il PRD**: il PRD resta la fonte dei requisiti e delle regole di
dominio; questo documento non li modifica. Le policy subordinate a
[Q-012](../../prd/household-hub-v1/open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione),
[Q-014](../../prd/household-hub-v1/open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro)
e [Q-015](../../prd/household-hub-v1/open-questions-and-risks.md#q-015--comportamento-alleliminazione-in-attesa-di-q-012)
non sono considerate definitive ([§7](#7-policy-subordinate-a-q-012-q-014-e-q-015)).

## 1. Decisioni approvate

Decisioni del product owner del 2026-10-30: prima stack e stile, poi, dopo la
Decision Review, gli ADR indispensabili per M0. Con la loro approvazione
[Q-011](../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico)
è chiusa.

| Decisione | Riferimento |
|---|---|
| Stack di riferimento della V1: Python, Django, PostgreSQL, HTMX | [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) |
| Monolite modulare: una sola applicazione, un solo database, un solo deploy | [ADR-001](adr/ADR-001-modular-monolith.md) |
| Pagine renderizzate dal server; nessuna SPA | [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) |
| Nessuna API pubblica nella V1 | [ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md) |
| ADR indispensabili prima di M0 | [ADR-001](adr/ADR-001-modular-monolith.md) – [ADR-006](adr/ADR-006-testing-and-continuous-integration.md) |

**Condizioni dell'approvazione**

- ADR-004: l'isolamento degli spazi è garantito come risultato; il meccanismo
  di accesso filtrato si sceglie durante M0 con VER-016. Nessuna garanzia sui
  tempi di risposta del 404.
- ADR-005: approvato nei principi (convenzioni di persistenza, importi,
  principio delle invarianti). I meccanismi di trigger e contatori del §3 non
  sono approvati e restano da verificare (VER-010 – VER-013).
- Le verifiche architetturali di M0 si completano durante M0
  ([§9](#9-dettagli-da-verificare)); le parti che dipendono dall'hosting
  seguono DEF-001.

## 2. Requisiti che guidano l'architettura

| Requisito | Fonte nel PRD | Conseguenza architetturale |
|---|---|---|
| Nessun accesso fuori perimetro, con esito uguale a una risorsa inesistente | NFR-001, DR-003, SM-03, RISK-001 | Autorizzazione in un solo punto, accesso ai dati filtrato per spazio, test negativi generati ([ADR-004](adr/ADR-004-space-isolation-and-authorization.md)) |
| Importi esatti al centesimo; capienza delle attribuzioni anche con operazioni concorrenti | NFR-004, DR-009, FR-028 | Tipo `Money` con validazione rigorosa; invarianti garantite nel database ([ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md)) |
| Operazioni indivisibili (rettifica con riconciliazione, preavvisi, giroconti, annullamento dei lotti) | DR-023 p.6, DR-026 p.5, DR-006, DR-017 | Transazioni ACID locali in un solo database: esclude architetture distribuite ([ADR-001](adr/ADR-001-modular-monolith.md)) |
| Report coerenti e aggiornati subito | NFR-005, DR-012 | Calcolo al momento della lettura da una fonte unica, senza aggregati salvati ([§5.4](#54-report-calcolati-in-lettura)) |
| File importati non conservati, contenuti mai eseguiti | NFR-011 | File effimero, anteprima non salvata ([§5.6](#56-importazione)) |
| Identità dell'ex membro nascosta subito | DR-023 p.2, NFR-005 | Visibilità calcolata in lettura, viste diverse per destinatario ([§5.5](#55-visibilità-per-destinatario)) |
| Cancellazione entro i tempi, backup ≤ 35 giorni, eliminazioni riapplicate dopo un ripristino | DR-024, NFR-012 | Cancellazione per modulo e registro delle eliminazioni fuori dai backup ([§5.7](#57-privacy-e-cancellazione)) |
| Operatori senza accesso ai dati tramite il prodotto | NFR-013, DR-002 | Nessun admin Django esposto; back-office del referente dedicato in M5 ([ADR-003](adr/ADR-003-authentication-and-sessions.md), DEF-010) |
| Requisiti di sicurezza completi già al livello 1 | [Livelli di rilascio](../../prd/household-hub-v1/roadmap.md#livelli-di-rilascio) | Hosting, backup e prova di ripristino decisi prima dell'uso reale (DEF-001) |
| Progetto personale con un solo sviluppatore | Contesto | Pochi componenti, nessun componente infrastrutturale prima che serva ([§8](#8-infrastruttura-minima-e-componenti-rinviati)) |

## 3. Vista d'insieme

```
 Browser (HTML + HTMX, it-IT)
      │ HTTPS · cookie di sessione · token CSRF
 ┌────▼──────────────────────────────────────────────────────┐
 │ Applicazione Django: un processo web, un deploy           │
 │                                                           │
 │  viste e template, per modulo                             │
 │  moduli: identity · spaces · classification · ledger ·    │
 │          imports · planning · reporting · privacy · audit │
 │  core:   Money · orologio · identificativi ·              │
 │          contesto d'accesso                               │
 └────┬───────────────────────────────────────┬──────────────┘
      │                                       │
 PostgreSQL                             Email transazionale
 (un database, uno schema)              (in sviluppo: console)
```

In M0 servono solo il processo web, PostgreSQL e l'invio delle email. Ogni
altro componente è rinviato al momento in cui un requisito lo richiede
([§8](#8-infrastruttura-minima-e-componenti-rinviati)).

## 4. Moduli

Ogni modulo è un'app Django con un'API pubblica di comandi e query; le regole
di dipendenza sono in [ADR-001](adr/ADR-001-modular-monolith.md). Un modulo
viene creato quando la prima milestone che lo usa inizia: M0 non contiene
moduli vuoti.

| Modulo | Responsabilità | Storie | Introdotto in |
|---|---|---|---|
| `core` | Tipo `Money`, orologio iniettabile, identificativi, contesto d'accesso | — | M0 |
| `identity` | Utenti, credenziali, sessioni, verifica email, recupero, verifica in due passaggi, ri-verifica dell'identità | US-001 | M0 |
| `spaces` | Spazi personali e nuclei, appartenenze per periodo, ruoli, inviti, preavvisi; matrice dei permessi; condivisioni in sola lettura | US-002, US-014, US-015, US-017 | M0 (spazio personale); M4 (nuclei) |
| `classification` | Tassonomie, categorie, regole di categorizzazione, eliminazione e unione con riassegnazione | US-004, US-011 | M1 |
| `ledger` | Conti, saldi, movimenti, giroconti, trasferimenti tra spazi; attribuzioni e quote storiche; rettifica contabile | US-003, US-005, US-006, US-016, US-018 | M1 (attribuzioni in M4) |
| `imports` | Sessioni di importazione, lettura dei file, mappatura, profili, duplicati, lotti, annullamento, abbinamento dei giroconti | US-008 – US-012 | M2 |
| `planning` | Budget; abbonamenti e posizioni d'investimento | US-013, US-019, US-023, US-024 | M3 (abbonamenti e posizioni in M6) |
| `reporting` | Sole letture: report mensile, consuntivi, patrimonio | US-007, US-019, US-024 | M1 |
| `audit` | Audit minimo del nucleo, poi registro completo; registro degli accessi del referente | US-022 | M4 |
| `privacy` | Esportazioni, eliminazione dell'account, opposizioni, registro delle eliminazioni | US-020, US-021 | M5 (progettazione in M4) |

## 5. Principi trasversali

Questi principi valgono con qualsiasi stack. Quelli necessari a M0 sono
dettagliati negli ADR; gli altri saranno formalizzati negli ADR del
[§10](#10-piano-degli-adr), prima della milestone che li usa.

### 5.1 Isolamento applicativo

Ogni risorsa appartiene a uno spazio; lo spazio è esplicito nell'URL; ogni
accesso ai dati passa da query filtrate per spazio. L'esito di una
risorsa fuori perimetro è identico a quello di una risorsa inesistente. La RLS
di PostgreSQL non è adottata in M0: garanzie, limiti e criterio di riesame
sono in [ADR-004](adr/ADR-004-space-isolation-and-authorization.md).
Stato: approvata; meccanismo di accesso filtrato scelto con VER-016.

### 5.2 Importi e date

Importi in `Decimal`, con tipo `Money` e validazione rigorosa: nessun
arrotondamento implicito, nessun `float`, un solo punto di arrotondamento
documentato ([DR-020](../../prd/household-hub-v1/domain-rules.md#dr-020--abbonamenti)).
Date contabili senza orario, fuso Europe/Rome per "oggi" e per i confini del
mese. Dettagli in [ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md).
Stato: approvata.

### 5.3 Invarianti nel database

Le invarianti finanziarie e di governance sono garantite dal database dove
possibile. Quelle che riguardano più righe sono verificate su una riga
"padre" che serializza le scritture concorrenti. Il principio è approvato in
[ADR-005](adr/ADR-005-persistence-and-monetary-amounts.md); i meccanismi
concreti (trigger, vincoli differiti) restano da verificare con test di
concorrenza prima della milestone che li usa (VER-010 – VER-013).

### 5.4 Report calcolati in lettura

Report, consuntivi di budget e "spese non pianificate" sono calcolati al
momento della lettura da un'unica vista delle righe di report: movimenti
ordinari, quote attribuite e quote storiche non limitate. Così
[DR-012](../../prd/household-hub-v1/domain-rules.md#dr-012--invariante-dei-totali)
punti 6 e 7 valgono per costruzione, NFR-005 non richiede invalidazioni e il
ricalcolo del ripiego di DR-024 non richiede elaborazioni. Con i volumi di
A-005 il limite di NFR-006 non richiede cache. Stato: proposta, da
formalizzare prima di M1.

### 5.5 Visibilità per destinatario

Ogni vista che mostra dati a un destinatario diverso dal titolare (membri del
nucleo, ex membro, referente) riceve oggetti dedicati con i soli campi
ammessi, mai istanze di modello. L'identità dell'autore di un'attribuzione è
calcolata in lettura dal periodo di appartenenza; uscita, rientro ed
eliminazione la nascondono subito senza riscrivere dati. Stato: la regola sugli
oggetti dedicati è approvata in
[ADR-004](adr/ADR-004-space-isolation-and-authorization.md); il resto va
formalizzato prima di M4.

### 5.6 Importazione

Il file caricato è effimero ed escluso dai backup. L'anteprima è calcolata,
non salvata. Alla conferma, sotto lock del conto, il controllo dei duplicati si
ripete e, se l'esito è cambiato, si torna all'anteprima. L'idempotenza è su due
livelli: la stessa richiesta (stato della sessione) e gli stessi dati
([DR-016](../../prd/household-hub-v1/domain-rules.md#dr-016--possibili-duplicati)).
L'abbinamento dei duplicati è deterministico. Stato: proposta, da formalizzare
prima di M2.

### 5.7 Privacy e cancellazione

Ogni modulo con dati personali implementa la propria esportazione e
cancellazione; `privacy` le coordina. Le eliminazioni sono annotate in un
registro conservato fuori dalla linea di backup del database, per
riapplicarle dopo un ripristino (NFR-012). Stato: proposta, da formalizzare
prima di M4 (progettazione) e M5 (realizzazione).

### 5.8 Audit

Le voci di audit si scrivono nella stessa transazione dell'azione. I registri
sono di sola aggiunta: il ruolo applicativo del database non ha permessi di
modifica; le cancellazioni previste da DR-024 passano da una procedura
dedicata. Stato: proposta, da formalizzare prima di M4.

## 6. Interfaccia

Pagine renderizzate dal server; HTMX aggiorna parti della pagina. Regole in
[ADR-002](adr/ADR-002-stack-and-server-rendered-ui.md):

- htmx servito come file statico versionato, senza CDN e senza richieste a terzi;
- nessuna valutazione di codice nelle richieste HTMX (`allowEval` disattivato) e
  nessuna cache delle pagine nel browser;
- stessa autorizzazione per pagine intere e frammenti;
- nessun polling, che terrebbe aperte le sessioni oltre il timeout di
  inattività (NFR-003);
- HTML semantico, gestione del focus e annunci `aria-live` dopo le
  sostituzioni (NFR-008).

## 7. Policy subordinate a Q-012, Q-014 e Q-015

L'architettura non anticipa queste decisioni: le isola in punti di
configurazione o strategie sostituibili, così che l'esito cambi un
componente e non la struttura.

| Questione | Cosa resta aperto | Come l'architettura lo isola | Quando serve |
|---|---|---|---|
| Q-012 | Base giuridica e trattamenti del [gate di utilizzo](../../prd/household-hub-v1/open-questions-and-risks.md#gate-di-utilizzo) | Funzioni dei nuclei disattivabili per ambiente fino al superamento del gate; strategia di eliminazione configurabile (quote storiche o cancellazione con ricalcolo); inclusione delle quote limitate nei report come singolo predicato della vista di report; testi degli avvisi configurabili | Progettazione in M4; uso reale al livello 2 |
| Q-014 | Chi autorizza la riconciliazione nei nuclei lasciati; ritiro senza errore | Politica di riconciliazione sostituibile, con default "nega"; il modello conserva periodo di appartenenza e collegamento tecnico, quindi le alternative A e B sarebbero aggiunte | M4 (US-015, US-018) |
| Q-015 | Ordine di realizzazione tra quote storiche e ripiego | Le due strategie condividono la stessa interfaccia; il ripiego serve comunque per le opposizioni accolte | Prima di TASK-066 (M5) |

Nessuna di queste policy è realizzata in M0. Le fondazioni di M0 non
contengono assunzioni sul loro esito.

## 8. Infrastruttura minima e componenti rinviati

**Presenti in M0**: processo web Django, PostgreSQL, invio email (console in
sviluppo), integrazione continua su GitHub Actions
([ADR-006](adr/ADR-006-testing-and-continuous-integration.md)). La cache
condivisa per i limiti di tentativi usa PostgreSQL
([ADR-003](adr/ADR-003-authentication-and-sessions.md)).

| ID | Scelta rinviata | Quando o a quale condizione | Default fino ad allora |
|---|---|---|---|
| DEF-001 | Fornitore di hosting e database gestito. Criteri: dati in UE, PostgreSQL gestito con ripristino a un istante e conservazione dei backup configurabile ≤ 35 giorni, cifratura a riposo, rete privata, accordo sul trattamento dei dati. Comprende la parte di VER-004 sul rilevamento dell'IP dietro proxy e la conferma di VER-015 presso il fornitore | Prima del livello 1 | Sviluppo locale e CI |
| DEF-002 | Provider email transazionale in UE | Prima del livello 1 | Backend email su console |
| DEF-003 | Esecuzione di attività periodiche (pulizie, scadenze) | M2, con la pulizia dei file di importazione | Nessuna; comandi di gestione eseguibili a mano |
| DEF-004 | Coda di lavori asincroni | Solo se un requisito richiede lavoro fuori dalla richiesta che non sia periodico | Non prevista nella V1 |
| DEF-005 | Archiviazione temporanea dei file di importazione | M2 (ADR di importazione) | — |
| DEF-006 | Object storage per esportazioni e registro delle eliminazioni | M5 | — |
| DEF-007 | Ambiente di staging separato | Prima del livello 1 | Nessun ambiente ospitato con dati reali |
| DEF-008 | Error tracking esterno | Dopo la valutazione rispetto a NFR-010 | Log strutturati senza importi né descrizioni |
| DEF-009 | Row-Level Security di PostgreSQL | Revisione di sicurezza di fine M4, prima del livello 2 ([ADR-004](adr/ADR-004-space-isolation-and-authorization.md)) | Isolamento applicativo |
| DEF-010 | Back-office del referente e account del personale | M5 | Nessun accesso del personale tramite il prodotto |
| DEF-011 | API per client esterni (es. app nativa) | Dopo la V1, su necessità, con un ADR dedicato | Nessuna API pubblica (approvato) |
| DEF-012 | Pipeline di rilascio continuo | Con DEF-001 | Solo integrazione continua |
| DEF-013 | Migrazione a htmx 4 | Quando htmx 4 diventa la versione "latest" (prevista a inizio 2027) | htmx 2.x |
| DEF-014 | Verifica in due passaggi per gli utenti (AC-US-001-08, rinviabile nel PRD) e passkey | Prima di chiudere M0, oppure dopo l'MVP | TOTP disponibile nella libreria, non esposto |
| DEF-015 | Strumenti di build per CSS e JavaScript | Solo se il CSS scritto a mano non basta | Nessuna toolchain Node |
| DEF-016 | Test di prestazioni periodici sui volumi di NFR-006 | M1–M2 | Nessuno |
| DEF-017 | Scansione dinamica di sicurezza su un ambiente ospitato | Prima del livello 1, con DEF-007 | Nessuna |

**Esclusi dalla V1 salvo necessità dimostrata**: Redis, broker di messaggi,
CDN, Kubernetes, microservizi, servizi di feature flag, cache dei report.

## 9. Dettagli da verificare

Nessuna verifica condiziona le decisioni approvate: la Decision Review del
2026-10-30 ha accertato che il loro esito può cambiare il meccanismo con cui
una decisione si realizza, non la decisione. Le verifiche sono di due classi:

- **Da completare durante M0**: il loro completamento fa parte del criterio
  di completamento di [M0](../../prd/household-hub-v1/milestones/M0-foundation.md).
  Le parti che dipendono dall'hosting seguono DEF-001, prima del livello 1.
- **Rinviabili**: si chiudono entro il momento indicato. Se una verifica
  fallisce, la decisione interessata si rivede con un nuovo ADR prima della
  milestone che la usa.

### Da completare durante M0

| ID | Verifica | ADR | Momento e dipendenze |
|---|---|---|---|
| VER-001 | Versioni effettive e compatibilità reciproca delle dipendenze, con l'ultima patch disponibile | ADR-002 | Avvio di M0 |
| VER-022 | Strumento di gestione delle dipendenze con lockfile e hash | ADR-006 | Avvio di M0 |
| VER-004 | Configurazione di django-allauth rispetto ai criteri di US-001, incluso il rilevamento dell'IP del client dietro proxy per i limiti di tentativi | ADR-003 | Durante M0, con i test di US-001; la parte sul proxy segue DEF-001 |
| VER-005 | Durata massima assoluta della sessione e comportamento alla scadenza nelle richieste HTMX | ADR-003 | Durante M0 |
| VER-006 | Chiusura delle altre sessioni al cambio e al recupero della password (AC-US-001-06) | ADR-003 | Durante M0, con i test di accettazione di US-001 |
| VER-014 | Meccanismo di immutabilità dello spazio di una risorsa | ADR-004 | Durante M0 |
| VER-015 | Ruoli distinti per applicazione e migrazioni | ADR-004 | Durante M0 in locale e in CI; conferma presso il fornitore con DEF-001 |
| VER-016 | Scelta del meccanismo di accesso filtrato per spazio e comportamento delle relazioni tra modelli | ADR-004 | Durante M0 (TASK-005) |
| VER-017 | Generazione della matrice di test negativi dall'elenco degli URL | ADR-006 | Durante M0 (TASK-007) |
| VER-018 | Formato degli identificativi (UUIDv7 di Python 3.14 o UUIDv4) | ADR-005 | Durante M0, prima del primo modello |
| VER-019 | Configurazione CSP compatibile con htmx e assenza di cache delle pagine nel browser | ADR-002 | Durante M0, con il template di base |
| VER-021 | Contratti di dipendenza tra moduli verificabili in CI | ADR-001 | Durante M0 |

### Rinviabili

| ID | Verifica | ADR | Entro |
|---|---|---|---|
| VER-012 | Coerenza dei due lati dei giroconti | ADR-005 | Prima di M1 (US-006) |
| VER-013 | Strumento con cui dichiarare e migrare i trigger | ADR-005 | Con la prima tra VER-010 – VER-012 |
| VER-007 | Comportamento di Django e psycopg con importi a più di due decimali: errore o arrotondamento silenzioso | ADR-005 | Prima dei primi importi (M1) |
| VER-008 | Parser degli importi in formato italiano, anche da tastiera di smartphone | ADR-005 | M1 |
| VER-020 | Accessibilità delle sostituzioni HTMX (focus, annunci) | ADR-002 | Primi flussi di M1 |
| VER-009 | Conversione dei numeri delle celle Excel in importi esatti | ADR-005 | M2, con i file di esempio di Q-008 |
| VER-010 | Capienza delle attribuzioni garantita nel database sotto concorrenza | ADR-005 | Prima di M4 (US-018) |
| VER-011 | Invariante "almeno un amministratore" garantita nel database sotto concorrenza | ADR-005 | Prima di M4 (US-015) |
| VER-002 | Piano di aggiornamento a Django 6.2 (uscita prevista il 2027-04-06) | ADR-002 | Entro il 2027-04; obbligatorio prima della fine del supporto esteso di 6.1 (2027-12) |
| VER-003 | Supporto di Python 3.15 nelle dipendenze; base attuale Python 3.14 | ADR-002 | Riesame a ogni aggiornamento di Django |

## 10. Piano degli ADR

**Prima di M0**: ADR-001 – ADR-006, approvati il 2026-10-30. La loro
approvazione ha chiuso
[Q-011](../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico);
gli ADR successivi non la riaprono.

**Successivi**, redatti appena prima della milestone che li richiede
(numerazione assegnata alla redazione):

| Tema | Entro |
|---|---|
| Report calcolati in lettura e vista delle righe di report | Prima di M1 |
| Invarianti concorrenti: esito di VER-010 – VER-013 | Prima di M1 per i giroconti; aggiornamento prima di M4 |
| Hosting, ambienti, backup e ripristino, cifratura, accessi tecnici (NFR-002, NFR-012, NFR-013) | Prima del livello 1 |
| Importazione: file, anteprima, duplicati, lotti, attività periodiche | Prima di M2 |
| Visibilità per destinatario, appartenenze, attribuzioni e quote | Prima di M4 |
| Audit e registri immutabili | Prima di M4 |
| Row-Level Security: decisione definitiva (DEF-009) | Revisione di sicurezza di fine M4 |
| Esportazione, cancellazione, opposizioni, registro delle eliminazioni | Progettazione in M4, prima di M5 |
| Back-office del referente (DEF-010) | M5 |

## 11. Rischi architetturali

| ID | Rischio | Mitigazione |
|---|---|---|
| RA-001 | L'isolamento è solo applicativo: una query non filtrata o una relazione attraversata in un template espone dati di altri spazi (RISK-001) | Accesso filtrato per spazio (meccanismo scelto con VER-016), oggetti dedicati per destinatario, matrice di test negativi, riesame della RLS (ADR-004, DEF-009) |
| RA-002 | I meccanismi previsti per le invarianti concorrenti non reggono sotto concorrenza | Verifiche VER-010 – VER-013 con test di concorrenza prima della milestone; alternative documentate in ADR-005 |
| RA-003 | La logica nel database (trigger) è poco visibile e difficile da manutenere | Ammessa solo per invarianti, dichiarata nel codice, testata esplicitamente |
| RA-004 | Il supporto di Django 6.1 termina a dicembre 2027 | Aggiornamento pianificato a 6.2 (VER-002) |
| RA-005 | I confini tra moduli dipendono da strumenti e disciplina, non dal linguaggio | Contratti di dipendenza in CI (VER-021) |
| RA-006 | La migrazione da htmx 2 a htmx 4 richiede modifiche agli attributi | Rinvio fino al rilascio "latest" (DEF-013), uso prudente dell'ereditarietà degli attributi |
| RA-007 | In un progetto personale sviluppatore e operatore coincidono (NFR-013) | Controllo procedurale e registrato degli accessi tecnici, da definire nell'ADR di hosting |
| RA-008 | Arrotondamenti silenziosi tra applicazione e database | Validazione rigorosa in `Money`, verifica VER-007 |

## Revisioni

| Versione | Data | Modifiche |
|---|---|---|
| 0.1 | 2026-10-30 | Prima bozza: stack e stile approvati dal product owner; ADR-001 – ADR-006 proposti; verifiche e rinvii elencati |
| 0.1.1 | 2026-10-30 | Verifiche divise tra bloccanti prima di M0 e rinviabili (§9, tabelle degli ADR); criterio di chiusura di Q-011 (§10); Q-011 aggiornata nel PRD come parzialmente risolta. Stato degli ADR invariato: Proposto |
| 0.2 | 2026-10-30 | Decision Review: ADR-001 – ADR-006 approvati (ADR-005 nei principi, non nei meccanismi di trigger e contatori); ADR-004 garantisce l'isolamento come risultato, con meccanismo scelto in VER-016, e non promette tempi indistinguibili per il 404; rimosso da ADR-002 il riferimento al framework Tasks; verifiche bloccanti riclassificate come da completare durante M0 (con VER-006, già prevista in M0), con le parti dipendenti dall'hosting assegnate a DEF-001; Q-011 chiusa. Nessun identificativo modificato |

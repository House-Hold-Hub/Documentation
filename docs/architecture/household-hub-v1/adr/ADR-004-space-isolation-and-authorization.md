# ADR-004 — Isolamento degli spazi e autorizzazione applicativa, senza RLS

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato** (2026-10-30) |
| Data | 2026-10-30 |
| Decisore | mdellapa (product owner) |
| Questione | [Q-011](../../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Requisiti | NFR-001, NFR-013, SM-03; [DR-001](../../../prd/household-hub-v1/domain-rules.md#dr-001--appartenenza-delle-risorse) – [DR-004](../../../prd/household-hub-v1/domain-rules.md#dr-004--condivisione-in-sola-lettura), [DR-009](../../../prd/household-hub-v1/domain-rules.md#dr-009--attribuzioni), [matrice dei permessi](../../../prd/household-hub-v1/domain-rules.md#matrice-dei-permessi-del-nucleo); [US-002](../../../prd/household-hub-v1/stories/US-002-space-isolation.md); RISK-001 |
| Correlati | [ADR-001](ADR-001-modular-monolith.md), [ADR-003](ADR-003-authentication-and-sessions.md), [ADR-006](ADR-006-testing-and-continuous-integration.md) |

## Contesto

L'esposizione di dati tra spazi è il rischio principale del prodotto
(RISK-001, obiettivo SM-03 = 0). NFR-001 richiede che un accesso non
autorizzato abbia lo stesso esito di una risorsa inesistente. Esistono due
vie d'accesso legittime tra spazi diversi:

- i conti personali condivisi in sola lettura con un nucleo (DR-004);
- i diritti dell'autore sulle proprie attribuzioni, che appartengono al
  nucleo, anche dopo l'uscita (DR-009, DR-023).

La Row-Level Security (RLS) di PostgreSQL è stata valutata come difesa in
profondità. Con Django avrebbe costi rilevanti già in M0:

- il contesto va impostato in ogni transazione (`SET LOCAL`), con rischio di
  esiti vuoti o di contesti sbagliati tra connessioni riusate;
- i test verificano davvero le policy solo se eseguiti con un ruolo non
  proprietario;
- le tre vie d'accesso complicano le policy;
- le JOIN dell'ORM filtrate restituiscono risultati vuoti senza errori, e il
  debug costa caro.

## Decisione

### Modello

1. **Appartenenza.** Ogni risorsa di uno spazio ha `space_id` obbligatorio,
   assegnato alla creazione dallo spazio dell'URL e immutabile (AC-US-002-02;
   meccanismo in VER-014).
2. **Spazio esplicito.** Le pagine di uno spazio hanno lo spazio nell'URL
   (es. `/s/<space_id>/movimenti/`). Il server non conserva uno "spazio
   attivo": il selettore dell'interfaccia cambia URL.
3. **Contesto d'accesso.** A ogni richiesta autenticata si costruisce un
   oggetto immutabile con utente, spazio personale e nuclei attivi con il
   ruolo. Non si conserva tra richieste, quindi revoche, uscite e rimozioni
   valgono dalla richiesta successiva.
4. **Permessi dichiarati.**
   - Ogni vista dichiara il permesso richiesto, preso da un'unica matrice
     nel codice che riproduce la
     [matrice del PRD](../../../prd/household-hub-v1/domain-rules.md#matrice-dei-permessi-del-nucleo).
   - Una vista senza dichiarazione fa fallire i test
     ([ADR-006](ADR-006-testing-and-continuous-integration.md)).
5. **Accesso ai dati filtrato per spazio.**
   - Risultato garantito: nessuna query su dati di uno spazio è eseguita senza
     il filtro per gli spazi del contesto d'accesso, salvo i punti ammessi
     sotto. Il risultato è verificato da test e da un controllo in CI.
   - Il meccanismo si sceglie durante M0 con VER-016 tra due candidati: un
     manager predefinito che impone il filtro, oppure selettori con contesto
     d'accesso obbligatorio e divieto di usare direttamente i modelli fuori
     dal modulo che li possiede. La scelta non cambia questa decisione.
   - L'accesso non filtrato richiede un metodo esplicito, ammesso solo in
     moduli e funzioni elencati (attività periodiche, `privacy`) e
     controllato in CI.
   - Si carica sempre con il filtro; non si carica prima per poi controllare.
6. **Vie d'accesso tra spazi.** Solo due, ciascuna con selettori dedicati e
   test propri:
   - conti condivisi in sola lettura;
   - attribuzioni dell'autore.
   Nessun accesso generico tra spazi.
7. **Oggetti dedicati per destinatario.**
   - Le viste che mostrano dati a destinatari diversi dal titolare (membri
     del nucleo, ex membro) ricevono oggetti costruiti dai selettori con i
     soli campi ammessi (es. FR-029), mai istanze di modello.
   - Così un template non può attraversare una relazione, ad esempio
     dall'attribuzione al movimento di origine.

### Esiti delle richieste

| Situazione | Esito |
|---|---|
| Utente non autenticato | Reindirizzamento all'accesso; per le richieste HTMX `HX-Redirect` ([ADR-003](ADR-003-authentication-and-sessions.md)) |
| Risorsa o spazio inesistente, oppure fuori dal perimetro dell'utente (incluso ex membro, membro di altro nucleo, utente esterno) | **404**, con pagina e intestazioni identiche a quelle di una risorsa inesistente |
| Spazio accessibile ma ruolo insufficiente (es. un Membro che crea un conto del nucleo) | **403** |
| Filtri manipolati con identificativi di altri spazi (AC-US-002-04) | Nessun dato oltre il perimetro: il filtro si applica dentro l'accesso già filtrato |

### Database

- **Ruoli separati.** L'applicazione si collega con un ruolo **non
  proprietario**, senza permessi sulla struttura del database. Le migrazioni
  usano un ruolo proprietario distinto (VER-015).
- **Base per i registri immutabili** di M4 e M5, i cui permessi in sola
  aggiunta richiedono questa separazione.

### RLS: non adottata in M0

Preparativi già in M0, così da poterla aggiungere senza rifacimenti:

- `space_id` su ogni tabella di spazio;
- contesto d'accesso costruito in un unico punto;
- ruolo applicativo non proprietario.

Il riesame (DEF-009) avviene alla revisione di sicurezza di fine M4, prima
del livello 2, quando arrivano nuclei, condivisioni e attribuzioni. Ognuna di
queste condizioni orienta verso l'adozione:

- eccezioni all'accesso filtrato oltre quelle elencate;
- SQL scritto a mano diffuso al di fuori di `reporting`;
- difetti di isolamento trovati da test o revisioni;
- apertura del servizio a utenti esterni.

## Garanzie e limiti dell'isolamento applicativo

### Cosa è garantito, e come

| Garanzia | Meccanismo | Verifica |
|---|---|---|
| Ogni vista applica un permesso | Dichiarazione obbligatoria e matrice unica | Test che enumera gli URL e fallisce sulle viste senza permesso |
| Le query dell'ORM non escono dagli spazi del contesto | Accesso filtrato per spazio, con il meccanismo scelto in VER-016; accesso non filtrato esplicito e circoscritto | Matrice di test negativi; controllo in CI sull'accesso diretto ai modelli e sull'uso dell'accesso non filtrato |
| Le risorse fuori perimetro sono indistinguibili da quelle inesistenti | Caricamento sempre filtrato, poi 404 | Test negativi con riferimenti diretti a identificativi altrui |
| I destinatari non titolari vedono solo i campi ammessi | Oggetti dedicati costruiti dai selettori | Test di riservatezza sui campi esposti (TASK-055) |
| Le revoche hanno effetto immediato | Contesto ricostruito a ogni richiesta | Test su uscita, rimozione e revoca della condivisione |
| Lo spazio di una risorsa non cambia | Immutabilità di `space_id` (VER-014) | Test di modifica |

### Limiti, e come sono mitigati

| Limite | Effetto possibile | Mitigazione | Rischio residuo |
|---|---|---|---|
| SQL scritto a mano (viste di report, query ottimizzate) non passa dall'accesso filtrato | Righe di altri spazi in un report | SQL ammesso solo in `reporting` e nelle migrazioni; ogni query richiede il parametro dello spazio; test negativi sui report | Basso, se il perimetro resta circoscritto |
| Le relazioni tra modelli usano il manager di base, non filtrato | Un template o un servizio attraversa una relazione verso dati di un altro spazio | Oggetti dedicati per i destinatari non titolari; nessuna istanza di modello passata a quei template (VER-016) | Medio fino alla verifica VER-016 |
| Uso improprio dell'accesso non filtrato | Esposizione in una funzione nuova | Elenco chiuso dei punti ammessi, controllo in CI, revisione | Basso |
| Errore nella matrice dei permessi | Permesso sbagliato concesso a un ruolo | Matrice unica allineata al PRD; un test per ogni riga (AC-US-015-02) | Basso |
| Il database non impone l'isolamento | Un difetto applicativo non è fermato da un secondo livello | Riesame della RLS (DEF-009) | Accettato fino a fine M4; da rivalutare prima del livello 2 |
| Accessi tecnici (shell, database) di chi gestisce il servizio | Lettura di qualsiasi dato fuori dal prodotto | Admin non esposto; accessi tecnici regolati e registrati nell'ADR di hosting (NFR-013) | Procedurale (RA-007) |
| Differenze di tempi di risposta tra 404 "inesistente" e "non autorizzato" | Deduzione dell'esistenza di una risorsa | Stesso percorso di codice: caricamento filtrato, poi 404 | Trascurabile con identificativi non enumerabili |

## Da verificare

| ID | Verifica | Entro |
|---|---|---|
| VER-014 | Immutabilità di `space_id`: vincolo nel database (trigger) o protezione applicativa con test | Durante M0 |
| VER-015 | Ruoli distinti per applicazione e migrazioni in locale e in CI; disponibilità presso il fornitore (DEF-001) | Durante M0 in locale e in CI; conferma presso il fornitore con DEF-001 |
| VER-016 | Scelta del meccanismo di accesso filtrato tra i due candidati del punto 5, verificandone la compatibilità con relazioni, form, migrazioni e test; elenco delle relazioni attraversabili dai template | Durante M0 (TASK-005) |

## Rinviato

- DEF-009: decisione definitiva sulla RLS, alla revisione di sicurezza di fine M4.
- Back-office del referente e suoi permessi (DEF-010, M5).

## Alternative considerate

| Alternativa | Motivo dello scarto per M0 |
|---|---|
| RLS fin da M0 | Costi elevati in configurazione, test e debug prima che esistano gli accessi tra spazi; il rischio che copre è mitigato dai meccanismi applicativi |
| Database o schema separato per spazio | Romperebbe attribuzioni e condivisioni, che collegano spazi diversi per natura |
| Controlli di permesso sparsi nelle viste, senza matrice né accesso filtrato | Copertura non verificabile; un controllo dimenticato espone dati |

## Conseguenze

- L'isolamento dipende da un numero ridotto di meccanismi centrali, tutti
  verificati da test automatici.
- L'accettazione del rischio residuo senza RLS vale fino alla revisione di
  fine M4 e va rinnovata o superata prima del livello 2.

# ADR-001 — Monolite modulare con app Django

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato** (2026-10-30) |
| Data | 2026-10-30 |
| Revisione | 2026-11-01 — regola 2 allineata ad ADR-004, VER-016 e VER-021: elenco chiuso delle superfici tecniche pubbliche (M0.1, D-9; vedi [Revisione del 2026-11-01](#revisione-del-2026-11-01--superfici-tecniche-pubbliche)) |
| Decisore | mdellapa (product owner) |
| Questione | [Q-011](../../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Requisiti | NFR-001, NFR-005, RISK-001, RISK-002 |
| Correlati | [ADR-002](ADR-002-stack-and-server-rendered-ui.md), [ADR-004](ADR-004-space-isolation-and-authorization.md), [ADR-005](ADR-005-persistence-and-monetary-amounts.md) |

## Contesto

Il PRD richiede operazioni indivisibili che toccano più aree del dominio:

- la rettifica contabile con riconciliazione delle attribuzioni (DR-023 punto 6);
- l'applicazione ordinata dei preavvisi con rivalidazione (DR-026 punto 5);
- l'annullamento dei lotti, che scioglie giroconti e rimuove attribuzioni (DR-017);
- l'unione di categorie, che riassegna movimenti, attribuzioni, quote, budget e regole (FR-018).

Il progetto ha un solo sviluppatore e volumi piccoli (A-005). Serve una
struttura che mantenga queste operazioni in transazioni locali e che renda
leggibili i confini del dominio, senza costi operativi distribuiti.

## Decisione

### Stile

Una sola applicazione Django, un solo database PostgreSQL, un solo deploy,
organizzata in moduli con confini espliciti.

### Struttura e regole di dipendenza

**Moduli.** Ogni modulo è un'app Django: `core`, `identity`, `spaces`,
`classification`, `ledger`, `imports`, `planning`, `reporting`, `audit`,
`privacy` (responsabilità nel [documento di architettura](../README.md#4-moduli)).
Un modulo nasce quando la milestone che lo usa inizia.

**Struttura interna di un modulo**

| Elemento | Ruolo | Visibilità |
|---|---|---|
| `models.py` | Modelli e vincoli del modulo | Privato |
| `services.py` | Comandi: unico modo di cambiare lo stato del modulo; definiscono i confini di transazione | Pubblico |
| `selectors.py` | Letture usate da altri moduli; restituiscono oggetti dedicati, non istanze di modello | Pubblico |
| Superfici tecniche (`core.access`, `core.clock`, `core.ids`, `spaces.permissions`, `spaces.scoping`) | Tipi e contratti trasversali richiesti da ADR-004 e ADR-005; solo quelli elencati nella regola 2 | Pubblico |
| `views.py`, `forms.py`, `templates/<modulo>/` | Interfaccia: validano l'input, chiamano servizi e selettori, renderizzano | Privato |

Le viste restano sottili: nessuna regola di dominio in viste, form o template.

**Regole di dipendenza**

1. `core` non dipende da altri moduli.
2. Un modulo usa un altro modulo solo tramite i suoi `services` e `selectors`,
   i tipi pubblici che essi espongono e le **superfici tecniche pubbliche**
   di questo elenco chiuso; non importa i `models` né altri sottomoduli di
   altri moduli.

   | Superficie | Contenuto | Fonte |
   |---|---|---|
   | `core.access`, `core.clock`, `core.ids` | Contesto d'accesso, orologio, identificativi | [Architettura, §4](../README.md#4-moduli); ADR-004 punto 3; ADR-005 |
   | `spaces.permissions` | Matrice dei permessi e dichiarazione del permesso delle viste | ADR-004 punto 4 |
   | `spaces.scoping` | Modello, chiavi esterne e form delle risorse di uno spazio; accesso filtrato | ADR-004 punti 1 e 5; VER-016 |

   Una nuova superficie tecnica richiede, nella stessa modifica,
   l'aggiornamento di questo elenco e dei contratti di dipendenza verificati in
   CI (VER-021).
3. **Chiavi esterne tra moduli** ammesse solo verso modelli di riferimento
   stabili, dichiarate con l'etichetta (es. `"spaces.Space"`) senza
   importare il modulo: spazio (`spaces`), conto (`ledger`),
   categoria (`classification`) e utente (`identity`). Ogni nuova eccezione
   richiede un aggiornamento di questo ADR.
4. **Dipendenze inverse** (es. `classification` che deve riassegnare i
   movimenti di `ledger` quando una categoria è eliminata): tramite punti di
   estensione espliciti. Un registro di funzioni dichiarate dai moduli
   interessati, chiamate nella stessa transazione. Niente *signals* di Django.
5. **Signals di Django** ammessi solo per l'integrazione con il framework e le
   librerie (es. eventi di autenticazione), mai per effetti di dominio.
6. **Letture aggregate di `reporting`** su tabelle di altri moduli: solo
   tramite viste SQL di cui `reporting` è proprietario, definite nelle sue
   migrazioni.
7. Nessun ciclo tra moduli.

**Transazioni.** Un comando che coinvolge più moduli si esegue in una sola
transazione aperta dal servizio che lo avvia; i servizi chiamati vi
partecipano. Gli effetti esterni (email) partono dopo il commit
(`transaction.on_commit`).

**Codice e documentazione.**

- Il codice applicativo vive in un repository dedicato dell'organizzazione
  `House-Hold-Hub` (nome da definire all'avvio di M0).
- PRD, architettura e ADR restano in questo repository `Documentation`.

## Revisione del 2026-11-01 — superfici tecniche pubbliche

Decisione del product owner del 2026-11-01 (D-9 di
[M0.1](../M0.1-structural-refactoring.md#d-9--allineamento-di-adr-001-e-allentamento-registrato)).

- **Motivo.** Il testo originale della regola 2 ammetteva solo `services`,
  `selectors` e i tipi che essi espongono. ADR-004, approvato lo stesso giorno,
  richiede invece a ogni modulo con risorse di dichiarare i permessi da
  un'unica matrice (punto 4) e di usare l'accesso filtrato per spazio
  (punti 1 e 5). Il meccanismo scelto con VER-016 e i contratti di VER-021,
  approvati con la chiusura di M0, realizzano queste regole con
  `spaces.permissions`, `spaces.scoping` e i tipi di `core`. La revisione
  allinea il testo di questo ADR alle decisioni già approvate.
- **Merito invariato.** Restano i confini espliciti, il divieto di importare i
  `models` e gli altri sottomoduli di un altro modulo, le chiavi esterne solo
  verso i riferimenti stabili e l'assenza di cicli. Per questo la revisione è
  in loco e non richiede un nuovo ADR, come la revisione di
  [ADR-006](ADR-006-testing-and-continuous-integration.md) (decisione B1).
- **Allentamento registrato.** Il controllo manuale `ConfiniTraModuliTests` di
  `household-hub` vietava al codice applicativo di `identity` di importare
  `spaces.permissions` e `spaces.scoping`. Con la sua rimozione (TASK-090 di
  M0.1) vale per `identity` la stessa superficie di ogni altro modulo. Le altre
  asserzioni di quel controllo sono coperte da contratti più stretti.
- **Elenco chiuso.** Superfici aggiuntive (es. il tipo `Money` di `core` in M1)
  si aggiungono all'elenco della regola 2 insieme ai contratti di CI.

## Da verificare

| ID | Verifica | Entro |
|---|---|---|
| VER-021 | Le regole 2, 3 e 7 sono esprimibili come contratti verificati in CI (es. import-linter) anche con i riferimenti tra modelli per etichetta | Durante M0 |

## Rinviato

- Estrazione di un modulo in un servizio separato: non prevista. Si
  riconsidera solo con un requisito che lo giustifichi.
- Contratti di esportazione e cancellazione per modulo: ADR di privacy prima di M4.

## Alternative considerate

| Alternativa | Motivo dello scarto |
|---|---|
| Microservizi | Le invarianti di DR-009, DR-023 e DR-026 diventerebbero transazioni distribuite, con compensazioni; costo operativo sproporzionato |
| Monolite senza moduli | Più rapido all'inizio, ma la logica di nuclei, privacy e contabilità si intreccia; confini non verificabili |
| Backend-as-a-Service (es. Supabase) | Regole di dominio sparse tra policy SQL e funzioni; accesso diretto dei client al database |
| App Django con logica nei modelli e nei *signals* | Effetti tra moduli impliciti, difficili da testare e da rendere atomici |

## Conseguenze

- Le operazioni composte restano transazioni ACID locali.
- Un solo processo da distribuire e osservare.
- I confini sono garantiti da strumenti e revisione, non dal linguaggio (RA-005).
- I punti di estensione aggiungono un piccolo meccanismo da mantenere, ma
  rendono visibili gli effetti tra moduli.

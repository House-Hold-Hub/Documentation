# ADR-001 — Monolite modulare con app Django

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato** (2026-10-30) |
| Data | 2026-10-30 |
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
| `views.py`, `forms.py`, `templates/<modulo>/` | Interfaccia: validano l'input, chiamano servizi e selettori, renderizzano | Privato |

Le viste restano sottili: nessuna regola di dominio in viste, form o template.

**Regole di dipendenza**

1. `core` non dipende da altri moduli.
2. Un modulo usa un altro modulo solo tramite `services`, `selectors` e i tipi
   pubblici che essi espongono; non importa i `models` di altri moduli.
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

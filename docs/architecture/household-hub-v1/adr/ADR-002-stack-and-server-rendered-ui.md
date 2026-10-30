# ADR-002 — Stack, versioni e interfaccia renderizzata dal server

[← Architettura](../README.md)

| Campo | Valore |
|---|---|
| Stato | **Approvato** (2026-10-30) |
| Data | 2026-10-30 |
| Decisore | mdellapa (product owner) |
| Questione | [Q-011](../../../prd/household-hub-v1/open-questions-and-risks.md#q-011--architettura-e-stack-tecnologico) |
| Requisiti | NFR-003, NFR-007, NFR-008, NFR-009, NFR-010 |
| Correlati | [ADR-001](ADR-001-modular-monolith.md), [ADR-003](ADR-003-authentication-and-sessions.md) |

## Contesto

Il product owner ha come stack principale Python, Django e PostgreSQL. Il PRD
richiede soprattutto form, tabelle, filtri e drill-down:

- anteprima di importazione con esito per riga;
- report per categoria;
- budget;
- attribuzioni con residuo.

È richiesto l'uso da smartphone (≥ 360 px), WCAG 2.1 AA e localizzazione
italiana. Sono state confrontate tre opzioni: Django con HTMX, Django con
React/TypeScript, ASP.NET Core .NET 10 con React/TypeScript.

## Decisione

### Stack e interfaccia

- Backend Python con Django; database PostgreSQL.
- Pagine HTML renderizzate dal server, con HTMX per gli aggiornamenti parziali.
- Nessuna SPA.
- Nessuna API pubblica nella V1: le viste restituiscono HTML. Un'eventuale API
  futura (es. per un'app nativa) richiede un ADR dedicato e si appoggia agli
  stessi servizi dei moduli (DEF-011).

### Versioni

Verificate il 2026-10-30 sulle fonti elencate in fondo. Le versioni effettive
si confermano all'avvio di M0 (VER-001).

| Componente | Versione | Supporto | Note |
|---|---|---|---|
| Python | 3.14.x | Correzioni di bug; fine supporto ottobre 2030 | 3.15 è uscito il 2026-10-09, ma non tutte le dipendenze lo dichiarano supportato (VER-003) |
| Django | 6.1.x, ultima patch | Supporto principale fino ad aprile 2027, esteso fino a dicembre 2027 | Aggiornamento pianificato a 6.2 (VER-002) |
| Django 6.2 (obiettivo) | — | Uscita prevista il 2027-04-06; supporto esteso fino ad aprile 2030 | Ultima versione con etichetta LTS: dal 2028 Django passa a un rilascio annuale con tre anni di supporto per versione |
| PostgreSQL | 18.x | Supporto fino al 2030-11-14 | Django 6.1 richiede PostgreSQL ≥ 15; 17.x accettabile se il fornitore non offre 18 (supporto fino al 2029-11-08) |
| Driver PostgreSQL | psycopg 3 | Django 6.1 richiede psycopg ≥ 3.1.12 | psycopg2 escluso: Django ne prevede la futura deprecazione |
| django-allauth | ≥ 65.21 | Supporto ufficiale di Django 6.1 da 65.19.0 | 65.20.1 corregge il riuso dei codici TOTP e i limiti di tentativi WebAuthn: versioni precedenti escluse |
| htmx | 2.x | Supportato a tempo indeterminato; 2.x resta la versione "latest" | htmx 4.0.0 è uscito il 2026-08-28 ma resta "next" fino a inizio 2027 (DEF-013) |
| django-htmx | ≥ 1.28 | Django 5.2 – 6.1; Python fino a 3.14 | Il supporto di Django 6.1 è indicato nella 1.28.0; da confermare sul changelog ufficiale (VER-001) |

**Perché 6.1 e non 5.2 LTS.**

- 5.2 ha supporto esteso fino ad aprile 2028, ma da 5.2 l'aggiornamento
  successivo sarebbe comunque a 6.2, con un salto maggiore.
- Partendo da 6.1, il passaggio a 6.2 è un aggiornamento minore.
- Si usa subito la CSP integrata, introdotta in 6.0.

### Componenti di esecuzione

| Componente | Proposta | Motivo |
|---|---|---|
| Server applicativo | gunicorn (WSGI) | Nessun requisito di WebSocket o streaming; ASGI non necessario |
| File statici | WhiteNoise | Nessun CDN né server web separato |
| CSS e JavaScript | CSS scritto a mano; htmx come file statico versionato nel repository | Nessuna toolchain Node (DEF-015); nessuna richiesta a CDN di terzi (NFR-010) |
| JavaScript aggiuntivo | Piccoli script senza framework, solo dove necessari | Alpine.js o simili non adottati salvo necessità |

### Regole dell'interfaccia

1. **Pagine complete e frammenti.** Ogni URL restituisce una pagina completa;
   con l'intestazione `HX-Request` può restituire un frammento. Le risposte
   dichiarano `Vary: HX-Request`.
2. **Miglioramento progressivo.** I flussi principali (navigazione, form di
   inserimento, filtri) funzionano anche come link e form tradizionali.
   Interazioni intrinsecamente dinamiche (anteprima di mappatura che si
   aggiorna) possono richiedere JavaScript.
3. **Stessa autorizzazione** per pagine e frammenti: un frammento è una vista
   come le altre ([ADR-004](ADR-004-space-isolation-and-authorization.md)).
4. **Configurazione sicura di htmx**:
   - valutazione di codice disattivata (`allowEval: false`), quindi niente `hx-on`;
   - richieste solo verso la stessa origine;
   - nessuna copia delle pagine nella cronologia del browser, che finirebbe
     in `localStorage` con dati finanziari.
5. **CSP restrittiva** con il supporto integrato di Django (dalla 6.0):
   script solo dalla stessa origine, nessuno script inline senza nonce.
6. **Nessun polling**: terrebbe attiva la sessione oltre il timeout di
   inattività (NFR-003).
7. **Accessibilità**: HTML semantico; dopo ogni sostituzione il focus è
   gestito e le modifiche rilevanti sono annunciate con `aria-live`;
   verifica con audit (NFR-008).
8. **Localizzazione**: lingua `it`, fuso `Europe/Rome`, formattazione di date
   e numeri con la localizzazione di Django. L'interpretazione degli importi
   inseriti segue il parser rigoroso di
   [ADR-005](ADR-005-persistence-and-monetary-amounts.md), non la
   localizzazione implicita dei form.

## Da verificare

| ID | Verifica | Entro |
|---|---|---|
| VER-001 | Versioni effettive e compatibilità reciproca delle dipendenze, con l'ultima patch | Avvio di M0 |
| VER-002 | Piano e prova di aggiornamento a Django 6.2 | Entro aprile 2027; obbligatorio prima di dicembre 2027 |
| VER-003 | Supporto di Python 3.15 in Django, allauth, django-htmx e nelle altre dipendenze | Riesame a ogni aggiornamento di Django |
| VER-019 | Opzioni di htmx 2 che disattivano valutazione di codice e cache della cronologia; CSP che funziona con htmx | Durante M0, con il template di base |
| VER-020 | Gestione del focus e annunci dopo le sostituzioni, su lettori di schermo | Primi flussi di M1 |

## Rinviato

- DEF-011: API per client esterni.
- DEF-013: migrazione a htmx 4.
- DEF-015: strumenti di build per CSS e JavaScript.

## Alternative considerate

| Alternativa | Motivo dello scarto |
|---|---|
| ASP.NET Core .NET 10 + React/TypeScript | Tecnicamente solida, ma richiede di imparare due ecosistemi senza vantaggi decisivi su sicurezza o correttezza, che dipendono da PostgreSQL e dalle regole architetturali |
| Django + React/TypeScript | Raddoppia lo stack (API, client, build, validazione e formattazione duplicate in TypeScript) per esigenze di interfaccia che HTMX copre |
| Django 5.2 LTS | Orizzonte di supporto più breve rispetto al percorso 6.1 → 6.2; aggiornamento successivo più ampio |
| htmx 4 subito | Non ancora "latest"; ecosistema in transizione |

## Conseguenze

- Un solo linguaggio e una sola toolchain; i test delle viste coprono anche i
  frammenti HTMX senza browser
  ([ADR-006](ADR-006-testing-and-continuous-integration.md)).
- Superficie esposta ridotta: nessuna API, quasi nessuna dipendenza JavaScript.
- Un'app nativa o un'integrazione futura richiederanno un'API dedicata, resa
  economica dalla separazione tra servizi e viste
  ([ADR-001](ADR-001-modular-monolith.md)).
- Aggiornamento di Django obbligatorio entro dicembre 2027 (RA-004).

## Fonti (consultate il 2026-10-30)

- [Django — Download e calendario di supporto](https://www.djangoproject.com/download/)
- [Django 6.1 release notes](https://docs.djangoproject.com/en/6.1/releases/6.1/)
- [Django 6.1 — Databases (PostgreSQL e psycopg)](https://docs.djangoproject.com/en/6.1/ref/databases/)
- [Django 6.1 — FAQ installazione (versioni di Python)](https://docs.djangoproject.com/en/6.1/faq/install/)
- [Django 6.2 Roadmap](https://www.djangoproject.com/download/6.2/roadmap/)
- [Django is moving to an annual release cycle](https://www.djangoproject.com/weblog/2026/aug/10/annual-release-cycle/)
- [Django 6.0 release notes (CSP)](https://docs.djangoproject.com/en/6.0/releases/6.0/)
- [Status of Python versions](https://devguide.python.org/versions/)
- [PostgreSQL Versioning Policy](https://www.postgresql.org/support/versioning/)
- [django-allauth release notes](https://docs.allauth.org/en/dev/release-notes/index.html), [65.20.1](https://allauth.org/news/2026/10/django-allauth-65.20.1-released/), [65.21.0](https://allauth.org/news/2026/10/django-allauth-65.21.0-released/)
- [htmx 4.0.0 has been released](https://four.htmx.org/announcements/2026-08-28-htmx-4.0.0-is-released)
- [django-htmx — installazione](https://django-htmx.readthedocs.io/en/latest/installation.html), [changelog](https://django-htmx.readthedocs.io/en/latest/changelog.html)

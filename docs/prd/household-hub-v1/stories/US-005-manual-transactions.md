# US-005 — Movimenti manuali

| Campo | Valore |
|---|---|
| Milestone | [M1 — Analisi mensile personale](../milestones/M1-personal-monthly-analysis.md) |
| Requisiti | [FR-012](../requirements.md#fr-012--inserimento-manuale-dei-movimenti), [FR-013](../requirements.md#fr-013--modifica-ed-eliminazione-dei-movimenti), [FR-015](../requirements.md#fr-015--ricerca-e-filtri-dei-movimenti), NFR-004 |
| Regole | [DR-005](../domain-rules.md#dr-005--movimenti), [DR-008](../domain-rules.md#dr-008--categorie), [DR-013](../domain-rules.md#dr-013--mese-di-competenza) |
| Dipende da | [US-003](US-003-personal-accounts.md), [US-004](US-004-categories.md) |
| Questioni collegate | [Q-014](../open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro) (movimenti vincolati, default adottato) |
| DoR | READY |

## Storia

Come utente, voglio registrare a mano entrate e uscite e ritrovarle
facilmente, così da tenere traccia anche delle spese che non arrivano
dagli estratti conto (es. contanti).

## Esito atteso

L'utente registra, corregge, elimina e cerca i propri movimenti; saldi e
report riflettono subito ogni modifica.

## Criteri di accettazione

- **AC-US-005-01** — Registro un'uscita di 45,50 € con data, conto,
  descrizione e sottocategoria Cene: compare nell'elenco dei movimenti e il
  saldo del conto diminuisce di 45,50 €.
- **AC-US-005-02** — Sono rifiutati, con indicazione del campo e senza
  perdere i dati inseriti: importo nullo, negativo o con più di due
  decimali; data non valida; descrizione vuota; conto archiviato;
  un'uscita con categoria di entrata.
- **AC-US-005-03** — Un movimento senza categoria risulta "Da categorizzare".
- **AC-US-005-04** — Modificare importo, data, conto o categoria aggiorna
  saldi e report di tutti i mesi interessati (es. spostando la data da
  marzo ad aprile l'importo passa dal report di marzo a quello di aprile).
- **AC-US-005-05** — L'eliminazione richiede conferma e aggiorna saldi e
  report.
- **AC-US-005-06** — Posso filtrare l'elenco per periodo, conto, tipo,
  natura, categoria, sottocategoria, testo della descrizione e stato "Da
  categorizzare", combinando i filtri; vedo il totale dei movimenti
  filtrati.
- **AC-US-005-07** — Un movimento con data futura o anteriore alla data del
  saldo iniziale è accettato e conteggiato nel mese della propria data.

## Verifica

Test di accettazione automatizzati; test negativi di accesso estesi ai
movimenti (US-002). I vincoli sui movimenti attribuiti (DR-010) sono
verificati in [US-018](US-018-transaction-attribution.md) e quelli sui
movimenti vincolati (DR-023) in [US-015](US-015-household-roles-and-members.md);
la natura dei movimenti è verificata in [US-006](US-006-transfers.md).

## Task

- **TASK-014** — Inserimento dei movimenti con validazione (AC-01 – AC-03, AC-07).
- **TASK-015** — Modifica ed eliminazione con aggiornamento di saldi e
  report (AC-04, AC-05).
- **TASK-016** — Elenco dei movimenti con ricerca e filtri combinabili (AC-06).

## Definition of Ready

READY.

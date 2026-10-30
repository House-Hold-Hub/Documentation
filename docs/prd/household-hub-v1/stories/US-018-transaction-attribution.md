# US-018 — Attribuzione dei movimenti al nucleo

| Campo | Valore |
|---|---|
| Milestone | [M4 — Nuclei familiari](../milestones/M4-households.md) |
| Requisiti | [FR-027](../requirements.md#fr-027--attribuzione-dei-movimenti-a-un-nucleo), [FR-028](../requirements.md#fr-028--limite-delle-attribuzioni), [FR-029](../requirements.md#fr-029--riservatezza-delle-attribuzioni), [FR-044](../requirements.md#fr-044--informativa-sullo-storico-del-nucleo), NFR-001, NFR-004 |
| Regole | [DR-009](../domain-rules.md#dr-009--attribuzioni), [DR-010](../domain-rules.md#dr-010--modifica-di-movimenti-attribuiti), [DR-007](../domain-rules.md#dr-007--movimenti-tra-spazi-diversi), [DR-012](../domain-rules.md#dr-012--invariante-dei-totali), [DR-014](../domain-rules.md#dr-014--rimborsi), [DR-023](../domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo), [DR-024](../domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo) |
| Dipende da | [US-016](US-016-household-accounts-and-categories.md); per le attribuzioni verso nuclei lasciati (AC-06, AC-10, AC-12) [US-015](US-015-household-roles-and-members.md) |
| Questioni collegate | [Q-003](../open-questions-and-risks.md#q-003--campi-visibili-delle-attribuzioni), [Q-004](../open-questions-and-risks.md#q-004--attribuzioni-di-un-membro-uscito) (non bloccanti); [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione) (contenuto dell'informativa e gate di utilizzo); [Q-014](../open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro) (default adottato) |
| DoR | READY |

## Storia

Come membro di un nucleo che paga alcune spese familiari dal proprio conto
personale, voglio attribuire al nucleo quelle spese, anche solo in parte,
così che entrino nell'analisi familiare senza esporre il mio conto.

## Esito atteso

Le quote attribuite entrano nel nucleo con categorie del nucleo; il
movimento originale e il conto restano privati e invariati.

## Criteri di accettazione

- **AC-US-018-01** — Data un'uscita di 100,00 € "Spesa supermercato" sul
  mio conto personale non condiviso, attribuisco 60,00 € al nucleo A con
  la categoria del nucleo "Alimentari": la quota compare tra le
  attribuzioni ricevute da A; il movimento originale resta di 100,00 € con
  la mia categoria personale.
- **AC-US-018-02** — Attribuisco 60,00 € al nucleo A e 40,00 € al nucleo
  B; un ulteriore centesimo su qualsiasi nucleo è rifiutato e il sistema
  mostra il residuo attribuibile (0,00 €).
- **AC-US-018-03** — Sono rifiutati: importo nullo, negativo, con più di
  due decimali o superiore al residuo; una seconda attribuzione dello
  stesso movimento allo stesso nucleo (si modifica quella esistente,
  oppure resta quella di una precedente appartenenza, DR-023); un
  nucleo di cui non sono membro attivo; una categoria che non appartiene
  al nucleo o incompatibile con il tipo del movimento.
- **AC-US-018-04** — I membri di A vedono della quota solo data, 60,00 €,
  "Alimentari", il mio nome e la descrizione che ho scritto (o il nome
  della categoria se non l'ho scritta); non vedono il conto, l'importo
  totale né la descrizione originale. I membri di B non vedono la quota
  attribuita ad A.
- **AC-US-018-05** — Posso modificare importo, categoria e descrizione di
  una mia attribuzione o rimuoverla; nessun altro membro, amministratori
  compresi, può farlo.
- **AC-US-018-06** — Ridurre l'importo del movimento sotto la somma di
  tutte le sue attribuzioni, comprese quelle verso nuclei lasciati, è
  rifiutato con un messaggio che indica le attribuzioni da ridurre; cambiare
  la data sposta la data delle quote verso nuclei di cui sono membro attivo;
  eliminare il movimento, cambiarne il tipo o trasformarlo in giroconto o in
  trasferimento tra spazi richiede una conferma che elenca i nuclei
  coinvolti e rimuove quelle attribuzioni. Per un movimento vincolato queste
  ultime operazioni sono rifiutate, salvo rettifica contabile (DR-023).
- **AC-US-018-07** — Non è possibile attribuire un giroconto, un
  trasferimento tra spazi né un movimento di un conto del nucleo.
- **AC-US-018-08** — Posso attribuire un'entrata personale ricevuta da
  terzi (es. il rimborso del negozio per una spesa familiare) con una
  categoria di spesa del nucleo, secondo DR-014. Il denaro ricevuto dal
  conto del nucleo è un trasferimento tra spazi e non è attribuibile
  (DR-007).
- **AC-US-018-09** — L'attribuzione non richiede che il conto sia
  condiviso; se il conto è anche condiviso con A, la quota e il movimento
  condiviso restano distinti nella vista del nucleo.
- **AC-US-018-10** — Su ogni mio movimento vedo a quali nuclei e per quale
  importo è attribuito, e posso consultare l'elenco delle mie attribuzioni
  per nucleo, comprese quelle verso nuclei che ho lasciato (DR-023), che
  restano nel calcolo del residuo attribuibile.
- **AC-US-018-11** — Alla prima attribuzione verso ciascun nucleo vedo
  l'informativa di FR-044: le quote entrano nello storico del nucleo; se
  esco dal nucleo vi restano senza il mio nome e il movimento resta
  vincolato; se elimino l'account vi restano in forma minimizzata senza il
  mio nome; sono indicati base giuridica e diritto di opposizione. Non mi
  viene chiesto un consenso; l'informativa resta consultabile in seguito.
- **AC-US-018-12** — Sul dataset di verifica, dopo qualsiasi sequenza di
  attribuzioni, uscite e rientri nei nuclei, modifiche ed eliminazioni di
  movimenti e annullamenti di lotti, per ogni movimento la somma delle
  attribuzioni, comprese quelle verso nuclei lasciati, non supera l'importo
  (DR-012 punto 8).

## Verifica

Test di accettazione automatizzati con un utente membro di due nuclei;
test di riservatezza sui campi esposti; estensione della suite di test
negativi. La correttezza dei totali del nucleo è verificata in
[US-019](US-019-household-reports-and-budgets.md); le parti di AC-06, AC-10 e
AC-12 relative ai nuclei lasciati sono verificabili dopo
[US-015](US-015-household-roles-and-members.md).

## Task

- **TASK-054** — Creazione, modifica e rimozione delle attribuzioni con i
  vincoli di DR-009 (AC-01 – AC-03, AC-05, AC-07, AC-08).
- **TASK-055** — Vista riservata delle attribuzioni nel nucleo (AC-04, AC-09).
- **TASK-056** — Vincoli sulla modifica dei movimenti attribuiti e
  capienza, comprese le attribuzioni verso nuclei lasciati (AC-06, AC-12).
- **TASK-057** — Riepilogo delle attribuzioni per il titolare (AC-10).
- **TASK-076** — Informativa sullo storico del nucleo alla prima
  attribuzione (AC-11).

## Definition of Ready

READY. I campi visibili seguono il default di Q-003; il testo
dell'informativa (AC-11) va validato con Q-012 e non è usato con utenti
reali prima del gate di utilizzo.

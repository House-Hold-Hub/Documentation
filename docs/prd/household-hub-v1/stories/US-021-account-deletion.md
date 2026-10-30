# US-021 — Eliminazione dell'account

| Campo | Valore |
|---|---|
| Milestone | [M5 — Privacy e controllo dei dati](../milestones/M5-privacy-and-data-control.md) |
| Requisiti | [FR-042](../requirements.md#fr-042--eliminazione-dellaccount), [FR-044](../requirements.md#fr-044--informativa-sullo-storico-del-nucleo), [FR-045](../requirements.md#fr-045--gestione-delle-opposizioni), NFR-010, NFR-012, NFR-013 |
| Regole | [DR-024](../domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo), [DR-025](../domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo), [DR-022](../domain-rules.md#dr-022--almeno-un-amministratore), [DR-011](../domain-rules.md#dr-011--perimetro-dei-report), [DR-012](../domain-rules.md#dr-012--invariante-dei-totali) |
| Dipende da | [US-015](US-015-household-roles-and-members.md), [US-016](US-016-household-accounts-and-categories.md), [US-018](US-018-transaction-attribution.md), [US-020](US-020-data-export.md), [US-022](US-022-activity-log.md) |
| Questioni collegate | [Q-001](../open-questions-and-risks.md#q-001--dati-conferiti-ai-nuclei-dopo-leliminazione-dellaccount) (decisione provvisoria), [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione) (prerequisito per l'implementazione definitiva), [Q-013](../open-questions-and-risks.md#q-013--gestione-dellopposizione) (decisa), [Q-015](../open-questions-and-risks.md#q-015--comportamento-alleliminazione-in-attesa-di-q-012) (default adottato) |
| DoR | READY per la progettazione funzionale; implementazione definitiva e uso con dati reali subordinati al gate di Q-012 |

## Storia

Come utente, voglio eliminare il mio account e i miei dati, così da
esercitare il mio diritto alla cancellazione; come membro di un nucleo,
voglio che lo storico familiare resti coerente quando un altro membro
elimina il proprio account.

## Esito atteso

Account e spazio personale eliminati. Nei nuclei restano solo quote storiche
minimizzate e i dati contabili necessari dei conti del nucleo, senza
riferimenti diretti all'utente; report e budget del nucleo non cambiano,
salvo il ripiego di cancellazione e ricalcolo.

## Criteri di accettazione

Esempio: il dataset di riferimento di
[US-019](US-019-household-reports-and-budgets.md), in cui Marco ha
attribuito 60,00 € di Alimentari al nucleo A a maggio.

- **AC-US-021-01** — L'eliminazione richiede una nuova verifica
  dell'identità e una conferma esplicita; prima della conferma il sistema
  propone l'esportazione dei dati ([US-020](US-020-data-export.md)).
- **AC-US-021-02** — Prima della conferma vedo, per ogni nucleo, quante
  quote resteranno come quote storiche senza il mio nome e quanti movimenti
  dei conti del nucleo resteranno senza autore, con l'indicazione della
  base giuridica (FR-044) e la possibilità di oppormi.
- **AC-US-021-03** — Se sono l'ultimo amministratore di un nucleo con altri
  membri, l'eliminazione è bloccata finché non nomino un altro
  amministratore; i nuclei in cui sono l'unico membro sono elencati ed
  eliminati con l'account.
- **AC-US-021-04** — Dopo la conferma non è più possibile accedere con le
  credenziali dell'account, tutte le sessioni sono chiuse e, nello stesso
  momento, nessun membro vede più in alcun nucleo il mio nome né le
  descrizioni che avevo scritto; lo spazio personale e tutte le sue risorse
  sono eliminati entro i tempi di AC-16.
- **AC-US-021-05** — Le condivisioni in sola lettura dei miei conti sono
  revocate e gli inviti in attesa inviati da me o a me destinati sono
  annullati.
- **AC-US-021-06** — Senza opposizione, ciascuna mia attribuzione diventa
  una quota storica in tutti i nuclei, compresi quelli che avevo già lasciato. Con
  l'esempio, dopo l'eliminazione dell'account di Marco il report di maggio
  del nucleo A resta: uscite 270,00 €, Alimentari 180,00 €; il dettaglio di
  Alimentari mostra una "Quota storica del nucleo" di 60,00 € riferita a
  maggio, senza autore, giorno, descrizione né conto di origine. Nessun
  avviso di ricalcolo viene mostrato.
- **AC-US-021-07** — Le quote storiche non sono accorpate in modo
  distruttivo: se Marco avesse attribuito anche 25,00 € di Alimentari il
  20 maggio, resterebbero registrate due quote storiche di 60,00 € e
  25,00 €, ciascuna rettificabile e oggetto possibile di opposizione. Nella
  vista e nell'esportazione del nucleo compare un'unica riga "Quote storiche
  del nucleo" per Alimentari a maggio con il totale di tutte le quote
  storiche, senza distinguerne la provenienza: se anche un altro utente
  eliminato avesse una quota storica di Alimentari a maggio, la riga ne
  mostrerebbe il totale insieme a quelle di Marco. I consuntivi di budget
  del nucleo non cambiano.
- **AC-US-021-08** — Nessun membro, amministratori compresi, può modificare
  o eliminare una quota storica; se la sua categoria viene eliminata o
  unita, la quota passa alla destinazione; eliminando il nucleo, le sue
  quote storiche sono eliminate.
- **AC-US-021-09** — I movimenti che ho registrato o importato nei conti del
  nucleo restano con data, importo, tipo, conto, categoria, descrizione,
  giroconti e lotti invariati, quindi saldi e report del nucleo non
  cambiano; non indicano più l'autore, né i movimenti né i lotti.
- **AC-US-021-10** — Una ricerca nei dati dei nuclei del mio nome, del mio
  indirizzo email, dei nomi dei miei conti personali e delle descrizioni
  originali dei miei movimenti personali non restituisce risultati, con
  l'unica eccezione dei testi dei movimenti dei conti del nucleo
  (descrizioni bancarie e note), documentata in DR-024.
- **AC-US-021-11** — Le voci del registro attività di cui sono autore o
  oggetto sono eliminate dai registri visibili ai membri: l'audit minimo
  e, se realizzato, il registro completo.
- **AC-US-021-12** — Se mi oppongo, indicando i motivi, per tutte o per
  alcune quote, account e spazio personale diventano subito inaccessibili
  e sono eliminati nei tempi di AC-16, mentre le quote interessate sono
  limitate fino all'esito: conservate singolarmente
  e collegate a me senza che i membri lo vedano, non trasformate in quote
  storiche, non modificabili ed escluse da report e budget del nucleo. I membri vedono
  un avviso senza nome sui mesi con importi sospesi; con l'esempio, durante
  la limitazione il report di maggio del nucleo A mostra uscite 210,00 €.
- **AC-US-021-13** — L'opposizione è decisa da un referente autorizzato del
  titolare del trattamento, con decisione motivata e registrata (data di
  ricezione, nuclei e quote, motivi, eventuale proroga, decisione,
  motivazione, referente, data di comunicazione). L'esito mi è comunicato
  all'indirizzo email dell'account entro un mese dal ricevimento; se serve
  una proroga, fino a due mesi ulteriori, ne ricevo i motivi entro il primo
  mese. La comunicazione indica la possibilità di reclamo all'autorità di
  controllo e di ricorso giurisdizionale; dopo la comunicazione l'indirizzo
  email è eliminato e il nome dell'account è eliminato al termine
  dell'eventuale ripiego.
- **AC-US-021-14** — Se l'opposizione è accolta si applica il ripiego: le
  quote sono eliminate, il report di maggio del nucleo A resta con uscite
  210,00 € e Alimentari 120,00 €, le invarianti di DR-012 restano valide, i
  membri vedono un avviso con i mesi ricalcolati che non nomina la persona e
  nelle descrizioni e note dei movimenti dei conti del nucleo le occorrenze
  del mio nome, cognome e indirizzo email, come registrati nell'account,
  sono sostituite da "ex membro", senza cambiare importi, date, tipi,
  conti e categorie. Se è respinta, sono informato prima che la limitazione
  sia revocata; poi le quote diventano quote storiche come in AC-06 e il
  report di maggio torna a uscite 270,00 €.
- **AC-US-021-15** — Amministratori e membri dei nuclei non vedono le
  opposizioni né il registro delle opposizioni, non ne conoscono l'autore e
  non possono decidere o modificarne l'esito.
- **AC-US-021-16** — Eliminazioni e trasformazioni terminano entro un mese
  dalla conferma (obiettivo: 30 giorni); le quote oggetto di opposizione
  seguono i termini di AC-13. Ripristinando un backup precedente, le
  eliminazioni sono riapplicate prima che i dati tornino disponibili.
- **AC-US-021-17** — Se durante la limitazione la categoria del nucleo di
  una quota limitata viene eliminata con destinazione, la quota segue la
  destinazione e l'operazione è annotata nel registro delle opposizioni; se
  l'opposizione è poi respinta, la quota rientra nei report nella categoria
  di destinazione. Se il nucleo viene eliminato, le quote sono eliminate con
  il nucleo e l'esito mi è comunicato.
- **AC-US-021-18** — Una nuova opposizione sulle stesse quote, anche dopo
  una decisione, è registrata, valutata nei termini di AC-13 e applica di
  nuovo la limitazione (DR-025 punto 8).
- **AC-US-021-19** — Un operatore del servizio senza ruolo di referente non
  accede ad alcun dato degli spazi né al registro delle opposizioni; il
  referente vede solo il registro e le quote oggetto di opposizione, con
  verifica in due passaggi, e ogni suo accesso è registrato (NFR-013).

## Verifica

Test di accettazione automatizzati sul dataset di US-019 con un membro
attivo e un ex membro che eliminano l'account, con e senza opposizione,
anche parziale o ripetuta;
test di ricerca dei riferimenti residui (AC-10) su tutti i dati conservati;
confronto di report, budget e saldi del nucleo prima e dopo l'eliminazione;
prova di ripristino da backup con riapplicazione delle eliminazioni
(NFR-012).

## Task

- **TASK-064** — Flusso di eliminazione con verifica, riepilogo degli effetti,
  informativa, conferma e proposta di esportazione (AC-01 – AC-03).
- **TASK-065** — Eliminazione dello spazio personale, chiusura delle
  sessioni, revoca delle condivisioni e annullamento degli inviti (AC-04, AC-05).
- **TASK-066** — Trasformazione di ciascuna attribuzione in una quota
  storica immutabile, con riferimento di provenienza e vista aggregata per
  autore, inclusa nel perimetro dei report del nucleo (AC-06 – AC-08).
- **TASK-073** — Rimozione dei riferimenti all'utente da movimenti, lotti e
  registri dei nuclei e occultamento immediato dell'identità (AC-04,
  AC-09 – AC-11).
- **TASK-074** — Completamento entro i tempi e riapplicazione delle
  eliminazioni ai backup ripristinati (AC-16).
- **TASK-075** — Opposizione nel flusso di eliminazione, limitazione delle
  quote ed esito con ripiego o revoca della limitazione (AC-12, AC-14,
  AC-17, AC-18).
- **TASK-077** — Valutazione delle opposizioni da parte del referente
  autorizzato, con registro delle decisioni, termini dell'art. 12 e
  comunicazione dell'esito e accessi limitati del referente (AC-13, AC-15,
  AC-19).

## Definition of Ready

READY per la progettazione funzionale: Q-001 ha una decisione di prodotto
provvisoria (quote storiche minimizzate, base giuridica proposta,
opposizione e ripiego) e Q-013 è decisa (referente autorizzato del titolare
del trattamento).

L'implementazione definitiva e l'uso con dati reali sono subordinati al
gate di utilizzo di Q-012, che resta aperta. Se la valutazione esclude la
base giuridica proposta, il ripiego diventa il comportamento per tutte le
eliminazioni e cambiano AC-06 – AC-08; le risposte su informativa,
limitazione (art. 18), termini (art. 12), opposizioni ripetute e tempi
possono cambiare AC-02 e AC-12 – AC-19. L'ordine di implementazione tra
quote storiche e ripiego è oggetto di Q-015.

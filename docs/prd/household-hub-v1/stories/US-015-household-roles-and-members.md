# US-015 — Ruoli e gestione dei membri

| Campo | Valore |
|---|---|
| Milestone | [M4 — Nuclei familiari](../milestones/M4-households.md) |
| Requisiti | [FR-006](../requirements.md#fr-006--ruoli-nel-nucleo), [FR-007](../requirements.md#fr-007--gestione-dei-membri), [FR-028](../requirements.md#fr-028--limite-delle-attribuzioni), [FR-045](../requirements.md#fr-045--gestione-delle-opposizioni), [FR-046](../requirements.md#fr-046--esportazione-dei-dati-del-nucleo), NFR-001 |
| Regole | [DR-009](../domain-rules.md#dr-009--attribuzioni), [DR-010](../domain-rules.md#dr-010--modifica-di-movimenti-attribuiti), [DR-022](../domain-rules.md#dr-022--almeno-un-amministratore), [DR-023](../domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo), [DR-025](../domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo), [DR-026](../domain-rules.md#dr-026--tutela-dei-dati-condivisi-del-nucleo), [Matrice dei permessi](../domain-rules.md#matrice-dei-permessi-del-nucleo) |
| Dipende da | [US-014](US-014-household-creation-and-invitations.md); per parti di singoli criteri [US-017](US-017-read-only-sharing.md), [US-018](US-018-transaction-attribution.md), [US-020](US-020-data-export.md), [US-021](US-021-account-deletion.md), [US-022](US-022-activity-log.md) (vedi Verifica) |
| Questioni collegate | [Q-004](../open-questions-and-risks.md#q-004--attribuzioni-di-un-membro-uscito) (decisa), [Q-013](../open-questions-and-risks.md#q-013--gestione-dellopposizione) (decisa), [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione) (base giuridica per quote e collegamento degli ex membri; gate di utilizzo), [Q-014](../open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro) (default adottato) |
| DoR | READY per la progettazione; uso con dati reali subordinato al gate di Q-012 |

## Storia

Come amministratore, voglio gestire ruoli e membri del nucleo, e come
membro voglio poterlo lasciare senza che il nucleo continui a vedere la mia
identità nelle mie attribuzioni, così che l'accesso ai dati comuni
rispecchi sempre la composizione reale della famiglia e lo storico resti
coerente e senza doppi conteggi.

## Esito atteso

I permessi seguono la matrice, l'accesso cessa subito per chi esce, le sue
quote restano al nucleo senza la sua identità e senza superare l'importo dei
movimenti di origine, il nucleo non resta mai senza amministratore e nessun
amministratore elimina dati comuni senza preavviso.

## Criteri di accettazione

- **AC-US-015-01** — Un amministratore può promuovere un Membro ad
  Amministratore e riportare un Amministratore a Membro, nel rispetto del
  preavviso di AC-13.
- **AC-US-015-02** — Per ogni riga della matrice dei permessi, le azioni
  non consentite al ruolo sono rifiutate (es. un Membro non può creare
  conti del nucleo, gestire categorie o budget, invitare o rimuovere
  membri).
- **AC-US-015-03** — Un membro rimosso perde subito l'accesso (un
  amministratore alla scadenza del preavviso di AC-13): le sue richieste
  successive sul nucleo hanno lo stesso esito di risorse inesistenti e le
  sue condivisioni verso il nucleo sono revocate. Nelle sue attribuzioni
  storiche e nelle voci del registro che le riguardano i membri vedono "ex
  membro" al posto del nome e non vedono più la descrizione che aveva
  scritto; importi, date e categorie restano, i report del nucleo non
  cambiano e le attribuzioni restano collegate ai movimenti di origine in
  modo non visibile al nucleo.
- **AC-US-015-04** — Un membro che lascia il nucleo ottiene gli stessi
  effetti. Prima di confermare vede quante attribuzioni resteranno al
  nucleo senza il suo nome e quanti movimenti resteranno vincolati, può
  ancora modificarle o rimuoverle ed è informato che l'uscita non elimina
  l'account e che potrà opporsi alla conservazione delle quote.
- **AC-US-015-05** — L'ultimo amministratore di un nucleo con altri membri
  non può lasciarlo né rinunciare al ruolo finché non nomina un altro
  amministratore.
- **AC-US-015-06** — Se l'unico membro lascia il nucleo, il sistema chiede
  conferma esplicita che nucleo e dati saranno eliminati; dopo la conferma
  nessuno vi accede più.
- **AC-US-015-07** — Un amministratore può rinominare il nucleo.
  L'eliminazione di un nucleo con altri membri richiede conferma esplicita
  e ha effetto dopo un preavviso di 7 giorni comunicato a tutti i membri,
  durante il quale il nucleo resta consultabile, ogni membro attivo può
  esportarne i dati e qualsiasi amministratore può annullarla. Al termine i
  dati del nucleo sono eliminati; i dati personali dei membri e i movimenti
  originali delle attribuzioni restano invariati e non sono più vincolati da
  quel nucleo.
- **AC-US-015-08** — Uscita o rimozione non modificano alcun dato
  personale del membro e non eliminano il suo account.
- **AC-US-015-09** — Dopo l'uscita nessuno, ex membro compreso, può
  modificare o rimuovere le attribuzioni verso quel nucleo. L'ex membro le
  vede sul movimento e nel proprio spazio personale (nucleo, data, importo,
  nome della categoria al momento dell'uscita), non vede modifiche
  successive del nucleo e le ritrova nell'esportazione
  ([US-020](US-020-data-export.md)).
- **AC-US-015-10** — Dopo l'uscita l'ex membro può opporsi alla
  conservazione di tutte o di alcune delle proprie quote nel nucleo
  (FR-045). Durante la valutazione le quote sono limitate ed escluse da
  report e budget del nucleo; se l'opposizione è accolta sono eliminate dal
  nucleo, i report ricalcolati con un avviso senza nome, i movimenti
  originali restano invariati e non sono più vincolati da quelle quote; se è
  respinta l'ex membro è informato prima della revoca della limitazione.
- **AC-US-015-11** — Data un'uscita personale di 100,00 € attribuita per
  60,00 € al nucleo A e per 40,00 € al nucleo B, dopo la mia uscita da A: il
  residuo attribuibile resta 0,00 €; ridurre l'importo è rifiutato finché
  non riduco l'attribuzione a B e non può comunque scendere sotto 60,00 €;
  eliminare il movimento, cambiarne il tipo, trasformarlo in giroconto o in
  trasferimento tra spazi è rifiutato con un messaggio che indica la quota
  in un nucleo lasciato e la possibilità di una rettifica contabile;
  cambiarne la data è consentito e la quota di A
  resta nel mese originale.
- **AC-US-015-12** — Se rientro in A con un nuovo invito, la quota di
  60,00 € resta con "ex membro" e non modificabile; una nuova attribuzione
  dello stesso movimento ad A è rifiutata e il report di A conta 60,00 € una
  sola volta. Posso attribuire ad A altri movimenti.
- **AC-US-015-13** — La rimozione o il declassamento di un altro
  amministratore ha effetto dopo un preavviso di 7 giorni, comunicato
  all'interessato e visibile a tutti i membri; durante il preavviso
  l'interessato mantiene ruolo e accessi e può esportare i dati del nucleo;
  l'amministratore che l'ha avviato può annullarlo. La rinuncia al proprio
  ruolo e la rimozione di un Membro hanno effetto immediato.
- **AC-US-015-14** — Con il movimento di AC-11, se l'importo corretto era
  80,00 € e chiedo una rettifica contabile dichiarandone il motivo,
  l'operazione è bloccata e nulla cambia finché non riconcilio
  esplicitamente le attribuzioni: se indico 20,00 € per l'attribuzione a B,
  importo e attribuzione sono aggiornati in un'unica operazione e la quota
  di 60,00 € in A resta invariata. Se il movimento era un duplicato, la
  rettifica resta bloccata anche se indico la rimozione dell'attribuzione a
  B: la quota in A si riconcilia solo con le autorizzazioni da definire in
  [Q-014](../open-questions-and-risks.md#q-014--movimenti-vincolati-e-ritiro-delle-quote-dellex-membro),
  il movimento resta vincolato e il messaggio indica la quota in A. In
  nessun caso un'attribuzione è ridotta automaticamente né si apre
  un'opposizione.
- **AC-US-015-15** — Alla scadenza ogni preavviso è rivalidato in un'unica
  operazione: se durante il preavviso con cui l'amministratore A declassa
  l'amministratore B, A lascia il nucleo o rinuncia al ruolo, il
  declassamento decade e B resta amministratore; se A e B avviano preavvisi
  l'uno contro l'altro, si applica solo quello avviato per primo e l'altro
  decade. Un nucleo con altri membri non resta mai senza amministratore e
  i membri sono informati delle decadenze.

## Verifica

Test di accettazione automatizzati, inclusa una prova per ogni riga della
matrice dei permessi; estensione della suite di test negativi con il caso
"ex membro"; verifica che nessuna vista del nucleo mostri nome o descrizioni
scritte dall'ex membro nelle attribuzioni né il collegamento con i movimenti
di origine; verifica della capienza (DR-012 punto 8) su sequenze di uscita,
rientro, modifica ed eliminazione.

Verificabilità per parti: le parti di AC-03 e AC-04 su condivisioni e
attribuzioni e AC-09, AC-11, AC-12 e AC-14 dopo [US-017](US-017-read-only-sharing.md)
e [US-018](US-018-transaction-attribution.md); la parte di AC-03 sulle
voci del registro dopo [US-022](US-022-activity-log.md), se il registro
completo è realizzato, mentre le voci dell'audit minimo sulle azioni di
questa storia sono verificate da AC-US-022-01; l'esportazione in AC-07 e
AC-13 dopo [US-020](US-020-data-export.md); AC-10 dopo
[US-021](US-021-account-deletion.md), che realizza la valutazione delle
opposizioni. Le parti che dipendono da storie di M5 sono verificate al
completamento di M5.

## Task

- **TASK-045** — Cambio di ruolo e applicazione della matrice dei permessi
  (AC-01, AC-02).
- **TASK-046** — Rimozione e uscita dei membri con revoca degli accessi e
  delle condivisioni e occultamento dell'identità nelle attribuzioni
  storiche e nel registro (AC-03, AC-04, AC-08).
- **TASK-047** — Continuità dell'amministrazione, rinomina ed eliminazione
  del nucleo (AC-05 – AC-07).
- **TASK-078** — Mantenimento del collegamento tecnico tra attribuzioni,
  movimenti di origine ed ex membro, vincoli di capienza e rientro (AC-09,
  AC-11, AC-12).
- **TASK-079** — Opposizione dell'ex membro, che usa la valutazione delle
  opposizioni di TASK-077 (AC-10).
- **TASK-083** — Preavviso per rimozione e declassamento di amministratori
  e per l'eliminazione del nucleo, con rivalidazione alla scadenza (AC-07,
  AC-13, AC-15).
- **TASK-085** — Rettifica contabile dei movimenti vincolati, con blocco e
  riconciliazione esplicita delle attribuzioni (AC-14).

## Definition of Ready

READY per la progettazione. Q-004 è decisa e il collegamento tecnico con il
movimento è deciso (2026-10-28); il blocco dei movimenti vincolati segue il
default di Q-014. La base giuridica per conservare quote e collegamento
degli ex membri è inclusa in Q-012: AC-03, AC-04, AC-09 – AC-12 e AC-14 possono
cambiare e non si usano con dati reali prima del gate di utilizzo. TASK-079
va pianificato dopo TASK-077.

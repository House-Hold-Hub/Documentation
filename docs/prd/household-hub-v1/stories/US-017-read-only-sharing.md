# US-017 — Condivisione in sola lettura

| Campo | Valore |
|---|---|
| Milestone | [M4 — Nuclei familiari](../milestones/M4-households.md) |
| Requisiti | [FR-026](../requirements.md#fr-026--condivisione-in-sola-lettura), NFR-001 |
| Regole | [DR-002](../domain-rules.md#dr-002--privacy-per-default), [DR-004](../domain-rules.md#dr-004--condivisione-in-sola-lettura), [DR-011](../domain-rules.md#dr-011--perimetro-dei-report) |
| Dipende da | [US-015](US-015-household-roles-and-members.md), [US-003](US-003-personal-accounts.md) |
| DoR | READY |

## Storia

Come titolare di un conto personale, voglio mostrarlo alla mia famiglia
senza che possa modificarlo, così da essere trasparente quando lo scelgo.

## Esito atteso

Il conto condiviso è visibile ai membri dei nuclei scelti, in sola
lettura, revocabile in ogni momento e senza effetti sui totali del nucleo.

## Criteri di accettazione

- **AC-US-017-01** — Condivido il mio "Conto personale" con il nucleo A:
  i membri di A ne vedono nome, tipologia, saldo e movimenti con le mie
  categorie personali; i membri del nucleo B, di cui pure faccio parte,
  non lo vedono.
- **AC-US-017-02** — I membri di A non possono modificare, eliminare,
  categorizzare, attribuire movimenti del conto né importarvi file.
- **AC-US-017-03** — Posso condividere lo stesso conto con più nuclei e
  vedere per ogni conto con quali nuclei è condiviso.
- **AC-US-017-04** — Dopo la revoca, ogni accesso dei membri di A al conto
  ha lo stesso esito di una risorsa inesistente.
- **AC-US-017-05** — Report, budget e patrimonio del nucleo A sono identici
  prima e dopo la condivisione.
- **AC-US-017-06** — Posso condividere solo con nuclei di cui sono membro
  attivo; se lascio un nucleo o ne vengo rimosso, le mie condivisioni verso
  quel nucleo sono revocate.
- **AC-US-017-07** — La condivisione non rende visibili altri miei conti,
  le mie categorie non usate dal conto né i miei budget.
- **AC-US-017-08** — Un conto condiviso poi archiviato resta visibile in
  sola lettura finché la condivisione è attiva.

## Verifica

Test di accettazione automatizzati con un titolare membro di due nuclei;
confronto dei totali del nucleo prima e dopo la condivisione; estensione
della suite di test negativi.

## Task

- **TASK-051** — Condivisione e revoca per conto e nucleo (AC-01, AC-03,
  AC-04, AC-06).
- **TASK-052** — Vista in sola lettura del conto condiviso (AC-02, AC-07, AC-08).
- **TASK-053** — Esclusione dei conti condivisi da report, budget e
  patrimonio del nucleo (AC-05).

## Definition of Ready

READY.

# US-019 — Report e budget del nucleo

| Campo | Valore |
|---|---|
| Milestone | [M4 — Nuclei familiari](../milestones/M4-households.md) |
| Requisiti | [FR-030](../requirements.md#fr-030--report-mensile-per-categoria), [FR-033](../requirements.md#fr-033--perimetro-dei-report-del-nucleo), [FR-034](../requirements.md#fr-034--budget-mensili), NFR-005, NFR-006 |
| Regole | [DR-007](../domain-rules.md#dr-007--movimenti-tra-spazi-diversi), [DR-011](../domain-rules.md#dr-011--perimetro-dei-report), [DR-012](../domain-rules.md#dr-012--invariante-dei-totali), [DR-019](../domain-rules.md#dr-019--budget), [DR-023](../domain-rules.md#dr-023--uscita-e-rimozione-dal-nucleo), [DR-024](../domain-rules.md#dr-024--eliminazione-dellaccount-e-storico-del-nucleo), [DR-025](../domain-rules.md#dr-025--opposizione-alla-conservazione-nello-storico-del-nucleo) |
| Dipende da | [US-016](US-016-household-accounts-and-categories.md), [US-017](US-017-read-only-sharing.md), [US-018](US-018-transaction-attribution.md), [US-013](US-013-budgets.md) |
| Questioni collegate | [Q-004](../open-questions-and-risks.md#q-004--attribuzioni-di-un-membro-uscito) (decisa), [Q-012](../open-questions-and-risks.md#q-012--valutazione-legale-del-trattamento-alleliminazione) (quote di ex membri e storiche, gate di utilizzo) |
| DoR | READY |

## Storia

Come membro di un nucleo, voglio vedere quanto spende la famiglia per
categoria e confrontarlo con il budget familiare, così da pianificare
insieme senza doppi conteggi.

## Esito atteso

Report e budget del nucleo calcolati sul perimetro corretto: conti del
nucleo più quote attribuite, mai i conti condivisi in sola lettura.

## Dataset di riferimento

Nucleo A, maggio:

| Elemento | Importo | Categoria del nucleo |
|---|---|---|
| Uscita dal conto cointestato | 120,00 | Alimentari |
| Uscita dal conto cointestato | 50,00 | Bollette › Luce |
| Versamento di Marco dal conto personale al conto cointestato (trasferimento tra spazi) | 1.000,00 | — |
| Giroconto dal conto cointestato al conto deposito del nucleo | 200,00 | — |
| Quota attribuita da Marco (movimento personale di 100,00) | 60,00 | Alimentari |
| Quota attribuita da Giulia (movimento personale di 80,00) | 40,00 | Ristorazione |
| Rimborso dal conto cointestato a Marco della spesa che ha attribuito (trasferimento tra spazi; Marco lo registra come trasferimento tra spazi anche nel proprio spazio) | 60,00 | — |
| Uscite del conto personale di Giulia condiviso in sola lettura con A | 300,00 | — |

## Criteri di accettazione

- **AC-US-019-01** — Con il dataset di riferimento il report di maggio del
  nucleo A mostra: entrate 0,00; uscite 270,00; saldo netto −270,00;
  Alimentari 180,00; Bollette 50,00 (Luce 50,00); Ristorazione 40,00. Le
  uscite del conto condiviso, il giroconto e i trasferimenti tra spazi non
  sono conteggiati: la spesa di Marco entra una sola volta, tramite la quota
  di 60,00, anche se il nucleo gliel'ha rimborsata. Fuori dai totali il
  report mostra trasferimenti tra spazi in entrata 1.000,00 e in uscita
  60,00.
- **AC-US-019-02** — Su ogni mese del dataset di verifica del nucleo valgono
  tutte le invarianti di DR-012, incluso il caso di un conto condiviso con
  A che ha anche movimenti attribuiti ad A e il caso di un membro che esce
  e rientra in A.
- **AC-US-019-03** — Il dettaglio di Alimentari mostra il movimento del
  conto cointestato e la quota di Marco nella forma riservata di FR-029.
- **AC-US-019-04** — Una quota attribuita al nucleo B non compare mai nel
  report di A.
- **AC-US-019-05** — Ridurre, rimuovere o cambiare data a un'attribuzione
  aggiorna subito report e consuntivo del budget dei mesi interessati.
- **AC-US-019-06** — Un amministratore definisce voci di budget del nucleo
  con le categorie del nucleo; il consuntivo include le quote attribuite
  secondo DR-019; i Membri vedono il budget ma non possono modificarlo.
- **AC-US-019-07** — Il report personale di Marco per maggio continua a
  mostrare 100,00 € nella sua categoria personale e non conta il versamento
  di 1.000,00 né il rimborso di 60,00, registrati come trasferimenti tra
  spazi.
- **AC-US-019-08** — Le quote di un membro uscito dal nucleo restano
  conteggiate nei mesi in cui sono state attribuite e nel dettaglio
  compaiono come attribuite a un "ex membro", senza nome e senza
  distinguere tra ex membri diversi (DR-023). Se l'ex
  membro elimina il proprio account restano come quote storiche del nucleo
  e i totali non cambiano, salvo opposizione accolta e ripiego (DR-024,
  DR-025; [US-021](US-021-account-deletion.md)); durante un'opposizione le
  quote interessate sono escluse dai totali (DR-025).
- **AC-US-019-09** — Report e budget del nucleo rispettano NFR-006.
- **AC-US-019-10** — Con il dataset di riferimento il saldo del conto
  cointestato varia a maggio di +570,00 € e quello del conto deposito del
  nucleo di +200,00 €: la somma, 770,00 €, è uguale ai movimenti ordinari
  dei soli conti del nucleo (−170,00 €) più i trasferimenti tra spazi netti
  (+940,00 €); le quote attribuite (100,00 €) entrano nel report ma in
  nessun saldo (DR-012 punto 7).

## Verifica

Test di accettazione automatizzati sul dataset di riferimento e sul
dataset di verifica di [US-007](US-007-monthly-report.md) esteso con conti
del nucleo, attribuzioni parziali a due nuclei, conti condivisi, trasferimenti tra
spazi, rimborsi a un membro e membri usciti e rientrati; misura di prestazioni.

## Task

- **TASK-058** — Calcolo del report del nucleo sul perimetro di DR-011
  (AC-01, AC-02, AC-04, AC-05, AC-07, AC-08, AC-10).
- **TASK-059** — Dettaglio del report con quote attribuite in forma
  riservata (AC-03).
- **TASK-060** — Budget del nucleo con permessi per ruolo (AC-06).
- **TASK-061** — Estensione del dataset di verifica e misura delle
  prestazioni (AC-02, AC-09).

## Definition of Ready

READY.

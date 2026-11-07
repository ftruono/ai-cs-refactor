# Analisi dei refactoring validi (stesso file e stessa funzione) — subset `small`

- Occorrenze di smell (una riga del CSV ciascuna): **397**
- Refactoring **valido** = entry di PyRef nello stesso file (`same_file`) e sulla stessa funzione (`same_function`) dello smell
- Tipologie ricavate dalle entry gia' filtrate (`pyref_out_same_function_*`), non dall'elenco generico del commit

## Introduzione

### Copertura (status PyRef)

| Status | # occorrenze | % |
|---|---:|---:|
| `ok` | 316 | 79.6% |
| `nodiff` | 45 | 11.3% |
| `timeout` | 30 | 7.6% |
| `missing` | 6 | 1.5% |

### Dal refactoring generico a quello valido

Occorrenze con `status=ok`: **316**

| Passo | # occorrenze | % su ok |
|---|---:|---:|
| PyRef trova refactoring nel commit (qualsiasi file) | 139 | 44.0% |
| ... di cui nello stesso file (`same_file`) | 60 | 19.0% |
| ... di cui sulla stessa funzione (`same_function`) = **valido** | 27 | 8.5% |

### Quota con refactoring valido

Domanda: in quante introduzioni di smell c'e' un refactoring valido (stesso file e stessa funzione)?

| Unita' | Con refactoring valido | Analizzabili (`ok`) | Quota | IC 95% (Wilson) |
|---|---:|---:|---:|---|
| Occorrenze di smell | 27 | 316 | 8.5% | 5.9% - 12.1% |
| Commit (almeno una occorrenza valida) | 18 | 161 | 11.2% | 7.2% - 17.0% |

L'intervallo sulle occorrenze e' ottimistico: le occorrenze dello stesso commit non sono indipendenti (l'intervallo per commit e' piu' prudente).

### Ratio di refactoring valido per tipologia di smell

| Smell | Istanze totali | Analizzabili | Con refactoring valido | Ratio |
|---|---:|---:|---:|---:|
| `pytorch_call_method_misused` | 55 | 46 | 9 | 19.6% |
| `gradients_not_cleared_before_backward_propagation` | 17 | 11 | 2 | 18.2% |
| `in_place_apis_misused` | 88 | 80 | 8 | 10.0% |
| `columns_and_datatype_not_explicitly_set` | 221 | 167 | 8 | 4.8% |
| `Chain_Indexing` | 1 | 1 | 0 | 0.0% |
| `tensor_array_not_used` | 15 | 11 | 0 | 0.0% |

### Tipologie di refactoring valide

- Occorrenze con refactoring valido: **27**
- Entry di PyRef valide (stesso file e stessa funzione): **29**
- Tipi di refactoring contati: **31** (una entry puo' avere piu' tipi)
- Media: 1.07 entry valide per occorrenza

| Entry valide per occorrenza | # occorrenze |
|---|---:|
| 1 | 25 |
| 2 | 2 |

| Tipo di refactoring | Occorrenze | % |
|---|---:|---:|
| Rename Method | 12 | 38.7% |
| Extract Method | 8 | 25.8% |
| Remove Parameter | 4 | 12.9% |
| Change/Rename Parameter | 2 | 6.5% |
| Pull Up Method | 2 | 6.5% |
| Add Parameter | 2 | 6.5% |
| Move Method | 1 | 3.2% |

### Tipologie di refactoring valide per smell

**`pytorch_call_method_misused`** (totale: 13)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Remove Parameter | 4 |
| Rename Method | 4 |
| Extract Method | 3 |
| Pull Up Method | 2 |

**`gradients_not_cleared_before_backward_propagation`** (totale: 2)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 1 |
| Move Method | 1 |

**`in_place_apis_misused`** (totale: 8)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 7 |
| Extract Method | 1 |

**`columns_and_datatype_not_explicitly_set`** (totale: 8)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 4 |
| Change/Rename Parameter | 2 |
| Add Parameter | 1 |
| Rename Method | 1 |

### Correlazione di Spearman: refactoring valido vs numero di smell nel commit

Occorrenze in commit con `status=ok` e almeno un refactoring (`pyref_refactor_intro_count` > 0): **139** (commit distinti: 70)

- rho di Spearman: **-0.226** (p-value = 0.00741, n = 139)

| Refactoring valido (A) | # occorrenze | smell nel commit (B): mediana | media |
|---|---:|---:|---:|
| 0 | 112 | 3.5 | 3.70 |
| 1 | 27 | 2.0 | 2.26 |

Nota: le occorrenze dello stesso commit hanno lo stesso B, quindi non sono osservazioni indipendenti e il p-value tende a essere troppo ottimistico.

## Rimozione

### Copertura (status PyRef)

| Status | # occorrenze | % |
|---|---:|---:|
| `ok` | 300 | 75.6% |
| `timeout` | 56 | 14.1% |
| `nodiff` | 35 | 8.8% |
| `missing` | 6 | 1.5% |

### Dal refactoring generico a quello valido

Occorrenze con `status=ok`: **300**

| Passo | # occorrenze | % su ok |
|---|---:|---:|
| PyRef trova refactoring nel commit (qualsiasi file) | 137 | 45.7% |
| ... di cui nello stesso file (`same_file`) | 65 | 21.7% |
| ... di cui sulla stessa funzione (`same_function`) = **valido** | 17 | 5.7% |

### Quota con refactoring valido

Domanda: in quante rimozioni di smell c'e' un refactoring valido (stesso file e stessa funzione)?

| Unita' | Con refactoring valido | Analizzabili (`ok`) | Quota | IC 95% (Wilson) |
|---|---:|---:|---:|---|
| Occorrenze di smell | 17 | 300 | 5.7% | 3.6% - 8.9% |
| Commit (almeno una occorrenza valida) | 13 | 119 | 10.9% | 6.5% - 17.8% |

L'intervallo sulle occorrenze e' ottimistico: le occorrenze dello stesso commit non sono indipendenti (l'intervallo per commit e' piu' prudente).

### Ratio di refactoring valido per tipologia di smell

| Smell | Istanze totali | Analizzabili | Con refactoring valido | Ratio |
|---|---:|---:|---:|---:|
| `gradients_not_cleared_before_backward_propagation` | 17 | 9 | 1 | 11.1% |
| `columns_and_datatype_not_explicitly_set` | 221 | 159 | 11 | 6.9% |
| `pytorch_call_method_misused` | 55 | 44 | 2 | 4.5% |
| `in_place_apis_misused` | 88 | 74 | 3 | 4.1% |
| `Chain_Indexing` | 1 | 1 | 0 | 0.0% |
| `tensor_array_not_used` | 15 | 13 | 0 | 0.0% |

### Tipologie di refactoring valide

- Occorrenze con refactoring valido: **17**
- Entry di PyRef valide (stesso file e stessa funzione): **22**
- Tipi di refactoring contati: **22** (una entry puo' avere piu' tipi)
- Media: 1.29 entry valide per occorrenza

| Entry valide per occorrenza | # occorrenze |
|---|---:|
| 1 | 15 |
| 3 | 1 |
| 4 o piu | 1 |

| Tipo di refactoring | Occorrenze | % |
|---|---:|---:|
| Extract Method | 8 | 36.4% |
| Remove Parameter | 5 | 22.7% |
| Add Parameter | 5 | 22.7% |
| Rename Method | 3 | 13.6% |
| Change/Rename Parameter | 1 | 4.5% |

### Tipologie di refactoring valide per smell

**`gradients_not_cleared_before_backward_propagation`** (totale: 1)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Remove Parameter | 1 |

**`columns_and_datatype_not_explicitly_set`** (totale: 13)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 8 |
| Add Parameter | 3 |
| Change/Rename Parameter | 1 |
| Rename Method | 1 |

**`pytorch_call_method_misused`** (totale: 2)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 1 |
| Rename Method | 1 |

**`in_place_apis_misused`** (totale: 6)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Remove Parameter | 4 |
| Add Parameter | 1 |
| Rename Method | 1 |

### Correlazione di Spearman: refactoring valido vs numero di smell nel commit

Occorrenze in commit con `status=ok` e almeno un refactoring (`pyref_ref_removed_count` > 0): **137** (commit distinti: 56)

- rho di Spearman: **-0.110** (p-value = 0.202, n = 137)

| Refactoring valido (A) | # occorrenze | smell nel commit (B): mediana | media |
|---|---:|---:|---:|
| 0 | 120 | 3.0 | 5.97 |
| 1 | 17 | 3.0 | 4.82 |

Nota: le occorrenze dello stesso commit hanno lo stesso B, quindi non sono osservazioni indipendenti e il p-value tende a essere troppo ottimistico.

# Analisi dei refactoring validi (stesso file e stessa funzione) — subset `large`

- Occorrenze di smell (una riga del CSV ciascuna): **3905**
- Refactoring **valido** = entry di PyRef nello stesso file (`same_file`) e sulla stessa funzione (`same_function`) dello smell
- Tipologie ricavate dalle entry gia' filtrate (`pyref_out_same_function_*`), non dall'elenco generico del commit

## Introduzione

### Copertura (status PyRef)

| Status | # occorrenze | % |
|---|---:|---:|
| `ok` | 2530 | 64.8% |
| `nodiff` | 562 | 14.4% |
| `timeout` | 506 | 13.0% |
| `missing` | 307 | 7.9% |

### Dal refactoring generico a quello valido

Occorrenze con `status=ok`: **2530**

| Passo | # occorrenze | % su ok |
|---|---:|---:|
| PyRef trova refactoring nel commit (qualsiasi file) | 1180 | 46.6% |
| ... di cui nello stesso file (`same_file`) | 603 | 23.8% |
| ... di cui sulla stessa funzione (`same_function`) = **valido** | 206 | 8.1% |

### Quota con refactoring valido

Domanda: in quante introduzioni di smell c'e' un refactoring valido (stesso file e stessa funzione)?

| Unita' | Con refactoring valido | Analizzabili (`ok`) | Quota | IC 95% (Wilson) |
|---|---:|---:|---:|---|
| Occorrenze di smell | 206 | 2530 | 8.1% | 7.1% - 9.3% |
| Commit (almeno una occorrenza valida) | 89 | 921 | 9.7% | 7.9% - 11.7% |

L'intervallo sulle occorrenze e' ottimistico: le occorrenze dello stesso commit non sono indipendenti (l'intervallo per commit e' piu' prudente).

### Ratio di refactoring valido per tipologia di smell

| Smell | Istanze totali | Analizzabili | Con refactoring valido | Ratio |
|---|---:|---:|---:|---:|
| `memory_not_freed` | 7 | 7 | 2 | 28.6% |
| `merge_api_parameter_not_explicitly_set` | 4 | 4 | 1 | 25.0% |
| `Chain_Indexing` | 15 | 11 | 2 | 18.2% |
| `columns_and_datatype_not_explicitly_set` | 1477 | 1074 | 155 | 14.4% |
| `dataframe_conversion_api_misused` | 8 | 8 | 1 | 12.5% |
| `pytorch_call_method_misused` | 329 | 253 | 15 | 5.9% |
| `in_place_apis_misused` | 325 | 224 | 7 | 3.1% |
| `tensor_array_not_used` | 1566 | 833 | 21 | 2.5% |
| `gradients_not_cleared_before_backward_propagation` | 172 | 115 | 2 | 1.7% |
| `unnecessary_iteration` | 1 | 1 | 0 | 0.0% |

### Tipologie di refactoring valide

- Occorrenze con refactoring valido: **206**
- Entry di PyRef valide (stesso file e stessa funzione): **210**
- Tipi di refactoring contati: **229** (una entry puo' avere piu' tipi)
- Media: 1.02 entry valide per occorrenza

| Entry valide per occorrenza | # occorrenze |
|---|---:|
| 1 | 202 |
| 2 | 4 |

| Tipo di refactoring | Occorrenze | % |
|---|---:|---:|
| Rename Method | 131 | 57.2% |
| Add Parameter | 33 | 14.4% |
| Extract Method | 28 | 12.2% |
| Move Method | 20 | 8.7% |
| Change/Rename Parameter | 7 | 3.1% |
| Inline Method | 4 | 1.7% |
| Remove Parameter | 3 | 1.3% |
| Change Return Type | 3 | 1.3% |

### Tipologie di refactoring valide per smell

**`memory_not_freed`** (totale: 2)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 2 |

**`merge_api_parameter_not_explicitly_set`** (totale: 1)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 1 |

**`Chain_Indexing`** (totale: 2)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 2 |

**`columns_and_datatype_not_explicitly_set`** (totale: 173)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 96 |
| Add Parameter | 24 |
| Extract Method | 23 |
| Move Method | 18 |
| Change Return Type | 3 |
| Change/Rename Parameter | 3 |
| Inline Method | 3 |
| Remove Parameter | 3 |

**`dataframe_conversion_api_misused`** (totale: 1)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 1 |

**`pytorch_call_method_misused`** (totale: 16)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 14 |
| Change/Rename Parameter | 1 |
| Extract Method | 1 |

**`in_place_apis_misused`** (totale: 10)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 3 |
| Change/Rename Parameter | 3 |
| Rename Method | 3 |
| Extract Method | 1 |

**`tensor_array_not_used`** (totale: 22)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 15 |
| Add Parameter | 4 |
| Move Method | 2 |
| Inline Method | 1 |

**`gradients_not_cleared_before_backward_propagation`** (totale: 2)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 2 |

### Correlazione di Spearman: refactoring valido vs numero di smell nel commit

Occorrenze in commit con `status=ok` e almeno un refactoring (`pyref_refactor_intro_count` > 0): **1180** (commit distinti: 383)

- rho di Spearman: **-0.096** (p-value = 0.000979, n = 1180)

| Refactoring valido (A) | # occorrenze | smell nel commit (B): mediana | media |
|---|---:|---:|---:|
| 0 | 974 | 5.0 | 28.87 |
| 1 | 206 | 4.5 | 7.02 |

Nota: le occorrenze dello stesso commit hanno lo stesso B, quindi non sono osservazioni indipendenti e il p-value tende a essere troppo ottimistico.

## Rimozione

### Copertura (status PyRef)

| Status | # occorrenze | % |
|---|---:|---:|
| `ok` | 2488 | 63.7% |
| `timeout` | 602 | 15.4% |
| `nodiff` | 508 | 13.0% |
| `missing` | 307 | 7.9% |

### Dal refactoring generico a quello valido

Occorrenze con `status=ok`: **2488**

| Passo | # occorrenze | % su ok |
|---|---:|---:|
| PyRef trova refactoring nel commit (qualsiasi file) | 1328 | 53.4% |
| ... di cui nello stesso file (`same_file`) | 779 | 31.3% |
| ... di cui sulla stessa funzione (`same_function`) = **valido** | 174 | 7.0% |

### Quota con refactoring valido

Domanda: in quante rimozioni di smell c'e' un refactoring valido (stesso file e stessa funzione)?

| Unita' | Con refactoring valido | Analizzabili (`ok`) | Quota | IC 95% (Wilson) |
|---|---:|---:|---:|---|
| Occorrenze di smell | 174 | 2488 | 7.0% | 6.1% - 8.1% |
| Commit (almeno una occorrenza valida) | 133 | 789 | 16.9% | 14.4% - 19.6% |

L'intervallo sulle occorrenze e' ottimistico: le occorrenze dello stesso commit non sono indipendenti (l'intervallo per commit e' piu' prudente).

### Ratio di refactoring valido per tipologia di smell

| Smell | Istanze totali | Analizzabili | Con refactoring valido | Ratio |
|---|---:|---:|---:|---:|
| `memory_not_freed` | 7 | 6 | 2 | 33.3% |
| `Chain_Indexing` | 15 | 8 | 2 | 25.0% |
| `merge_api_parameter_not_explicitly_set` | 4 | 4 | 1 | 25.0% |
| `gradients_not_cleared_before_backward_propagation` | 172 | 138 | 15 | 10.9% |
| `columns_and_datatype_not_explicitly_set` | 1477 | 1050 | 98 | 9.3% |
| `pytorch_call_method_misused` | 329 | 249 | 21 | 8.4% |
| `in_place_apis_misused` | 325 | 222 | 13 | 5.9% |
| `tensor_array_not_used` | 1566 | 803 | 22 | 2.7% |
| `dataframe_conversion_api_misused` | 8 | 7 | 0 | 0.0% |
| `unnecessary_iteration` | 1 | 1 | 0 | 0.0% |

### Tipologie di refactoring valide

- Occorrenze con refactoring valido: **174**
- Entry di PyRef valide (stesso file e stessa funzione): **188**
- Tipi di refactoring contati: **205** (una entry puo' avere piu' tipi)
- Media: 1.08 entry valide per occorrenza

| Entry valide per occorrenza | # occorrenze |
|---|---:|
| 1 | 161 |
| 2 | 12 |
| 3 | 1 |

| Tipo di refactoring | Occorrenze | % |
|---|---:|---:|
| Rename Method | 91 | 44.4% |
| Extract Method | 41 | 20.0% |
| Add Parameter | 32 | 15.6% |
| Change/Rename Parameter | 13 | 6.3% |
| Remove Parameter | 11 | 5.4% |
| Inline Method | 11 | 5.4% |
| Change Return Type | 4 | 2.0% |
| Move Method | 2 | 1.0% |

### Tipologie di refactoring valide per smell

**`memory_not_freed`** (totale: 4)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 4 |

**`Chain_Indexing`** (totale: 2)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 2 |

**`merge_api_parameter_not_explicitly_set`** (totale: 1)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 1 |

**`gradients_not_cleared_before_backward_propagation`** (totale: 17)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 13 |
| Add Parameter | 2 |
| Rename Method | 2 |

**`columns_and_datatype_not_explicitly_set`** (totale: 120)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 57 |
| Extract Method | 19 |
| Add Parameter | 18 |
| Change/Rename Parameter | 8 |
| Remove Parameter | 8 |
| Inline Method | 5 |
| Change Return Type | 3 |
| Move Method | 2 |

**`pytorch_call_method_misused`** (totale: 23)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 15 |
| Inline Method | 5 |
| Add Parameter | 2 |
| Change/Rename Parameter | 1 |

**`in_place_apis_misused`** (totale: 15)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 5 |
| Change/Rename Parameter | 3 |
| Rename Method | 3 |
| Extract Method | 2 |
| Change Return Type | 1 |
| Remove Parameter | 1 |

**`tensor_array_not_used`** (totale: 23)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 13 |
| Add Parameter | 3 |
| Extract Method | 3 |
| Remove Parameter | 2 |
| Change/Rename Parameter | 1 |
| Inline Method | 1 |

### Correlazione di Spearman: refactoring valido vs numero di smell nel commit

Occorrenze in commit con `status=ok` e almeno un refactoring (`pyref_ref_removed_count` > 0): **1328** (commit distinti: 379)

- rho di Spearman: **-0.249** (p-value = 3.25e-20, n = 1328)

| Refactoring valido (A) | # occorrenze | smell nel commit (B): mediana | media |
|---|---:|---:|---:|
| 0 | 1154 | 7.0 | 16.70 |
| 1 | 174 | 2.0 | 6.61 |

Nota: le occorrenze dello stesso commit hanno lo stesso B, quindi non sono osservazioni indipendenti e il p-value tende a essere troppo ottimistico.

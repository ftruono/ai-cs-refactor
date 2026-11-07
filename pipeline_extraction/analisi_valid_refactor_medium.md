# Analisi dei refactoring validi (stesso file e stessa funzione) — subset `medium`

- Occorrenze di smell (una riga del CSV ciascuna): **2048**
- Refactoring **valido** = entry di PyRef nello stesso file (`same_file`) e sulla stessa funzione (`same_function`) dello smell
- Tipologie ricavate dalle entry gia' filtrate (`pyref_out_same_function_*`), non dall'elenco generico del commit

## Introduzione

### Copertura (status PyRef)

| Status | # occorrenze | % |
|---|---:|---:|
| `ok` | 1300 | 63.5% |
| `timeout` | 411 | 20.1% |
| `nodiff` | 277 | 13.5% |
| `missing` | 60 | 2.9% |

### Dal refactoring generico a quello valido

Occorrenze con `status=ok`: **1300**

| Passo | # occorrenze | % su ok |
|---|---:|---:|
| PyRef trova refactoring nel commit (qualsiasi file) | 346 | 26.6% |
| ... di cui nello stesso file (`same_file`) | 191 | 14.7% |
| ... di cui sulla stessa funzione (`same_function`) = **valido** | 69 | 5.3% |

### Quota con refactoring valido

Domanda: in quante introduzioni di smell c'e' un refactoring valido (stesso file e stessa funzione)?

| Unita' | Con refactoring valido | Analizzabili (`ok`) | Quota | IC 95% (Wilson) |
|---|---:|---:|---:|---|
| Occorrenze di smell | 69 | 1300 | 5.3% | 4.2% - 6.7% |
| Commit (almeno una occorrenza valida) | 41 | 501 | 8.2% | 6.1% - 10.9% |

L'intervallo sulle occorrenze e' ottimistico: le occorrenze dello stesso commit non sono indipendenti (l'intervallo per commit e' piu' prudente).

### Ratio di refactoring valido per tipologia di smell

| Smell | Istanze totali | Analizzabili | Con refactoring valido | Ratio |
|---|---:|---:|---:|---:|
| `pytorch_call_method_misused` | 82 | 51 | 4 | 7.8% |
| `columns_and_datatype_not_explicitly_set` | 1214 | 759 | 45 | 5.9% |
| `in_place_apis_misused` | 618 | 409 | 18 | 4.4% |
| `gradients_not_cleared_before_backward_propagation` | 57 | 32 | 1 | 3.1% |
| `tensor_array_not_used` | 52 | 32 | 1 | 3.1% |
| `Chain_Indexing` | 3 | 1 | 0 | 0.0% |
| `dataframe_conversion_api_misused` | 16 | 11 | 0 | 0.0% |
| `memory_not_freed` | 2 | 2 | 0 | 0.0% |
| `merge_api_parameter_not_explicitly_set` | 4 | 3 | 0 | 0.0% |

### Tipologie di refactoring valide

- Occorrenze con refactoring valido: **69**
- Entry di PyRef valide (stesso file e stessa funzione): **70**
- Tipi di refactoring contati: **78** (una entry puo' avere piu' tipi)
- Media: 1.01 entry valide per occorrenza

| Entry valide per occorrenza | # occorrenze |
|---|---:|
| 1 | 68 |
| 2 | 1 |

| Tipo di refactoring | Occorrenze | % |
|---|---:|---:|
| Rename Method | 27 | 34.6% |
| Extract Method | 22 | 28.2% |
| Add Parameter | 12 | 15.4% |
| Change/Rename Parameter | 6 | 7.7% |
| Inline Method | 6 | 7.7% |
| Change Return Type | 3 | 3.8% |
| Remove Parameter | 2 | 2.6% |

### Tipologie di refactoring valide per smell

**`pytorch_call_method_misused`** (totale: 4)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 2 |
| Extract Method | 1 |
| Rename Method | 1 |

**`columns_and_datatype_not_explicitly_set`** (totale: 51)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 21 |
| Extract Method | 14 |
| Add Parameter | 8 |
| Change Return Type | 3 |
| Change/Rename Parameter | 3 |
| Remove Parameter | 2 |

**`in_place_apis_misused`** (totale: 21)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 7 |
| Inline Method | 6 |
| Rename Method | 4 |
| Change/Rename Parameter | 3 |
| Add Parameter | 1 |

**`gradients_not_cleared_before_backward_propagation`** (totale: 1)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 1 |

**`tensor_array_not_used`** (totale: 1)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 1 |

### Correlazione di Spearman: refactoring valido vs numero di smell nel commit

Occorrenze in commit con `status=ok` e almeno un refactoring (`pyref_refactor_intro_count` > 0): **346** (commit distinti: 163)

- rho di Spearman: **-0.098** (p-value = 0.0691, n = 346)

| Refactoring valido (A) | # occorrenze | smell nel commit (B): mediana | media |
|---|---:|---:|---:|
| 0 | 277 | 3.0 | 3.86 |
| 1 | 69 | 2.0 | 2.88 |

Nota: le occorrenze dello stesso commit hanno lo stesso B, quindi non sono osservazioni indipendenti e il p-value tende a essere troppo ottimistico.

## Rimozione

### Copertura (status PyRef)

| Status | # occorrenze | % |
|---|---:|---:|
| `ok` | 1549 | 75.6% |
| `timeout` | 283 | 13.8% |
| `nodiff` | 156 | 7.6% |
| `missing` | 60 | 2.9% |

### Dal refactoring generico a quello valido

Occorrenze con `status=ok`: **1549**

| Passo | # occorrenze | % su ok |
|---|---:|---:|
| PyRef trova refactoring nel commit (qualsiasi file) | 501 | 32.3% |
| ... di cui nello stesso file (`same_file`) | 238 | 15.4% |
| ... di cui sulla stessa funzione (`same_function`) = **valido** | 63 | 4.1% |

### Quota con refactoring valido

Domanda: in quante rimozioni di smell c'e' un refactoring valido (stesso file e stessa funzione)?

| Unita' | Con refactoring valido | Analizzabili (`ok`) | Quota | IC 95% (Wilson) |
|---|---:|---:|---:|---|
| Occorrenze di smell | 63 | 1549 | 4.1% | 3.2% - 5.2% |
| Commit (almeno una occorrenza valida) | 47 | 319 | 14.7% | 11.3% - 19.0% |

L'intervallo sulle occorrenze e' ottimistico: le occorrenze dello stesso commit non sono indipendenti (l'intervallo per commit e' piu' prudente).

### Ratio di refactoring valido per tipologia di smell

| Smell | Istanze totali | Analizzabili | Con refactoring valido | Ratio |
|---|---:|---:|---:|---:|
| `gradients_not_cleared_before_backward_propagation` | 57 | 19 | 4 | 21.1% |
| `dataframe_conversion_api_misused` | 16 | 11 | 1 | 9.1% |
| `pytorch_call_method_misused` | 82 | 60 | 4 | 6.7% |
| `columns_and_datatype_not_explicitly_set` | 1214 | 931 | 47 | 5.0% |
| `tensor_array_not_used` | 52 | 34 | 1 | 2.9% |
| `in_place_apis_misused` | 618 | 488 | 6 | 1.2% |
| `Chain_Indexing` | 3 | 2 | 0 | 0.0% |
| `memory_not_freed` | 2 | 2 | 0 | 0.0% |
| `merge_api_parameter_not_explicitly_set` | 4 | 2 | 0 | 0.0% |

### Tipologie di refactoring valide

- Occorrenze con refactoring valido: **63**
- Entry di PyRef valide (stesso file e stessa funzione): **66**
- Tipi di refactoring contati: **74** (una entry puo' avere piu' tipi)
- Media: 1.05 entry valide per occorrenza

| Entry valide per occorrenza | # occorrenze |
|---|---:|
| 1 | 60 |
| 2 | 3 |

| Tipo di refactoring | Occorrenze | % |
|---|---:|---:|
| Rename Method | 36 | 48.6% |
| Extract Method | 18 | 24.3% |
| Change/Rename Parameter | 6 | 8.1% |
| Add Parameter | 6 | 8.1% |
| Remove Parameter | 4 | 5.4% |
| Inline Method | 4 | 5.4% |

### Tipologie di refactoring valide per smell

**`gradients_not_cleared_before_backward_propagation`** (totale: 4)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Extract Method | 2 |
| Add Parameter | 1 |
| Rename Method | 1 |

**`dataframe_conversion_api_misused`** (totale: 1)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Add Parameter | 1 |

**`pytorch_call_method_misused`** (totale: 5)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 3 |
| Extract Method | 1 |
| Remove Parameter | 1 |

**`columns_and_datatype_not_explicitly_set`** (totale: 53)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 28 |
| Extract Method | 15 |
| Change/Rename Parameter | 5 |
| Add Parameter | 2 |
| Inline Method | 2 |
| Remove Parameter | 1 |

**`tensor_array_not_used`** (totale: 2)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Remove Parameter | 2 |

**`in_place_apis_misused`** (totale: 9)

| Tipo di refactoring | Occorrenze |
|---|---:|
| Rename Method | 4 |
| Add Parameter | 2 |
| Inline Method | 2 |
| Change/Rename Parameter | 1 |

### Correlazione di Spearman: refactoring valido vs numero di smell nel commit

Occorrenze in commit con `status=ok` e almeno un refactoring (`pyref_ref_removed_count` > 0): **501** (commit distinti: 114)

- rho di Spearman: **-0.331** (p-value = 2.63e-14, n = 501)

| Refactoring valido (A) | # occorrenze | smell nel commit (B): mediana | media |
|---|---:|---:|---:|
| 0 | 438 | 15.0 | 22.46 |
| 1 | 63 | 3.0 | 5.29 |

Nota: le occorrenze dello stesso commit hanno lo stesso B, quindi non sono osservazioni indipendenti e il p-value tende a essere troppo ottimistico.

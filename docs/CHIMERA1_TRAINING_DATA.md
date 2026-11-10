# Chimera 1 — dati reali per il primo addestramento

**Priorità:** modello Chimera 1 con pesi nuovi, NON laboratorio completo o applicazione Genesis.

Questo script **non scarica nulla alla CI**. Quando eseguito dall'operatore usa i dataset open-weight/data seguenti:

| Fonte | Scopo | Licenza dichiarata dal repository |
|---|---|---|
| [Aya](https://huggingface.co/datasets/CohereLabs/aya_dataset) | Istruzioni umane italiano/francese/inglese | Apache 2.0 |
| [OpenAssistant OASST1](https://huggingface.co/datasets/OpenAssistant/oasst1) | Risposte conversazionali sottoposte a review | Apache 2.0 |
| [GSM8K](https://huggingface.co/datasets/openai/gsm8k) | Ragionamento matematico con set di test separato | MIT |
| [MetaMathQA](https://huggingface.co/datasets/meta-math/MetaMathQA) | Varianti su problemi matematici (solo famiglia MATH) | MIT |

Controllare sempre le licenze aggiornate e la provenienza prima di distribuire dati o pesi derivati. Niente dati delle chat private.

## Preparazione dei dati

Dalla radice del repository con Python 3.11:

~~~bash
python -m pip install -e ".[data,train]"
python -m chimera_lab.prepare_sft
python -m chimera_lab validate-data --train-file data/chimera1_train.jsonl --eval-file data/chimera1_math_eval.jsonl
~~~

L'operazione scarica dati pubblici dai repository indicati e produce file JSONL **ignorati da Git**. Il manifesto contiene le licenze dichiarate e gli SHA256 degli output. Il campionamento è riproducibile, filtrato per lingua, reviewer e duplicazione delle richieste. Il set **GSM8K test** viene tenuto fuori dall'addestramento. I dataset pubblici potrebbero essere già presenti nel pretraining del modello base: questo rimane un limite della valutazione.

## Esecuzione effettiva (solo su CUDA NVIDIA)

La baseline e la candidata **devono essere valutate con lo stesso dataset e gli stessi parametri**:

~~~bash
python -m chimera_lab evaluate --model Qwen/Qwen3-4B-Instruct-2507 --eval-file data/chimera1_math_eval.jsonl --output runs/chimera1_base.json --max-new-tokens 256
python -m chimera_lab train --model Qwen/Qwen3-4B-Instruct-2507 --train-file data/chimera1_train.jsonl --eval-file data/chimera1_math_eval.jsonl --output outputs/chimera1_sft --steps 3500 --max-length 1024
python -m chimera_lab evaluate --model outputs/chimera1_sft --eval-file data/chimera1_math_eval.jsonl --output runs/chimera1_sft.json --max-new-tokens 256
python -m chimera_lab compare --baseline runs/chimera1_base.json --candidate runs/chimera1_sft.json --output runs/chimera1_comparison.json
~~~

**Attenzione**: 3500 step su 4B con 1024 token **non garantiscono** che l'ASUS RTX 4060 8 GB possa completare il training. Se non basta, serve una GPU Cloud più capace **solo previa autorizzazione a eventuali spese**. I dati e l'addestramento devono essere effettivamente eseguiti prima di chiamare Chimera 1 un modello creato.

Il primo rapporto di matematiche non prova intelligenza generale. Seguiranno test indipendenti di programmazione, ragionamento, robustezza, italiano/francese/inglese e uso degli strumenti. La qualità di un modello non si riduce alla precisione di un singolo benchmark.

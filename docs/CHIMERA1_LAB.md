# Chimera 1 — Protocollo del primo esperimento

**Non esiste ancora un modello Chimera 1 addestrato e validato.** Questa PR prepara un laboratorio riproducibile, senza costruire l'app Genesis.

## Modelli iniziali

- Principale: **Qwen/Qwen3-4B-Instruct-2507**, Apache 2.0, 4B generalista. Verificare licenza nel repository modello ufficiale.
- Piano ridotto, se la RTX 4060 8 GB non riesce a fare training della 4B: **Qwen/Qwen3-1.7B**, Apache 2.0.
- Chimera 1 deve avere nuovi pesi realmente addestrati (qui: adapter LoRA). Una LoRA **non** è una foundation model da zero. In un ciclo seguente aggiungeremo più basi, fusione e/o distillazione consentita.
- Gary Baldi 0.0.1 è un nome futuro **solo dopo** una maturità misurata, non il nome della prima Chimera.

## Installazione Windows 11 ASUS

Prerequisiti: Git, Python 3.11 64 bit, driver NVIDIA, spazio disponibile e PyTorch CUDA compatibile. In PowerShell, dalla radice del repository:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m chimera_lab doctor
python -m chimera_lab validate-data
python -m unittest discover -s tests -v
```

## Installazione Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m chimera_lab doctor
python -m chimera_lab validate-data
python -m unittest discover -s tests -v
```

Per usare i pesi reali, installare PyTorch CUDA seguendo https://pytorch.org/get-started/locally/ e poi:

```bash
python -m pip install -e '.[train]'
```

Su PowerShell utilizzare le doppie virgolette: `python -m pip install -e ".[train]"`. L'installazione delle dipendenze e il download del modello possono consumare diversi GB. Nessun download di modello viene avviato dai test CI.

## Esperimento reale, in questo ordine

**1. Misurare la baseline**, prima di qualsiasi modifica:

```bash
python -m chimera_lab evaluate --model Qwen/Qwen3-4B-Instruct-2507 --eval-file data/eval_demo.jsonl --output runs/baseline.json --quantization 4bit --max-new-tokens 96
```

**2. Addestrare realmente un nuovo adapter 4-bit LoRA** (passi ridotti, verifica della pipeline, non promessa di miglioramento):

```bash
python -m chimera_lab train --model Qwen/Qwen3-4B-Instruct-2507 --train-file data/train_demo.jsonl --eval-file data/eval_demo.jsonl --output outputs/chimera1_adapter --steps 8 --max-length 256
```

**3. Testare i nuovi pesi e confrontare i rapporti:**

```bash
python -m chimera_lab evaluate --model outputs/chimera1_adapter --eval-file data/eval_demo.jsonl --output runs/chimera1.json --quantization 4bit --max-new-tokens 96
python -m chimera_lab compare --baseline runs/baseline.json --candidate runs/chimera1.json --output runs/comparison.json
```

Se la GPU esaurisce la memoria, registrare l'errore e usare **lo stesso workflow con modello 1.7B** per primo esperimento, misurando prima la sua baseline. Gli 8 GB dell'ASUS non garantiscono che il training 4B sia possibile. Se serve, eseguire il training su GPU Cloud ma verificare l'inferenza locale con hardware adeguato.

Il training salva `adapter_model.safetensors`, `adapter_config.json` e `chimera_manifest.json` **solo se l'addestramento riesce davvero**. Cartelle output e report locali sono escluse da Git. Le licenze delle basi devono essere rispettate.

## Interpretare i risultati correttamente

- Quattro esempi di training e quattro domande di test servono a collaudare la pipeline, non a migliorare l'intelligenza. Nessuna conclusione su superiorità o maturità può derivarne.
- Il punteggio exact-match è diagnostico, non rappresenta accuratezza generale. Occorreranno benchmark non contaminati su ragionamento, codice, matematica, lingue, creatività, affidabilità, latenza e consumo.
- Il confrontatore rifiuta dataset e impostazioni di decodifica differenti; non promuove automaticamente modelli.
- Non usare risposte di servizi Cloud come dati di addestramento se la relativa licenza o le condizioni del provider lo vietano.

## Genesis dopo Chimera

La futura applicazione Genesis Windows/Linux potrà riusare le parti che si dimostrano affidabili: controlli delle fonti e licenze, esperimenti, selezione Local/Cloud, dataset, benchmark, catalogo versioni, librerie condivise e rollback. Non verrà costruita prima di avere risultati con Chimera 1.

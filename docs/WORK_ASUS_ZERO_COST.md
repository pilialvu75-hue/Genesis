# Handoff a Work — ASUS / Chimera 1 / costo 0 €

**Data preparazione:** 10 novembre 2026. **Finestra prevista:** 11 novembre 2026, quando Work avrà accesso autorizzato all'ASUS.

## Obiettivo unico
Verificare sull'ASUS Windows 11 la possibilità di **eseguire e, se sostenibile, addestrare davvero Chimera 1**. Non progettare l'app Genesis, un laboratorio nuovo o una UI. I risultati devono essere misure reali, non simulazioni.

## Vincoli inderogabili
- **Budget servizi a pagamento: 0 €**. Non avviare GPU Cloud a consumo, endpoint commerciali, abbonamenti, crediti fatturabili o risorse che possano produrre addebiti. Chiedere esplicitamente approvazione in una fase futura se il percorso gratuito non è sufficiente.
- Usare **solo ASUS e strumenti gratuiti**; GitHub Actions CPU per controlli del codice. Nessuna promessa di training via GitHub Actions: le macchine Windows/Ubuntu standard non forniscono una GPU CUDA dedicata.
- Non installare tool sconosciuti, non eseguire comandi come amministratore, non cambiare BIOS, driver o impostazioni di sicurezza senza approvazione.
- **Niente chiavi API, password, dati personali o telemetria privata nel repository**.
- Fare attenzione a spazio sul disco (SSD 512 GB), 16 GB RAM, GPU RTX 4060 Laptop 8 GB VRAM, temperatura e alimentazione. Non saturare la GPU né lasciarla allenare per ore senza limiti e monitoraggio. Fermarsi con OOM, instabilità o temperature anomale.
- I download da Hugging Face sono gratuiti ma possono essere grandi. Prima di scaricare qualsiasi modello, verificare lo spazio libero e comunicare modello/dimensione stimata. Non scaricare 4B e 1.7B entrambi senza necessità.
- Le misure di un set dimostrativo di 4 domande **non provano** superiorità e non permettono la promozione a Gary Baldi.

## Scelta di Work e risparmio della quota inclusa

In Work Desktop con accesso locale autorizzato, per la **prima diagnosi hardware e raccolta dei log** usare un modello economico, preferibilmente **GPT-6 Luna** se disponibile, a velocità **Standard**. Per problemi tecnici complessi, provare **GPT-6.1 Sol** (o la versione Sol effettivamente disponibile); riservare **Astra** a blocchi particolarmente difficili, non per l'esecuzione ordinaria. **Codex** è più indicato di Work per modifiche di codice e repository.

Usare attività brevi, senza parallelizzare agenti superflui. Controllare **Impostazioni → Utilizzo** e fermarsi se si è vicini al limite; non acquistare crediti e non abilitare sovrapprezzi. La quota Work inclusa nel piano può comunque essere consumata, anche se non si compra nulla.

**Se Chimera 1 non può avanzare:** documentare il blocco; svolgere attività di preparazione **strettamente utili al modello**. Solo quando anche queste sono esaurite lavorare sul laboratorio riutilizzabile; Genesis soltanto come ultima opzione. Tornare subito al modello quando l'ASUS/CUDA diventa disponibile.

## Fase 1 — ispezione hardware, senza download e senza addestramento

Nel desktop Work con accesso all'ASUS:
1. Leggere versione Windows, RAM libera, disco libero, Python e driver NVIDIA.
2. In PowerShell (senza privilegi admin):
   ```powershell
   nvidia-smi
   py -3.11 --version
   Get-CimInstance Win32_OperatingSystem | Select-Object Caption,TotalVisibleMemorySize,FreePhysicalMemory
   Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID,FreeSpace,Size
   ```
   Se `py -3.11` non esiste, rilevare le versioni disponibili con `py -0p` e `python --version`. Non installare Python automaticamente senza valutare conflitti.
3. Controllare l'ambiente: `python -m pip --version`, `python -c "import torch; print(torch.__version__, torch.cuda.is_available())"` (solo se già installato), e versione `nvidia-smi`.
4. Riportare VRAM libera, RAM libera, spazio disco e temperatura GPU, se `nvidia-smi` le espone.

**Gate:** se CUDA non disponibile o la memoria è già impegnata, fermarsi. Nessun download o training a caso.

## Fase 2 — controlli del codice già pronto, gratuiti

Se Work dispone del repository in locale, aggiornare soltanto la copia di lavoro del progetto `pilialvu75-hue/Genesis` senza toccare AIVEXUS. Se non esiste, clonarlo in una cartella autorizzata.

In PowerShell dalla cartella Genesis:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m chimera_lab doctor
.\.venv\Scripts\python.exe -m chimera_lab validate-data
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
Questi comandi usano un ambiente isolato e **non scaricano modelli AI**. La creazione della venv e l'installazione di dipendenze Python possono richiedere l'accesso a PyPI; installare solo quando si è certi che il disco e le impostazioni locali lo permettano.

Registrare versioni, esiti e qualsiasi errore riproducibile.

## Fase 3 — prima inferenza e prova CUDA, solo se fattibile

- Scegliere **un solo modello** per il primo collaudo: `Qwen/Qwen3-4B-Instruct-2507` se la VRAM disponibile lo consente; altrimenti `Qwen/Qwen3-1.7B` (piano ridotto). I due modelli riportano licenza Apache 2.0 nel catalogo Hugging Face; verificare la card aggiornata.
- Verificare la versione di PyTorch CUDA, bitsandbytes, transformers e PEFT necessarie; fare installazioni nell'ambiente isolato senza acquisti, dopo conferma di spazio e traffico.
- Eseguire **baseline reale** su campione piccolo e registrare tempi di caricamento, token/s, memoria e temperatura. La sintassi prevista (da modificare solo secondo l'esito reale) è:
  ```powershell
  .\.venv\Scripts\python.exe -m chimera_lab evaluate --model Qwen/Qwen3-4B-Instruct-2507 --eval-file data/eval_demo.jsonl --output runs/asus_baseline.json --quantization 4bit
  ```
- Non confondere il programma `evaluate` con training. **Non affermare che Chimera 1 esiste** finché non sono presenti nuovi pesi addestrati e verificati.
- Non avviare subito l'addestramento da migliaia di step: dopo baseline, stimare memoria e rischio OOM con test molto breve e monitorato; se impossibile, proporre un'alternativa gratuita o rimandare senza addebiti.
- I dataset più ampi possono essere preparati successivamente tramite `python -m chimera_lab.prepare_sft`, ma **non scaricare l'intero corpus prima** di aver verificato CUDA, spazio, formato e qualità dei campioni.

## Fase 4 — riportare risultati realmente ottenuti

Aprire o aggiornare un commento nell'[issue #1](https://github.com/pilialvu75-hue/Genesis/issues/1) con:
- data, commit, ambiente e versione CUDA/PyTorch;
- RAM/VRAM libera, GPU, temperatura iniziale e finale, spazio libero;
- comandi realmente eseguiti, esiti **PASS / FAIL / NON ESEGUITO**, errori con stacktrace privati depurati;
- modello e dimensione scaricata (se scaricato);
- token/s, tempo di caricamento, eventuale OOM;
- nuovi file di pesi prodotti **solo se realmente prodotti**, senza caricare gigabyte nel repository;
- prossimo esperimento consigliato, senza fingere un miglioramento di capacità.

**Consegna attesa:** un report di fattibilità locale verificabile e, se tecnicamente possibile e autorizzato dai vincoli sopra, la prima inferenza reale. L'addestramento successivo ha priorità massima, ma nessuna spesa o rischio non approvato.

## Distinzione fra Work e ASUS

Work deve operare sul **computer ASUS realmente accessibile e autorizzato**. Non basta che usi un computer Cloud remoto: le misure di quel computer non descriverebbero la RTX 4060 locale. Se il collegamento al dispositivo non è disponibile, limitarsi a GitHub e dichiarare il blocco; non inventare risultati hardware.

**Ordine del progetto:** modello Chimera 1 → laboratorio completo → Genesis per Windows e Linux → eventuale Gary Baldi dopo risultati verificati.

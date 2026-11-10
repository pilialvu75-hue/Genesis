# Chimera 1 — addestramento reale CPU gratuito (prova tecnica)

**Importante:** questo esperimento è una prova di produzione di pesi, non Chimera 1 completa. Il modello principale da perfezionare resta un candidato 4B; la piccola base Qwen3-0.6B serve per produrre e ricaricare un adapter verificabile gratuitamente anche prima dell'accesso all'ASUS.

- Repo **pubblico**: runner GitHub Actions standard Ubuntu CPU gratuiti, senza GPU e senza acquisto di crediti.
- Fonte: Qwen/Qwen3-0.6B, modello open-weight con licenza Apache-2.0. Nessun dato di utenti, chiavi, credenziali o servizi a pagamento.
- 24 coppie domanda-risposta originali in italiano/francese/inglese in `data/chimera1_cpu_proof_train.jsonl`; non sono dati sufficienti per migliorare l'intelligenza generale.
- Training CPU LoRA di **12 piccoli step**; se riesce salva `adapter_model.safetensors`, `adapter_config.json`, tokenizer e `report.json`.
- Gate reale: la modifica dei pesi deve essere non nulla, il file pesi deve esistere e un nuovo caricamento PEFT deve generare le stesse risposte del modello appena addestrato.
- Output pubblicato soltanto come **artifact GitHub Actions**, non incorporato nel codice e **non** proposto come aggiornamento ufficiale AIVEXUS.
- Questo approccio **non garantisce** alcun miglioramento di capacità. Eventuali peggioramenti sono un risultato da registrare. Il vero passo successivo è un training più lungo e un confronto su 4B, con ASUS o altre risorse gratuite e dati di qualità.

Per testare su AIVEXUS in futuro: usare una build separata per il collaudo e verificare supporto formato GGUF, licenze, memoria e conversione, **senza sostituire modelli o interrompere la beta attuale**.

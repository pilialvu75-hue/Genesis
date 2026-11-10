# Chimera 1 — Prova di conversione LoRA → GGUF (costo 0 €)

**Questa non è Chimera 1 finita**. Un prototipo LoRA basato su Qwen3-0.6B è stato realmente addestrato su GitHub ([run #42866886858](https://github.com/pilialvu75-hue/Genesis/actions/runs/42866886858)), con SHA256 adapter `510a75e163f4c5e76d2987f596fa5020da23ce81a93e352a3bc1b3aa53b6d64c`.

Questo workflow GitHub Actions su **CPU standard gratuita di repository pubblico** verifica i passaggi fondamentali per provare il prototipo su AIVEXUS:

1. Scarica l'artefatto LoRA **esatto** già addestrato e verifica SHA256 e modello base.
2. Carica il modello `Qwen/Qwen3-0.6B` (Apache 2.0) e fonde realmente l'adapter.
3. Converte il modello unificato in GGUF F16 con `llama.cpp` bloccato al commit `582eab718608b99792286729890aac1675547c29`.
4. Quantizza in GGUF Q4_K_M con `llama-quantize`.
5. Esegue **inferenza vera** con `llama-cli` CPU e registra l'output.
6. Pubblica file GGUF, SHA256 e log come artifact GitHub Actions di durata 30 giorni **solo se tutti i controlli sono PASS**.

**Limitazioni:** nessun benchmark serio né confronto di qualità con la baseline; non provato su hardware ASUS/Galaxy, né verificata la compatibilità del `llama.cpp` integrato nella beta AIVEXUS. Prima di utilizzare in AIVEXUS: test separato e reversibile tramite importazione del file GGUF, senza sostituire modelli installati o pubblicare automaticamente APK.

**Finanziamento:** 0 € di servizi nuovi, niente GPU Cloud a pagamento. I soli costi sono quote GitHub Actions standard per il repository pubblico, secondo il piano di GitHub.

**Attenzione:** il primo file GGUF è piccolo e utile a testare il processo, ma non riflette l'ambizione di Chimera 1 generalista di alta qualità. Il vero modello resta la priorità e richiede dati, addestramento e valutazioni più estesi.

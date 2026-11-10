# Roadmap Genesis — apprendere dalla costruzione di Gary Baldi

## Decisione del 10 novembre 2026

**Prima si costruisce e collauda Gary Baldi (Chimera 1) direttamente; solo dopo si implementa Genesis sulla base di ciò che funziona davvero.** Non creare un'app Genesis, una UI o un orchestratore completo come prerequisito di Gary Baldi.

**Nome definitivo del modello:** **Gary Baldi**, in omaggio a Giuseppe Garibaldi. Il nome esprime una soglia ambiziosa: intelligenza generalista, capacità di trovare soluzioni creative e strategie efficaci in problemi nuovi, non soltanto prestazioni in un benchmark ristretto. La superiorità va **dimostrata**, non dichiarata.

## Gary Baldi — primo modello reale

### 1. Obiettivo

Costruire il modello generalista più capace possibile entro le risorse disponibili **ad ogni ciclo**, puntando a:
- ragionamento multi-passo, matematica e problem solving;
- programmazione, debugging, comprensione di codice;
- competenza multilingue (almeno italiano, francese, inglese);
- comprensione e sintesi di conoscenze, affidabilità fattuale;
- pianificazione, uso corretto di strumenti e adattamento a problemi nuovi;
- creatività e «astuzia» misurate attraverso problemi non familiari, senza scorciatoie o fuga dei dati di test.

**Un solo modello principale con pesi reali**, utilizzabile senza dover interpellare i modelli sorgente. Librerie e strumenti esterni sono opzionali e condivisibili, non sostituti delle capacità interne. Una federazione di modelli può aiutare a **crearlo**, ma non va confusa con il modello finale.

### 2. Costruzione ibrida: una parte da zero e una da basi esistenti

- **Basi esistenti:** identificare pochi modelli open-weight eccellenti e compatibili, verificarne architetture, tokenizer, licenze e condizioni di utilizzo.
- **Componenti originali:** creare e addestrare **nuovi pesi** inizializzati da zero (ad esempio adattatori o nuovi moduli realmente addestrabili), nuove ricette di training, dataset di allenamento autorizzati, valutazioni, ottimizzazioni e strategie di integrazione.
- **Integrazione:** fusione di pesi solo fra strutture compatibili; altrimenti apprendimento tramite distillazione o fine-tuning e consolidamento in un modello distribuibile dove possibile.
- **Cloud/Local:** modelli Cloud grandi, preferibilmente >500B, per guida, progettazione e revisione **quando la licenza/ToS consente l'uso previsto**; modelli Local per esecuzione e sperimentazione. Il cloud può essere predominante all'inizio.
- **Sperimentazione iniziale:** ASUS VivoBook (i7-12700H, RTX 4060 Laptop 8 GB VRAM, 16 GB RAM) come banco prova. Non rappresenta un tetto futuro; conservare la possibilità di versioni più grandi per hardware/Cloud più potente.

Questa è una costruzione ibrida originale **basata su pesi preaddestrati e parti nuove**; non è la pretesa di addestrare un foundation model interamente da zero. Quello sarà un percorso futuro distinto: **Genesis Origin**.

### 3. Evidenze richieste per dire «Gary Baldi 1 esiste»

1. Pesi/adattatori nuovi, caricabili, con hash e versioni; configurazione, provenienza e licenze tracciate.
2. Inferenza riuscita **reale** sull'ASUS, non risposte simulate, con RAM, VRAM, latenza, token/s e stabilità misurati.
3. Benchmark confrontabili eseguiti su baseline, Gary Baldi e, ove applicabile, candidati alternativi: ragionamento, coding, matematica, linguaggio, affidabilità, generalizzazione e creatività/strategia. Set di valutazione separati dai dati d'addestramento.
4. Report riproducibile con errori e regressioni, non solo esempi selezionati.
5. Promozione del modello per un ruolo soltanto se migliora significativamente i criteri di valore definiti per quel ruolo senza regressioni critiche; rollback sempre possibile.

Il primo esperimento può fallire o risultare meno capace del modello di partenza. Va reso pubblico come risultato tecnico, poi corretto. Non promettere di battere tutte le IA esistenti con le risorse attuali.

### 4. Approccio minimo per risparmiare tempo

- Scegliere baseline e prove prima dell'addestramento.
- Fare un primo esperimento breve, con pochi modelli e almeno un componente originale addestrabile.
- Convalidare pesi, misure e miglioramenti, poi ripetere o allargare. Non costruire prima UI, sistemi di plugin complessi o infrastrutture non necessarie.
- Portare in Genesis solo tecniche dimostrate utili: ricerca e selezione modelli, registro licenze, training, gestione risorse, benchmark, versioning, promozione e ripristino.

## Genesis — dopo le lezioni di Gary Baldi

Genesis sarà il sistema capace di **ripetere e migliorare autonomamente** il procedimento usato per creare Gary Baldi. Architettura obiettivo:
- **Core di orchestrazione** Local/Cloud con scelta basata su qualità, velocità, costi e risorse reali; possibilità di riusare componenti maturi AIVEXUS.
- **Chimera Lab** per modelli open-weight, fusioni compatibili, distillazione e training.
- **Librerie indipendenti e condivise**, consultabili contemporaneamente da più modelli tramite API/permessi, per moduli, conoscenze/RAG, dataset e cataloghi pesi.
- **Valutazione autonoma** con confronti indipendenti, report e rollback.
- **Windows e Linux**, un core condiviso con adattatori piattaforma.
- **Origin**, futura esplorazione e addestramento di modelli anche completamente da zero.

**Governance risorse:** nessun tetto arbitrario al miglioramento; per ogni ciclo limiti espliciti a costi Cloud, durata, spazio, RAM/VRAM/CPU/GPU, energia e permessi.

**Priorità concorrenti:** questo progetto non deve compromettere le attività P0 di AIVEXUS, Libreria e Ricercatore verso moduli realmente autonomi.

## Stato

- [x] Visione di Gary Baldi e distinzione dal futuro Genesis documentate.
- [ ] Baseline e modelli sorgente selezionati e provati.
- [ ] Primo addestramento/fusione ibrida eseguito.
- [ ] Pesi reali di Gary Baldi prodotti e testati.
- [ ] Prestazioni e superiorità rispetto alla baseline documentate.
- [ ] Lezioni convertite in requisiti e codice per Genesis Windows/Linux.

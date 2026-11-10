# Roadmap Genesis — da Chimera sperimentale a Gary Baldi

## Decisione del 10 novembre 2026

**Prima si costruiscono e collaudano Chimera 1, Chimera 2, Chimera 3… come modelli sperimentali; solo dopo si implementa Genesis sulla base di ciò che funziona davvero.** Non creare l'app Genesis come prerequisito delle Chimere.

**Regola dei nomi (confermata dall'utente):** fino alla maturità desiderata si utilizza **Chimera 1 → Chimera 2 → Chimera 3 → …**. Solo quando una Chimera dimostra capacità generaliste, ingegnosità, ragionamento e affidabilità al livello concordato, ottiene il nome d'onore **Gary Baldi**, in omaggio a Giuseppe Garibaldi, iniziando da **Gary Baldi 0.0.1 → 0.0.2 → 0.0.3…**. Il numero non determina da solo la promozione; nessuna data o soglia di generazione è imposta anticipatamente. La superiorità deve essere dimostrata con prove indipendenti.

## Chimera 1, 2, 3… — modelli sperimentali reali

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

### 3. Evidenze richieste per dire «Chimera 1 esiste»

1. Pesi/adattatori nuovi, caricabili, con hash e versioni; configurazione, provenienza e licenze tracciate.
2. Inferenza riuscita **reale** sull'ASUS, non risposte simulate, con RAM, VRAM, latenza, token/s e stabilità misurati.
3. Benchmark confrontabili eseguiti su baseline, Chimera e, ove applicabile, candidati alternativi: ragionamento, coding, matematica, linguaggio, affidabilità, generalizzazione e creatività/strategia. Set di valutazione separati dai dati d'addestramento.
4. Report riproducibile con errori e regressioni, non solo esempi selezionati.
5. Promozione del modello per un ruolo soltanto se migliora significativamente i criteri di valore definiti per quel ruolo senza regressioni critiche; rollback sempre possibile.

Il primo esperimento può fallire o risultare meno capace del modello di partenza. Va reso pubblico come risultato tecnico, poi corretto. Non promettere di battere tutte le IA esistenti con le risorse attuali.

### 4. Approccio minimo per risparmiare tempo

- Scegliere baseline e prove prima dell'addestramento.
- Fare un primo esperimento breve, con pochi modelli e almeno un componente originale addestrabile.
- Convalidare pesi, misure e miglioramenti, poi ripetere o allargare. Non costruire prima UI, sistemi di plugin complessi o infrastrutture non necessarie.
- Portare in Genesis solo tecniche dimostrate utili: ricerca e selezione modelli, registro licenze, training, gestione risorse, benchmark, versioning, promozione e ripristino.

## Quando nasce Gary Baldi

Il passaggio dal nome sperimentale **Chimera N** a **Gary Baldi 0.0.1** è una decisione di promozione basata su test e non sul conteggio delle generazioni. Le release successive seguono **0.0.2, 0.0.3, …**, mantenendo lo storico Chimera e la possibilità di rollback. Una Gary Baldi iniziale può ancora essere migliorata: il nome non significa sviluppo terminato.

## Genesis — dalle lezioni di Chimera e Gary Baldi

Genesis sarà il sistema capace di **ripetere e migliorare autonomamente** il procedimento usato per creare le Chimere e, in seguito, Gary Baldi. Architettura obiettivo:
- **Core di orchestrazione** Local/Cloud con scelta basata su qualità, velocità, costi e risorse reali; possibilità di riusare componenti maturi AIVEXUS.
- **Chimera Lab** per modelli open-weight, fusioni compatibili, distillazione e training.
- **Librerie indipendenti e condivise**, consultabili contemporaneamente da più modelli tramite API/permessi, per moduli, conoscenze/RAG, dataset e cataloghi pesi.
- **Valutazione autonoma** con confronti indipendenti, report e rollback.
- **Windows e Linux**, un core condiviso con adattatori piattaforma.
- **Origin**, futura esplorazione e addestramento di modelli anche completamente da zero.

**Governance risorse:** nessun tetto arbitrario al miglioramento; per ogni ciclo limiti espliciti a costi Cloud, durata, spazio, RAM/VRAM/CPU/GPU, energia e permessi.

**Priorità concorrenti:** questo progetto non deve compromettere le attività P0 di AIVEXUS, Libreria e Ricercatore verso moduli realmente autonomi.

## Stato

- [x] Visione Chimera → Gary Baldi e distinzione dal futuro Genesis documentate.
- [ ] Baseline e modelli sorgente selezionati e provati.
- [ ] Primo addestramento/fusione ibrida eseguito.
- [ ] Pesi reali di Chimera 1 prodotti e testati.
- [ ] Criteri di maturità verificati prima della denominazione Gary Baldi 0.0.1.
- [ ] Prestazioni e superiorità rispetto alla baseline documentate.
- [ ] Lezioni convertite in requisiti e codice per Genesis Windows/Linux.

# Roadmap Genesis — da Chimera sperimentale a Gary Baldi

## Decisione del 10 novembre 2026

**Prima si costruiscono e collaudano Chimera 1, Chimera 2, Chimera 3… come modelli sperimentali; solo dopo si implementa Genesis sulla base di ciò che funziona davvero.** Non creare l'app Genesis come prerequisito delle Chimere.

**Regola dei nomi (confermata dall'utente):** fino alla maturità desiderata si utilizza **Chimera 1 → Chimera 2 → Chimera 3 → …**. Solo quando una Chimera dimostra capacità generaliste, ingegnosità, ragionamento e affidabilità al livello concordato, ottiene il nome d'onore **Gary Baldi**, in omaggio a Giuseppe Garibaldi, iniziando da **Gary Baldi 0.0.1 → 0.0.2 → 0.0.3…**. Il numero non determina da solo la promozione; nessuna data o soglia di generazione è imposta anticipatamente. La superiorità deve essere dimostrata con prove indipendenti.

## Ordine di sviluppo vincolante — chiarimento 10/11/2026

**1. MODELLO PRIMA.** Prima ottenere **Chimera 1 con pesi/adattatori realmente addestrati, inferenza verificata e primi confronti con la base**. Sono ammessi solo gli script e i controlli minimi necessari a produrre e testare il modello. La PR #2 contiene già una struttura di laboratorio minimale, **ma non è il risultato richiesto** e non autorizza a spostare l'attenzione su un laboratorio completo.

**2. LABORATORIO DOPO.** Soltanto dopo un primo risultato reale progettare un laboratorio strutturato, riproducendo gli esperimenti efficaci, con gestione dati, benchmark, tracciabilità e controllo delle risorse.

**3. GENESIS INFINE.** Una volta provato il procedimento, costruire il software autonomo Genesis per Windows e Linux, sfruttando esperienza e componenti validati.

## Regola di avanzamento quando il modello è bloccato — 10/11/2026

**Priorità sempre: MODELLO > LABORATORIO > GENESIS.**

1. **MODELLO — massimo sforzo.** Tutto ciò che produce o migliora i pesi reali Chimera 1, i dati efficaci, l'inferenza e i benchmark pertinenti ha precedenza. Provare alternative gratuite (ASUS/CPU quando sensato, piccole prove, software compatibile) prima di dichiarare il blocco.
2. **LABORATORIO — solo se il modello è realmente bloccato** da indisponibilità di GPU, accesso locale, dati o autorizzazioni. Lavorare su un pezzo strettamente riutilizzabile per lo stesso modello (ripresa checkpoint, misurazione, qualità dati, compatibilità): niente UI, dashboard o infrastrutture decorative.
3. **GENESIS — ultima alternativa** se non ci sono attività modello/laboratorio utili eseguibili senza nuove risorse. Limitarsi a specifiche e componenti riutilizzabili dalla futura versione Windows/Linux, con avanzamento concreto e tracciato; non cominciare a costruire l'app completa.
4. **RITORNO IMMEDIATO AL MODELLO** appena cade il blocco. Report ogni volta: attività svolta, risultato verificato, ragione del blocco e prossimo test sul modello.

**Vincolo economico:** 0 € di nuove spese; nessun lavoro GPU Cloud a pagamento, acquisto di crediti o upgrade senza esplicita nuova autorizzazione. La quota Work inclusa nel piano va conservata scegliendo compiti piccoli e modelli efficienti: Work Desktop locale per usare l'ASUS, Codex per codice, un modello economico per diagnostica e uno più capace solo per problemi realmente difficili. Non affermare accesso all'ASUS quando Work opera soltanto sul suo computer Cloud.

**Obiettivo futuro Computer Use AIVEXUS:** l'ASUS potrà ospitare un agente locale sotto autorizzazione esplicita, con privilegi minimi, esecuzione tracciata, timeout, limiti a RAM/VRAM/temperature e stop manuale. AIVEXUS potrà coordinare test e addestramento in autonomia controllata, così da ridurre il consumo di Work. Finché Computer Use non è implementato e testato, questa resta una capacità futura e non va presentata come disponibile.

## Principio di addestramento: qualità prima della velocità (10/11/2026)

**Decisione vincolante:** scegliere metodi e dati che producano le **migliori capacità generaliste dimostrabili** per le risorse effettivamente disponibili, anche se richiedono più tempo. La rapidità serve per ottenere feedback, **non** è un criterio superiore alla qualità. La prima Chimera può nascere da un esperimento piccolo, ma non va proclamata riuscita perché sono stati eseguiti pochi step LoRA.

- **Dati prima di tutto:** provenienza e licenze verificabili, qualità e varietà elevate (ragionamento, codice, matematica, lingue, conoscenza, uso di strumenti); filtraggio, deduplicazione, controllo di errori e distribuzione delle difficoltà.
- **Tecniche selezionate per evidenza, non per moda:** baseline e ablation test tra fine-tuning completo se sostenibile, LoRA/QLoRA, distillazione autorizzata, fusione architetturalmente compatibile, supervised fine-tuning (SFT) e successive ottimizzazioni di preferenze o reinforcement learning con ricompense verificabili, **solo quando appropriate**. Nessuna tecnica è universalmente migliore.
- **Insegnanti forti Local/Cloud:** sfruttare modelli esterni per generare o verificare dati soltanto dove licenze e termini lo permettono; combinare più fonti e verifiche indipendenti per limitare gli errori insegnati.
- **Training serio:** split di test non contaminati, curriculum e mistura dei dati motivati, monitoraggio loss/overfitting, checkpoint, seed e parametri tracciati; possibilità di interrompere o riprendere senza perdere lavoro.
- **Confronti su problemi nuovi:** benchmark e prove pratiche ripetibili su ragionamento, matematica, coding, multilingua, creatività e robustezza, oltre a latency/VRAM/RAM/costo. Verificare anche regressioni e generalizzazione. Nessuna promozione da microbenchmark.
- **Scelta secondo vincoli reali:** se l'ASUS non basta per l'addestramento migliore, usare risorse Cloud/GPU più capaci nei limiti del budget; prevedere una variante d'inferenza efficiente per l'ASUS, senza imporre la dimensione dell'ASUS ai modelli futuri.
- **Conferma per generazione:** conservare baseline, pesi e report delle candidate; promuovere solo miglioramenti reali, accettando un esperimento più lungo o una generazione scartata quando necessario.

**Ordine immutato:** prima pesi Chimera reali, poi laboratorio strutturato, infine Genesis Windows/Linux.

### Apprendimento dai video — possibilità futura, non blocco per Chimera 1

- **Prima modalità (text-only):** ricavare da filmati autorizzati trascrizioni e descrizioni accurate, trasformandole in esempi di addestramento. Il modello impara dai **testi**, non vede il video né comprende il movimento direttamente.
- **Modalità visiva:** integrare encoder visivo e addestramento multimodale con fotogrammi, audio, timestamp, didascalie e domande/risposte per legare sequenze visive e significato.
- **Modalità temporale avanzata:** per azioni, causalità e dinamiche, valutare un'architettura video-aware con campionamento temporale e dati etichettati, confrontandola con semplici modelli visione-linguaggio.
- **Verifiche:** misurare se migliora davvero la comprensione e generalizzazione su filmati nuovi; non confondere il recupero di didascalie con l'apprendimento visivo.
- **Vincoli:** fonti utilizzabili legalmente, licenze e termini di piattaforma, diritti d'autore, consenso e privacy dei soggetti ripresi, costi e memoria GPU. L'ASUS con 8 GB VRAM può iniziare con elaborazione preliminare/esperimenti leggeri; training video su larga scala richiederà probabilmente Cloud/GPU più potenti.

**Scelta operativa:** non introdurre adesso la pipeline video se ritarda l'ottenimento di Chimera 1; registrarla fra le opportunità per le generazioni successive.

## Decisione del 12 novembre 2026 — pacchetti incrementali di intelligenza pratica

**Visione del proprietario:** a ogni generazione recuperare pacchetti di esperienze e capacità verificabili, inizialmente piccoli e poi anche più grandi, per costruire progressivamente Chimera e arrivare, **solo a maturità dimostrata**, a Gary Baldi. Priorità al **saper fare** (ragionamento, pianificazione, uso di strumenti, strategie, auto-correzione, generalizzazione), non all'accumulo indiscriminato di cultura nozionistica: conoscenza aggiornata e RAG possono restare esterni, con accesso verificabile quando necessario.

**Il "pacchetto" non è sempre un file di pesi sommabile ad altri.** Distinguere esplicitamente:
1. **Esperienze e dataset**: dimostrazioni, traiettorie osservazione→azione→risultato, scenari di successo/fallimento, preferenze di esecuzione e metadati di qualità/licenza. Possono crescere, essere selezionati e convertiti, ma non migliorano i pesi senza apprendimento.
2. **Competenze procedurali e strumenti**: procedure verificate, programmi e moduli operativi condivisibili fra modelli. Rendono l'agente più capace come sistema senza far credere che il modello abbia acquisito quella capacità internamente.
3. **Competenze apprese nei pesi**: LoRA/QLoRA, fine-tuning, distillazione da insegnanti autorizzati, RL con feedback verificabile, ed eventualmente merging **solo** di modelli/adapter compatibili. Ogni candidata deve avere benchmark e rollback.
4. **Prove indipendenti**: suite di attività nuove, separata da training e retrieval, che misuri capacità reali e trasferimento a compiti non visti. La dimensione del pacchetto non equivale a intelligenza.

### Curriculum cumulativo proposto, da adattare all'evidenza

- **A. Fondamenta operative:** ragionamento multi-step, puzzle, logica, pianificazione, revisione e correzione autonoma su scenari verificabili.
- **B. Computer Use Windows:** lettura dello schermo e delle UI, mouse/tastiera, 2048 e Car Jam su WEmulDroid; ogni decisione deve essere del vero modello e ogni esito verificato indipendentemente.
- **C. Tool use/autonomia:** browser, file, editor, coding, debugging, test e recupero errori, con strumenti autorizzati e senza sequenze rigidamente predefinite.
- **D. Trasferimento generalista:** affrontare software, giochi e problemi nuovi, concatenare abilità, progettare piani alternativi, verificare e generalizzare. Comprensione multilingue necessaria come interfaccia, non priorità nozionistica.
- **E. Ulteriori cicli:** acquisire pacchetti più grandi e più difficili **solo quando** il precedente ha aumentato risultati riproducibili e non introduce regressioni rilevanti. Il numero di livelli non è prefissato.

### Ciclo di incorporazione

`scoperta → controllo licenza/provenienza → filtraggio/dedup → formato condiviso → baseline → addestramento o retrieval → prova held-out → regressioni/forgetting → promozione o scarto → checkpoint`

- Mantenere un **registro capacità** per generazione: compito, metrica, baseline, fonte, modello insegnante quando lecito, versione, hardware, risultati nuovi, abilità perdute, archiviazione e rollback.
- Contrastare il **catastrophic forgetting** con replay selezionato di abilità precedenti, curriculum bilanciato, distillazione/regularizzazione quando utili e prove su compiti vecchi e nuovi. Non dichiarare acquisita una capacità se peggiorano significativamente quelle già possedute.
- Per la visione di prodotto di **un unico modello principale con pesi reali**, le librerie e gli specialisti sono ausili di training/esecuzione; il trasferimento nella Chimera candidata richiede training e convalida. Evitare di spacciare un insieme di modelli instradati per un singolo modello superiore.
- Raccogliere esperienze AIVEXUS tramite un contratto di esportazione **esplicito**, dati sintetici/di test o consenso appropriato, senza trasferimento automatico di screenshot, chat, account o altre informazioni personali.
- Iniziare con campioni e capacità realistiche sull'ASUS (RTX 4060 8 GB) e budget 0 €; i pacchetti possono diventare più grandi in futuro e il limite hardware attuale non è definitivo. Controllare sempre termini di modelli, pesi e dataset prima della distribuzione.
- **Ordine preesistente immutato:** ottenere prima Chimera 1 reale, poi laboratorio strutturato, poi applicazione Genesis. I nuovi pacchetti non sono un motivo per rinviare la prima verifica dei pesi.

**Tracciamento:** [Genesis #12 — dataset ed esperienze esterne](https://github.com/pilialvu75-hue/Genesis/issues/12), [Chimera 1 #1](https://github.com/pilialvu75-hue/Genesis/issues/1), [AIVEXUS Computer Use #1115](https://github.com/pilialvu75-hue/Ai-orchestrator-riserva/issues/1115).

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

## Gary Baldi pubblico — chat gratuita e laboratorio di capacità reali (fase successiva)

**Decisione 10 novembre 2026:** una volta che un modello Chimera avrà superato i criteri e ottenuto il nome **Gary Baldi 0.0.1**, predisporre un **sito Web con chat pubblica gratuita**. Non avviare lo sviluppo del sito come prerequisito di Chimera 1.

**Visione:** un «piccolo ChatGPT» generalista, proporzionato alle risorse disponibili, che le persone possano usare gratuitamente per compiti reali. Il sito ha **due funzioni inseparabili**: servizio utile agli utenti e laboratorio di valutazione sul campo. La chat non deve essere presentata come equivalente a ChatGPT in funzioni o qualità prima di averne dimostrato le capacità.

### Capacità da valutare e ampliare

- Conversazione naturale, ragionamento, creatività, capacità strategica e adattamento alle richieste nuove.
- Codice, matematica, spiegazioni, documenti e lingue (italiano/francese/inglese e progressivamente altre).
- Quando tecnicamente disponibili e realmente collaudati: navigazione/ricerca, strumenti, documenti, immagini, audio e altre funzioni multimodali.
- Un **modello principale Gary Baldi** con librerie esterne separate e condivise; distinguere nella telemetria le capacità proprie del modello da quelle fornite dagli strumenti, dalle librerie e da eventuali servizi Cloud.

### Laboratorio pubblico, verifiche e rispetto delle persone

- Misurare in forma aggregata: qualità delle risposte (feedback volontario e valutazioni indipendenti), errori, allucinazioni, latenze, disponibilità, token/s, costo per richiesta, RAM/VRAM, saturazione e stabilità.
- Usare benchmark **non pubblicati nei dataset di addestramento**, test di regressione e prove reali per identificare lacune e priorità.
- Offrire feedback volontario e segnalazione di problemi. **Non usare automaticamente le chat personali per addestramento**: informativa chiara, consenso separato se necessario, minimizzazione, retention e cancellazione, protezione dei dati personali, verifica GDPR e obblighi pertinenti prima dell'apertura pubblica.
- Difese operative: limiti d'uso per contenere costi e abusi, moderazione proporzionata, protezione da prompt injection e richieste pericolose, isolamento degli strumenti, backup/rollback. Nessuna promessa di servizio illimitato: **gratuito per gli utenti non significa calcolo gratuito**.
- Accesso aperto progressivo (prima piccolo gruppo e collaudo di carico, poi chat pubblica), senza imporre all'utente di pagare per il normale uso previsto.
- Pubblicare in modo trasparente capacità, limiti e progressi; non equiparare numero di utenti o valutazioni positive a superiorità scientificamente dimostrata.

**Dopo il periodo di test pubblico:** valutare con dati reali se proseguire come servizio aperto, rilasciare i pesi, sviluppare altre versioni o scegliere una strategia diversa. **Decisione rimandata**, senza assumere ora licenze di rilascio dei pesi o modello commerciale.

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
- [ ] Dopo la promozione a Gary Baldi: predisporre chat pubblica gratuita e laboratorio con privacy, costi, valutazioni e protezioni validate.

# Genesis — Chimera / Origin

> **Decisione di progetto:** sviluppare prima i prototipi sperimentali **Chimera 1, Chimera 2, Chimera 3…**, combinando basi open-weight e componenti nuovi addestrati da zero. Il nome d'onore **Gary Baldi** sarà assegnato **solo dopo** aver raggiunto e dimostrato il livello generalista desiderato. La prima release si chiamerà **Gary Baldi 0.0.1**, poi **0.0.2, 0.0.3…**. Non costruire prima l'app Genesis: nascerà dalle lezioni di Chimera. [Roadmap completa](docs/ROADMAP_GARY_BALDI_GENESIS.md).

Genesis è un progetto indipendente per **creare, valutare e migliorare modelli di intelligenza artificiale**. Riusa, quando utile, componenti collaudati di [AIVEXUS](https://github.com/pilialvu75-hue/Ai-orchestrator-riserva) senza dipenderne dall'interfaccia o modificare il suo sviluppo prioritario.

## Obiettivo immediato: Chimera 1 reale

**Dati concreti per il primo addestramento:** [Aya + OASST1 + GSM8K + MetaMathQA e procedimento](docs/CHIMERA1_TRAINING_DATA.md). Lo script di preparazione usa dataset pubblici solo quando viene eseguito. Nessun nuovo peso addestrato è ancora disponibile.



**Laboratorio implementato in PR:** [protocollo Chimera 1](docs/CHIMERA1_LAB.md) — CLI Python senza UI Genesis, validazione dati, benchmark e primo esperimento QLoRA; i test software non equivalgono ad addestramento riuscito.



Produrre nel minor tempo possibile **un modello open-weight modificato/addestrato con pesi eseguibili propri**, verificando con benchmark riproducibili se migliora rispetto alla base. Un semplice orchestratore che interroga più modelli **non** equivale a una Chimera riuscita.

- **Inizio ibrido:** modelli Local + Cloud possono assistere progettazione, coding e ricerca; i modelli Cloud >500B sono una preferenza iniziale, non un requisito che prevale sulla qualità misurata.
- **Base open-weight:** selezionare modelli utilizzabili legalmente; fusione dei pesi solo quando compatibile, altrimenti distillazione, LoRA/QLoRA, fine-tuning o altre tecniche verificabili. Rispettare licenze e termini di utilizzo dei modelli insegnanti.
- **ASUS come primo laboratorio:** Intel i7-12700H, RTX 4060 Laptop 8 GB VRAM, 16 GB RAM. I primi esperimenti devono poter essere collaudati su questa macchina; non è un tetto permanente alla capacità dei futuri modelli.
- **Sostituzione meritocratica:** una Chimera sostituisce il modello di un ruolo solo dopo test indipendenti di qualità, latenza, affidabilità e costi/risorse; mantenere il rollback.
- **Evoluzione aperta:** nessun limite artificiale al miglioramento; limiti configurabili sulle risorse per singolo ciclo.
- **Genesis Origin:** sviluppo successivo di modelli/architetture da zero; non escluso e non confuso con il primo MVP.

## Architettura prevista

- **Genesis Core:** orchestratore ed esecuzione dei cicli (scelta Local/Cloud, checkpoint, budget, esperimenti).
- **Chimera Lab:** selezione delle basi, addestramento/fusione/distillazione, valutazione, versioni e promozione.
- **Shared Library:** conoscenze/RAG, moduli, dataset e catalogo dei modelli, accessibili anche da più modelli tramite interfacce e permessi controllati.
- **Interfacce Windows e Linux:** stesso core e stessi formati dei dati; adapter per sistemi operativi differenti.

Le librerie esterne accrescono le conoscenze consultabili, **non sostituiscono** l'addestramento necessario a migliorare le capacità interne di Chimera.

## Primo criterio di successo

1. Definire una baseline open-weight, il suo ambiente e benchmark riproducibili.
2. Realizzare un esperimento che produca **pesi modificati reali** e un manifesto con provenienza, licenza e parametri.
3. Eseguire **baseline e Chimera candidata** sugli stessi test, registrando qualità, velocità, RAM/VRAM e stabilità.
4. Pubblicare risultati e artefatti verificabili, senza proclamare superiore un modello che non supera i test.

**Stato attuale:** roadmap dei prototipi Chimera documentata; nessun modello Chimera 1 è stato ancora addestrato e validato. **Gary Baldi è un nome riservato al traguardo**, non il nome della prima Chimera. Genesis è previsto dopo i primi collaudi, non come prerequisito.

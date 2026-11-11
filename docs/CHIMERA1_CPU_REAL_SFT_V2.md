# Chimera — CPU LoRA v2 con dati reali, senza costi aggiuntivi

Priorità: **modello**. La prima prova 0.6B di Chimera aveva 12 passaggi su 24 esempi originali e non basta a dimostrare intelligenza. Questo secondo esperimento è ancora un **prototipo 0.6B**, ma usa dati pubblici reali provenienti da Aya, OASST1, GSM8K e MetaMathQA, già verificati nel gate GitHub Actions #42972287236 (545 esempi validi/50 held-out nel campionamento ridotto).

Il workflow su **GitHub Actions runner standard CPU del repository pubblico**, budget aggiuntivo 0 €:
- scarica soltanto dataset e modello Qwen3-0.6B Apache-2.0;
- applica filtraggio di lunghezza, bilanciamento per fonte e lingua e LoRA rango 8;
- esegue 240 step con seed fisso, grad clipping e programma LR warmup+cosine;
- salva un vero PEFT LoRA adapter + SHA256, e ricarica il modello da disco;
- compara in condizioni uguali Qwen base e candidato su 6 domande aritmetiche non presenti nel training, segnalando regressioni;
- conserva soltanto l'adapter e il report nella run, non redistribuisce i dataset di terzi.

**Limiti:** resta 0.6B, 240 step ancora pochi rispetto a un addestramento importante, il confronto di 6 domande non misura generalità e i dati di benchmark pubblici possono essere presenti nel pretraining originale. Non distribuire in AIVEXUS come sostituzione della beta. La scelta della vera Chimera 1 resta valutare una base maggiore e train con CUDA sull'ASUS o su risorse gratuite sostenibili, con test indipendenti ampi.

**Rendimento prima della velocità:** questo esperimento privilegia la tracciabilità e la qualità dei dati, non è un requisito che il candidato batta il baseline. Se non migliora, non verrà promosso.

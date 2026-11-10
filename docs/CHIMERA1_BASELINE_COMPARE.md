# Chimera 1 — confronto reale con Qwen originale (0 €)

Obiettivo: sapere **se il primo prototipo addestrato è migliorato, peggiorato o rimasto equivalente**. È scorretto giudicare l'intelligenza soltanto dal successo di una conversione GGUF.

Il workflow GitHub Actions esegue su runner CPU gratuito: Qwen3-0.6B originale e Chimera-pilot (Qwen3-0.6B + LoRA reale), convertiti entrambi in GGUF Q4_K_M con la stessa versione di llama.cpp, e confrontati su **12 domande non usate nei 24 esempi di training**: 9 operazioni aritmetiche in IT/FR/EN e tre domande aperte da rivedere manualmente. Il rapporto JSON contiene tutte le risposte, tempi, hash dei file e score aritmetico semplice.

**Limiti importanti:** 12 domande non rappresentano un benchmark serio; nessuna misura della qualità generale, nessuna contaminazione di pretraining esclusa, tre risposte richiedono review umana; l'euristica di estrazione del numero può sbagliare. L'esito non conferisce a Chimera 1 uno stato di prontezza.

Durante il collaudo con AIVEXUS ASUS: non modificare i modelli preinstallati, testare con una nuova conversazione LOCAL manuale e raccogliere latenza/RAM/risposte/Diagnostics. I risultati ASUS restano distinti dai runner di GitHub.

Nessun addebito Cloud, budget aggiuntivo 0 €. Priorità modello Chimera 1, non interfaccia Genesis.

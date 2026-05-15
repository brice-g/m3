# Ressources — Module 3

## Cadre du module

M3 prolonge la pipeline FastIA construite en M2 en y branchant **plusieurs sources hétérogènes** (email, web, chat) et en anticipant un **nouveau besoin métier**. Pas de nouveau papier fondateur ici : on capitalise sur ce qui a été lu en M2 (Gebru, Wei & Zou) et on ajoute des références plus opérationnelles.

---

## Documentation technique

### Ingestion multi-source
- [Python `mailbox`](https://docs.python.org/3/library/mailbox.html) — lecture mbox
- [Python `email.parser`](https://docs.python.org/3/library/email.parser.html) — décodage en-têtes / corps multipart
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — extraction texte depuis HTML
- [Pandas — `read_csv` paramétrage avancé](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Pydantic v2 — modèles, validators, dataclasses](https://docs.pydantic.dev/latest/)

### Stockage et migrations
- [PostgreSQL — type `JSONB` et indexation](https://www.postgresql.org/docs/current/datatype-json.html)
- [Alembic — migrations SQLAlchemy](https://alembic.sqlalchemy.org/en/latest/) — autogenerate, downgrade, branches
- [MongoDB — getting started Python](https://pymongo.readthedocs.io/) — bonus B2 si la source NoSQL est ajoutée

### Déduplication
- [`datasketch` — MinHash et LSH](https://ekzhu.com/datasketch/minhash.html) — alternative au hash naïf pour B2
- [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) — embeddings légers pour dédup sémantique (bonus B2)

### Enrichissement (B3)
- [`langdetect`](https://pypi.org/project/langdetect/) — détection de langue rapide
- [`fasttext` — `lid.176`](https://fasttext.cc/docs/en/language-identification.html) — détection de langue robuste
- [`cmarkea/distilcamembert-base-sentiment`](https://huggingface.co/cmarkea/distilcamembert-base-sentiment) — sentiment français

### Outillage
- [Loguru](https://loguru.readthedocs.io) — déjà en place depuis M1
- [Pytest — fixtures, paramétrage, tmp_path](https://docs.pytest.org)

---

## Cadre réglementaire et éthique — à recroiser

- **RGPD — principe de minimisation** : <https://www.cnil.fr/fr/principes-cles/rgpd-minimisation-donnees> — particulièrement utile au B2 (champ `consent_marketing` à exclure)
- **CNIL — IA et données personnelles** : <https://www.cnil.fr/fr/intelligence-artificielle>
- **AI Act — texte officiel (règlement 2024/1689)** : <https://eur-lex.europa.eu/eli/reg/2024/1689/oj> — annexes utiles au B3 pour catégoriser le système
- **Green Algorithms** : <https://www.green-algorithms.org/> — empreinte carbone d'un calcul (bonus B3)

---

## Papiers — rappel M2 (toujours pertinents)

- Gebru et al. — *Datasheets for Datasets* — la datasheet est mise à jour à chaque brief M3 (nouvelles sources, champs dérivés)
- Wei & Zou — *EDA: Easy Data Augmentation* — utile en B2 si on doit générer du chat synthétique pour combler un gap

---

## Données fournies (`data/raw/`)

| Fichier | Brief | Description |
|---|---|---|
| `emails_fastia.mbox` | B1 | Échantillon ~30 emails clients (mix `text/plain`, `text/html`, multipart, encodages divers) |
| `formulaires_web.json` | B2 | ~50 soumissions de formulaire web, format JSON Lines |
| `chat_logs.csv` | B2 | ~80 lignes de transcript chat (visitor + agent), réparties sur 15-20 sessions |

Les volumétries sont volontairement faibles pour permettre une exécution locale rapide. Les **biais d'échantillonnage** sont assumés et font l'objet de l'analyse en B2.

# Hedge Counterexample

[English](README.en.md) · [Español](README.es.md)

**Trouver le scénario exact où une couverture apparemment complémentaire ne couvre plus.**

Deux titres similaires ne garantissent ni la même règle de résolution, ni l’exécution des deux jambes. Ce laboratoire examine des règles temporelles déclarées et des quantités exécutées explicites ; il exporte un témoin rejouable, avec calcul en centimes entiers.

## Essayer

Python 3.11+ ; bibliothèque standard, aucune clé ni connexion à une plateforme.

```sh
git clone https://github.com/gbesse/hedge-counterexample
cd hedge-counterexample
python3 -m hedge_counterexample serve --lang fr
```

Ouvrir `http://127.0.0.1:8773/?lang=fr`. Deux exercices, entièrement **fictifs** :

- **Fuseaux différents** : acheter oui avant 22 h UTC et non avant 22 h à New York ne couvre pas l’événement situé entre ces échéances. Avec dix unités par jambe, coût et frais déclarés, le pire net réglé vaut **−924 centimes fictifs**.
- **Exécutions partielles** : avec exactement la même règle, l’exécution totale des deux jambes donne un minimum de **+76**. Autoriser indépendamment 0, 5 ou 10 unités laisse un pire cas à **−462**, lorsqu’une seule jambe est exécutée.

Activer « résolution en attente » conserve une **fourchette nette**, pas une perte réalisée : pour dix unités sur deux jambes, `[−924, 1076]`, coût engagé non résolu 924. Le champ `settled_net_cents` reste `null`. Aucune probabilité ou recommandation n’en est déduite.

![Témoin](docs/preview-fr.png)

```sh
python3 -m hedge_counterexample demo > analyse.json
python3 -m hedge_counterexample analyze hedge_counterexample/examples/partial-fill-gap.json
python3 -m hedge_counterexample verify cas.json temoin.json
```

L’export navigateur contient `source_case` et `worst` : enregistrer ces deux objets séparément pour la commande `verify`. `pip install .` fournit aussi `hedge-counterexample`. UI et erreurs FR/EN/ES ; données utilisateur conservées telles quelles.

## Portée exacte du calcul

Les contrats paient 100 centimes par unité gagnante, avec côté oui/non, prix entier, frais par unité et frais fixes si au moins une unité est exécutée. Les frais des exemples sont **inventés** : 1 centime par unité + 2 par jambe exécutée, zéro frais fixe pour quantité nulle. Aucune formule de frais de plateforme n’est implémentée.

Le langage de règles accepte `before`, `at_or_before`, `not`, `and`, `or` sur des événements horodatés, éventuellement absents. Chaque événement a un domaine explicite de secondes UTC entières. Les échéances sont UTC/offset explicite ou heure locale + fuseau IANA. Les heures inexistantes sont refusées ; une heure d’automne ambiguë exige `fold: 0` ou `fold: 1`.

Pour chaque événement, la recherche examine les bornes du domaine et les secondes de part et d’autre de chaque échéance, puis regroupe les mêmes vecteurs de vérité atomiques. Ces cellules suffisent **pour ce langage restreint**. Le produit avec toutes les quantités d’exécution déclarées fournit le pire net ou la pire borne basse. L’exhaustivité exclut toute règle ou quantité omise. Limites : trois événements, six contrats, vingt prédicats atomiques, cinq quantités par contrat, 100 000 essais. Le vérificateur rejoue un témoin avec les mêmes règles et le même moteur arithmétique ; il n’est pas une preuve indépendante d’exhaustivité.

## Existant et limites

[Polymarket documente les exécutions totales ou partielles](https://docs.polymarket.com/trading/place-orders) et la [résolution selon les règles prédéfinies](https://help.polymarket.com/en/articles/13364518-how-are-prediction-markets-resolved). Ces sources motivent le problème ; aucun texte contractuel de marché n’est redistribué. Notre [jev-contract-graph](https://github.com/gbesse/jev-contract-graph) explore déjà les relations entre contrats. Ici, l’angle est le **témoin temporel normalisé + quantité exécutée + frais + résolution inconnue**, sans collecte de marchés.

Les données sont des contrats inventés, pas un arbitrage réel. Aucune interprétation automatique de contrat juridique, API de trading, carnet réel, risque de change, latence, capital requis, liquidité, effet de marché ou recommandation de placement. Les valeurs ne sont pas des prévisions. Pas de supériorité SOTA, de rentabilité réelle ou d’usage humain revendiqué.

## Vérifier

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Treize tests : frontières inclusives, changements d’heure, heures ambiguës/inexistantes, frais, zéro exécution, intervalles non résolus et témoin falsifié. Les cellules critiques sont comparées à une énumération seconde par seconde sur vingt petits cas aléatoires. Navigateur FR/EN/ES, deux exercices, exécutions totales/partielles, attente, export et mobile. CI Python 3.11/3.12 et roue hors sources. Licence MIT ; alpha publique.

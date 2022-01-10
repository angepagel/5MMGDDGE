# TP MongoDB

Ensimag 5MMGDDGE, Ange Pagel (N° étudiant 41900875)


## Interrogation de la base

### 1. 

Donnez la liste de tous les restaurants de la collection, triée par ordre de noms croissant.

```json
db.restaurants.find({
    name: { $ne: '' }
}).projection({
    name: 1
}).sort({
    name: 1
})
```

### 2. 

Donnez la liste de tous les restaurants proposant une cuisine de type `Italian` et affichez, pour chacun d'entre eux, le nom, le code postal et les coordonnées géographiques. De plus, assurez-vous que la réponse soit ordonnée selon la clé de tri (code postal croissant, nom décroissant).

```json
db.restaurants.find({
    cuisine: 'Italian'
}).projection({
    name: 1,
    'address.zipcode': 1,
    'address.coord': 1
}).sort({
    'address.zipcode': 1,
    name: -1
})
```

### 3.

Donnez la liste de tous les restaurants italiens ayant pour code postal `10075` et pour lesquels le numéro de téléphone est fourni dans la base de données. Affichez nom, code postal et numéro de téléphone.

```json
db.restaurants.find({
    cuisine: 'Italian',
    'address.zipcode': '10075',
    telephoneNumber: { $exists: true }
}).projection({
    name: 1,
    'address.zipcode': 1,
    telephoneNumber: 1
})
```

### 4.

Trouvez tous les restaurants ayant au moins un score supérieur ou égal à `50`.

```json
db.restaurants.find({
    'grades.score': { $gte: 50 }
})
```

### 5.

Donnez la liste de tous les restaurants qui sont soit italiens, soit ayant le code postal `10075`.

```json
db.restaurants.find({
    $or: [
        { cuisine: 'Italian' },
        { 'address.zipcode': '10075' }
    ]
})
```

### 6.

Donnez la liste de tous les restaurants dont le code postal est `10075` ou `10098`, dont la cuisine est soit italienne, soit américaine, et ayant au moins un score supérieur ou égal à `50`.

```json
db.restaurants.find({
    $and: [
        { 'address.zipcode': { $in: ['10075', '10098'] } },
        { cuisine: { $in: ['Italian', 'American'] } },
        { 'grades.score': { $gte: 50 } }
    ]
})
```

### 7.

Donnez la liste de tous les restaurants ayant au moins un score concernant le grade `customer service (C)`, `price (P)` ou `quality (Q)`. Affichez simplement les noms, la cuisine et le code postal.

```json
db.restaurants.find({
    $or: [
        { 'grades.grade': 'C' },
        { 'grades.grade': 'P' },
        { 'grades.grade': 'Q' }
    ]
}).projection({
    name: 1,
    cuisine: 1,
    'address.zipcode': 1
})
```

## Mises à jour

### 8.

Modifiez le type de cuisine du restaurant `Juni` pour le mettre à `American (new)`. Enregistrez également dans un champ `lastModified` la date et l’heure du système au moment où la modification est effectuée. S’il existe plusieurs restaurants portant le même nom, seul le premier doit être modifié.

```json
db.restaurants.updateOne({
    name: 'Juni'
}, {
    $set: {
        cuisine: 'American (new)',
        lastModified: new Date()
    }
})
```

### 9.

Changez l’adresse du restaurant dont l’identifiant (`restaurant_id`) est `41156888` en `East 31st Street`.

```json
db.restaurants.updateOne({
    restaurant_id: '41156888'
}, {
    $set: {
        'address.street': 'East 31st Street'
    }
})
```

### 10.

Changez le type de cuisine de tous les restaurants dont le code postal est `10016` et le type de cuisine `Other` en `Cuisine to be determined`. Enregistrez également dans un champ `lastModified` la date et l’heure du système au moment où la modification est effectuée.

```json
db.restaurants.updateMany({
    'address.zipcode': '10016',
    cuisine: 'Other'
}, {
    $set: {
        cuisine: 'Cuisine to be determined',
        lastModified: new Date()
    }
})
```

### 11.

Remplacez toute l’information concernant le restaurant dont l’identifiant est `41154403` par l’information suivante : 

```json
{
    "name": "Vella 2",
    "address": {
        "city": "1480",
        "street": "2 Avenue",
        "zipcode": "10075"
}
```

```json
db.restaurants.updateOne({
    restaurant_id: '41154403'
}, {
    $set: {
        name: 'Vella 2',
        address: {
            city: '1480',
            street: '2 Avenue',
            zipcode: '10075'
	    }
    }
})
```

## Interrogation complexe (agrégation)

### 12.

Dressez la liste des types de cuisine représentés dans la base. Pour chaque type, affichez le nombre de restaurants associés. Ordonnez le résultat par nombre de restaurants décroissants.

```json
db.restaurants.aggregate([
    {
        $group: {
            _id: '$cuisine',
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    }
])
```

### 13.

Affichez, pour chaque code postal, le nombre de restaurants italiens ayant ce code postal. Ordonnez le résultat par nombre de restaurants décroissants.

```json
db.restaurants.aggregate([
    {
        $match: {
            cuisine: 'Italian'
        }
    },
    {
        $group: {
            _id: '$address.zipcode',
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    }
])
```


### 14.

Considérez les restaurants italiens dont l’identifiant (`restaurant_id`) est supérieur ou égal à `41205309`, et possédant un attribut `averagePrice`. Calculez la moyenne de ces prix moyens. Puis refaites la même opération en calculant la moyenne par code postal.

```json
db.restaurants.aggregate([
    {
        $match: {
            cuisine: 'Italian',
            restaurant_id: { $gte: '41205309' },
            averagePrice: { $exists: true }
        }
    },
    {
        $group: {
            _id: '',
            moyenne: { $avg: '$averagePrice' }
        }
    }
])
```

```json
db.restaurants.aggregate([
    {
        $match: {
            cuisine: 'Italian',
            restaurant_id: { $gte: '41205309' },
            averagePrice: { $exists: true }
        }
    },
    {
        $group: {
            _id: '$address.zipcode',
            moyenne: { $avg: '$averagePrice' }
        }
    }
])
```

## Références entre collections et jointures

### 15.

Créer une nouvelle collection appelée `comments`, dans la même base de données.

```json
db.createCollection('comments')
```

### 16.

Insérez trois documents dans la collection précédemment créée, en utilisant le schéma suivant :

```json
{
    "_id": "----",
    "restaurant_id": "----",
    "client_id": "----",
    "comment": "----",
    "date": ISODate("----"),
    "type": "----"
}
```

Quelques précisions utiles :

- les identifiants de restaurants doivent correspondre à des restaurants existants dans la collection `restaurants `;
- vous devez fournir des commentaires de différents clients, et pour des restaurants différents ;
- l’attribut `type ` peut prendre uniquement les valeurs `positive` ou `negative`.

```json
db.comments.insertMany([
    {
        restaurant_id: '50003263',
        client_id: '56434124',
        comment: 'Surprizingly good cuisine. The location was leaving doubts',
        date: ISODate('2020-04-15T04:37:00.000Z'),
        type: 'positive'
    },
    {
        restaurant_id: '50008109',
        client_id: '794212638',
        comment: 'Very bad cuisine. To avoid !',
        date: ISODate('2019-12-31T00:00:00.000Z'),
        type: 'negative'
    },
    {
        restaurant_id: '50015658',
        client_id: '32189446',
        comment: 'Classical cuisine, but good',
        date: ISODate('2020-06-12T14:21:59.999Z'),
        type: 'positive'
    }
])
```

### 17.

Donnez la liste de tous les commentaires de votre base de données. Chaque commentaire doit contenir également toutes les informations concernant le restaurant auquel il se rapporte

```json
db.comments.aggregate([
    {
        $lookup: {
            from: 'restaurants',
            localField: 'restaurant_id',
            foreignField: 'restaurant_id',
            as: 'restaurant'
        }
    }
])
```

### 18.

Insérez 7 autres documents dans la collection `comments`, en suivant le schéma précédemment décrit, et en respectant les règles suivantes :

- les identifiants de restaurants doivent correspondre à des restaurants existants dans la collection `restaurants `;
- l’un des restaurants au moins doit avoir plusieurs commentaires ;
- l’un des clients au moins doit avoir commenté plusieurs fois ;
- l’un des clients au moins doit avoir commenté plusieurs fois le même restaurant ;
- l’attribut type peut prendre uniquement les valeurs `positive` ou `negative`.

```json
db.comments.insertMany([
{
  	 restaurant_id: '50003263',
	 client_id: '56434124',
	 comment: 'Gosh, looks bad but taste better',
	 date: ISODate('2018-04-15T04:37:00.000Z'),
	 type: 'positve'
   },
   {
  	 restaurant_id: '50008109',
	 client_id: '32189446',
	 comment: 'I ended sick...',
	 date: ISODate('2019-12-31T00:00:00.000Z'),
	 type: 'negative'
   },
   {
  	 restaurant_id: '40386062',
	 client_id: '32189446',
	 comment: 'Not bad at all',
	 date: ISODate('2020-01-12T14:21:59.999Z'),
	 type: 'positive'
  },
  {
  	 restaurant_id: '40386062',
	 client_id: '56434124',
	 comment: 'Berk !',
	 date: ISODate('2029-04-10T04:37:00.000Z'),
	 type: 'negative'
   },
   {
  	 restaurant_id: '50008109',
	 client_id: '79423638',
	 comment: "Bof... I've seen better food",
	 date: ISODate('2011-12-31T00:00:00.000Z'),
	 type: 'negative'
   },
   {
  	 restaurant_id: '50015658',
	 client_id: '32368446',
	 comment: 'Very good !',
	 date: ISODate('2018-03-12T14:21:59.999Z'),
	 type: 'positive'
  },
  {
	 restaurant_id: '50015658',
	 client_id: '32167246',
	 comment: 'Un régal !',
	 date: ISODate('2020-03-18T14:21:59.999Z'),
	 type: 'positive'
  }
])
```

### 19.

Trouvez la liste des restaurants ayant des commentaires, et affichez pour chaque restaurant uniquement le nom et la liste des commentaires. Plusieurs stratégies sont possibles.

```json
db.comments.aggregate([
    {
        $lookup: {
            from: 'restaurants',
            localField: 'restaurant_id',
            foreignField: 'restaurant_id',
            as: 'restaurant'
        }
    },
    {
        $unwind: '$restaurant'
    },
    {
        $group: {
            _id: '$restaurant.name',
            comments: { $push: '$comment' }
        }
    }
])
```

## Index

### 20.

Créez un index ascendant sur l’attribut `cuisine ` de la collection `restaurants`.

```json
db.restaurants.createIndex({ cuisine: 1 })
```

### 21.

Créez un autre index pour la collection `restaurants`, composé de l’attribut `cuisine ` (ascendant) et de l’attribut `zipcode ` (descendant).

```json
db.restaurants.createIndex({ cuisine: 1, zipcode: -1 })
```

### 22.

Affichez la liste des index créés sur la collection `restaurants`.

```json
db.restaurants.getIndexes()
```

### 23.

Utilisez la méthode `explain ` pour afficher le plan d’exécution d’une requête renvoyant tous les restaurants italiens. Quelles informations sont fournies par le système ?

```json
db.restaurants.find({ cuisine: 'Italian' }).explain()
```
Résultat de la commande `explain` :

```json
{ explainVersion: '1',
  queryPlanner: 
   { namespace: 'restaurants.restaurants',
     indexFilterSet: false,
     parsedQuery: { cuisine: { '$eq': 'Italian' } },
     maxIndexedOrSolutionsReached: false,
     maxIndexedAndSolutionsReached: false,
     maxScansToExplodeReached: false,
     winningPlan: 
      { stage: 'FETCH',
        inputStage: 
         { stage: 'IXSCAN',
           keyPattern: { cuisine: 1 },
           indexName: 'cuisine_1',
           isMultiKey: false,
           multiKeyPaths: { cuisine: [] },
           isUnique: false,
           isSparse: false,
           isPartial: false,
           indexVersion: 2,
           direction: 'forward',
           indexBounds: { cuisine: [ '["Italian", "Italian"]' ] } } },
     rejectedPlans: 
      [ { stage: 'FETCH',
          inputStage: 
           { stage: 'IXSCAN',
             keyPattern: { cuisine: 1, zipcode: -1 },
             indexName: 'cuisine_1_zipcode_-1',
             isMultiKey: false,
             multiKeyPaths: { cuisine: [], zipcode: [] },
             isUnique: false,
             isSparse: false,
             isPartial: false,
             indexVersion: 2,
             direction: 'forward',
             indexBounds: 
              { cuisine: [ '["Italian", "Italian"]' ],
                zipcode: [ '[MaxKey, MinKey]' ] } } } ] },
  command: 
   { find: 'restaurants',
     filter: { cuisine: 'Italian' },
     '$db': 'restaurants' },
  serverInfo: 
   { host: '43267c4cbc87',
     port: 27017,
     version: '5.0.5',
     gitVersion: 'd65fd89df3fc039b5c55933c0f71d647a54510ae' },
  serverParameters: 
   { internalQueryFacetBufferSizeBytes: 104857600,
     internalQueryFacetMaxOutputDocSizeBytes: 104857600,
     internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
     internalDocumentSourceGroupMaxMemoryBytes: 104857600,
     internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
     internalQueryProhibitBlockingMergeOnMongoS: 0,
     internalQueryMaxAddToSetBytes: 104857600,
     internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600 },
  ok: 1 }
```

Le système renvoie des informations sur le serveur MongoDB et sa configuration (`serverInfo` et `serverParameters`, ainsi que sur la requête et son optimisation (`command` et `queryPlanner`). L'objet `queryPlanner` contient des informations sur le plan d'exécution « gagnant » et sur les plans d'exécutions « rejetés », dont chaque opération est détaillée.

On observe que le plan d'exécution « gagnant » s'appuie sur une opération `IXSCAN` ciblée sur l'index `cuisine_1` : grâce à cet index, MongoDB n'a pas besoin de scanner tous les restaurants de la collection. Étant donné que la requête ne s'intéresse **qu'à l'attribut `cuisine`**, cela fait sens que le plan d'exécution basé sur l'index `cuisine_1_zipcode_-1` n'ait pas été retenu.

### 24.

Même question mais en ajoutant l’argument `executionStats` en paramètre de la méthode `explain`.

```json
db.restaurants.find({ cuisine: 'Italian' }).explain('executionStats')
```
Résultat de la commande `explain` :

```json
{ explainVersion: '1',
  queryPlanner: 
   { namespace: 'restaurants.restaurants',
     indexFilterSet: false,
     parsedQuery: { cuisine: { '$eq': 'Italian' } },
     maxIndexedOrSolutionsReached: false,
     maxIndexedAndSolutionsReached: false,
     maxScansToExplodeReached: false,
     winningPlan: 
      { stage: 'FETCH',
        inputStage: 
         { stage: 'IXSCAN',
           keyPattern: { cuisine: 1 },
           indexName: 'cuisine_1',
           isMultiKey: false,
           multiKeyPaths: { cuisine: [] },
           isUnique: false,
           isSparse: false,
           isPartial: false,
           indexVersion: 2,
           direction: 'forward',
           indexBounds: { cuisine: [ '["Italian", "Italian"]' ] } } },
     rejectedPlans: 
      [ { stage: 'FETCH',
          inputStage: 
           { stage: 'IXSCAN',
             keyPattern: { cuisine: 1, zipcode: -1 },
             indexName: 'cuisine_1_zipcode_-1',
             isMultiKey: false,
             multiKeyPaths: { cuisine: [], zipcode: [] },
             isUnique: false,
             isSparse: false,
             isPartial: false,
             indexVersion: 2,
             direction: 'forward',
             indexBounds: 
              { cuisine: [ '["Italian", "Italian"]' ],
                zipcode: [ '[MaxKey, MinKey]' ] } } } ] },
  executionStats: 
   { executionSuccess: true,
     nReturned: 1070,
     executionTimeMillis: 4,
     totalKeysExamined: 1070,
     totalDocsExamined: 1070,
     executionStages: 
      { stage: 'FETCH',
        nReturned: 1070,
        executionTimeMillisEstimate: 0,
        works: 1071,
        advanced: 1070,
        needTime: 0,
        needYield: 0,
        saveState: 1,
        restoreState: 1,
        isEOF: 1,
        docsExamined: 1070,
        alreadyHasObj: 0,
        inputStage: 
         { stage: 'IXSCAN',
           nReturned: 1070,
           executionTimeMillisEstimate: 0,
           works: 1071,
           advanced: 1070,
           needTime: 0,
           needYield: 0,
           saveState: 1,
           restoreState: 1,
           isEOF: 1,
           keyPattern: { cuisine: 1 },
           indexName: 'cuisine_1',
           isMultiKey: false,
           multiKeyPaths: { cuisine: [] },
           isUnique: false,
           isSparse: false,
           isPartial: false,
           indexVersion: 2,
           direction: 'forward',
           indexBounds: { cuisine: [ '["Italian", "Italian"]' ] },
           keysExamined: 1070,
           seeks: 1,
           dupsTested: 0,
           dupsDropped: 0 } } },
  command: 
   { find: 'restaurants',
     filter: { cuisine: 'Italian' },
     '$db': 'restaurants' },
  serverInfo: 
   { host: '43267c4cbc87',
     port: 27017,
     version: '5.0.5',
     gitVersion: 'd65fd89df3fc039b5c55933c0f71d647a54510ae' },
  serverParameters: 
   { internalQueryFacetBufferSizeBytes: 104857600,
     internalQueryFacetMaxOutputDocSizeBytes: 104857600,
     internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
     internalDocumentSourceGroupMaxMemoryBytes: 104857600,
     internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
     internalQueryProhibitBlockingMergeOnMongoS: 0,
     internalQueryMaxAddToSetBytes: 104857600,
     internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600 },
  ok: 1 }
```

L'argument `executionStats` de la méthode `explain` dévoile un nouvel objet `executionStats` détaillant les performances des étapes du plan d'exécution « gagnant ». On observe que, grâce à l'index `cuisine_1`, **MongoDB n'a examiné que le nombre exact de documents répondant au critère de la requête** (1070) : le coût total n'est que de 1071 « work units », et le temps d'exécution estimé de la requête est de 4 millisecondes.

### 25.

Supprimez les deux index que vous avez précédemment créés, puis affichez à nouveau les statistiques sur le plan d’exécution de la requête renvoyant tous les restaurants italiens. Que constatez-vous ?

```json
db.restaurants.dropIndex('cuisine_1')
db.restaurants.dropIndex('cuisine_1_zipcode_-1')
db.restaurants.find({ cuisine: 'Italian' }).explain('executionStats')
```
Résultat de la commande `explain` :

```json
{ explainVersion: '1',
  queryPlanner: 
   { namespace: 'restaurants.restaurants',
     indexFilterSet: false,
     parsedQuery: { cuisine: { '$eq': 'Italian' } },
     maxIndexedOrSolutionsReached: false,
     maxIndexedAndSolutionsReached: false,
     maxScansToExplodeReached: false,
     winningPlan: 
      { stage: 'COLLSCAN',
        filter: { cuisine: { '$eq': 'Italian' } },
        direction: 'forward' },
     rejectedPlans: [] },
  executionStats: 
   { executionSuccess: true,
     nReturned: 1070,
     executionTimeMillis: 22,
     totalKeysExamined: 0,
     totalDocsExamined: 25356,
     executionStages: 
      { stage: 'COLLSCAN',
        filter: { cuisine: { '$eq': 'Italian' } },
        nReturned: 1070,
        executionTimeMillisEstimate: 2,
        works: 25358,
        advanced: 1070,
        needTime: 24287,
        needYield: 0,
        saveState: 25,
        restoreState: 25,
        isEOF: 1,
        direction: 'forward',
        docsExamined: 25356 } },
  command: 
   { find: 'restaurants',
     filter: { cuisine: 'Italian' },
     '$db': 'restaurants' },
  serverInfo: 
   { host: '43267c4cbc87',
     port: 27017,
     version: '5.0.5',
     gitVersion: 'd65fd89df3fc039b5c55933c0f71d647a54510ae' },
  serverParameters: 
   { internalQueryFacetBufferSizeBytes: 104857600,
     internalQueryFacetMaxOutputDocSizeBytes: 104857600,
     internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
     internalDocumentSourceGroupMaxMemoryBytes: 104857600,
     internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
     internalQueryProhibitBlockingMergeOnMongoS: 0,
     internalQueryMaxAddToSetBytes: 104857600,
     internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600 },
  ok: 1 }
```

Sans index, on remarque que le plan d'exécution « gagnant » de cette requête est **beaucoup plus coûteux**. En effet, il repose sur une unique opération `COLLSCAN` qui **examine les 25356 documents de la collection** pour répondre au critère de la requête. Le temps d'exécution estimé de la requête est ici de 22 millisecondes (x5), et le coût s'élève à 25358 « work units » (x23).
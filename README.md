# blescan-pico

URL du repo : https://github.com/CLT-38/blescan-pico/

# Pico BLE Scanner

Ce projet transforme un Raspberry Pi Pico W en un scanner Bluetooth Low Energy (BLE). Il détecte les appareils à proximité, tente d'identifier leur fabricant, affiche leurs informations dans la console et fait clignoter la LED embarquée pour indiquer son fonctionnement.

## Matériel requis
- Un Raspberry Pi Pico W (le modèle **W** est indispensable pour le Bluetooth)
- Un PC
- Un câble USB (micro-B vers type A)

## Logiciel requis
- Le [firmware MicroPython pour Pico W](https://micropython.org/download/RPI_PICO_W/) installé sur le Raspberry Pico.
- Le logiciel [Thonny](https://thonny.org/) installé sur le PC.
- Le code de ce projet : `pico_ble_scan.py`.

## Connexion
Reliez le PC (port USB-A) et le Pico W (port micro-USB) avec le câble.

## Préparation dans Thonny
1.  Ouvrez Thonny.
2.  Allez dans le menu "Outils" -> "Options...".
3.  Dans l'onglet "Interpréteur", sélectionnez `MicroPython (Raspberry Pi Pico)` comme interpréteur.
4.  Juste en dessous, sélectionnez le port série correspondant à votre Pico (par ex. `COM3` sur Windows, `/dev/ttyACM0` sur Linux).
5.  Cliquez sur "OK". La console en bas devrait afficher une invite MicroPython (`>>>`).

## Télécharger et exécuter le code
1.  Ouvrez le fichier [pico_ble_scan.py](pico_ble_scan.py) dans l'éditeur de Thonny.
2.  Cliquez sur le bouton vert avec une flèche (ou appuyez sur F5) pour envoyer et exécuter le programme sur le Pico.

## Vérifier la bonne exécution
1.  Regardez la LED embarquée sur le Pico : elle doit se mettre à clignoter, indiquant que le script est actif.
2.  Observez la console dans Thonny. Après quelques secondes, vous devriez voir une sortie similaire à celle-ci, listant les appareils détectés :

```
Bonjour depuis la Pico

--- Nouveau cycle de scan ---
Scan des appareils BLE pendant 10 secondes...
Appareil: 67:c6:57:42:31:f2, RSSI: -99, Nom: N/A, Compagnie: Samsung Electronics Co., Ltd.
Appareil: 50:b3:0e:55:77:34, RSSI: -96, Nom: N/A, Compagnie: Plus Location Systems
Appareil: 0b:d6:b9:d3:02:9a, RSSI: -61, Nom: N/A, Compagnie: Microsoft

Scan terminé.
3 appareil(s) unique(s) trouvé(s) :
  - Addr: 0b:d6:b9:d3:02:9a, RSSI: -61, Nom: N/A, Compagnie: Microsoft
    MfgData: 06000109202225c95bd071072c903d6feb75f28259bcc386a549c4c3ac
  - Addr: 67:c6:57:42:31:f2, RSSI: -99, Nom: N/A, Compagnie: Samsung Electronics Co., Ltd.
    MfgData: 7500021861b1834556c7696e75d1dcc2635324f136a452e6c75d
  - Addr: 50:b3:0e:55:77:34, RSSI: -96, Nom: N/A, Compagnie: Plus Location Systems
    MfgData: c400013302131580

Pause de 60 secondes avant le prochain scan...
```

Le programme continuera de scanner, faire une pause, et recommencer, tant que le Pico est alimenté.

Combien d'appareils ont-ils été trouvés pendant ton exécution ?
Est-ce que tu reconnais ce que c'est comme appareil ?

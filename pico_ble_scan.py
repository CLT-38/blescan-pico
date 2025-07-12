from machine import Pin
from time import sleep
import ubluetooth
import time

led = Pin("LED", Pin.OUT)
print("Bonjour depuis la Pico")

# Classe pour gérer le scan BLE
class BLEScanner:
    # Dictionnaire des identifiants d'entreprise BLE connus (Company IDs)
    # La liste complète est sur bluetooth.com
    COMPANY_IDS = {
        0x0006: "Microsoft",
        0x004C: "Apple, Inc.",
        0x0075: "Samsung Electronics Co., Ltd.",
        0x00E0: "Google",
        0x0157: "Bose Corporation",
        0x00C4: "Plus Location Systems", # Trouvé dans votre scan précédent
    }

    def __init__(self):
        self.ble = ubluetooth.BLE()
        # Activer l'interface Bluetooth
        self.ble.active(True)
        # Définir le gestionnaire d'interruptions pour les événements BLE
        self.ble.irq(self.irq_handler)
        self.found_devices = {}

    def clear_devices(self):
        """Vide la liste des appareils trouvés."""
        self.found_devices = {}

    @staticmethod
    def decode_name(adv_data):
        """Recherche et décode le nom de l'appareil dans les données de l'annonce."""
        i = 0
        while i < len(adv_data):
            length = adv_data[i]
            if length == 0:
                break
            ad_type = adv_data[i + 1]
            # Type de donnée pour "Shortened Local Name" (0x08) ou "Complete Local Name" (0x09)
            if ad_type == 0x08 or ad_type == 0x09:
                return bytes(adv_data[i + 2 : i + 1 + length]).decode('utf-8', 'ignore')
            i += 1 + length
        return None

    @staticmethod
    def decode_manufacturer_data(adv_data):
        """Recherche et décode les données du fabricant dans les données de l'annonce."""
        i = 0
        while i < len(adv_data):
            length = adv_data[i]
            if length == 0:
                break
            ad_type = adv_data[i + 1]
            # Type de donnée pour "Manufacturer Specific Data" (0xFF)
            if ad_type == 0xFF:
                return bytes(adv_data[i + 2 : i + 1 + length]).hex()
            i += 1 + length
        return None

    @staticmethod
    def get_company_name(mfg_data):
        """Extrait l'ID de l'entreprise des données du fabricant et retourne son nom."""
        if not mfg_data or len(mfg_data) < 4:
            return None
        # L'ID de l'entreprise est sur 2 octets (4 caractères hex), en format little-endian.
        # On inverse les octets pour la lecture. Ex: "7500" -> "0075"
        company_id_str = mfg_data[2:4] + mfg_data[0:2]
        try:
            company_id = int(company_id_str, 16)
            return BLEScanner.COMPANY_IDS.get(company_id)
        except (ValueError, IndexError):
            return None

    # Gestionnaire d'interruptions pour les résultats du scan
    def irq_handler(self, event, data):
        # _IRQ_SCAN_RESULT: un appareil a été trouvé
        if event == 5:
            addr_type, addr, adv_type, rssi, adv_data = data
            # Convertir l'adresse en une chaîne de caractères lisible
            addr_str = ":".join(f"{b:02x}" for b in addr)
            
            name = self.decode_name(adv_data)
            mfg_data = self.decode_manufacturer_data(adv_data)
            company = self.get_company_name(mfg_data)

            # On met à jour si c'est un nouvel appareil, ou si on a trouvé des infos qu'on n'avait pas avant
            if addr_str not in self.found_devices or \
               (name and not self.found_devices[addr_str].get('name')) or \
               (mfg_data and not self.found_devices[addr_str].get('mfg_data')):
                
                self.found_devices[addr_str] = {
                    "addr": addr_str,
                    "rssi": rssi,
                    "name": name,
                    "mfg_data": mfg_data,
                    "company": company,
                    "data": bytes(adv_data).hex()
                }
                print(f"Appareil: {addr_str}, RSSI: {rssi}, Nom: {name or 'N/A'}, Compagnie: {company or 'Inconnue'}")

    # Fonction pour démarrer le scan
    def scan(self, duration_s=10):
        print(f"Scan des appareils BLE pendant {duration_s} secondes...")
        # Démarrer le scan (durée en ms, intervalle en µs, fenêtre en µs)
        # Le dernier paramètre (False) indique un scan passif
        self.ble.gap_scan(duration_s * 1000, 30000, 30000, False)
        
        # Attendre la fin de la durée du scan
        time.sleep(duration_s)
        
        # Arrêter le scan
        self.ble.gap_scan(None)
        
        print("\nScan terminé.")
        if self.found_devices:
            print(f"{len(self.found_devices)} appareil(s) unique(s) trouvé(s) :")
            # Afficher tous les appareils trouvés
            for addr, device_info in self.found_devices.items():
                name = device_info.get('name')
                mfg_data = device_info.get('mfg_data')
                company = device_info.get('company')
                print(f"  - Addr: {addr}, RSSI: {device_info['rssi']}, Nom: {name or 'N/A'}, Compagnie: {company or 'Inconnue'}")
                if mfg_data:
                    print(f"    MfgData: {mfg_data}")
        else:
            print("Aucun appareil trouvé.")

# Point d'entrée principal du script
# Créer l'instance du scanner une seule fois
scanner = BLEScanner()

while True:
    led.toggle() # Faire clignoter la LED pour montrer que le programme est actif
    
    print("\n--- Nouveau cycle de scan ---")
    # Optionnel: vider la liste avant chaque nouveau scan
    # Si vous commentez la ligne suivante, la liste contiendra tous les appareils
    # vus depuis le démarrage.
    scanner.clear_devices()
    
    scanner.scan(10) # Lancer un scan de 10 secondes
    
    print(f"Pause de 60 secondes avant le prochain scan...")
    # Faire une pause, mais faire clignoter la LED pendant ce temps
    for _ in range(60):
        led.toggle()
        time.sleep(0.5)
        led.toggle()
        time.sleep(0.5)

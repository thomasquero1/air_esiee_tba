"""
Script pour générer les images de base pour le jeu Air ESIEE.
Ces images serviront d'images temporaires de haute qualité jusqu'à ce que vous les remplaciez
par vos propres images.
"""

from PIL import Image, ImageDraw
import os

# Créer le dossier images s'il n'existe pas
images_dir = os.path.join(os.path.dirname(__file__), "images")
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

def create_cockpit():
    """Crée l'image du cockpit."""
    img = Image.new("RGB", (1280, 960), color="#001a33")
    draw = ImageDraw.Draw(img)
    
    # Cadre principal
    draw.rectangle([40, 40, 1240, 920], outline="#00ff00", width=4)
    
    # Titre
    draw.text((400, 60), "COCKPIT A320", fill="#00ff00")
    draw.text((350, 120), "Air ESIEE - Systemes Avioniques", fill="#00ff00")
    
    # Sieges
    draw.rectangle([80, 180, 300, 380], fill="#333333", outline="#00ff00", width=3)
    draw.text((130, 270), "COMMANDANT", fill="#00ff00")
    
    draw.rectangle([350, 180, 570, 380], fill="#555555", outline="#ffff00", width=3)
    draw.text((400, 270), "COPILOTE", fill="#ffff00")
    
    # Tableau de bord principal
    draw.rectangle([80, 420, 1200, 900], fill="#1a1a1a", outline="#00ff00", width=3)
    draw.text((400, 450), "SYSTEMES AVIONIQUES - FCU", fill="#00ff00")
    
    # Instruments
    draw.text((120, 520), "ALTITUDE : 35 000 ft", fill="#00ff00")
    draw.text((500, 520), "VITESSE : 450 kt", fill="#00ff00")
    draw.text((920, 520), "CAP : 090", fill="#00ff00")
    
    draw.text((120, 580), "VITESSE VERTICALE : 0 ft/min", fill="#00ff00")
    draw.text((500, 580), "MACH : 0,78", fill="#00ff00")
    draw.text((920, 580), "TEMPÉRATURE : -56°C", fill="#00ff00")
    
    draw.text((120, 650), "CARBURANT : 3000 kg", fill="#00ff00")
    draw.text((500, 650), "MOTEURS : N1 = 25 %, N2 = 60 %", fill="#00ff00")
    draw.text((120, 720), "HYDRAULIQUE : VERTE", fill="#00ff00")
    draw.text((500, 720), "ÉLECTRIQUE : 28,5 V", fill="#00ff00")
    
    img.save(os.path.join(images_dir, "Cockpit.jpg"), quality=95)
    print("✓ Cockpit.jpg créé")

def create_copilot_seat():
    """Crée l'image du siège du copilote."""
    img = Image.new("RGB", (1280, 960), color="#2a2a2a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#0080ff", width=4)
    draw.text((350, 60), "POSITION COPILOTE", fill="#0080ff")
    
    # Siège
    draw.ellipse([400, 250, 880, 650], fill="#444444", outline="#0080ff", width=4)
    draw.rectangle([450, 650, 830, 750], fill="#333333", outline="#0080ff", width=3)
    
    # Détails
    draw.text((300, 800), "Siege confortable, vue panoramique sur les instruments", fill="#0080ff")
    draw.text((300, 850), "Ceinture de securite: ATTACHEE", fill="#00ff00")
    
    img.save(os.path.join(images_dir, "CopilotSeat.jpg"), quality=95)
    print("✓ CopilotSeat.jpg créé")

def create_central_panel():
    """Crée l'image du panneau central (ECAM)."""
    img = Image.new("RGB", (1280, 960), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#ff8800", width=4)
    draw.text((350, 60), "PANNEAU CENTRAL - ECAM", fill="#ff8800")
    
    # Écran ECAM
    draw.rectangle([80, 150, 1200, 850], fill="#0a0a0a", outline="#ff8800", width=3)
    
    draw.text((120, 180), "STATUT ECAM - PHASE CROISIÈRE", fill="#ff8800")
    draw.line([(120, 220), (1180, 220)], fill="#ff8800", width=2)
    
    # Systèmes
    draw.text((120, 260), "SEATBELT: OFF", fill="#ff0000")
    draw.text((120, 310), "NO SMOKING: AUTO", fill="#ffff00")
    draw.text((120, 360), "X-BLEED: OFF", fill="#ff0000")
    draw.text((120, 410), "PRESSURIZATION: AUTO", fill="#00ff00")
    draw.text((120, 460), "CABIN TEMP: 22C", fill="#00ff00")
    
    draw.text((600, 260), "HYDRAULIC A: GREEN 3000 psi", fill="#00ff00")
    draw.text((600, 310), "HYDRAULIC B: GREEN 3000 psi", fill="#00ff00")
    draw.text((600, 360), "HYDRAULIC RAT: OFF", fill="#ff0000")
    draw.text((600, 410), "BRAKES: NORMAL", fill="#00ff00")
    
    draw.text((120, 650), "QRH - Quick Reference Handbook disponible", fill="#ffff00")
    draw.text((120, 700), "Pour voir les checklist: utilisez la commande 'use QRH'", fill="#ffff00")
    
    img.save(os.path.join(images_dir, "CentralPanel.jpg"), quality=95)
    print("✓ CentralPanel.jpg créé")

def create_top_panel():
    """Crée l'image du panneau supérieur."""
    img = Image.new("RGB", (1280, 960), color="#1a0a1a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#ff00ff", width=4)
    draw.text((300, 60), "PANNEAU HAUT - ECLAIRAGE & ELECTRICITE", fill="#ff00ff")
    
    # Batteries
    draw.rectangle([80, 150, 600, 400], fill="#0a0a0a", outline="#ff00ff", width=3)
    draw.text((120, 180), "BATTERIES", fill="#ff00ff")
    draw.text((120, 240), "BAT: ON", fill="#00ff00")
    draw.text((120, 290), "TENSION: 28.5V", fill="#00ff00")
    draw.text((120, 340), "CAPACITE: 85%", fill="#00ff00")
    
    # Fuel
    draw.rectangle([680, 150, 1200, 400], fill="#0a0a0a", outline="#ff00ff", width=3)
    draw.text((720, 180), "CARBURANT", fill="#ff00ff")
    draw.text((720, 240), "RESTE: 3000 kg", fill="#00ff00")
    draw.text((720, 290), "CONSOMMATION: 500 kg/h", fill="#00ff00")
    draw.text((720, 340), "AUTONOMIE: 6h30", fill="#00ff00")
    
    # Lights
    draw.rectangle([80, 450, 1200, 850], fill="#0a0a0a", outline="#ff00ff", width=3)
    draw.text((120, 480), "LIGHTS", fill="#ff00ff")
    draw.text((120, 540), "LANDING LIGHT: ON", fill="#00ff00")
    draw.text((120, 590), "TAXI LIGHT: ON", fill="#00ff00")
    draw.text((120, 640), "STROBE: ON", fill="#00ff00")
    draw.text((120, 690), "CABIN LIGHT: AUTO", fill="#00ff00")
    
    draw.text((600, 540), "NAVIGATION LIGHTS: ON", fill="#00ff00")
    draw.text((600, 590), "EMERGENCY EXIT LIGHTS: ARMED", fill="#ffff00")
    
    img.save(os.path.join(images_dir, "TopPanel.jpg"), quality=95)
    print("✓ TopPanel.jpg créé")

def create_bottom_panel():
    """Crée l'image du panneau inférieur."""
    img = Image.new("RGB", (1280, 960), color="#0a1a1a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#00ff88", width=4)
    draw.text((250, 60), "PANNEAU BAS - MANETTES & COMMUNICATIONS", fill="#00ff88")
    
    # Manettes de gaz
    draw.rectangle([80, 150, 600, 500], fill="#0a0a0a", outline="#00ff88", width=3)
    draw.text((120, 180), "THROTTLE (GAZ)", fill="#00ff88")
    draw.text((120, 240), "MOTEUR 1: IDLE (0%)", fill="#00ff00")
    draw.text((120, 290), "MOTEUR 2: IDLE (0%)", fill="#00ff00")
    draw.text((120, 340), "THRUST MODE: SPEED", fill="#00ff00")
    draw.text((120, 390), "VOLETS: 1 (5)", fill="#00ff00")
    draw.text((120, 440), "GEAR: DOWN", fill="#00ff00")
    
    # Communications
    draw.rectangle([680, 150, 1200, 500], fill="#0a0a0a", outline="#00ff88", width=3)
    draw.text((720, 180), "COMMUNICATIONS", fill="#00ff88")
    draw.text((720, 240), "RADIO: 121.5 MHz (TOWER)", fill="#00ff00")
    draw.text((720, 290), "STATUS: CLAIR", fill="#00ff00")
    draw.text((720, 340), "TRANSPONDER: 8681", fill="#00ff00")
    draw.text((720, 390), "SELCAL: ON", fill="#00ff00")
    
    # Notes
    draw.text((80, 600), "Note: Reposer les manettes est important en croisiere", fill="#ffff00")
    draw.text((80, 650), "Les moteurs sont a vide (IDLE) pour economiser le carburant", fill="#ffff00")
    
    img.save(os.path.join(images_dir, "BottomPanel.jpg"), quality=95)
    print("✓ BottomPanel.jpg créé")

def create_altimeter():
    """Crée l'image de l'altimètre."""
    img = Image.new("RGB", (1280, 960), color="#001a00")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#00ff00", width=4)
    draw.text((300, 60), "ALTIMETRE & VARIOMETRE", fill="#00ff00")
    
    # Altimètre
    draw.ellipse([150, 180, 550, 580], outline="#00ff00", width=4)
    draw.text((250, 370), "35000 ft", fill="#00ff00")
    draw.text((200, 450), "Croisiere", fill="#00ff00")
    
    # Variomètre
    draw.ellipse([700, 180, 1100, 580], outline="#00ff00", width=4)
    draw.text((800, 370), "VS: 0 ft/min", fill="#00ff00")
    draw.text((800, 450), "Stable", fill="#00ff00")
    
    # Info
    draw.text((80, 700), "Vous maintenez une altitude de croisiere stable", fill="#00ff00")
    draw.text((80, 750), "Vitesse verticale: ZERO - Pas de montee ni de descente", fill="#00ff00")
    draw.text((80, 850), "C'est l'altitude ideale pour la croisiere transatlantique", fill="#ffff00")
    
    img.save(os.path.join(images_dir, "Altimeter.jpg"), quality=95)
    print("✓ Altimeter.jpg créé")

def create_radar():
    """Crée l'image du radar."""
    img = Image.new("RGB", (1280, 960), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#00ffff", width=4)
    draw.text((250, 60), "RADAR METEO & NAVIGATION", fill="#00ffff")
    
    # Radar météo
    draw.ellipse([80, 180, 550, 650], outline="#00ffff", width=3)
    draw.text((250, 410), "CLEAR", fill="#00ff00")
    draw.text((180, 480), "No Weather", fill="#00ff00")
    draw.text((150, 550), "Perfect visibility", fill="#00ff00")
    
    # Navigation
    draw.rectangle([650, 180, 1200, 650], fill="#0a0a0a", outline="#00ffff", width=3)
    draw.text((690, 210), "NAVIGATION", fill="#00ffff")
    draw.text((690, 280), "ROUTE: ORLY -> DESTINATION", fill="#00ff00")
    draw.text((690, 330), "DISTANCE: 150 nm", fill="#00ff00")
    draw.text((690, 380), "HEADING: 090", fill="#00ff00")
    draw.text((690, 430), "ETA: 12:30 UTC", fill="#00ff00")
    draw.text((690, 480), "TRACK: ON COURSE", fill="#00ff00")
    draw.text((690, 530), "WIND: 20 kt FROM 270", fill="#00ff00")
    
    # Info
    draw.text((80, 750), "Meteo degagee sur toute la route", fill="#00ffff")
    draw.text((80, 850), "Navigation: parfait alignement avec la route prevue", fill="#ffff00")
    
    img.save(os.path.join(images_dir, "Radar.jpg"), quality=95)
    print("✓ Radar.jpg créé")

def create_crew_zone():
    """Crée l'image de la zone équipage."""
    img = Image.new("RGB", (1280, 960), color="#2a1a1a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#ff6600", width=4)
    draw.text((350, 60), "ZONE EQUIPAGE", fill="#ff6600")
    
    # Hôtesse
    draw.ellipse([400, 250, 600, 500], fill="#ffaa00", outline="#ff6600", width=3)
    draw.text((450, 370), "HOTESSE", fill="#000000")
    
    # Info
    draw.text((150, 600), "L'hotesse semble fatiguee...", fill="#ff6600")
    draw.text((150, 660), "Elle a besoin de se detendre", fill="#ff6600")
    draw.text((150, 720), "Un cafe lui ferait du bien...", fill="#ffff00")
    
    draw.text((150, 830), "QUETE: Apportez un cafe a l'hotesse", fill="#ff8800")
    
    img.save(os.path.join(images_dir, "CrewZone.jpg"), quality=95)
    print("✓ CrewZone.jpg créé")

def create_business_cabin():
    """Crée l'image de la cabine business."""
    img = Image.new("RGB", (1280, 960), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#cccccc", width=4)
    draw.text((350, 60), "CABINE BUSINESS", fill="#cccccc")
    
    # Sièges business
    for i in range(3):
        draw.rectangle([120 + i*350, 200, 320 + i*350, 400], 
                      fill="#666666", outline="#cccccc", width=3)
        draw.text((200 + i*350, 290), f"P{i+1}", fill="#ffffff")
    
    # Info
    draw.text((150, 550), "3 passagers Business a bord", fill="#cccccc")
    draw.text((150, 620), "Passager 1: demande de l'eau", fill="#ffff00")
    draw.text((150, 680), "Passager 2: dort paisiblement", fill="#00ff00")
    draw.text((150, 740), "Passager 3: travaille sur laptop", fill="#00ff00")
    
    draw.text((150, 850), "QUETE: Servez de l'eau au passager 1", fill="#ff8800")
    
    img.save(os.path.join(images_dir, "BusinessCabin.jpg"), quality=95)
    print("✓ BusinessCabin.jpg créé")

def create_economy_cabin():
    """Crée l'image de la cabine économique."""
    img = Image.new("RGB", (1280, 960), color="#1a1a1a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#888888", width=4)
    draw.text((350, 60), "CABINE ECONOMY", fill="#888888")
    
    # Sièges economy
    for row in range(3):
        for col in range(4):
            x = 100 + col*280
            y = 150 + row*180
            draw.rectangle([x, y, x+240, y+140], fill="#333333", outline="#888888", width=2)
    
    # Info
    draw.text((150, 700), "80 passagers en cabine economique", fill="#888888")
    draw.text((150, 760), "Un passager (P2) semble malade...", fill="#ff0000")
    draw.text((150, 820), "Il a besoin d'aide medicale immediatement!", fill="#ff0000")
    
    draw.text((150, 880), "QUETE URGENT: Intervenez avec trousse medicale", fill="#ff8800")
    
    img.save(os.path.join(images_dir, "EconomyCabin.jpg"), quality=95)
    print("✓ EconomyCabin.jpg créé")

def create_back_crew_zone():
    """Crée l'image de la zone arrière équipage."""
    img = Image.new("RGB", (1280, 960), color="#1a1a0a")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 40, 1240, 920], outline="#ffff00", width=4)
    draw.text((250, 60), "ZONE ARRIERE EQUIPAGE", fill="#ffff00")
    
    # Caféière
    draw.rectangle([100, 180, 400, 450], fill="#8B4513", outline="#ffff00", width=3)
    draw.text((140, 300), "CAFETIERE", fill="#ffff00")
    
    # Provisions
    draw.rectangle([550, 180, 850, 450], fill="#666666", outline="#ffff00", width=3)
    draw.text((570, 300), "PROVISIONS", fill="#ffff00")
    
    # Passager
    draw.ellipse([1000, 250, 1150, 400], fill="#ffcc00", outline="#ffff00", width=3)
    draw.text((1030, 320), "P3", fill="#000000")
    
    # Info
    draw.text((100, 550), "Zone arriere equipage", fill="#ffff00")
    draw.text((100, 610), "Cafe disponible - Chaud et revigorant", fill="#00ff00")
    draw.text((100, 670), "Provisions: eau, snacks, trousse medicale", fill="#00ff00")
    draw.text((100, 730), "Passager 3: Nerveux, demande quand on atterrit", fill="#ffff00")
    
    draw.text((100, 850), "QUETE: Rassurez le passager 3", fill="#ff8800")
    
    img.save(os.path.join(images_dir, "BackCrewZone.jpg"), quality=95)
    print("✓ BackCrewZone.jpg créé")

def main():
    """Génère toutes les images."""
    print("\n" + "="*60)
    print("GENERATION DES IMAGES DU JEU AIR ESIEE")
    print("="*60 + "\n")
    
    create_cockpit()
    create_copilot_seat()
    create_central_panel()
    create_top_panel()
    create_bottom_panel()
    create_altimeter()
    create_radar()
    create_crew_zone()
    create_business_cabin()
    create_economy_cabin()
    create_back_crew_zone()
    
    print("\n" + "="*60)
    print("✓ TOUTES LES IMAGES SONT GENEREES!")
    print("="*60)
    print("\nLes images sont situees dans: images/")
    print("Vous pouvez les remplacer par vos propres images en conservant les memes noms de fichiers.")
    print("\nFormats supportes: JPG, PNG, GIF, BMP, etc.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

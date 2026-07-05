# 🔭 Astro Studio

Astro Studio est une application de traitement d’images astrophotographiques centrée sur le mix SHO (SII / Hα / OIII).  
Elle permet de charger un projet, manipuler des palettes, ajuster le stretch et le zoom, et exporter des images RGB.

---

## ✨ Fonctionnalités actuelles

- 📂 Gestion de projets astrophotographiques
- 🌈 Mixage SHO (SII / Hα / OIII)
- 🎨 Palettes prédéfinies + mode manuel
- 🔍 Preview interactive en temps réel
- 📈 Ajustement du stretch
- 🔎 Zoom d’inspection
- 💾 Export des canaux RGB en FITS

---

## 🧪 Workflow utilisateur

1. Créer ou sélectionner un dossier projet
2. Ajouter les fichiers :
   - `SII.fit`
   - `HA.fit`
   - `OIII.fit`
3. Aller dans l’onglet **Traitement**
4. Choisir une palette ou régler manuellement les coefficients
5. Ajuster stretch et zoom
6. Exporter les images RGB

---

## 📁 Structure d’un projet
mon_projet/
├── SII.fit
├── HA.fit
├── OIII.fit


---

## 🚀 Installation (mode développement)

### 1. Cloner le projet
```bash
git clone https://github.com/Sikuath/Astro_studio.git
cd Astro_studio

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

### 3. Installer les dépendances
```bash
pip install -r requirements.txt


## ▶️ Utiliser l'application
lancer Astro_studio.bat

⚙️ Dépendances principales
streamlit
numpy
scipy
astropy (lecture FITS si utilisé)
pillow (preview image)

🎨 Palettes disponibles
Manual
Hubble SHO
HOO Boost
HOO Natural
Hα Rich
OIII Rich
Foraxx Pro
Gold & Blue
Teal & Orange

💾 Export

L’application génère :

R.fit
G.fit
B.fit

aucune installation Python requise pour les utilisateurs
🔭 Vision à long terme

Astro Studio est conçu pour évoluer vers un outil pédagogique pour club astro :

simplification de l’interface pour les élèves
presets de traitement automatiques
mode guidé (workflow pas à pas)
distribution facile sous Windows
📄 Licence

MIT License © 2026
# Architecture — Theta Ingénierie

Connecteurs Claude pour l'architecture et le béton armé. Le dépôt est sur le compte [thetaingenierie-png](https://github.com/thetaingenierie-png). Le même contenu se clone sur un Mac ou un PC Windows : les nouveautés Autodesk suivent le dépôt, pas une seule machine.

Compte Claude visé : `thetaingenierie@gmail.com`.

Les skills AutoCAD sont dans [thetaingenierie-png/autocad-skills](https://github.com/thetaingenierie-png/autocad-skills).

## Connecteurs dans ce dépôt

| Connecteur | Usage |
| --- | --- |
| Autodesk Product Help | Documentation officielle à jour : Revit, ferraillage, AutoCAD, Robot, Navisworks, Civil 3D. |
| IFC | Métrés béton et acier depuis un fichier IFC, sans Revit ouvert. |
| AutoCAD | Plans DXF, sans AutoCAD ouvert. |
| Fusion Data | Projets Fusion, après une connexion au compte Autodesk. |

Sur un PC Windows où Revit 2027.2 et le serveur officiel Read-Tools sont installés, `scripts/install.py` ajoute aussi le connecteur Revit. Il ne parle au modèle que pendant que Revit est ouvert.

## Nouvelle machine

```bash
git clone https://github.com/thetaingenierie-png/architecture.git
cd architecture
python3 scripts/install.py
```

Sur Windows :

```powershell
git clone https://github.com/thetaingenierie-png/architecture.git
cd architecture
python scripts/install.py
```

Le script ajoute les connecteurs dans Claude Desktop et dans Claude Code. Il ne retire pas les autres connecteurs. Fermez ensuite Claude complètement, puis rouvrez-le avec le compte `thetaingenierie@gmail.com`.

`uv` et Node.js doivent être installés (`uvx` et `npx`). Sans eux, l'aide Autodesk en HTTP reste utilisable par Claude Code via `.mcp.json`, mais IFC et AutoCAD ne démarrent pas.

## Claude Code dans ce dossier

Ouvrir ce dépôt dans Claude Code charge `.mcp.json`. Les connecteurs sont alors ceux de Theta, sur la machine où le dossier est cloné.

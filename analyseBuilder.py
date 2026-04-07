import inspect
import importlib
import re

modules_to_scan = ["Data", "Engine", "InventorySystem", "Main", "Objects", "SceneManager", "TilemapManager", "Tools", "UI"]

def slugify(text):
    return text.lower().strip().replace(' ', '-')

def extract_pure_attributes(cls):
    """Extrait les variables d'instance et leurs types à partir du code source."""
    attrs = {} # Utilisation d'un dict pour éviter les doublons et garder les types
    
    # 1. Analyse des annotations de classe standard (si présentes)
    annotations = getattr(cls, '__annotations__', {})
    for attr, t in annotations.items():
        if not callable(getattr(cls, attr, None)):
            attrs[attr] = getattr(t, '__name__', str(t))
    
    # 2. Analyse du code source pour les attributs d'instance (self.xxx: type = ...)
    try:
        source = inspect.getsource(cls)
        
        # Regex améliorée : 
        # Cherche "self.nom", optionnellement ": type", puis un "=" 
        # MAIS ignore si suivi de "(" (appel de méthode)
        pattern = r"self\.([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*:\s*([a-zA-Z0-9_\[\]\"']+))?\s*="
        matches = re.findall(pattern, source)
        
        for name, type_hint in matches:
            # On vérifie que ce n'est pas une méthode existante
            if not hasattr(cls, name) or not callable(getattr(cls, name)):
                # Si on a trouvé un type (ex: float), on l'utilise, sinon "any"
                t = type_hint if type_hint else "any"
                # On ne remplace pas si on a déjà un type précis via les annotations de classe
                if name not in attrs or attrs[name] == "any":
                    attrs[name] = t.replace("'", "").replace('"', '') # Nettoyage des strings de type
    except:
        pass
        
    # Formattage final
    result = [f"{name} : `{t}`" for name, t in attrs.items()]
    return sorted(result)

def get_markdown_class_info(cls, all_classes_names):
    name = cls.__name__
    md = f"### {name}\n\n"
    
    # Héritage
    parents = [b for b in cls.__bases__ if b.__name__ != 'object']
    if parents:
        links = [f"[{p.__name__}](#{slugify(p.__name__)})" if p.__name__ in all_classes_names else f"`{p.__name__}`" for p in parents]
        md += f"**Hérite de :** {', '.join(links)}\n\n"

    # SECTION ATTRIBUTS
    md += "**Attributs (propres) :**\n"
    attrs = extract_pure_attributes(cls)
    if attrs:
        for a in attrs:
            md += f"* {a}\n"
    else:
        md += "* (Aucun attribut propre détecté)\n"
    
    # SECTION MÉTHODES
    md += "\n**Méthodes (propres) :**\n"
    methods_found = False
    for m_name, obj in cls.__dict__.items():
        # On ne garde que ce qui est callable et pas privé (ou alors garde les _ si tu veux)
        actual_obj = getattr(cls, m_name)
        if callable(actual_obj) and not m_name.startswith("__"):
            methods_found = True
            try:
                sig = inspect.signature(actual_obj)
                clean_sig = str(sig).replace('self, ', '').replace('self', '')
                md += f"* {m_name}{clean_sig}\n"
            except:
                md += f"* {m_name}(...)\n"
    
    if not methods_found:
        md += "* (Aucune méthode propre)\n"
    
    md += "\n---\n\n"
    return md

def main():
    full_markdown = "# Document d'Analyse du Projet\n_réalisé avec la bibliothèque inspect_\n"
    all_classes = []
    
    # Passage 1 : Indexation
    for mod_name in modules_to_scan:
        try:
            module = importlib.import_module(mod_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == mod_name: all_classes.append(name)
        except: pass

    # Passage 2 : Génération
    for mod_name in modules_to_scan:
        try:
            module = importlib.import_module(mod_name)
            full_markdown += f"## Fichier : {mod_name}.py\n\n"
            classes = [obj for _, obj in inspect.getmembers(module, inspect.isclass) if obj.__module__ == mod_name]
            for obj in classes:
                full_markdown += get_markdown_class_info(obj, all_classes)
        except Exception as e:
            full_markdown += f"**Erreur {mod_name}** : {e}\n"

    with open("ANALYSE.md", "w", encoding="utf-8") as f:
        f.write(full_markdown)

if __name__ == "__main__":
    main()
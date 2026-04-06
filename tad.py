import inspect
import importlib
import urllib.parse

# Liste de tes modules
modules_to_scan = ["Data", "Engine", "InventorySystem", "Main", "Objects", "SceneManager", "TilemapManager", "Tools", "UI"]

def get_markdown_class_info(cls, all_classes_names):
    """Génère une chaîne Markdown pour une classe avec gestion de l'héritage."""
    name = cls.__name__
    # Création d'une ancre HTML pour le lien interactif
    md = f"### <a name='{name}'></a>Type de données : `{name}`\n\n"
    
    # Gestion de l'héritage
    parents = [b for b in cls.__bases__ if b.__name__ != 'object']
    if parents:
        parent_links = []
        for p in parents:
            p_name = p.__name__
            # Si le parent fait partie de notre scan, on crée un lien interne
            if p_name in all_classes_names:
                parent_links.append(f"[{p_name}](#{p_name})")
            else:
                parent_links.append(f"`{p_name}`")
        md += f"**Hérite de :** {', '.join(parent_links)}\n\n"

    # Attributs propres à cette classe (non hérités)
    md += "**Attributs (propres) :**\n"
    annotations = getattr(cls, '__annotations__', {})
    if annotations:
        for attr, t in annotations.items():
            type_name = getattr(t, '__name__', str(t))
            md += f"* {attr} : `{type_name}`\n"
    else:
        md += "* (Aucun attribut spécifique détecté)\n"
    
    # Méthodes propres à cette classe
    md += "\n**Méthodes (propres) :**\n"
    methods_found = False
    
    # On récupère toutes les méthodes définies directement dans le dictionnaire de la classe
    # pour éviter de lister les méthodes héritées des parents
    local_members = cls.__dict__
    
    for m_name, obj in local_members.items():
        if not m_name.startswith("__") and (inspect.isfunction(obj) or isinstance(obj, (staticmethod, classmethod))):
            methods_found = True
            # On récupère la fonction réelle pour la signature
            func = obj.__func__ if isinstance(obj, (staticmethod, classmethod)) else obj
            try:
                sig = inspect.signature(func)
                clean_sig = str(sig).replace('self, ', '').replace('self', '')
                md += f"* {m_name}{clean_sig}\n"
            except:
                md += f"* {m_name}(...)\n"
    
    if not methods_found:
        md += "* (Aucune méthode spécifique)\n"
    
    md += "\n---\n\n"
    return md

def main():
    full_markdown = "# Documentation Technique du Projet\n\n"
    
    # Premier passage pour lister toutes les classes (pour les liens interactifs)
    all_classes = {}
    for mod_name in modules_to_scan:
        try:
            module = importlib.import_module(mod_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == mod_name:
                    all_classes[name] = obj
        except: pass

    # Deuxième passage pour la génération du texte
    for mod_name in modules_to_scan:
        try:
            module = importlib.import_module(mod_name)
            full_markdown += f"## Fichier : {mod_name}.py\n\n"
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == mod_name:
                    full_markdown += get_markdown_class_info(obj, all_classes.keys())
        except Exception as e:
            full_markdown += f"**Erreur sur {mod_name}** : {e}\n\n"

    # Sauvegarde et Presse-papier
    with open("doc_projet.md", "w", encoding="utf-8") as f:
        f.write(full_markdown)
    
    try:
        import pyperclip
        pyperclip.copy(full_markdown)
        print("✅ Markdown généré et COPIÉ dans le presse-papier !")
    except ImportError:
        print("✅ Fichier 'doc_projet.md' créé (installez pyperclip pour la copie auto).")

if __name__ == "__main__":
    main()
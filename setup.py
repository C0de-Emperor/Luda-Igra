from cx_Freeze import setup, Executable

exe = [Executable("Main.py", target_name="Luda Igra.exe")] #, base="gui")]
build_exe_options = {"include_files": ["data"]}

# On appelle la fonction setup
setup(
    name = "Luda Igra",
    version = "1",
    description = "Jeu vidéo réalisé dans le cadre du cours de tronc commun informatique du S4",
    executables = exe,
    options={"build_exe": build_exe_options},
)
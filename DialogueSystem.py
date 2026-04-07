class Dialogue:
    currentDialogue:"Dialogue" = None

    def __init__(self, dialogueContent:str, dialogueTime:float):
        self.dialogueContent:str = dialogueContent
        self.dialogueTime:float = dialogueTime
    
    @staticmethod
    def changeCurrentDialogue(newDialogue):
        Dialogue.currentDialogue = newDialogue
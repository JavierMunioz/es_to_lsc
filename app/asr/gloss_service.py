class GlossService:
    def to_gloss(self, text: str) -> str:
        words = text.lower().split()
        ignore = {"a", "el", "la", "de", "que"}
        return " ".join(w.upper() for w in words if w not in ignore).replace("."," ")

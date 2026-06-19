import re

BANNED_WORDS = [
    # Overused power words
    "leverage", "leveraging", "leveraged",
    "utilize", "utilizing", "utilized",
    "synergy", "synergies", "synergistic",
    "dynamic", "innovative", "impactful",
    "passionate", "driven", "motivated",
    "results-driven", "detail-oriented",
    "thought leader", "game-changer",
    "cutting-edge", "best-in-class",
    "value-add", "deep dive", "bandwidth",
    "circle back", "move the needle",
    "paradigm", "ecosystem", "holistic",
    "seamless", "robust", "scalable solution",
    "proactive", "strategic", "transformative",
    # Filler skill descriptors
    "adept", "strong command of", "proficient",
    "proven track record", "highly skilled",
    "efficiently", "effectively", "exemplary", "commendable",
    "highly motivated", "dedicated", "ever-evolving", "tech-savvy",
    # AI verb clichés
    "delve", "embark", "foster", "spearhead", "champion",
    "cultivate", "aligns", "augment", "maximize", "facilitate",
    "streamline", "optimize", "landscape", "integration",
    "transformation", "methodology", "framework", "innovation",
    # Vague insight phrases
    "insights", "in-depth", "actionable insights",
    "data-driven decisions", "driving efficiency",
    # Filler phrases
    "working closely with", "committed to",
    "fast-paced environment"
]

def remove_em_dashes(text: str) -> str:
    text =  text.replace("\u2014","-")
    text =  text.replace("\u2013","-")
    text =  re.sub(r"\s*-\s*"," - ",text)
    return text

def remove_banned_words(text: str) -> str:
    for word in BANNED_WORDS:
        pattern = re.compile(re.escape(word),re.IGNORECASE)
        text = pattern.sub("",text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r" ([,\.\;\:])", r"\1", text)
    return text
def fix_punctuation(text: str) -> str:
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r" \.",".",text)
    text = re.sub(r" ,",",",text)
    return text.strip()

def clean(text: str) -> str:
    text = remove_em_dashes(text)
    text = remove_banned_words(text)
    text = fix_punctuation(text)

    return text 
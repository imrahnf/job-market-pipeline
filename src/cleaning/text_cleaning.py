# src/cleaning/text_cleaning.py
import re
import unicodedata

# normalie text
def normalize_text(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text)

# clean the description of the job posting
def clean_desc(desc: str) -> str:
    if not desc:
        return ""
    
    # normalize the text
    desc = normalize_text(desc)

    # remove weird whitespaces with regex
    desc = re.sub("\\s+", " ", desc).strip()

    return desc

# ensure consistency in the title
def clean_title(title: str) -> str:
    if not title:
        return ""
    
    title = normalize_text(title).strip()

    # lowercase the ttiele for parsing consistnency
    title = title.lower()

    # remove abbreviatoins
    title = title.replace("sr.", "senior")
    title = title.replace("jr.", "junior")

    return title.title() # capitalize again but properly

"""Writes src/data/vocabulary-synonyms.json: advanced synonyms of 100 basic English words.

The basic words and their synonyms follow a table the user shared (19/11/2026). Synonyms already in a
vocabulary file or in the synonym/antonym exercise, repeats across rows and five that the table pairs
with the wrong meaning (audition, subtracted, alleviated, singular, unanimous) were left out; "hush"
became "hushed". Basic words missing from the project (stupid, cruel, fake, all, some...) were added.
Levels, Vietnamese meanings, English definitions and examples are written for EnglishUp. Each example
contains the headword. The data lives in scripts/content/synonyms-*.txt: "## <topic>", then
"### <basic word>", then "word|pos|level|meaning|definition|example" lines.
Run: python scripts/create-synonyms.py
"""
import json
import pathlib
import re

VI = {
    "Size, quality and importance": "Kích thước, chất lượng, tầm quan trọng",
    "Feelings": "Cảm xúc",
    "Age, looks and wealth": "Tuổi tác, ngoại hình, giàu nghèo",
    "Mind and speed": "Trí tuệ và tốc độ",
    "Speaking and the senses": "Lời nói và giác quan",
    "Everyday actions": "Hành động thường ngày",
    "Likes and needs": "Yêu ghét và nhu cầu",
    "Describing things": "Miêu tả sự vật",
    "Character": "Tính cách",
    "Amount and frequency": "Số lượng và tần suất",
    "Common nouns": "Danh từ thông dụng",
}
LEVELS = {"A1", "A2", "B1", "B2", "C1", "C2"}
POS = {"adjective", "verb", "noun", "adverb", "determiner", "pronoun"}


def norm(word):
    return re.sub(r"^(a|an|the) ", "", word.lower().strip())


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    data = root / "src" / "data"
    taken = set()
    for path in data.glob("vocabulary*.json"):
        if path.name != "vocabulary-synonyms.json":
            taken |= {norm(w["word"]) for w in json.loads(path.read_text(encoding="utf-8"))}
    for path in data.glob("wordRelations-*.json"):
        for entry in json.loads(path.read_text(encoding="utf-8")):
            taken |= {norm(w["word"]) for w in [entry, *entry["synonyms"], *entry["antonyms"]]}
    out, topic, base, clashes = [], None, None, []
    for path in sorted((root / "scripts" / "content").glob("synonyms-*.txt")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("# "):
                continue
            if line.startswith("### "):
                base = line[4:].replace(" (person)", " (of a person)")
                continue
            if line.startswith("## "):
                topic = line[3:]
                assert topic in VI, topic
                continue
            word, pos, level, meaning, definition, example = line.split("|")
            assert pos in POS and level in LEVELS, line
            if norm(word) in taken:
                clashes.append(word)
                continue
            taken.add(norm(word))
            assert word.lower() in example.lower(), f"example misses the headword: {word}"
            if word != base:
                definition += f"; a synonym of {base}"
            out.append({
                "id": "v-syn-" + re.sub(r"[^a-z]+", "-", word.lower()).strip("-"),
                "word": word,
                "ipa": "",
                "pos": pos,
                "meaning": meaning,
                "definition": definition,
                "examples": [example],
                "level": level,
                "topic": f"Synonyms: {topic}",
            })
    assert not clashes, f"already in the project: {clashes}"
    assert len({w["id"] for w in out}) == len(out)
    (data / "vocabulary-synonyms.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {}
    for w in out:
        counts[w["topic"]] = counts.get(w["topic"], 0) + 1
    print(len(out), json.dumps(counts, ensure_ascii=False))
    print("topicVi:", json.dumps({f"Synonyms: {t}": f"Đồng nghĩa: {v}" for t, v in VI.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()

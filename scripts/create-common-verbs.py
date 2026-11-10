"""Writes src/data/vocabulary-verbs.json: common verbs from a study list the user shared (11/11/2026)
that the library did not have yet, added to the existing "Everyday verbs" topic.

Of 141 distinct words in the list, 96 were already in the library (any topic) and are left out.
The IPA is taken from the user's list (American transcriptions). The Vietnamese meanings follow the
verb sense, the definitions and examples are written for EnglishUp, and every example contains the
headword. Run: python scripts/create-common-verbs.py
"""
import json
import pathlib

TOPIC = "Everyday verbs"

# (word, IPA, level, Vietnamese meaning, English definition, example)
ITEMS = [
    ("should", "/ʃʊd/", "A1", "nên", "used to say what is the right or best thing to do", "You should drink more water every day."),
    ("can", "/kæn/", "A1", "có thể", "to be able to do something, or to be allowed to", "I can swim, but not very fast."),
    ("sort", "/sɔrt/", "A2", "phân loại, sắp xếp", "to put things into groups or into order", "Please sort the books by size."),
    ("state", "/steɪt/", "B1", "tuyên bố, nêu rõ", "to say or write something clearly and formally", "The report will state the main results."),
    ("inform", "/ɪnˈfɔrm/", "B1", "thông báo, báo cho biết", "to tell someone about a fact officially", "Please inform the teacher if you will be absent."),
    ("intend", "/ɪnˈtɛnd/", "B1", "có ý định, dự định", "to plan or mean to do something", "I intend to finish the course by June."),
    ("involve", "/ɪnˈvɑlv/", "B1", "bao gồm; liên quan, kéo vào", "to include something as a necessary part, or to make someone take part", "The job will involve some travel abroad."),
    ("kill", "/kɪl/", "A2", "giết; làm chết", "to cause a person, animal or plant to die", "Too much water can kill a cactus."),
    ("represent", "/ˌrɛprəˈzɛnt/", "B1", "đại diện cho; tượng trưng cho", "to speak or act for someone, or to stand for something", "Two students will represent our class at the meeting."),
    ("roll", "/roʊl/", "A2", "lăn; cuộn", "to move by turning over and over, or to make into a tube shape", "Help me roll the carpet before we move it."),
    ("set", "/sɛt/", "A2", "đặt; thiết lập; (mặt trời) lặn", "to put something in a place, to fix a time or rule, or to go down below the horizon", "Let's set a date for the next meeting."),
    ("claim", "/kleɪm/", "B1", "khẳng định; đòi (quyền lợi)", "to say that something is true, or to ask for something that is yours", "He likes to claim that he never gets lost."),
    ("commit", "/kəˈmɪt/", "B2", "phạm (lỗi, tội); cam kết", "to do something wrong or illegal, or to promise to give time or effort", "Few people commit crimes in this quiet town."),
    ("point", "/pɔɪnt/", "A2", "chỉ, trỏ", "to show where something is with your finger", "Please point to the word you do not know."),
    ("press", "/prɛs/", "A2", "nhấn, ấn", "to push something firmly", "Press the green button to start the machine."),
    ("regard", "/rəˈgɑrd/", "B2", "coi như, xem là", "to think of someone or something in a particular way", "Many people regard her as the best teacher in the school."),
    ("release", "/riˈlis/", "B1", "thả ra; phát hành", "to let someone or something go free, or to make a film or product available", "The band will release a new song next week."),
    ("base", "/beɪs/", "B1", "dựa trên, đặt nền tảng", "to use something as the main reason or starting point for something else", "We base our prices on the cost of materials."),
    ("burn", "/bɜrn/", "A2", "đốt cháy; bị bỏng, cháy", "to destroy or damage something with fire or heat", "Don't burn the toast this time."),
    ("shake", "/ʃeɪk/", "A2", "lắc, rung", "to move something quickly up and down or from side to side", "Shake the bottle before you open it."),
    ("complain", "/kəmˈpleɪn/", "A2", "phàn nàn", "to say that you are not happy about something", "Customers often complain about slow delivery."),
    ("concern", "/kənˈsɜrn/", "B2", "liên quan đến; làm lo lắng", "to be about or affect someone, or to make someone worried", "This change does not concern first-year students."),
    ("consist", "/kənˈsɪst/", "B1", "gồm có", "to be made of particular parts (consist of)", "The test will consist of three short sections."),
    ("contact", "/ˈkɑnˌtækt/", "A2", "liên lạc, liên hệ", "to call, write to or email someone", "Please contact us if you have any questions."),
    ("care", "/kɛr/", "A2", "quan tâm; chăm sóc (care for)", "to feel that something is important, or to look after someone", "Good doctors care about their patients."),
    ("charge", "/ʧɑrʤ/", "B1", "tính phí; sạc (pin)", "to ask for money for something, or to put electricity into a battery", "Some hotels charge extra for breakfast."),
    ("exist", "/ɪgˈzɪst/", "B1", "tồn tại", "to be real or present", "Do you think life could exist on other planets?"),
    ("express", "/ɪkˈsprɛs/", "B1", "bày tỏ, diễn đạt", "to show a feeling or opinion in words or actions", "Children often express their feelings through drawing."),
    ("extend", "/ɪkˈstɛnd/", "B1", "kéo dài; mở rộng", "to make something longer or bigger", "The library will extend its opening hours during exams."),
    ("fail", "/feɪl/", "A2", "thất bại; trượt (kỳ thi)", "to not succeed in doing something", "If you don't study, you may fail the test."),
    ("fasten", "/ˈfæsən/", "B1", "buộc chặt, cài (dây an toàn)", "to close or join something so that it stays firmly in place", "Please fasten your seatbelt before we leave."),
    ("feed", "/fid/", "A2", "cho ăn", "to give food to a person or an animal", "It is my job to feed the cat every morning."),
    ("fight", "/faɪt/", "A2", "đánh nhau; chiến đấu, đấu tranh", "to use force against someone, or to try hard to stop something bad", "Doctors fight hard to save every patient."),
    ("fill", "/fɪl/", "A2", "đổ đầy, lấp đầy", "to make something full", "Please fill the jug with cold water."),
    ("fit", "/fɪt/", "A2", "vừa (kích cỡ); phù hợp", "to be the right size or shape for someone or something", "These shoes don't fit me any more."),
    ("fold", "/foʊld/", "A2", "gấp, gập", "to bend something so that one part lies on another", "Fold the paper in half."),
    ("apply", "/əˈplaɪ/", "B1", "nộp đơn; áp dụng", "to ask formally for something, or to use a rule or method", "You can apply the same rule to other verbs."),
    ("argue", "/ˈɑrgju/", "B1", "tranh cãi; lập luận", "to disagree angrily, or to give reasons for an opinion", "My brothers often argue about football."),
    ("attack", "/əˈtæk/", "B1", "tấn công", "to try to hurt or damage someone or something", "Some dogs attack when they feel afraid."),
    ("hide", "/haɪd/", "A2", "trốn; giấu", "to go or put something where others cannot see or find it", "The children like to hide behind the curtains."),
    ("hit", "/hɪt/", "A2", "đánh, đập; va vào", "to touch someone or something hard with your hand or an object", "Try to hit the ball over the net."),
    ("deny", "/dɪˈnaɪ/", "B1", "phủ nhận; từ chối", "to say that something is not true, or to refuse to give something", "He continued to deny that he broke the window."),
    ("destroy", "/dɪˈstrɔɪ/", "B1", "phá hủy", "to damage something so badly that it cannot be used", "The storm could destroy the old bridge."),
    ("die", "/daɪ/", "A2", "chết; (cây) héo chết", "to stop living", "Plants die without enough light."),
    ("discuss", "/dɪˈskʌs/", "A2", "thảo luận, bàn bạc", "to talk about something with other people", "Let's discuss the plan after lunch."),
]


def main():
    root = pathlib.Path(__file__).resolve().parent.parent / "src" / "data"
    existing = {w["word"].lower() for f in ["vocabulary", "vocabulary-it", "vocabulary-phrasal", "vocabulary-collocations"]
                for w in json.loads((root / f"{f}.json").read_text(encoding="utf-8"))}
    out = []
    for word, ipa, level, meaning, definition, example in ITEMS:
        assert word not in existing, f"{word} is already in the library"
        assert word in example.lower() and ipa.startswith("/") and ipa.endswith("/"), word
        out.append({
            "id": f"v-verb-{word}", "word": word, "ipa": ipa,
            "pos": "modal verb" if word in ("should", "can") else "verb",
            "meaning": meaning, "definition": definition, "examples": [example], "level": level, "topic": TOPIC,
        })
    assert len({w["word"] for w in out}) == len(out) == 45
    (root / "vocabulary-verbs.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "verbs:", {lv: sum(1 for w in out if w["level"] == lv) for lv in ["A1", "A2", "B1", "B2"]})


if __name__ == "__main__":
    main()

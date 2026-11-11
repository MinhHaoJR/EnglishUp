"""Writes src/data/roadmaps.json, the seed for the learning paths (one per step from A1 to C2).

Each path has four stages; each stage a goal and tasks that open a practice page at a level. Listening, reading,
speaking and writing have lessons at every level; translation sentences exist at A2-B2 only, so the
higher paths use B2 sentences for translation and say so. Run: python scripts/create-roadmaps.py
"""
import json
import pathlib


def task(skill, level, vi, en, category=None):
    """A practice step; a grammar race may name one grammar point (a quiz category)."""
    return {"skill": skill, "level": level, **({"category": category} if category else {}), "vi": vi, "en": en}


def stage(title, goal, tasks):
    return {"title": {"vi": title[0], "en": title[1]}, "goal": {"vi": goal[0], "en": goal[1]}, "tasks": tasks}


PATHS = [
    ("A1", "A2", 8,
     ("Từ A1 lên A2: nền móng giao tiếp hằng ngày", "A1 to A2: the basics of everyday English"),
     ("Dành cho người mới bắt đầu: học từ vựng đời sống, các thì cơ bản và đọc, nghe những đoạn ngắn.",
      "For beginners: everyday words, the basic tenses, and short texts and dialogues."),
     [
         stage(("Từ vựng đời sống", "Everyday words"),
               ("Nắm khoảng 200 từ về gia đình, nhà cửa, đồ ăn và thời gian.",
                "Learn about 200 words for family, home, food and time."),
               [task("vocabulary", "A1", "Học 2 cụm từ vựng chủ đề Đời sống và ôn thẻ mỗi ngày.",
                     "Study two Daily life word clusters and review the cards every day."),
                task("wordgame", "A1", "Chơi Đua từ vựng A1, mục tiêu 100 điểm.", "Play the A1 vocabulary race; aim for 100 points."),
                task("relations", "A1", "Học 12 cặp đồng nghĩa – trái nghĩa A1.", "Learn the 12 A1 synonym and antonym sets.")]),
         stage(("Câu đơn và các thì cơ bản", "Simple sentences and basic tenses"),
               ("Dùng đúng hiện tại đơn, hiện tại tiếp diễn và quá khứ đơn.",
                "Use the present simple, present continuous and past simple correctly."),
               [task("grammar", "A1", "Học nhóm cấu trúc Thói quen, sở thích, khả năng.", "Study the Habits, likes and abilities patterns."),
                task("grammargame", "A1", "Đua ngữ pháp A1 dạng Thì động từ.", "Play the A1 grammar race on tenses.", "tense"),
                task("grammargame", "A1", "Đua ngữ pháp A1 với mọi dạng: mạo từ, giới từ, đại từ.", "Play the A1 grammar race on every point: articles, prepositions, pronouns.")]),
         stage(("Nghe và đọc đoạn ngắn", "Short texts and dialogues"),
               ("Hiểu hội thoại và bài đọc ngắn về chủ đề quen thuộc.",
                "Understand short dialogues and texts on familiar topics."),
               [task("listening", "A2", "Nghe một bài hội thoại A2, nghe lại từng câu rồi trả lời.", "Listen to an A2 dialogue line by line, then answer."),
                task("reading", "A2", "Đọc một bài A2 và bấm vào từ mới để tra nghĩa.", "Read an A2 text and tap new words to look them up."),
                task("speaking", "A2", "Đọc nhại theo mẫu 2 bài nói A2.", "Shadow two A2 speaking models.")]),
         stage(("Viết và tự kiểm tra", "Write and check your level"),
               ("Viết đoạn ngắn về bản thân và kiểm tra lại trình độ.",
                "Write a short paragraph about yourself and check your level again."),
               [task("writing", "A2", "Viết một bài A2 theo đề và sửa theo nhận xét.", "Write an A2 task and revise it with the feedback."),
                task("assistant", "A2", "Hỏi trợ giảng AI về một lỗi bạn hay mắc.", "Ask the AI tutor about a mistake you often make."),
                task("placement", "A2", "Làm lại bài kiểm tra trình độ, mục tiêu đạt A2.", "Retake the level test; aim for A2.")]),
     ]),
    ("A2", "B1", 10,
     ("Từ A2 lên B1: tự tin trong tình huống quen thuộc", "A2 to B1: confident in familiar situations"),
     ("Mở rộng vốn từ du lịch, công việc, mua sắm; nắm thì hoàn thành, so sánh và viết email ngắn.",
      "Widen your words for travel, work and shopping; master the perfect tenses, comparison and short emails."),
     [
         stage(("Mở rộng vốn từ", "Widen your vocabulary"),
               ("Học các chủ đề Du lịch, Công việc, Mua sắm ở trình độ A2.", "Learn Travel, Work and Shopping words at A2."),
               [task("vocabulary", "A2", "Học 3 cụm từ vựng A2 và ôn thẻ đến hạn mỗi ngày.", "Study three A2 word clusters and review due cards daily."),
                task("relations", "A2", "Học 12 cặp đồng nghĩa – trái nghĩa A2.", "Learn the 12 A2 synonym and antonym sets."),
                task("wordgame", "A2", "Đua từ vựng A2, mục tiêu 150 điểm.", "Play the A2 vocabulary race; aim for 150 points.")]),
         stage(("Thì hoàn thành và so sánh", "Perfect tenses and comparison"),
               ("Phân biệt quá khứ đơn với hiện tại hoàn thành; dùng đúng so sánh hơn, so sánh nhất.",
                "Tell the past simple from the present perfect; use comparatives and superlatives."),
               [task("grammar", "A2", "Học nhóm Thời gian và thì hoàn thành, nhóm So sánh và lựa chọn.", "Study the Time and perfect tenses and the Comparing and preferring patterns."),
                task("grammargame", "A2", "Đua ngữ pháp A2 dạng Thì động từ.", "Play the A2 grammar race on tenses.", "tense"),
                task("grammargame", "A2", "Đua ngữ pháp A2 dạng So sánh và Từ chỉ lượng.", "Play the A2 grammar race on comparison and quantifiers.")]),
         stage(("Nghe – nói về kinh nghiệm", "Talk about experiences"),
               ("Nghe hiểu và kể lại kinh nghiệm, kế hoạch bằng câu đơn giản.", "Understand and retell experiences and plans in simple sentences."),
               [task("listening", "B1", "Nghe một bài B1, ghi lại 3 ý chính.", "Listen to a B1 dialogue and note three main points."),
                task("speaking", "B1", "Nói tự do về một chuyến đi đáng nhớ.", "Talk freely about a trip you remember."),
                task("translation", "A2", "Dịch 10 câu Việt → Anh và so sánh với đáp án.", "Translate ten sentences from Vietnamese and compare.")]),
         stage(("Viết email và kiểm tra", "Write emails and check"),
               ("Viết email 80–120 từ có mở đầu, nội dung và kết thúc rõ ràng.", "Write an 80–120-word email with a clear opening, body and close."),
               [task("writing", "B1", "Viết một email B1 theo đề và đếm số từ.", "Write a B1 email task within the word count."),
                task("grammargame", "B1", "Đua ngữ pháp B1 mọi dạng, mục tiêu 150 điểm.", "Play the B1 grammar race on every point; aim for 150 points."),
                task("placement", "B1", "Làm lại bài kiểm tra trình độ, mục tiêu đạt B1.", "Retake the level test; aim for B1.")]),
     ]),
    ("B1", "B2", 12,
     ("Từ B1 lên B2: diễn đạt ý kiến rõ ràng", "B1 to B2: state your views clearly"),
     ("Từ vựng học thuật và công việc, câu điều kiện, bị động, mệnh đề quan hệ, đọc tìm bằng chứng và viết nghị luận.",
      "Academic and work vocabulary, conditionals, the passive, relative clauses, reading for evidence and opinion essays."),
     [
         stage(("Từ vựng học thuật và công việc", "Academic and work vocabulary"),
               ("Học từ B2 về công nghệ, môi trường, giáo dục và công việc.", "Learn B2 words for technology, the environment, education and work."),
               [task("vocabulary", "B2", "Học 3 cụm từ vựng B2, mỗi ngày ôn thẻ đến hạn.", "Study three B2 word clusters; review due cards daily."),
                task("relations", "B1", "Học 12 cặp đồng nghĩa – trái nghĩa B1 và chú ý ghi chú cách dùng.", "Learn the 12 B1 synonym and antonym sets and their usage notes."),
                task("translation", "B1", "Dịch câu B1 cả hai chiều.", "Translate B1 sentences both ways.")]),
         stage(("Điều kiện, bị động, mệnh đề quan hệ", "Conditionals, passive, relative clauses"),
               ("Dùng đúng câu điều kiện loại 1–3, câu bị động và mệnh đề quan hệ.", "Use conditionals 1–3, the passive and relative clauses correctly."),
               [task("grammar", "B1", "Học nhóm Nối câu và nhóm Nguyên nhân – kết quả.", "Study the Linking and the Cause and effect patterns."),
                task("grammargame", "B1", "Đua ngữ pháp B1 dạng Câu điều kiện.", "Play the B1 grammar race on conditionals.", "conditional"),
                task("grammargame", "B2", "Đua ngữ pháp B2 dạng Câu bị động và Mệnh đề quan hệ.", "Play the B2 grammar race on the passive and relative clauses.")]),
         stage(("Đọc hiểu và nghe ý chính", "Reading and listening for the main idea"),
               ("Tìm ý chính và câu làm bằng chứng trong bài B2.", "Find the main idea and the evidence in B2 texts."),
               [task("reading", "B2", "Đọc một bài B2, trả lời và đối chiếu câu làm bằng chứng.", "Read a B2 text, answer and check the evidence."),
                task("listening", "B2", "Nghe một bài B2 ở tốc độ thường, bật lời thoại sau khi trả lời.", "Listen to a B2 dialogue at normal speed; open the transcript after answering."),
                task("speaking", "B2", "Trình bày ý kiến trong 1 phút với bài nói B2.", "Give a one-minute opinion with a B2 speaking task.")]),
         stage(("Viết bài nêu ý kiến", "Write an opinion essay"),
               ("Viết bài 150–200 từ có luận điểm, ví dụ và từ nối.", "Write 150–200 words with a position, examples and linking words."),
               [task("writing", "B2", "Viết một bài nêu ý kiến B2 và sửa theo nhận xét.", "Write a B2 opinion task and revise it."),
                task("assistant", "B2", "Nhờ trợ giảng AI giải thích khác nhau giữa although, despite và however.", "Ask the AI tutor how although, despite and however differ."),
                task("placement", "B2", "Làm lại bài kiểm tra trình độ, mục tiêu đạt B2.", "Retake the level test; aim for B2.")]),
     ]),
    ("B2", "C1", 16,
     ("Từ B2 lên C1: chính xác và tự nhiên", "B2 to C1: precise and natural"),
     ("Từ vựng lập luận, đảo ngữ, điều kiện hỗn hợp, thức giả định và diễn đạt có sắc thái. Bài dịch câu dùng câu B2.",
      "Vocabulary for argument, inversion, mixed conditionals, the subjunctive and nuance. Translation uses B2 sentences."),
     [
         stage(("Từ vựng lập luận", "Vocabulary for argument"),
               ("Học từ C1 để nêu luận điểm, bằng chứng và mức độ chắc chắn.", "Learn C1 words to state claims, evidence and certainty."),
               [task("vocabulary", "C1", "Học các cụm từ vựng C1 chủ đề Ôn thi nâng cao.", "Study the C1 word clusters on advanced exam topics."),
                task("relations", "C1", "Học 12 cặp đồng nghĩa – trái nghĩa C1.", "Learn the 12 C1 synonym and antonym sets."),
                task("wordgame", "C1", "Đua từ vựng C1, mục tiêu 150 điểm.", "Play the C1 vocabulary race; aim for 150 points.")]),
         stage(("Đảo ngữ và câu phức", "Inversion and complex sentences"),
               ("Dùng đảo ngữ, điều kiện hỗn hợp và thức giả định trong văn trang trọng.", "Use inversion, mixed conditionals and the subjunctive in formal writing."),
               [task("grammargame", "C1", "Đua ngữ pháp C1 dạng Đảo ngữ.", "Play the C1 grammar race on inversion.", "inversion"),
                task("grammargame", "C1", "Đua ngữ pháp C1 dạng Câu điều kiện và Dạng động từ.", "Play the C1 grammar race on conditionals and verb forms."),
                task("grammar", "B2", "Ôn toàn bộ 100 cấu trúc ở chế độ luyện điền chỗ trống.", "Review all 100 patterns in fill-the-blank practice.")]),
         stage(("Đọc và nghe chuyên sâu", "Read and listen in depth"),
               ("Đọc, nghe bài khó nhất hiện có và tóm tắt bằng lời của bạn.", "Read and listen to the hardest lessons available and summarise them in your own words."),
               [task("reading", "C1", "Đọc một bài C1, tóm tắt bằng 3 câu không nhìn bài.", "Read a C1 text and summarise it in three sentences without looking."),
                task("listening", "C1", "Nghe một bài C1 ở tốc độ 1,25× rồi chép lại một câu.", "Listen to a C1 discussion at 1.25× and write one line down."),
                task("assistant", "C1", "Hỏi trợ giảng AI cách dùng một cấu trúc đảo ngữ trong bài viết.", "Ask the AI tutor how to use an inversion in your writing.")]),
         stage(("Viết trang trọng và kiểm tra", "Formal writing and check"),
               ("Viết bài 200–250 từ dùng ít nhất một câu đảo ngữ và một câu bị động.", "Write 200–250 words with at least one inversion and one passive."),
               [task("writing", "C1", "Viết một bài nghị luận C1 ở văn phong trang trọng.", "Write a C1 opinion task in a formal style."),
                task("speaking", "C1", "Nói tự do 2 phút về một chủ đề C1.", "Talk freely for two minutes on a C1 topic."),
                task("placement", "C1", "Làm lại bài kiểm tra trình độ, mục tiêu đạt C1.", "Retake the level test; aim for C1.")]),
     ]),
    ("C1", "C2", 16,
     ("Từ C1 lên C2: thành thạo sắc thái", "C1 to C2: mastery of nuance"),
     ("Từ vựng C2, cấu trúc trang trọng hiếm gặp, liên từ học thuật và tự sửa lỗi. Bài dịch câu dùng câu B2.",
      "C2 vocabulary, rare formal structures, academic connectors and self-correction. Translation uses B2 sentences."),
     [
         stage(("Từ vựng C2", "C2 vocabulary"),
               ("Học từ C2 và phân biệt sắc thái của các từ gần nghĩa.", "Learn C2 words and the nuances between near-synonyms."),
               [task("vocabulary", "C2", "Học toàn bộ từ vựng C2 và ôn thẻ đến hạn.", "Study all C2 words and review due cards."),
                task("relations", "C2", "Học 12 cặp đồng nghĩa – trái nghĩa C2 và ghi chú cách dùng.", "Learn the 12 C2 synonym and antonym sets and their usage notes."),
                task("wordgame", "C2", "Đua từ vựng C2, mục tiêu 200 điểm.", "Play the C2 vocabulary race; aim for 200 points.")]),
         stage(("Cấu trúc trang trọng", "Formal structures"),
               ("Dùng đảo ngữ, thức giả định và liên từ trang trọng (albeit, notwithstanding).", "Use inversion, the subjunctive and formal connectors (albeit, notwithstanding)."),
               [task("grammargame", "C2", "Đua ngữ pháp C2 dạng Đảo ngữ.", "Play the C2 grammar race on inversion.", "inversion"),
                task("grammargame", "C2", "Đua ngữ pháp C2 dạng Liên từ và từ nối.", "Play the C2 grammar race on linking words.", "connector"),
                task("grammargame", "C1", "Đua ngữ pháp C1 mọi dạng, mục tiêu 200 điểm.", "Play the C1 grammar race on every point; aim for 200 points.")]),
         stage(("Đọc, nghe và thảo luận", "Read, listen and discuss"),
               ("Phân tích lập luận và sắc thái trong bài khó nhất hiện có.", "Analyse argument and nuance in the hardest lessons available."),
               [task("reading", "C2", "Đọc một bài C2 và chỉ ra giọng điệu, mục đích của tác giả.", "Read a C2 text and name the writer's tone and purpose."),
                task("listening", "C2", "Nghe một bài C2 không xem lời thoại, chú ý hàm ý của người nói, rồi kiểm tra từng câu.", "Listen to a C2 discussion without the transcript, notice what the speakers imply, then check each line."),
                task("assistant", "C2", "Thảo luận với trợ giảng AI về sắc thái của hai từ gần nghĩa.", "Discuss the nuance of two near-synonyms with the AI tutor.")]),
         stage(("Viết và tự đánh giá", "Write and assess yourself"),
               ("Viết bài 250 từ chính xác, đa dạng cấu trúc và tự sửa lỗi.", "Write 250 precise, varied words and correct your own mistakes."),
               [task("writing", "C2", "Viết một bài C2 ở văn phong học thuật, dùng ít nhất 3 cấu trúc C1–C2.", "Write a C2 task in an academic style with at least three C1–C2 structures."),
                task("translation", "B2", "Dịch câu B2 sang tiếng Việt tự nhiên, rồi dịch ngược lại.", "Translate B2 sentences into natural Vietnamese, then back."),
                task("placement", "C2", "Làm lại bài kiểm tra trình độ, mục tiêu đạt C2.", "Retake the level test; aim for C2.")]),
     ]),
]


def main():
    out = []
    for start, end, weeks, title, summary, stages in PATHS:
        path_id = f"rm-{start.lower()}-{end.lower()}"
        for s, st in enumerate(stages, 1):
            st["id"] = f"s{s}"
            for t, tk in enumerate(st["tasks"], 1):
                tk["id"] = f"s{s}t{t}"
        out.append({
            "id": path_id, "from": start, "to": end, "weeks": weeks,
            "title": {"vi": title[0], "en": title[1]}, "summary": {"vi": summary[0], "en": summary[1]},
            "stages": [{"id": st["id"], **{k: v for k, v in st.items() if k != "id"}} for st in stages],
        })
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "roadmaps.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(out)} paths, {sum(len(t['tasks']) for p in out for t in p['stages'])} tasks")


if __name__ == "__main__":
    main()

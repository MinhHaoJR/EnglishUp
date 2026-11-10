"""Writes src/data/tenses.json: the 12 English tenses plus "be going to", for the grammar page.

Checked against a common Vietnamese summary of the 12 tenses (11/11/2026); each tense has its form (affirmative, negative, question), its uses with an example, signal words, a tip
on a common mistake, and three fill-in-the-blank checks with one grammatical answer. Explanations are in
Vietnamese and English for the interface; examples are original English. Run: python scripts/create-tenses.py
"""
import json
import pathlib


def use(vi, en, example):
    return {"vi": vi, "en": en, "example": example}


def check(sentence, answer, wrong, explanation):
    return {"sentence": sentence, "options": [answer, *wrong], "answer": answer, "explanation": explanation}


TENSES = [
    ("present-simple", "present", "A1", ("Hiện tại đơn", "Present simple"),
     (["S + V(s/es) + O", "S + am/is/are + N/Adj"],
      ["S + do/does + not + V", "S + am/is/are + not + N/Adj"],
      ["Do/Does + S + V?", "Am/Is/Are + S + N/Adj?"]),
     [use("Thói quen, việc lặp đi lặp lại", "Habits and repeated actions", "I walk to school every day."),
      use("Sự thật hiển nhiên, chân lý", "Facts and general truths", "Water boils at 100 degrees Celsius."),
      use("Lịch trình, thời gian biểu cố định", "Fixed timetables", "The train leaves at seven in the morning.")],
     ["always", "usually", "often", "sometimes", "never", "every day", "on Mondays"],
     ("Với he/she/it, động từ thêm -s/-es. Sau does, động từ trở về nguyên mẫu: Does she like tea? (không nói Does she likes).",
      "With he/she/it, add -s/-es. After does the verb goes back to its base form: Does she like tea? (not Does she likes)."),
     [check("She usually ___ to work by bus.", "goes", ["go", "going", "gone"], "Thói quen (usually), chủ ngữ she → goes."),
      check("Water ___ at 100 degrees Celsius.", "boils", ["boil", "boiling", "is boil"], "Sự thật hiển nhiên → hiện tại đơn; water là danh từ số ít → boils."),
      check("___ your brother play the guitar?", "Does", ["Do", "Is", "Has"], "Câu hỏi hiện tại đơn với your brother (he) → Does + S + V.")]),
    ("present-continuous", "present", "A1", ("Hiện tại tiếp diễn", "Present continuous"),
     (["S + am/is/are + V-ing"], ["S + am/is/are + not + V-ing"], ["Am/Is/Are + S + V-ing?"]),
     [use("Việc đang diễn ra lúc nói", "Actions happening now", "She is cooking dinner now."),
      use("Việc tạm thời, diễn ra xung quanh thời điểm nói", "Temporary actions around the time of speaking", "I am staying with my aunt this week."),
      use("Kế hoạch tương lai đã sắp xếp", "Arranged future plans", "We are meeting the teacher tomorrow afternoon.")],
     ["now", "right now", "at the moment", "Look!", "Listen!", "this week", "today"],
     ("Động từ chỉ trạng thái (know, like, want, believe, need) thường không dùng tiếp diễn: nói I know, không nói I am knowing.",
      "State verbs (know, like, want, believe, need) are rarely continuous: say I know, not I am knowing."),
     [check("Listen! Someone ___ at the door.", "is knocking", ["knock", "are knocking", "knocking"], "Listen! báo hiệu việc đang xảy ra → is knocking."),
      check("I ___ with my aunt this week while my parents are away.", "am staying", ["is staying", "are staying", "staying"], "Việc tạm thời (this week), chủ ngữ I → am staying."),
      check("They ___ TV at the moment; they are doing homework.", "aren't watching", ["isn't watching", "not watching", "aren't watch"], "Phủ định hiện tại tiếp diễn: are + not + V-ing.")]),
    ("present-perfect", "present", "A2", ("Hiện tại hoàn thành", "Present perfect"),
     (["S + have/has + V3/ed"], ["S + have/has + not + V3/ed"], ["Have/Has + S + V3/ed?"]),
     [use("Trải nghiệm tính đến hiện tại", "Experiences up to now", "I have visited Hue twice."),
      use("Việc vừa xảy ra, còn ảnh hưởng tới hiện tại", "Past actions with a result now", "She has lost her keys, so she can't get in."),
      use("Kéo dài từ quá khứ đến nay", "Situations that started in the past and continue", "We have lived here since 2019.")],
     ["ever", "never", "already", "yet", "just", "since", "for", "so far", "recently"],
     ("Không dùng với thời điểm quá khứ cụ thể (yesterday, last year, in 2010): nói I saw him yesterday, không nói I have seen him yesterday.",
      "Do not use it with a finished past time (yesterday, last year, in 2010): say I saw him yesterday, not I have seen him yesterday."),
     [check("I ___ this film three times.", "have seen", ["has seen", "have saw", "having seen"], "Trải nghiệm tính đến nay → have + V3 (see → seen)."),
      check("She ___ here since 2020.", "has worked", ["have worked", "has work", "working"], "Since + mốc thời gian → hiện tại hoàn thành; she → has."),
      check("Have you ever ___ to Da Lat?", "been", ["be", "being", "was"], "Have you ever + V3; trải nghiệm đi đâu đó dùng been.")]),
    ("present-perfect-continuous", "present", "B1", ("Hiện tại hoàn thành tiếp diễn", "Present perfect continuous"),
     (["S + have/has + been + V-ing"], ["S + have/has + not + been + V-ing"], ["Have/Has + S + been + V-ing?"]),
     [use("Kéo dài đến hiện tại, nhấn mạnh quá trình", "Actions continuing up to now, stressing the duration", "I have been learning English for three years."),
      use("Vừa dừng lại, còn để lại dấu hiệu", "Recent actions with visible signs", "Her eyes are red; she has been crying.")],
     ["for", "since", "all day", "all morning", "so far", "how long", "lately", "recently"],
     ("So với hiện tại hoàn thành: thì này nhấn mạnh thời gian kéo dài (I have been reading for two hours), còn hiện tại hoàn thành nhấn mạnh kết quả (I have read three chapters).",
      "Compared with the present perfect, it stresses how long (I have been reading for two hours) rather than the result (I have read three chapters)."),
     [check("It ___ all morning, so the roads are wet.", "has been raining", ["has been rain", "have been raining", "has raining"], "Kéo dài cả buổi sáng, còn dấu hiệu (đường ướt) → has been + V-ing."),
      check("How long ___ you been waiting?", "have", ["has", "are", "did"], "How long + have/has + S + been + V-ing; you → have."),
      check("She is tired because she ___ for ten hours.", "has been driving", ["have been driving", "has been drive", "is drive"], "Việc kéo dài đến hiện tại gây ra mệt → has been + V-ing.")]),
    ("past-simple", "past", "A1", ("Quá khứ đơn", "Past simple"),
     (["S + V2/ed", "S + was/were + N/Adj"], ["S + did not + V", "S + was/were + not + N/Adj"], ["Did + S + V?", "Was/Were + S + N/Adj?"]),
     [use("Việc đã xong tại một thời điểm xác định", "Finished actions at a known past time", "I visited my grandparents last weekend."),
      use("Chuỗi hành động nối tiếp trong quá khứ", "A sequence of past actions", "He opened the door, turned on the light and sat down."),
      use("Thói quen trong quá khứ", "Past habits", "As a child, she walked to school every day.")],
     ["yesterday", "last week", "last year", "ago", "in 2010", "when I was a child"],
     ("Sau did và didn't, động từ trở về nguyên mẫu: Did you go? (không nói Did you went?).",
      "After did and didn't the verb is in its base form: Did you go? (not Did you went?)."),
     [check("We ___ to the beach last summer.", "went", ["go", "goes", "going"], "Last summer → quá khứ đơn; go → went."),
      check("She ___ at home yesterday evening.", "was", ["were", "be", "is been"], "Quá khứ của be với she → was."),
      check("___ you call your mother last night?", "Did", ["Do", "Have", "Were"], "Câu hỏi quá khứ đơn với động từ thường → Did + S + V.")]),
    ("past-continuous", "past", "A2", ("Quá khứ tiếp diễn", "Past continuous"),
     (["S + was/were + V-ing"], ["S + was/were + not + V-ing"], ["Was/Were + S + V-ing?"]),
     [use("Đang diễn ra tại một thời điểm trong quá khứ", "In progress at a past moment", "At 8 p.m. yesterday, I was having dinner."),
      use("Đang diễn ra thì bị việc khác cắt ngang", "Interrupted by another action", "I was walking home when it started to rain."),
      use("Hai việc diễn ra song song", "Two actions at the same time", "While she was cooking, he was setting the table.")],
     ["at that time", "at 8 p.m. yesterday", "while", "when", "all evening"],
     ("Việc dài dùng quá khứ tiếp diễn, việc ngắn chen vào dùng quá khứ đơn: I was reading when the phone rang.",
      "Use it for the longer action and the past simple for the short one that interrupts: I was reading when the phone rang."),
     [check("At nine o'clock last night, we ___ a film together.", "were watching", ["was watching", "were watch", "watching"], "Đang diễn ra tại một thời điểm quá khứ; we → were + V-ing."),
      check("I ___ home when it started to rain.", "was walking", ["were walking", "was walk", "walking"], "Việc dài bị cắt ngang; I → was + V-ing."),
      check("While she ___, the baby fell asleep.", "was singing", ["were singing", "is singing", "singing"], "While + quá khứ tiếp diễn cho việc đang diễn ra.")]),
    ("past-perfect", "past", "B1", ("Quá khứ hoàn thành", "Past perfect"),
     (["S + had + V3/ed"], ["S + had not + V3/ed"], ["Had + S + V3/ed?"]),
     [use("Xảy ra trước một việc hoặc mốc khác trong quá khứ", "Before another past action or time", "When we arrived, the film had already started."),
      use("Giải thích nguyên nhân của một tình huống trong quá khứ", "The reason for a past situation", "She was upset because she had lost her bag.")],
     ["before", "after", "by the time", "already", "when + quá khứ đơn"],
     ("Chỉ cần dùng khi muốn nói rõ việc nào xảy ra trước. Nếu kể theo đúng thứ tự thì quá khứ đơn là đủ.",
      "Use it only when you need to show which action came first. Telling events in order, the past simple is enough."),
     [check("By the time we got to the station, the train ___.", "had left", ["had leave", "has leaving", "leaving"], "Việc xảy ra trước một mốc quá khứ → had + V3."),
      check("She didn't come because she ___ her ankle.", "had hurt", ["had hurted", "has hurting", "hurting"], "Nguyên nhân xảy ra trước → had + V3 (hurt là bất quy tắc)."),
      check("___ you finished your homework before dinner?", "Had", ["Has", "Does", "Were"], "Câu hỏi quá khứ hoàn thành → Had + S + V3.")]),
    ("past-perfect-continuous", "past", "B2", ("Quá khứ hoàn thành tiếp diễn", "Past perfect continuous"),
     (["S + had been + V-ing"], ["S + had not been + V-ing"], ["Had + S + been + V-ing?"]),
     [use("Kéo dài cho đến một mốc trong quá khứ", "Lasting up to a past moment", "I had been waiting for an hour when she arrived."),
      use("Nguyên nhân kéo dài của một tình trạng quá khứ", "The ongoing cause of a past situation", "The ground was wet because it had been raining.")],
     ["for", "since", "until then", "how long", "before", "by the time"],
     ("Giống hiện tại hoàn thành tiếp diễn nhưng lùi về quá khứ: mốc kết thúc là một thời điểm đã qua.",
      "Like the present perfect continuous, shifted to the past: the end point is a moment that has passed."),
     [check("They ___ for two hours when the bus finally came.", "had been waiting", ["had been wait", "has been waiting", "had waiting"], "Kéo dài đến một mốc quá khứ → had been + V-ing."),
      check("His eyes were red because he ___ all night.", "had been studying", ["had been study", "has been studying", "had studying"], "Nguyên nhân kéo dài trước mốc quá khứ → had been + V-ing."),
      check("How long ___ she been living there before she moved?", "had", ["has", "did", "was"], "Câu hỏi quá khứ hoàn thành tiếp diễn → had + S + been + V-ing.")]),
    ("future-simple", "future", "A1", ("Tương lai đơn", "Future simple (will)"),
     (["S + will + V"], ["S + will not (won't) + V"], ["Will + S + V?"]),
     [use("Quyết định ngay lúc nói", "Decisions made at the moment of speaking", "It's cold. I will close the window."),
      use("Dự đoán không có căn cứ rõ ràng, theo ý kiến cá nhân", "Predictions without clear evidence, based on opinion", "I think it will rain tomorrow."),
      use("Lời hứa, lời đề nghị giúp đỡ", "Promises and offers", "I will help you with your homework.")],
     ["tomorrow", "next week", "soon", "I think", "probably", "in 2030"],
     ("Sau will luôn là động từ nguyên mẫu: She will come (không nói She will comes).",
      "After will, always use the base form: She will come (not She will comes)."),
     [check("The phone is ringing. I ___ it.", "will answer", ["will answers", "will answering", "am answer"], "Quyết định ngay lúc nói → will + V nguyên mẫu."),
      check("I promise I ___ late again.", "won't be", ["won't being", "won't is", "not will be"], "Lời hứa → will not (won't) + V nguyên mẫu."),
      check("Do you think she ___ the exam?", "will pass", ["will passes", "will passing", "wills pass"], "Dự đoán theo ý kiến (Do you think) → will + V.")]),
    ("be-going-to", "future", "A2", ("Tương lai gần (be going to)", "Near future (be going to)"),
     (["S + am/is/are + going to + V"], ["S + am/is/are + not + going to + V"], ["Am/Is/Are + S + going to + V?"]),
     [use("Dự định đã có từ trước", "Plans made before now", "We are going to visit Hoi An next month."),
      use("Dự đoán có dấu hiệu rõ ràng", "Predictions based on what we can see", "Look at those clouds! It is going to rain.")],
     ["tonight", "tomorrow", "next week", "Look!", "dấu hiệu trước mắt"],
     ("Quyết định ngay lúc nói dùng will; dự định đã lên kế hoạch dùng be going to.",
      "Use will for decisions made now and be going to for plans already made."),
     [check("Look at those dark clouds! It ___ rain.", "is going to", ["going to", "is go to", "goes to"], "Dự đoán có dấu hiệu (mây đen) → be going to + V."),
      check("We ___ visit our grandparents this weekend; we have bought the tickets.", "are going to", ["is going to", "going to", "are go to"], "Dự định đã có (đã mua vé); we → are going to."),
      check("___ she going to study abroad next year?", "Is", ["Does", "Will", "Has"], "Câu hỏi be going to → Am/Is/Are + S + going to + V; she → Is.")]),
    ("future-continuous", "future", "B1", ("Tương lai tiếp diễn", "Future continuous"),
     (["S + will be + V-ing"], ["S + will not be + V-ing"], ["Will + S + be + V-ing?"]),
     [use("Đang diễn ra tại một thời điểm trong tương lai", "In progress at a future moment", "At nine tomorrow morning, I will be taking the exam."),
      use("Hỏi lịch sự về kế hoạch của người khác", "Polite questions about plans", "Will you be using the car tonight?")],
     ["at this time tomorrow", "at 9 a.m. next Monday", "this time next week"],
     ("Dùng khi có một thời điểm cụ thể trong tương lai và việc đang diễn ra lúc đó.",
      "Use it with a specific future moment when the action will be in progress."),
     [check("This time next week, we ___ on the beach.", "will be lying", ["will lying", "will be lie", "are lie"], "Đang diễn ra tại thời điểm tương lai → will be + V-ing."),
      check("Don't call at eight; I ___ dinner then.", "will be having", ["will having", "will be have", "have had"], "Một thời điểm tương lai cụ thể (at eight) → will be + V-ing."),
      check("___ you be using the printer this afternoon?", "Will", ["Are", "Do", "Have"], "Câu hỏi tương lai tiếp diễn → Will + S + be + V-ing.")]),
    ("future-perfect", "future", "B2", ("Tương lai hoàn thành", "Future perfect"),
     (["S + will have + V3/ed"], ["S + will not have + V3/ed"], ["Will + S + have + V3/ed?"]),
     [use("Sẽ hoàn thành trước một mốc trong tương lai", "Finished before a future time", "By 2030, they will have built the new bridge."),
      use("Dự đoán về việc đã xong tính đến một lúc sau", "Predicting what will be done by a later time", "By the time you read this, I will have left.")],
     ["by + thời gian", "by the time", "before", "by then"],
     ("Thường đi với by + mốc tương lai: By Friday, I will have finished.",
      "It usually comes with by + a future time: By Friday, I will have finished."),
     [check("By next June, I ___ from university.", "will have graduated", ["will have graduate", "will has graduated", "will graduated"], "By + mốc tương lai → will have + V3."),
      check("She ___ the report by the time you arrive.", "will have finished", ["will have finish", "will finished", "will has finished"], "Hoàn thành trước một mốc tương lai → will have + V3."),
      check("Will they ___ the work before Friday?", "have completed", ["completed", "completing", "has completed"], "Câu hỏi tương lai hoàn thành → Will + S + have + V3.")]),
    ("future-perfect-continuous", "future", "C1", ("Tương lai hoàn thành tiếp diễn", "Future perfect continuous"),
     (["S + will have been + V-ing"], ["S + will not have been + V-ing"], ["Will + S + have been + V-ing?"]),
     [use("Kéo dài đến một mốc tương lai, nhấn mạnh thời lượng", "Lasting up to a future time, stressing how long", "By next year, I will have been teaching for ten years.")],
     ["by + mốc tương lai", "for + khoảng thời gian", "by the time", "by then"],
     ("Ít gặp trong hội thoại; thường dùng để nhấn mạnh một quãng thời gian dài tính đến một mốc tương lai.",
      "Rare in conversation; mostly used to stress a long period up to a future point."),
     [check("By December, she ___ here for five years.", "will have been working", ["will have working", "will been working", "has been worked"], "Kéo dài đến một mốc tương lai → will have been + V-ing."),
      check("By the time you get home, I ___ for three hours.", "will have been studying", ["will have been study", "will be studied", "have been studied"], "Quãng thời gian tính đến một mốc tương lai → will have been + V-ing."),
      check("How long will you ___ by the end of this month?", "have been training", ["has been training", "be train", "had trained"], "Câu hỏi: Will + S + have been + V-ing.")]),
]


def main():
    out = []
    for order, (slug, group, level, name, forms, uses, signals, tip, practice) in enumerate(TENSES, 1):
        for q in practice:
            assert q["sentence"].count("___") == 1 and len(set(q["options"])) == 4, q
        out.append({
            "id": f"t-{slug}", "order": order, "group": group, "level": level,
            "name": {"vi": name[0], "en": name[1]},
            "forms": {"affirmative": forms[0], "negative": forms[1], "question": forms[2]},
            "uses": uses, "signals": signals, "tip": {"vi": tip[0], "en": tip[1]}, "practice": practice,
        })
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "tenses.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "tenses,", sum(len(t["practice"]) for t in out), "checks")


if __name__ == "__main__":
    main()

"""Writes src/data/grammar-quiz.json, the seed for the grammar game and the placement test.

Each item is original: one sentence with a single blank (___), four options with exactly one correct
answer, and a Vietnamese explanation. Distractors are chosen so that only the answer is grammatical
(or clearly the only natural choice) in the sentence. Run: python scripts/create-grammar-quiz.py
"""
import json
import pathlib

# (level, category, sentence, answer, [three wrong options], explanation in Vietnamese)
ITEMS = [
    # ---------- A1 ----------
    ("A1", "tense", "She ___ to school every day.", "walks", ["walk", "walking", "is walk"], "Hiện tại đơn với chủ ngữ số ít (she): động từ thêm -s."),
    ("A1", "tense", "I ___ a student.", "am", ["is", "are", "be"], "Chủ ngữ I đi với am."),
    ("A1", "tense", "They ___ football now.", "are playing", ["play", "plays", "is playing"], "Có now → hiện tại tiếp diễn; they đi với are."),
    ("A1", "tense", "He ___ like coffee.", "doesn't", ["don't", "isn't", "not"], "Phủ định hiện tại đơn với he/she/it: doesn't + động từ nguyên mẫu."),
    ("A1", "tense", "___ you like music?", "Do", ["Does", "Are", "Is"], "Câu hỏi hiện tại đơn với you: Do + chủ ngữ + động từ."),
    ("A1", "tense", "Yesterday I ___ to the park.", "went", ["go", "goes", "going"], "Yesterday → quá khứ đơn; go có dạng quá khứ bất quy tắc là went."),
    ("A1", "tense", "Look! It ___.", "is raining", ["rains", "rain", "rained"], "Look! báo hiệu việc đang xảy ra → hiện tại tiếp diễn."),
    ("A1", "article", "I have ___ apple in my bag.", "an", ["a", "many", "two"], "Apple bắt đầu bằng nguyên âm nên dùng an."),
    ("A1", "article", "My father is ___ doctor.", "a", ["an", "some", "many"], "Nói nghề nghiệp của một người: a/an + danh từ; doctor bắt đầu bằng phụ âm."),
    ("A1", "article", "___ sun is very hot today.", "The", ["A", "An", "Some"], "Vật duy nhất (the sun, the moon) dùng the."),
    ("A1", "preposition", "We have lunch ___ twelve o'clock.", "at", ["in", "on", "for"], "Giờ cụ thể dùng at."),
    ("A1", "preposition", "My birthday is ___ May.", "in", ["on", "at", "to"], "Tháng dùng in."),
    ("A1", "preposition", "I go swimming ___ Mondays.", "on", ["in", "at", "to"], "Thứ trong tuần dùng on."),
    ("A1", "preposition", "The book is ___ the table.", "on", ["to", "of", "from"], "Nằm trên bề mặt dùng on."),
    ("A1", "quantifier", "There ___ two books on the table.", "are", ["is", "am", "be"], "There are + danh từ số nhiều."),
    ("A1", "quantifier", "How ___ apples do you want?", "many", ["much", "any", "lot"], "Danh từ đếm được số nhiều (apples) dùng how many."),
    ("A1", "quantifier", "There isn't ___ milk in the fridge.", "any", ["many", "a", "few"], "Câu phủ định với danh từ không đếm được dùng any."),
    ("A1", "modal", "I ___ speak English, but I can't speak French.", "can", ["am", "is", "does"], "Can + động từ nguyên mẫu nói về khả năng."),
    ("A1", "adverb", "He drives very ___.", "carefully", ["careful", "care", "carefulness"], "Bổ nghĩa cho động từ drive cần trạng từ (careful → carefully)."),
    ("A1", "comparison", "My brother is ___ than me.", "taller", ["tall", "tallest", "more tall"], "Tính từ ngắn so sánh hơn: thêm -er + than."),
    ("A1", "pronoun", "This is my sister. ___ name is Lan.", "Her", ["She", "His", "Hers"], "Trước danh từ (name) dùng tính từ sở hữu her."),
    ("A1", "pronoun", "Can you help ___?", "me", ["I", "my", "mine"], "Sau động từ help dùng đại từ tân ngữ me."),
    # ---------- A2 ----------
    ("A2", "tense", "I was watching TV when the phone ___.", "rang", ["rings", "ring", "has rung"], "Việc xen vào (quá khứ đơn) cắt ngang việc đang diễn ra (quá khứ tiếp diễn)."),
    ("A2", "tense", "Have you ever ___ sushi?", "eaten", ["ate", "eat", "eating"], "Hiện tại hoàn thành: have + quá khứ phân từ (eat → eaten)."),
    ("A2", "tense", "We ___ here since 2020.", "have lived", ["live", "lived", "are living"], "Since + mốc thời gian → hiện tại hoàn thành."),
    ("A2", "tense", "I ___ my keys. I can't find them now.", "have lost", ["lose", "am losing", "was lose"], "Việc trong quá khứ còn ảnh hưởng tới hiện tại → hiện tại hoàn thành."),
    ("A2", "tense", "Look at those dark clouds! It ___ rain.", "is going to", ["goes to", "is going", "going to"], "Dự đoán dựa trên dấu hiệu trước mắt: be going to + động từ."),
    ("A2", "comparison", "This is the ___ film I have ever seen.", "best", ["good", "better", "most good"], "So sánh nhất của good là the best."),
    ("A2", "comparison", "Lan is ___ than her sister.", "more careful", ["carefuller", "most careful", "careful"], "Tính từ dài so sánh hơn: more + tính từ + than."),
    ("A2", "comparison", "My bag is as heavy ___ yours.", "as", ["than", "like", "so"], "So sánh bằng: as + tính từ + as."),
    ("A2", "modal", "You ___ wear a seatbelt in the car. It's the law.", "must", ["can", "might", "would"], "Bắt buộc theo luật: must."),
    ("A2", "modal", "You ___ smoke here. It's not allowed.", "mustn't", ["don't have to", "needn't", "can"], "Cấm đoán: mustn't (khác don't have to = không cần)."),
    ("A2", "verbform", "I enjoy ___ to music.", "listening", ["listen", "to listen", "listened"], "Enjoy + V-ing."),
    ("A2", "verbform", "She wants ___ a doctor.", "to become", ["becoming", "become", "became"], "Want + to V."),
    ("A2", "article", "She plays ___ piano every evening.", "the", ["a", "an", "some"], "Chơi nhạc cụ: play the + nhạc cụ."),
    ("A2", "article", "I'd like ___ information about the course.", "some", ["an", "a", "many"], "Information không đếm được, không dùng a/an; dùng some."),
    ("A2", "preposition", "I'm interested ___ art.", "in", ["on", "at", "about"], "Interested in + danh từ/V-ing."),
    ("A2", "preposition", "She is good ___ maths.", "at", ["on", "of", "with"], "Good at + môn học/kỹ năng."),
    ("A2", "quantifier", "We don't have ___ time. Hurry up!", "much", ["many", "a few", "few"], "Time không đếm được: much trong câu phủ định."),
    ("A2", "quantifier", "There are ___ people in the room, maybe three or four.", "a few", ["a little", "much", "any"], "Một vài (đếm được): a few + danh từ số nhiều."),
    ("A2", "connector", "I was tired, ___ I went to bed early.", "so", ["but", "because", "although"], "So nêu kết quả: mệt nên đi ngủ sớm."),
    ("A2", "connector", "She stayed at home ___ she was ill.", "because", ["so", "but", "or"], "Because nêu lý do."),
    ("A2", "passive", "This bridge ___ in 1990.", "was built", ["built", "is building", "was build"], "Bị động quá khứ đơn: was/were + quá khứ phân từ."),
    ("A2", "relative", "The woman ___ lives next door is a teacher.", "who", ["which", "where", "whose"], "Who thay cho người, làm chủ ngữ của mệnh đề quan hệ."),
    ("A2", "adverb", "He ___ goes to the gym. He goes every day.", "always", ["never", "rarely", "seldom"], "Đi mỗi ngày → always (luôn luôn)."),
    ("A2", "adverb", "The test was ___ easy.", "surprisingly", ["surprising", "surprise", "surprised"], "Bổ nghĩa cho tính từ easy cần trạng từ."),
    ("A2", "pronoun", "This isn't my umbrella. It's ___.", "hers", ["her", "she", "herself"], "Đứng một mình thay cho her umbrella: đại từ sở hữu hers."),
    # ---------- B1 ----------
    ("B1", "tense", "By the time we arrived, the film ___.", "had started", ["has started", "starts", "will start"], "Việc xảy ra trước một mốc quá khứ → quá khứ hoàn thành."),
    ("B1", "tense", "I ___ for two hours when she finally called.", "had been waiting", ["have been waiting", "am waiting", "wait"], "Việc kéo dài đến một thời điểm trong quá khứ → quá khứ hoàn thành tiếp diễn."),
    ("B1", "tense", "This time tomorrow, I ___ on a beach.", "will be lying", ["lie", "have lain", "lay"], "Việc đang diễn ra tại một thời điểm tương lai → tương lai tiếp diễn."),
    ("B1", "tense", "I have ___ finished my homework, so I can go out now.", "already", ["yet", "still", "ever"], "Already (đã rồi) trong câu khẳng định thì hoàn thành."),
    ("B1", "conditional", "If it ___ tomorrow, we will stay at home.", "rains", ["will rain", "rained", "would rain"], "Câu điều kiện loại 1: If + hiện tại đơn, will + V."),
    ("B1", "conditional", "If I ___ more money, I would travel the world.", "had", ["have", "will have", "would have"], "Câu điều kiện loại 2: If + quá khứ đơn, would + V."),
    ("B1", "conditional", "I would call him if I ___ his number.", "knew", ["know", "will know", "knows"], "Điều kiện không có thật ở hiện tại: quá khứ đơn trong mệnh đề if."),
    ("B1", "passive", "English ___ in many countries.", "is spoken", ["speaks", "is speaking", "spoken"], "Bị động hiện tại đơn: is/are + quá khứ phân từ."),
    ("B1", "passive", "The letters ___ yet.", "haven't been sent", ["haven't sent", "didn't send", "weren't sending"], "Bị động hiện tại hoàn thành: have/has been + quá khứ phân từ."),
    ("B1", "modal", "She ___ be at home. Her car is outside.", "must", ["can't", "mustn't", "shouldn't"], "Suy đoán chắc chắn dựa trên bằng chứng: must be."),
    ("B1", "modal", "You ___ have told me earlier! Now it's too late.", "should", ["can", "will", "need"], "Should have + quá khứ phân từ: trách việc lẽ ra nên làm."),
    ("B1", "verbform", "I'm looking forward to ___ you.", "seeing", ["see", "to see", "saw"], "Look forward to + V-ing (to ở đây là giới từ)."),
    ("B1", "verbform", "He stopped ___ because it was bad for his health.", "smoking", ["to smoke", "smoke", "smoked"], "Stop + V-ing = bỏ hẳn việc đó; stop + to V = dừng lại để làm việc khác."),
    ("B1", "verbform", "She let me ___ her car.", "use", ["to use", "using", "used"], "Let + tân ngữ + động từ nguyên mẫu không to."),
    ("B1", "relative", "This is the house ___ I was born.", "where", ["which", "who", "what"], "Where thay cho nơi chốn (in which)."),
    ("B1", "relative", "The man ___ car was stolen called the police.", "whose", ["who", "which", "that"], "Whose chỉ sự sở hữu (chiếc xe của người đàn ông)."),
    ("B1", "reported", "She told me she ___ the film the day before.", "had seen", ["has seen", "sees", "will see"], "Tường thuật lùi thì: quá khứ đơn → quá khứ hoàn thành."),
    ("B1", "article", "___ Mekong is one of the longest rivers in Asia.", "The", ["A", "An", "Some"], "Tên sông dùng the."),
    ("B1", "article", "She is ___ honest person.", "an", ["a", "the", "some"], "Honest đọc bắt đầu bằng nguyên âm (h câm) nên dùng an."),
    ("B1", "preposition", "It depends ___ the weather.", "on", ["of", "from", "at"], "Depend on."),
    ("B1", "preposition", "I apologised ___ being late.", "for", ["to", "of", "with"], "Apologise for + V-ing (apologise to + người)."),
    ("B1", "quantifier", "___ of my friends like football; the rest prefer tennis.", "Some", ["Any", "Much", "Every"], "Some of + danh từ số nhiều: một số trong nhóm."),
    ("B1", "connector", "___ it was raining, we went for a walk.", "Although", ["Because", "So", "Despite"], "Although + mệnh đề: mặc dù (despite + danh từ/V-ing)."),
    ("B1", "connector", "She passed the exam ___ studying very little.", "despite", ["although", "because", "so"], "Despite + V-ing/danh từ."),
    ("B1", "comparison", "The more you practise, ___ you get.", "the better", ["better", "the best", "more better"], "So sánh kép: the + so sánh hơn ..., the + so sánh hơn."),
    # ---------- B2 ----------
    ("B2", "tense", "By next June, she ___ here for ten years.", "will have worked", ["will work", "works", "has worked"], "Đến một mốc tương lai thì việc đã kéo dài → tương lai hoàn thành."),
    ("B2", "tense", "I ___ English for five years, and I still have a lot to learn.", "have been studying", ["am studying", "study", "had studied"], "Việc bắt đầu trong quá khứ, còn tiếp diễn → hiện tại hoàn thành tiếp diễn."),
    ("B2", "conditional", "If you had told me, I ___ you.", "would have helped", ["will help", "helped", "had helped"], "Câu điều kiện loại 3: If + quá khứ hoàn thành, would have + quá khứ phân từ."),
    ("B2", "conditional", "___ you need any help, just call me.", "Should", ["Would", "Had", "Were"], "Đảo ngữ điều kiện loại 1: Should + chủ ngữ + V = If you need."),
    ("B2", "conditional", "I wish I ___ more time to read.", "had", ["have", "will have", "would have"], "Ước điều trái hiện tại: wish + quá khứ đơn."),
    ("B2", "conditional", "I wish I ___ that email. It caused so many problems.", "hadn't sent", ["didn't send", "haven't sent", "wouldn't send"], "Hối tiếc về quá khứ: wish + quá khứ hoàn thành."),
    ("B2", "passive", "The results are expected ___ next week.", "to be announced", ["to announce", "being announced", "announced"], "Expected + to be + quá khứ phân từ (bị động)."),
    ("B2", "passive", "I'm going to have my hair ___ tomorrow.", "cut", ["cutting", "to cut", "cuts"], "Thể sai khiến: have + vật + quá khứ phân từ."),
    ("B2", "modal", "He ___ have left already; his coat is still here.", "can't", ["mustn't", "shouldn't", "needn't"], "Suy đoán phủ định về quá khứ: can't have + quá khứ phân từ."),
    ("B2", "modal", "You ___ have bought milk. We already had some.", "needn't", ["mustn't", "couldn't", "wouldn't"], "Needn't have + quá khứ phân từ: đã làm nhưng hoá ra không cần."),
    ("B2", "verbform", "I regret ___ you that your application was unsuccessful.", "to tell", ["telling", "tell", "told"], "Regret + to V: lấy làm tiếc phải báo (thư trang trọng); regret + V-ing là hối tiếc việc đã làm."),
    ("B2", "verbform", "She is used to ___ up early.", "getting", ["get", "got", "have got"], "Be used to + V-ing: đã quen với."),
    ("B2", "relative", "My sister, ___ lives in Hanoi, is a nurse.", "who", ["that", "which", "whom"], "Mệnh đề không xác định (có dấu phẩy) không dùng that; người làm chủ ngữ → who."),
    ("B2", "relative", "He failed the exam, ___ surprised everyone.", "which", ["that", "what", "who"], "Which thay cho cả mệnh đề phía trước."),
    ("B2", "reported", "He asked me where ___.", "I lived", ["did I live", "do I live", "lived I"], "Câu hỏi gián tiếp giữ trật tự câu kể: chủ ngữ + động từ."),
    ("B2", "article", "___ rich should pay more tax.", "The", ["A", "An", "Some"], "The + tính từ chỉ một nhóm người (the rich, the poor)."),
    ("B2", "preposition", "She insisted ___ paying for dinner.", "on", ["in", "at", "for"], "Insist on + V-ing."),
    ("B2", "preposition", "There has been a sharp rise ___ prices.", "in", ["on", "at", "by"], "A rise/increase in + danh từ."),
    ("B2", "connector", "___ the bad weather, the match went ahead.", "In spite of", ["Although", "Even though", "However"], "In spite of + danh từ."),
    ("B2", "connector", "He's very talented. ___, he's lazy.", "However", ["Although", "Despite", "Because"], "However đứng đầu câu, sau đó là dấu phẩy, nối hai câu đối lập."),
    ("B2", "quantifier", "___ student has to take the test.", "Every", ["All", "Both", "Many"], "Every + danh từ số ít + động từ số ít."),
    ("B2", "quantifier", "I have two sisters, but ___ of them lives near me.", "neither", ["none", "both", "either"], "Hai người, phủ định cả hai: neither of them."),
    ("B2", "comparison", "It was ___ difficult exam that nobody finished it.", "such a", ["so", "so a", "such"], "Such + a/an + tính từ + danh từ + that."),
    ("B2", "comparison", "The film was ___ boring that I fell asleep.", "so", ["such", "too", "very"], "So + tính từ + that."),
    ("B2", "adverb", "I could ___ hear him because of the noise.", "hardly", ["hard", "harder", "hardest"], "Hardly = hầu như không (khác hard = chăm chỉ, mạnh)."),
    # ---------- C1 ----------
    ("C1", "inversion", "No sooner had I arrived ___ the phone rang.", "than", ["when", "then", "as"], "No sooner ... than: vừa mới ... thì."),
    ("C1", "inversion", "Rarely ___ such a beautiful sunset.", "have I seen", ["I have seen", "I saw", "saw I"], "Rarely đứng đầu câu → đảo trợ động từ lên trước chủ ngữ."),
    ("C1", "inversion", "Not until the end of the meeting ___ the truth.", "did she reveal", ["she revealed", "she did reveal", "revealed she"], "Not until ... đứng đầu → đảo ngữ ở mệnh đề chính."),
    ("C1", "conditional", "___ it not been for your help, I would have failed.", "Had", ["If", "Were", "Should"], "Đảo ngữ điều kiện loại 3: Had it not been for = If it hadn't been for."),
    ("C1", "conditional", "If I had taken that job, I ___ in London now.", "would be living", ["would have lived", "will live", "lived"], "Điều kiện hỗn hợp: quá khứ khác đi → kết quả ở hiện tại (would + V)."),
    ("C1", "verbform", "The doctor recommended that he ___ more exercise.", "take", ["takes", "took", "taking"], "Thức giả định sau recommend that: động từ nguyên mẫu."),
    ("C1", "verbform", "It's high time we ___ home.", "went", ["go", "will go", "have gone"], "It's (high) time + chủ ngữ + quá khứ đơn: đã đến lúc."),
    ("C1", "verbform", "I'd rather you ___ smoke in the house.", "didn't", ["don't", "won't", "not"], "Would rather + người khác + quá khứ đơn."),
    ("C1", "passive", "He is said ___ a fortune in the 1990s.", "to have made", ["to make", "making", "that he made"], "Bị động kể lại với việc đã qua: is said to have + quá khứ phân từ."),
    ("C1", "passive", "It ___ that the company will cut jobs.", "is rumoured", ["rumours", "is rumouring", "has rumoured"], "It is rumoured/said/believed that ... (bị động khách quan)."),
    ("C1", "modal", "You ___ as well take an umbrella; it might rain.", "may", ["must", "should", "can"], "May/might as well: cũng nên làm (vì chẳng mất gì)."),
    ("C1", "relative", "The committee, most of ___ are volunteers, meets monthly.", "whom", ["who", "which", "them"], "Sau most of/some of chỉ người dùng whom."),
    ("C1", "relative", "That is the reason ___ I resigned.", "why", ["which", "what", "how"], "The reason why + mệnh đề."),
    ("C1", "article", "___ number of applicants has risen sharply this year.", "The", ["A", "An", "Some"], "The number of + danh từ số nhiều + động từ số ít (khác a number of + động từ số nhiều)."),
    ("C1", "preposition", "The new policy is ___ odds with our values.", "at", ["in", "on", "by"], "At odds with: mâu thuẫn với."),
    ("C1", "preposition", "She was accused ___ stealing the documents.", "of", ["for", "with", "about"], "Accuse somebody of + V-ing."),
    ("C1", "connector", "___ as it may seem, the plan actually worked.", "Strange", ["Strangely", "Although strange", "However strange"], "Tính từ + as + chủ ngữ + may seem: dù có vẻ ... đến đâu."),
    ("C1", "connector", "We should leave now ___ we miss the last train.", "lest", ["unless", "provided", "whereas"], "Lest = để khỏi, kẻo (trang trọng)."),
    ("C1", "quantifier", "___ the students passed the exam; it was a disaster.", "Hardly any of", ["Hardly", "Few", "Much of"], "Hardly any of + danh từ xác định: hầu như không ai trong số."),
    ("C1", "comparison", "The ___ he gets, the wiser he becomes.", "older", ["old", "oldest", "more old"], "So sánh kép: the + so sánh hơn, the + so sánh hơn."),
    # ---------- C2 ----------
    ("C2", "inversion", "Little ___ that he was being watched.", "did he know", ["he knew", "knew he", "he did know"], "Little đứng đầu câu (phủ định) → đảo trợ động từ."),
    ("C2", "inversion", "So severe ___ that the town was cut off.", "was the storm", ["the storm was", "did the storm", "the storm"], "So + tính từ đứng đầu → đảo động từ be lên trước chủ ngữ."),
    ("C2", "conditional", "Were the government ___ taxes, there would be protests.", "to raise", ["raising", "raise", "raised"], "Đảo ngữ Were + chủ ngữ + to V = If the government raised."),
    ("C2", "verbform", "It is essential that every applicant ___ the form in person.", "submit", ["submits", "submitted", "will submit"], "Thức giả định sau It is essential that: động từ nguyên mẫu cho mọi chủ ngữ."),
    ("C2", "passive", "The issue is believed ___ for years before anyone noticed.", "to have been ignored", ["to be ignored", "to have ignored", "being ignored"], "Bị động kể lại, việc đã qua và bị động: to have been + quá khứ phân từ."),
    ("C2", "modal", "She ___ have been more helpful if she had known the facts.", "might well", ["must", "needn't", "ought"], "Might well have + quá khứ phân từ: rất có thể đã (khả năng trong quá khứ)."),
    ("C2", "verbform", "He denied ___ the meeting, despite clear evidence.", "having attended", ["to have attended", "attend", "to attend"], "Deny + V-ing; having + quá khứ phân từ nhấn mạnh việc đã xảy ra."),
    ("C2", "verbform", "Far from ___ the problem, the new law made it worse.", "solving", ["solve", "to solve", "solved"], "Far from + V-ing: không những không ... mà còn."),
    ("C2", "relative", "The scientist, ___ work the prize was awarded, gave a short speech.", "for whose", ["whose", "for whom", "for which"], "Giới từ + whose + danh từ: (the prize was awarded for his work)."),
    ("C2", "article", "She has ___ unusual ability to remember faces.", "an", ["a", "much", "few"], "Ability đếm được, unusual bắt đầu bằng nguyên âm → an."),
    ("C2", "preposition", "The decision was made ___ consultation with local residents.", "in", ["at", "on", "by"], "In consultation with: có tham vấn với."),
    ("C2", "preposition", "His theory is ___ variance with the evidence.", "at", ["in", "on", "of"], "At variance with: trái ngược với."),
    ("C2", "connector", "___ his lack of experience, he handled the crisis remarkably well.", "Notwithstanding", ["Nevertheless", "Whereas", "Albeit"], "Notwithstanding + danh từ = despite (trang trọng)."),
    ("C2", "connector", "The plan was ambitious, ___ unrealistic.", "albeit", ["despite", "whereas", "unless"], "Albeit + tính từ/cụm từ = although (trang trọng)."),
    ("C2", "quantifier", "___ of the two proposals was accepted.", "Neither", ["None", "Nor", "No"], "Hai lựa chọn, không cái nào: Neither of + động từ số ít."),
    ("C2", "comparison", "This is by ___ the most difficult problem we have faced.", "far", ["much", "very", "so"], "By far + so sánh nhất: nhấn mạnh vượt trội."),
]


def main():
    out, counts = [], {}
    for level, category, sentence, answer, wrong, explanation in ITEMS:
        assert sentence.count("___") == 1, sentence
        options = [answer, *wrong]
        assert len(set(options)) == 4, sentence
        counts[level] = counts.get(level, 0) + 1
        out.append({
            "id": f"q-{level.lower()}-{counts[level]:03d}",
            "level": level,
            "category": category,
            "sentence": sentence,
            "options": options,
            "answer": answer,
            "explanation": explanation,
        })
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "grammar-quiz.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(out)} items: {counts}")


if __name__ == "__main__":
    main()

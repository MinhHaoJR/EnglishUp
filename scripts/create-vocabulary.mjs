import { writeFileSync } from 'node:fs';
// Original authoring source. Each row: word | General American IPA | POS | vi | definition | example | CEFR.
const groups = {
  'Daily life': `routine|ruːˈtiːn|noun|thói quen hằng ngày|the usual order in which you do things|A short walk is part of my morning routine.|A2
neighbor|ˈneɪbɚ|noun|người hàng xóm|a person who lives near you|Our neighbor waters our plants when we travel.|A2
laundry|ˈlɔːndri|noun|quần áo cần giặt; việc giặt giũ|clothes that need washing or have been washed|I do the laundry on Sunday morning.|A2
tidy|ˈtaɪdi|adjective|gọn gàng|neat and arranged in the right place|A tidy desk helps me concentrate.|A2
errand|ˈɛrənd|noun|việc vặt cần đi làm|a short trip to do a small job|Buying stamps was my last errand today.|B1
budget|ˈbʌdʒɪt|noun|ngân sách; khoản chi dự tính|a plan for how much money you can spend|We set a weekly budget for groceries.|B1
appointment|əˈpɔɪntmənt|noun|cuộc hẹn|an arrangement to meet someone at a set time|My dental appointment is at nine tomorrow.|A2
habit|ˈhæbɪt|noun|thói quen|something you do regularly without much thought|Reading before bed is a useful habit.|A2
household|ˈhaʊshoʊld|noun|hộ gia đình|the people who live together in one home|Everyone in our household helps with cooking.|B1
convenient|kənˈviːniənt|adjective|thuận tiện|easy to use or suitable for your needs|The nearby bus stop is convenient for work.|B1
chore|tʃɔːr|noun|việc nhà|a small regular task at home|Washing the dishes is my evening chore.|B1
borrow|ˈbɑːroʊ|verb|mượn|to use something and return it later|May I borrow your umbrella until tomorrow?|A2
lend|lɛnd|verb|cho mượn|to let someone use something temporarily|I can lend you my bicycle this afternoon.|A2
repair|rɪˈpɛr|verb|sửa chữa|to make a broken thing work again|We repair old chairs instead of replacing them.|A2
receipt|rɪˈsiːt|noun|hóa đơn; biên nhận|a document showing that you paid|Keep the receipt in case the lamp breaks.|A2
occasionally|əˈkeɪʒənəli|adverb|thỉnh thoảng|sometimes but not often|I occasionally take a different route home.|B1
prioritize|praɪˈɔːrətaɪz|verb|ưu tiên|to decide which tasks matter most|I prioritize urgent tasks before checking messages.|B2
efficient|ɪˈfɪʃənt|adjective|hiệu quả, ít lãng phí|working well without wasting time or energy|Planning meals makes shopping more efficient.|B2
balance|ˈbæləns|noun|sự cân bằng|a fair or useful mixture of different things|She wants a better balance between work and rest.|B1
commitment|kəˈmɪtmənt|noun|sự cam kết; trách nhiệm đã nhận|a promise or responsibility that requires time|Caring for a garden is a long-term commitment.|B2`,
  Travel: `journey|ˈdʒɝːni|noun|hành trình|travel from one place to another|The train journey took three hours.|A2
platform|ˈplætfɔːrm|noun|sân ga|the area beside a railway track for passengers|Our train leaves from platform four.|A2
luggage|ˈlʌɡɪdʒ|noun|hành lý|bags and cases used when traveling|Please keep your luggage beside your seat.|A2
destination|ˌdɛstəˈneɪʃən|noun|điểm đến|the place you are traveling to|A quiet coastal town is our final destination.|B1
itinerary|aɪˈtɪnəˌrɛri|noun|lịch trình chuyến đi|a detailed plan for a trip|Our itinerary includes a morning at the museum.|B2
departure|dɪˈpɑːrtʃɚ|noun|sự khởi hành|the act or time of leaving|Check the departure time before booking a taxi.|B1
arrival|əˈraɪvəl|noun|sự đến nơi|the act or time of reaching a place|We called the hotel after our arrival.|A2
reservation|ˌrɛzɚˈveɪʃən|noun|việc đặt chỗ|an arrangement to keep a room or seat for you|I made a reservation for two nights.|B1
fare|fɛr|noun|giá vé đi lại|the price of a trip on public transport|The bus fare includes one large bag.|B1
route|ruːt|noun|tuyến đường|a way from one place to another|This route follows the river through town.|B1
passport|ˈpæspɔːrt|noun|hộ chiếu|an official document for international travel|Keep a copy of your passport in a separate bag.|A2
souvenir|ˌsuːvəˈnɪr|noun|quà lưu niệm|an object kept to remember a place|I bought a small wooden bird as a souvenir.|A2
landmark|ˈlændmɑːrk|noun|địa danh nổi bật|a recognizable building or feature of a place|The old clock tower is a local landmark.|B1
accommodation|əˌkɑːməˈdeɪʃən|noun|chỗ ở khi đi xa|a place where travelers can stay|We found affordable accommodation near the station.|B2
explore|ɪkˈsplɔːr|verb|khám phá|to travel around a place to learn about it|We plan to explore the island on foot.|B1
delay|dɪˈleɪ|noun|sự chậm trễ|a period when something happens later than planned|Heavy rain caused a short delay.|B1
transfer|ˈtrænsfɝː|noun|việc chuyển tuyến|a change from one vehicle or service to another|The airport transfer takes forty minutes.|B1
scenic|ˈsiːnɪk|adjective|có phong cảnh đẹp|having attractive natural views|We chose the scenic road along the coast.|B2
flexible|ˈflɛksəbəl|adjective|linh hoạt|able to change when circumstances change|A flexible ticket lets us leave a day later.|B2
crowded|ˈkraʊdɪd|adjective|đông đúc|full of people with little free space|The market is crowded on Saturday evenings.|A2`,
  Work: `colleague|ˈkɑːliːɡ|noun|đồng nghiệp|a person you work with|A colleague helped me prepare the presentation.|B1
deadline|ˈdɛdlaɪn|noun|hạn chót|the latest time by which work must be finished|Our deadline is Friday afternoon.|B1
meeting|ˈmiːtɪŋ|noun|cuộc họp|an event where people discuss something|The team meeting starts after lunch.|A2
schedule|ˈskɛdʒuːl|noun|lịch làm việc|a plan of activities and their times|I keep my work schedule on the wall.|A2
salary|ˈsæləri|noun|lương|regular payment for a job|The job offers training and a fair salary.|B1
interview|ˈɪntɚvjuː|noun|buổi phỏng vấn|a meeting to assess someone for a job|She practiced answering questions before her interview.|A2
task|tæsk|noun|nhiệm vụ|a piece of work that must be done|My first task is to check the orders.|A2
skill|skɪl|noun|kỹ năng|an ability developed through learning and practice|Listening carefully is an important workplace skill.|A2
feedback|ˈfiːdbæk|noun|ý kiến phản hồi|comments that help someone improve|The manager gave specific feedback on my report.|B1
promotion|prəˈmoʊʃən|noun|sự thăng chức|a move to a more senior job|His promotion brought new responsibilities.|B1
responsibility|rɪˌspɑːnsəˈbɪləti|noun|trách nhiệm|something you are expected to take care of|Keeping customer records safe is our responsibility.|B1
collaborate|kəˈlæbəreɪt|verb|cộng tác|to work together on a shared goal|Two teams will collaborate on the new service.|B2
negotiate|nɪˈɡoʊʃieɪt|verb|đàm phán|to discuss terms in order to reach agreement|We need to negotiate a realistic delivery date.|B2
proposal|prəˈpoʊzəl|noun|bản đề xuất|a formal suggestion for a plan|Her proposal explains how to reduce waiting times.|B2
remote|rɪˈmoʊt|adjective|từ xa|done away from a central workplace|Remote work saves me an hour of travel.|B1
productive|prəˈdʌktɪv|adjective|có năng suất|producing useful results|A quiet morning is my most productive time.|B2
training|ˈtreɪnɪŋ|noun|đào tạo|learning the skills needed for a job|New staff receive two days of safety training.|A2
client|ˈklaɪənt|noun|khách hàng sử dụng dịch vụ|a person or organization buying professional services|The client asked for a simpler design.|B1
strategy|ˈstrætədʒi|noun|chiến lược|a plan for achieving a long-term goal|Our strategy is to improve service before expanding.|B2
initiative|ɪˈnɪʃətɪv|noun|sự chủ động; sáng kiến|an action started to solve a problem|The recycling initiative began with one employee.|B2`,
  Food: `ingredient|ɪnˈɡriːdiənt|noun|nguyên liệu|one of the foods used to make a dish|Fresh ginger is the main ingredient in this sauce.|A2
recipe|ˈrɛsəpi|noun|công thức nấu ăn|instructions for preparing a dish|My aunt shared her soup recipe with me.|A2
portion|ˈpɔːrʃən|noun|khẩu phần|an amount of food served to one person|A small portion is enough for a light lunch.|B1
flavor|ˈfleɪvɚ|noun|hương vị|the taste of food or drink|Lemon gives the rice a fresh flavor.|B1
boil|bɔɪl|verb|luộc; đun sôi|to heat liquid until it bubbles|Boil the water before adding the noodles.|A2
stir|stɝː|verb|khuấy|to mix food with a spoon or similar tool|Stir the sauce slowly for one minute.|A2
slice|slaɪs|verb|thái lát|to cut something into thin flat pieces|Slice the tomatoes just before serving.|A2
ripe|raɪp|adjective|chín (trái cây)|ready to eat after growing fully|A ripe mango smells sweet.|B1
fresh|frɛʃ|adjective|tươi|recently produced and still in good condition|We buy fresh vegetables at the morning market.|A2
spicy|ˈspaɪsi|adjective|cay; nhiều gia vị|having a strong hot taste|This spicy soup warms me on rainy days.|A2
nutritious|nuːˈtrɪʃəs|adjective|bổ dưỡng|containing substances that support good health|Beans can be part of a nutritious meal.|B2
appetite|ˈæpətaɪt|noun|cảm giác thèm ăn|the desire to eat|A long walk gave us a good appetite.|B1
leftovers|ˈlɛftoʊvɚz|noun|thức ăn còn thừa|food remaining after a meal|We packed the leftovers for tomorrow's lunch.|B1
homemade|ˌhoʊmˈmeɪd|adjective|làm tại nhà|made at home instead of bought ready-made|She brought homemade bread to the picnic.|B1
seasonal|ˈsiːzənəl|adjective|theo mùa|available or happening at a particular time of year|Seasonal fruit often costs less.|B2
crunchy|ˈkrʌntʃi|adjective|giòn|firm and making a sound when bitten|The salad needs something crunchy.|B1
steam|stiːm|verb|hấp|to cook food using hot water vapor|Steam the vegetables until they are just tender.|B1
allergy|ˈælɚdʒi|noun|dị ứng|a harmful body reaction to a particular substance|Tell the restaurant about your peanut allergy.|B1
sustainable|səˈsteɪnəbəl|adjective|bền vững|able to continue without using up resources|The cafe buys fish from sustainable sources.|B2
beverage|ˈbɛvərɪdʒ|noun|đồ uống|a drink, especially one served with a meal|Choose a hot beverage from the menu.|B2`,
  Health: `exercise|ˈɛksɚsaɪz|noun|việc tập thể dục|physical activity to keep the body fit|Gentle exercise helps me feel more awake.|A2
sleep|sliːp|noun|giấc ngủ|the natural resting state of the body and mind|A regular bedtime can improve sleep.|A2
symptom|ˈsɪmptəm|noun|triệu chứng|a change in the body that may indicate illness|A persistent cough can be a symptom worth discussing.|B1
recover|rɪˈkʌvɚ|verb|hồi phục|to become well again|She took time off to recover from the flu.|B1
stretch|strɛtʃ|verb|duỗi; giãn cơ|to gently extend a part of the body|I stretch my legs after sitting for a long time.|A2
balanced|ˈbælənst|adjective|cân đối|including a suitable mixture of different things|He tries to eat a balanced selection of foods.|B1
hydration|haɪˈdreɪʃən|noun|sự bổ sung nước cho cơ thể|the process of providing enough water to the body|We discussed hydration before the summer walk.|B2
wellbeing|ˌwɛlˈbiːɪŋ|noun|trạng thái khỏe mạnh và thoải mái|the state of feeling healthy and comfortable|Time with friends supports her wellbeing.|B2
stress|strɛs|noun|sự căng thẳng|mental pressure caused by difficult situations|Short breaks help me manage everyday stress.|B1
rest|rɛst|noun|sự nghỉ ngơi|time spent relaxing instead of working|We stopped for a rest halfway up the hill.|A2
clinic|ˈklɪnɪk|noun|phòng khám|a place where people receive medical care|The clinic is beside the library.|A2
checkup|ˈtʃɛkʌp|noun|buổi khám sức khỏe|an examination to check general health|I booked a routine checkup for next week.|B1
energy|ˈɛnɚdʒi|noun|năng lượng; sức lực|the strength needed to do activities|I have more energy after a good night's sleep.|A2
posture|ˈpɑːstʃɚ|noun|tư thế cơ thể|the way you hold your body|She adjusted her chair to improve her posture.|B2
prevent|prɪˈvɛnt|verb|ngăn ngừa|to stop something from happening|A clear path can help prevent falls.|B1
mental|ˈmɛntəl|adjective|thuộc tinh thần|relating to the mind|The workshop focuses on mental wellbeing.|B1
gradual|ˈɡrædʒuəl|adjective|dần dần|happening slowly in small stages|His return to regular exercise was gradual.|B2
endurance|ɪnˈdʊrəns|noun|sức bền|the ability to continue an activity for a long time|The gentle training plan builds endurance over months.|B2
breath|brɛθ|noun|hơi thở|air taken into or released from the lungs|Take a slow breath before your presentation.|B1
routine care|ruːˈtiːn kɛr|noun|chăm sóc định kỳ|regular attention to maintain health|Routine care includes discussing concerns with a professional.|B2`,
  Technology: `device|dɪˈvaɪs|noun|thiết bị|a piece of equipment made for a purpose|This device measures the temperature in the room.|A2
screen|skriːn|noun|màn hình|the surface that displays digital information|The screen is easier to read in shade.|A2
password|ˈpæswɝːd|noun|mật khẩu|a secret string used to access an account|Use a different password for each account.|A2
update|ˈʌpdeɪt|noun|bản cập nhật|a newer version with changes or fixes|The update adds larger text options.|A2
download|ˈdaʊnloʊd|verb|tải xuống|to copy data from a network to a device|Download the map before leaving the hotel.|A2
upload|ˈʌploʊd|verb|tải lên|to send data from a device to a network|Please upload the report by noon.|B1
backup|ˈbækʌp|noun|bản sao lưu|a copy kept in case the original is lost|Make a backup before changing the files.|B1
privacy|ˈpraɪvəsi|noun|quyền riêng tư|control over access to personal information|The app explains its privacy settings clearly.|B1
network|ˈnɛtwɝːk|noun|mạng kết nối|a group of connected devices or systems|The library network is temporarily unavailable.|B1
storage|ˈstɔːrɪdʒ|noun|khả năng; nơi lưu trữ|space used to keep data or objects|Video files use a lot of storage.|B1
reliable|rɪˈlaɪəbəl|adjective|đáng tin cậy|working well consistently|We need a reliable connection for the call.|B1
accessible|əkˈsɛsəbəl|adjective|dễ tiếp cận, sử dụng|usable by people with different needs|Clear labels make the website more accessible.|B2
interface|ˈɪntɚfeɪs|noun|giao diện|the controls through which a person uses software|The interface has only three main buttons.|B2
innovation|ˌɪnəˈveɪʃən|noun|sự đổi mới|a new useful idea or method|The sensor is a small but practical innovation.|B2
automate|ˈɔːtəmeɪt|verb|tự động hóa|to make a process run with little human effort|We automate simple reminders to save time.|B2
notification|ˌnoʊtəfəˈkeɪʃən|noun|thông báo|a message telling you that something has happened|I turned off notifications during the lesson.|B1
attachment|əˈtætʃmənt|noun|tệp đính kèm|a file sent with a message|The attachment contains the meeting notes.|B1
wireless|ˈwaɪɚləs|adjective|không dây|working without a physical cable|My wireless keyboard needs new batteries.|B1
troubleshoot|ˈtrʌbəlʃuːt|verb|tìm và khắc phục lỗi|to identify and solve a technical problem|The guide helps users troubleshoot sound problems.|B2
permission|pɚˈmɪʃən|noun|quyền cho phép|approval to perform an action|The browser asks for microphone permission.|B1`,
  Environment: `recycle|riːˈsaɪkəl|verb|tái chế|to process used materials so they can be used again|We recycle clean paper at the community center.|A2
reuse|riːˈjuːz|verb|tái sử dụng|to use something again|You can reuse this glass jar for rice.|A2
waste|weɪst|noun|chất thải; sự lãng phí|unwanted material or unnecessary use of resources|The school measures food waste each week.|A2
pollution|pəˈluːʃən|noun|ô nhiễm|harmful substances added to air, water or land|The project studies pollution in the river.|B1
climate|ˈklaɪmət|noun|khí hậu|the usual weather conditions of a region|The region has a warm and wet climate.|B1
resource|ˈriːsɔːrs|noun|tài nguyên|something useful that people can draw on|Clean water is a valuable resource.|B1
renewable|rɪˈnuːəbəl|adjective|có thể tái tạo|naturally replaced as it is used|The building gets power from renewable sources.|B2
habitat|ˈhæbəˌtæt|noun|môi trường sống tự nhiên|the natural home of an animal or plant|The wetland is an important bird habitat.|B2
wildlife|ˈwaɪldlaɪf|noun|động vật hoang dã|animals living in their natural surroundings|Visitors should watch wildlife from a distance.|B1
conserve|kənˈsɝːv|verb|bảo tồn; tiết kiệm|to protect something from loss or waste|Simple repairs can conserve water at home.|B2
emission|ɪˈmɪʃən|noun|sự phát thải|the release of gas or other substances|The report compares emission levels from different buses.|B2
compost|ˈkɑːmpoʊst|noun|phân hữu cơ từ rác phân hủy|decayed organic material used to improve soil|Dry leaves become compost for the garden.|B2
reduce|rɪˈduːs|verb|giảm bớt|to make something smaller in amount|We reduce packaging by buying larger refill bags.|A2
protect|prəˈtɛkt|verb|bảo vệ|to keep something safe from harm|The fence helps protect young trees.|A2
forest|ˈfɔːrɪst|noun|rừng|a large area covered mainly with trees|A narrow path leads into the forest.|A2
drought|draʊt|noun|hạn hán|a long period with very little rain|The drought changed how farmers used water.|B2
flood|flʌd|noun|lũ lụt|water covering land that is normally dry|The flood closed the road for two days.|B1
community|kəˈmjuːnəti|noun|cộng đồng|people connected by a place or shared interest|Our community planted trees beside the playground.|B1
awareness|əˈwɛrnəs|noun|nhận thức|knowledge that something exists or matters|The exhibition raises awareness of local river life.|B2
impact|ˈɪmpækt|noun|tác động|a strong effect on something|We considered the environmental impact of our trip.|B2`,
  Education: `lesson|ˈlɛsən|noun|bài học; buổi học|a period of teaching or learning|Today's lesson includes a short conversation.|A2
practice|ˈpræktɪs|noun|sự luyện tập|repeated activity to improve a skill|Daily practice makes new words easier to remember.|A2
revise|rɪˈvaɪz|verb|ôn tập; chỉnh sửa|to study again or improve an earlier version|I revise my notes before the weekly quiz.|B1
explain|ɪkˈspleɪn|verb|giải thích|to make an idea easier to understand|Can you explain this step with an example?|A2
knowledge|ˈnɑːlɪdʒ|noun|kiến thức|information and understanding gained through learning|The project connects classroom knowledge with daily life.|B1
curious|ˈkjʊriəs|adjective|tò mò, ham tìm hiểu|wanting to learn or know more|Curious students often ask unexpected questions.|B1
confidence|ˈkɑːnfədəns|noun|sự tự tin|belief in your ability to do something|Small speaking tasks helped build her confidence.|B1
progress|ˈprɑːɡrɛs|noun|sự tiến bộ|movement toward a better or more developed state|Keep old drafts so you can see your progress.|A2
assignment|əˈsaɪnmənt|noun|bài tập được giao|a piece of work given to a learner|The assignment asks us to interview a neighbor.|B1
research|ˈriːsɝːtʃ|noun|nghiên cứu|careful study to discover or check information|Our research compares three ways of taking notes.|B1
evidence|ˈɛvədəns|noun|bằng chứng|information that supports a claim or conclusion|Find evidence in the passage before answering.|B2
evaluate|ɪˈvæljueɪt|verb|đánh giá|to judge the quality or value of something|We evaluate each source before using it.|B2
curriculum|kəˈrɪkjələm|noun|chương trình học|the subjects and content taught in a course|The curriculum includes practical communication tasks.|B2
scholarship|ˈskɑːlɚʃɪp|noun|học bổng|money awarded to help someone study|The scholarship covers books and travel costs.|B2
independent|ˌɪndɪˈpɛndənt|adjective|độc lập; tự chủ|able to act or learn without constant help|An independent learner knows when to ask for support.|B1
concentrate|ˈkɑːnsəntreɪt|verb|tập trung|to give all your attention to something|I concentrate better when my phone is silent.|B1
memorize|ˈmɛməraɪz|verb|ghi nhớ, học thuộc|to learn something so it can be recalled|It helps to memorize words in useful phrases.|B1
reflect|rɪˈflɛkt|verb|suy ngẫm|to think carefully about an experience or idea|We reflect on one useful thing after each lesson.|B2
achievement|əˈtʃiːvmənt|noun|thành tựu|something successfully completed through effort|Finishing her first English book was an achievement.|B2
lifelong|ˈlaɪflɔːŋ|adjective|suốt đời|continuing throughout a person's life|Curiosity is at the heart of lifelong learning.|B2`,
};
const words = Object.entries(groups).flatMap(([topic, rows], g) =>
  rows.split('\n').map((line, i) => {
    const [word, ipa, pos, meaning, definition, example, level] = line.split('|');
    return {
      id: `v-${g + 1}-${i + 1}`,
      word,
      ipa: `/${ipa}/`,
      pos,
      meaning,
      definition,
      examples: [example],
      level,
      topic,
    };
  }),
);
writeFileSync('src/data/vocabulary.json', JSON.stringify(words, null, 2) + '\n');

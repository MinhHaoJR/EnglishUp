"""Writes src/data/speaking.json: the sixteen original prompts (s1-s16) plus prompts written for EnglishUp
on 2026-11-11 so that every level from A1 to C2 has 50 speaking tasks, 25 to read aloud and 25 topic talks.

Each line is: title | topic code | mode (r = read aloud, t = topic talk) | text | cues separated by " ; ".
Read-aloud texts grow from one or two short sentences at A1 to a short paragraph at C2; their cues are
pronunciation tips. Topic talks give a task and three guiding points. Titles are unique, because a saved
attempt marks a prompt done by its title. Run: python scripts/create-speaking-prompts.py
"""
import json
import pathlib

TOPICS = {
    "DL": "Daily life", "TR": "Travel", "WK": "Work", "FD": "Food", "HE": "Health", "TE": "Technology",
    "EN": "Environment", "ED": "Education", "SH": "Shopping", "CO": "Communication", "PF": "People and family",
    "HS": "Hobbies and sport", "TP": "Transport", "NW": "Nature and weather", "HF": "Home and furniture",
    "PT": "Places in town", "MS": "Money and shopping", "AN": "Animals",
}
MODES = {"r": "read", "t": "talk"}
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

PROMPTS = {}

PROMPTS["A1"] = """
Good morning | DL | r | Good morning! My name is Lan. I am a student. | Say good morning with a smile in your voice. ; Pause after the first sentence.
My family | PF | r | I have a big family. I live with my parents and my two sisters. | Stress big and two. ; Say the s at the end of sisters.
At the café | FD | r | Can I have a cup of coffee and a small cake, please? | Let your voice go up at the end. ; Say please clearly.
Sunny and warm | NW | r | It is sunny and warm today. Let's go to the park. | Stress sunny and warm. ; Say let's go as one group.
My room | HF | r | My room is small, but it is bright. There is a bed, a desk and a lamp. | Pause at the comma. ; Say each thing in the list clearly.
Where is the bus stop? | TP | r | Excuse me, where is the bus stop? Is it near the bank? | Let your voice go up at the end of the second question. ; Say excuse me slowly.
My favourite colour | DL | r | My favourite colour is blue. I like the sea and the sky. | Stress blue. ; Put your tongue between your teeth for the.
Shopping for fruit | SH | r | I would like three apples and a bag of oranges, please. | Put your tongue between your teeth for three. ; Keep a steady pace.
Every morning | DL | r | I get up at six o'clock. I have breakfast, and then I walk to school. | Say six o'clock clearly. ; Say and then as one group.
My little cat | AN | r | I have a little cat. She is white, and she sleeps all day. | Stress little and white. ; Say sleeps with a clear s at the end.
Saturday and Sunday | HS | r | On Saturday I play football with my friends. On Sunday I rest at home. | Pause after each sentence. ; Stress Saturday and Sunday.
Nice to meet you | CO | r | Nice to meet you. Where are you from? I am from Viet Nam. | Say Where are you from with a falling voice. ; Say Viet Nam as two words.
At school | ED | r | Our teacher is kind. We read books and sing songs in class. | Stress kind. ; Say the ng at the end of sing and songs.
Lunch time | FD | r | I am hungry. Let's have rice, chicken and some vegetables for lunch. | Pause at each comma. ; Say vegetables with three beats: VEG-ta-bles.
My new phone | TE | r | This is my new phone. I use it to call my mum and to take photos. | Stress new. ; Say photos with a long o.
Thank you very much | CO | r | Thank you very much for your help. You are very kind. | Put your tongue between your teeth for thank. ; Stress very.
A day at the beach | TR | r | We swim in the sea and play on the sand. The water is cool. | Say swim and sea with a clear s. ; Stress cool.
What time is it? | DL | r | What time is it, please? It's half past three. | Use a falling voice for the question. ; Say half past as one group.
I feel tired | HE | r | I feel tired today. I want to go to bed early. | Stress tired and early. ; Say want to as one group.
My father's job | WK | r | My father is a driver. He drives a bus in the city. | Say driver and drives with a clear v. ; Stress bus.
The morning market | PT | r | The market is open every morning. People sell fish, meat and fruit. | Pause at the commas. ; Say fish with a soft sh.
Happy birthday | PF | r | Happy birthday! Here is a present for you. I hope you like it. | Say happy birthday with energy. ; Stress present on the first part: PRE-sent.
Take your umbrella | NW | r | It is raining. Please take your umbrella and your coat. | Stress raining. ; Say umbrella with the stress in the middle: um-BREL-la.
I like drawing | HS | r | I like drawing. I draw animals and trees in my notebook. | Say drawing and draw clearly. ; Pause after the first sentence.
Good night | DL | r | It is late. Good night, see you tomorrow. | Say good night softly. ; Stress tomorrow in the middle: to-MOR-row.
Introduce yourself | PF | t | Introduce yourself to a new classmate. | What is your name? ; How old are you? ; What do you like?
My home | HF | t | Talk about your home. | Where is it? ; How many rooms are there? ; What is your favourite room?
The people in my family | PF | t | Talk about the people in your family. | Who is in your family? ; What do they do? ; What do you do together?
My favourite food | FD | t | Talk about a food you love. | What is it? ; When do you eat it? ; Who makes it?
My day | DL | t | Describe your day from morning to evening. | What time do you get up? ; What do you do in the afternoon? ; What do you do in the evening?
My best friend | PF | t | Talk about your best friend. | What is your friend's name? ; What does your friend look like? ; What do you do together?
My school or work | ED | t | Talk about your school or your work. | Where is it? ; How do you get there? ; What do you like about it?
The weather where I live | NW | t | Talk about the weather where you live. | What is the weather like today? ; What is your favourite season? ; What do you wear in winter?
My town | PT | t | Talk about your town or city. | What places are there? ; Where do you like to go? ; What do you not like about it?
Animals I like | AN | t | Talk about an animal you like. | What animal is it? ; What does it look like? ; Why do you like it?
Where I go shopping | SH | t | Talk about where you go shopping. | Which shop do you like? ; What do you buy there? ; Who do you go with?
My weekends | HS | t | Talk about what you do at the weekend. | Where do you go? ; Who do you see? ; What do you like best?
What I am wearing | SH | t | Describe what you are wearing today. | What clothes are you wearing? ; What colours are they? ; Do you like them?
A sport I like | HS | t | Talk about a sport you like. | What sport is it? ; Do you play it or watch it? ; When do you play or watch it?
My breakfast | FD | t | Talk about your breakfast. | What do you eat? ; What do you drink? ; Where do you eat it?
How I use my phone | TE | t | Talk about how you use your phone. | What do you use it for? ; Which app do you like? ; How many hours do you use it?
A holiday place | TR | t | Talk about a place you visited on holiday. | Where did you go? ; Who did you go with? ; What did you do there?
Getting around my town | TP | t | Talk about how you travel in your town. | Do you walk, ride or take a bus? ; How long does it take? ; Do you like it?
Feeling good | HE | t | Talk about what you do to stay healthy. | What do you eat? ; Do you do any sport? ; When do you go to bed?
My last birthday | PF | t | Talk about your last birthday. | Where were you? ; Who was there? ; What presents did you get?
A person I like | PF | t | Talk about a person you like, such as a teacher or a neighbour. | Who is the person? ; What does the person do? ; Why do you like them?
My favourite room at home | HF | t | Describe your favourite room at home. | What is in the room? ; What colour is it? ; What do you do there?
Music I like | HS | t | Talk about music you like. | What songs do you like? ; When do you listen to music? ; Can you sing or play an instrument?
A park near me | EN | t | Talk about a park or a green place near you. | Where is it? ; What can you see there? ; What do people do there?
How I learn English | ED | t | Talk about how you learn English. | When do you study? ; What is easy? ; What is difficult?
"""

PROMPTS["A2"] = """
Ordering a meal | FD | r | Could I have the chicken soup and a glass of orange juice, please? And could we have some water too? | Let your voice go up at the end of each question. ; Say could I as one group.
Calling the doctor | HE | r | Hello, I'd like to make an appointment with the doctor. I've had a headache since yesterday. | Say I'd and I've clearly. ; Stress headache.
At the train station | TP | r | Excuse me, which platform does the train to Hue leave from? Is it on time today? | Let your voice go up at the end of the second question. ; Stress platform.
Visiting my grandparents | DL | r | This weekend I'm going to visit my grandparents. We usually cook together and go for a walk after dinner. | Say going to naturally. ; Pause after grandparents.
My friend Minh | PF | r | My friend Minh is tall and friendly. He always makes people laugh, and he's very good at football. | Stress always. ; Link he's very.
Booking a room | TR | r | I'd like to book a double room for two nights, from Friday to Sunday. Is breakfast included? | Stress double and two. ; Let your voice go up for the question.
Where are my keys? | DL | r | I can't find my keys anywhere. I think I left them on the kitchen table this morning. | Say can't with a clear t. ; Stress anywhere.
A new job | WK | r | I started a new job last month. The work is interesting, and my colleagues are very helpful. | Say started with an extra beat for -ed. ; Stress interesting on the first part.
Shoes in a bigger size | SH | r | Do you have these shoes in a bigger size? These ones are a little too small for me. | Stress bigger and small. ; Say shoes with a clear sh.
A film on a rainy day | NW | r | It's been raining all day, so we stayed inside and watched a film. It was a relaxing afternoon. | Link all day. ; Say watched with one beat.
My hometown | PT | r | My hometown is near the sea. It's quiet in winter, but in summer there are many tourists. | Pause after winter. ; Stress quiet and many.
Twenty minutes a day | ED | r | I practise English for twenty minutes every day. I listen to songs and write new words in a notebook. | Stress twenty. ; Say practise with a clear s at the end.
I'm running late | CO | r | Hi Nam, it's Hoa. I'm going to be ten minutes late. Please wait for me outside the cinema. | Pause after Hoa. ; Stress ten minutes.
Healthy habits | HE | r | I try to drink more water and walk to work. I feel better when I sleep for eight hours. | Stress more and eight. ; Link walk to.
My sister's party | PF | r | We had a party for my sister's birthday. Everyone brought food, and we danced until midnight. | Say sister's with a z sound at the end. ; Say danced with a t sound at the end.
A simple app | TE | r | I use this app to check the weather and the bus times. It's simple, and it saves me a lot of time. | Stress simple. ; Link a lot of.
Three bins | EN | r | We put paper, plastic and glass in different bins. It only takes a minute, and it helps the environment. | Pause at each comma. ; Stress environment on the second part: en-VI-ron-ment.
The swimming club | HS | r | I joined a swimming club in March. We practise twice a week, on Tuesdays and Thursdays. | Say Thursdays with th. ; Stress twice.
Turn right at the lights | TP | r | Go straight ahead and turn right at the traffic lights. The library is on your left, next to the bank. | Stress right and left. ; Pause after lights.
Thank you for the flowers | CO | r | Thank you so much for the flowers. They're beautiful, and they made me very happy. | Say thank you warmly. ; Stress beautiful.
Saving for a bike | MS | r | I want to buy a new bike, so I'm saving a little money every week. I hope to buy it in June. | Link want to. ; Stress every week.
A visit to the zoo | AN | r | At the zoo we saw elephants, monkeys and a very old turtle. The children loved the penguins most. | Pause at the commas. ; Stress loved.
A good weekend | DL | t | Describe a weekend you really enjoyed. | Where were you? ; What did you do? ; Why was it good?
A place to eat | FD | t | Recommend a restaurant or café in your town to a visitor. | What kind of food does it serve? ; How much does it cost? ; Why do you recommend it?
A teacher I remember | ED | t | Talk about a teacher you remember from primary school. | What was the teacher like? ; What did you learn? ; Why do you remember them?
A trip I want to take | TR | t | Talk about a place you would like to visit in the future. | Where is it? ; Who would you go with? ; What would you do there?
Around my home | PT | t | Describe the area where you live. | What shops and places are near you? ; Is it quiet or busy? ; What would you change?
Staying healthy | HE | t | Explain what you do to stay healthy. | What do you eat? ; How do you exercise? ; What is difficult for you?
A present I gave | PF | t | Talk about a present you gave to someone. | Who was it for? ; Why did you choose it? ; How did the person react?
Jobs at home | HF | t | Talk about the jobs you do at home. | Which jobs do you do? ; Which job do you dislike? ; Who does the most work?
An app I use every day | TE | t | Talk about an app you use every day. | What does it do? ; When do you use it? ; Would you recommend it?
A film I enjoyed | HS | t | Talk about a film or TV programme you enjoyed. | What was it about? ; Who was in it? ; Why did you like it?
Buses in my town | TP | t | Talk about public transport in your town. | What kinds are there? ; Do you use them? ; How could they be better?
Buying things online | SH | t | Talk about buying things online. | What do you buy online? ; What is good about it? ; What problems can happen?
A celebration in my country | DL | t | Describe a festival or celebration in your country. | When is it? ; What do people eat? ; What do you do?
A day that went wrong | DL | t | Talk about a day when things went wrong. | What happened? ; How did you feel? ; What did you do?
What I do | WK | t | Talk about what you do: your job or your studies. | What do you do every day? ; What do you like about it? ; What would you like to change?
Having a pet | AN | t | Talk about having a pet. | Do you have a pet, or would you like one? ; What do pets need? ; Are pets good for children?
Clean air, clean streets | EN | t | Talk about the environment in your town. | Is the air clean? ; Is there much rubbish? ; What can people do?
Making new friends | CO | t | Talk about how people make new friends. | Where do you meet new people? ; Is it easy for you? ; How do you keep in touch?
Trying a new sport | HS | t | Talk about a sport or game you tried for the first time. | What was it? ; Was it difficult? ; Would you try it again?
Where my money goes | MS | t | Talk about how you spend your money. | What do you spend most on? ; Do you save money? ; What would you like to buy?
Two seasons | NW | t | Compare two seasons in your country. | What is the weather like? ; What do people do? ; Which season do you prefer?
A skill I want to learn | ED | t | Talk about a skill you would like to learn. | What is the skill? ; Why do you want to learn it? ; How will you learn it?
"""

PROMPTS["B1"] = """
Changing my plans | DL | r | I was planning to stay at home tonight, but my friends invited me to a concert. I think I'll go, because I haven't seen them for weeks. | Pause at the comma before but. ; Stress haven't and weeks.
A lesson outside the textbook | ED | r | The most useful thing I learned this year wasn't in a textbook. It was how to ask for help when I didn't understand something. | Stress useful and help. ; Link ask for.
The battery only lasts an hour | SH | r | I bought this laptop last week, but the battery only lasts an hour. I'd like to exchange it or get a refund, please. | Stress hour. ; Pause before or get a refund.
Running in the mornings | HE | r | Since I started running in the mornings, I've had more energy during the day. It was hard at first, but now I really enjoy it. | Say I've had clearly. ; Stress really.
A delayed flight | TR | r | Our flight has been delayed by two hours because of the weather. The airline is giving everyone a free meal while we wait. | Stress two hours. ; Pause after weather.
Sharing ideas | WK | r | In our team, everyone shares ideas before we make a decision. It takes longer, but the results are usually better. | Stress everyone and better. ; Pause at the comma.
Cooking more often | FD | r | I've started cooking at home more often. It's cheaper than eating out, and I know exactly what's in my food. | Stress cheaper and exactly. ; Say what's clearly.
Life on a busy street | PT | r | I live on a busy street, so it's never really quiet. I've got used to the noise, but I still use earplugs at night. | Say got used to as one group. ; Stress never.
Turning off the lights | EN | r | If everyone turned off the lights when they left a room, we would save a surprising amount of energy. | Read the long sentence in two sense groups. ; Stress surprising.
My first interview | WK | r | I was so nervous before my first interview that I forgot the manager's name. Luckily, she was very understanding. | Stress so nervous. ; Pause after Luckily.
Concentrating in online classes | ED | r | Online classes save time, but it's easy to lose concentration. I turn off my phone and sit at a proper desk. | Stress easy and proper. ; Pause at the comma.
A leaking tap | HF | r | Hello, this is the tenant from flat twelve. The kitchen tap has been leaking since Monday. Could someone come and look at it? | Pause after twelve. ; Use a polite rising tone in the question.
Choosing a phone | TE | r | When I choose a phone, I care more about the battery and the camera than about the brand. | Stress battery and camera. ; Link care more.
The library reopens | PT | r | Our local library has just reopened after a long renovation. There's now a quiet study room and a small café. | Stress quiet and small. ; Say renovation with stress on the third part: ren-o-VA-tion.
Worth the effort | NW | r | We walked for three hours to reach the top of the mountain. The view was amazing, and it was definitely worth the effort. | Stress amazing and definitely. ; Pause after mountain.
Seeds for the birds | AN | r | Every winter my grandmother leaves seeds for the birds in her garden. She can name every bird that visits. | Stress every. ; Say birds with a clear ending.
A real bargain | MS | r | I found this jacket in the sales for half the original price. It's warm, it fits well, and it was a real bargain. | Pause at each comma. ; Stress half and bargain.
Learning to drive | TP | r | I'm learning to drive at the moment. Parking is the hardest part, but my instructor is very patient. | Stress hardest. ; Say instructor with stress on the second part: in-STRUC-tor.
Sunday video calls | CO | r | My parents live in another city, so we have a video call every Sunday evening. It's not the same as being there, but it helps. | Pause after city. ; Stress helps.
Joining a choir | HS | r | Last year I joined a choir, even though I'd never sung in public. Now I look forward to our rehearsals every week. | Say choir as KWAI-er. ; Stress never.
A stranger with a toolkit | DL | r | When my bike broke down, a stranger stopped and helped me fix it. I didn't even get the chance to thank him properly. | Pause after down. ; Stress properly.
Less sugar | HE | r | I've been trying to eat less sugar. I still have dessert at weekends, but I've stopped putting sugar in my coffee. | Stress less and stopped. ; Say I've been as one group.
A recent decision | PF | t | Talk about a decision you made recently and how you made it. | What were the options? ; What helped you decide? ; Are you happy with the decision?
The perfect holiday | TR | t | Describe your idea of the perfect holiday. | Where would you go? ; What would you do each day? ; Why does this kind of holiday suit you?
Studying at home | WK | t | Discuss the advantages and disadvantages of working or studying from home. | What is better at home? ; What is more difficult? ; Which do you prefer?
What we eat in my country | FD | t | Explain to a visitor what people in your country usually eat. | What is a typical breakfast? ; What do people eat on special days? ; Which dish should the visitor try?
A book or film that made me think | HS | t | Talk about a book or film that made you think differently. | What was it about? ; What did you learn? ; Would you recommend it?
Social media and me | TE | t | Talk about how you use social media. | Which platforms do you use? ; What do you like about them? ; What problems do they cause?
A problem in my city | PT | t | Describe a problem in your city and suggest a solution. | What is the problem? ; Who does it affect? ; What could be done?
A mistake that taught me something | ED | t | Talk about a mistake that taught you something. | What happened? ; How did you feel? ; What did you learn?
Exercise in a busy life | HE | t | Explain why exercise is important and how people can fit it into a busy life. | Why is it important? ; What stops people? ; What simple ideas can you suggest?
Markets, supermarkets or online? | SH | t | Compare shopping in markets, in supermarkets and online. | What are the advantages of each? ; Which do you use most? ; How have your habits changed?
A good neighbour | PF | t | Describe what makes a good neighbour. | What should a good neighbour do? ; What should they avoid? ; Give an example from your life.
Travelling alone | TR | t | Would you like to travel alone? Explain your view. | What are the benefits? ; What are the risks? ; Where would you go?
Less plastic every day | EN | t | Talk about how people could use less plastic. | Where do we use plastic every day? ; What alternatives are there? ; What have you changed?
A job I would like | WK | t | Describe a job you would like to do in the future. | What does the job involve? ; What skills do you need? ; Why does it interest you?
Friends who live far away | CO | t | Talk about how you keep in touch with friends who live far away. | Which ways do you use? ; How often do you talk? ; Is it enough?
Weekdays and weekends | DL | t | Compare your weekdays and your weekends. | How are they different? ; Which part of the week do you prefer? ; What would you change?
Why people keep pets | AN | t | Talk about why people keep pets. | What do pets give people? ; What are the responsibilities? ; Which pet suits a busy person?
Money lessons at school | MS | t | Should young people learn to manage money at school? Explain your view. | What should they learn? ; Who should teach it? ; What happens if they do not learn?
A memorable meal | FD | t | Describe a meal you remember well. | Where were you? ; Who were you with? ; Why do you remember it?
The home I would like | HF | t | Describe the home you would like to live in one day. | Where is it? ; What does it look like? ; What is the most important room?
Travel in twenty years | TP | t | Talk about how people might travel in twenty years. | What will change? ; What will stay the same? ; Will it be better for the environment?
A hobby that relaxes me | HS | t | Describe a hobby that helps you relax. | When did you start? ; How does it help you? ; Would you recommend it to others?
"""

PROMPTS["B2"] = """
The value of sleep | HE | r | Many people treat sleep as something they can sacrifice when they are busy. In reality, a lack of sleep affects concentration, mood and even the immune system. | Group the words: many people treat sleep / as something they can sacrifice. ; Stress reality and immune.
The city before the traffic | PT | r | The city is at its most fascinating early in the morning, when the street vendors are setting up and the traffic hasn't yet reached its usual chaos. | Pause after morning. ; Stress fascinating and chaos.
Clear boundaries | WK | r | Working remotely gives people more control over their time, but it also blurs the line between work and home. Setting clear boundaries has become an essential skill. | Pause at the comma before but. ; Stress essential.
The real cost of cheap clothes | SH | r | Cheap clothing seems like a bargain, yet its real cost is often paid by workers and the environment. Buying fewer, better-made items is one way to respond. | Stress real cost. ; Pause after environment.
Learning a language as an adult | ED | r | Learning a language as an adult is challenging, but it isn't impossible. Regular practice, realistic goals and a little patience make a remarkable difference. | Pause at each comma in the list. ; Stress remarkable.
The overnight train | TR | r | We took the overnight train to the north, and I barely slept. I spent most of the night watching small towns pass by in the dark. | Link took the. ; Stress barely.
Advertising to children | CO | r | Advertisers know that children influence what their families buy. That is why many experts believe advertising aimed at young audiences should be strictly limited. | Stress influence and strictly. ; Pause after buy.
Scooters on the pavement | TP | r | Electric scooters are convenient for short trips, but they have created new problems on crowded pavements. Many cities are now introducing rules about where they can be parked. | Pause after trips. ; Stress convenient and introducing.
Cleaning the river | DL | r | Every spring, the whole village gathers to clean the river and plant trees along its banks. It started as a small project and has become a tradition. | Stress whole and tradition. ; Pause after banks.
Privacy settings | TE | r | Most of us accept privacy settings without reading them. We rarely consider how much personal information we share in exchange for convenience. | Stress rarely and convenience. ; Link exchange for.
At the food bank | CO | r | Volunteering at the food bank taught me more about my own city than years of living there. You meet people whose lives are completely different from yours. | Pause after bank. ; Stress completely.
Delivery and packaging | FD | r | Food delivery apps have changed the way people eat, especially in big cities. They are convenient, but they also create a great deal of packaging waste. | Pause after eat. ; Stress great deal.
Honesty with kindness | PF | r | Telling a friend something they don't want to hear is never easy. However, honesty delivered with kindness usually strengthens a friendship rather than damaging it. | Pause after However. ; Stress honesty and kindness.
Gardens on the roof | EN | r | Rooftop gardens are appearing across the city. They provide fresh vegetables, reduce heat in summer and give neighbours a reason to spend time together. | Pause at each comma. ; Stress rooftop.
Changing careers | WK | r | Changing careers in your thirties can feel risky. Yet many people discover that the skills they developed in one field are surprisingly valuable in another. | Stress risky and surprisingly. ; Pause after Yet.
Animals near our towns | AN | r | As forests shrink, many animals are forced closer to towns and farms. Protecting their habitats is better for both wildlife and the people living nearby. | Pause after farms. ; Stress habitats.
A simple budget | MS | r | Keeping a simple budget does not mean giving up everything you enjoy. It simply helps you notice where your money goes and decide what really matters. | Stress simple and really matters. ; Link where your.
What team sports teach | HS | r | Team sports teach lessons that are hard to learn elsewhere: how to lose gracefully, how to rely on others and how to keep going when you are tired. | Pause at the colon. ; Keep the three parts of the list even.
Weather or climate? | NW | r | Weather describes what happens on a particular day, while climate describes long-term patterns. Confusing the two often leads to misleading conclusions. | Contrast weather and climate with stress. ; Pause after day.
Smart homes | HF | r | Smart home devices can adjust the lighting and temperature automatically. They are useful, but some people worry about how much data these devices collect. | Stress automatically. ; Pause after useful.
Using your nerves | ED | r | Most people feel nervous before speaking in public. The trick is not to remove the nerves but to use that energy to sound more engaged. | Stress trick and engaged. ; Pause before but.
Searching for symptoms | HE | r | Searching for symptoms online can be reassuring or terrifying. Information from reliable sources is helpful, but it can never replace a proper medical examination. | Contrast reassuring and terrifying. ; Stress never.
Renting instead of buying | MS | r | Renting tools, cars and even clothes instead of buying them is becoming more common. Supporters say it saves money and resources, while critics worry about safety. | Pause after them. ; Stress supporters and critics.
News from social media | TE | t | Discuss how social media has changed the way people get news. | What are the advantages? ; What are the dangers? ; How do you check whether news is true?
Should university be free? | ED | t | Give your opinion on whether university education should be free. | Who would benefit? ; Who would pay? ; What alternatives are there?
A leader I admire | PF | t | Describe a leader you admire, in any field, and explain why. | What has this person achieved? ; What qualities do they have? ; What can others learn from them?
Tourism and local life | TR | t | Discuss how tourism affects the lives of local people. | What benefits does it bring? ; What problems can it cause? ; How can the balance be improved?
Work-life balance | WK | t | Explain what work-life balance means to you and how it can be achieved. | What makes it difficult? ; What can employers do? ; What can individuals do?
A healthier city | HE | t | Describe how a city could be designed to help people live healthier lives. | What would you change about transport? ; What about green spaces? ; Who should pay for these changes?
Do we buy too much? | SH | t | Discuss whether people today buy too much. | Why do people buy more than they need? ; What are the consequences? ; How could habits change?
Grandparents today | PF | t | Talk about the role grandparents play in families today. | How do they help? ; How has their role changed? ; What can younger people learn from them?
Artificial intelligence every day | TE | t | Discuss how artificial intelligence is already part of everyday life. | Where do people use it? ; What are the benefits? ; What concerns do people have?
Saving endangered animals | AN | t | Discuss whether protecting endangered species should be a priority. | Why does it matter? ; What are the costs? ; What can individuals do?
The daily commute | TP | t | Compare different ways of commuting and their impact. | Which is fastest? ; Which is best for the environment? ; How would you improve commuting in your city?
A skill everyone should have | ED | t | Describe a practical skill you think everyone should learn and explain why. | What is the skill? ; How is it useful? ; How could people learn it?
Friends made online | CO | t | Discuss whether friendships made online are as valuable as others. | How are they different? ; What are the benefits? ; What are the risks?
Food waste | FD | t | Discuss the causes of food waste and possible solutions. | Where is food wasted? ; Why does it happen? ; What could families and shops do?
A first home | HF | t | Discuss the difficulties young people face in finding a home. | Why is it difficult? ; What are the consequences? ; What could help?
How advertising persuades | CO | t | Discuss how advertising influences what people want. | How does advertising persuade people? ; Is it always harmful? ; Should it be more strictly controlled?
Children and competition | HS | t | Discuss whether competitive sport is good for children. | What can children learn? ; What pressures can it create? ; How should adults behave?
Cash or cards? | MS | t | Discuss whether societies should stop using cash. | What are the advantages of digital payments? ; Who might be left behind? ; What do you prefer?
Extreme weather | NW | t | Talk about how extreme weather is affecting daily life. | What examples have you seen? ; How do people prepare? ; What should governments do?
The future of local shops | PT | t | Discuss what will happen to high streets and local shops in the future. | Why are some shops closing? ; What could replace them? ; How can communities support them?
Is ambition always good? | WK | t | Discuss whether ambition is always a positive quality. | When is ambition helpful? ; When can it be harmful? ; Give an example.
Fame and privacy | CO | t | Discuss whether famous people deserve privacy. | Why are people interested in celebrities? ; Where should the limits be? ; How has social media changed this?
City or countryside? | DL | t | Compare life in the city with life in the countryside. | What are the advantages of each? ; Which suits families better? ; Where would you prefer to live?
"""

PROMPTS["C1"] = """
Too many options | SH | r | We tend to assume that more choice makes us happier, yet faced with dozens of almost identical options, many people feel anxious rather than free. Sometimes a shorter list leads to a better decision. | Pause after happier. ; Stress anxious and free.
Heat in the city | EN | r | Dense cities trap heat in their concrete and asphalt, which is why temperatures in the centre can be several degrees higher than in the surrounding countryside. Planting trees is one of the simplest remedies. | Pause after asphalt. ; Stress several and simplest.
Feedback that helps | WK | r | Useful feedback is specific, timely and focused on actions rather than personality. Telling someone they are careless achieves little; showing them which steps they missed gives them something to work with. | Pause at the semicolon. ; Contrast careless with the steps they missed.
Memory and sleep | HE | r | Researchers have found that sleep plays an active role in memory. While we rest, the brain appears to replay and organise the day's experiences, strengthening what is worth keeping. | Stress active. ; Pause after rest.
The art of listening | CO | r | Genuine listening is rarer than we like to admit. Most of us are already preparing our reply while the other person is still speaking, which means we hear the words but miss the meaning. | Stress rarer and meaning. ; Pause after admit.
What travel can do | TR | r | Travelling rarely changes who we are overnight. What it can do is loosen our assumptions, showing us that habits we thought were universal are simply one way of living among many. | Pause after overnight. ; Stress loosen and universal.
Tasks, not jobs | TE | r | Automation tends to replace tasks rather than entire jobs. The people who adapt best are usually those who learn to work alongside new tools instead of competing with them. | Contrast tasks and entire jobs. ; Stress alongside.
Reading for pleasure | ED | r | Children who read for pleasure tend to do better at school, not only in language but across subjects. The habit seems to build vocabulary, concentration and curiosity at the same time. | Stress pleasure. ; Pause at each comma in the list.
The slow food movement | FD | r | The slow food movement began as a reaction against fast food, but it has grown into a broader argument about where our food comes from, who produces it and what it is worth. | Pause after food. ; Keep the three questions at the end even.
Transport and opportunity | TP | r | Reliable public transport is not just a matter of convenience. For people who cannot afford a car, it decides which jobs they can reach and how much of their day is spent travelling. | Stress convenience and afford. ; Pause after car.
In defence of boredom | DL | r | We rarely allow ourselves to be bored any more, reaching for our phones at the first quiet moment. Yet boredom may be exactly what the mind needs to wander and produce new ideas. | Pause after more. ; Stress exactly and wander.
Ageing well | HE | r | Ageing well depends less on avoiding every risk than on staying active, connected and curious. Older adults with strong social ties often report better health than those who live in isolation. | Pause at each comma. ; Stress connected and isolation.
Two languages, two selves | CO | r | Many bilingual people say they feel slightly different in each language, as if switching languages also switches their sense of humour, their gestures and even their opinions. | Stress different. ; Pause after language.
After the floods | PF | r | After the floods, volunteers arrived from all over the country. Their help was invaluable, although coordinating so many people turned out to be a challenge in itself. | Stress invaluable. ; Pause after invaluable.
Museums online | ED | r | Museums now publish thousands of images online, allowing anyone to explore their collections. Some feared this would keep visitors away, but early evidence suggests it does the opposite. | Pause after online. ; Stress opposite.
Water from the tap | EN | r | We often treat water as limitless because it flows from the tap at the turn of a handle. In many regions, however, underground reserves are being used faster than they can be refilled. | Pause after however. ; Stress limitless and faster.
Failing and starting again | MS | r | Most new businesses fail within a few years, but the founders often go on to succeed with later projects. What they learn from failure appears to be as valuable as any early funding. | Pause after years. ; Stress valuable.
The inner lives of animals | AN | r | Scientists were once reluctant to say that animals had emotions. Today, studies of elephants, dogs and even fish suggest that the inner lives of animals are richer than we assumed. | Stress reluctant and richer. ; Pause after Today.
A city's soundtrack | PT | r | Every city has its own soundtrack: the calls of street vendors, the rhythm of motorbikes, the bells of a distant temple. Visitors often remember these sounds long after they have forgotten the sights. | Pause at the colon. ; Keep the rhythm of the list steady.
What separates champions | HS | r | Top athletes are often admired for their talent, but what separates them is usually less visible: years of repetition, careful recovery and the discipline to rest when they would rather train. | Pause at the colon. ; Stress discipline.
Renting into our thirties | HF | r | In many countries, owning a home was once seen as a natural step into adulthood. Rising prices have made that step much harder, and many young people now rent well into their thirties. | Stress natural and harder. ; Pause after adulthood.
Winter light | NW | r | Shorter days in winter can affect people's energy and mood more than they expect. Spending time outdoors in daylight, even briefly, is one of the simplest ways to counter the effect. | Stress shorter and simplest. ; Pause after daylight.
Pause before you share | TE | r | False stories often spread faster than corrections because they are designed to provoke strong emotions. Pausing before sharing something shocking is a small habit with surprisingly large effects. | Stress faster and pausing. ; Pause after corrections.
What a mentor does | WK | r | A good mentor does not provide all the answers. Instead, they ask the kind of questions that help you discover what you already know and notice what you have been avoiding. | Stress answers and questions. ; Pause after Instead.
Patterns in history | ED | r | History does not repeat itself exactly, but patterns do recur. Studying them will not predict the future; it can, however, make us more alert to familiar warning signs. | Pause at the semicolon. ; Stress exactly and familiar.
Technology in the classroom | ED | t | Evaluate the role technology should play in education. | Where does it genuinely help learning? ; Where can it distract or replace thinking? ; How should teachers decide when to use it?
Global and local cultures | CO | t | Discuss whether globalisation threatens local cultures. | What is being lost? ; What is being gained? ; Can the two exist together?
Who protects the environment? | EN | t | Who should take the greatest responsibility for protecting the environment: governments, businesses or individuals? | Consider the power of each group. ; Give examples. ; Reach a conclusion.
Work in twenty years | WK | t | Discuss how work is likely to change in the next twenty years. | What skills will matter most? ; Which jobs may disappear? ; How should people prepare?
Success and happiness | PF | t | Discuss the relationship between success and happiness. | How do people define success? ; Does success guarantee happiness? ; What matters more to you?
Is privacy still possible? | TE | t | Discuss whether privacy is still possible in the digital age. | What information do we give away? ; Who benefits from it? ; What can individuals do?
Shopping with a conscience | SH | t | Discuss whether consumers can change company behaviour through what they buy. | What examples are there? ; What are the limits? ; How do you shop?
An ageing population | PF | t | Discuss the challenges and opportunities of an ageing population. | How will families be affected? ; What about the economy? ; How can older people contribute?
Spending on health | HE | t | Discuss how governments should decide where to spend healthcare money. | Prevention or treatment? ; Who should decide? ; What would you prioritise?
The city of the future | PT | t | Describe what an ideal city of the future would be like. | How would people move around? ; How would it handle growth? ; What would make it pleasant to live in?
Seeing the real culture | TR | t | Discuss whether tourists experience the real culture of the places they visit. | What do tourists usually see? ; What do they miss? ; How could travel be more meaningful?
The power of habits | HE | t | Explain how habits shape our lives and how they can be changed. | Give an example of a helpful habit. ; Why are habits hard to change? ; What strategies work?
Why false stories spread | TE | t | Discuss the causes of false information online and how societies should respond. | Why does false information spread? ; Who should deal with it? ; What can individuals do?
Changing expectations of men and women | PF | t | Discuss how expectations of men and women have changed in your lifetime. | What has changed at home? ; What has changed at work? ; What still needs to change?
Cheap food and animal welfare | AN | t | Discuss the balance between cheap food and the welfare of farm animals. | Why is cheap meat so common? ; What are the costs? ; What should consumers and governments do?
Competition or cooperation at school | ED | t | Discuss whether schools should encourage competition or cooperation. | What does each teach? ; What are the risks? ; Which should come first?
Influencers and young people | CO | t | Discuss the influence that celebrities and online influencers have on young people. | Is it mostly positive or negative? ; Why are people influenced? ; Should influencers have responsibilities?
Has money become too important? | MS | t | Discuss whether money has become too important in modern life. | Where do you see this? ; What are the effects? ; How can people keep a balance?
Mistakes at work | WK | t | Discuss how organisations should treat mistakes made by their staff. | What happens when mistakes are punished? ; What happens when they are discussed openly? ; Give an example.
City and country opportunities | DL | t | Discuss the gap in opportunities between cities and rural areas. | What differences exist? ; Why do they matter? ; How could they be reduced?
Sport and national identity | HS | t | Discuss why sport matters so much to national identity. | Give examples. ; Is it healthy? ; When does it go too far?
Adapting to a changing climate | NW | t | Discuss how communities can adapt to a changing climate. | What risks do they face? ; What practical measures exist? ; Who should pay?
Where we live and how we feel | HF | t | Discuss how the place where we live affects our wellbeing. | Space, light or location: what matters most? ; How does housing affect families? ; What should planners consider?
Public money for the arts | ED | t | Discuss whether public money should be spent on the arts. | What do the arts offer society? ; What are the competing priorities? ; What is your view?
The internet in remote places | TE | t | Discuss how internet access changes life in remote communities. | What opportunities does it create? ; What risks are there? ; Should access be a right?
"""

PROMPTS["C2"] = """
A careful "it depends" | ED | r | Experts are often most persuasive when they sound certain, yet the most honest answer to a complex question is frequently a qualified one. Learning to trust a careful "it depends" may be one of the subtler skills of adult life. | Pause after certain. ; Stress honest and qualified.
The translator's balance | CO | r | A translator is forever negotiating between faithfulness and readability. Render a sentence too literally and it sounds foreign; adapt it too freely and the author's voice disappears beneath the translator's own. | Pause at the semicolon. ; Contrast literally and freely.
When attention is the product | TE | r | When a service is free, our attention is usually the product being sold. Every notification competes for a resource that is finite, and the companies that capture it most effectively are rewarded handsomely. | Pause after sold. ; Stress finite and handsomely.
The selective past | DL | r | Nostalgia is curiously selective. It edits out the inconvenience and anxiety of the past, leaving a softened version that can make the present seem poorer than it really is. | Stress selective. ; Pause after past.
Layers of a city | PT | r | Old cities resemble manuscripts that have been written over many times. Beneath a modern shopping street you may find the outline of a medieval market, and beneath that, traces of a settlement no one remembers. | Pause after times. ; Keep a steady rhythm through the long sentence.
The hidden cost of flexibility | WK | r | Flexibility at work is generally welcomed, but it carries a hidden cost: when every hour could be working time, it becomes harder to justify any hour that is not. | Pause at the colon. ; Stress hidden and justify.
Speaking about uncertainty | HE | r | Patients often want a definite diagnosis, while doctors must weigh probabilities. Communicating that uncertainty honestly, without causing unnecessary alarm, is one of the most demanding parts of medical practice. | Contrast definite and probabilities. ; Pause after honestly.
Stepping back from nature | EN | r | Rewilding asks a provocative question: what if, instead of managing nature so tightly, we stepped back and allowed natural processes to reshape the land? The answer, in several projects, has been a surprising return of wildlife. | Pause at the colon. ; Stress provocative and surprising.
Stage sets for tourists | TR | r | Travel broadens the mind, we are told, but mass tourism can also flatten the places it celebrates. Neighbourhoods become stage sets, and the residents who gave them character are gradually priced out. | Pause after told. ; Stress broadens and flatten.
Private fortunes, public problems | MS | r | Generous donations by the very rich are rightly welcomed, yet they raise an uncomfortable question about accountability: should private fortunes decide which public problems receive attention first? | Pause after welcomed. ; Stress accountability.
Persuasion that does not feel like it | CO | r | The most effective persuasion rarely feels like persuasion at all. It works by framing a choice so that one option seems natural and the other faintly unreasonable. | Stress rarely and framing. ; Pause after all.
The notes left out | HS | r | Musicians often say that the notes they leave out matter as much as those they play. A well-placed silence gives the listener time to anticipate, and anticipation is half the pleasure of music. | Stress leave out. ; Pause after anticipate.
Recipes and memory | FD | r | What we eat is rarely just a matter of taste. Recipes carry memories of migration, scarcity and celebration, which is why a single dish can provoke surprisingly fierce arguments about authenticity. | Pause after taste. ; Stress fierce.
The promise of merit | WK | r | A meritocracy promises that talent and effort will be rewarded. Its critics point out, however, that those who succeed often credit their own merit while overlooking the advantages that smoothed their path. | Pause after however. ; Stress merit and advantages.
What data cannot explain | TE | r | Data can describe what people do with remarkable precision, but it struggles to explain why they do it. Without that understanding, decisions based purely on numbers risk being efficient and wrong at the same time. | Contrast what and why. ; Stress efficient and wrong.
Learning to judge danger | PF | r | Children today are supervised more closely than any previous generation. The intention is protective, but some researchers argue that free play, with its small risks, is precisely how children learn to judge danger. | Pause after protective. ; Stress precisely.
Monuments and memory | ED | r | Monuments tell us less about the past than about the people who chose to build them. Each statue reflects a decision about who deserved to be remembered and, by implication, who did not. | Stress less and implication. ; Pause after them.
Judging a fish by climbing | AN | r | Measuring animal intelligence by human standards is a little like judging a fish by its ability to climb a tree. Each species has developed the abilities its environment demanded. | Pause after standards. ; Stress developed.
The winters we remember | NW | r | Oddly, we remember the weather of our childhood as more extreme than the records suggest: summers longer, snow deeper. Memory, it seems, prefers a good story to an accurate one. | Pause at the colon. ; Contrast a good story and an accurate one.
How a house becomes a home | HF | r | A house becomes a home not through its furniture but through repetition: the same chair by the window, the same creak on the stairs, the familiar sounds of other people moving through the rooms. | Pause at the colon. ; Keep the list flowing.
The hours lost travelling | TP | r | Long commutes are one of the few costs people consistently underestimate when choosing where to live. A larger house rarely makes up for the hours lost every week travelling to and from it. | Stress underestimate and rarely. ; Pause after live.
The engine of science | ED | r | Doubt is often treated as a weakness, but in science it is the engine of progress. A theory earns our confidence only after surviving determined attempts to prove it wrong. | Pause after weakness. ; Stress engine and surviving.
Experts and beginners | WK | r | The more people learn about a field, the more aware they become of what they do not know. Genuine experts are therefore often more cautious in their claims than confident beginners. | Stress more and cautious. ; Pause after field.
Suggestion, not statement | SH | r | Advertising rarely lies outright; it prefers suggestion. A product is placed beside happiness, freedom or success, and the viewer is left to draw the connection that the advertiser cannot legally state. | Pause at the semicolon. ; Stress suggestion and legally.
A few kilometres apart | HE | r | Life expectancy can differ by years between neighbourhoods only a few kilometres apart. Such gaps reflect not personal choices alone but housing, income, education and access to care. | Pause after apart. ; Stress alone.
Can anyone be objective? | ED | t | Discuss whether journalists, historians or scientists can ever be fully objective. | What influences their work? ; Is objectivity still a useful goal? ; How should audiences respond?
How much do we control? | PF | t | Discuss how much control people really have over the course of their lives. | Consider background, chance and choice. ; Give examples. ; Present a nuanced view.
When AI causes harm | TE | t | Discuss who should be responsible when an artificial intelligence system causes harm. | The developers, the users or the owners? ; How should the rules be made? ; Give a realistic example.
Exchange or appropriation? | CO | t | Discuss where the line lies between cultural exchange and cultural appropriation. | Give examples of each. ; Who should decide? ; Does intention matter?
Growth and the planet | EN | t | Discuss whether endless economic growth is compatible with protecting the planet. | Present the main arguments. ; Consider alternatives. ; State your position.
What is education for? | ED | t | Discuss what the main purpose of education should be. | Jobs, citizenship or personal growth? ; How do these conflict? ; How should schools balance them?
A lie to protect feelings | CO | t | Discuss whether it is ever right to lie to protect someone's feelings. | Give examples. ; Consider the consequences. ; Where would you draw the line?
Reducing inequality | MS | t | Discuss the causes of inequality and whether it can be reduced without harming the economy. | Identify the causes. ; Evaluate policies. ; Consider the trade-offs.
Editing human genes | HE | t | Discuss the ethical questions raised by changing human genes. | Medical treatment or improvement? ; Who should decide? ; What are the risks?
Meaning or income? | WK | t | Discuss whether work should provide meaning or simply an income. | What do people expect from work? ; Is meaningful work a privilege? ; How has this changed?
Security and privacy | TE | t | Discuss the trade-off between public security and personal privacy. | Where is surveillance justified? ; What are the dangers? ; Who should oversee it?
Remembering painful history | ED | t | Discuss how societies should remember painful parts of their history. | Why is remembering important? ; What forms can remembrance take? ; How should disagreements be handled?
Should animals have rights? | AN | t | Discuss whether animals should have legal rights. | What would rights mean in practice? ; What are the objections? ; Where do you stand?
What algorithms decide | TE | t | Discuss how algorithms shape what people see, think and buy. | Give examples. ; What are the benefits and risks? ; Should algorithms be more transparent?
Is some art better than other art? | HS | t | Discuss whether some art is objectively better than other art. | What makes art good? ; Is taste purely personal? ; How do experts judge?
A global food system | FD | t | Discuss the cultural and environmental effects of a global food system. | What has been gained? ; What has been lost? ; What would a better system look like?
Leaving and arriving | TR | t | Discuss the effects of migration on both the countries people leave and the countries they join. | Consider the economic effects. ; Consider the cultural effects. ; Avoid generalisation.
Born or made leaders? | WK | t | Discuss whether good leaders are born or made. | What qualities matter? ; Can they be learned? ; Give examples.
Lonely in a crowd | PT | t | Discuss why people can feel lonely in crowded cities. | What causes it? ; How does city design matter? ; What could help?
We are what we buy? | SH | t | Discuss how far people's identities are shaped by what they buy. | Give examples. ; Is this new? ; Is it harmful?
Who pays for climate damage? | NW | t | Discuss who should pay for the damage caused by climate change. | Past responsibility or present ability? ; How should poorer countries be supported? ; Is fairness achievable?
A home or an investment? | HF | t | Discuss whether housing should be treated as a human right rather than an investment. | What would change? ; What are the risks? ; What is your view?
Trust in science | HE | t | Discuss why public trust in science varies and how it could be strengthened. | What damages trust? ; What role do the media play? ; What should scientists do differently?
Between generations | PF | t | Discuss the tensions between generations and how they could be eased. | Where do generations disagree? ; Are the differences exaggerated? ; What could bring them together?
Too fast to live well? | DL | t | Discuss whether modern life has become too fast, and what we lose as a result. | Give examples of speed in daily life. ; What are the costs? ; Is slowing down realistic?
"""


def main():
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "speaking.json"
    original = [p for p in json.loads(path.read_text(encoding="utf-8")) if int(p["id"][1:]) <= 16]
    out = list(original)
    n = 16
    for level, block in PROMPTS.items():
        for line in filter(None, (l.strip() for l in block.strip().splitlines())):
            title, topic, mode, text, cues = (part.strip() for part in line.split(" | "))
            items = [c.strip() for c in cues.split(" ; ")]
            assert len(items) >= (2 if mode == "r" else 3) and all(items), title
            n += 1
            out.append({"id": f"s{n}", "title": title, "level": level, "topic": TOPICS[topic],
                        "mode": MODES[mode], "text": text, "cues": items})
    titles = [p["title"].lower() for p in out]
    assert len(set(titles)) == len(titles), sorted({t for t in titles if titles.count(t) > 1})
    for level in PROMPTS:
        for mode in MODES.values():
            count = sum(1 for p in out if p["level"] == level and p["mode"] == mode)
            assert count == 25, (level, mode, count)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "prompts", {lv: sum(1 for p in out if p["level"] == lv) for lv in LEVELS})


main()

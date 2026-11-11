"""Writes src/data/writing.json: the ten original prompts (w1-w10) plus prompts written for EnglishUp
on 2026-11-11 so that every level from A1 to C2 has 50 writing tasks.

Each line is: title | topic code | genre code | prompt | checklist items separated by " ; ".
Word ranges grow with the level. Run: python scripts/create-writing-prompts.py
"""
import json
import pathlib

TOPICS = {
    "DL": "Daily life", "TR": "Travel", "WK": "Work", "FD": "Food", "HE": "Health", "TE": "Technology",
    "EN": "Environment", "ED": "Education", "SH": "Shopping", "CO": "Communication", "PF": "People and family",
    "HS": "Hobbies and sport", "TP": "Transport", "NW": "Nature and weather", "HF": "Home and furniture",
    "PT": "Places in town", "MS": "Money and shopping", "AN": "Animals",
}
GENRES = {"e": "email", "o": "opinion", "d": "description", "s": "story"}
WORDS = {"A1": (30, 60), "A2": (60, 100), "B1": (100, 160), "B2": (160, 250), "C1": (220, 320), "C2": (280, 400)}

PROMPTS = {}

PROMPTS["A1"] = """
About me | PF | d | Write about yourself. Give your name, your age, where you live and one thing you like. | Say your name and age. ; Say where you live. ; Add one thing you like.
My best friend | PF | d | Describe your best friend. Write what your friend looks like and what you do together. | Give your friend's name. ; Describe how your friend looks. ; Say one thing you do together.
My bedroom | HF | d | Describe your bedroom. Write about the furniture, the colours and your favourite thing in the room. | Name three pieces of furniture. ; Use colour words. ; Say your favourite thing and why.
Can I borrow your book? | CO | e | Write a short message to a classmate. Ask to borrow a book and say when you can give it back. | Start with "Hi" and the name. ; Ask politely with "Can I...?". ; Say a day to give it back.
My morning | DL | d | Write about what you do every morning, from getting up to leaving home. | Use the present simple. ; Use first, then and after that. ; Write at least five actions.
My favourite food | FD | o | What is your favourite food? Write what it is, when you eat it and why you like it. | Name the food. ; Say when you eat it. ; Give one reason with "because".
A postcard from the beach | TR | e | You are on holiday at the beach. Write a postcard to a friend about the weather, the hotel and what you do. | Write about the weather. ; Describe the hotel. ; Say two things you do.
The people in my family | PF | d | Write about the people in your family. Say who they are and one thing about each person. | Name each person. ; Use "is" and "has". ; Write one fact about each person.
A day at my school | ED | d | Write about a normal day at your school or class. What subjects do you have, and which one do you like? | Name your subjects. ; Say your favourite subject and why. ; Use the present simple.
Last weekend | DL | s | Write about what you did last weekend. Use the past simple. | Use past verbs such as went, played and ate. ; Say where you went. ; Say how you felt.
A shopping list for a party | SH | d | You are having a small party. Write a shopping list and say why you need some of the things. | List at least five things. ; Use numbers or "some". ; Say why you need two of them.
My town | PT | d | Describe your town. What places are there, and where do you like to go? | Name four places. ; Use "there is" and "there are". ; Say your favourite place.
Come to my birthday party | CO | e | Invite a friend to your birthday party. Say the day, the time and the place. | Say what the party is for. ; Give the day, time and place. ; Ask your friend to reply.
The weather today | NW | d | Describe the weather today and say what you want to do because of it. | Say what the weather is like. ; Use words like sunny, cold or windy. ; Say one thing you want to do.
A pet I like | AN | d | Describe your pet, or a pet you would like to have. Say what it looks like and what it eats. | Name the animal. ; Describe its size and colour. ; Say what it eats.
How I get to school | TP | d | Write how you travel to school or work every day. Say how long it takes and what you see on the way. | Say how you travel. ; Say how long it takes. ; Name two things you see.
Thank you for your help | CO | e | Write a short note to thank a neighbour who helped you carry your bags. | Say thank you at the start. ; Say what the neighbour did. ; End with a kind sentence.
My favourite sport | HS | o | What sport do you like to play or watch? Write why you like it and when you play or watch it. | Name the sport. ; Say when you play or watch it. ; Give a reason with "because".
A healthy day | HE | d | Write about a healthy day: what you eat, what you drink and what you do to stay well. | Name healthy food and drinks. ; Name one activity. ; Use times of the day.
My phone | TE | d | Describe your phone or computer. What do you use it for every day? | Describe how it looks. ; Write three things you use it for. ; Say if you like it.
Dinner at a restaurant | FD | s | Write a short story about a visit to a restaurant. What did you order, and was it good? | Say who you went with. ; Say what you ordered. ; Say if the food was good.
A job I like | WK | o | Which job do you like? Write what this worker does and why you want the job. | Name the job. ; Say what the worker does. ; Give one reason.
My English class | ED | d | Describe your English class: the teacher, the classroom and what you do in class. | Describe the teacher. ; Describe the room. ; Say two things you do in class.
I lost my bag | TR | e | You lost your bag on a bus. Write a message to the bus company. Describe the bag and say what is in it. | Say when and where you lost it. ; Describe the bag. ; List what is in it.
A clean street | EN | o | Is your street clean? Write two things people can do to keep it clean. | Say if your street is clean. ; Give two ideas. ; Use "can" or "should".
A family photo | PF | d | Describe a family photo. Who is in it, where are they, and what are they doing? | Say who is in the photo. ; Say where they are. ; Use the present continuous.
My favourite clothes | SH | d | Describe your favourite clothes. Say the colours and when you wear them. | Name the clothes. ; Use colour words. ; Say when you wear them.
My hobby | HS | d | Write about your hobby. When did you start it, and how often do you do it? | Name your hobby. ; Say when you started. ; Say how often you do it.
A rainy afternoon | NW | s | Write a short story about a rainy afternoon. What happened, and what did you do? | Use the past simple. ; Say where you were. ; Say what you did.
I am ill today | ED | e | You are ill today. Write a short message to your teacher. Say why you cannot come and ask for the homework. | Say you are ill. ; Say you cannot come. ; Ask about the homework.
My kitchen | HF | d | Describe your kitchen and say what you like to cook there. | Name things in the kitchen. ; Use "there is" or "there are". ; Say what you cook.
Hello from Viet Nam | CO | e | Write a first message to a new online friend in another country. Tell them about yourself and ask two questions. | Say hello and your name. ; Write two facts about you. ; Ask two questions.
Plans for Saturday | DL | e | Write a message to a friend about your plans for Saturday and invite them to join you. | Say your plans. ; Invite your friend. ; Give a time to meet.
The shop near my home | SH | d | Describe a market or shop near your home. What can you buy there? | Say where it is. ; Name four things you can buy. ; Say if it is cheap or expensive.
The best day of the week | DL | o | Which day of the week do you like best? Write why. | Name the day. ; Say what you do on that day. ; Give a reason.
A trip by train | TP | s | Write about a train or bus trip you took. Where did you go, and what did you see? | Say where you went. ; Say how long the trip was. ; Name two things you saw.
My dream holiday | TR | d | Describe your dream holiday. Where do you want to go, and what do you want to do? | Name the place. ; Use "I want to" or "I would like to". ; Name three activities.
At the doctor's | HE | s | Write about a time you visited the doctor. What was wrong, and what did the doctor say? | Say what was wrong. ; Say what the doctor said. ; Say how you felt after.
A park I know | EN | d | Describe a park or garden you know. What plants and trees are there, and what do people do there? | Name the park. ; Describe the plants and trees. ; Say what people do there.
The app I use most | TE | o | Which app do you use most? Write what it does and why you like it. | Name the app. ; Say what it does. ; Give two reasons you like it.
My breakfast | FD | d | Describe your breakfast. What do you eat and drink, and who makes it? | Name your food and drink. ; Say what time you eat. ; Say who makes it.
A busy day for a nurse | WK | s | Write about a busy day for a worker you know, such as a nurse or a shop assistant. | Name the job. ; Use the past simple. ; Write three things the worker did.
My neighbour | PF | d | Describe one of your neighbours. What does your neighbour do, and are you friends? | Describe the neighbour. ; Say their job or hobby. ; Say if you are friends.
A present for Mum | SH | e | Write a message to your brother or sister about a present for your mother. Suggest one present and its price. | Suggest a present. ; Give the price. ; Ask for their opinion.
Sports day at school | HS | s | Write about a sports day or a game you played at school. | Say what game it was. ; Say who played. ; Say who won.
My favourite season | NW | o | Which season do you like best? Write about the weather and the things you do then. | Name the season. ; Describe the weather. ; Say two things you do.
How to find my house | CO | e | A friend is coming to your home for the first time. Write a message telling them how to get there from the bus stop. | Use turn left, turn right and go straight. ; Name one place on the way. ; Say the house number or colour.
Drink more water | HE | o | Why is water important? Write how much water you drink and when you drink it. | Say why water is important. ; Say how much you drink. ; Say when you drink it.
Saving for something | MS | o | Do you save money? Write about one thing you want to buy and how you save for it. | Name the thing you want. ; Say how much it costs. ; Say how you save.
A new café in town | PT | d | A new café opened in your town. Describe it and say if you want to go there. | Say where it is. ; Describe the café. ; Say if you want to go.
"""

PROMPTS["A2"] = """
A school trip I remember | ED | s | Write about a class trip you remember. Where did you go, what did you do, and what was the best part? | Use the past simple. ; Say where and when you went. ; Describe the best moment.
I need a new appointment | HE | e | Write an email to a dental clinic. You cannot come to your appointment on Tuesday. Explain why and ask for a new time. | Say which appointment you have. ; Give a short reason. ; Suggest two other times.
My neighbourhood has changed | PT | d | Describe how your neighbourhood has changed in the last few years. What is new, and what has stayed the same? | Use the present perfect for changes. ; Mention at least two new things. ; Say how you feel about the changes.
An app I could not live without | TE | d | Describe an app you use often. Explain what it does, how often you use it and one thing you would change. | Name the app and its main use. ; Say how often you use it. ; Suggest one improvement.
My first online order | SH | s | Write about a time you bought something online. Did it arrive on time, and were you happy with it? | Say what you bought and why. ; Describe the delivery. ; Say whether you would buy there again.
Alone or with a roommate? | HF | o | Is it better to live alone or with a roommate? Give your opinion with two reasons. | State your opinion clearly. ; Give two reasons. ; End with a short conclusion.
Thank you, host family | TR | e | You stayed with a host family abroad. Write an email to thank them and say what you enjoyed most. | Thank them at the start. ; Mention two things you enjoyed. ; Invite them to visit you.
My first day at work | WK | s | Write about your first day at a job or a new class. What happened, and how did you feel at the end of the day? | Describe the place and the people. ; Say what you did. ; Describe your feelings.
The gym near my house | HS | d | Describe a sports club or gym near your home: the place, the activities and the price. | Describe the place. ; Name three activities. ; Say if it is good value.
Eating out or cooking at home? | FD | o | Do you prefer eating at restaurants or cooking at home? Explain why. | Give your choice. ; Compare cost and health. ; Use "better" or "cheaper than".
Welcome to the team | WK | e | A new colleague starts next week. Write an email to welcome them and explain three things about the office. | Welcome the colleague. ; Explain three things about the office. ; Offer help.
The best present I ever got | PF | s | Write about the best present you have ever received. Who gave it to you, and why was it special? | Say who gave it and when. ; Describe the present. ; Explain why it was special.
Rules in our home | PF | d | Describe the rules in your home, for example about chores, screens or bedtime. Do you think they are fair? | Describe three rules. ; Use "have to" and "can't". ; Say whether they are fair.
Wrong size shoes | SH | e | You received the wrong size shoes from an online shop. Write an email to explain the problem and ask for a change. | Give your order details. ; Explain the problem. ; Say what you want the shop to do.
Where I relax | DL | d | Describe a place where you relax. What can you see and hear there? | Say where it is. ; Use words for sounds and sights. ; Say why it helps you relax.
Recycling bins in every classroom | EN | o | Should every school have recycling bins in each classroom? Give your opinion and one example. | Give your opinion. ; Give one example. ; Mention one possible problem.
The day everything went wrong | TR | s | Write about a trip where something went wrong, such as a late train or a lost ticket. How did you solve the problem? | Describe the problem. ; Say what you did. ; Say what you learned.
Learning something new | ED | d | Describe a skill you are learning now, such as cooking or playing the guitar. How do you practise? | Name the skill. ; Describe how you practise. ; Say what is difficult.
Tips for a tired friend | HE | e | Your friend feels tired all the time. Write an email with three pieces of advice. | Show that you care. ; Give three pieces of advice. ; Use "should" or "why don't you".
A festival in my country | DL | d | Describe a festival or holiday in your country: when it is, what people eat and what they do. | Say when it is. ; Describe the food. ; Describe two activities.
Online or in the classroom? | ED | o | Do you prefer online lessons or lessons in a classroom? Give two reasons. | Give your preference. ; Give two reasons. ; Mention one advantage of the other choice.
Booking a hotel room | TR | e | Write an email to a hotel to book a room for two nights. Ask about breakfast and parking. | Give the dates. ; Say what room you want. ; Ask two questions.
Someone I admire | PF | d | Describe a person you admire, such as a teacher or a relative. What do they do, and why do you admire them? | Say who the person is. ; Describe what they do. ; Give two reasons.
A walk in the hills | NW | s | Write about a walk in the countryside or a park. What did you see, and what happened? | Describe the place. ; Say what you saw. ; Say what happened.
Too much time on phones? | TE | o | Do young people spend too much time on their phones? Give your opinion with examples. | Give your opinion. ; Give two examples. ; Suggest one change.
My ideal home | HF | d | Describe your ideal home: where it is, how many rooms it has and what is special about it. | Say where it is. ; Describe the rooms. ; Describe one special thing.
Music after midnight | CO | e | Your neighbour plays loud music late at night. Write a polite note asking them to turn it down. | Be polite. ; Explain the problem. ; Suggest a solution.
A morning at the market | SH | s | Write about a visit to a busy market. What did you buy, and who did you talk to? | Describe the market. ; Say what you bought. ; Describe a conversation.
Buses and trains in my city | TP | d | Describe public transport in your city. Is it cheap, fast and clean? | Name the types of transport. ; Talk about price and speed. ; Say what could be better.
A lunch I like to make | FD | d | Describe a healthy lunch you like to make. What do you need, and how long does it take? | List the ingredients. ; Describe the steps. ; Say why it is healthy.
How can I join? | HS | e | Write an email to a club, for example a running or chess club, asking how to join, when they meet and how much it costs. | Say why you are writing. ; Ask three questions. ; End politely.
Saving electricity at home | EN | d | Describe three things your family does or could do to save electricity at home. | Describe three actions. ; Say why each one helps. ; Use "could" for new ideas.
The surprise | PF | s | Write a story about a surprise party or a surprise visit. Who planned it, and how did the person react? | Say who planned it. ; Describe the moment of surprise. ; Describe the reaction.
Should students work at weekends? | WK | o | Is it a good idea for students to work at weekends? Give your opinion with reasons. | Give your opinion. ; Give two reasons. ; Mention school work.
How I study | ED | d | Describe how and when you study. Where do you sit, and what helps you concentrate? | Say when you study. ; Describe the place. ; Give two things that help you.
The wallet on the bench | DL | s | Write a story about finding something that someone had lost. What did you do next? | Say what you found and where. ; Say what you did. ; Describe the ending.
Information about a course | ED | e | Write an email to a language school asking about class times, the price and the level test. | Introduce yourself. ; Ask about times, price and the test. ; Thank them.
My favourite café | FD | d | Describe a café you like: what it looks like, what you order and why you go there. | Describe the café. ; Say what you order. ; Say why you go there.
A day without the internet | TE | s | Imagine the internet stopped working for a whole day. Write what you did instead. | Describe the problem. ; Say what you did instead. ; Say how you felt.
Visiting a friend in hospital | HE | s | Write about visiting someone in hospital. What did you bring, and what did you talk about? | Say who you visited. ; Say what you brought. ; Describe the visit.
Should more people cycle? | TP | o | Should more people cycle to work or school? Give two advantages and one problem. | Give two advantages. ; Give one problem. ; Give your opinion.
A picnic on Sunday | DL | e | Write an email to friends to plan a picnic. Suggest a place, a time and what each person should bring. | Suggest a place and time. ; Give each person a job. ; Ask them to reply.
The rainy season | NW | d | Describe the rainy season, or winter, where you live. How does it change daily life? | Describe the weather. ; Give two changes in daily life. ; Say if you like it.
Where my money goes | MS | d | Describe how you spend and save money each week. What do you spend most on? | Say what you spend money on. ; Say how you save. ; Say what you spend most on.
I forgot your birthday | CO | e | You forgot your friend's birthday. Write a message to say sorry and suggest a way to celebrate later. | Say sorry. ; Give a reason without excuses. ; Suggest a plan.
A teacher who helped me | ED | d | Describe a teacher who helped you. What did they do that was different? | Describe the teacher. ; Say what they did. ; Say how it helped you.
The best time to visit my country | TR | o | Which is the best time of year to visit your country? Explain why. | Name the season or month. ; Give two reasons. ; Suggest one place to visit.
"""

PROMPTS["B1"] = """
A late and damaged delivery | SH | e | An online order arrived two weeks late and one item was damaged. Write an email to the company describing what happened and what you expect them to do. | Give the order details and dates. ; Describe the damage clearly. ; Say whether you want a refund, a replacement or a discount.
Should homework be stopped? | ED | o | Some people think primary schools should stop giving homework. Do you agree? | State your view in the introduction. ; Give two supported reasons. ; Mention the other side briefly.
A place that surprised me | TR | d | Describe a place you visited that was very different from what you expected. | Say what you expected. ; Describe what you found. ; Explain how your opinion changed.
The day I helped a stranger | DL | s | Write a story about a time you helped a stranger, or a stranger helped you. | Set the scene. ; Describe the problem and the help. ; End with what you learned.
Applying for a summer job | WK | e | You saw an advertisement for a summer job at a café. Write an email applying for the job. | Say which job you are applying for. ; Describe relevant experience or qualities. ; Say when you are available.
Fast food and young people | FD | o | Fast food is popular with young people. Is this a problem? Give your opinion with examples. | Give your opinion. ; Use examples. ; Suggest one solution.
A family tradition | PF | d | Describe a tradition your family keeps, such as a special meal or a yearly trip. Explain why it matters to you. | Describe the tradition. ; Explain how it started. ; Say why it matters.
Something to watch this weekend | HS | e | A friend wants something to watch this weekend. Write an email recommending a film or series. | Name it and say what type it is. ; Describe it without spoiling the ending. ; Explain why your friend will enjoy it.
Home office or real office? | WK | o | Is working from home better than working in an office? Discuss the advantages and disadvantages. | Give advantages. ; Give disadvantages. ; Give your conclusion.
A difficult decision | PF | s | Write about a difficult decision you made, such as choosing a school or moving house. | Explain the choice. ; Describe your thinking. ; Say whether it was the right decision.
Ideas for our park | PT | e | Write an email to your local council suggesting improvements to a park in your area. | Describe the current problems. ; Suggest two improvements. ; Explain who would benefit.
Paying for plastic bags | EN | o | Should shops charge customers for plastic bags? | Give your opinion. ; Give two reasons. ; Respond to one objection.
An invention that changed habits | TE | d | Describe an invention that makes daily life easier and explain how it changed people's habits. | Name and describe the invention. ; Explain how it is used. ; Describe its effect on habits.
My best holiday memory | TR | s | Write about your best holiday memory. Include details that help the reader picture the place. | Use descriptive adjectives. ; Use past tenses correctly. ; Explain why it was memorable.
Two courses, one choice | CO | e | You have been offered places on two different courses. Write an email to a friend explaining the choice and asking for advice. | Describe both options. ; Explain what worries you. ; Ask a clear question.
Exercise during exams | HE | o | Some students say they have no time for exercise. Is exercise important even during exams? | Give your opinion. ; Use one personal example. ; Suggest a practical routine.
A market worth visiting | SH | d | Describe a market in your city for a visitor guide: what it sells, when to go and how to get there. | Describe what is sold. ; Give practical tips. ; Use a friendly guide style.
The train left without me | TP | s | Write a story that begins: "I watched the train leave without me." | Use the opening sentence. ; Build some tension. ; Give a clear ending.
Learning from free videos | ED | o | Can people learn a skill well using only free online videos? | Give your opinion. ; Mention quality and motivation. ; Give an example.
Thanks for your help on the project | WK | e | A colleague helped you finish an important project. Write an email to thank them and explain what difference their help made. | Thank them clearly. ; Explain the help. ; Describe the result.
A meal to remember | FD | s | Write about a meal you will never forget, for good or bad reasons. | Describe the setting. ; Describe the food. ; Explain why you remember it.
Pets in small flats | AN | o | Should people who live in small flats keep pets? | Give your opinion. ; Consider the animal's needs. ; Consider the neighbours.
My ideal weekend | DL | d | Describe your ideal weekend from Friday evening to Sunday night. | Organise it by time. ; Use "would" for imagined plans. ; Include a variety of activities.
Looking after the plants | CO | e | Your neighbour is going away and has asked you to look after their plants. Write an email accepting and asking what you need to know. | Accept the request. ; Ask three practical questions. ; Offer extra help.
Free museums for everyone? | ED | o | Should museums and galleries be free for everyone? | Give your opinion. ; Discuss the cost. ; Discuss the benefits for society.
A day in the life of a bus driver | WK | d | Describe a typical day for a bus driver, a farmer or another worker you know about. | Describe the routine. ; Mention the difficulties. ; Mention the rewards.
The evening the lights went out | DL | s | Write a story about an evening when the electricity went off in your building. | Set the scene. ; Describe how people reacted. ; End with a surprise or a lesson.
Changing my tour date | TR | e | You booked a tour for next Saturday, but you now need to change the date. Write to the tour company. | Give the booking details. ; Explain why. ; Suggest new dates and ask about fees.
Phones in lessons | TE | o | Should students be allowed to use smartphones during school lessons? | Give your opinion. ; Give two reasons. ; Suggest a fair rule.
A sport worth trying | HS | d | Describe a sport or activity you think everyone should try at least once. | Explain what it involves. ; Describe how it feels. ; Give advice for beginners.
Feedback on a short course | ED | e | You have just finished a short course. Write an email to the organisers giving feedback. | Say what you liked. ; Suggest one improvement. ; Keep a polite tone.
Life without a car | TP | o | Is it possible to live comfortably in your city without a car? | Give your opinion. ; Describe the transport options. ; Mention one difficulty.
A small act of kindness | PF | s | Write a story about a small act of kindness that changed someone's day. | Introduce the characters. ; Describe the act. ; Show its effect.
Better food in the canteen | HE | e | Write an email to your manager suggesting healthier food in the office canteen. | Explain the current situation. ; Suggest two changes. ; Explain the benefits.
My favourite room | HF | d | Describe your favourite room in your home and what makes it comfortable. | Describe the layout. ; Describe the atmosphere. ; Explain how you use it.
Buying second-hand | SH | o | Is buying second-hand clothes and furniture a good idea? | Give the advantages. ; Mention one risk. ; Give your opinion.
Lost in a new city | TR | s | Write a story about getting lost in a city you did not know. | Describe how you got lost. ; Describe who or what helped. ; Describe the ending.
Join our clean-up day | EN | e | Write an email to your neighbours inviting them to a community clean-up day. | Give the date, time and place. ; Explain what people will do. ; Encourage them to come.
The best way to learn new words | ED | o | What is the best way to learn new vocabulary in a foreign language? | Describe one or two methods. ; Explain why they work. ; Give a personal example.
A farewell party | WK | s | Write about a celebration at a workplace or school, such as an anniversary or a farewell party. | Describe the event. ; Describe one memorable moment. ; Explain why it mattered.
Weather and mood | NW | o | Does the weather affect people's mood? Give your opinion with examples. | Give your opinion. ; Give examples. ; Explain your reasons.
A weekend trip on a budget | MS | d | Describe how you would plan a budget for a weekend trip with friends. | List the main costs. ; Explain how to save money. ; Give a total estimate.
Friends you have never met | CO | o | Can online friendships be as strong as friendships in real life? | Give your opinion. ; Compare the two. ; Use an example.
A visit to the animal shelter | AN | s | Write a story about a visit to an animal shelter. | Describe the shelter. ; Describe one animal. ; Describe a decision.
Advice for a new student | ED | e | A new student is joining your class next week. Write an email with advice about the school and the teachers. | Welcome the student. ; Give three pieces of advice. ; Offer to meet.
Technology for my grandparents | TE | d | Describe how a piece of technology helps an older person you know in daily life. | Describe the person and the technology. ; Explain how it helps. ; Mention one difficulty.
"""

PROMPTS["B2"] = """
A four-day working week | WK | o | Some companies are trying a four-day working week. Discuss the benefits and drawbacks for employees and employers, and give your view. | Discuss benefits for both groups. ; Discuss drawbacks. ; Give a reasoned conclusion.
Cancelled classes | ED | e | You paid for an evening course, but classes were often cancelled. Write a formal complaint to the director. | Use a formal register. ; Give specific dates and facts. ; Request a clear remedy.
Tourism: blessing or burden? | TR | o | Mass tourism brings money but also problems to popular cities. To what extent should tourist numbers be limited? | Present both sides. ; Use specific examples. ; Give a balanced conclusion.
A street that remembers | PT | d | Describe a building or street in your city that shows its history. Explain what it reveals about the past. | Describe it vividly. ; Explain the history. ; Reflect on its meaning today.
The interview that went wrong | WK | s | Write a story about a job interview that did not go as planned. | Build tension. ; Use dialogue. ; Give a surprising or meaningful ending.
A quiet room for studying | ED | e | Write an email to your school or university director proposing a new quiet study space. | Explain the need. ; Describe the proposal. ; Address the cost and the benefits.
Advertising to children | FD | o | Should advertising for unhealthy food be banned during children's TV programmes? | Present arguments for and against. ; Support them with examples. ; State your position.
A restaurant review | FD | d | Write a review of a restaurant for a local website, covering the food, service, atmosphere and value. | Cover all four areas. ; Use precise adjectives. ; Give a clear recommendation.
The first month abroad | TR | s | Write a story about someone's first month living in a foreign country. | Show the character's feelings. ; Include a turning point. ; Use varied past tenses.
Fewer cars in the city | TP | o | What measures would most effectively reduce car use in cities? | Suggest at least two measures. ; Evaluate how effective they are. ; Consider objections.
A reference for a former colleague | WK | e | A former colleague has applied for a job and asked you for a reference. Write an email to the employer recommending them. | Explain how you know them. ; Describe their strengths with examples. ; Make a clear recommendation.
News from social media | TE | o | Many people now get their news from social media. Is this a positive development? | Discuss the advantages. ; Discuss risks such as false information. ; Conclude with your view.
A turning point | PF | s | Write about a moment that changed the direction of someone's life. | Establish the situation before. ; Describe the turning point. ; Show the consequences.
Parks or new homes? | EN | o | Should city planners give more land to parks even if it means fewer new homes? | Weigh both priorities. ; Use examples. ; Give your conclusion.
A festival for visitors | DL | d | Write an article for an international magazine describing a festival in your country for visitors. | Engage the reader at the start. ; Describe the sights, sounds and food. ; Give practical advice.
Higher rent, no repairs | HF | e | Your landlord wants to raise your rent while repairs remain undone. Write an email explaining your position. | Stay polite but firm. ; List the repairs. ; Propose a solution.
Do exams show what we know? | ED | o | Do exams measure what students have really learned? | Present your view. ; Discuss alternatives. ; Use examples.
The last bus home | TP | s | Write a story that begins: "The last bus home was almost empty, except for one passenger." | Use the opening line. ; Create atmosphere. ; Develop an unexpected ending.
Health apps and their limits | HE | d | Describe how health and fitness apps are changing the way people look after themselves, with their benefits and limitations. | Describe typical apps. ; Explain the benefits. ; Explain the limitations.
Volunteer with me | CO | e | Write an email persuading a friend to volunteer with you at a local charity. | Describe the charity. ; Give persuasive reasons. ; Answer likely doubts.
Who should stop fast fashion? | SH | o | Is fast fashion a problem that consumers or companies should solve? | Explain the problem. ; Discuss who is responsible. ; Give your view.
A performance I will not forget | HS | d | Describe a concert, play or sports match you saw and explain why it impressed you. | Set the scene. ; Describe the key moments. ; Explain its impact.
Will machines take our jobs? | TE | o | Will robots and artificial intelligence create more jobs than they destroy? | Present both views. ; Use examples. ; Give your prediction.
The letter that arrived too late | PF | s | Write a story about a letter that arrives many years late. | Describe the letter. ; Show the reactions. ; Give a meaningful ending.
Applying for a scholarship | ED | e | Write an email applying for a scholarship to study abroad, explaining your goals and why you deserve support. | State your goals. ; Give evidence of commitment. ; Explain the benefit to others.
Your first salary | MS | e | A younger relative has just started their first job. Write an email giving advice on managing money. | Give practical advice. ; Explain why it matters. ; Keep a friendly tone.
Do we still need zoos? | AN | o | Do zoos still have a role in protecting animals? | Discuss conservation. ; Discuss animal welfare. ; Give your view.
My street after dark | PT | d | Describe your neighbourhood at night, focusing on sounds, lights and people. | Use details from the senses. ; Organise the description clearly. ; Create a mood.
Working while studying | WK | o | Should university students work part-time? Discuss the effects on study, money and experience. | Discuss three effects. ; Use examples. ; Conclude clearly.
A mistake I learned from | PF | s | Write about a mistake that taught you something important. | Describe the mistake. ; Describe the consequences. ; Reflect on the lesson.
Organising a class reunion | CO | e | You are organising a reunion for former classmates. Write an email with the plan, asking for help. | Describe the plan. ; Give people tasks. ; Ask for replies by a date.
Can one person make a difference? | EN | o | Can individual choices make a real difference to climate change? | Discuss individual action. ; Discuss the role of governments and businesses. ; Give your view.
The night train | TR | d | Describe a long journey by night train or bus, focusing on the people and the atmosphere. | Describe the people. ; Describe the atmosphere. ; Show how the journey felt.
Online shopping and the high street | SH | o | Is online shopping destroying local shops, and does it matter? | Describe the trend. ; Discuss the effects on communities. ; Give your view.
The new coach | HS | s | Write a story about a coach or mentor who changed a team. | Introduce the team's problem. ; Describe the coach's methods. ; Show the result.
A website that frustrates users | TE | e | Write an email to a company explaining problems with its website and suggesting improvements. | Describe the problems. ; Suggest specific improvements. ; Explain the benefits.
Sleep or longer hours? | HE | o | Is getting enough sleep more important than working longer hours? | Give your view. ; Use evidence or examples. ; Address counterarguments.
A craft worth keeping | DL | d | Describe a traditional craft from your region and explain why it should be preserved. | Describe the craft. ; Explain its history. ; Argue for keeping it alive.
Teaching students to fail well | ED | o | Should schools teach students how to deal with failure? | Explain what this means. ; Give reasons. ; Suggest how to do it.
From the city to the fields | NW | s | Write a story about a city family that moves to the countryside. | Show their first expectations. ; Describe the challenges. ; Show how they adapt.
Save our library | CO | e | A local newspaper suggested closing the library to save money. Write an email to the editor giving your view. | State your view early. ; Support it with arguments. ; End with a call to action.
Cooking as a school subject | FD | o | Should cooking be a compulsory school subject? | Give your view. ; Discuss health and independence. ; Consider objections.
A home that tells a story | HF | d | Describe a home, real or imagined, whose objects tell the story of the people who live there. | Describe several objects. ; Link them to the people. ; Create a clear impression.
Are electric cars the answer? | TP | o | Are electric cars the answer to pollution from transport? | Discuss the benefits. ; Discuss the limitations. ; Give your view.
What makes a team work | WK | d | Describe what makes a team project succeed, using an example from your experience. | Describe the example. ; Identify the success factors. ; Draw a conclusion.
Before you adopt a dog | AN | e | Write an email to a friend who is thinking of adopting a dog, explaining the responsibilities. | Explain the time, cost and care involved. ; Be honest but encouraging. ; Ask about their plans.
Tips or fair wages? | MS | o | In some countries, waiters depend on tips. Should tipping be replaced by higher wages? | Explain the current system. ; Discuss both options. ; Give your conclusion.
"""

PROMPTS["C1"] = """
A basic income for all? | MS | o | Some governments are testing a universal basic income. Evaluate whether it would reduce poverty without discouraging work. | Define the idea briefly. ; Evaluate the likely effects on poverty and work. ; Reach a qualified conclusion.
How our city commutes | TP | d | Write a report for your city council on how residents commute, and recommend changes. | Use clear headings. ; Summarise the main patterns. ; Make specific recommendations.
Replying to a harsh review | WK | e | Your company received a harsh online review. Write a public reply that acknowledges the problem and restores trust. | Acknowledge the problem without being defensive. ; Explain what will change. ; Invite further contact.
What failure teaches | ED | o | "Failure teaches more than success." Discuss this statement with reference to education and work. | Interpret the statement. ; Use examples from both areas. ; Present a nuanced view.
A town that reinvented itself | PT | d | Describe a city or town that changed its economy or image, and analyse why the change worked or failed. | Describe the before and after. ; Analyse the causes. ; Draw a wider lesson.
The negotiation | WK | s | Write a story centred on a tense negotiation in which both sides have something to hide. | Establish both characters' aims. ; Use dialogue to build tension. ; Resolve the plot with a twist.
Paying with our data | TE | o | Are people right to trade personal data for free online services? | Explain the trade. ; Weigh convenience against risk. ; Recommend a position.
A mentoring scheme for new staff | ED | e | Write a formal email to your head of department proposing a mentoring scheme that pairs new and experienced staff. | Explain the problem it solves. ; Outline how it would work. ; Anticipate objections.
Local food or global choice? | FD | o | Should consumers prioritise locally produced food over imported products? | Consider environmental, economic and cultural factors. ; Use examples. ; Avoid oversimplification.
In praise of slow travel | TR | d | Write a magazine article encouraging readers to try slow travel, such as long train journeys or staying in one place for weeks. | Hook the reader. ; Use vivid examples. ; Address common objections.
What remote learning taught us | ED | o | What lasting lessons should schools take from periods of remote learning? | Identify specific lessons. ; Evaluate their importance. ; Make recommendations.
Writing to the energy regulator | CO | e | Your energy supplier has repeatedly overcharged you and ignored your complaints. Write to the regulator. | Summarise the history concisely. ; Include facts and dates. ; State the outcome you seek.
The architect's dilemma | PT | s | Write a story about an architect asked to design a building she believes will harm the neighbourhood. | Present the dilemma clearly. ; Develop the character's inner conflict. ; Show the consequence of her choice.
Whose job is wellbeing at work? | HE | o | Who is responsible for employees' mental health: the employer or the individual? | Define the issue. ; Discuss both responsibilities. ; Propose practical measures.
A thought-provoking book | ED | d | Write a review of a non-fiction book you found thought-provoking, assessing its argument and style. | Summarise the main argument. ; Evaluate the evidence and the style. ; Recommend it to a particular reader.
Plastic-free supermarkets | EN | o | Should supermarkets be required to stop using single-use plastic packaging within five years? | Assess whether it is feasible. ; Discuss costs and benefits. ; Give a reasoned view.
Dear sixteen-year-old me | PF | e | Write a letter to yourself at sixteen, giving advice based on what you know now. | Keep a consistent, reflective tone. ; Give specific advice. ; Avoid clichés.
Sport and national pride | HS | o | Why do international sporting events matter so much to national identity, and is this healthy? | Explain the connection. ; Evaluate positive and negative effects. ; Conclude thoughtfully.
The market at dawn | SH | d | Describe a wholesale market at dawn for a travel anthology, capturing the people and the rhythm of work. | Use precise sensory detail. ; Convey movement and rhythm. ; Keep a consistent point of view.
The safety report | WK | s | Write a story about an employee who discovers that her company is hiding a safety problem. | Establish the stakes. ; Show the pressure on the character. ; End with ambiguity or resolution.
Societies growing older | PF | o | How should societies adapt to a rapidly ageing population? | Identify the key challenges. ; Propose solutions. ; Evaluate their trade-offs.
A case for flexible hours | WK | e | Write a formal request to your manager for a flexible working arrangement, making a business case for it. | Propose a specific arrangement. ; Show the benefit to the team. ; Address possible concerns.
Does handwriting still matter? | ED | o | Does it matter if children write less by hand? | Consider learning and practical arguments. ; Use examples. ; Give a balanced conclusion.
What the festival left behind | DL | d | Write a report assessing the economic and social impact of a large festival on a small town. | Organise it under headings. ; Present benefits and costs. ; Recommend improvements.
Bridges for wildlife | AN | o | Should new roads and railways be required to include wildlife crossings, even at high cost? | Explain the problem. ; Weigh cost against benefit. ; Give your view.
We missed the deadline | CO | e | Your team missed a deadline that affected a client. Write an email of apology that explains, takes responsibility and proposes a fix. | Take responsibility clearly. ; Explain without making excuses. ; Propose concrete next steps.
The inheritance | PF | s | Write a story in which siblings disagree over an unexpected inheritance. | Develop distinct characters. ; Use dialogue to reveal tension. ; Resolve or deepen the conflict.
Do algorithms narrow our taste? | TE | o | Do recommendation algorithms narrow our cultural tastes? | Explain in general terms how they work. ; Present arguments on both sides. ; Conclude with your view.
Somewhere for teenagers to go | PT | e | Write to the local council arguing for public spaces designed for teenagers. | Explain the current gap. ; Propose specific spaces. ; Anticipate concerns.
An unsung hero | PF | d | Write a profile for a community magazine of someone whose work goes unnoticed, such as a cleaner or a volunteer. | Describe the person vividly. ; Explain their contribution. ; Convey why it matters.
Breaking a promise | CO | o | Is it ever right to break a promise? Discuss with examples. | Define the issue. ; Use examples. ; Present a nuanced position.
The storm | NW | s | Write a story set during a storm that forces strangers to depend on each other. | Create atmosphere. ; Develop relationships under pressure. ; Give a satisfying ending.
A region running out of water | EN | d | Write an article explaining how a region facing water shortages could manage its supply better. | Explain the causes. ; Describe possible measures. ; Evaluate how feasible they are.
Disappointing leadership training | WK | e | Your company paid for leadership training that disappointed staff. Write constructive feedback to the provider. | Be specific about the problems. ; Acknowledge strengths. ; Suggest improvements.
A gap year: waste or gift? | ED | o | Is taking a gap year before university a waste of time or a valuable experience? | Discuss benefits and risks. ; Consider different students. ; Conclude clearly.
A neighbourhood in transition | PT | d | Describe a neighbourhood that is changing as new residents arrive, showing both gains and losses. | Describe concrete changes. ; Present different perspectives. ; Avoid a one-sided judgement.
One sentence to translate | CO | s | Write a story about an interpreter who realises a negotiation depends on how she translates one sentence. | Establish the setting. ; Build tension around the sentence. ; Show the consequence.
The price of medicine | HE | o | Should governments control the prices of essential medicines? | Explain the issue. ; Discuss arguments on both sides. ; Give your view.
Pitching to investors | MS | e | Write an email to potential investors presenting a small business idea and explaining why it will succeed. | Describe the idea and the market. ; Give evidence of demand. ; State what you need.
Is meat harder to justify? | FD | o | Is eating meat becoming harder to justify? | Consider ethical, environmental and cultural views. ; Use evidence. ; Give your position.
Reviewing a public service | DL | d | Write a review of a public service you use, such as a library or clinic, assessing what works and what does not. | Describe the service. ; Assess strengths and weaknesses. ; Recommend changes.
The comeback | HS | s | Write a story about an athlete returning after a serious injury. | Show the setback. ; Show the struggle. ; Give a believable ending.
No cars in the centre | TP | e | Write to a newspaper responding to a plan to ban private cars from the city centre. | State your position. ; Support it with arguments. ; Consider the groups affected.
Screens and young children | TE | o | How much should parents limit young children's screen time? | Discuss research and practical concerns. ; Consider different families. ; Give advice.
Moving for work | WK | d | Describe the experience of relocating to a new city for work, and what helps people settle. | Describe the challenges. ; Describe what helps. ; Draw a conclusion.
Fairer exams | ED | e | Write to an exam board about how its tests could be made fairer for students with disabilities. | Identify the problems. ; Propose adjustments. ; Explain the benefits.
Who does volunteering abroad help? | TR | o | Does short-term volunteering abroad help communities, or mainly the volunteers? | Present both perspectives. ; Use examples. ; Suggest better practice.
The village that refused | NW | s | Write a story about a village that refuses to leave its land when a dam is planned. | Present the community. ; Show the conflict. ; Give a powerful ending.
Buy less, buy better | SH | o | Would people be happier if they bought fewer but higher-quality things? | Explain the idea. ; Evaluate it. ; Give your view.
The staff wellbeing survey | HE | d | Write a report summarising a staff wellbeing survey and recommending three actions. | Summarise the findings. ; Identify the priorities. ; Recommend three actions.
"""

PROMPTS["C2"] = """
The limits of merit | WK | o | "A society that rewards only merit will become less fair, not more." Discuss. | Interpret the claim precisely. ; Engage with counterarguments. ; Reach a nuanced conclusion.
An open letter on summer heat | EN | e | Write an open letter to your city's mayor about rising summer temperatures and how the city should adapt. | Establish urgency with evidence. ; Propose prioritised measures. ; Keep a persuasive but measured tone.
The narrator who lies | PF | s | Write a story told by a narrator whose account the reader gradually learns not to trust. | Plant subtle clues. ; Control the reveal. ; Keep the voice consistent.
Statues of the past | ED | o | Should public monuments to controversial historical figures be removed? | Distinguish history from commemoration. ; Consider different communities. ; Propose a principled approach.
What translation loses and gains | CO | d | Write an essay on what is lost and what can be gained when literature is translated. | Use precise examples. ; Engage with the idea of faithfulness. ; Develop an original argument.
Responding to a sugar tax consultation | HE | e | A government is consulting on a sugar tax. Write a formal response on behalf of a public health charity. | Summarise your organisation's position. ; Use evidence and anticipate objections. ; Make specific recommendations.
Nostalgia and progress | DL | o | Is nostalgia an obstacle to progress or a necessary check on it? | Define both terms carefully. ; Use cultural or political examples. ; Avoid a simple verdict.
The last speaker | CO | s | Write a story about the last fluent speaker of a language. | Convey loss without sentimentality. ; Use precise detail. ; Find a resonant ending.
The attention economy | TE | o | Are digital technologies eroding our capacity for sustained attention, and if so, what should be done? | Evaluate the evidence critically. ; Distinguish individual and collective responses. ; Conclude with a defensible position.
An exhibition with a message | ED | d | Write a critical review of an exhibition, real or imagined, that tries to address a social issue. | Describe the exhibition concisely. ; Evaluate its argument and methods. ; Judge whether it succeeds.
Resigning with dignity | WK | e | Write a letter resigning from a senior position over a disagreement about the company's direction, without burning bridges. | State the decision clearly. ; Explain the reasons with restraint. ; Leave the relationship intact.
Billionaires and democracy | MS | o | Does large-scale philanthropy by the very rich strengthen or weaken democracy? | Explain the mechanisms. ; Weigh the benefits against accountability. ; Conclude with nuance.
The house after the funeral | HF | s | Write a story in which a family sorts through a relative's house and discovers something that changes how they remember him. | Build character through objects. ; Pace the discovery. ; Leave a lasting impression.
Returning farmland to the wild | EN | o | Should large areas of farmland be returned to the wild? | Consider nature, food security and livelihoods. ; Use examples. ; Offer a balanced judgement.
Evaluating the four-day week trial | WK | d | Write a report evaluating a company's six-month trial of a four-day week, with findings and a recommendation. | Present the data clearly in prose. ; Interpret the limitations. ; Make a justified recommendation.
Knowing our genetic risks | HE | o | Should people be told about genetic risks they can do nothing about? | Define the dilemma. ; Consider freedom of choice and possible harm. ; Reach a careful conclusion.
To be opened in fifty years | DL | e | Write a letter to be opened in fifty years, describing ordinary life now and what you hope will change. | Choose revealing details. ; Balance description and reflection. ; Address the future reader convincingly.
Cities for people, not cars | TP | o | "Cities have been designed for cars for a century; it is time to design them for people." Discuss. | Assess the historical claim. ; Evaluate the proposed changes. ; Consider who wins and who loses.
The unanswered email | WK | s | Write a story in which an email that is never answered changes the course of two careers. | Use structure creatively. ; Develop both characters. ; Avoid an obvious ending.
Can a machine make art? | TE | o | Can work produced with artificial intelligence be considered art? | Define art carefully. ; Engage with opposing views. ; Develop your own position.
Loneliness and solitude | PF | d | Write a reflective essay on the difference between loneliness and solitude. | Define the terms precisely. ; Use observation or examples. ; Develop a reflective argument.
On behalf of the residents | PT | e | As chair of a residents' association, write to a developer about the impact of a construction project on your street. | Represent residents' concerns accurately. ; Cite specific incidents. ; Propose remedies and a deadline.
The search for the authentic | TR | o | Can tourism ever show visitors an "authentic" culture, or does it always change what it displays? | Question the idea of authenticity. ; Use examples. ; Reach a nuanced view.
The understudy | HS | s | Write a story about an understudy who finally gets to perform, on the worst possible night. | Build anticipation. ; Use vivid detail. ; Craft an ironic or moving ending.
Can schools reduce inequality? | ED | o | Can schools reduce social inequality, or do they mainly reproduce it? | Consider evidence and theory. ; Discuss policy options. ; Conclude carefully.
A graduation speech without clichés | ED | d | Write a graduation speech that avoids clichés and offers graduates something genuinely useful. | Open memorably. ; Offer specific insight. ; Close with resonance.
Declining with tact | CO | e | Write a letter declining a prestigious invitation for reasons you cannot fully state, without causing offence. | Decline clearly. ; Use tactful, indirect language. ; Preserve the relationship.
Growth or wellbeing? | MS | o | Should governments measure success by wellbeing rather than economic growth? | Explain both measures. ; Assess the practical difficulties. ; Take a position.
The ferry crossing | TR | s | Write a story set on a ferry crossing in which two strangers realise they have met before. | Create atmosphere. ; Reveal the past gradually. ; End with restraint.
Food waste in our restaurants | FD | d | Write a report on food waste in a chain of restaurants, with its causes and a costed plan to reduce it. | Identify the causes. ; Propose measures with costs. ; Prioritise them.
Offensive but legal | TE | o | Should social media platforms remove content that is offensive but legal? | Distinguish harm from offence. ; Consider who decides. ; Propose principles.
A eulogy for a teacher | PF | d | Write a eulogy for a fictional teacher who influenced many students, capturing both strengths and flaws. | Use specific anecdotes. ; Balance warmth and honesty. ; Give a fitting close.
Animals in medical research | AN | o | Is the use of animals in medical research still justifiable? | Present the ethical arguments. ; Consider alternatives. ; Reach a reasoned view.
An honest reference | WK | e | Write a reference for a former employee who is talented but unreliable, being honest without being unfair. | Describe strengths specifically. ; Address weaknesses tactfully. ; Give a fair overall judgement.
The archive | ED | s | Write a story about a researcher who finds a document in an archive that contradicts an accepted version of events. | Build intrigue. ; Show the character's dilemma. ; Resolve or suspend the tension.
People displaced by climate | EN | o | How should the international community respond to people displaced by climate change? | Define the problem. ; Evaluate responsibilities. ; Propose responses.
One city, three moments | PT | d | Write a descriptive piece portraying the same city at dawn, at midday and at midnight. | Contrast the three moments. ; Use precise imagery. ; Unify the piece with a theme.
Experts and the public | CO | o | In a democracy, how much should experts influence decisions that affect everyone? | Consider legitimacy and knowledge. ; Use examples. ; Present a nuanced view.
Answering an accusation | WK | e | A journalist has accused your organisation of misleading customers. Write a formal response for publication. | Address the claims precisely. ; Acknowledge any valid points. ; Maintain credibility.
The doctor's choice | HE | s | Write a story about a doctor in a remote clinic who is forced to choose between two patients. | Establish the setting. ; Convey the pressure. ; Explore the consequences.
Should voting be compulsory? | CO | o | Should voting be compulsory? | Present arguments on both sides. ; Use examples in general terms. ; Give your conclusion.
A decade of smartphones | TE | d | Write an essay reviewing how smartphones have changed social life over the past decade. | Identify the key changes. ; Assess their significance. ; Avoid easy conclusions.
Housing as a right | HF | o | Should adequate housing be treated as a legal right? | Explain the implications. ; Assess feasibility. ; Take a position.
Free buses for everyone | TP | o | Write an editorial for a local newspaper arguing that public transport should be free. | State the thesis. ; Support it with evidence. ; Answer objections.
The last match | HS | s | Write a story about a veteran player's final match, told from the point of view of a rival. | Use the rival's perspective. ; Build to the climax. ; End with insight.
Taste and social class | FD | o | To what extent are our food preferences shaped by social class? | Consider the evidence. ; Use examples. ; Avoid generalisation.
How I changed my mind | ED | d | Write a reflective essay about a belief you changed and how the change happened. | Explain the original belief. ; Trace the change. ; Reflect on what it means.
AI tutors in our schools | TE | e | Write a letter to an education minister about how schools should use AI tutors responsibly. | Identify opportunities and risks. ; Propose safeguards. ; Conclude persuasively.
Luck and success | MS | o | How much of success is due to luck? | Define success and luck. ; Use examples. ; Develop an argument.
The old map | TR | s | Write a story about an old map that leads its owner somewhere unexpected, and not necessarily to a place. | Use the map as a symbol. ; Develop the character. ; Give an open but satisfying ending.
"""


def main():
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "writing.json"
    original = [p for p in json.loads(path.read_text(encoding="utf-8")) if int(p["id"][1:]) <= 10]
    out = list(original)
    n = 10
    for level, block in PROMPTS.items():
        lo, hi = WORDS[level]
        for line in filter(None, (l.strip() for l in block.strip().splitlines())):
            title, topic, genre, prompt, checklist = (part.strip() for part in line.split(" | "))
            items = [c.strip() for c in checklist.split(" ; ")]
            assert len(items) >= 3 and all(items), title
            n += 1
            out.append({"id": f"w{n}", "title": title, "level": level, "topic": TOPICS[topic],
                        "genre": GENRES[genre], "prompt": prompt, "minWords": lo, "maxWords": hi,
                        "checklist": items})
    titles = [p["title"].lower() for p in out]
    assert len(set(titles)) == len(titles), [t for t in titles if titles.count(t) > 1]
    counts = {lv: sum(1 for p in out if p["level"] == lv) for lv in WORDS}
    for level in PROMPTS:
        assert counts[level] == 50, counts
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "prompts", counts)


main()

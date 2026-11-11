"""Writes src/data/listening.json: the 24 earlier lessons (l1-l24) plus lessons written for EnglishUp
on 2026-11-11 so that every level from A1 to C2 has 50 listening lessons.

Format, one lesson after another:
    ## Title | topic code
    Speaker: what they say
    ? c | question | *right option | other option | ... | explanation | evidence
    ? b | sentence with ____ | accepted answer / another accepted answer | explanation | evidence
    ? t | statement | T, F or N (True, False, Not Given) | explanation | evidence
Every evidence must be an exact part of the script; the script refuses a lesson otherwise.
Run: python scripts/create-listening-lessons.py
"""
import json
import pathlib

TOPICS = {
    "DL": "Daily life", "TR": "Travel", "WK": "Work", "FD": "Food", "HE": "Health", "TE": "Technology",
    "EN": "Environment", "ED": "Education", "SH": "Shopping", "CO": "Communication", "PF": "People and family",
    "HS": "Hobbies and sport", "TP": "Transport", "NW": "Nature and weather", "HF": "Home and furniture",
    "PT": "Places in town", "MS": "Money and shopping", "AN": "Animals",
}
TFNG = {"T": "True", "F": "False", "N": "Not Given"}
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

LESSONS = {}

LESSONS["A1"] = """
## Ordering a drink | FD
Waiter: Hello. What would you like to drink?
Mai: A cup of tea, please.
Waiter: Hot or cold?
Mai: Cold, please, with some ice.
Waiter: OK. That's two dollars.
? c | What does Mai order? | *A cup of tea | A cup of coffee | A glass of milk | Mai asks for tea. | A cup of tea, please.
? c | Does Mai want her drink hot or cold? | *Cold | Hot | Warm | She answers the waiter's question. | Cold, please, with some ice.
? b | The drink costs two ____. | dollars | The waiter says the price. | That's two dollars.
? t | Mai wants sugar in her tea. | N | Mai talks about ice, not sugar. | Cold, please, with some ice.

## What's your phone number? | CO
Tom: Can I have your phone number?
Lisa: Sure. It's zero nine one, two three four, five six seven.
Tom: Zero nine one, two three four, five six seven. Thanks.
Lisa: And what's your name again?
Tom: Tom. Tom Green.
? b | Lisa's number starts with zero nine ____. | one / 1 | Lisa says the first three numbers. | It's zero nine one
? c | What is Tom's family name? | *Green | Brown | Grey | Tom says his full name. | Tom. Tom Green.
? t | Tom says the number back to Lisa. | T | He repeats it to check. | Zero nine one, two three four, five six seven. Thanks.
? c | Who asks for the phone number? | *Tom | Lisa | Both of them | Tom asks first. | Can I have your phone number?

## At the bus stop | TP
Woman: Excuse me, does this bus go to the hospital?
Man: No, it doesn't. You need bus number eight.
Woman: Where can I get it?
Man: Across the street, next to the bakery.
Woman: Thank you!
? c | Where does the woman want to go? | *To the hospital | To the bakery | To the station | She asks about the hospital. | does this bus go to the hospital?
? b | She needs bus number ____. | eight / 8 | The man gives the number. | You need bus number eight.
? c | Where is the other bus stop? | *Next to the bakery | Next to the bank | Behind the hospital | The man explains where to go. | Across the street, next to the bakery.
? t | This bus goes to the hospital. | F | The man says no. | No, it doesn't.

## Our new teacher | ED
Lan: We have a new English teacher.
Dad: Oh? What's her name?
Lan: Ms. Carter. She's from Australia.
Dad: Is she nice?
Lan: Yes, she's very friendly, and her lessons are fun.
? c | What does the new teacher teach? | *English | Maths | Music | Lan says it at the start. | We have a new English teacher.
? c | Where is Ms. Carter from? | *Australia | Canada | England | Lan says where she is from. | She's from Australia.
? t | Lan likes the new teacher. | T | Lan says she is friendly and fun. | she's very friendly, and her lessons are fun.
? b | The teacher's name is Ms. ____. | Carter | Lan gives her name. | Ms. Carter.

## Buying a T-shirt | SH
Customer: How much is this T-shirt?
Assistant: It's fifteen dollars.
Customer: Do you have it in blue?
Assistant: Yes, here you are. What size?
Customer: Medium, please.
? b | The T-shirt costs ____ dollars. | fifteen / 15 | The assistant gives the price. | It's fifteen dollars.
? c | Which colour does the customer want? | *Blue | Red | Green | The customer asks for this colour. | Do you have it in blue?
? c | What size does the customer want? | *Medium | Small | Large | The customer answers the question about size. | Medium, please.
? t | The shop does not have the T-shirt in blue. | F | The assistant has one. | Yes, here you are.

## The weather tomorrow | NW
Presenter: Good evening. Here is the weather for tomorrow.
Presenter: In the morning it will be cloudy and cool.
Presenter: In the afternoon it will be sunny and warm.
Presenter: There will be rain in the evening, so take an umbrella.
? c | What will the morning be like? | *Cloudy and cool | Sunny and hot | Rainy and cold | The presenter starts with the morning. | In the morning it will be cloudy and cool.
? c | When will it be sunny? | *In the afternoon | In the morning | In the evening | The presenter says when. | In the afternoon it will be sunny and warm.
? b | Take an ____ in the evening. | umbrella | Rain is coming. | so take an umbrella.
? t | It will snow tomorrow. | N | The forecast talks about clouds, sun and rain only. | There will be rain in the evening

## Where are my glasses? | HF
Grandma: Have you seen my glasses?
Ben: Are they on the table?
Grandma: No, I looked there.
Ben: Oh, look! They're on your head, Grandma!
Grandma: Oh dear. Thank you, Ben.
? c | What is Grandma looking for? | *Her glasses | Her keys | Her phone | She asks at the start. | Have you seen my glasses?
? c | Where are the glasses? | *On her head | On the table | In her bag | Ben finds them. | They're on your head, Grandma!
? t | Grandma looked on the table. | T | She says she looked there. | No, I looked there.
? b | The boy's name is ____. | Ben | Grandma thanks him by name. | Thank you, Ben.

## Sandwiches for lunch | FD
Anna: I'm hungry. Let's make sandwiches.
Leo: OK. We have bread, cheese and tomatoes.
Anna: Do we have any eggs?
Leo: No, we don't. But we have some chicken.
Anna: Great. Chicken and cheese, then.
? c | What do they make? | *Sandwiches | Soup | Pizza | Anna suggests it. | Let's make sandwiches.
? t | They have some eggs. | F | Leo says no. | No, we don't.
? c | What will be in the sandwiches? | *Chicken and cheese | Eggs and tomatoes | Only cheese | Anna decides at the end. | Chicken and cheese, then.
? b | They have bread, cheese and ____. | tomatoes / tomato | Leo lists the food. | We have bread, cheese and tomatoes.

## A film tonight | HS
Sam: Do you want to see a film tonight?
Kim: Yes! What time?
Sam: The film starts at seven thirty.
Kim: Let's meet at seven, in front of the cinema.
Sam: Great. See you then.
? b | The film starts at seven ____. | thirty / 30 | Sam says the time. | The film starts at seven thirty.
? c | What time will they meet? | *At seven | At seven thirty | At eight | Kim suggests a time. | Let's meet at seven
? c | Where will they meet? | *In front of the cinema | At Sam's house | At the bus stop | Kim says where. | in front of the cinema.
? t | They will see the film in the morning. | F | It is tonight. | Do you want to see a film tonight?

## A trip to the museum | ED
Teacher: Listen, everyone. Tomorrow we have a trip to the museum.
Teacher: Please come to school at eight o'clock.
Teacher: Bring a drink and a small snack.
Teacher: We will come back at two in the afternoon.
? c | Where is the class going? | *To the museum | To the zoo | To the park | The teacher says it first. | Tomorrow we have a trip to the museum.
? b | Students must come at ____ o'clock. | eight / 8 | The teacher gives the time. | come to school at eight o'clock.
? c | What should students bring? | *A drink and a snack | Lunch money | A book and a pen | The teacher says what to bring. | Bring a drink and a small snack.
? t | They will come back in the evening. | F | They come back in the afternoon. | We will come back at two in the afternoon.

## Is this seat free? | TP
Man: Excuse me, is this seat free?
Woman: Yes, it is. Please sit down.
Man: Thanks. Is this train going to Hanoi?
Woman: Yes. We arrive at six.
? c | Where are they? | *On a train | On a bus | In a café | The man asks about the train. | Is this train going to Hanoi?
? t | The seat is free. | T | The woman says yes. | Yes, it is. Please sit down.
? b | The train arrives at ____. | six / 6 | The woman gives the time. | We arrive at six.
? c | Where is the train going? | *Hanoi | Hue | Da Nang | The man asks and the woman says yes. | Is this train going to Hanoi?

## My dog Lucky | AN
Nam: I have a dog. His name is Lucky.
Nam: He is brown and white, and he is three years old.
Nam: Every evening I take him for a walk in the park.
Nam: He loves playing with a ball.
? b | The dog's name is ____. | Lucky | Nam says the name. | His name is Lucky.
? c | What colour is the dog? | *Brown and white | Black | Grey and white | Nam describes the dog. | He is brown and white
? c | How old is the dog? | *Three | Two | Four | Nam says his age. | he is three years old.
? t | Nam walks the dog in the morning. | F | He walks him in the evening. | Every evening I take him for a walk in the park.

## A call from Mum | PF
Mum: Hi, Linh. Where are you?
Linh: I'm at Hoa's house. We're doing homework.
Mum: OK. Come home before six. Dinner is at six thirty.
Linh: OK, Mum. See you soon.
? c | Where is Linh? | *At Hoa's house | At school | At the library | Linh tells her mum. | I'm at Hoa's house.
? c | What are the girls doing? | *Homework | Cooking | Watching TV | Linh says what they are doing. | We're doing homework.
? b | Dinner is at six ____. | thirty / 30 | Mum gives the time. | Dinner is at six thirty.
? t | Linh must come home before six. | T | Mum asks her to. | Come home before six.

## A sore throat | HE
Doctor: Hello. What's the matter?
Boy: I have a sore throat and a headache.
Doctor: Do you have a temperature?
Boy: Yes, a little.
Doctor: Drink warm water and rest at home for two days.
? c | What is wrong with the boy? | *A sore throat and a headache | A stomach ache | A broken arm | He tells the doctor. | I have a sore throat and a headache.
? t | The boy has a temperature. | T | He says yes, a little. | Yes, a little.
? c | What does the doctor tell him to do? | *Drink warm water and rest | Go to school | Eat ice cream | The doctor gives advice. | Drink warm water and rest at home
? b | He should rest for ____ days. | two / 2 | The doctor says how long. | rest at home for two days.

## Saturday at the beach | DL
Ali: What are you doing on Saturday?
Mia: I'm going to the beach with my family.
Ali: Nice! And on Sunday?
Mia: On Sunday I'm staying at home. I have a test on Monday.
? c | Where is Mia going on Saturday? | *To the beach | To the mountains | To school | She says her plan. | I'm going to the beach with my family.
? c | What is Mia doing on Sunday? | *Staying at home | Visiting friends | Going shopping | She explains Sunday. | On Sunday I'm staying at home.
? b | Mia has a test on ____. | Monday | She gives the reason. | I have a test on Monday.
? t | Mia is going to the beach alone. | F | She is going with her family. | with my family.

## The lost cat | AN
Woman: Hello, this is Mrs. Brown from number twelve.
Woman: My cat is lost. She is small and black, with white feet.
Woman: Her name is Daisy.
Woman: If you see her, please call me. Thank you.
? b | Mrs. Brown lives at number ____. | twelve / 12 | She says her house number. | from number twelve.
? c | What does the cat look like? | *Small and black with white feet | Big and white | Grey with black feet | She describes the cat. | She is small and black, with white feet.
? c | What is the cat's name? | *Daisy | Lucky | Kitty | She gives the name. | Her name is Daisy.
? t | Mrs. Brown asks people to bring the cat to a shop. | F | She asks people to call her. | please call me.

## Two coffees, please | FD
Customer: Two coffees, please.
Server: With milk?
Customer: One with milk and one without.
Server: Anything to eat?
Customer: Yes, two croissants, please.
? c | How many coffees does the customer order? | *Two | One | Three | The customer orders at the start. | Two coffees, please.
? c | How does the customer want the coffees? | *One with milk, one without | Both with milk | Both without milk | The customer explains. | One with milk and one without.
? b | The customer also orders two ____. | croissants / croissant | The customer orders food. | two croissants, please.
? t | The customer does not want anything to eat. | F | They order croissants. | Yes, two croissants, please.

## Where do you live? | PT
Jack: Where do you live, Hana?
Hana: I live on Green Street, near the post office.
Jack: Is it a house or a flat?
Hana: It's a flat on the fourth floor.
Jack: Do you have a lift?
Hana: Yes, we do, thank goodness!
? c | Which street does Hana live on? | *Green Street | Park Street | Bank Street | Hana says her street. | I live on Green Street
? c | What is near Hana's home? | *The post office | The school | The market | She says what is near. | near the post office.
? b | Hana lives on the ____ floor. | fourth / 4th | She says the floor. | It's a flat on the fourth floor.
? t | There is a lift in Hana's building. | T | She says yes. | Yes, we do, thank goodness!

## Happy birthday, Tom | PF
Amy: Happy birthday, Tom! This is for you.
Tom: Thank you, Amy! Can I open it now?
Amy: Of course.
Tom: Oh, a football! I love it.
Amy: How old are you today?
Tom: I'm ten.
? c | What is the present? | *A football | A book | A bike | Tom opens it. | Oh, a football! I love it.
? b | Tom is ____ years old today. | ten / 10 | Tom answers Amy. | I'm ten.
? t | Tom must wait to open the present. | F | Amy says he can open it now. | Of course.
? c | Who gives Tom the present? | *Amy | His mother | His teacher | Amy gives it at the start. | This is for you.

## At the library desk | ED
Student: Excuse me, how many books can I borrow?
Librarian: You can borrow five books.
Student: For how long?
Librarian: For two weeks.
Student: And is the library open on Sunday?
Librarian: No, it's closed on Sunday.
? b | Students can borrow ____ books. | five / 5 | The librarian answers. | You can borrow five books.
? c | For how long can they keep the books? | *Two weeks | One week | One month | The librarian says how long. | For two weeks.
? t | The library is open on Sunday. | F | It is closed. | No, it's closed on Sunday.
? c | What does the student ask first? | *How many books they can borrow | Where the books are | How much a book costs | The first question is about the number of books. | how many books can I borrow?

## No milk today | FD
Dad: What do you want for breakfast?
Kate: Can I have some cereal and milk?
Dad: Sorry, there's no milk. How about toast and an egg?
Kate: OK. And some orange juice, please.
? c | What does Kate ask for first? | *Cereal and milk | Toast and an egg | Rice | Kate asks at the start. | Can I have some cereal and milk?
? t | There is no milk. | T | Dad says so. | there's no milk.
? c | What does Dad offer instead? | *Toast and an egg | Pancakes | Noodles | Dad suggests another breakfast. | How about toast and an egg?
? b | Kate also wants some orange ____. | juice | She asks for a drink. | some orange juice, please.

## Sports day | HS
Coach: Good morning, everyone! Welcome to sports day.
Coach: The running race starts at nine.
Coach: After that, we have football and basketball.
Coach: Lunch is at twelve, near the big tree.
? b | The running race starts at ____. | nine / 9 | The coach gives the time. | The running race starts at nine.
? c | Which games come after the race? | *Football and basketball | Tennis and swimming | Volleyball | The coach lists them. | we have football and basketball.
? c | Where is lunch? | *Near the big tree | In the classroom | At the café | The coach says where. | Lunch is at twelve, near the big tree.
? t | Lunch is at one o'clock. | F | Lunch is at twelve. | Lunch is at twelve

## A taxi to the airport | TP
Driver: Hello. Where to?
Woman: The airport, please. How long does it take?
Driver: About thirty minutes.
Woman: How much is it?
Driver: Around twenty dollars.
? c | Where does the woman want to go? | *The airport | The station | The hotel | She tells the driver. | The airport, please.
? b | The trip takes about ____ minutes. | thirty / 30 | The driver answers. | About thirty minutes.
? b | It costs around ____ dollars. | twenty / 20 | The driver gives the price. | Around twenty dollars.
? t | The woman asks about the time and the price. | T | She asks both questions. | How long does it take?

## Lily's bedroom | HF
Lily: My bedroom is my favourite room.
Lily: The walls are yellow, and the door is white.
Lily: My bed is next to the window.
Lily: I have a green chair and lots of books.
? c | What colour are the walls? | *Yellow | White | Green | Lily describes the walls. | The walls are yellow
? c | Where is the bed? | *Next to the window | Next to the door | Under the window | Lily says where. | My bed is next to the window.
? b | Lily has a green ____. | chair | She describes the furniture. | I have a green chair
? t | Lily's bedroom is her favourite room. | T | She says it at the start. | My bedroom is my favourite room.

## A heavy box | CO
Girl: Can you help me with this box? It's heavy.
Boy: Sure. Where do you want it?
Girl: In the kitchen, please. On the floor.
Boy: Here you go.
Girl: Thanks a lot!
? c | What is the problem? | *The box is heavy | The box is broken | The box is lost | The girl explains. | It's heavy.
? c | Where does the box go? | *In the kitchen | In the garden | In the bedroom | The girl says where. | In the kitchen, please.
? t | The box goes on the table. | F | She wants it on the floor. | On the floor.
? c | How does the girl feel at the end? | *Thankful | Angry | Sad | She thanks the boy. | Thanks a lot!

## An old phone | TE
Son: Dad, my phone is very old. Can I get a new one?
Dad: What's wrong with it?
Son: The battery dies every afternoon, and the camera doesn't work.
Dad: OK. Let's look at phones this weekend.
? c | What is wrong with the phone? | *The battery and the camera | The screen is broken | It is too big | The son explains. | The battery dies every afternoon, and the camera doesn't work.
? t | The phone is new. | F | The son says it is very old. | my phone is very old.
? c | When will they look at phones? | *This weekend | Tonight | Next month | Dad suggests a time. | Let's look at phones this weekend.
? b | The battery dies every ____. | afternoon | The son says when. | The battery dies every afternoon

## Fresh fish | SH
Seller: Fresh fish! Fresh fish!
Woman: How much is this fish?
Seller: Eight dollars a kilo.
Woman: I'll take one kilo. Do you have any prawns?
Seller: Sorry, no prawns today.
? b | The fish costs ____ dollars a kilo. | eight / 8 | The seller gives the price. | Eight dollars a kilo.
? c | How much fish does the woman buy? | *One kilo | Two kilos | Half a kilo | She says how much. | I'll take one kilo.
? t | The seller has prawns today. | F | The seller says no. | Sorry, no prawns today.
? c | What does the seller sell? | *Fish | Fruit | Bread | The seller calls out to customers. | Fresh fish! Fresh fish!

## My grandfather | PF
Huy: My grandfather is seventy years old.
Huy: He lives with us in a big house.
Huy: Every morning he reads the newspaper and drinks green tea.
Huy: In the afternoon he works in the garden.
? b | Huy's grandfather is ____ years old. | seventy / 70 | Huy gives his age. | My grandfather is seventy years old.
? c | What does the grandfather drink every morning? | *Green tea | Coffee | Milk | Huy describes his morning. | drinks green tea.
? c | What does he do in the afternoon? | *He works in the garden | He sleeps | He goes shopping | Huy describes the afternoon. | In the afternoon he works in the garden.
? t | The grandfather lives alone. | F | He lives with Huy's family. | He lives with us in a big house.

## Swimming lessons | HS
Mother: I'd like swimming lessons for my son.
Receptionist: How old is he?
Mother: He's six.
Receptionist: OK. The children's class is on Tuesday and Thursday at four.
Mother: How much is it?
Receptionist: Forty dollars a month.
? c | Who are the lessons for? | *The woman's son | The woman | The woman's daughter | She says it at the start. | I'd like swimming lessons for my son.
? b | The boy is ____ years old. | six / 6 | The mother answers. | He's six.
? c | When is the class? | *Tuesday and Thursday at four | Monday at four | Saturday morning | The receptionist explains. | on Tuesday and Thursday at four.
? b | The lessons cost forty dollars a ____. | month | The receptionist gives the price. | Forty dollars a month.

## A rainy afternoon at home | NW
Ella: Oh no, it's raining!
Max: Let's stay inside and play a game.
Ella: Good idea. Do you want to play cards?
Max: Yes! And let's make hot chocolate.
? t | It is sunny. | F | Ella says it is raining. | Oh no, it's raining!
? c | What will they play? | *Cards | Football | A computer game | Ella suggests a game. | Do you want to play cards?
? c | What will they drink? | *Hot chocolate | Cold juice | Tea | Max suggests a drink. | let's make hot chocolate.
? c | Where will they play? | *Inside | In the garden | At the park | Max suggests staying in. | Let's stay inside and play a game.

## A key that doesn't work | TR
Guest: Hello. My room key doesn't work.
Receptionist: I'm sorry. What's your room number?
Guest: Room two hundred and five.
Receptionist: Here is a new key. Have a nice evening.
? c | What is the guest's problem? | *The room key doesn't work | The room is dirty | The room is too small | The guest explains. | My room key doesn't work.
? b | The guest is in room two hundred and ____. | five / 5 | The guest gives the number. | Room two hundred and five.
? t | The guest gets a new key. | T | A new key solves the problem. | Here is a new key.
? c | What time of day is it? | *Evening | Morning | Lunchtime | The receptionist wishes the guest a nice evening. | Have a nice evening.

## My friend Yen | PF
Sara: My best friend is called Yen.
Sara: She has long black hair and brown eyes.
Sara: We are in the same class.
Sara: At the weekend we ride our bikes together.
? b | Sara's best friend is called ____. | Yen | Sara gives her name. | My best friend is called Yen.
? c | What does Yen look like? | *Long black hair and brown eyes | Short hair and blue eyes | Long brown hair | Sara describes her. | She has long black hair and brown eyes.
? t | The two girls are in the same class. | T | Sara says so. | We are in the same class.
? c | What do they do at the weekend? | *Ride their bikes | Go swimming | Watch films | Sara describes the weekend. | we ride our bikes together.

## Cleaning day | HF
Mum: It's Saturday. Let's clean the house.
Kid: Oh, Mum! What do I have to do?
Mum: Please tidy your room and wash the dishes.
Kid: And then can I go out?
Mum: Yes, after lunch.
? c | What day is it? | *Saturday | Sunday | Friday | Mum says the day. | It's Saturday.
? c | What must the child do? | *Tidy the room and wash the dishes | Cook lunch | Clean the car | Mum gives two jobs. | Please tidy your room and wash the dishes.
? t | The child can go out before lunch. | F | Mum says after lunch. | Yes, after lunch.
? b | They are going to clean the ____. | house | Mum suggests it. | Let's clean the house.

## Which flavour? | FD
Boy: Can I have an ice cream, please?
Seller: Which flavour? We have chocolate, strawberry and lemon.
Boy: Chocolate, please. How much is it?
Seller: One dollar fifty.
? c | Which flavour does the boy choose? | *Chocolate | Strawberry | Lemon | The boy chooses. | Chocolate, please.
? b | The ice cream costs one dollar ____. | fifty / 50 | The seller says the price. | One dollar fifty.
? t | The seller has three flavours. | T | The seller names three. | We have chocolate, strawberry and lemon.
? c | What does the boy ask for? | *An ice cream | A cake | A drink | He asks at the start. | Can I have an ice cream, please?

## Mr. Lam goes to work | WK
Mr. Lam: I work in a bank in the city centre.
Mr. Lam: I go to work by bus every day.
Mr. Lam: The bus takes forty minutes.
Mr. Lam: I start work at eight and finish at five.
? c | Where does Mr. Lam work? | *In a bank | In a school | In a hospital | He says where he works. | I work in a bank in the city centre.
? c | How does he go to work? | *By bus | By car | On foot | He explains. | I go to work by bus every day.
? b | The bus takes ____ minutes. | forty / 40 | He gives the time. | The bus takes forty minutes.
? t | He finishes work at six. | F | He finishes at five. | I start work at eight and finish at five.

## A picnic by the lake | NW
Jane: It's a lovely day. Let's have a picnic.
Paul: Good idea! Where?
Jane: In the park, by the lake.
Paul: I can bring sandwiches and fruit.
Jane: And I'll bring some drinks.
? c | Where will they have the picnic? | *In the park, by the lake | On the beach | In the garden | Jane suggests a place. | In the park, by the lake.
? c | What will Paul bring? | *Sandwiches and fruit | Drinks | A cake | Paul offers. | I can bring sandwiches and fruit.
? c | What will Jane bring? | *Drinks | Sandwiches | Chairs | Jane says at the end. | And I'll bring some drinks.
? t | The weather is bad. | F | Jane says it is a lovely day. | It's a lovely day.

## Page twenty | ED
Teacher: Open your books at page twenty.
Student: Sorry, which page?
Teacher: Page twenty. Read the story and answer the questions.
Student: Can we work in pairs?
Teacher: Yes, you can.
? b | Students open their books at page ____. | twenty / 20 | The teacher repeats it. | Page twenty.
? c | What must students do? | *Read a story and answer questions | Write a letter | Draw a picture | The teacher explains. | Read the story and answer the questions.
? t | Students can work in pairs. | T | The teacher says yes. | Yes, you can.
? c | Why does the student ask a question? | *They did not hear the page number | They lost their book | They are ill | The student asks again. | Sorry, which page?

## A message for Peter | CO
Anna: Hi Peter, it's Anna.
Anna: I can't come to football practice today. I'm ill.
Anna: Can you tell the coach, please?
Anna: Thanks. See you on Friday.
? c | Who leaves the message? | *Anna | Peter | The coach | She says her name. | Hi Peter, it's Anna.
? c | Why can't Anna come? | *She is ill | She is busy | She is on holiday | She gives a reason. | I'm ill.
? c | What does Anna ask Peter to do? | *Tell the coach | Call her mother | Bring her bag | She asks for help. | Can you tell the coach, please?
? b | Anna will see Peter on ____. | Friday | She says goodbye. | See you on Friday.

## The new café | PT
Mai: Have you been to the new café on Main Street?
Tuan: Not yet. Is it good?
Mai: Yes! The cakes are great, and it's not expensive.
Tuan: Is it open on Monday?
Mai: Yes, every day from seven to nine.
? c | Where is the new café? | *On Main Street | On Park Street | Near the school | Mai says the street. | the new café on Main Street?
? t | Tuan has been to the café. | F | He says not yet. | Not yet.
? c | What does Mai like there? | *The cakes | The music | The coffee | Mai describes it. | The cakes are great
? b | It is open every day from seven to ____. | nine / 9 | Mai gives the times. | every day from seven to nine.

## Lost at the station | TP
Boy: Excuse me, I can't find my mum.
Officer: Don't worry. What does she look like?
Boy: She has short hair, and she's wearing a red coat.
Officer: Let's go to the information desk. We can call her.
? c | What is the boy's problem? | *He can't find his mum | He lost his ticket | He missed the train | He tells the officer. | I can't find my mum.
? c | What is his mum wearing? | *A red coat | A blue dress | A black hat | The boy describes her. | she's wearing a red coat.
? t | The boy's mum has long hair. | F | She has short hair. | She has short hair
? c | Where do they go? | *To the information desk | To the train | To the café | The officer suggests it. | Let's go to the information desk.

## Vegetable soup | FD
Chef: Today we're making vegetable soup.
Chef: You need two carrots, one onion and three potatoes.
Chef: Cut the vegetables into small pieces.
Chef: Cook them in water for twenty minutes.
? c | What are they making? | *Vegetable soup | Fried rice | Salad | The chef says it at the start. | Today we're making vegetable soup.
? b | You need three ____. | potatoes / potato | The chef lists the vegetables. | three potatoes.
? c | How long do you cook the soup? | *Twenty minutes | Ten minutes | One hour | The chef gives the time. | Cook them in water for twenty minutes.
? t | You need two onions. | F | You need one onion. | one onion

## Piano and guitar | HS
Ken: Do you like music?
Lucy: Yes, I love it. I play the piano.
Ken: Really? I play the guitar.
Lucy: We can play together one day!
Ken: Great idea.
? c | What does Lucy play? | *The piano | The guitar | The drums | Lucy says what she plays. | I play the piano.
? c | What does Ken play? | *The guitar | The piano | The violin | Ken answers. | I play the guitar.
? t | Lucy does not like music. | F | She says she loves it. | Yes, I love it.
? c | What does Lucy suggest? | *Playing together | Going to a concert | Buying a guitar | She makes a suggestion. | We can play together one day!

## A big grey animal | AN
Child: Look! What's that big grey animal?
Father: That's an elephant.
Child: Wow! And what does it eat?
Father: It eats grass, fruit and leaves.
Child: Can we see the monkeys next?
Father: Yes, they're over there.
? c | What animal do they see first? | *An elephant | A monkey | A lion | The father names it. | That's an elephant.
? c | What colour is the animal? | *Grey | Brown | Black | The child describes it. | What's that big grey animal?
? b | The elephant eats grass, fruit and ____. | leaves | The father lists the food. | It eats grass, fruit and leaves.
? c | What does the child want to see next? | *The monkeys | The birds | The tigers | The child asks. | Can we see the monkeys next?

## A busy morning | DL
Mother: Every morning is busy in our house.
Mother: I get up at six and make breakfast.
Mother: My husband takes the children to school.
Mother: Then I go to work by bike.
? b | The mother gets up at ____. | six / 6 | She gives the time. | I get up at six
? c | Who takes the children to school? | *Her husband | She does | The grandmother | She explains. | My husband takes the children to school.
? c | How does she go to work? | *By bike | By car | By bus | She says it at the end. | Then I go to work by bike.
? t | Mornings are quiet in her house. | F | She says they are busy. | Every morning is busy in our house.

## Can I borrow your pen? | ED
Lan: Can I borrow your pen? Mine doesn't work.
Minh: Sure. Blue or black?
Lan: Black, please.
Minh: Here you are. Keep it for today.
Lan: Thanks, I'll give it back tomorrow.
? c | Why does Lan need a pen? | *Lan's pen doesn't work | Lan lost a pen | Lan has no money | Lan explains. | Mine doesn't work.
? c | Which colour does Lan want? | *Black | Blue | Red | Lan chooses. | Black, please.
? t | Lan will give the pen back tomorrow. | T | Lan says so. | I'll give it back tomorrow.
? b | Minh says Lan can keep it for ____. | today | Minh is kind. | Keep it for today.

## Cleaning the beach | EN
Leader: Hello, everyone, and thank you for coming.
Leader: Today we are cleaning the beach.
Leader: Please take a bag and some gloves.
Leader: Put plastic in the blue bags and glass in the green bags.
? c | What are the people doing today? | *Cleaning the beach | Swimming | Fishing | The leader explains. | Today we are cleaning the beach.
? c | What should everyone take? | *A bag and some gloves | A towel | A bottle of water | The leader says it. | Please take a bag and some gloves.
? c | Where does plastic go? | *In the blue bags | In the green bags | In the black bags | The leader explains. | Put plastic in the blue bags
? b | Glass goes in the ____ bags. | green | The leader explains. | glass in the green bags.
"""

LESSONS["A2"] = """
## A table for four | FD
Waiter: Good evening. Do you have a reservation?
Man: Yes, a table for four, under the name Harris.
Waiter: Ah yes, Mr. Harris. Your table is by the window. Would you like to see the drinks menu?
Man: Yes, please. And could we have some bread while we wait? Two of us are very hungry.
Waiter: Of course. Today's special is grilled salmon with rice.
? c | How many people is the table for? | *Four | Two | Six | The man says the number. | a table for four
? b | The reservation is under the name ____. | Harris | The man gives his name. | under the name Harris.
? c | Where is the table? | *By the window | Near the door | Outside | The waiter says where. | Your table is by the window.
? c | What is today's special? | *Grilled salmon with rice | Chicken soup | Beef noodles | The waiter tells them. | Today's special is grilled salmon with rice.

## Two return tickets | TP
Clerk: Good morning. Where are you going?
Woman: Two return tickets to Hai Phong, please. For tomorrow morning.
Clerk: There's a train at seven fifteen and another at nine forty.
Woman: The nine forty, please. How much is that?
Clerk: That's thirty dollars for two returns.
Woman: Can I pay by card?
Clerk: Yes, of course.
? c | What tickets does the woman buy? | *Two return tickets | One single ticket | Two single tickets | She asks at the start. | Two return tickets to Hai Phong
? c | Which train does she choose? | *The nine forty | The seven fifteen | The eleven o'clock | She chooses the later train. | The nine forty, please.
? b | The tickets cost ____ dollars. | thirty / 30 | The clerk gives the total. | That's thirty dollars for two returns.
? t | She pays in cash. | F | She asks to pay by card and the clerk agrees. | Can I pay by card?

## The gym on Lake Road | HS
Kevin: Hi Rosa. You look fit! Have you joined a gym?
Rosa: Yes, I joined the new one on Lake Road last month.
Kevin: Is it expensive?
Rosa: Not really. It's twenty-five dollars a month, and there's a swimming pool.
Kevin: When do you go?
Rosa: Usually before work, at six. It's quiet then.
? c | Where is the new gym? | *On Lake Road | On Hill Street | Near the station | Rosa says where. | the new one on Lake Road
? b | It costs twenty-five dollars a ____. | month | Rosa gives the price. | It's twenty-five dollars a month
? t | The gym has a swimming pool. | T | Rosa mentions it. | there's a swimming pool.
? c | Why does Rosa go at six? | *It's quiet then | It's cheaper then | Her friend goes then | She explains. | It's quiet then.

## Moving house | HF
Phong: We're moving house next Saturday.
Lily: Really? Where to?
Phong: To a bigger flat near my office. It has three bedrooms and a balcony.
Lily: Do you need any help?
Phong: That would be great. Can you come at nine? I've booked a van for ten.
Lily: No problem. I'll bring some boxes.
? c | When is Phong moving? | *Next Saturday | Tomorrow | Next month | He says it first. | We're moving house next Saturday.
? b | The new flat has ____ bedrooms. | three / 3 | Phong describes the flat. | It has three bedrooms and a balcony.
? c | What time will the van come? | *At ten | At nine | At eleven | Phong booked it. | I've booked a van for ten.
? c | What will Lily bring? | *Some boxes | Some food | A van | She offers at the end. | I'll bring some boxes.

## Tonight's class is cancelled | ED
Teacher: Hello, this is Mrs. Nguyen from the language centre.
Teacher: I'm sorry, but tonight's English class is cancelled because I'm ill.
Teacher: We'll have the lesson next Wednesday instead, at the same time.
Teacher: Please do exercises four and five on page thirty-two for homework.
? c | Why is the class cancelled? | *The teacher is ill | The room is closed | It's a holiday | She gives the reason. | because I'm ill.
? c | When is the new lesson? | *Next Wednesday | Tomorrow | Next Friday | She says when. | We'll have the lesson next Wednesday instead
? b | The homework is on page thirty-____. | two / 2 | She gives the page. | on page thirty-two
? t | The new lesson is at a different time. | F | It is at the same time. | at the same time.

## The lost umbrella | TP
Man: Hello. I left my umbrella on the number twelve bus this morning.
Clerk: What does it look like?
Man: It's long and dark green, with a wooden handle.
Clerk: Let me check. Yes, we have a green umbrella here. Can you come and collect it?
Man: Yes. When are you open?
Clerk: Until six this evening.
? b | He left the umbrella on bus number ____. | twelve / 12 | He tells the clerk. | the number twelve bus
? c | What does the umbrella look like? | *Long and dark green | Short and black | Red with a metal handle | He describes it. | It's long and dark green, with a wooden handle.
? t | The office has found the umbrella. | T | The clerk finds a green one. | Yes, we have a green umbrella here.
? c | When does the office close? | *At six this evening | At five | At noon | The clerk says when. | Until six this evening.

## Grandma's soup | FD
Jenny: This soup is delicious! What's in it?
Grandma: Chicken, ginger, some carrots and a little lemon.
Jenny: How long does it take to make?
Grandma: About an hour. The secret is to cook it slowly.
Jenny: Can you write down the recipe for me?
Grandma: Of course, dear. I'll give it to you after lunch.
? c | Which of these is NOT in the soup? | *Potatoes | Ginger | Carrots | Grandma lists chicken, ginger, carrots and lemon. | Chicken, ginger, some carrots and a little lemon.
? b | The soup takes about an ____ to make. | hour | Grandma says how long. | About an hour.
? c | What is the secret? | *Cooking it slowly | Adding salt | Using fresh fish | Grandma explains. | The secret is to cook it slowly.
? t | Grandma will write the recipe before lunch. | F | She will give it after lunch. | I'll give it to you after lunch.

## A day off for a wedding | WK
Manager: Hi Duc. You wanted to talk to me?
Duc: Yes. Could I have next Friday off? My sister is getting married.
Manager: Congratulations! Is your work finished for this week?
Duc: Almost. I'll finish the report on Thursday.
Manager: Then that's fine. Enjoy the wedding.
? c | What does Duc ask for? | *A day off next Friday | A new job | More money | He asks his manager. | Could I have next Friday off?
? c | Why does he need it? | *His sister is getting married | He is ill | He is moving house | He gives the reason. | My sister is getting married.
? b | He will finish the report on ____. | Thursday | Duc explains. | I'll finish the report on Thursday.
? t | The manager says no. | F | The manager agrees. | Then that's fine.

## The weekend forecast | NW
Presenter: Here's the forecast for the weekend.
Presenter: Saturday will be hot and sunny, with temperatures of around thirty-four degrees.
Presenter: On Sunday, strong winds and heavy rain are coming from the sea.
Presenter: If you're going to the beach, go on Saturday, and remember your sun cream.
? c | What will Saturday be like? | *Hot and sunny | Windy and wet | Cold and cloudy | The presenter describes Saturday. | Saturday will be hot and sunny
? b | The temperature on Saturday will be around thirty-____ degrees. | four / 4 | The presenter gives the number. | around thirty-four degrees.
? c | What is coming on Sunday? | *Strong winds and heavy rain | Snow | Fog | The presenter warns about Sunday. | strong winds and heavy rain are coming from the sea.
? t | The presenter suggests going to the beach on Sunday. | F | The advice is to go on Saturday. | go on Saturday

## A present for my brother | SH
Assistant: Can I help you?
Girl: Yes, I'm looking for a present for my brother. He's fifteen.
Assistant: What does he like?
Girl: Music and video games.
Assistant: How about these headphones? They're on sale this week, only forty dollars.
Girl: Perfect. Can you wrap them, please?
? c | Who is the present for? | *Her brother | Her father | Her friend | She tells the assistant. | a present for my brother.
? b | Her brother is ____ years old. | fifteen / 15 | She gives his age. | He's fifteen.
? c | What does the assistant suggest? | *Headphones | A video game | A book | The assistant suggests them. | How about these headphones?
? t | The headphones are cheaper this week. | T | They are on sale. | They're on sale this week

## Music after midnight | HF
Woman: Hi. I live next door, in number ten.
Young man: Oh, hello. Is everything OK?
Woman: Well, your music was very loud last night, after midnight. My baby couldn't sleep.
Young man: I'm really sorry. It was my birthday party.
Woman: That's OK, but please keep it quiet after ten o'clock.
Young man: Of course. It won't happen again.
? b | The woman lives in number ____. | ten / 10 | She introduces herself. | in number ten.
? c | What was the problem? | *Loud music after midnight | A broken window | A dog barking | She explains. | your music was very loud last night, after midnight.
? c | Why was there music? | *It was his birthday party | He was practising | He forgot to turn it off | He explains. | It was my birthday party.
? t | The young man promises it will not happen again. | T | He says so at the end. | It won't happen again.

## Directions to the museum | PT
Tourist: Excuse me. How do I get to the history museum?
Local: Go down this street and turn left at the church.
Tourist: Left at the church.
Local: Then walk for about five minutes. The museum is opposite the park.
Tourist: Is it open today?
Local: Yes, but it closes early on Sundays, at three.
? c | Where should the tourist turn left? | *At the church | At the park | At the bank | The local explains. | turn left at the church.
? b | Walk for about ____ minutes. | five / 5 | The local gives the time. | walk for about five minutes.
? c | Where is the museum? | *Opposite the park | Next to the church | Behind the station | The local says where. | The museum is opposite the park.
? c | What time does it close on Sundays? | *At three | At five | At noon | The local warns the tourist. | it closes early on Sundays, at three.

## Booking a haircut | DL
Receptionist: Good morning, Style Salon.
Customer: Hi. I'd like to book a haircut for Thursday afternoon.
Receptionist: We have two o'clock or four thirty.
Customer: Four thirty, please. My name is Vy.
Receptionist: OK, Vy. Do you want a wash too?
Customer: No, just a cut, thanks.
? c | Which day does the customer want? | *Thursday | Tuesday | Friday | She says the day. | for Thursday afternoon.
? c | What time is the appointment? | *Four thirty | Two o'clock | Three thirty | She chooses. | Four thirty, please.
? t | The customer wants a wash. | F | She wants just a cut. | No, just a cut, thanks.
? b | The customer's name is ____. | Vy | She gives her name. | My name is Vy.

## The school concert | ED
Principal: Good morning, parents.
Principal: Our school concert is on Friday the twentieth, at six o'clock, in the school hall.
Principal: The children will sing, dance and play music.
Principal: Tickets are free, but please tell your child's teacher how many seats you need by Monday.
? b | The concert is on Friday the ____. | twentieth / 20th | The principal gives the date. | on Friday the twentieth
? c | Where is the concert? | *In the school hall | In the park | At the theatre | The principal says where. | in the school hall.
? c | How much are the tickets? | *They are free | Five dollars | Ten dollars | The principal explains. | Tickets are free
? t | Parents must tell the teacher about seats by Monday. | T | The principal asks for this. | please tell your child's teacher how many seats you need by Monday.

## Feeling ill at work | HE
Hoa: You don't look well. Are you OK?
Nam: I've had a stomach ache since this morning.
Hoa: Did you eat something bad?
Nam: Maybe. I had some seafood last night.
Hoa: You should go home and rest. I'll tell the manager.
Nam: Thanks, Hoa. I'll call the doctor too.
? c | What is wrong with Nam? | *A stomach ache | A headache | A cold | He explains. | I've had a stomach ache since this morning.
? c | What did he eat last night? | *Seafood | Chicken | Pizza | He tells Hoa. | I had some seafood last night.
? c | What does Hoa suggest? | *Going home to rest | Eating more | Working harder | Hoa gives advice. | You should go home and rest.
? t | Hoa will call the doctor. | F | Nam will call the doctor; Hoa will tell the manager. | I'll call the doctor too.

## Mum's birthday dinner | PF
Linh: It's Mum's birthday on Sunday. What shall we do?
Tuan: Let's cook dinner for her.
Linh: Good idea. She loves Italian food.
Tuan: I can make pasta, and you can make a cake.
Linh: OK. And let's buy her some flowers in the morning.
? c | When is Mum's birthday? | *On Sunday | On Saturday | Today | Linh says it. | It's Mum's birthday on Sunday.
? c | What kind of food does Mum love? | *Italian food | Japanese food | Thai food | Linh tells Tuan. | She loves Italian food.
? c | What will Linh make? | *A cake | Pasta | Soup | Tuan suggests it. | you can make a cake.
? b | They will buy flowers in the ____. | morning | Linh suggests a time. | let's buy her some flowers in the morning.

## The best way to the airport | TP
Woman: What's the best way to get to the airport from here?
Man: You can take a taxi, but it's expensive. About forty dollars.
Woman: Is there a bus?
Man: Yes, the airport bus leaves every twenty minutes from the main square. It costs five dollars.
Woman: How long does it take?
Man: About forty-five minutes.
? c | Why doesn't the man recommend a taxi? | *It is expensive | It is slow | It is dangerous | He explains. | it's expensive.
? b | The airport bus leaves every ____ minutes. | twenty / 20 | The man says how often. | leaves every twenty minutes
? c | Where does the bus leave from? | *The main square | The station | The hotel | He says where. | from the main square.
? c | How much is the bus? | *Five dollars | Forty dollars | Twenty dollars | He gives the price. | It costs five dollars.

## A phone that keeps freezing | TE
Customer: Hi. My phone keeps freezing, and the screen goes black.
Technician: How old is it?
Customer: About two years.
Technician: Have you updated the software?
Customer: No, I haven't.
Technician: Try that first. If it still freezes, bring it back and we'll look inside.
? c | What is the problem with the phone? | *It freezes and the screen goes black | It won't charge | It is broken in half | The customer explains. | My phone keeps freezing, and the screen goes black.
? b | The phone is about ____ years old. | two / 2 | The customer answers. | About two years.
? t | The customer has updated the software. | F | The customer hasn't. | No, I haven't.
? c | What should the customer do first? | *Update the software | Buy a new phone | Leave the phone at the shop | The technician advises. | Try that first.

## Volunteering with animals | AN
Interviewer: Why do you want to volunteer here?
Mai: I love animals, and I have free time at weekends.
Interviewer: Great. Volunteers walk the dogs and clean the cages. Is that OK?
Mai: Yes, no problem.
Interviewer: Can you come every Saturday morning, from eight to twelve?
Mai: Yes, I can.
? c | Why does Mai want to volunteer? | *She loves animals and has free time | She needs money | Her school asked her | She explains. | I love animals, and I have free time at weekends.
? c | What do volunteers do? | *Walk the dogs and clean the cages | Feed the birds | Answer the phone | The interviewer explains. | Volunteers walk the dogs and clean the cages.
? b | Mai will volunteer every Saturday ____. | morning | The interviewer asks about Saturday. | every Saturday morning
? t | Mai will work for four hours each time. | T | From eight to twelve is four hours. | from eight to twelve?

## Getting ready for a party | DL
Ben: How many people are coming to your party?
Sara: About twenty. I've invited my classmates and some neighbours.
Ben: Do you need any help with food?
Sara: Yes, please. Could you make some spring rolls?
Ben: Sure. What time does it start?
Sara: At seven. Come at six if you can, to help me get ready.
? b | About ____ people are coming. | twenty / 20 | Sara answers. | About twenty.
? c | What will Ben make? | *Spring rolls | A cake | Pizza | Sara asks him. | Could you make some spring rolls?
? c | What time does the party start? | *At seven | At six | At eight | Sara says the time. | At seven.
? t | Sara wants Ben to arrive early. | T | She asks him to come at six. | Come at six if you can

## Kenji's first day | ED
Teacher: Class, this is Kenji. He's from Japan.
Kenji: Hello, everyone.
Teacher: Kenji, you can sit next to Minh. Minh, can you show him around the school today?
Minh: Sure. Hi, Kenji. Do you like football?
Kenji: Yes, I love it!
Minh: Great. We play every day at lunchtime.
? c | Where is Kenji from? | *Japan | Korea | China | The teacher introduces him. | He's from Japan.
? c | Who will Kenji sit next to? | *Minh | The teacher | Nobody | The teacher says so. | you can sit next to Minh.
? t | Kenji does not like football. | F | He says he loves it. | Yes, I love it!
? c | When do they play football? | *Every day at lunchtime | After school | At the weekend | Minh says when. | We play every day at lunchtime.

## Saving for a holiday | MS
Anh: I want to go to Thailand next summer, but it's expensive.
Bao: How much do you need?
Anh: About six hundred dollars.
Bao: You could save fifty dollars a month. That's twelve months.
Anh: Hmm, that's a whole year. I'll take a weekend job too.
? c | Where does Anh want to go? | *Thailand | Japan | Singapore | Anh says it first. | I want to go to Thailand next summer
? b | Anh needs about six hundred ____. | dollars | Anh gives the amount. | About six hundred dollars.
? c | How much does Bao suggest saving each month? | *Fifty dollars | Six hundred dollars | Twelve dollars | Bao suggests it. | You could save fifty dollars a month.
? c | What else will Anh do? | *Take a weekend job | Borrow money | Travel later | Anh decides. | I'll take a weekend job too.

## City bikes | TP
Speaker: Welcome to the city bike scheme.
Speaker: You can rent a bike from any of our sixty stations.
Speaker: The first thirty minutes are free. After that, it costs one dollar an hour.
Speaker: Download our app to unlock a bike, and please return it to a station when you finish.
? b | There are ____ stations. | sixty / 60 | The speaker gives the number. | any of our sixty stations.
? c | How much are the first thirty minutes? | *Free | One dollar | Two dollars | The speaker explains the price. | The first thirty minutes are free.
? c | How do you unlock a bike? | *With the app | With a key | With a card | The speaker explains. | Download our app to unlock a bike
? t | You can leave the bike anywhere. | F | You must return it to a station. | please return it to a station when you finish.

## Lunch with a colleague | WK
Lan: Do you want to have lunch together?
Peter: Sure. Where shall we go?
Lan: There's a new noodle shop across the road. It's cheap and fast.
Peter: Great. I have a meeting at one, so I need to be back by twelve forty-five.
Lan: No problem. Let's go now.
? c | Where will they eat? | *At a new noodle shop | In the office | At a pizza place | Lan suggests it. | There's a new noodle shop across the road.
? c | Why does Lan like the shop? | *It's cheap and fast | It's quiet | It has a garden | She explains. | It's cheap and fast.
? b | Peter has a meeting at ____. | one / 1 | Peter says when. | I have a meeting at one
? t | Peter must be back by twelve forty-five. | T | He says so. | I need to be back by twelve forty-five.

## A dog or a cat? | AN
Daughter: Can we get a pet, Dad?
Dad: What kind of pet?
Daughter: A dog!
Dad: A dog needs a lot of time and space. Our flat is small.
Daughter: What about a cat, then? Cats are happy inside.
Dad: OK, let's think about a cat. But you must feed it every day.
? c | Which pet does the daughter want first? | *A dog | A cat | A fish | She asks for one. | A dog!
? c | Why isn't a dog a good idea? | *The flat is small | Dad doesn't like dogs | Dogs are expensive | Dad explains. | Our flat is small.
? c | Which pet might they get? | *A cat | A rabbit | A bird | Dad agrees to think about it. | let's think about a cat.
? t | The daughter must feed the pet every day. | T | Dad says so. | you must feed it every day.

## A book three days late | ED
Student: Hi. I'm returning this book. I'm sorry it's late.
Librarian: Let me see. It's three days late.
Student: Do I have to pay?
Librarian: Yes, it's twenty cents a day, so sixty cents.
Student: OK. Here you are.
Librarian: Thank you. Next time you can renew books online.
? b | The book is ____ days late. | three / 3 | The librarian checks. | It's three days late.
? c | How much does the student pay? | *Sixty cents | Twenty cents | Three dollars | The librarian works it out. | so sixty cents.
? c | What can the student do next time? | *Renew books online | Borrow more books | Return books by post | The librarian explains. | Next time you can renew books online.
? t | The student refuses to pay. | F | The student pays. | OK. Here you are.

## Why breakfast matters | HE
Nurse: Many people don't eat breakfast, but it's an important meal.
Nurse: A good breakfast gives you energy for the morning.
Nurse: Try eggs, fruit or a bowl of oats instead of sweet cakes.
Nurse: And drink water or milk, not sugary drinks.
? t | The nurse says breakfast is important. | T | She says so. | it's an important meal.
? c | What does a good breakfast give you? | *Energy for the morning | A good night's sleep | Strong teeth | The nurse explains. | A good breakfast gives you energy for the morning.
? c | What does the nurse suggest instead of cakes? | *Eggs, fruit or oats | Bread and jam | Chocolate | The nurse gives examples. | Try eggs, fruit or a bowl of oats
? c | What should you drink? | *Water or milk | Coffee | Fruit juice | The nurse advises. | drink water or milk

## A cooking class for beginners | FD
Receptionist: Hello, Saigon Cooking School.
Man: Hi. Do you have a class for beginners?
Receptionist: Yes. Our beginners' class is on Saturday, from ten to one. You cook three dishes.
Man: How much is it?
Receptionist: Thirty-five dollars, and you eat everything you cook!
Man: Great. Can I book for this Saturday?
? c | Who is the class for? | *Beginners | Children | Chefs | The man asks for beginners. | Do you have a class for beginners?
? b | Students cook ____ dishes. | three / 3 | The receptionist explains. | You cook three dishes.
? b | The class costs thirty-____ dollars. | five / 5 | The receptionist gives the price. | Thirty-five dollars
? t | The class lasts three hours. | T | From ten to one is three hours. | from ten to one.

## The broken shower | HF
Guest: Hello, reception? The shower in my room isn't working.
Receptionist: I'm sorry. Which room are you in?
Guest: Room three one four.
Receptionist: I'll send someone up in ten minutes. Would you like to use the gym shower meanwhile?
Guest: No, I'll wait. Thank you.
? c | What is the problem? | *The shower isn't working | The light is broken | The room is noisy | The guest explains. | The shower in my room isn't working.
? b | The guest is in room three one ____. | four / 4 | The guest gives the room number. | Room three one four.
? c | When will someone come? | *In ten minutes | In an hour | Tomorrow | The receptionist says when. | I'll send someone up in ten minutes.
? t | The guest will use the gym shower. | F | The guest will wait. | No, I'll wait.

## Action or comedy? | HS
Nga: What shall we watch tonight?
Tom: How about the new action film?
Nga: I don't really like action films. What about a comedy?
Tom: OK. There's a funny one about a family on holiday. It starts at eight fifteen.
Nga: Perfect. Let's have dinner first, at seven.
? c | What kind of film does Tom suggest first? | *An action film | A comedy | A cartoon | Tom suggests it. | How about the new action film?
? c | What kind of film do they choose? | *A comedy | An action film | A horror film | Nga prefers it. | What about a comedy?
? b | The film starts at eight ____. | fifteen / 15 | Tom gives the time. | It starts at eight fifteen.
? c | What will they do at seven? | *Have dinner | Watch the film | Meet friends | Nga suggests it. | Let's have dinner first, at seven.

## A new day for recycling | EN
Speaker: Hello, this is a message from the city council.
Speaker: From next week, the recycling truck will come on Tuesdays, not Mondays.
Speaker: Please put paper and plastic in the yellow bin, and glass in the blue bin.
Speaker: Thank you for helping to keep our city clean.
? c | Who is the message from? | *The city council | A school | A supermarket | The speaker says it first. | this is a message from the city council.
? c | When will the truck come from next week? | *On Tuesdays | On Mondays | On Fridays | The speaker explains the change. | the recycling truck will come on Tuesdays, not Mondays.
? b | Glass goes in the ____ bin. | blue | The speaker explains. | glass in the blue bin.
? t | Paper goes in the blue bin. | F | Paper goes in the yellow bin. | Please put paper and plastic in the yellow bin

## A photo from Sa Pa | TR
Kim: Is this you in the photo?
Lan: Yes! That's me and my cousin in Sa Pa last winter.
Kim: It looks cold!
Lan: It was very cold, about five degrees. But the mountains were beautiful.
Kim: Did you walk a lot?
Lan: Yes, we walked to a village and stayed with a local family for two nights.
? c | Where was the photo taken? | *In Sa Pa | In Da Lat | In Hue | Lan says where. | in Sa Pa last winter.
? b | The temperature was about ____ degrees. | five / 5 | Lan remembers. | about five degrees.
? c | Who is in the photo with Lan? | *Her cousin | Her sister | Her friend Kim | Lan says who. | That's me and my cousin
? t | They stayed with a local family for two nights. | T | Lan says so. | stayed with a local family for two nights.

## Where is my parcel? | SH
Ben: I ordered a jacket online, but it hasn't arrived.
Mia: When did you order it?
Ben: Ten days ago. They said delivery takes five days.
Mia: Did you check the tracking number?
Ben: Yes. It says the parcel is at the post office.
Mia: Then go and collect it. Take your ID card.
? c | What did Ben order? | *A jacket | Some shoes | A phone | Ben says so. | I ordered a jacket online
? b | He ordered it ____ days ago. | ten / 10 | Ben says when. | Ten days ago.
? c | Where is the parcel? | *At the post office | At his neighbour's house | In the shop | The tracking shows it. | It says the parcel is at the post office.
? c | What should Ben take? | *His ID card | His phone | Some money | Mia advises him. | Take your ID card.

## A nurse and a teacher | WK
Huong: What do you do, Mark?
Mark: I'm a nurse. I work at the children's hospital.
Huong: Do you like it?
Mark: Yes, but the hours are long. Sometimes I work at night.
Huong: I'm a teacher, so I work during the day and have long holidays.
Mark: Lucky you!
? c | What is Mark's job? | *A nurse | A doctor | A teacher | Mark answers. | I'm a nurse.
? c | Where does he work? | *At the children's hospital | At a school | At a clinic | He explains. | I work at the children's hospital.
? t | Mark sometimes works at night. | T | He says so. | Sometimes I work at night.
? c | What is good about Huong's job? | *Long holidays | High pay | Short days | Huong says so. | have long holidays.

## Feeding the ducks | NW
Grandpa: Shall we go for a walk in the park?
Linh: OK, but it's a bit windy.
Grandpa: Put on your jacket. The fresh air will be good for us.
Linh: Can we feed the ducks?
Grandpa: Yes, but not with bread. I've brought some seeds.
? c | What is the weather like? | *A bit windy | Very hot | Rainy | Linh says so. | it's a bit windy.
? c | What does Grandpa tell Linh to do? | *Put on a jacket | Take an umbrella | Wear a hat | He gives advice. | Put on your jacket.
? c | What will they feed the ducks? | *Seeds | Bread | Rice | Grandpa explains. | I've brought some seeds.
? t | Grandpa says bread is good for the ducks. | F | He says not with bread. | but not with bread.

## At the pharmacy | HE
Pharmacist: Good afternoon. How can I help?
Woman: I have a cold and a runny nose.
Pharmacist: Take these tablets three times a day, after meals.
Woman: Can I drive after taking them?
Pharmacist: It's better not to. They can make you sleepy.
? c | What is wrong with the woman? | *A cold and a runny nose | A headache | A cough | She explains. | I have a cold and a runny nose.
? b | She should take the tablets ____ times a day. | three / 3 | The pharmacist explains. | three times a day
? c | When should she take them? | *After meals | Before meals | At night only | The pharmacist explains. | after meals.
? t | The tablets can make her sleepy. | T | The pharmacist warns her. | They can make you sleepy.

## The photography club | HS
Student: Hi. I'd like to join the photography club.
Leader: Great! We meet every Wednesday at four in room twelve.
Student: Do I need a good camera?
Leader: No, you can start with your phone.
Student: Is there a fee?
Leader: Ten dollars a term. That pays for printing photos.
? c | Which club does the student want to join? | *Photography | Music | Chess | The student says it. | I'd like to join the photography club.
? c | Where does the club meet? | *In room twelve | In the library | In the hall | The leader says where. | in room twelve.
? t | Members need an expensive camera. | F | They can start with a phone. | you can start with your phone.
? b | The fee pays for printing ____. | photos / photographs | The leader explains. | That pays for printing photos.

## An accident on the bridge | TP
Woman: Excuse me, has the number five bus come yet?
Man: No. It's twenty minutes late. There's an accident on the bridge.
Woman: Oh no. I need to be at work at nine.
Man: You could take the train. The station is just around the corner.
Woman: Good idea. Thanks!
? c | Why is the bus late? | *There's an accident on the bridge | The driver is ill | It's raining | The man explains. | There's an accident on the bridge.
? b | The bus is ____ minutes late. | twenty / 20 | The man says how late. | It's twenty minutes late.
? c | What does the man suggest? | *Taking the train | Walking | Taking a taxi | He gives an idea. | You could take the train.
? c | Where is the station? | *Around the corner | Over the bridge | Next to her office | The man says where. | The station is just around the corner.

## A leaking pipe | HF
Woman: Hello, this is Mrs. Tran at forty-two Hoa Binh Street.
Woman: The pipe under my kitchen sink is leaking, and there's water on the floor.
Woman: Could you come today, please? I'm at home all afternoon.
Woman: My number is zero nine eight, seven six five, four three two.
? b | Mrs. Tran lives at forty-____ Hoa Binh Street. | two / 2 | She gives her address. | at forty-two Hoa Binh Street.
? c | Where is the leak? | *Under the kitchen sink | In the bathroom | On the roof | She describes it. | The pipe under my kitchen sink is leaking
? c | When is she at home? | *All afternoon | All morning | In the evening | She says when. | I'm at home all afternoon.
? t | She wants the plumber to come next week. | F | She asks for today. | Could you come today, please?

## A conversation course | ED
Teacher: Welcome to the English conversation course.
Teacher: Classes are on Monday and Wednesday evenings, from six to eight.
Teacher: Please speak English all the time in class, even if you make mistakes.
Teacher: At the end of the course there is a short speaking test, not a written exam.
? c | What kind of course is it? | *English conversation | English writing | Business English | The teacher says it. | Welcome to the English conversation course.
? c | When are the classes? | *Monday and Wednesday evenings | Tuesday and Thursday mornings | Saturday afternoons | The teacher explains. | Classes are on Monday and Wednesday evenings
? t | Students should never make mistakes. | F | The teacher says mistakes are fine. | even if you make mistakes.
? c | What happens at the end of the course? | *A short speaking test | A written exam | A party | The teacher explains. | there is a short speaking test, not a written exam.

## A friend moving to Canada | PF
Nam: My friend is moving to Canada. I want to give him something.
Hoa: How about a photo album of your trips together?
Nam: That's lovely. Do you think he'll like it?
Hoa: Of course. He can show it to his new friends.
Nam: I'll print the photos tomorrow.
? c | Where is Nam's friend moving? | *To Canada | To Australia | To Japan | Nam says so. | My friend is moving to Canada.
? c | What does Hoa suggest? | *A photo album | A book | A watch | Hoa suggests it. | How about a photo album of your trips together?
? b | Nam will print the photos ____. | tomorrow | Nam decides. | I'll print the photos tomorrow.
? t | Nam doesn't like the idea. | F | He says it's lovely. | That's lovely.

## Saving water at home | EN
Teacher: How can we save water at home?
An: We can turn off the tap when we brush our teeth.
Bich: And we can take short showers, not long baths.
Teacher: Good. What else?
An: My family collects rainwater for the garden.
Teacher: Excellent idea!
? c | What can people do when they brush their teeth? | *Turn off the tap | Use warm water | Use a small cup | An suggests it. | turn off the tap when we brush our teeth.
? c | What does Bich suggest? | *Taking short showers | Having baths | Washing less often | Bich gives an idea. | we can take short showers, not long baths.
? b | An's family collects ____ for the garden. | rainwater / rain water | An explains. | My family collects rainwater for the garden.
? t | The teacher likes the last idea. | T | The teacher says it is excellent. | Excellent idea!

## A new neighbour | PT
Carlos: Hi, I'm Carlos. I just moved into number six.
Thu: Welcome! I'm Thu. How do you like the area?
Carlos: It's nice, but where's the nearest supermarket?
Thu: There's one on Pine Road, five minutes away. The market is cheaper, though.
Carlos: Where's the market?
Thu: Behind the school. It's open every morning.
? b | Carlos lives at number ____. | six / 6 | He introduces himself. | I just moved into number six.
? c | Where is the nearest supermarket? | *On Pine Road | Behind the school | Next to the market | Thu explains. | There's one on Pine Road
? t | Thu says the market is cheaper. | T | Thu says so. | The market is cheaper, though.
? c | When is the market open? | *Every morning | Every evening | At weekends only | Thu says so. | It's open every morning.

## Homework left at home | ED
Teacher: Where's your homework, Long?
Long: I'm sorry. I left it at home.
Teacher: Did you finish it?
Long: Yes, I did. Can I bring it tomorrow?
Teacher: OK, but this is the second time this month. Please be more careful.
? c | Why doesn't Long have his homework? | *He left it at home | He didn't do it | He lost it | Long explains. | I left it at home.
? t | Long finished the homework. | T | He says yes. | Yes, I did.
? c | When will he bring it? | *Tomorrow | Next week | After school today | He asks. | Can I bring it tomorrow?
? b | It is the ____ time this month. | second / 2nd | The teacher warns him. | this is the second time this month.

## Opening a bank account | MS
Clerk: Good morning. How can I help?
Student: I'd like to open a bank account.
Clerk: Of course. Do you have your ID card?
Student: Yes, here it is.
Clerk: Thank you. Is it a savings account or a normal account?
Student: A savings account, please. I want to save for university.
? c | What does the student want? | *To open a bank account | To borrow money | To change money | The student says it. | I'd like to open a bank account.
? c | What does the clerk ask for? | *An ID card | A photo | A letter | The clerk asks. | Do you have your ID card?
? c | What kind of account does the student choose? | *A savings account | A normal account | A business account | The student chooses. | A savings account, please.
? b | The student wants to save for ____. | university | The student explains. | I want to save for university.

## Ordering a taxi with an app | TE
Dad: Can you help me with this app? I want to order a taxi.
Daughter: Sure. First, type where you want to go.
Dad: OK. The station.
Daughter: Now choose the kind of car and press Book.
Dad: It says the driver will arrive in four minutes.
Daughter: See? Easy!
? c | What does Dad want to do? | *Order a taxi | Buy a ticket | Send a message | He explains. | I want to order a taxi.
? c | Where does he want to go? | *The station | The airport | The hospital | Dad types it. | The station.
? b | The driver will arrive in ____ minutes. | four / 4 | The app tells him. | the driver will arrive in four minutes.
? t | The daughter thinks the app is difficult. | F | She says it is easy. | See? Easy!
"""

LESSONS["B1"] = """
## Choosing a laptop | TE
Assistant: Are you looking for anything in particular?
Customer: I need a laptop for university. Mostly for writing essays and video calls.
Assistant: Then you don't need anything powerful. This one is light, and the battery lasts about twelve hours.
Customer: That sounds good. What about storage? I keep a lot of photos.
Assistant: It has enough for most students, but you could also use cloud storage for your photos.
Customer: And the price?
Assistant: Five hundred and fifty, and there's a student discount of ten percent.
? c | What will the customer mainly use the laptop for? | *Essays and video calls | Games and films | Photo editing | The customer explains. | Mostly for writing essays and video calls.
? b | The battery lasts about ____ hours. | twelve / 12 | The assistant says so. | the battery lasts about twelve hours.
? c | What does the assistant suggest for photos? | *Cloud storage | A bigger laptop | A second laptop | The photos can be kept online. | you could also use cloud storage for your photos.
? t | Students pay less than the normal price. | T | There is a student discount. | there's a student discount of ten percent.

## An interview at a café | WK
Manager: So, Lan, why do you want to work here?
Lan: I love coffee, and I enjoy meeting people. I also want to improve my English, and you have many foreign customers.
Manager: Have you worked in a café before?
Lan: Not in a café, but I worked in a bookshop last summer, so I'm used to serving customers.
Manager: The job is three evenings a week and Saturday mornings. Is that OK with your studies?
Lan: Yes, my classes finish at four, so evenings are fine.
? c | Why does Lan want this job in particular? | *To practise English with foreign customers | It pays very well | It is near her home | Lan mentions the foreign customers. | I also want to improve my English, and you have many foreign customers.
? t | Lan has worked in a café before. | F | Lan worked in a bookshop. | Not in a café, but I worked in a bookshop last summer
? c | When is the job? | *Three evenings a week and Saturday mornings | Every morning | Weekends only | The manager explains. | The job is three evenings a week and Saturday mornings.
? b | Lan's classes finish at ____. | four / 4 | Lan explains. | my classes finish at four

## No heating in the flat | HF
Tenant: Hi, Mr. Long. I'm calling about the heating in the flat. It stopped working last night.
Landlord: Oh no. Is it completely off, or just weak?
Tenant: Completely off. The radiators are cold, and it's only eight degrees inside.
Landlord: I'll call the repair company now. They usually come within a day.
Tenant: Could you ask them to come in the morning? I work from home after lunch and have meetings.
Landlord: I'll try. I'll text you the time.
? c | What is the problem? | *The heating has stopped working | The water is cold | The lights are off | The tenant explains. | It stopped working last night.
? b | It is ____ degrees inside. | eight / 8 | The tenant says so. | it's only eight degrees inside.
? c | Why does the tenant prefer the morning? | *The tenant has meetings after lunch | The tenant goes out in the afternoon | The shops close early | The tenant explains. | I work from home after lunch and have meetings.
? t | The landlord will send a text with the time. | T | He promises to. | I'll text you the time.

## The train to Da Nang | TP
Announcer: Attention, please. Passengers for the twelve thirty service to Da Nang.
Announcer: Because of a signal problem near Hue, this train is delayed by approximately forty minutes.
Announcer: The new departure time is one ten, from platform three instead of platform one.
Announcer: Passengers can get a free drink at the station café by showing their ticket. We apologise for the delay.
? c | Why is the train delayed? | *A signal problem | Bad weather | A broken train | The announcer explains. | Because of a signal problem near Hue
? b | The new departure time is one ____. | ten / 10 | The new time is given. | The new departure time is one ten
? c | Which platform will the train leave from? | *Platform three | Platform one | Platform ten | The platform has changed. | from platform three instead of platform one.
? c | What can passengers get at the café? | *A free drink | A free meal | A cheaper ticket | Passengers show their ticket. | Passengers can get a free drink

## Learning to cook | FD
Minh: I've decided to learn to cook properly. I spend too much on takeaways.
Sara: Good for you. How are you learning?
Minh: I watch short videos online and try one new recipe every weekend.
Sara: What's the best thing you've made so far?
Minh: A fish curry. It took ages, but my flatmates loved it.
Sara: You should start with quick dishes for weekdays, though. Then you'll actually cook after work.
? c | Why did Minh decide to learn to cook? | *He spends too much on takeaways | His flatmates asked him | He wants to be a chef | He gives his reason. | I spend too much on takeaways.
? c | How is he learning? | *By watching videos and trying a recipe each weekend | By taking a class | By reading cookbooks | He explains. | I watch short videos online and try one new recipe every weekend.
? t | The fish curry was quick to make. | F | It took ages. | It took ages
? c | What does Sara advise? | *Starting with quick dishes for weekdays | Cooking only at weekends | Buying better pans | She gives advice. | You should start with quick dishes for weekdays

## A tour of the history museum | ED
Guide: Welcome to the National History Museum. Our tour today lasts about an hour.
Guide: We'll start on the ground floor with tools and pottery more than two thousand years old.
Guide: Then we'll go upstairs to see how people lived in the nineteenth century.
Guide: Please don't touch the objects. Photos are allowed, but without flash. The gift shop is next to the exit.
? b | The tour lasts about an ____. | hour | The guide says so. | Our tour today lasts about an hour.
? c | What is on the ground floor? | *Very old tools and pottery | Paintings | Nineteenth-century homes | The guide explains. | tools and pottery more than two thousand years old.
? t | Visitors may not take any photos. | F | Photos are allowed without flash. | Photos are allowed, but without flash.
? c | Where is the gift shop? | *Next to the exit | Upstairs | At the entrance | The guide says so. | The gift shop is next to the exit.

## Tired all the time | HE
Doctor: You said you're tired all the time. How many hours do you sleep?
Patient: About five. I go to bed late because I study at night.
Doctor: Do you use your phone in bed?
Patient: Yes, usually for an hour or so.
Doctor: Try putting it away thirty minutes before sleeping, and go to bed at the same time every night. Most adults need seven to eight hours.
Patient: I'll try. Should I drink less coffee too?
Doctor: Yes, especially after lunch.
? b | The patient sleeps about ____ hours. | five / 5 | The patient answers. | About five.
? c | Why does the patient go to bed late? | *They study at night | They work late | They watch films | The patient explains. | I go to bed late because I study at night.
? c | What does the doctor suggest about the phone? | *Putting it away thirty minutes before sleeping | Turning it off all day | Using it only in the morning | The doctor advises. | Try putting it away thirty minutes before sleeping
? t | The doctor says coffee after lunch is fine. | F | The doctor advises less coffee, especially after lunch. | Yes, especially after lunch.

## A camping weekend | NW
Huy: The forecast says it'll rain on Saturday but be sunny on Sunday.
Anna: Then let's leave on Sunday morning and come back Monday evening.
Huy: Monday? I have to work.
Anna: Can't you take a day off? You said you have holidays left.
Huy: True. I'll ask my boss tomorrow. What do we need to bring?
Anna: The tent is in my garage. You bring the food, and I'll bring the cooking things.
? c | Why do they change the plan? | *Rain is forecast on Saturday | Huy is ill | The tent is broken | Huy mentions the forecast. | it'll rain on Saturday but be sunny on Sunday.
? c | What problem does Huy have with Monday? | *He has to work | He has an exam | His car is broken | Huy explains. | I have to work.
? c | Who will bring the food? | *Huy | Anna | Both of them | Anna divides the jobs. | You bring the food
? t | The tent is at Huy's house. | F | It is in Anna's garage. | The tent is in my garage.

## The Sunrise Running Group | HS
Leader: Welcome to the Sunrise Running Group. We meet at the lake every Tuesday and Friday at six.
Leader: We have three groups: beginners run three kilometres, the middle group runs five, and the fast group runs ten.
Leader: Everyone starts in the beginners' group for the first two weeks, even if you're fit.
Leader: It's free, but please bring water and wear bright clothes in the dark winter months.
? c | When does the group meet? | *Tuesday and Friday at six | Every day at six | Weekends at seven | The leader explains. | every Tuesday and Friday at six.
? b | The fast group runs ____ kilometres. | ten / 10 | The leader lists the groups. | the fast group runs ten.
? t | New members start in the beginners' group. | T | Everyone starts there for two weeks. | Everyone starts in the beginners' group for the first two weeks
? c | Why should runners wear bright clothes? | *It is dark in winter | It is a rule of the lake | It looks good in photos | The leader explains. | wear bright clothes in the dark winter months.

## The wrong sofa | SH
Customer: Hello, I ordered a blue sofa from your website, but you delivered a grey one.
Agent: I'm very sorry. Can I have your order number?
Customer: It's A four five seven two.
Agent: Thank you. Yes, I can see the mistake. We can collect the grey sofa and deliver the blue one next Tuesday.
Customer: Next Tuesday? That's a week away.
Agent: I understand. I can give you a twenty percent refund for the trouble.
Customer: OK, that's fair.
? c | What was the mistake? | *The sofa was the wrong colour | The sofa was broken | The sofa was late | The customer explains. | you delivered a grey one.
? b | The correct sofa will arrive next ____. | Tuesday | The agent explains. | deliver the blue one next Tuesday.
? c | How does the agent make up for the trouble? | *A twenty percent refund | A free cushion | Free delivery next time | The agent offers it. | I can give you a twenty percent refund for the trouble.
? t | The customer is unhappy with the final offer. | F | The customer says it's fair. | OK, that's fair.

## Medicine or design? | ED
Teacher: Have you decided what to do after school, Vy?
Vy: Not really. My parents want me to study medicine, but I'm more interested in design.
Teacher: Have you talked to them about it?
Vy: A little. They worry that design jobs aren't safe.
Teacher: Maybe you could show them some information about careers in design. There are more jobs than people think, especially online.
Vy: That's a good idea. I'll look for some examples this weekend.
? c | What do Vy's parents want her to study? | *Medicine | Design | Law | Vy says so. | My parents want me to study medicine
? c | Why are her parents worried? | *They think design jobs aren't safe | Design is expensive | Vy is not good at design | Vy explains. | They worry that design jobs aren't safe.
? c | What does the teacher suggest? | *Showing her parents information about design careers | Choosing medicine | Asking another teacher | The teacher advises. | show them some information about careers in design.
? t | Vy will look for examples this weekend. | T | She says so. | I'll look for some examples this weekend.

## The new shopping centre | PT
Reporter: The new shopping centre opened on Saturday, and thousands of people came.
Reporter: It has over a hundred shops, a cinema and a large food court.
Reporter: However, some local shop owners are worried. Mrs. Hanh, who runs a clothes shop nearby, says her customers have already dropped by a third.
Reporter: The city says it will build a new car park next year, which may bring more visitors to the old streets as well.
? c | What does the new shopping centre have? | *Over a hundred shops, a cinema and a food court | A hotel and a swimming pool | A market and a park | The reporter describes it. | It has over a hundred shops, a cinema and a large food court.
? c | Why is Mrs. Hanh worried? | *Her customers have dropped by a third | Her shop is too small | Her rent has gone up | The reporter explains. | her customers have already dropped by a third.
? t | The city has already built a new car park. | F | It will build one next year. | The city says it will build a new car park next year
? c | What may the car park do? | *Bring more visitors to the old streets | Reduce traffic | Close the old shops | The reporter suggests it. | may bring more visitors to the old streets as well.

## A tour of the Mekong Delta | TR
Agent: This tour of the Mekong Delta is our most popular. It's two days and one night.
Tourist: What's included?
Agent: Transport, a boat trip, the hotel and all meals except dinner on the first night.
Tourist: Is it suitable for children? My son is seven.
Agent: Yes, and children under ten pay half price.
Tourist: Great. Then we'll book for two adults and one child for next weekend.
? b | The tour lasts two days and one ____. | night | The agent says so. | It's two days and one night.
? c | Which meal is NOT included? | *Dinner on the first night | Breakfast on the second day | Lunch on the first day | The agent explains. | all meals except dinner on the first night.
? c | How much does the son pay? | *Half price | Nothing | Full price | Children under ten pay half. | children under ten pay half price.
? t | They will book for two adults and two children. | F | They book for one child. | we'll book for two adults and one child

## A car in front of the garage | HF
Man: Excuse me, is this your car? It's blocking my garage.
Woman: Oh, I'm so sorry. I was only going to be five minutes, but my friend kept me talking.
Man: I need to leave for the airport now.
Woman: Of course, I'll move it right away.
Man: Thanks. There's usually space on the next street if you need it.
Woman: Good to know. It won't happen again.
? c | What is the problem? | *The woman's car is blocking his garage | His car is broken | She took his parking space at work | He explains. | It's blocking my garage.
? c | Why did she stay longer? | *Her friend kept her talking | She was shopping | She lost her keys | She explains. | my friend kept me talking.
? c | Where is the man going? | *To the airport | To work | To the hospital | He says so. | I need to leave for the airport now.
? t | The man tells her where she could park. | T | He mentions the next street. | There's usually space on the next street

## Animals in the city | AN
Speaker: You might think cities are bad places for animals, but many species are doing surprisingly well.
Speaker: Foxes now live in many European cities, where they find food in bins.
Speaker: Some birds of prey nest on tall buildings because they look like cliffs.
Speaker: But city life has problems too. Bright lights confuse birds at night, so some cities now switch off office lights during migration season.
? t | The speaker says all animals do badly in cities. | F | Many species are doing well. | many species are doing surprisingly well.
? c | Why do some birds nest on tall buildings? | *The buildings are like cliffs | They are warm | There is food on them | The speaker explains. | because they look like cliffs.
? c | What problem do bright lights cause? | *They confuse birds at night | They keep people awake | They waste money | The speaker explains. | Bright lights confuse birds at night
? c | What do some cities do? | *Switch off office lights during migration | Build more parks | Feed the birds | The speaker gives an example. | some cities now switch off office lights during migration season.

## Small changes, real savings | MS
Speaker: Many young people say they can't save because their income is too low. But small changes add up.
Speaker: Try the twenty-four-hour rule: wait a day before buying anything that isn't essential. Often, you'll realise you don't need it.
Speaker: Another tip is to save first, not last. When you get paid, move some money into savings straight away.
Speaker: Even ten percent of a small salary becomes a useful amount after a year.
? c | What is the twenty-four-hour rule? | *Waiting a day before buying something you don't need | Saving money every day | Shopping only in the morning | The speaker explains it. | wait a day before buying anything that isn't essential.
? c | What does save first mean? | *Moving money into savings as soon as you are paid | Saving before you borrow | Saving only at the end of the month | The speaker explains. | When you get paid, move some money into savings straight away.
? b | Even ten ____ of a small salary becomes useful. | percent / per cent | The speaker gives an example. | Even ten percent of a small salary
? t | The speaker says young people can't save at all. | F | Small changes add up. | But small changes add up.

## English for work on Saturdays | ED
Advisor: So, you want to improve your English for work. Do you prefer evening or weekend classes?
Learner: Evenings are difficult because I often work late. Weekends are better.
Advisor: We have a Saturday course from nine to twelve. It focuses on emails and meetings.
Learner: That sounds perfect. How many students are in a class?
Advisor: No more than twelve, so everyone gets a chance to speak.
Learner: And when does it start?
Advisor: The first Saturday of next month.
? c | Why are evenings difficult? | *The learner often works late | The learner has young children | The learner lives far away | The learner explains. | Evenings are difficult because I often work late.
? c | What does the Saturday course focus on? | *Emails and meetings | Grammar tests | Travel English | The advisor explains. | It focuses on emails and meetings.
? b | There are no more than ____ students in a class. | twelve / 12 | The advisor says so. | No more than twelve
? t | The course starts this Saturday. | F | It starts next month. | The first Saturday of next month.

## The flat share | HF
Linh: So, how is the new flat share going?
Duc: Mostly fine. The rent is cheaper than living alone, and the others are friendly.
Linh: Any problems?
Duc: The kitchen is always a mess. Nobody washes up after cooking.
Linh: You should make a cleaning rota. Then everyone knows whose turn it is.
Duc: Good idea. We have a house meeting on Sunday, so I'll suggest it then.
? c | What is good about the flat share? | *It's cheaper and the others are friendly | It's close to work | It's very quiet | Duc explains. | The rent is cheaper than living alone, and the others are friendly.
? c | What is the problem? | *Nobody washes up | The rent is high | It is noisy at night | Duc explains. | Nobody washes up after cooking.
? c | What does Linh suggest? | *A cleaning rota | Moving out | Eating out | Linh suggests it. | You should make a cleaning rota.
? b | They have a house meeting on ____. | Sunday | Duc says when. | We have a house meeting on Sunday

## When to water the garden | EN
Gardener: In summer, many people water their gardens in the middle of the day. That's a mistake.
Gardener: In the heat, much of the water evaporates before it reaches the roots.
Gardener: It's better to water early in the morning or in the evening.
Gardener: You can also cover the soil with dry leaves. This keeps it cool and damp for longer, so you use less water.
? c | What mistake do many people make? | *Watering in the middle of the day | Watering too little | Using rainwater | The gardener explains. | many people water their gardens in the middle of the day.
? c | Why is it a mistake? | *Much of the water evaporates | The plants grow too fast | It costs more money | The gardener explains. | much of the water evaporates before it reaches the roots.
? c | When should you water? | *Early in the morning or in the evening | At noon | Only at night | The gardener advises. | It's better to water early in the morning or in the evening.
? t | Dry leaves on the soil help you use less water. | T | The gardener says so. | so you use less water.

## Hoa's wedding | PF
Mai: Did you get the invitation to Hoa's wedding?
Tom: Yes! It's in her hometown, isn't it? That's five hours by car.
Mai: I'm thinking of taking the night bus on Friday. Do you want to come with me?
Tom: Good idea. It's cheaper than driving, and we can sleep on the way.
Mai: The wedding is on Saturday at eleven, so we'll have time to change.
Tom: What should we give them?
Mai: Most people give money in an envelope.
? b | Hoa's hometown is ____ hours away by car. | five / 5 | Tom says so. | That's five hours by car.
? c | How will they travel? | *By night bus | By car | By plane | Mai suggests it. | I'm thinking of taking the night bus on Friday.
? c | Why does Tom like the idea? | *It's cheaper and they can sleep | It's faster | It's more comfortable | He explains. | It's cheaper than driving, and we can sleep on the way.
? t | Most guests give money as a present. | T | Mai says so. | Most people give money in an envelope.

## A watch for runners | TE
Assistant: This watch is very popular with runners.
Customer: What can it do?
Assistant: It measures your distance, speed and heart rate. It also shows messages from your phone.
Customer: Does it need my phone with it when I run?
Assistant: No, it has its own GPS, so you can leave your phone at home.
Customer: How long does the battery last?
Assistant: About a week, or ten hours if you use GPS all the time.
? c | What can the watch measure? | *Distance, speed and heart rate | Only steps | Sleep and weight | The assistant lists them. | It measures your distance, speed and heart rate.
? t | You must carry your phone when you run. | F | The watch has its own GPS. | you can leave your phone at home.
? b | The battery lasts about a ____. | week | The assistant says so. | About a week
? c | How long does the battery last with GPS on all the time? | *Ten hours | A week | Two days | The assistant explains. | ten hours if you use GPS all the time.

## A hole in a tooth | HE
Dentist: How long have you had this pain?
Patient: About a week. It's worse when I drink something cold.
Dentist: Let me look. You have a small hole in this tooth. I can fill it today.
Patient: Will it hurt?
Dentist: You'll have an injection first, so you won't feel much.
Patient: OK. And how can I stop it happening again?
Dentist: Brush twice a day, and cut down on sweet drinks.
? c | When is the pain worse? | *When the patient drinks something cold | At night | When eating bread | The patient explains. | It's worse when I drink something cold.
? c | What will the dentist do today? | *Fill the tooth | Take the tooth out | Clean all the teeth | The dentist says so. | I can fill it today.
? t | The patient will have an injection. | T | The dentist explains. | You'll have an injection first
? c | What advice does the dentist give? | *Brush twice a day and have fewer sweet drinks | Stop drinking cold water | Use a new toothbrush every week | The dentist advises. | Brush twice a day, and cut down on sweet drinks.

## A suitcase that didn't arrive | TR
Officer: How can I help?
Passenger: My suitcase didn't arrive. I was on the flight from Singapore.
Officer: Can you describe it?
Passenger: It's a large black suitcase with a red ribbon on the handle.
Officer: It may still be in Singapore. We'll send it on the next flight and deliver it to your hotel.
Passenger: When will that be?
Officer: Probably tomorrow afternoon. Here's a form and a reference number.
? c | Where was the flight from? | *Singapore | Bangkok | Seoul | The passenger says so. | I was on the flight from Singapore.
? c | How can the suitcase be recognised? | *A red ribbon on the handle | A name on the side | It is very small | The passenger describes it. | with a red ribbon on the handle.
? c | Where will they deliver it? | *To the hotel | To the airport | To the passenger's home | The officer explains. | deliver it to your hotel.
? b | It will probably arrive tomorrow ____. | afternoon | The officer says so. | Probably tomorrow afternoon.

## Too many emails | WK
Manager: How's the new project going?
Hien: Well, it's a bit slow. We have different ideas about the design.
Manager: That's normal at the start. Have you all met to discuss it?
Hien: Only by email. People write long messages, and nobody agrees.
Manager: Emails can make disagreements worse. Book a short meeting where everyone shares one idea, then vote.
Hien: OK, I'll book a room for Thursday.
? c | Why is the project slow? | *The team has different ideas about the design | Someone is ill | They have no money | Hien explains. | We have different ideas about the design.
? c | How have they discussed it so far? | *Only by email | In long meetings | By phone | Hien explains. | Only by email.
? c | What does the manager suggest? | *A short meeting and a vote | More emails | Asking the client | The manager advises. | Book a short meeting where everyone shares one idea, then vote.
? t | Hien will book a room for Friday. | F | The room is for Thursday. | I'll book a room for Thursday.

## Tomatoes from the farm | FD
Seller: These tomatoes come from our farm, just twenty kilometres away.
Customer: They look much better than the ones in the supermarket.
Seller: We pick them the day before the market, so they're very fresh.
Customer: Are they organic?
Seller: We don't use chemicals, but we don't have the official certificate. It's very expensive for small farms.
Customer: I'll take two kilos, then.
? b | The farm is ____ kilometres away. | twenty / 20 | The seller says so. | just twenty kilometres away.
? c | When are the tomatoes picked? | *The day before the market | On the morning of the market | A week before | The seller explains. | We pick them the day before the market
? c | Why doesn't the farm have an organic certificate? | *It is too expensive for small farms | They use some chemicals | They don't need one | The seller explains. | It's very expensive for small farms.
? t | The customer decides not to buy any tomatoes. | F | The customer buys two kilos. | I'll take two kilos, then.

## Life without a car | TP
Interviewer: Why did you sell your car?
Woman: Partly the cost. Petrol, parking and repairs were about three hundred dollars a month.
Interviewer: Isn't it difficult without a car?
Woman: Not really. The metro is five minutes from my flat, and I cycle to the shops.
Interviewer: What about long trips?
Woman: I rent a car once or twice a year. It's still much cheaper.
? c | Why did she sell her car? | *Partly because of the cost | It was too old | She moved abroad | She explains. | Partly the cost.
? b | The car cost about three hundred dollars a ____. | month | She gives the figure. | about three hundred dollars a month.
? c | How does she go shopping? | *By bike | By metro | On foot | She explains. | I cycle to the shops.
? t | She never uses a car now. | F | She rents one once or twice a year. | I rent a car once or twice a year.

## An ankle before the final | HS
Coach: How's your ankle?
Player: Better, thanks. I can walk without pain now.
Coach: Good, but don't play in Saturday's match. If you hurt it again, it could take months to heal.
Player: But it's the final!
Coach: I know. You can come and support the team, and start training again next week, slowly.
Player: OK. I'll do the exercises the physio gave me.
? c | How is the player's ankle now? | *Better; walking doesn't hurt | Still very painful | Completely healed | The player says so. | I can walk without pain now.
? c | Why shouldn't the player play on Saturday? | *A new injury could take months to heal | The team has enough players | The match is cancelled | The coach explains. | If you hurt it again, it could take months to heal.
? t | Saturday's match is the final. | T | The player says so. | But it's the final!
? c | When can the player start training again? | *Next week, slowly | Tomorrow | After two months | The coach says so. | start training again next week, slowly.

## A cheaper phone plan | TE
Agent: How can I help you today?
Customer: I'm paying too much for my phone plan. I hardly ever make calls, but I use a lot of data.
Agent: I see. Our data plan gives you thirty gigabytes and one hundred minutes of calls for fifteen dollars a month.
Customer: That's five dollars cheaper than what I pay now.
Agent: Yes, and you can keep your number.
Customer: Great. Can I change today?
Agent: Yes, it will start from the first of next month.
? c | What is the customer's problem? | *Paying too much for the plan | A bad signal | A broken phone | The customer explains. | I'm paying too much for my phone plan.
? c | How does the customer use the phone? | *Few calls but a lot of data | Many calls and little data | Only for messages | The customer explains. | I hardly ever make calls, but I use a lot of data.
? b | The new plan costs ____ dollars a month. | fifteen / 15 | The agent says so. | for fifteen dollars a month.
? t | The new plan starts today. | F | It starts next month. | it will start from the first of next month.

## Raising money for the library | ED
Principal: Good morning, everyone. Next Friday we're holding a fundraiser for the school library.
Principal: Each class will run a stall, selling food, books or games.
Principal: We hope to raise two thousand dollars to buy new books and computers.
Principal: Parents are welcome from three o'clock. Please bring small change, as the stalls can't accept cards.
? c | What is the money for? | *The school library | A school trip | Sports equipment | The principal explains. | a fundraiser for the school library.
? c | What will each class do? | *Run a stall | Perform a show | Wash cars | The principal explains. | Each class will run a stall
? b | They hope to raise two thousand ____. | dollars | The principal gives the goal. | We hope to raise two thousand dollars
? t | Visitors can pay by card. | F | The stalls can't accept cards. | the stalls can't accept cards.

## Dinner on Friday instead | CO
Lan: Sorry I missed your call. I was in a meeting.
Peter: No problem. I wanted to ask if you're free for dinner on Thursday.
Lan: Thursday is difficult. I have a work trip until Thursday night. How about Friday?
Peter: Friday's fine. There's a new Korean place near the river.
Lan: Sounds great. Shall we meet there at seven thirty?
Peter: Perfect. I'll book a table.
? c | Why did Lan miss the call? | *Lan was in a meeting | Lan's phone was off | Lan was asleep | Lan explains. | I was in a meeting.
? c | Why can't Lan meet on Thursday? | *Lan is on a work trip | Lan is ill | Lan has a class | Lan explains. | I have a work trip until Thursday night.
? c | What kind of restaurant will they go to? | *Korean | Italian | Vietnamese | Peter suggests it. | There's a new Korean place near the river.
? t | Lan will book the table. | F | Peter will book it. | I'll book a table.

## Ideas for Central Park | PT
Councillor: We're planning to improve Central Park next year, and we want your ideas.
Resident: The playground is very old. Some of the equipment is broken.
Councillor: Yes, a new playground is already in the plan. What else?
Resident: Better lights. Many people don't feel safe walking there after dark.
Councillor: That's a good point. We'll add it to the list. There's an online survey until the end of the month.
? c | Why does the councillor talk to residents? | *To collect ideas for the park | To close the park | To sell the land | The councillor explains. | we want your ideas.
? t | A new playground is already planned. | T | The councillor says so. | a new playground is already in the plan.
? c | Why does the resident want better lights? | *People don't feel safe after dark | To save energy | For sports at night | The resident explains. | Many people don't feel safe walking there after dark.
? c | How can people give more ideas? | *Through an online survey | At a meeting next year | By phone | The councillor explains. | There's an online survey until the end of the month.

## Five exams in two weeks | HE
Counsellor: You look worried, Nam. Is it the exams?
Nam: Yes. I have five exams in two weeks, and I can't sleep.
Counsellor: Have you made a study plan?
Nam: Not really. I just study whatever I feel like.
Counsellor: Try making a timetable with short breaks. And don't study late at night; your brain needs rest to remember things.
Nam: I'll try that. Thanks.
? b | Nam has ____ exams in two weeks. | five / 5 | Nam explains. | I have five exams in two weeks
? c | How does Nam study now? | *Without a plan | With a strict timetable | With a group | Nam explains. | I just study whatever I feel like.
? c | What does the counsellor suggest? | *A timetable with short breaks | Studying all night | Skipping one exam | The counsellor advises. | Try making a timetable with short breaks.
? t | The counsellor says studying late at night helps memory. | F | The brain needs rest to remember. | your brain needs rest to remember things.

## A second-hand bike | SH
Seller: So, you're interested in the bike?
Buyer: Yes. How old is it?
Seller: About three years, but I've only used it at weekends. The tyres are new.
Buyer: Why are you selling it?
Seller: I'm moving abroad next month, and I can't take it with me.
Buyer: Would you take eighty dollars?
Seller: Let's say ninety, and I'll give you the lock too.
Buyer: Deal.
? b | The bike is about ____ years old. | three / 3 | The seller says so. | About three years
? c | Why is the seller selling the bike? | *The seller is moving abroad | The seller is buying a car | It is too small | The seller explains. | I'm moving abroad next month
? c | What is the final price? | *Ninety dollars | Eighty dollars | A hundred dollars | They agree on it. | Let's say ninety
? t | The buyer gets the lock as well. | T | The seller includes it. | I'll give you the lock too.

## Weather for the lantern festival | NW
Presenter: Good news for the lantern festival this weekend.
Presenter: The rain we've had all week will stop by Friday evening.
Presenter: Saturday will be dry and warm, though it will become windy after midnight.
Presenter: So if you're planning to release a lantern on the river, do it early in the evening.
? c | What will happen to the rain? | *It will stop by Friday evening | It will continue all weekend | It will start on Saturday | The presenter says so. | The rain we've had all week will stop by Friday evening.
? c | What will Saturday be like? | *Dry and warm | Wet and cold | Windy all day | The presenter describes Saturday. | Saturday will be dry and warm
? t | It will become windy after midnight. | T | The presenter says so. | it will become windy after midnight.
? c | What does the presenter advise? | *Releasing lanterns early in the evening | Staying at home | Going on Sunday | The presenter gives advice. | do it early in the evening.

## Adopting Milo | AN
Volunteer: So you'd like to adopt Milo. He's two years old and very calm.
Woman: He's lovely. What do I need to know?
Volunteer: He's had all his vaccinations. He needs to stay indoors for the first two weeks while he gets used to your home.
Woman: I work during the day. Is that a problem?
Volunteer: Not for Milo. He sleeps most of the day. But give him some play time in the evening.
? b | Milo is ____ years old. | two / 2 | The volunteer says so. | He's two years old
? t | Milo has had his vaccinations. | T | The volunteer confirms it. | He's had all his vaccinations.
? c | Why should Milo stay indoors at first? | *To get used to his new home | Because he is ill | Because of the weather | The volunteer explains. | while he gets used to your home.
? c | What should the woman do in the evening? | *Play with him | Take him for a walk | Give him medicine | The volunteer advises. | give him some play time in the evening.

## A late electricity bill | MS
Caller: Hello, I've received a letter saying my electricity bill is late.
Agent: Let me check. Yes, the payment was due on the fifth, and it's now the twentieth.
Caller: I'm sorry. I changed banks and forgot to update my details.
Agent: I understand. If you pay today, there's no extra fee.
Caller: Great. Can I set up automatic payments too?
Agent: Yes, you can do that on our website in a few minutes.
? c | Why was the bill paid late? | *The caller changed banks | The caller had no money | The bill was wrong | The caller explains. | I changed banks and forgot to update my details.
? b | The payment was due on the ____. | fifth / 5th | The agent checks. | the payment was due on the fifth
? c | What happens if the caller pays today? | *There's no extra fee | The bill is cheaper | The account is closed | The agent explains. | If you pay today, there's no extra fee.
? t | Automatic payments can be set up on the website. | T | The agent says so. | you can do that on our website

## Grandma's first video call | TE
Grandson: OK, Grandma, press the green button to answer.
Grandma: This one? Oh, I can see you! But you're upside down.
Grandson: Just turn the phone around. That's it.
Grandma: Now I can't hear you.
Grandson: Your volume is off. Press the button on the side, the top one.
Grandma: Wonderful! Now I can call your aunt in Australia too.
? c | What does Grandma press to answer? | *The green button | The red button | The side button | The grandson explains. | press the green button to answer.
? c | What is the first problem? | *The picture is upside down | The screen is black | The call ends | Grandma says so. | But you're upside down.
? c | Why can't Grandma hear? | *The volume is off | The phone is broken | The internet is slow | The grandson explains. | Your volume is off.
? t | Grandma wants to call someone in Australia. | T | She plans to call the aunt. | Now I can call your aunt in Australia too.

## A noisy open office | WK
Thu: I can't concentrate. The open office is so noisy.
Kevin: Have you tried noise-cancelling headphones?
Thu: Yes, but I can't wear them all day; they hurt my ears.
Kevin: You could book one of the quiet rooms on the third floor. They're free in the mornings.
Thu: I didn't know we had quiet rooms!
Kevin: They're new. You book them on the company website.
? c | What is Thu's problem? | *The office is too noisy | Thu's computer is slow | Thu has too much work | Thu explains. | The open office is so noisy.
? c | Why doesn't Thu wear headphones all day? | *They hurt Thu's ears | They are expensive | They are not allowed | Thu explains. | they hurt my ears.
? b | The quiet rooms are on the ____ floor. | third / 3rd | Kevin says so. | the quiet rooms on the third floor.
? t | The quiet rooms are usually free in the afternoon. | N | Kevin only mentions the mornings. | They're free in the mornings.

## Three months in Nepal | TR
Interviewer: Tell us about your volunteer trip.
Hoa: I spent three months in a village in Nepal, teaching English at a primary school.
Interviewer: What was the hardest part?
Hoa: At first, the cold. We had no heating, and in winter it was below zero at night.
Interviewer: And the best part?
Hoa: The children. They were so keen to learn, even though some walked an hour to school.
? b | Hoa spent ____ months in Nepal. | three / 3 | Hoa says so. | I spent three months in a village in Nepal
? c | What did Hoa do there? | *Taught English at a primary school | Built houses | Worked in a hospital | Hoa explains. | teaching English at a primary school.
? c | What was the hardest part at first? | *The cold | The food | The language | Hoa explains. | At first, the cold.
? t | Some children walked an hour to school. | T | Hoa mentions it. | some walked an hour to school.

## The Young Chef final | FD
Host: Welcome to the final of the Young Chef competition!
Host: Our two finalists have ninety minutes to cook a three-course meal.
Host: They must use at least one ingredient from the mystery box, which today contains mangoes.
Host: The winner will receive a place on a six-month course at a top cooking school.
? b | The finalists have ____ minutes. | ninety / 90 | The host says so. | have ninety minutes to cook
? c | How many courses must they cook? | *Three | Two | Four | The host explains. | a three-course meal.
? c | What is in the mystery box today? | *Mangoes | Fish | Chocolate | The host reveals it. | which today contains mangoes.
? c | What does the winner get? | *A place on a six-month cooking course | A restaurant | A cash prize | The host explains. | a place on a six-month course at a top cooking school.

## The washing machine door | HF
Customer: My washing machine stopped in the middle of a wash, and now the door won't open.
Technician: Is there water inside?
Customer: Yes, the clothes are still wet.
Technician: Don't try to force the door. I can come on Wednesday morning.
Customer: Nothing sooner? I have a lot of washing.
Technician: I'm afraid not. Until then, you could use the launderette on the corner.
? c | What is the problem? | *The machine stopped and the door won't open | It is too noisy | It won't start | The customer explains. | now the door won't open.
? t | The technician says to force the door open. | F | He says not to. | Don't try to force the door.
? b | The technician can come on Wednesday ____. | morning | The technician says so. | I can come on Wednesday morning.
? c | What does the technician suggest until then? | *Using the launderette | Washing by hand | Buying a new machine | He suggests it. | you could use the launderette on the corner.

## New library hours | ED
Librarian: From next month, the library will open later on weekdays, until nine in the evening, because many students asked for more evening study time.
Librarian: To make this possible, we will close on Sundays.
Librarian: The computer room will also have new printers, and printing will be free for students.
? c | Why will the library open later? | *Students asked for more evening study time | It is cheaper | More staff have joined | The librarian explains. | because many students asked for more evening study time.
? b | On weekdays it will open until nine in the ____. | evening | The librarian gives the time. | until nine in the evening
? t | The library will now be open every day. | F | It will close on Sundays. | we will close on Sundays.
? c | What will be free for students? | *Printing | Coffee | Books to keep | The librarian says so. | printing will be free for students.

## Train or car to the coast? | TP
Anh: Should we drive to the coast or take the train?
Ben: The train takes four hours, but driving takes about three.
Anh: True, but we'd have to pay for petrol and tolls, and parking at the hotel isn't free.
Ben: And with the train, we can read or sleep.
Anh: Exactly. And the station is only ten minutes' walk from the beach.
Ben: OK, the train it is.
? c | Which is faster? | *Driving | The train | They take the same time | Ben compares them. | The train takes four hours, but driving takes about three.
? c | What is one cost of driving? | *Parking at the hotel | Expensive tickets | Taxi fares | Anh lists the costs. | parking at the hotel isn't free.
? b | The station is ____ minutes' walk from the beach. | ten / 10 | Anh says so. | only ten minutes' walk from the beach.
? t | They decide to drive. | F | They choose the train. | OK, the train it is.

## A book club at work | HS
Mai: I'm thinking of starting a book club at work.
Long: Nice idea. How would it work?
Mai: We'd read one book a month and meet at lunchtime on the last Friday to talk about it.
Long: Who chooses the book?
Mai: We'd take turns. Each person chooses once.
Long: Count me in. But please, nothing longer than three hundred pages!
? c | Where will the book club be? | *At work | At a library | At Mai's home | Mai says so. | starting a book club at work.
? c | When will they meet? | *At lunchtime on the last Friday of the month | Every Friday evening | On the first Monday | Mai explains. | meet at lunchtime on the last Friday
? c | How will they choose the books? | *They will take turns | Mai will choose | They will vote | Mai explains. | We'd take turns.
? t | Long wants to read very long books. | F | Long asks for nothing longer than three hundred pages. | nothing longer than three hundred pages!

## Less food in the bin | EN
Speaker: In many homes, about a third of the food we buy ends up in the bin.
Speaker: One simple solution is to plan meals for the week before you go shopping.
Speaker: Another is to understand dates. Best before means the food may be less fresh, not that it is unsafe.
Speaker: And leftovers can become tomorrow's lunch.
? c | How much bought food ends up in the bin in many homes? | *About a third | About half | About a tenth | The speaker gives the figure. | about a third of the food we buy ends up in the bin.
? c | What is one simple solution? | *Planning meals before shopping | Buying less fruit | Eating out more | The speaker explains. | plan meals for the week before you go shopping.
? t | Food past its best before date is always unsafe. | F | It may be less fresh, not unsafe. | not that it is unsafe.
? c | What can leftovers become? | *Tomorrow's lunch | Animal food | Compost only | The speaker suggests it. | leftovers can become tomorrow's lunch.

## Sorry I missed it | CO
Ha: I'm sorry I didn't come to your presentation yesterday.
Jun: I was a bit disappointed. I saved a seat for you.
Ha: I know. My boss asked me to stay late, and my phone battery died, so I couldn't even message you.
Jun: Ah, I see. How about coming to the next one? It's on Monday.
Ha: Definitely. And let me buy you a coffee to say sorry.
? c | What did Ha miss? | *Jun's presentation | Jun's birthday | A football match | Ha apologises. | I didn't come to your presentation yesterday.
? c | Why couldn't Ha send a message? | *Ha's phone battery died | Ha forgot | There was no signal | Ha explains. | my phone battery died
? b | The next presentation is on ____. | Monday | Jun says so. | It's on Monday.
? t | Ha offers to buy Jun a coffee. | T | Ha offers it as an apology. | let me buy you a coffee to say sorry.
"""

LESSONS["B2"] = """
## Should we move the office? | WK
Hana: The landlord wants to raise our rent by fifteen percent next year. I think it's time to consider moving.
Ken: Where to? Somewhere in the suburbs would be about forty percent cheaper, but half our staff would have a much longer commute.
Hana: That's my worry too. We could lose good people.
Ken: What if we took a smaller office in the centre and let people work from home two days a week? We'd only need desks for about sixty percent of staff at any time.
Hana: That could work. Let's run a quick survey before we decide anything.
? b | The landlord wants to raise the rent by ____ percent. | fifteen / 15 | Hana says so. | raise our rent by fifteen percent next year.
? c | What is the main problem with the suburbs? | *Many staff would have a longer commute | The offices are too small | The rent is higher | Ken explains. | half our staff would have a much longer commute.
? c | What does Ken propose? | *A smaller central office with two days at home | Moving everyone to the suburbs | Staying and paying more | Ken suggests it. | What if we took a smaller office in the centre and let people work from home two days a week?
? t | They decide to move immediately. | F | They want a survey first. | Let's run a quick survey before we decide anything.

## Giving away half of everything | DL
Host: Today's guest gave away half of her possessions last year. Why did you do it?
Guest: I was moving to a smaller flat and realised I'd been paying to store things I never used.
Host: Was it hard?
Guest: Books were the hardest. I kept only the ones I'd read twice. Clothes were surprisingly easy.
Host: Has it changed how you shop?
Guest: Completely. Before buying anything, I ask whether I'd carry it with me if I moved again. Usually the answer is no.
? c | What made the guest start? | *Moving to a smaller flat | Losing a job | A friend's advice | The guest explains. | I was moving to a smaller flat
? c | Which things were the hardest to give away? | *Books | Clothes | Furniture | The guest says so. | Books were the hardest.
? t | The guest found it easy to give away clothes. | T | Clothes were surprisingly easy. | Clothes were surprisingly easy.
? c | What question does the guest ask before buying? | *Whether she would carry it if she moved again | Whether it is on sale | Whether her friends have one | The guest explains. | I ask whether I'd carry it with me if I moved again.

## The bike lane debate | TP
Reporter: The city plans a new bike lane on Tran Phu Street, removing one lane of car parking.
Shop owner: My customers need to park. If they can't, they'll go to the shopping centre instead.
Cyclist: Studies in other cities show that people on bikes visit shops more often, even if they spend less each time.
Reporter: The council says it will add a car park two streets away and review the lane after six months.
? c | What will the plan remove? | *One lane of car parking | A bus stop | Two traffic lanes | The reporter explains. | removing one lane of car parking.
? c | What does the shop owner fear? | *Customers will shop elsewhere | Bikes will damage the street | The rent will rise | The owner explains. | they'll go to the shopping centre instead.
? c | What does the cyclist say about people on bikes? | *They visit shops more often | They spend more each time | They never shop locally | The cyclist mentions studies. | people on bikes visit shops more often, even if they spend less each time.
? b | The lane will be reviewed after ____ months. | six / 6 | The council promises a review. | review the lane after six months.

## Back to study at forty-two | ED
Interviewer: You started a degree at forty-two. What made you decide?
Mai: My job in a bank was disappearing as more services went online. I'd always wanted to study psychology, so it felt like the right moment.
Interviewer: How do you manage with a family?
Mai: I study early in the morning, before the children wake up, and my husband does the school run.
Interviewer: Any advice for others?
Mai: Don't wait for the perfect time. It doesn't exist.
? c | Why did Mai decide to study? | *Her bank job was disappearing | She was bored | Her children had left home | Mai explains. | My job in a bank was disappearing as more services went online.
? c | What is Mai studying? | *Psychology | Banking | Law | Mai says so. | I'd always wanted to study psychology
? c | When does Mai study? | *Early in the morning | Late at night | At weekends only | Mai explains. | I study early in the morning, before the children wake up
? t | Mai thinks people should wait for the right time. | F | She says the perfect time doesn't exist. | Don't wait for the perfect time.

## Working at night | HE
Presenter: Around one in five workers do shift work. Dr. Ha, what does it do to the body?
Dr. Ha: Our bodies follow a twenty-four-hour clock. Working at night confuses it, which affects sleep, digestion and even mood.
Presenter: Can people adapt?
Dr. Ha: Partly. Keeping the same sleep times on days off helps, as does a dark, quiet bedroom.
Presenter: And food?
Dr. Ha: Eat your main meal before the shift starts, and avoid heavy meals in the middle of the night.
? c | About how many workers do shift work? | *One in five | One in two | One in ten | The presenter says so. | Around one in five workers do shift work.
? c | What does night work confuse? | *The body's twenty-four-hour clock | Memory | Eyesight | Dr. Ha explains. | Our bodies follow a twenty-four-hour clock.
? c | What helps people adapt? | *Keeping the same sleep times on days off | Sleeping less | Drinking more coffee | Dr. Ha explains. | Keeping the same sleep times on days off helps
? t | Dr. Ha advises eating a big meal in the middle of the night. | F | Heavy meals should be avoided then. | avoid heavy meals in the middle of the night.

## A reef in trouble | EN
Guide: The reef you're about to see has lost almost half its coral in the last twenty years.
Guide: The main cause is warmer sea water, which turns the coral white. Coral can recover, but only if the water cools again quickly.
Guide: Sun cream with certain chemicals can also harm it, so please use the reef-safe cream we provide.
Guide: And remember, don't stand on or touch the coral. Even a gentle touch can damage it.
? c | How much coral has the reef lost? | *Almost half | About a tenth | All of it | The guide says so. | has lost almost half its coral in the last twenty years.
? c | What is the main cause? | *Warmer sea water | Fishing boats | Plastic | The guide explains. | The main cause is warmer sea water
? t | Coral can never recover after turning white. | F | It can recover if the water cools quickly. | Coral can recover, but only if the water cools again quickly.
? c | What does the guide provide? | *Reef-safe sun cream | Diving masks | Gloves | The guide says so. | please use the reef-safe cream we provide.

## Five minutes from the beach? | TR
Customer: The website said the hotel was five minutes from the beach. It was actually a twenty-minute walk along a busy road.
Agent: I'm sorry. Did you speak to our representative there?
Customer: Yes, on the second day. She offered to move us, but only to a more expensive hotel if we paid the difference.
Agent: I'll pass this to our customer relations team. Given the misleading description, I'd expect at least a partial refund.
Customer: I'd also like the website corrected, so it doesn't happen to anyone else.
? c | What was wrong with the hotel? | *It was much further from the beach | It was dirty | It was closed | The customer explains. | It was actually a twenty-minute walk along a busy road.
? c | What did the representative offer? | *A move if they paid the difference | A free upgrade | A full refund | The customer explains. | only to a more expensive hotel if we paid the difference.
? t | The agent expects some money to be returned. | T | The agent expects a partial refund. | I'd expect at least a partial refund.
? c | What else does the customer want? | *The website description corrected | A free holiday | A letter of apology | The customer asks for it. | I'd also like the website corrected

## Two job offers | WK
Linh: I've got two offers, and I can't decide.
Tom: What are they?
Linh: One is a big company with a higher salary, but the work sounds quite routine. The other is a small start-up. Less money, but I'd lead my own projects.
Tom: How secure is the start-up?
Linh: That's the problem. They have funding for about eighteen months.
Tom: Well, you're young. If it fails, you'll still have learned a lot. Big companies will still be there.
? c | What is the advantage of the big company? | *A higher salary | More interesting work | Leading projects | Linh explains. | a big company with a higher salary
? c | What is attractive about the start-up? | *Linh would lead her own projects | Higher pay | A shorter commute | Linh explains. | I'd lead my own projects.
? b | The start-up has funding for about ____ months. | eighteen / 18 | Linh explains. | They have funding for about eighteen months.
? t | Tom seems to favour the start-up. | T | He says she will learn a lot even if it fails. | If it fails, you'll still have learned a lot.

## Can you trust online reviews? | TE
Presenter: How much do you trust online reviews? Researchers estimate that a significant share of reviews on some sites are fake.
Expert: Watch for patterns. Many five-star reviews posted on the same day, very short, with no details, are a warning sign.
Presenter: What about bad reviews?
Expert: Read the three-star ones. They tend to be the most balanced and explain real strengths and weaknesses.
Presenter: Should sites do more?
Expert: Definitely. Some now only allow reviews from people who have actually bought the product.
? c | What is a warning sign? | *Many short five-star reviews on the same day | Long, detailed reviews | Reviews with photos | The expert explains. | Many five-star reviews posted on the same day, very short, with no details
? c | Which reviews does the expert recommend reading? | *Three-star reviews | Five-star reviews | One-star reviews | The expert says so. | Read the three-star ones.
? t | Three-star reviews are usually the most balanced. | T | The expert says so. | They tend to be the most balanced
? c | What have some sites started doing? | *Only allowing reviews from real buyers | Removing all reviews | Paying reviewers | The expert explains. | only allow reviews from people who have actually bought the product.

## A manager who asks everyone | WK
Ana: How's the new manager?
Ben: Different. The last one decided everything herself. This one asks for our opinions all the time.
Ana: Isn't that good?
Ben: Mostly. But sometimes we spend an hour discussing things that she could decide in five minutes.
Ana: Maybe she's trying to understand the team first.
Ben: That's probably true. She did say she'd make faster decisions after her first three months.
? c | How was the last manager different? | *She decided everything herself | She was rarely there | She asked for opinions | Ben explains. | The last one decided everything herself.
? c | What is Ben's complaint? | *Discussions take too long | The manager is unfriendly | There is too much work | Ben explains. | sometimes we spend an hour discussing things that she could decide in five minutes.
? t | The new manager plans to decide faster later. | T | She said so. | She did say she'd make faster decisions after her first three months.
? c | What does Ana suggest about the manager? | *She may be trying to understand the team | She is not confident | She wants to leave | Ana gives a reason. | Maybe she's trying to understand the team first.

## Food from a balcony | EN
Speaker: You don't need a garden to grow food. A sunny balcony can produce herbs, tomatoes and chillies.
Speaker: The key is light. Most vegetables need at least six hours of direct sunlight.
Speaker: Choose large pots, because small ones dry out quickly in summer.
Speaker: And start small. Many beginners plant too much at once, lose interest and give up.
? c | What can a balcony produce? | *Herbs, tomatoes and chillies | Rice and potatoes | Fruit trees | The speaker lists them. | A sunny balcony can produce herbs, tomatoes and chillies.
? b | Most vegetables need at least ____ hours of direct sunlight. | six / 6 | The speaker says so. | at least six hours of direct sunlight.
? c | Why choose large pots? | *Small ones dry out quickly | They are cheaper | They look better | The speaker explains. | small ones dry out quickly in summer.
? t | The speaker advises beginners to plant a lot at first. | F | The advice is to start small. | And start small.

## Renting or buying a home | MS
Son: I've saved enough for a deposit. Should I buy a flat?
Father: It depends. How long do you plan to stay in this city?
Son: Not sure. Maybe three or four years. My company might send me abroad.
Father: Then renting might be smarter. Buying and selling costs a lot in fees, and prices don't always rise in a few years.
Son: But rent feels like throwing money away.
Father: Not if it gives you freedom. Keep saving, and buy when you know where you want to settle.
? c | What has the son saved for? | *A deposit on a flat | A car | A trip abroad | The son says so. | I've saved enough for a deposit.
? c | Why is the son unsure about staying? | *His company might send him abroad | He dislikes the city | His job is ending | The son explains. | My company might send me abroad.
? c | Why does the father suggest renting? | *Buying and selling cost a lot in fees | Rent is very cheap | Flats are hard to find | The father explains. | Buying and selling costs a lot in fees
? t | The father tells his son never to buy. | F | He says to buy when he knows where to settle. | buy when you know where you want to settle.

## The noise of the city | PT
Researcher: We measured noise in twelve neighbourhoods for a month. In the busiest streets, the average level at night was over sixty decibels.
Interviewer: Is that harmful?
Researcher: Over long periods, yes. Night-time noise is linked to poor sleep, stress and even heart problems.
Interviewer: What can cities do?
Researcher: Quieter road surfaces, lower speed limits at night and more trees all help. Trees don't block much sound, but people feel calmer when they can see them.
? b | The researchers measured noise in ____ neighbourhoods. | twelve / 12 | The researcher says so. | We measured noise in twelve neighbourhoods
? c | What is night-time noise linked to? | *Poor sleep, stress and heart problems | Better concentration | Lower crime | The researcher explains. | Night-time noise is linked to poor sleep, stress and even heart problems.
? t | Trees block most traffic noise. | F | Trees don't block much sound. | Trees don't block much sound
? c | Why do trees still help? | *People feel calmer when they see them | They make the air colder | They stop cars driving fast | The researcher explains. | people feel calmer when they can see them.

## Learning by teaching | ED
Teacher: One of the best ways to learn something is to explain it to someone else.
Teacher: When you prepare to teach, you organise your knowledge and notice the gaps.
Teacher: In our class, each of you will teach a ten-minute lesson on a grammar point.
Teacher: You'll be marked on how clearly you explain, not on how perfect your English is.
? c | According to the teacher, what is one of the best ways to learn? | *Explaining it to someone else | Reading it many times | Taking tests | The teacher says so. | One of the best ways to learn something is to explain it to someone else.
? c | What happens when you prepare to teach? | *You organise your knowledge and notice gaps | You forget less | You need more books | The teacher explains. | you organise your knowledge and notice the gaps.
? b | Each student will teach a ____-minute lesson. | ten / 10 | The teacher explains. | a ten-minute lesson on a grammar point.
? t | Students will be marked mainly on perfect English. | F | They are marked on clarity. | not on how perfect your English is.

## Delivery riders | WK
Reporter: Food delivery riders say their pay has fallen this year. Minh has been riding for three years.
Minh: When I started, we earned a fixed amount per order. Now the app changes the price depending on demand, and on quiet days we earn much less.
Reporter: Do you have any protection if you're injured?
Minh: Not really. We're not employees, so there's no sick pay. Some riders have started a group to ask the companies for basic insurance.
? b | Minh has been riding for ____ years. | three / 3 | The reporter says so. | Minh has been riding for three years.
? c | How has pay changed? | *The price per order now changes with demand | It is now a fixed amount | It has doubled | Minh explains. | Now the app changes the price depending on demand
? t | Riders get sick pay. | F | They are not employees. | there's no sick pay.
? c | What are some riders asking for? | *Basic insurance | Faster bikes | Shorter routes | Minh explains. | to ask the companies for basic insurance.

## A hospital volunteer | HE
Interviewer: What do volunteers do at the hospital?
Volunteer: We don't do anything medical. We talk to patients who don't get visitors, help them write messages and guide families around the building.
Interviewer: Why is talking so important?
Volunteer: Long stays can be very lonely, especially for older patients. Nurses are too busy to sit and chat for long.
Interviewer: What do you get from it?
Volunteer: Perspective. My own problems seem much smaller after a morning there.
? c | What don't volunteers do? | *Anything medical | Talk to patients | Guide families | The volunteer says so. | We don't do anything medical.
? c | Why is talking important? | *Long stays can be lonely | Patients need to practise speaking | Doctors ask them to | The volunteer explains. | Long stays can be very lonely, especially for older patients.
? t | Nurses have plenty of time to chat. | F | Nurses are too busy. | Nurses are too busy to sit and chat for long.
? c | What does the volunteer gain? | *Perspective on their own problems | Money | Medical training | The volunteer explains. | My own problems seem much smaller after a morning there.

## The four-day festival | HS
Organiser: This year the music festival runs for four days instead of three, with over eighty bands.
Organiser: To reduce waste, we've banned single-use plastic cups. Every visitor gets a reusable cup with their ticket.
Organiser: Public transport is the best way to get here. There are extra night buses until three in the morning.
Organiser: And for families, Sunday is a quieter day with workshops for children.
? b | There will be over ____ bands. | eighty / 80 | The organiser says so. | with over eighty bands.
? c | What has the festival banned? | *Single-use plastic cups | Food stalls | Cameras | The organiser explains. | we've banned single-use plastic cups.
? c | Until when do the extra night buses run? | *Three in the morning | Midnight | One in the morning | The organiser explains. | extra night buses until three in the morning.
? t | Sunday is planned with families in mind. | T | It has workshops for children. | Sunday is a quieter day with workshops for children.

## Second-hand clothes online | SH
Lan: I've started selling my old clothes online. I made two hundred dollars last month.
Kim: Really? Is it a lot of work?
Lan: Taking good photos takes time. Clothes in natural light sell much faster.
Kim: What sells best?
Lan: Brand-name jackets and anything in very good condition. Cheap fast fashion hardly sells at all.
Kim: Maybe I should buy fewer cheap clothes in the first place.
? b | Lan made two hundred ____ last month. | dollars | Lan says so. | I made two hundred dollars last month.
? c | What helps clothes sell faster? | *Photos in natural light | Lower prices | Long descriptions | Lan explains. | Clothes in natural light sell much faster.
? c | What hardly sells? | *Cheap fast fashion | Brand-name jackets | Clothes in good condition | Lan explains. | Cheap fast fashion hardly sells at all.
? t | Kim draws a lesson about buying cheap clothes. | T | Kim decides to buy fewer. | Maybe I should buy fewer cheap clothes in the first place.

## A plan to reduce screen time | TE
Mother: I'm worried. You were on your phone for six hours yesterday.
Son: Most of it was homework and chatting with friends.
Mother: Some of it, maybe. How about a rule: no phones at meals and none after ten at night?
Son: After ten is fine, but I need my phone for the group project this week.
Mother: OK, the meal rule starts today, and the ten o'clock rule starts after your project.
Son: Deal.
? b | The son was on his phone for ____ hours yesterday. | six / 6 | The mother says so. | You were on your phone for six hours yesterday.
? c | What does the son say he was doing? | *Homework and chatting with friends | Playing games | Watching films | The son explains. | Most of it was homework and chatting with friends.
? c | Which rule starts today? | *No phones at meals | No phones after ten | No phones at weekends | They agree on it. | the meal rule starts today
? t | The ten o'clock rule starts immediately. | F | It starts after the project. | the ten o'clock rule starts after your project.

## A lecture on bees | AN
Lecturer: Bees pollinate about a third of the crops we eat, from apples to almonds.
Lecturer: In many countries, bee numbers have fallen sharply. The main causes are pesticides, disease and the loss of wild flowers.
Lecturer: Some farmers now leave strips of wild flowers along their fields, which gives bees food and shelter.
Lecturer: Even in cities, a window box of flowers can make a difference.
? c | How much of our food crops do bees pollinate? | *About a third | About half | Almost all | The lecturer says so. | Bees pollinate about a third of the crops we eat
? c | Which is NOT given as a cause of falling numbers? | *Cold winters | Pesticides | Loss of wild flowers | The lecturer lists pesticides, disease and wild flowers. | The main causes are pesticides, disease and the loss of wild flowers.
? c | What are some farmers doing? | *Leaving strips of wild flowers | Using more pesticides | Keeping bees indoors | The lecturer explains. | Some farmers now leave strips of wild flowers along their fields
? t | City residents cannot help bees. | F | A window box can make a difference. | a window box of flowers can make a difference.

## A difficult customer | CO
Trainer: Today we're practising difficult phone calls. What's the first thing to do when a customer is angry?
Trainee: Explain the company's rules?
Trainer: Not yet. First, let them finish. People calm down faster when they feel heard.
Trainee: And then?
Trainer: Repeat the problem in your own words, so they know you've understood. Only then offer a solution.
Trainee: What if I can't solve it?
Trainer: Be honest, explain what you can do, and give a time when you'll call back.
? c | What should you do first with an angry customer? | *Let them finish | Explain the rules | Transfer the call | The trainer explains. | First, let them finish.
? c | Why repeat the problem in your own words? | *So the customer knows you understood | To save time | To end the call | The trainer explains. | so they know you've understood.
? t | You should offer a solution before repeating the problem. | F | A solution comes after repeating the problem. | Only then offer a solution.
? c | What should you do if you can't solve it? | *Be honest and give a time to call back | Promise a refund | Ask them to call again | The trainer advises. | Be honest, explain what you can do, and give a time when you'll call back.

## A smart city sensor project | TE
Engineer: We've installed sensors in five hundred parking spaces downtown.
Engineer: Drivers can see free spaces on an app, so they spend less time driving around looking for one.
Engineer: In the first three months, the time spent searching fell by about a quarter.
Engineer: The next step is to adjust parking prices automatically, making busy streets more expensive at peak times.
? b | Sensors were installed in five hundred ____ spaces. | parking | The engineer explains. | sensors in five hundred parking spaces downtown.
? c | What can drivers see on the app? | *Free parking spaces | Traffic accidents | Bus times | The engineer explains. | Drivers can see free spaces on an app
? c | By how much did search time fall? | *About a quarter | About half | About a tenth | The engineer gives the result. | the time spent searching fell by about a quarter.
? t | Prices will be higher on busy streets at peak times. | T | That is the next step. | making busy streets more expensive at peak times.

## Saying no at work | WK
Coach: You said you're overloaded. Do you often say yes to extra tasks?
Client: Almost always. I don't want people to think I'm lazy.
Coach: Saying yes to everything means doing some things badly. Try this: when someone asks, say you'll check your priorities and reply later.
Client: That sounds less rude than a direct no.
Coach: Exactly. And when you do refuse, suggest an alternative, like a later deadline or someone else who could help.
? c | Why does the client accept extra tasks? | *They don't want to seem lazy | They need more money | Their manager insists | The client explains. | I don't want people to think I'm lazy.
? c | What does the coach suggest saying first? | *That you'll check your priorities and reply later | A direct no | Yes, then complain later | The coach advises. | say you'll check your priorities and reply later.
? t | The client thinks the suggestion sounds rude. | F | The client finds it less rude than a direct no. | That sounds less rude than a direct no.
? c | What should you do when you refuse? | *Suggest an alternative | Apologise many times | Explain your salary | The coach advises. | suggest an alternative

## Plastic in the ocean | EN
Presenter: Every year, millions of tonnes of plastic enter the ocean. Where does most of it come from?
Scientist: Mostly from land, through rivers. A relatively small number of rivers carry a large share of it.
Presenter: So cleaning up rivers could make a big difference?
Scientist: Yes. Barriers that catch rubbish in rivers are cheaper than collecting plastic at sea, where it breaks into tiny pieces.
Presenter: And what can individuals do?
Scientist: Use less single-use plastic, and support better waste collection in countries where it's lacking.
? c | Where does most ocean plastic come from? | *From land, through rivers | From ships | From fishing nets | The scientist explains. | Mostly from land, through rivers.
? c | Why are river barriers useful? | *They are cheaper than collecting plastic at sea | They make electricity | They stop floods | The scientist explains. | Barriers that catch rubbish in rivers are cheaper than collecting plastic at sea
? t | Plastic at sea breaks into tiny pieces. | T | The scientist says so. | where it breaks into tiny pieces.
? c | What can individuals do? | *Use less single-use plastic | Stop eating fish | Clean beaches every day | The scientist advises. | Use less single-use plastic

## The language exchange | ED
Mai: I've been meeting a British student every Thursday for a language exchange.
Tom: How does it work?
Mai: We speak English for half an hour, then Vietnamese for half an hour. We correct each other's mistakes.
Tom: Is it better than classes?
Mai: It's different. Classes give me structure, but the exchange teaches me how people really talk, with slang and jokes.
Tom: I might try it. Where did you find your partner?
Mai: Through the university's international office.
? c | How often does Mai meet her partner? | *Every Thursday | Every day | Once a month | Mai says so. | every Thursday for a language exchange.
? c | How is the time divided? | *Half an hour in each language | An hour of English only | Mostly Vietnamese | Mai explains. | We speak English for half an hour, then Vietnamese for half an hour.
? c | What does the exchange teach that classes don't? | *How people really talk | Grammar rules | Exam skills | Mai explains. | the exchange teaches me how people really talk, with slang and jokes.
? b | Mai found her partner through the university's international ____. | office | Mai says so. | Through the university's international office.

## The food truck business | FD
Interviewer: Why did you choose a food truck rather than a restaurant?
Owner: The start-up cost was about a tenth of a restaurant's. And if one area is quiet, I can simply drive somewhere else.
Interviewer: What are the difficulties?
Owner: Permits. Each district has different rules about where trucks can park. And in the rainy season, customers disappear.
Interviewer: What's your plan?
Owner: To use the truck to test my menu. If it's popular after two years, I'll open a small restaurant.
? c | What was cheaper about a food truck? | *The start-up cost | The ingredients | The staff | The owner explains. | The start-up cost was about a tenth of a restaurant's.
? c | What is one advantage of a truck? | *The owner can move if an area is quiet | It never needs permits | It can seat many people | The owner explains. | I can simply drive somewhere else.
? t | All districts have the same parking rules. | F | Each district has different rules. | Each district has different rules about where trucks can park.
? c | What is the owner's long-term plan? | *To open a small restaurant | To buy more trucks | To sell the business | The owner explains. | I'll open a small restaurant.

## Commuting by ferry | TP
Reporter: For many people on the islands, the ferry is the only way to the city. But the service has been unreliable.
Commuter: Last month it was cancelled five times because of engine problems. I was late for work every time.
Reporter: The company says a new boat will arrive in March.
Commuter: They said that last year too. What we need is a second boat, so there's a backup when one breaks down.
? c | Why is the ferry important for islanders? | *It is the only way to the city | It is cheap | It is fast | The reporter explains. | the ferry is the only way to the city.
? b | Last month the ferry was cancelled ____ times. | five / 5 | The commuter says so. | it was cancelled five times because of engine problems.
? c | What does the company promise? | *A new boat in March | Lower prices | More trips | The reporter explains. | a new boat will arrive in March.
? t | The commuter trusts the company's promise. | F | The commuter says they promised the same last year. | They said that last year too.

## A grandparent's story | PF
Granddaughter: Grandpa, what was school like when you were young?
Grandfather: We walked five kilometres each way, and there were sixty of us in one classroom.
Granddaughter: Sixty! How did the teacher manage?
Grandfather: The older children helped the younger ones. That's how I first learned to teach.
Granddaughter: Is that why you became a teacher?
Grandfather: Partly. I liked seeing someone suddenly understand. That feeling never gets old.
? b | Grandpa walked ____ kilometres each way. | five / 5 | He says so. | We walked five kilometres each way
? c | How many children were in one classroom? | *Sixty | Twenty | Forty | He says so. | there were sixty of us in one classroom.
? c | How did the teacher manage? | *Older children helped the younger ones | There were two teachers | Children studied alone | Grandpa explains. | The older children helped the younger ones.
? t | Grandpa enjoyed seeing people understand. | T | He says that feeling never gets old. | I liked seeing someone suddenly understand.

## A talk about time management | WK
Speaker: Most people overestimate what they can do in a day and underestimate what they can do in a year.
Speaker: Try writing just three important tasks each morning, not twenty. Finish those before checking email.
Speaker: Email is useful, but it's someone else's list of priorities. If you start the day with it, you spend the morning reacting.
Speaker: Finally, plan breaks. Your brain needs them to stay focused.
? c | What do people underestimate? | *What they can do in a year | What they can do in a day | How long email takes | The speaker says so. | underestimate what they can do in a year.
? b | Write just ____ important tasks each morning. | three / 3 | The speaker advises. | Try writing just three important tasks each morning
? c | Why shouldn't you start the day with email? | *It is someone else's list of priorities | It is too slow | It is not important | The speaker explains. | it's someone else's list of priorities.
? t | The speaker says breaks waste time. | F | Breaks help you stay focused. | Your brain needs them to stay focused.

## Booking accommodation for a conference | TR
Organiser: About a hundred guests are coming to the conference. Have you found hotels?
Assistant: The hotel next to the venue only has forty rooms left.
Organiser: Can we negotiate a group price?
Assistant: I asked. They'll give us fifteen percent off if we book all forty by Friday.
Organiser: Do it. And for the others?
Assistant: There's a cheaper hotel ten minutes away by shuttle bus. I'll check whether they can run a shuttle in the mornings.
? b | About a ____ guests are coming. | hundred / 100 | The organiser says so. | About a hundred guests are coming to the conference.
? c | How many rooms are left at the hotel next to the venue? | *Forty | Fifteen | A hundred | The assistant explains. | only has forty rooms left.
? c | What is the condition for the discount? | *Booking all forty rooms by Friday | Paying in cash | Staying a week | The assistant explains. | if we book all forty by Friday.
? t | The second hotel is next to the venue. | F | It's ten minutes away by shuttle. | There's a cheaper hotel ten minutes away by shuttle bus.

## Why we procrastinate | HE
Psychologist: People often think procrastination is about laziness. Usually, it's about emotion.
Psychologist: We delay tasks that make us feel anxious, bored or unsure, and do something that feels better right now.
Psychologist: One technique is to make the first step tiny. Instead of "write the report", try "open the document and write one sentence".
Psychologist: Once we start, the task usually feels less unpleasant than we expected.
? c | According to the psychologist, procrastination is usually about | *Emotion | Laziness | Lack of time | The psychologist explains. | Usually, it's about emotion.
? c | Which tasks do we delay? | *Tasks that make us feel anxious, bored or unsure | Easy tasks | Tasks for other people | The psychologist explains. | We delay tasks that make us feel anxious, bored or unsure
? c | What technique is suggested? | *Making the first step tiny | Working all night | Asking someone else to do it | The psychologist explains. | One technique is to make the first step tiny.
? t | Tasks usually feel worse once we start them. | F | They feel less unpleasant than expected. | the task usually feels less unpleasant than we expected.

## Moving to a new country | PF
Interviewer: What surprised you most when you moved to Canada?
Thanh: The weather, of course. But also how direct people are at work. If they disagree, they say so in the meeting.
Interviewer: Was that difficult?
Thanh: At first I felt it was rude. Then I realised it saves time, and nobody takes it personally.
Interviewer: What do you miss?
Thanh: Street food, and the noise. My neighbourhood here is so quiet that I sometimes can't sleep.
? c | What surprised Thanh at work? | *How directly people disagree | How long meetings are | How much people earn | Thanh explains. | how direct people are at work.
? c | How did Thanh first feel about it? | *It seemed rude | It seemed funny | It seemed normal | Thanh explains. | At first I felt it was rude.
? t | Thanh now sees an advantage in it. | T | It saves time. | Then I realised it saves time
? c | Why can Thanh sometimes not sleep? | *The neighbourhood is too quiet | The weather is too cold | The neighbours are noisy | Thanh explains. | My neighbourhood here is so quiet that I sometimes can't sleep.

## The library of things | PT
Presenter: A new kind of library has opened in the city centre. You can't borrow books there, but you can borrow a drill, a tent or a sewing machine.
Manager: Most people use a drill for only a few minutes in its whole life. It makes more sense to share one.
Presenter: How much does it cost?
Manager: Membership is ten dollars a year, plus a small fee for each item. Volunteers check and repair everything when it comes back.
? c | What can you borrow at the new library? | *Tools and equipment | Books | Films | The presenter explains. | you can borrow a drill, a tent or a sewing machine.
? c | Why does sharing a drill make sense? | *Most people use one for only a few minutes | Drills are dangerous | Drills are very heavy | The manager explains. | Most people use a drill for only a few minutes in its whole life.
? b | Membership is ten dollars a ____. | year | The manager explains. | Membership is ten dollars a year
? t | Items are checked when they are returned. | T | Volunteers check and repair them. | Volunteers check and repair everything when it comes back.

## A cancelled concert | HS
Fan: I bought tickets for the concert on Saturday, and I've just seen it's cancelled. What happens now?
Agent: The band has postponed the show to the twelfth of next month. Your tickets are still valid for the new date.
Fan: I can't go on that date. I'll be abroad.
Agent: In that case, you can request a full refund within thirty days. Just use the link in the email we sent.
Fan: Will I get the booking fee back too?
Agent: Yes, the full amount, including fees.
? c | What has happened to the concert? | *It has been moved to a later date | It has been cancelled for ever | It has moved to a new city | The agent explains. | The band has postponed the show to the twelfth of next month.
? c | Why can't the fan go on the new date? | *The fan will be abroad | The fan has to work | The fan is ill | The fan explains. | I'll be abroad.
? b | Refunds must be requested within ____ days. | thirty / 30 | The agent explains. | request a full refund within thirty days.
? t | The booking fee will not be refunded. | F | The full amount is refunded. | Yes, the full amount, including fees.

## Electric scooters in the city | TP
Reporter: Since rental scooters arrived last year, they've become hugely popular with young commuters.
Resident: They're useful, but people leave them in the middle of the pavement. My mother uses a wheelchair, and she can't get past.
Reporter: The scooter company says it will introduce parking zones, and riders who park badly will be fined.
Resident: That would help, as long as it's actually enforced.
? c | Who mainly uses the scooters? | *Young commuters | Tourists | Delivery riders | The reporter explains. | they've become hugely popular with young commuters.
? c | What problem does the resident describe? | *Scooters left in the middle of the pavement | Scooters going too fast | Scooters being too expensive | The resident explains. | people leave them in the middle of the pavement.
? c | What will the company introduce? | *Parking zones and fines | Lower prices | Speed limits | The reporter explains. | it will introduce parking zones
? t | The resident doubts the rules will be enforced. | T | The resident adds a condition. | as long as it's actually enforced.

## A science fair project | ED
Judge: Tell me about your project.
Student: I tested whether plants grow better with music. I grew three groups of beans: one with music, one with silence and one with traffic noise.
Judge: And the results?
Student: The music group grew slightly taller, but the difference was very small.
Judge: Would you trust that result?
Student: Not completely. I only had ten plants in each group. I'd need a bigger experiment to be sure.
? c | What did the student test? | *Whether plants grow better with music | Which soil is best | How much water plants need | The student explains. | I tested whether plants grow better with music.
? b | There were ____ groups of beans. | three / 3 | The student explains. | I grew three groups of beans
? c | What were the results? | *The music group grew slightly taller | The silent group grew most | All groups died | The student explains. | The music group grew slightly taller
? t | The student is completely sure of the result. | F | A bigger experiment is needed. | Not completely.

## Pets and wellbeing | AN
Presenter: Many people say their pets make them happier. Is there evidence?
Researcher: Some. Dog owners, for example, tend to walk more and meet more neighbours, which is good for health and mood.
Presenter: And cats?
Researcher: Cat owners report feeling calmer, though it's hard to prove the cat is the cause. Calmer people may simply be more likely to choose cats.
Presenter: Any downsides?
Researcher: Pets are a long commitment. Animal shelters see many pets returned when owners realise how much time they need.
? c | Why may dogs improve health? | *Owners walk more and meet neighbours | Dogs prevent illness | Dogs reduce noise | The researcher explains. | Dog owners, for example, tend to walk more and meet more neighbours
? t | It is proven that cats make people calmer. | F | It's hard to prove the cat is the cause. | it's hard to prove the cat is the cause.
? c | What alternative explanation is given? | *Calmer people may choose cats | Cats are quieter than dogs | Cat owners sleep more | The researcher explains. | Calmer people may simply be more likely to choose cats.
? c | What problem do shelters see? | *Many pets are returned | Too few pets | Pets get ill | The researcher explains. | Animal shelters see many pets returned

## The open-plan kitchen | HF
Designer: More families want open-plan kitchens, where cooking, eating and living all happen in one space.
Client: I like the idea, but won't the whole house smell of cooking?
Designer: A good extractor fan solves most of that. The bigger issue is noise. If someone's watching TV while you're cooking, it can be annoying.
Client: So what do you suggest?
Designer: A sliding glass door. You can open the space when you want to be together and close it when you need quiet.
? c | What is an open-plan kitchen? | *Cooking, eating and living in one space | A kitchen with no walls outside | A kitchen in the garden | The designer explains. | where cooking, eating and living all happen in one space.
? c | What solves the smell problem? | *A good extractor fan | Opening windows | Cooking less | The designer explains. | A good extractor fan solves most of that.
? c | What does the designer see as the bigger issue? | *Noise | Cost | Light | The designer explains. | The bigger issue is noise.
? b | The designer suggests a sliding glass ____. | door | The designer suggests it. | A sliding glass door.

## Volunteering after retirement | PF
Interviewer: You retired two years ago. How do you spend your time?
Mr. Binh: I teach maths to children whose parents can't afford tutors, three afternoons a week.
Interviewer: Why maths?
Mr. Binh: I was an engineer for forty years. Maths was the tool I used every day, and I think it's often taught in a way that frightens children.
Interviewer: Has it been rewarding?
Mr. Binh: Very. One of my students was failing last year. This term she came top of her class.
? c | Who does Mr. Binh teach? | *Children whose parents can't afford tutors | University students | Retired people | He explains. | I teach maths to children whose parents can't afford tutors
? b | Mr. Binh was an engineer for ____ years. | forty / 40 | He says so. | I was an engineer for forty years.
? c | What does he think about how maths is often taught? | *It often frightens children | It is too easy | It is too slow | He explains. | it's often taught in a way that frightens children.
? t | One of his students has improved a great deal. | T | She came top of her class. | This term she came top of her class.

## The cost of convenience | MS
Speaker: Convenience has a price that we rarely notice.
Speaker: A coffee bought every workday costs more than a thousand dollars a year in some cities.
Speaker: Subscriptions are similar. Streaming services, apps and memberships are each small, but together they can be surprisingly large.
Speaker: Once a year, list every subscription you pay for and cancel the ones you haven't used in the last month.
? c | What is the speaker's main point? | *Convenience has a hidden cost | Coffee is unhealthy | Apps are useless | The speaker starts with it. | Convenience has a price that we rarely notice.
? c | How much can a daily coffee cost in a year? | *More than a thousand dollars | About a hundred dollars | Exactly five hundred dollars | The speaker gives the figure. | costs more than a thousand dollars a year in some cities.
? t | Subscriptions are always expensive one by one. | F | Each is small, but together they add up. | each small, but together they can be surprisingly large.
? c | What does the speaker advise doing once a year? | *Listing subscriptions and cancelling unused ones | Buying a coffee machine | Changing banks | The speaker advises. | list every subscription you pay for and cancel the ones you haven't used in the last month.

## An accessible website | TE
Manager: We've had complaints that our website is hard to use for people with poor eyesight.
Developer: That's true. Some of the text is very small, and the colours don't have enough contrast.
Manager: How long would it take to fix?
Developer: The colours and text size, about a week. Making every form work with screen readers will take longer, maybe a month.
Manager: Let's start with the quick changes and plan the rest for next month.
? c | Who finds the website hard to use? | *People with poor eyesight | Older computers | Foreign visitors | The manager explains. | hard to use for people with poor eyesight.
? c | What are two problems? | *Small text and weak colour contrast | Slow pages and broken links | Too many photos | The developer explains. | Some of the text is very small, and the colours don't have enough contrast.
? b | Fixing the colours and text size will take about a ____. | week | The developer estimates it. | The colours and text size, about a week.
? t | They will fix everything this week. | F | Forms will be done next month. | plan the rest for next month.

## A rainy-season warning | NW
Officer: Heavy rain is expected over the next three days, with a risk of flooding in low-lying areas.
Officer: Residents near the river should move valuable items upstairs and keep their phones charged.
Officer: Do not try to drive through flooded roads. Even thirty centimetres of moving water can sweep a car away.
Officer: Emergency shelters will open at local schools if needed.
? b | Heavy rain is expected over the next ____ days. | three / 3 | The officer says so. | over the next three days
? c | What should residents near the river do? | *Move valuable items upstairs | Leave their homes at once | Buy sandbags | The officer advises. | Residents near the river should move valuable items upstairs
? c | Why shouldn't people drive through flooded roads? | *Moving water can sweep a car away | Cars break down | Police will fine them | The officer explains. | Even thirty centimetres of moving water can sweep a car away.
? c | Where will emergency shelters open? | *At local schools | At hospitals | At the stadium | The officer explains. | Emergency shelters will open at local schools if needed.

## A team-building day | WK
Hoa: HR wants us to do a team-building day. They've suggested rock climbing.
Peter: Climbing? Half the team is scared of heights.
Hoa: I said the same. I suggested a cooking class instead, where we prepare a meal together.
Peter: Much better. Everyone can take part, and we get lunch at the end.
Hoa: HR agreed, as long as it costs less than fifty dollars per person.
? c | What did HR suggest first? | *Rock climbing | A cooking class | A boat trip | Hoa says so. | They've suggested rock climbing.
? c | What is the problem with the first idea? | *Many people are afraid of heights | It is too expensive | It is too far | Peter explains. | Half the team is scared of heights.
? t | Hoa suggested a cooking class. | T | Hoa says so. | I suggested a cooking class instead
? b | It must cost less than fifty dollars per ____. | person | Hoa explains the condition. | less than fifty dollars per person.

## Teaching children about money | MS
Parent: Our son is eight. When should we start giving him pocket money?
Advisor: Around now is good. The amount matters less than the habit.
Parent: Should we tell him what to buy?
Advisor: Let him choose, even if he wastes it sometimes. A small mistake at eight is cheaper than a big one at twenty-five.
Parent: What about saving?
Advisor: Try three jars: one for spending, one for saving and one for giving to others.
? b | The son is ____ years old. | eight / 8 | The parent says so. | Our son is eight.
? c | What matters more than the amount? | *The habit | The day it is given | The coins used | The advisor explains. | The amount matters less than the habit.
? c | Why let children make mistakes with money? | *Small mistakes now are cheaper than big ones later | Children never waste money | Parents can save more | The advisor explains. | A small mistake at eight is cheaper than a big one at twenty-five.
? c | What are the three jars for? | *Spending, saving and giving | Coins, notes and cards | Food, toys and books | The advisor explains. | one for spending, one for saving and one for giving to others.

## The value of a walk | HE
Speaker: If you feel stuck on a problem, go for a walk.
Speaker: Studies suggest that walking helps people produce more creative ideas, both during the walk and shortly afterwards.
Speaker: It doesn't need to be long. Even fifteen minutes can help.
Speaker: Leave your phone in your pocket, though. The benefit seems to come from letting the mind wander.
? c | What does the speaker recommend when you're stuck? | *Going for a walk | Working longer | Asking a friend | The speaker says so. | If you feel stuck on a problem, go for a walk.
? c | What does walking help with? | *Producing more creative ideas | Remembering names | Sleeping longer | The speaker explains. | walking helps people produce more creative ideas
? b | Even ____ minutes can help. | fifteen / 15 | The speaker says so. | Even fifteen minutes can help.
? t | The speaker suggests checking your phone while walking. | F | Leave it in your pocket. | Leave your phone in your pocket, though.

## A complaint about a course | ED
Student: I'm writing to complain about the online course I paid for. Half of the videos don't play, and nobody answers my emails.
Support: I'm very sorry. When did you first report the problem?
Student: Two weeks ago, and again last week.
Support: That's unacceptable. I've fixed your access, and I'll extend your course by a month for free.
Student: Thank you. Will I get a reply faster next time?
Support: Yes, I've added a direct contact for you.
? c | What is wrong with the course? | *Half the videos don't play and emails get no answer | The course is too difficult | The course is too expensive | The student explains. | Half of the videos don't play, and nobody answers my emails.
? c | When did the student first report it? | *Two weeks ago | Yesterday | Last month | The student explains. | Two weeks ago, and again last week.
? c | How does support make up for it? | *A free one-month extension | A full refund | A new course | Support explains. | I'll extend your course by a month for free.
? t | The student will now have a direct contact. | T | Support adds one. | I've added a direct contact for you.
"""

LESSONS["C1"] = """
## A basic income trial | MS
Host: A two-year trial gave a thousand residents a monthly payment with no conditions. Professor Lam, what happened?
Professor Lam: Contrary to what critics predicted, employment barely changed. A few people worked slightly less, mostly parents of young children and students who returned to education.
Host: So it didn't make people lazy?
Professor Lam: Not in any measurable way. What did change was wellbeing. Participants reported less stress and visited doctors less often.
Host: Then why not introduce it everywhere?
Professor Lam: Cost, mainly. A trial with a thousand people tells us little about how a whole economy would respond.
? b | The trial lasted ____ years. | two / 2 | The host says so. | A two-year trial
? c | What happened to employment? | *It barely changed | It fell sharply | It rose sharply | Professor Lam explains. | employment barely changed.
? c | Who worked slightly less? | *Mostly parents of young children and returning students | Older workers | People with high incomes | Professor Lam explains. | mostly parents of young children and students who returned to education.
? c | Why is the professor cautious about introducing it everywhere? | *A small trial says little about a whole economy | Participants were unhappy | It made people ill | The professor explains. | A trial with a thousand people tells us little about how a whole economy would respond.

## Negotiating a salary | WK
Coach: When they ask what salary you expect, what will you say?
Client: I was going to say I'm flexible.
Coach: That usually means you'll get the lowest figure in their range. Research the market rate first, then give a specific number slightly above what you'd accept.
Client: Isn't that risky? What if they withdraw the offer?
Coach: Very rarely, if you're polite and give reasons, such as your experience with similar projects. And remember, salary isn't the only thing you can negotiate. Holidays and training budgets are often easier to move.
? c | What does the coach say about answering that you're flexible? | *It usually leads to the lowest offer | It shows confidence | It is the safest answer | The coach explains. | That usually means you'll get the lowest figure in their range.
? c | What does the coach advise? | *Giving a specific number slightly above your minimum | Asking for double | Refusing to answer | The coach advises. | give a specific number slightly above what you'd accept.
? t | According to the coach, employers often withdraw offers after a polite negotiation. | F | This happens very rarely. | Very rarely, if you're polite and give reasons
? c | What else can often be negotiated more easily? | *Holidays and training budgets | Job titles | The office location | The coach explains. | Holidays and training budgets are often easier to move.

## Losing the night sky | EN
Lecturer: For most of human history, people could see thousands of stars on a clear night. Today, around eighty percent of the world's population lives under skies polluted by artificial light.
Lecturer: This is not merely an aesthetic loss. Artificial light at night disrupts the migration of birds and the breeding of insects, and turtle hatchlings, which head for the brightest horizon, crawl inland towards roads instead of out to sea.
Lecturer: The encouraging part is that light pollution is unusually easy to reverse. Shielded street lamps that point downwards, warmer colours and timers can cut it dramatically without making streets less safe.
? c | What share of people live under light-polluted skies? | *Around eighty percent | Around half | Around a fifth | The lecturer gives the figure. | around eighty percent of the world's population lives under skies polluted by artificial light.
? c | Why do turtle hatchlings move inland? | *They head for the brightest horizon | They follow their mothers | They look for food | The lecturer explains. | which head for the brightest horizon, crawl inland towards roads
? c | What does the lecturer find encouraging? | *Light pollution is easy to reverse | Birds have adapted | People prefer bright streets | The lecturer explains. | light pollution is unusually easy to reverse.
? t | The lecturer says reducing light pollution makes streets less safe. | F | It can be cut without making streets less safe. | without making streets less safe.

## Rating your colleagues | WK
Mai: Our company has introduced peer reviews. Colleagues rate each other every six months.
Jon: How's that going?
Mai: Mixed. In theory, it gives a fuller picture than one manager's opinion. In practice, some people just give friends high scores.
Jon: Couldn't they make it anonymous?
Mai: It is anonymous, but in a team of six it's easy to guess who wrote what. So people avoid honest criticism.
Jon: Perhaps it works better in large teams.
Mai: Or if the comments focused on specific examples rather than scores.
? b | Colleagues rate each other every ____ months. | six / 6 | Mai explains. | Colleagues rate each other every six months.
? c | What problem has Mai noticed? | *Some people give friends high scores | Managers ignore the reviews | Reviews take too long | Mai explains. | some people just give friends high scores.
? c | Why do people avoid honest criticism? | *In a small team it's easy to guess who wrote what | The reviews are not anonymous | Managers punish criticism | Mai explains. | in a team of six it's easy to guess who wrote what.
? c | What improvement does Mai suggest? | *Focusing on specific examples rather than scores | Removing anonymity | Reviewing every month | Mai suggests it. | if the comments focused on specific examples rather than scores.

## The trouble with tipping | FD
Lena: I never know how much to tip when I travel. In some countries it's expected, in others it's almost rude.
Duc: The problem in places where tipping is expected is that it lets employers pay low wages and pass the cost to customers.
Lena: But if you don't tip there, the waiter suffers, not the employer.
Duc: Exactly, which is why some restaurants have abolished tipping and raised prices instead. Staff earn a stable wage, and customers know the real price.
Lena: Did it work?
Duc: For some. Others went back, because customers thought the menu looked expensive compared with their competitors.
? c | What does Duc see as the problem with expected tipping? | *It lets employers pay low wages | It is confusing for tourists | Customers tip too much | Duc explains. | it lets employers pay low wages and pass the cost to customers.
? c | Why should customers still tip in those places, according to Lena? | *Otherwise the waiter suffers | The employer will be fined | Tips are taxed | Lena explains. | if you don't tip there, the waiter suffers, not the employer.
? c | What have some restaurants done? | *Abolished tipping and raised prices | Doubled tips | Paid waiters in cash | Duc explains. | some restaurants have abolished tipping and raised prices instead.
? t | All restaurants that stopped tipping kept the new system. | F | Some went back. | Others went back

## The fifteen-minute city | PT
Planner: The idea of the fifteen-minute city is simple: most daily needs, such as shops, schools, clinics and parks, should be reachable within a fifteen-minute walk or bike ride.
Interviewer: Critics say it's a way of restricting people's movement.
Planner: That's a misunderstanding. Nobody is forbidden from going further. The aim is to make it unnecessary to drive for every errand.
Interviewer: Isn't it easier in old European cities than in sprawling ones?
Planner: Much easier, yes. In sprawling cities it means allowing small shops and services in residential areas, which current zoning often prohibits.
? c | What is the aim of the fifteen-minute city? | *Most daily needs within a short walk or ride | Banning cars | Building more motorways | The planner explains. | should be reachable within a fifteen-minute walk or bike ride.
? c | How does the planner respond to critics? | *Nobody is forbidden from going further | Movement should be restricted | The critics are right | The planner responds. | Nobody is forbidden from going further.
? t | The planner agrees it is easier in old European cities. | T | The planner says much easier. | Much easier, yes.
? c | What often prevents it in sprawling cities? | *Zoning rules | Lack of money | Bad weather | The planner explains. | which current zoning often prohibits.

## Learning a language from films | ED
Host: Can you really learn a language by watching films?
Guest: You can learn a lot, but not in the way people imagine. Simply having a film on in the background does very little.
Host: So what works?
Guest: Active watching. Choose a short scene, watch it with subtitles in the language you're learning, then without, and repeat lines aloud. Ten focused minutes beat two passive hours.
Host: Should beginners avoid subtitles in their own language?
Guest: Not at first. At early levels, understanding the story keeps you motivated, and motivation matters more than method.
? c | What does the guest say about having a film on in the background? | *It does very little | It works best | It is enough for beginners | The guest explains. | Simply having a film on in the background does very little.
? c | What is active watching? | *Repeating short scenes with and without subtitles and saying lines aloud | Watching whole films without stopping | Watching only cartoons | The guest explains. | watch it with subtitles in the language you're learning, then without, and repeat lines aloud.
? t | The guest says two passive hours are better than ten focused minutes. | F | Ten focused minutes are better. | Ten focused minutes beat two passive hours.
? c | Why can beginners use subtitles in their own language at first? | *Understanding the story keeps them motivated | It improves pronunciation | It is required in class | The guest explains. | understanding the story keeps you motivated

## Antibiotics and colds | HE
Doctor: Every time antibiotics are used, bacteria have a chance to evolve resistance. That's why we only prescribe them when they're really needed.
Patient: But my friend always gets antibiotics for a cold.
Doctor: Colds are caused by viruses, and antibiotics don't work against viruses at all. Taking them just exposes the bacteria in your body to the drug for no benefit.
Patient: So what should I do?
Doctor: Rest, fluids and patience. If you're not better in ten days, or if you develop a high fever, come back and we'll look again.
? c | Why does the doctor limit antibiotics? | *Each use gives bacteria a chance to become resistant | They are expensive | They cause colds | The doctor explains. | Every time antibiotics are used, bacteria have a chance to evolve resistance.
? c | Why don't antibiotics help with colds? | *Colds are caused by viruses | Colds are too mild | The doses are too small | The doctor explains. | Colds are caused by viruses, and antibiotics don't work against viruses at all.
? c | What does the doctor recommend? | *Rest, fluids and patience | A stronger antibiotic | Vitamin tablets | The doctor advises. | Rest, fluids and patience.
? b | Come back if you're not better in ____ days. | ten / 10 | The doctor gives a limit. | If you're not better in ten days

## Translating a poem | CO
Interviewer: Is poetry the hardest thing to translate?
Translator: In some ways. In a novel, if one sentence loses a little, the next one carries the story. In a poem, every word is doing several jobs at once: meaning, sound, rhythm, sometimes a double meaning.
Interviewer: So something always gets lost?
Translator: Always, but something can also be gained. Sometimes the new language offers a rhyme or an image the original didn't have. The skill is deciding which qualities matter most in a particular poem.
? c | Why is a novel easier to translate, according to the translator? | *The story carries on even if one sentence loses a little | Novels use simpler words | Novels are shorter | The translator explains. | if one sentence loses a little, the next one carries the story.
? c | What does each word in a poem do? | *Several jobs at once | Only carry meaning | Only make a rhyme | The translator explains. | every word is doing several jobs at once
? t | The translator believes translation can also add something. | T | Something can be gained. | but something can also be gained.
? c | What is the translator's key skill? | *Deciding which qualities matter most | Finding exact equivalents | Translating quickly | The translator explains. | The skill is deciding which qualities matter most in a particular poem.

## Cars without drivers | TE
Moderator: Should self-driving cars be allowed on city streets?
Speaker A: They don't get tired, drunk or distracted. Human error causes the vast majority of accidents, so removing the human should save lives.
Speaker B: In principle. But these systems still struggle with the unexpected: a child chasing a ball, road works, a police officer waving traffic through. City streets are full of exceptions.
Speaker A: Then start with motorways and controlled routes, and expand as the technology proves itself.
Speaker B: That I could support, provided the companies share their accident data publicly.
? c | What is Speaker A's main argument? | *Most accidents are caused by human error | Self-driving cars are cheaper | Cities need fewer cars | Speaker A explains. | Human error causes the vast majority of accidents
? c | What does Speaker B say the systems struggle with? | *The unexpected | Bad weather only | Long distances | Speaker B explains. | these systems still struggle with the unexpected
? c | What compromise does Speaker A suggest? | *Starting with motorways and controlled routes | Banning them completely | Using them only at night | Speaker A suggests it. | start with motorways and controlled routes
? t | Speaker B accepts the compromise without any conditions. | F | Accident data must be shared publicly. | provided the companies share their accident data publicly.

## The merger | WK
CEO: As you know, we've agreed to merge with Northbridge. I want to address the question everyone is asking: jobs.
CEO: There will be some overlap in finance and administration, and some roles will change. However, we expect most changes to be handled through retirements and people moving between teams, not redundancies.
CEO: Over the next month, every department head will meet their teams individually. I'd rather you hear details from them than from rumours.
CEO: I won't pretend this will be easy, but the combined company will be strong enough to invest in the projects we've had to postpone for years.
? c | What is the CEO's first concern in the speech? | *Jobs | Profits | The new name | The CEO says so. | I want to address the question everyone is asking: jobs.
? c | How does the CEO expect most changes to be handled? | *Through retirements and moves between teams | Through redundancies | Through new hiring | The CEO explains. | through retirements and people moving between teams, not redundancies.
? c | Why will department heads meet teams individually? | *So staff hear details from them rather than rumours | To choose who leaves | To plan a party | The CEO explains. | I'd rather you hear details from them than from rumours.
? t | The CEO says the merger will be easy. | F | The CEO won't pretend it will be easy. | I won't pretend this will be easy

## Letting the river curve | EN
Reporter: Twenty years ago, this river was straightened and lined with concrete to stop flooding. Now the concrete is being removed.
Ecologist: Straight channels move water faster, which simply sends the flood downstream to the next town. Letting the river curve again and spill onto meadows slows the water and stores it.
Reporter: Hasn't that meant some farmland flooding?
Ecologist: A little, yes, and farmers are compensated. But fish, insects and birds have returned within three years, and the town below hasn't flooded since.
? c | Why was the river originally straightened? | *To stop flooding | To help boats | To build houses | The reporter explains. | straightened and lined with concrete to stop flooding.
? c | What is the problem with straight channels? | *They send floods downstream | They dry up in summer | They are expensive | The ecologist explains. | which simply sends the flood downstream to the next town.
? t | Farmers whose land floods receive compensation. | T | The ecologist says so. | farmers are compensated.
? c | What has happened to the town below? | *It hasn't flooded since | It floods more often | It has been abandoned | The ecologist explains. | the town below hasn't flooded since.

## A gap in the CV | WK
Client: I spent two years caring for my father. Now there's a gap in my CV, and I'm worried employers will see it badly.
Advisor: Don't hide it. Unexplained gaps worry employers far more than explained ones.
Client: But what do I say?
Advisor: Be brief and honest, then move on to what you can offer. Caring involves organising appointments, managing a budget and handling stressful situations. Those are real skills.
Client: I hadn't thought of it that way.
Advisor: And mention any courses or reading you did to keep your skills up to date.
? c | Why does the client have a gap in the CV? | *Two years caring for a parent | Travelling abroad | Studying | The client explains. | I spent two years caring for my father.
? c | What worries employers more, according to the advisor? | *Unexplained gaps | Explained gaps | Long CVs | The advisor explains. | Unexplained gaps worry employers far more than explained ones.
? c | Which skills does the advisor point out? | *Organising, managing a budget and handling stress | Programming and design | Sales and marketing | The advisor lists them. | Caring involves organising appointments, managing a budget and handling stressful situations.
? t | The advisor recommends hiding the gap. | F | The advisor says not to hide it. | Don't hide it.

## A four-day school week | ED
Presenter: Some rural schools have moved to a four-day week to save money and attract teachers.
Researcher: The savings turned out to be modest, about two percent of budgets. Teacher recruitment did improve, though.
Presenter: And the students?
Researcher: Results were mixed. Older students generally did fine, but younger children, especially from poorer families, fell behind. For them, the fifth day had often meant a free meal and a safe place.
Presenter: So would you recommend it?
Researcher: Only with good programmes on the fifth day for families who need them.
? c | Why did some schools move to a four-day week? | *To save money and attract teachers | To improve results | To reduce traffic | The presenter explains. | to save money and attract teachers.
? c | How large were the savings? | *Modest, about two percent | Large, about half | Nothing at all | The researcher explains. | The savings turned out to be modest, about two percent of budgets.
? c | Which students fell behind? | *Younger children from poorer families | Older students | All students equally | The researcher explains. | younger children, especially from poorer families, fell behind.
? t | The researcher recommends the change without conditions. | F | Only with good fifth-day programmes. | Only with good programmes on the fifth day

## The repair café | SH
Organiser: Welcome to the repair café. Every Saturday, volunteers fix clothes, toasters, bikes, whatever you bring.
Visitor: Why not just buy a new one? It's often cheaper.
Organiser: Cheaper at the till, perhaps, but not for the planet. And many people find that fixing something they own creates a kind of attachment you don't get with a new item.
Visitor: Do you charge?
Organiser: No, but we ask people to sit with the volunteer while they work, so they learn to do it themselves next time.
? c | What happens at the repair café? | *Volunteers fix things people bring | Second-hand items are sold | People learn to cook | The organiser explains. | volunteers fix clothes, toasters, bikes, whatever you bring.
? c | What does the organiser say about buying new? | *It may be cheaper at the till but not for the planet | It is always more expensive | It is always better | The organiser explains. | Cheaper at the till, perhaps, but not for the planet.
? t | The café charges for repairs. | F | There is no charge. | No, but we ask people to sit with the volunteer
? c | Why do visitors sit with the volunteer? | *To learn to do the repair themselves | To pay the volunteer | To keep the volunteer company | The organiser explains. | so they learn to do it themselves next time.

## Ten years in a second language | CO
Interviewer: You've worked in English for ten years. Does it still feel different?
Lan: In meetings, yes. I can say what I mean, but jokes and quick arguments are harder. By the time I've found the right phrase, the conversation has moved on.
Interviewer: How do you deal with that?
Lan: I prepare key points before important meetings and send a short summary afterwards. Writing gives me time that speaking doesn't.
Interviewer: Any advantages to working in a second language?
Lan: I listen more carefully. Native speakers sometimes hear what they expect rather than what was said.
? b | Lan has worked in English for ____ years. | ten / 10 | The interviewer says so. | You've worked in English for ten years.
? c | What is still hard for Lan in meetings? | *Jokes and quick arguments | Formal presentations | Reading reports | Lan explains. | jokes and quick arguments are harder.
? c | Why does Lan send a summary afterwards? | *Writing gives Lan more time | A manager requires it | Meetings are recorded | Lan explains. | Writing gives me time that speaking doesn't.
? t | Lan thinks native speakers always listen carefully. | F | They sometimes hear what they expect. | Native speakers sometimes hear what they expect rather than what was said.

## Who pays for the stadium? | HS
Reporter: The city plans to spend five hundred million dollars on a new stadium, saying it will boost the local economy.
Economist: The evidence for that is weak. Most of the money fans spend at the stadium would otherwise have been spent elsewhere in the city, at cinemas or restaurants.
Reporter: What about tourism?
Economist: Major events do bring visitors, but only a few days a year. Meanwhile the city pays maintenance every day.
Reporter: So stadiums are never a good idea?
Economist: They can be, if the team pays most of the cost, or if the stadium is used for many other events throughout the year.
? b | The stadium will cost five hundred ____ dollars. | million | The reporter gives the figure. | five hundred million dollars
? c | Why is the economic argument weak? | *Fans would spend the money elsewhere in the city anyway | Stadiums are rarely full | Tickets are free | The economist explains. | Most of the money fans spend at the stadium would otherwise have been spent elsewhere in the city
? c | What does the economist say about tourism? | *Visitors come only a few days a year | It doubles | It is the main benefit | The economist explains. | Major events do bring visitors, but only a few days a year.
? t | The economist says stadiums are never a good idea. | F | They can be under some conditions. | They can be, if the team pays most of the cost

## A doctor four hours away | HE
Doctor: In our mountain clinic, many patients live four hours away. Video consultations have changed that.
Interviewer: Can you really examine someone through a screen?
Doctor: Not fully. But a large part of medicine is talking: understanding symptoms, adjusting medication, following up after treatment. For that, video works well.
Interviewer: What are the limits?
Doctor: Anything that needs touch, such as listening to the lungs, or tests. And older patients sometimes struggle with the technology, so a nurse often sits with them in the village health post.
? b | Many patients live ____ hours away from the clinic. | four / 4 | The doctor says so. | many patients live four hours away.
? c | Why does video work well for much of medicine? | *Much of it is talking | Cameras are very good | Patients prefer screens | The doctor explains. | a large part of medicine is talking
? c | What can't video do? | *Anything that needs touch, or tests | Adjust medication | Follow up after treatment | The doctor explains. | Anything that needs touch, such as listening to the lungs, or tests.
? t | Older patients sometimes get help from a nurse. | T | A nurse often sits with them. | a nurse often sits with them in the village health post.

## Reading a headline carefully | TE
Teacher: Read this headline: coffee cuts the risk of disease by fifty percent. What questions should we ask?
Student: How many people were in the study?
Teacher: Good. And?
Student: Whether the coffee caused it, or the coffee drinkers were different in other ways.
Teacher: Exactly. In this study, the coffee drinkers were also younger and exercised more. And fifty percent sounds huge, but the risk fell from two in a thousand to one in a thousand.
Student: So the headline is technically true but misleading.
? c | What is the first question the student asks? | *How many people were in the study | Who paid for the study | When it was published | The student asks it. | How many people were in the study?
? c | Why might coffee not be the cause? | *Coffee drinkers were different in other ways | Coffee is unhealthy | The study was too long | The teacher gives the details. | the coffee drinkers were also younger and exercised more.
? c | How did the risk actually change? | *From two in a thousand to one in a thousand | From fifty to twenty-five percent | From one in ten to one in twenty | The teacher explains. | the risk fell from two in a thousand to one in a thousand.
? t | The student concludes the headline is completely false. | F | It is technically true but misleading. | So the headline is technically true but misleading.

## Buying a home together | MS
Advisor: Before you buy together, have you discussed what happens if you separate?
Woman: We'd rather not think about that.
Advisor: I understand, but it protects you both. For example, if one of you pays a larger deposit, you can record that in writing, so that person gets it back first if you sell.
Man: That seems fair. My parents are helping with my share.
Advisor: Then that's even more reason. It avoids arguments later, when emotions are high.
? c | What does the advisor ask about first? | *What happens if they separate | Their salaries | The location | The advisor asks. | have you discussed what happens if you separate?
? c | Why does the advisor recommend recording deposits? | *So the person who paid more gets it back first | To pay less tax | To get a cheaper loan | The advisor explains. | so that person gets it back first if you sell.
? t | The man's parents are helping with his share. | T | He says so. | My parents are helping with my share.
? c | When are arguments more likely, according to the advisor? | *Later, when emotions are high | Before buying | When prices rise | The advisor explains. | It avoids arguments later, when emotions are high.

## Students as lodgers | PF
Speaker: Loneliness is sometimes described as being as harmful to health as smoking. Whatever the exact figure, the link is real.
Speaker: Older people are at particular risk, especially after retirement or losing a partner.
Speaker: One programme pairs older residents with university students who need cheap accommodation. The students pay low rent in exchange for spending a few evenings a week with their host.
Speaker: Both sides often say the most valuable part isn't the rent or the help, but the friendship.
? c | What comparison does the speaker mention? | *Loneliness may be as harmful as smoking | Loneliness is worse than poverty | Loneliness is like a cold | The speaker says so. | Loneliness is sometimes described as being as harmful to health as smoking.
? c | When are older people at particular risk? | *After retirement or losing a partner | In winter | When moving house | The speaker explains. | especially after retirement or losing a partner.
? c | What do students give in exchange for low rent? | *Evenings spent with their host | Cleaning services | Cooking every day | The speaker explains. | spending a few evenings a week with their host.
? t | Participants say the friendship is the most valuable part. | T | Both sides often say so. | the most valuable part isn't the rent or the help, but the friendship.

## Too many visitors | TR
Mayor: Last year, two million visitors came to a town of twenty thousand people. Residents can't get on buses, and rents have tripled as flats become holiday rentals.
Interviewer: What are you doing about it?
Mayor: We're introducing a daily entry fee for day visitors at peak times, and limiting new holiday rentals in the old centre.
Interviewer: Won't businesses suffer?
Mayor: Some might earn less in the short term. But if the town becomes a theme park with no residents, visitors will eventually stop coming too.
? c | How many people live in the town? | *Twenty thousand | Two million | Two hundred thousand | The mayor says so. | a town of twenty thousand people.
? c | What has happened to rents? | *They have tripled | They have halved | They have stayed the same | The mayor explains. | rents have tripled as flats become holiday rentals.
? c | What is one new measure? | *A daily entry fee for day visitors at peak times | Closing the town | Banning hotels | The mayor explains. | We're introducing a daily entry fee for day visitors at peak times
? t | The mayor admits some businesses may earn less. | T | In the short term. | Some might earn less in the short term.

## Meetings that work | WK
Consultant: Most meetings fail for the same three reasons: no clear purpose, too many people and no decisions at the end.
Consultant: Before booking a meeting, write one sentence describing what should be different when it ends. If you can't, send an email instead.
Consultant: Invite only those who need to decide or contribute. Others can read the notes.
Consultant: And finish by agreeing who will do what, by when. Without that, the same meeting will happen again next week.
? c | What are the three reasons meetings fail? | *No purpose, too many people, no decisions | Too short, too early, too formal | Bad rooms, bad coffee, bad timing | The consultant lists them. | no clear purpose, too many people and no decisions at the end.
? c | What should you do if you can't write the purpose in one sentence? | *Send an email instead | Make the meeting longer | Invite more people | The consultant advises. | If you can't, send an email instead.
? c | Who should be invited? | *Only those who need to decide or contribute | Everyone in the department | Only managers | The consultant advises. | Invite only those who need to decide or contribute.
? t | Without clear actions, the meeting may have to happen again. | T | The consultant warns of this. | Without that, the same meeting will happen again next week.
"""

LESSONS["C1"] += """
## Plastic we cannot see | HE
Presenter: Tiny pieces of plastic have been found in tap water, sea salt and even human blood. Should we be worried?
Scientist: Concerned, yes. Alarmed, not yet. We know microplastics are everywhere, but we don't yet know what levels, if any, harm human health.
Presenter: Why is it so hard to find out?
Scientist: Partly because there's no clean group to compare with. Everyone is exposed. And the particles vary enormously in size and chemistry.
Presenter: What would you advise in the meantime?
Scientist: Reasonable steps, like not heating food in plastic containers, which releases more particles. But the bigger solution is producing less plastic in the first place.
? c | What is the scientist's attitude? | *Concerned but not alarmed | Very alarmed | Not concerned at all | The scientist explains. | Concerned, yes. Alarmed, not yet.
? c | Why is the research difficult? | *There is no unexposed group to compare with | The particles are too large | Nobody funds it | The scientist explains. | there's no clean group to compare with. Everyone is exposed.
? c | What practical step does the scientist suggest? | *Not heating food in plastic containers | Drinking only bottled water | Avoiding salt | The scientist advises. | not heating food in plastic containers
? t | The scientist sees individual habits as the main solution. | F | The bigger solution is producing less plastic. | the bigger solution is producing less plastic in the first place.

## A team across time zones | WK
Manager: Our team is spread across three continents now. How are you finding it?
Developer: The work is fine, but meetings are hard. Someone is always joining at seven in the morning or ten at night.
Manager: We could rotate the meeting time, so the inconvenience is shared.
Developer: That would be fairer. But honestly, we could have fewer meetings. Most updates could be written in a shared document.
Manager: Agreed. Let's keep one weekly call for decisions and do the rest in writing.
? b | The team is spread across ____ continents. | three / 3 | The manager says so. | Our team is spread across three continents now.
? c | What is the developer's main difficulty? | *Meeting times are inconvenient for someone | The work is too hard | The software is slow | The developer explains. | Someone is always joining at seven in the morning or ten at night.
? c | What does the manager first suggest? | *Rotating the meeting time | Cancelling all meetings | Hiring local staff | The manager suggests it. | We could rotate the meeting time, so the inconvenience is shared.
? c | What do they finally agree? | *One weekly call for decisions and the rest in writing | Daily video calls | Meetings only at night | The manager concludes. | Let's keep one weekly call for decisions and do the rest in writing.

## Returning museum objects | ED
Interviewer: Several museums are returning objects that were taken during colonial times. Is that the right decision?
Curator: In many cases, yes. Some objects were taken by force or without any meaningful consent, and they have deep religious or cultural meaning for their communities.
Interviewer: Won't museums lose their collections?
Curator: Some objects will leave, but many returns lead to partnerships: shared exhibitions, loans and joint research. A museum's job is to help people understand cultures, not simply to own things.
Interviewer: And objects whose history is unclear?
Curator: Those need careful research, case by case. Not every object was taken unfairly.
? c | Why does the curator support many returns? | *Some objects were taken without real consent and matter deeply to communities | Museums have too many objects | Objects are often damaged | The curator explains. | Some objects were taken by force or without any meaningful consent
? c | What do returns often lead to? | *Partnerships such as shared exhibitions and loans | Closed museums | Lower visitor numbers | The curator explains. | many returns lead to partnerships: shared exhibitions, loans and joint research.
? c | What is a museum's job, according to the curator? | *Helping people understand cultures | Owning as many objects as possible | Making money | The curator explains. | A museum's job is to help people understand cultures, not simply to own things.
? t | The curator believes every object was taken unfairly. | F | Not every object was. | Not every object was taken unfairly.

## Watering with less | EN
Farmer: Ten years ago we flooded our fields, like everyone did. Then the dry seasons got longer.
Interviewer: What changed?
Farmer: We switched to drip irrigation. Water goes straight to the roots through thin pipes, so very little is lost.
Interviewer: Was it expensive?
Farmer: The pipes cost a lot at first, and the government covered about half. But we now use around forty percent less water, and our harvests are more reliable.
Interviewer: Why don't all farmers do it?
Farmer: The upfront cost, mostly. And some crops, like rice, really need flooded fields.
? c | Why did the farmer change methods? | *The dry seasons got longer | Water became free | The soil changed | The farmer explains. | Then the dry seasons got longer.
? c | How does drip irrigation work? | *Water goes straight to the roots through thin pipes | Fields are flooded at night | Rain is collected on roofs | The farmer explains. | Water goes straight to the roots through thin pipes
? b | They now use around ____ percent less water. | forty / 40 | The farmer gives the figure. | we now use around forty percent less water
? t | Drip irrigation suits every crop. | F | Some crops like rice need flooded fields. | some crops, like rice, really need flooded fields.

## Why online courses are left unfinished | ED
Researcher: Free online courses attract huge numbers of learners, but often fewer than one in ten finish.
Presenter: Does that mean they fail?
Researcher: Not necessarily. Many people sign up just to watch a few videos, and they get exactly what they wanted. Completion isn't always the right measure.
Presenter: But for those who want to finish?
Researcher: Deadlines and community make the biggest difference. Learners who join a study group, even online, are far more likely to complete the course than those who study alone.
? c | How many learners often finish free online courses? | *Fewer than one in ten | About half | Most of them | The researcher says so. | often fewer than one in ten finish.
? c | Why may low completion not mean failure? | *Many people only want to watch a few videos | The courses are too easy | Certificates are expensive | The researcher explains. | Many people sign up just to watch a few videos, and they get exactly what they wanted.
? c | What helps people finish? | *Deadlines and community | Longer videos | Harder tests | The researcher explains. | Deadlines and community make the biggest difference.
? t | Learners in study groups are less likely to finish. | F | They are far more likely to finish. | far more likely to complete the course than those who study alone.

## Photographing wildlife responsibly | AN
Photographer: Social media has made wildlife photography hugely popular, which has a downside.
Interviewer: In what way?
Photographer: When a rare owl appears, hundreds of people may arrive within hours. Some get too close, use flash or even play recorded calls to attract the bird. That stresses animals at sensitive times, like nesting.
Interviewer: What should photographers do?
Photographer: Keep a distance and use a longer lens. Don't share exact locations of rare or nesting animals. And accept that sometimes the right decision is to leave without the photo.
? c | What downside of popularity does the photographer describe? | *Crowds disturbing animals | Expensive cameras | Too many photos online | The photographer explains. | hundreds of people may arrive within hours.
? c | Which behaviour stresses animals? | *Using flash and playing recorded calls | Staying far away | Using long lenses | The photographer explains. | use flash or even play recorded calls to attract the bird.
? c | What should photographers avoid sharing? | *Exact locations of rare or nesting animals | Their camera settings | Their names | The photographer advises. | Don't share exact locations of rare or nesting animals.
? t | The photographer says you should always get the photo. | F | Sometimes the right decision is to leave without it. | sometimes the right decision is to leave without the photo.

## A world without cash? | MS
Presenter: In some countries, cash now makes up a small fraction of payments. Is that a problem?
Economist: For most people, card and phone payments are faster and safer. But a cashless society can exclude people.
Presenter: Who exactly?
Economist: Older people who aren't comfortable with technology, people without bank accounts, and anyone living where the network is unreliable. Cash also works when systems go down.
Presenter: So should governments protect cash?
Economist: I think so. Several countries now require shops and banks to keep accepting it, at least for essential goods.
? c | What does the economist say about card and phone payments? | *They are faster and safer for most people | They are always risky | They cost more | The economist explains. | card and phone payments are faster and safer.
? c | Who could be excluded? | *Older people, the unbanked and those with poor networks | Only young people | Only shop owners | The economist lists them. | Older people who aren't comfortable with technology, people without bank accounts
? c | What advantage of cash is mentioned? | *It works when systems go down | It is cleaner | It earns interest | The economist explains. | Cash also works when systems go down.
? t | Some countries require shops to accept cash. | T | The economist mentions this. | Several countries now require shops and banks to keep accepting it

## Later school start times | HE
Doctor: During adolescence, the body clock shifts. Teenagers genuinely find it hard to fall asleep before eleven, so an early school start leaves many of them short of sleep.
Interviewer: Some schools have moved their start time later. Did it help?
Doctor: In several studies, starting even an hour later improved attendance and mood, and fewer students fell asleep in class.
Interviewer: What are the objections?
Doctor: Mostly practical: bus timetables, parents' working hours, after-school sports. They're real, but they're problems of organisation, not of biology.
? c | Why do teenagers struggle with early starts? | *Their body clock shifts later | They use phones too much | They eat late | The doctor explains. | During adolescence, the body clock shifts.
? c | What happened when schools started later? | *Attendance and mood improved | Grades fell | Students slept less | The doctor explains. | improved attendance and mood
? c | What kind of objections are there? | *Practical ones like buses and parents' hours | Medical ones | Financial ones only | The doctor explains. | Mostly practical: bus timetables, parents' working hours, after-school sports.
? t | The doctor thinks the objections are about biology. | F | They are problems of organisation. | they're problems of organisation, not of biology.

## Video replays in football | HS
Commentator: Since video replays were introduced, there have been fewer clear refereeing mistakes. So why are many fans unhappy?
Former referee: Because football is emotional, and replays interrupt that emotion. You celebrate a goal, then wait three minutes while someone in a studio checks whether a toe was offside.
Commentator: But surely accuracy matters?
Former referee: It does. The problem is that tiny offside decisions are now judged by millimetres, which the rule was never designed for. I'd only use replays for clear and obvious errors, as originally intended.
? c | What has improved since replays were introduced? | *Fewer clear refereeing mistakes | Shorter matches | More goals | The commentator says so. | there have been fewer clear refereeing mistakes.
? c | Why are many fans unhappy? | *Replays interrupt the emotion | Tickets cost more | Matches are cancelled | The former referee explains. | replays interrupt that emotion.
? c | What problem does the former referee see with offside? | *Decisions judged by millimetres | Too few cameras | Referees ignore replays | The former referee explains. | tiny offside decisions are now judged by millimetres
? t | The former referee wants to stop using replays completely. | F | Only for clear and obvious errors. | I'd only use replays for clear and obvious errors

## A second life for batteries | TE
Engineer: An electric car battery is usually replaced when it holds about seventy percent of its original charge.
Interviewer: So it's thrown away?
Engineer: It shouldn't be. Seventy percent is too little for driving long distances, but perfectly useful for storing solar energy in a home or a building.
Interviewer: And when it finally wears out?
Engineer: Then it can be recycled. Current processes can recover most of the valuable metals, though recycling is still more expensive than mining new materials in many places.
? b | Batteries are usually replaced at about ____ percent of their original charge. | seventy / 70 | The engineer says so. | when it holds about seventy percent of its original charge.
? c | What can old car batteries be used for? | *Storing solar energy | Powering buses | Making new cars | The engineer explains. | perfectly useful for storing solar energy in a home or a building.
? c | What can recycling recover? | *Most of the valuable metals | All plastic parts | Only the case | The engineer explains. | Current processes can recover most of the valuable metals
? t | Recycling is always cheaper than mining. | F | In many places it is still more expensive. | recycling is still more expensive than mining new materials in many places.

## A garden for everyone | PT
Organiser: This community garden started on an empty car park five years ago. Now about sixty families grow food here.
Visitor: Who are the gardeners?
Organiser: A real mix: retired people, students and many families who have recently moved to the city. For some newcomers, it's the first place they made friends.
Visitor: Do people grow food from their home countries?
Organiser: Yes, and that's become a way of sharing. We hold a harvest meal each autumn where everyone cooks something from their plot.
? c | What was the garden before? | *An empty car park | A school | A farm | The organiser explains. | This community garden started on an empty car park five years ago.
? b | About ____ families grow food there. | sixty / 60 | The organiser says so. | about sixty families grow food here.
? c | What has the garden meant for some newcomers? | *The first place they made friends | A source of income | A place to live | The organiser explains. | it's the first place they made friends.
? t | There is a shared meal each spring. | F | It is each autumn. | We hold a harvest meal each autumn

## The problem with voluntourism | TR
Interviewer: Short volunteer trips abroad are very popular. What's your concern?
Researcher: Some programmes are designed more for the volunteers than the communities. Building a school with unskilled tourists can take jobs from local builders, and the result is sometimes poorly made.
Interviewer: And working with children?
Researcher: That's the most worrying. Children in care can form attachments to volunteers who leave after two weeks, again and again.
Interviewer: So should people not volunteer?
Researcher: They should choose carefully: longer stays, real skills that are actually requested, and organisations led by local people.
? c | What is the researcher's main concern? | *Some programmes serve volunteers more than communities | Volunteers spend too little | The trips are too long | The researcher explains. | Some programmes are designed more for the volunteers than the communities.
? c | What problem can building projects cause? | *Taking jobs from local builders | Using too much water | Damaging roads | The researcher explains. | can take jobs from local builders
? c | Why is working with children most worrying? | *Children form attachments to volunteers who leave | Volunteers are untrained teachers | It is too expensive | The researcher explains. | Children in care can form attachments to volunteers who leave after two weeks
? t | The researcher says people should never volunteer abroad. | F | They should choose carefully. | They should choose carefully

## Raising money from the crowd | MS
Founder: We raised forty thousand dollars on a crowdfunding site in a month, from about nine hundred supporters.
Interviewer: What made it work?
Founder: A clear video showing the product in use, and an honest budget. People want to know exactly where their money goes.
Interviewer: Any regrets?
Founder: We underestimated shipping costs. Sending rewards to supporters in thirty countries cost far more than expected, and we nearly lost money.
Interviewer: Advice for others?
Founder: Calculate the cost of every reward, including delivery, before you launch.
? b | They raised forty ____ dollars. | thousand | The founder says so. | We raised forty thousand dollars
? c | What helped the campaign work? | *A clear video and an honest budget | Celebrity support | Very low prices | The founder explains. | A clear video showing the product in use, and an honest budget.
? c | What did they underestimate? | *Shipping costs | The number of supporters | The time needed | The founder explains. | We underestimated shipping costs.
? t | They made a large profit on shipping. | F | They nearly lost money. | we nearly lost money.

## Notes by hand or on a laptop? | ED
Lecturer: Students who take notes on laptops often write more, but some studies suggest they remember less.
Student: Why would writing more mean remembering less?
Lecturer: Because fast typists tend to copy the lecture word for word. Writing by hand is slower, so you're forced to choose and summarise, which means processing the ideas.
Student: So should we ban laptops?
Lecturer: No. A laptop is fine if you use it the same way: summarise in your own words rather than transcribing.
? c | What do some studies suggest about laptop note-takers? | *They write more but may remember less | They write less | They remember more | The lecturer explains. | write more, but some studies suggest they remember less.
? c | Why may handwriting help memory? | *It forces you to summarise | It is more relaxing | It is neater | The lecturer explains. | so you're forced to choose and summarise
? c | What does the lecturer advise for laptop users? | *Summarise in your own words | Type every word | Use only short notes | The lecturer advises. | summarise in your own words rather than transcribing.
? t | The lecturer wants to ban laptops. | F | A laptop is fine if used well. | A laptop is fine if you use it the same way

## An airline apologises | CO
Spokesperson: Last weekend, a system failure cancelled more than two hundred flights. I want to apologise to every passenger affected.
Spokesperson: We understand that apologies aren't enough. All passengers on cancelled flights will receive a full refund and a travel voucher, whether or not they chose to rebook.
Spokesperson: We've also commissioned an independent review of what went wrong, and we'll publish its findings in full.
Spokesperson: Our immediate priority is making sure the backup system can take over within minutes, not hours.
? c | What caused the cancellations? | *A system failure | A strike | Bad weather | The spokesperson explains. | a system failure cancelled more than two hundred flights.
? c | What will affected passengers receive? | *A full refund and a travel voucher | A free flight only | Nothing unless they rebook | The spokesperson explains. | will receive a full refund and a travel voucher
? t | The review's findings will be published only in part. | F | They will be published in full. | we'll publish its findings in full.
? c | What is the immediate priority? | *A backup system that takes over within minutes | Hiring more staff | Lowering prices | The spokesperson explains. | making sure the backup system can take over within minutes, not hours.

## Heat and older people | NW
Doctor: During heatwaves, deaths among older people rise sharply, and many happen at home, not in hospital.
Presenter: Why are older people more at risk?
Doctor: The body's ability to cool down weakens with age, and some medicines make it worse. Many older people also don't feel thirsty, so they drink too little.
Presenter: What can families do?
Doctor: Call or visit elderly relatives during hot spells, especially those who live alone. Check that they're drinking regularly and that at least one room stays cool.
? c | Where do many heat-related deaths happen? | *At home | In hospital | Outdoors | The doctor explains. | many happen at home, not in hospital.
? c | Why do older people drink too little? | *Many don't feel thirsty | Water is expensive | They forget to buy it | The doctor explains. | Many older people also don't feel thirsty
? c | What can make cooling down harder? | *Some medicines | Cold food | Light clothes | The doctor explains. | some medicines make it worse.
? t | The doctor advises checking on relatives who live alone. | T | The doctor says so. | especially those who live alone.

## Tall towers or low streets? | HF
Architect: Many people assume that tall towers are the only way to house more people in cities. But some of the densest neighbourhoods in Europe are only five or six storeys high.
Interviewer: How is that possible?
Architect: Buildings sit close together around shared courtyards, with shops on the ground floor. There's less empty space between them.
Interviewer: Why do you prefer that?
Architect: Streets feel more human. People can call down to a child in the courtyard. In a fortieth-floor flat, the street is a different world.
? c | What assumption does the architect challenge? | *Tall towers are the only way to house more people | Low buildings are cheaper | Cities should stop growing | The architect explains. | Many people assume that tall towers are the only way to house more people in cities.
? b | Some dense neighbourhoods are only five or ____ storeys high. | six / 6 | The architect says so. | only five or six storeys high.
? c | How do these neighbourhoods reach high density? | *Buildings sit close together around courtyards | They have no shops | They use underground homes | The architect explains. | Buildings sit close together around shared courtyards
? t | The architect prefers very tall towers. | F | Lower streets feel more human. | Streets feel more human.

## Colours on food labels | FD
Presenter: Some countries print traffic-light colours on food packets: red for high sugar, salt or fat, green for low.
Nutritionist: They're simple, which is their strength. Shoppers make decisions in seconds, and colours work faster than numbers.
Presenter: Do they change what people buy?
Nutritionist: Modestly. More importantly, they've pushed companies to change recipes, because nobody wants a red label on the front of their product.
Presenter: Any criticism?
Nutritionist: They judge single nutrients rather than the whole food, so some healthy foods, like nuts, can look worse than they are.
? c | What is the strength of the labels? | *They are simple and quick to understand | They are very detailed | They are cheap to print | The nutritionist explains. | They're simple, which is their strength.
? c | What effect have they had on companies? | *Companies have changed their recipes | Companies have stopped selling food | Companies have raised prices | The nutritionist explains. | they've pushed companies to change recipes
? c | What is one criticism? | *Some healthy foods can look worse than they are | They are too colourful | People ignore green | The nutritionist explains. | some healthy foods, like nuts, can look worse than they are.
? t | The labels have hugely changed what shoppers buy. | F | Only modestly. | Modestly.

## The product that failed | WK
Manager: Our new app launched three months ago, and only a few hundred people use it. I'd like us to understand why, without blaming anyone.
Designer: We built what we thought users wanted, but we only tested it with our own staff.
Manager: So we never checked with real customers?
Designer: Not until the end, and by then changing it was expensive.
Manager: Then the lesson isn't that the idea was bad. It's that we tested too late. Next time, we'll show a simple version to real users within the first month.
? c | How many people use the app? | *Only a few hundred | Several thousand | Nobody at all | The manager explains. | only a few hundred people use it.
? c | What does the manager want to avoid? | *Blaming anyone | Spending money | Talking to customers | The manager says so. | without blaming anyone.
? c | Who was the app tested with? | *Only the company's own staff | Thousands of customers | Students | The designer explains. | we only tested it with our own staff.
? t | The manager concludes the idea itself was bad. | F | The lesson is that they tested too late. | the lesson isn't that the idea was bad. It's that we tested too late.

## Phones out of school | TE
Headteacher: A year ago we asked students to lock their phones away from the start of the school day until it ended.
Interviewer: How did students react?
Headteacher: Badly, at first. There were complaints and some parents were worried about emergencies. We made sure parents could always reach the school office.
Interviewer: And now?
Headteacher: Teachers say lessons are calmer, and there's much more conversation at break time. Reports of online bullying during school hours have fallen. I wouldn't claim it solved everything, but nobody wants to go back.
? c | What did the school ask students to do? | *Lock their phones away during the school day | Use phones only in lessons | Leave phones at home | The headteacher explains. | we asked students to lock their phones away from the start of the school day until it ended.
? c | How were parents' worries handled? | *Parents could always reach the school office | Students kept one phone each | Teachers carried phones | The headteacher explains. | We made sure parents could always reach the school office.
? c | What has fallen? | *Reports of online bullying during school hours | Exam results | Attendance | The headteacher explains. | Reports of online bullying during school hours have fallen.
? t | The headteacher says the ban solved every problem. | F | The headteacher wouldn't claim that. | I wouldn't claim it solved everything

## Raising bilingual children | PF
Interviewer: Your children are growing up with Vietnamese at home and English at school. Any challenges?
Parent: Around age six, they started answering us in English, even when we spoke Vietnamese. It was easier for them.
Interviewer: What did you do?
Parent: We didn't force it, but we made Vietnamese fun: songs, cartoons, video calls with their grandparents. The grandparents were the real motivation. You can't talk to Grandma in English.
Interviewer: Was it worth the effort?
Parent: Absolutely. They switch between languages without thinking, and they understand two cultures from the inside.
? c | What happened around age six? | *The children started answering in English | They stopped speaking | They refused school | The parent explains. | they started answering us in English, even when we spoke Vietnamese.
? c | How did the parents respond? | *They made Vietnamese fun | They punished English | They changed schools | The parent explains. | we made Vietnamese fun
? c | What was the real motivation for the children? | *Talking to their grandparents | Passing exams | Watching films | The parent explains. | The grandparents were the real motivation.
? t | The parent thinks the effort was not worth it. | F | The parent says absolutely worth it. | Absolutely.

## A dispute over noise at work | WK
Mediator: You've both agreed to talk, which is a good start. Hoa, could you describe the problem?
Hoa: My desk is next to the sales team. They're on the phone all day, and I can't concentrate on financial reports.
Mediator: Duc, how do you see it?
Duc: Phone calls are our job. We can't do them silently. We've been asked to keep it down so often that the team feels criticised.
Mediator: So you both have a reasonable point. Would moving Hoa's desk be possible?
Duc: There's a free desk by the window, away from us.
Hoa: That would actually be better for both of us.
? c | Why can't Hoa concentrate? | *The sales team is on the phone all day | The office is cold | The computer is slow | Hoa explains. | They're on the phone all day, and I can't concentrate on financial reports.
? c | How does the sales team feel? | *Criticised | Ignored | Overworked | Duc explains. | the team feels criticised.
? c | What solution is found? | *Moving Hoa's desk near the window | Banning phone calls | Moving the sales team home | They agree on it. | There's a free desk by the window, away from us.
? t | The mediator thinks only Hoa has a reasonable point. | F | Both have a reasonable point. | So you both have a reasonable point.

## Learning to disagree well | CO
Trainer: In most teams, the problem isn't too much disagreement. It's too little. People stay quiet, and bad ideas go ahead.
Participant: But disagreeing with a manager feels risky.
Trainer: It can be. That's why the way you do it matters. Start with what you agree with, then ask a question rather than making a statement. For example, how would this work if the budget were cut?
Participant: Questions sound less like an attack.
Trainer: Exactly. And separate the idea from the person. You're criticising a plan, not the person who suggested it.
? c | What is the main problem in most teams, according to the trainer? | *Too little disagreement | Too much disagreement | Too many meetings | The trainer explains. | It's too little.
? c | How should you start when you disagree? | *With what you agree with | With a strong statement | With a complaint | The trainer advises. | Start with what you agree with
? c | Why are questions useful? | *They sound less like an attack | They are shorter | They avoid decisions | The participant and trainer agree. | Questions sound less like an attack.
? t | The trainer says you should criticise the person rather than the plan. | F | Criticise the plan, not the person. | You're criticising a plan, not the person who suggested it.
"""

LESSONS["C2"] = """
## A very brave presentation | CO
Mia: The director said my presentation was very brave. Was that a compliment?
Tom: Depends on the tone. In my experience, brave is what people say when they think you've taken a risk they wouldn't have taken themselves.
Mia: So, foolish but polite.
Tom: Not necessarily. Did she ask any questions afterwards?
Mia: Three, all about the budget.
Tom: Then she's taking it seriously. People don't interrogate the numbers of an idea they've already dismissed. I'd worry if she'd said it was interesting and moved on.
? c | What does Tom suggest brave often means? | *Someone took a risk the speaker wouldn't take | The work was excellent | The work was too long | Tom explains. | brave is what people say when they think you've taken a risk they wouldn't have taken themselves.
? c | Why does Tom think the director is taking the idea seriously? | *She asked detailed questions about the budget | She smiled | She praised the slides | Tom explains. | People don't interrogate the numbers of an idea they've already dismissed.
? c | Which reaction would worry Tom more? | *Calling it interesting and moving on | Asking about the budget | Asking for a second meeting | Tom says so. | I'd worry if she'd said it was interesting and moved on.
? t | Mia is sure the director meant it as a compliment. | F | Mia is unsure and asks Tom. | Was that a compliment?

## Do we choose freely? | ED
Lecturer: Neuroscience experiments have shown brain activity that predicts a simple choice, such as pressing a button, a fraction of a second before people report deciding.
Lecturer: Some have concluded that free will is an illusion. I'd urge caution. Pressing a button at a random moment is hardly the kind of decision we care about when we talk about responsibility.
Lecturer: Choosing a career or keeping a promise unfolds over days or years, involving reflection, revision and reasons. Whether such decisions are free is a philosophical question that a brief flicker of brain activity can't settle.
? c | What did the experiments show? | *Brain activity predicting a simple choice before people report deciding | People cannot press buttons | Choices take years | The lecturer explains. | brain activity that predicts a simple choice, such as pressing a button, a fraction of a second before people report deciding.
? c | What is the lecturer's attitude to the conclusion that free will is an illusion? | *Cautious and sceptical | Fully convinced | Uninterested | The lecturer urges caution. | I'd urge caution.
? c | Why does the lecturer doubt the experiments' relevance? | *Pressing a button is unlike decisions that matter for responsibility | The experiments were badly run | Too few people took part | The lecturer explains. | Pressing a button at a random moment is hardly the kind of decision we care about
? t | The lecturer believes brain scans have settled the question. | F | A brief flicker of brain activity can't settle it. | a brief flicker of brain activity can't settle.

## Declining a commission | WK
Client: We were hoping you'd design the new headquarters. The budget is generous.
Architect: I'm flattered, genuinely. Before I answer, may I ask about the site?
Client: It's the old riverside park. The council has agreed to sell it.
Architect: I see. I suspect you'll find architects better suited to this particular project than I am. My practice tends to work on sites where we're adding something to a neighbourhood rather than replacing what's there.
Client: Is that a no?
Architect: It's a no, with my respect for your ambition, and a list of three colleagues who'd do it beautifully.
? c | What does the architect ask about before answering? | *The site | The budget | The deadline | The architect asks. | may I ask about the site?
? c | What can we infer about the architect's reason? | *The architect objects to building on the park | The budget is too small | The architect is too busy | The architect prefers adding to neighbourhoods rather than replacing what's there. | rather than replacing what's there.
? t | The architect accepts the commission. | F | It's a no. | It's a no, with my respect for your ambition
? c | How does the architect soften the refusal? | *By recommending three colleagues | By offering a discount | By promising to reconsider | The architect explains. | a list of three colleagues who'd do it beautifully.

## Paying with attention | TE
Moderator: Is it fair to say we pay for free apps with our attention?
Panellist: It's more than fair; it's the business model. The product is designed to keep you scrolling because every extra minute can be sold to advertisers.
Moderator: Isn't that just advertising, as newspapers always did?
Panellist: Newspapers didn't adjust themselves to each reader in real time, testing which headline kept you from putting the paper down. The scale and precision are new, and so is the effect on how we feel.
Moderator: What would you change?
Panellist: Make the defaults gentler: no endless feeds, no autoplay, notifications off unless you ask for them.
? c | What does the panellist say about paying with attention? | *It is the business model | It is an exaggeration | It applies only to games | The panellist explains. | it's the business model.
? c | How does the panellist distinguish apps from newspapers? | *Apps adjust to each reader in real time | Newspapers had no adverts | Apps are free | The panellist explains. | Newspapers didn't adjust themselves to each reader in real time
? c | What change does the panellist propose? | *Gentler default settings | Banning advertising | Charging for all apps | The panellist explains. | Make the defaults gentler
? t | The panellist thinks only the scale is new, not the effects. | F | The effect on feelings is new too. | and so is the effect on how we feel.

## An ambitious novel | ED
Host: You've both read the new novel everyone's talking about. Verdict?
Critic A: It's certainly ambitious. Six narrators, three centuries, a great deal of research.
Host: That sounds like a polite way of saying something else.
Critic A: Let's say I admired it more than I enjoyed it. By the fourth narrator, I was checking how many pages were left.
Critic B: I'm less generous. Ambition isn't a virtue in itself. Every narrator sounds like the same well-read author doing voices.
Host: Any redeeming features?
Critic B: The final chapter is genuinely moving. It's a pity you need to cross four hundred pages to get there.
? c | What does Critic A really mean by certainly ambitious? | *Admiration without much enjoyment | Complete praise | Strong anger | Critic A explains. | I admired it more than I enjoyed it.
? c | What suggests Critic A was bored? | *Checking how many pages were left | Reading it twice | Recommending it | Critic A admits it. | I was checking how many pages were left.
? c | What is Critic B's main criticism? | *All the narrators sound the same | It is too short | It has too little research | Critic B explains. | Every narrator sounds like the same well-read author doing voices.
? t | Critic B finds nothing good in the book. | F | The final chapter is moving. | The final chapter is genuinely moving.

## Who is the neighbourhood for? | PT
Reporter: In ten years, this district has gone from cheap workshops to expensive cafés. Long-time residents have mixed feelings.
Resident: The streets are safer and cleaner, I'll grant you that. But my landlord doubled the rent, and half my neighbours have moved to the edge of the city.
Café owner: I understand the anger, but I didn't raise anyone's rent. I opened a business on an empty street.
Resident: Nobody blames you personally. The question is whether a neighbourhood that has improved for newcomers has improved at all, if the people who lived through the bad years can't stay to enjoy the good ones.
? c | What positive change does the resident admit? | *Safer and cleaner streets | Lower rents | More jobs for residents | The resident grants it. | The streets are safer and cleaner, I'll grant you that.
? c | How does the café owner defend themselves? | *They didn't raise anyone's rent | Residents are wrong | Rents fell | The café owner explains. | I didn't raise anyone's rent.
? c | What is the resident's central question? | *Whether improvement counts if original residents can't stay | Whether cafés are too expensive | Whether streets should be closed | The resident explains. | The question is whether a neighbourhood that has improved for newcomers has improved at all
? t | The resident blames the café owner personally. | F | Nobody blames them personally. | Nobody blames you personally.

## The placebo puzzle | HE
Presenter: Placebos are sugar pills, yet they sometimes reduce pain. How?
Researcher: Expectation seems to trigger the brain's own pain relief. The ritual matters too: a confident doctor, a pill with a brand name, even the price.
Presenter: The price?
Researcher: In one study, people told a pill was expensive reported more relief than those told it was cheap, though both were identical.
Presenter: Remarkably, some placebos work even when patients know they're placebos.
Researcher: For some conditions, yes, which suggests the ritual of treatment, not just deception, does part of the work. That said, a placebo won't shrink a tumour. Its effects are mainly on how symptoms are experienced.
? c | What seems to trigger relief from a placebo? | *Expectation | Sugar | Exercise | The researcher explains. | Expectation seems to trigger the brain's own pain relief.
? c | What did the study about price find? | *An expensive-seeming pill brought more reported relief | Cheap pills worked better | Price made no difference | The researcher explains. | people told a pill was expensive reported more relief than those told it was cheap
? c | What does the effect of known placebos suggest? | *The ritual of treatment does part of the work | Patients are lying | Placebos are real drugs | The researcher explains. | the ritual of treatment, not just deception, does part of the work.
? t | The researcher says placebos can shrink tumours. | F | A placebo won't shrink a tumour. | a placebo won't shrink a tumour.

## An answer without an answer | CO
Interviewer: Minister, will the new tax affect families on middle incomes, yes or no?
Minister: What I can tell you is that this government has always been committed to supporting working families, and the package as a whole is designed with fairness at its heart.
Interviewer: That's not what I asked. Will a family earning an average wage pay more?
Minister: Some families may see changes in one area offset by support elsewhere. It would be irresponsible to speculate before the full details are published.
Interviewer: So some will pay more.
Minister: I've said what I can say.
? c | What does the interviewer want? | *A clear yes or no about middle-income families | Details of the minister's career | The date of the election | The interviewer asks. | will the new tax affect families on middle incomes, yes or no?
? c | How does the minister respond? | *By avoiding a direct answer | By saying no clearly | By saying yes clearly | The minister talks about commitment and fairness instead. | the package as a whole is designed with fairness at its heart.
? c | What does the minister's second answer imply? | *Some families may pay more in one area | Nobody will pay more | Taxes will fall for everyone | The minister mentions changes offset elsewhere. | Some families may see changes in one area offset by support elsewhere.
? t | The minister finally gives a clear yes. | F | The minister refuses to say more. | I've said what I can say.

## Green on the label | EN
Presenter: Products are increasingly described as eco-friendly or natural. How much should we trust those words?
Analyst: Very little, on their own. Neither has a legal definition in many places. A company can call a bottle eco-friendly because the cap uses slightly less plastic.
Presenter: What about carbon neutral?
Analyst: Often that means the company keeps emitting but pays for projects elsewhere, such as planting trees. Some are sound, some are dubious, and trees can burn.
Presenter: So what should consumers look for?
Analyst: Specific, checkable claims, like the percentage of recycled material, ideally verified by an independent body. Vague virtue is cheap.
? c | Why should we distrust eco-friendly on its own? | *It often has no legal definition | It is always false | It is too technical | The analyst explains. | Neither has a legal definition in many places.
? c | What does carbon neutral often mean? | *Paying for projects elsewhere while still emitting | Producing no emissions at all | Using only solar power | The analyst explains. | the company keeps emitting but pays for projects elsewhere
? c | What should consumers look for? | *Specific, checkable claims verified independently | Green packaging | Famous brands | The analyst advises. | Specific, checkable claims
? t | The analyst implies that vague claims cost companies little. | T | Vague virtue is cheap. | Vague virtue is cheap.

## Zoos as arks? | AN
Moderator: Modern zoos describe themselves as arks, saving species from extinction. Is that convincing?
Conservationist: For a handful of species, absolutely. Some animals survive today only because zoos bred them and returned them to the wild.
Critic: A handful is the key word. Most animals in zoos aren't endangered at all, and they're there because visitors want to see them.
Conservationist: Visitors pay for the breeding programmes.
Critic: Then be honest about the bargain. Call it what it is: entertainment that funds some conservation, rather than conservation that happens to entertain.
? c | What does the conservationist claim? | *Some species survive only because of zoo breeding | All zoo animals are endangered | Zoos should close | The conservationist explains. | Some animals survive today only because zoos bred them and returned them to the wild.
? c | What is the critic's main point? | *Most zoo animals are not endangered | Zoos breed too many animals | Visitors pay too much | The critic explains. | Most animals in zoos aren't endangered at all
? c | How does the critic want zoos to describe themselves? | *As entertainment that funds some conservation | As pure conservation | As museums | The critic explains. | entertainment that funds some conservation, rather than conservation that happens to entertain.
? t | The conservationist argues that visitors fund breeding programmes. | T | The conservationist says so. | Visitors pay for the breeding programmes.

## The trouble with merit | WK
Author: We like to believe that success reflects talent and hard work. Partly it does. But the belief has a side effect.
Interviewer: Which is?
Author: If success is earned, then failure must be deserved. People at the top feel entitled, and those at the bottom feel humiliated, even when luck, family and timing played a large part.
Interviewer: Are you against merit, then?
Author: Not at all. I'd rather a surgeon be chosen for skill than connections. I'm against forgetting how much good fortune shapes who gets to develop their skills in the first place.
? c | What side effect of believing in merit does the author describe? | *Failure is seen as deserved | Success becomes impossible | People stop working | The author explains. | If success is earned, then failure must be deserved.
? c | How might people at the top feel? | *Entitled | Humiliated | Guilty | The author explains. | People at the top feel entitled
? t | The author opposes choosing surgeons by skill. | F | The author prefers skill to connections. | I'd rather a surgeon be chosen for skill than connections.
? c | What is the author really against? | *Forgetting the role of good fortune | Hard work | Competition | The author explains. | I'm against forgetting how much good fortune shapes who gets to develop their skills

## Selling the past | SH
Presenter: Why are so many adverts full of old songs and childhood memories?
Marketer: Because nostalgia lowers our guard. When people feel warmly about the past, they're more willing to spend. It's one of the oldest tricks there is.
Presenter: You sound almost critical of your own industry.
Marketer: Let's say I'm clear-eyed about it. The products being sold rarely have anything to do with the memories being used to sell them. A bank uses a song from your teenage years, and suddenly a mortgage feels like a summer holiday.
Presenter: Is that dishonest?
Marketer: It's not lying. It's borrowing an emotion that isn't the product's to give.
? c | Why do adverts use nostalgia, according to the marketer? | *It lowers our guard and makes us spend | It is cheaper | It is required by law | The marketer explains. | nostalgia lowers our guard.
? c | How does the marketer describe their own attitude? | *Clear-eyed | Proud | Angry | The marketer says so. | Let's say I'm clear-eyed about it.
? c | What does the bank example illustrate? | *Products often have nothing to do with the memories used | Banks are honest | Songs make mortgages cheaper | The marketer explains. | The products being sold rarely have anything to do with the memories being used to sell them.
? t | The marketer says nostalgic adverts are lies. | F | It's not lying but borrowing an emotion. | It's not lying.

## The power of silence | WK
Negotiator: The most underused tool in negotiation is silence.
Interviewer: Why is it so effective?
Negotiator: Most people find a pause uncomfortable, so they fill it, often by making a concession nobody asked for. If someone names a price and you simply wait, they frequently improve the offer themselves.
Interviewer: Doesn't that feel manipulative?
Negotiator: It can be, if used as a trick. But silence also has an honest purpose: it gives both sides time to think. The best agreements rarely come from whoever talks fastest.
? c | Why is silence effective? | *People fill pauses, often with concessions | It makes people angry | It ends the negotiation | The negotiator explains. | Most people find a pause uncomfortable, so they fill it, often by making a concession nobody asked for.
? c | What often happens if you wait after a price is named? | *The other side improves the offer | The other side leaves | The price rises | The negotiator explains. | they frequently improve the offer themselves.
? t | The negotiator admits silence can be used manipulatively. | T | It can be, if used as a trick. | It can be, if used as a trick.
? c | What honest purpose does silence have? | *Giving both sides time to think | Saving time | Hiding information | The negotiator explains. | it gives both sides time to think.

## The expert witness | CO
Lawyer: Doctor, can you say with certainty that the injury was caused by the fall?
Expert: With certainty, no. I can say it is consistent with a fall from that height.
Lawyer: Consistent with. Could it also be consistent with something else?
Expert: It could, in principle. However, the pattern of fractures is what I would expect from a fall, and I've seen nothing that points elsewhere.
Lawyer: So you can't rule out other explanations.
Expert: In medicine, one can rarely rule anything out completely. What I can say is that the fall is by far the most likely explanation on the evidence available.
? c | What does consistent with mean in the expert's answer? | *It fits a fall without proving it | It definitely proves a fall | It rules out a fall | The expert refuses certainty. | With certainty, no.
? c | What supports the fall explanation? | *The pattern of fractures | A witness | A video | The expert explains. | the pattern of fractures is what I would expect from a fall
? c | What is the lawyer trying to do? | *Suggest other explanations are possible | Prove there was a fall | Praise the expert | The lawyer presses the point. | So you can't rule out other explanations.
? t | The expert says the fall is the most likely explanation. | T | The expert says so. | the fall is by far the most likely explanation on the evidence available.

## Slow news | TE
Editor: We publish fewer stories than any other news site, and we publish them late, sometimes weeks after the event.
Interviewer: Isn't late news simply old news?
Editor: It depends what news is for. If it's for knowing what happened in the last ten minutes, we're useless. If it's for understanding why it happened, the first reports are often wrong, and waiting lets us get it right.
Interviewer: Do readers really pay for that?
Editor: Enough of them. Our members say they're tired of feeling anxious and uninformed at the same time.
? c | What is unusual about the editor's publication? | *It publishes fewer stories and publishes them late | It has no website | It only covers sport | The editor explains. | We publish fewer stories than any other news site, and we publish them late
? c | What purpose of news does the editor value? | *Understanding why things happened | Knowing what happened ten minutes ago | Entertainment | The editor explains. | If it's for understanding why it happened
? c | Why can waiting help? | *First reports are often wrong | Readers are busy | Writers are slow | The editor explains. | the first reports are often wrong, and waiting lets us get it right.
? t | Members say constant news makes them feel both anxious and uninformed. | T | The editor reports this. | they're tired of feeling anxious and uninformed at the same time.

## Should inheritance be taxed more? | MS
Moderator: Should large inheritances be taxed more heavily?
Economist: I'd say yes. Inheritance is the purest form of unearned wealth. The heir did nothing to earn it, and large inheritances entrench advantage across generations.
Opponent: But the person who earned it already paid tax on it. Taxing it again when they die punishes them for wanting to help their children.
Economist: The tax falls on the heir, not the dead. And I'm talking about very large estates, not the family home.
Opponent: Wealthy families simply move their money abroad.
Economist: Some do, which is an argument for international cooperation, not for giving up.
? c | Why does the economist favour higher inheritance tax? | *Inheritance is unearned and entrenches advantage | It is easy to collect | It funds schools only | The economist explains. | Inheritance is the purest form of unearned wealth.
? c | What is the opponent's first objection? | *The money was already taxed | Heirs are poor | It is too complicated | The opponent explains. | the person who earned it already paid tax on it.
? c | What does the economist clarify? | *The proposal concerns very large estates, not family homes | All estates should be taxed equally | Only homes should be taxed | The economist clarifies. | I'm talking about very large estates, not the family home.
? t | The economist thinks people moving money abroad is a reason to give up. | F | It is a reason for international cooperation. | which is an argument for international cooperation, not for giving up.

## Measured to death | WK
Speaker: A hospital wanted to reduce waiting times in its emergency department, so it set a target: every patient seen within four hours.
Speaker: Waiting times fell, on paper. In practice, some patients were moved to corridors labelled as assessment areas, so the clock stopped without anyone being treated faster.
Speaker: This is the classic problem with targets. When a measure becomes a goal, people find ways to hit the number rather than achieve the purpose behind it.
Speaker: Measurement is essential. The danger is forgetting that the number is a sign of what we care about, not the thing itself.
? c | What target did the hospital set? | *Every patient seen within four hours | Fewer staff | More beds | The speaker explains. | every patient seen within four hours.
? c | How was the target met on paper? | *Patients were moved to areas relabelled for assessment | More doctors were hired | Patients were sent home | The speaker explains. | some patients were moved to corridors labelled as assessment areas
? c | What is the classic problem with targets? | *People hit the number rather than achieve the purpose | Targets are too easy | Nobody measures them | The speaker explains. | people find ways to hit the number rather than achieve the purpose behind it.
? t | The speaker argues that measurement should be abandoned. | F | Measurement is essential. | Measurement is essential.

## The authentic dish | FD
Chef: People often ask me whether my pho is authentic.
Interviewer: Is it?
Chef: It depends what you mean. The dish itself has changed constantly. The version many people now call traditional was shaped by migration, war and whatever ingredients were available.
Interviewer: So authenticity is a myth?
Chef: Not quite. I'd say a dish is authentic when it's made with care and knowledge of where it comes from, not when it's frozen at a particular moment in history. My grandmother adapted recipes all the time. Nobody accused her of being inauthentic.
? c | What does the chef say about the dish's history? | *It has changed constantly | It has never changed | It was invented recently | The chef explains. | The dish itself has changed constantly.
? c | What shaped the version called traditional? | *Migration, war and available ingredients | Restaurant critics | Government rules | The chef explains. | shaped by migration, war and whatever ingredients were available.
? c | How does the chef define authenticity? | *Care and knowledge of origins, not a fixed moment | Using only old recipes | Using expensive ingredients | The chef explains. | a dish is authentic when it's made with care and knowledge of where it comes from
? t | The chef says authenticity is a complete myth. | F | Not quite. | Not quite.

## The final concert | HS
Interviewer: After forty years, this is your final season as a conductor. How does it feel?
Conductor: Rather like reaching the last page of a book you've enjoyed. You slow down a little, to make it last.
Interviewer: Any regrets?
Conductor: A few recordings I'd rather people didn't hear. I was young and in a hurry.
Interviewer: And advice for young conductors?
Conductor: Listen to the orchestra more than you speak to it. Musicians usually know what the music needs. The conductor's job is often to remove obstacles, not to impose ideas.
? b | The conductor has worked for ____ years. | forty / 40 | The interviewer says so. | After forty years
? c | How does the conductor describe the feeling? | *Like reaching the last page of an enjoyable book | Like starting a new job | Like being relieved | The conductor explains. | Rather like reaching the last page of a book you've enjoyed.
? c | What does the conductor regret? | *Some recordings made when young | Choosing music as a career | Leaving too early | The conductor explains. | A few recordings I'd rather people didn't hear.
? t | The conductor sees the job mainly as imposing ideas. | F | The job is often to remove obstacles. | The conductor's job is often to remove obstacles, not to impose ideas.

## The wolves return | AN
Reporter: Wolves have returned to parts of the countryside after more than a century. Not everyone is pleased.
Farmer: I've lost six sheep this year. Compensation arrives months later, and it doesn't cover the stress.
Ecologist: The losses are real, and farmers deserve faster support. But wolves also control deer numbers, which allows young trees to grow again.
Farmer: Trees don't pay my bills.
Ecologist: No, which is why protection has to include practical help: guard dogs, electric fencing and payment within weeks, not months.
? c | What does the farmer complain about? | *Lost sheep and slow compensation | Too many trees | Noise from tourists | The farmer explains. | I've lost six sheep this year. Compensation arrives months later
? c | What benefit of wolves does the ecologist mention? | *They control deer, letting young trees grow | They attract tourists | They eat rats | The ecologist explains. | wolves also control deer numbers, which allows young trees to grow again.
? t | The ecologist dismisses the farmer's losses. | F | The losses are real. | The losses are real
? c | What practical help does the ecologist propose? | *Guard dogs, electric fencing and faster payment | Removing the wolves | Moving farms | The ecologist explains. | guard dogs, electric fencing and payment within weeks, not months.

## What a city remembers | PT
Historian: Cities remember selectively. Street names, statues and plaques tell us which stories a society chose to keep.
Historian: What's absent can be just as revealing. In many cities, the people who actually built the bridges and railways appear nowhere, while the men who financed them have squares named after them.
Historian: I'm not arguing that we should rename everything. But a walk through a city is a lesson in power, and it's worth asking who wrote the lesson.
? c | According to the historian, what do street names and statues reveal? | *Which stories a society chose to keep | How old a city is | Where to find shops | The historian explains. | tell us which stories a society chose to keep.
? c | Who is often missing from public memory? | *The people who built bridges and railways | The people who financed them | Kings and queens | The historian explains. | the people who actually built the bridges and railways appear nowhere
? t | The historian wants to rename everything. | F | That is not the argument. | I'm not arguing that we should rename everything.
? c | What does the historian suggest we ask? | *Who wrote the lesson | Who lives there now | How much it cost | The historian suggests it. | it's worth asking who wrote the lesson.

## Learning from a near miss | TR
Pilot: In aviation, we report our own mistakes, even when nothing went wrong.
Interviewer: Why would you report something that didn't cause harm?
Pilot: Because a near miss is a free lesson. If two of us nearly made the same error, there's probably a flaw in the system, perhaps a confusing switch or a badly worded checklist.
Interviewer: Aren't people afraid of being punished?
Pilot: That's exactly why reports are protected. If honest mistakes were punished, people would hide them, and the next time the luck might run out.
? c | What do pilots report? | *Their own mistakes, even without harm | Only accidents | Other pilots' mistakes | The pilot explains. | we report our own mistakes, even when nothing went wrong.
? c | Why is a near miss valuable? | *It reveals flaws without causing harm | It saves fuel | It shortens flights | The pilot explains. | a near miss is a free lesson.
? c | Why are reports protected? | *Otherwise people would hide mistakes | To save money | To protect airlines' reputations | The pilot explains. | If honest mistakes were punished, people would hide them
? t | The pilot thinks repeated near misses point to a problem in the system. | T | There's probably a flaw in the system. | there's probably a flaw in the system

## The confidence of forecasts | MS
Presenter: Economic forecasts are often wrong. Why do we keep listening to them?
Economist: Because uncertainty is uncomfortable, and a precise number feels reassuring, even when it shouldn't.
Presenter: Should forecasters stop giving numbers?
Economist: I'd rather they gave ranges and were honest about how wide they are. Growth of two percent sounds authoritative. Growth somewhere between minus one and five percent is truer, though it makes a poorer headline.
Presenter: And the public?
Economist: Treat a confident forecast with the same suspicion you'd give a confident weather forecast for a month from now.
? c | Why do people keep listening to forecasts? | *Precise numbers feel reassuring | Forecasts are always right | They are required to | The economist explains. | a precise number feels reassuring, even when it shouldn't.
? c | What does the economist prefer forecasters to give? | *Honest ranges | Single exact numbers | No information | The economist explains. | I'd rather they gave ranges and were honest about how wide they are.
? c | Why is a range less popular? | *It makes a poorer headline | It is harder to calculate | It is always wrong | The economist explains. | though it makes a poorer headline.
? t | The economist compares confident forecasts to long-range weather forecasts. | T | The economist makes this comparison. | the same suspicion you'd give a confident weather forecast for a month from now.
"""

LESSONS["C2"] += """
## Busy as a badge | DL
Sociologist: Ask someone how they are, and the answer is often busy, said with a certain pride.
Interviewer: Why pride?
Sociologist: In the past, leisure signalled status: the wealthy didn't need to work. Now, being in demand signals that you're valuable. Busyness has become a way of saying I matter.
Interviewer: Is that harmful?
Sociologist: It can be. If being busy is admirable, then rest looks like laziness, and people feel guilty for doing nothing, which is precisely when the mind recovers and some of our best ideas arrive.
? c | How do people often answer how they are? | *Busy, with some pride | Tired, with embarrassment | Happy, without detail | The sociologist explains. | the answer is often busy, said with a certain pride.
? c | What signalled status in the past? | *Leisure | Long working hours | Large families | The sociologist explains. | In the past, leisure signalled status
? c | What does busyness signal today? | *That you are valuable and in demand | That you are poor | That you are lazy | The sociologist explains. | being in demand signals that you're valuable.
? t | The sociologist suggests rest is unproductive. | F | Rest is when the mind recovers. | which is precisely when the mind recovers

## A gentle push | HE
Presenter: Governments increasingly use nudges: small changes in how choices are presented. For example, making organ donation the default unless you opt out.
Philosopher: Nudges can be effective and cheap. My concern is transparency. A nudge works best when people don't notice it, which sits uneasily with the idea of free citizens making informed choices.
Presenter: But nobody is forced to do anything.
Philosopher: True, and that's their appeal. I'd simply insist that nudges be public and open to debate. If a government wouldn't be comfortable explaining a nudge openly, it probably shouldn't use it.
? c | What is a nudge? | *A small change in how choices are presented | A new law | A tax | The presenter explains. | small changes in how choices are presented.
? c | What concerns the philosopher? | *Transparency | Cost | Effectiveness | The philosopher explains. | My concern is transparency.
? c | Why is transparency an issue? | *Nudges work best when people don't notice them | Nudges are expensive | Nudges are illegal | The philosopher explains. | A nudge works best when people don't notice it
? t | The philosopher proposes a test based on whether a nudge could be explained openly. | T | The philosopher suggests this test. | If a government wouldn't be comfortable explaining a nudge openly, it probably shouldn't use it.

## Jokes that don't travel | CO
Interviewer: What's the hardest thing to translate in a comedy film?
Subtitler: Wordplay, without question. If a joke depends on a word having two meanings in English, there's rarely a word in the target language that does the same.
Interviewer: So what do you do?
Subtitler: Sometimes I replace the joke with a different one that works locally, at the same moment, with a similar tone. Purists hate it. But a joke that nobody laughs at has been translated accurately and still failed.
Interviewer: Is there anything you refuse to change?
Subtitler: Anything that tells you about the character. If a joke reveals cruelty or insecurity, that has to survive, even if the laugh doesn't.
? c | What does the subtitler find hardest to translate? | *Wordplay | Names | Numbers | The subtitler explains. | Wordplay, without question.
? c | What does the subtitler sometimes do? | *Replace the joke with one that works locally | Leave it untranslated | Add a long explanation | The subtitler explains. | Sometimes I replace the joke with a different one that works locally
? c | What is the subtitler's view of accurate but unfunny translation? | *It has still failed | It is ideal | It is rare | The subtitler explains. | a joke that nobody laughs at has been translated accurately and still failed.
? t | The subtitler will sacrifice what a joke reveals about a character to keep the laugh. | F | Character must survive, even if the laugh doesn't. | that has to survive, even if the laugh doesn't.

## The last bookshop on the street | SH
Owner: When I opened, there were four bookshops on this street. Now there's one.
Interviewer: How have you survived?
Owner: By accepting that I can't compete on price. The online giants will always be cheaper. So I compete on what they can't offer: someone who has actually read the books.
Interviewer: Does that pay the rent?
Owner: Barely, some months. We host readings and a children's story hour, and people buy a book partly to keep the place alive.
Interviewer: Is that sustainable?
Owner: Ask me in five years. But I've noticed that people who say they love bookshops are increasingly willing to prove it.
? c | How many bookshops were on the street originally? | *Four | Two | One | The owner says so. | there were four bookshops on this street.
? c | What does the owner compete on? | *Personal knowledge of the books | Lower prices | Faster delivery | The owner explains. | someone who has actually read the books.
? c | Why do some customers buy books there, according to the owner? | *Partly to keep the shop alive | Because prices are lowest | Because of free coffee | The owner explains. | people buy a book partly to keep the place alive.
? t | The owner is certain the shop will survive. | F | The owner says ask again in five years. | Ask me in five years.

## The return to the office | WK
Executive: We've asked staff to return to the office four days a week. Productivity, collaboration, culture.
Employee: With respect, our productivity rose while we worked from home. That's in the company's own figures.
Executive: Individual productivity, perhaps. But new staff learn by overhearing, and ideas come from unplanned conversations.
Employee: Then why not design office days around that, with teams in together on the same days, rather than a flat rule that has us commuting to sit on video calls?
Executive: That's a fair point, and frankly one I haven't heard put so clearly before.
? c | How many days must staff return? | *Four days a week | Two days a week | Every day | The executive says so. | four days a week.
? c | What evidence does the employee cite? | *Company figures showing productivity rose at home | A survey of other firms | Customer complaints | The employee explains. | our productivity rose while we worked from home. That's in the company's own figures.
? c | What does the executive say new staff need? | *To learn by overhearing and unplanned conversations | More training videos | Higher pay | The executive explains. | new staff learn by overhearing, and ideas come from unplanned conversations.
? t | The executive dismisses the employee's suggestion. | F | The executive calls it a fair point. | That's a fair point

## Science by volunteers | EN
Scientist: Every spring, thousands of volunteers count birds in their gardens and send us the results.
Interviewer: Can data from amateurs really be trusted?
Scientist: Individually, there are errors: a sparrow mistaken for something else. But with tens of thousands of counts, the errors largely cancel out, and the patterns become clear.
Interviewer: What have you learned?
Scientist: That some common birds are declining faster than anyone realised, in time for something to be done. No research team could cover a whole country every year. Volunteers can.
? c | What do volunteers do? | *Count birds in their gardens | Ring birds | Feed birds in parks | The scientist explains. | thousands of volunteers count birds in their gardens
? c | Why can the data be trusted overall? | *With many counts, errors largely cancel out | Volunteers never make mistakes | Experts check every count | The scientist explains. | with tens of thousands of counts, the errors largely cancel out
? c | What has been learned? | *Some common birds are declining faster than realised | Rare birds are increasing | Bird numbers are stable | The scientist explains. | some common birds are declining faster than anyone realised
? t | The scientist suggests professional teams could easily cover the whole country. | F | No research team could. | No research team could cover a whole country every year.

## What the eulogy left out | PF
Ana: It was a beautiful speech. Generous, loyal, devoted to his family.
Ben: All true. Though I noticed nobody mentioned his temper.
Ana: Funerals aren't the place for that.
Ben: I'm not saying they should be. I just wonder whether we do the dead a favour by smoothing them into saints. He was difficult, and he was loved anyway. That seems the more remarkable thing.
Ana: Maybe the people who knew him heard both, even if only one was said aloud.
? c | What did the eulogy praise? | *Generosity, loyalty and devotion to family | His career | His temper | Ana lists them. | Generous, loyal, devoted to his family.
? c | What did Ben notice was missing? | *Any mention of his temper | His name | His children | Ben says so. | nobody mentioned his temper.
? c | What does Ben find more remarkable? | *That he was loved despite being difficult | That he was a saint | That the speech was long | Ben explains. | He was difficult, and he was loved anyway.
? t | Ben thinks funerals should list people's faults. | F | Ben says he is not saying that. | I'm not saying they should be.

## Mining the deep sea | EN
Presenter: Companies want to mine the deep sea floor for metals used in batteries. Supporters say it's essential for clean energy.
Marine biologist: The demand is real. But we know less about the deep sea floor than about the surface of the moon. Many species there have never been described, and they grow and recover extremely slowly.
Presenter: So you'd ban it?
Marine biologist: I'd pause it. Once a habitat that took thousands of years to form is destroyed, the damage is, in human terms, permanent. Better recycling and battery designs that need fewer of these metals should come first.
? c | Why do companies want to mine the deep sea? | *For metals used in batteries | For oil | For fish | The presenter explains. | to mine the deep sea floor for metals used in batteries.
? c | What does the biologist say about our knowledge of the deep sea floor? | *We know less about it than the moon's surface | We know it well | It has no life | The biologist explains. | we know less about the deep sea floor than about the surface of the moon.
? c | What does the biologist recommend? | *A pause | A permanent ban | Immediate mining | The biologist says so. | I'd pause it.
? t | The biologist says the demand for metals is imaginary. | F | The demand is real. | The demand is real.

## Against productivity | WK
Writer: We've turned everything into productivity, even rest. People optimise their sleep so they can work better and schedule hobbies as if they were meetings.
Interviewer: Isn't it good to use time well?
Writer: Of course. My objection is to the idea that time is only well used if it produces something. A walk with no destination, a conversation that leads nowhere in particular: these aren't failures of efficiency. They're much of what makes life worth living.
Interviewer: Some would call that a luxury.
Writer: For people working two jobs, it is, and that's an argument about wages, not about whether rest has value.
? c | What does the writer object to? | *The idea that time is well used only if it produces something | Using time well | Sleeping | The writer explains. | My objection is to the idea that time is only well used if it produces something.
? c | Which example does the writer give of valuable time? | *A walk with no destination | A productive meeting | Answering emails | The writer gives examples. | A walk with no destination
? c | How does the writer respond to the luxury criticism? | *It concerns wages, not the value of rest | Rest is only for the rich | Everyone has enough time | The writer explains. | that's an argument about wages, not about whether rest has value.
? t | The writer says people even schedule hobbies like meetings. | T | The writer says so. | schedule hobbies as if they were meetings.

## The charm of leaders | WK
Interviewer: How much does charisma matter in leadership?
Researcher: In hiring, a great deal. Confident, charming candidates are consistently rated more highly, even when their results are no better.
Interviewer: And in practice?
Researcher: The evidence is less flattering. Charismatic leaders are good at inspiring people in a crisis, but some are poor at listening and surround themselves with admirers. The quieter qualities, such as humility and consistency, predict long-term success at least as well.
Interviewer: So should we distrust charisma?
Researcher: Not distrust. Discount it. Ask what the person has actually done, not how they made you feel in the interview.
? c | How does charisma affect hiring? | *Charming candidates are rated more highly | It has no effect | It makes candidates rated lower | The researcher explains. | Confident, charming candidates are consistently rated more highly
? c | What weakness do some charismatic leaders have? | *They are poor at listening | They avoid crises | They are too humble | The researcher explains. | some are poor at listening and surround themselves with admirers.
? c | What qualities predict long-term success as well? | *Humility and consistency | Confidence and charm | Speed and ambition | The researcher explains. | The quieter qualities, such as humility and consistency
? t | The researcher advises distrusting charisma completely. | F | Not distrust, discount it. | Not distrust. Discount it.

## Bringing a language back | ED
Linguist: Every few weeks, a language loses its last fluent speaker. But some languages have been revived from very few speakers.
Interviewer: How?
Linguist: Usually through children. Language nests, where young children spend the day with elders who speak only the language, have been remarkably successful.
Interviewer: Why children rather than adult classes?
Linguist: Adults can learn, and should. But a language survives when it becomes the language a child dreams in, argues in and eventually speaks to their own children. Classes alone rarely achieve that.
? c | How often does a language lose its last fluent speaker? | *Every few weeks | Every year | Every century | The linguist explains. | Every few weeks, a language loses its last fluent speaker.
? c | What are language nests? | *Places where young children spend the day with elders speaking only the language | Online courses | Libraries for old books | The linguist explains. | where young children spend the day with elders who speak only the language
? c | When does a language survive, according to the linguist? | *When children use it in all of life and pass it on | When adults take classes | When it is written down | The linguist explains. | a language survives when it becomes the language a child dreams in
? t | The linguist says adults cannot learn the language. | F | Adults can learn, and should. | Adults can learn, and should.

## Meat from a laboratory | FD
Presenter: Meat grown from animal cells, without raising animals, is now approved for sale in a few places. Is this the future?
Food scientist: Possibly part of it. It could greatly reduce land use and animal suffering. But the energy needed to grow cells at scale is considerable, and if that energy isn't clean, the climate benefit shrinks.
Presenter: And taste?
Food scientist: Minced products are convincing. A whole steak, with fat and texture, is far harder to grow.
Presenter: Will people eat it?
Food scientist: Many say they won't. People said the same about many foods now considered ordinary.
? c | What could lab-grown meat reduce? | *Land use and animal suffering | The price of vegetables | Water in rivers | The scientist explains. | It could greatly reduce land use and animal suffering.
? c | What could limit the climate benefit? | *Energy that isn't clean | Too much land | Too many animals | The scientist explains. | if that energy isn't clean, the climate benefit shrinks.
? c | Which products are already convincing? | *Minced products | Whole steaks | Seafood | The scientist explains. | Minced products are convincing.
? t | The scientist suggests initial refusal may not last. | T | People said the same about foods now ordinary. | People said the same about many foods now considered ordinary.

## Leaving home for good | PF
Interviewer: You emigrated thirty years ago. Do you still feel you left home, or did you find a new one?
Writer: Both, and neither. When I go back, the country I remember no longer exists. My friends have changed, the streets have changed, even the slang has moved on without me.
Interviewer: And where you live now?
Writer: I'm at home, but I still notice I'm noticing. A local person never wonders why the post office closes at five. I still do, a little.
Interviewer: Is that sad?
Writer: Less than you'd think. Being slightly outside everything is useful for a writer.
? b | The writer emigrated ____ years ago. | thirty / 30 | The interviewer says so. | You emigrated thirty years ago.
? c | What has happened to the country the writer remembers? | *It no longer exists in that form | It is exactly the same | The writer never visits | The writer explains. | the country I remember no longer exists.
? c | What does I still notice I'm noticing suggest? | *The writer still sees the place partly as an outsider | The writer is lost | The writer dislikes the post office | The writer explains. | A local person never wonders why the post office closes at five.
? t | The writer finds the situation deeply sad. | F | Less than you'd think; it is useful. | Less than you'd think.

## The doping question | HS
Presenter: Every few years another doping scandal hits sport. Some argue we should simply allow performance-enhancing drugs.
Ethicist: The argument is that it would level the playing field. But it would also force every athlete, including teenagers, to take health risks just to compete.
Presenter: Isn't that already happening informally?
Ethicist: In some sports, sadly. But making it legal would turn a hidden pressure into an official requirement. Testing is imperfect, but an imperfect rule still protects athletes who want to compete clean.
? c | What argument for allowing drugs is mentioned? | *It would level the playing field | It would be cheaper | It would make sport shorter | The ethicist explains. | it would level the playing field.
? c | What problem does the ethicist see with legalising drugs? | *Every athlete would have to take health risks | Matches would be boring | Tickets would cost more | The ethicist explains. | it would also force every athlete, including teenagers, to take health risks
? c | What would legalisation turn the hidden pressure into? | *An official requirement | A minor issue | A crime | The ethicist explains. | would turn a hidden pressure into an official requirement.
? t | The ethicist believes imperfect testing still has value. | T | It protects clean athletes. | an imperfect rule still protects athletes who want to compete clean.

## A machine that hires | TE
Reporter: A growing number of companies use software to screen job applications. One firm found its system was rejecting more women.
Data scientist: The software had learned from ten years of past hiring decisions, and those decisions favoured men. The machine didn't invent the bias. It copied it efficiently.
Reporter: Couldn't they just remove gender from the data?
Data scientist: They tried. But the system found proxies, like certain sports or women's colleges listed on CVs. Bias in data is hard to remove by deleting one column.
Reporter: So should we avoid such software?
Data scientist: Use it cautiously, audit it regularly, and never let it make final decisions alone.
? c | What problem did the firm find? | *Its system rejected more women | It was too slow | It hired too many people | The reporter explains. | its system was rejecting more women.
? c | Where did the bias come from? | *Past hiring decisions the software learned from | The programmers' intentions | A virus | The data scientist explains. | The software had learned from ten years of past hiring decisions
? c | Why didn't removing gender solve it? | *The system found proxies on CVs | The data was deleted | The software crashed | The data scientist explains. | the system found proxies
? t | The data scientist recommends letting the software make final decisions. | F | Never alone. | never let it make final decisions alone.

## The unfinished painting | ED
Curator: This is one of the most visited rooms in the gallery, and every painting in it is unfinished.
Visitor: Why would people prefer unfinished work?
Curator: Partly curiosity: you can see how the artist worked, the lines they changed, the decisions still being made. And partly because the viewer completes it. An unfinished face invites you to imagine the rest.
Visitor: Did the artists want them shown?
Curator: That's the uncomfortable question. Some would surely be horrified. We show them because they teach us something, but we try to be honest on the labels about what the artist intended.
? c | What is special about the room? | *Every painting is unfinished | It has the oldest paintings | It is closed to visitors | The curator explains. | every painting in it is unfinished.
? c | What does unfinished work reveal? | *How the artist worked | The price of paintings | The artist's age | The curator explains. | you can see how the artist worked
? c | What does the curator mean by the viewer completes it? | *The viewer imagines the missing parts | The viewer paints on it | The viewer buys it | The curator explains. | An unfinished face invites you to imagine the rest.
? t | The curator is sure all the artists would approve of the display. | F | Some would surely be horrified. | Some would surely be horrified.

## The selfie at the waterfall | TR
Guide: This waterfall became famous because of one photograph that was shared millions of times.
Tourist: It's beautiful, but I didn't expect the queue.
Guide: Most visitors now come for that single spot. They wait an hour, take the photo and leave without walking the trail.
Tourist: Isn't that their choice?
Guide: Of course. But the path to the viewpoint has eroded badly, and the village sees little benefit because people don't stay. We're now limiting numbers at the viewpoint and encouraging visitors to walk the whole valley.
? c | Why did the waterfall become famous? | *A photograph shared millions of times | A film | A festival | The guide explains. | one photograph that was shared millions of times.
? c | What do most visitors do? | *Take one photo and leave | Walk the whole trail | Stay in the village | The guide explains. | take the photo and leave without walking the trail.
? c | What problem has this caused? | *Erosion and little benefit for the village | Too many hotels | Water pollution | The guide explains. | the path to the viewpoint has eroded badly, and the village sees little benefit
? t | The guide thinks visitors have no right to choose. | F | The guide says of course it's their choice. | Of course.

## Anxious about the climate | HE
Psychologist: More young people tell me they feel anxious, even hopeless, about climate change.
Interviewer: Is that anxiety irrational?
Psychologist: Not at all. It's a reasonable response to a real threat. The problem arises when it becomes paralysing.
Interviewer: What helps?
Psychologist: Action, mostly. People who join a local project, however small, tend to feel less helpless than those who only read the news. And talking about it openly, rather than being told not to worry, which only makes people feel unheard.
? c | What do many young people report? | *Anxiety about climate change | Boredom | Anger at teachers | The psychologist explains. | More young people tell me they feel anxious, even hopeless, about climate change.
? c | How does the psychologist view the anxiety? | *As a reasonable response to a real threat | As irrational | As a phase | The psychologist explains. | It's a reasonable response to a real threat.
? c | What tends to reduce helplessness? | *Joining a local project | Reading more news | Avoiding the topic | The psychologist explains. | People who join a local project, however small, tend to feel less helpless
? t | The psychologist recommends telling people not to worry. | F | That makes people feel unheard. | rather than being told not to worry, which only makes people feel unheard.

## Regretfully, we cannot attend | PF
Lan: I need to reply to my cousin's wedding invitation. We can't go.
Huy: Just say you're busy.
Lan: That sounds as if we have better things to do. I want to decline without suggesting we don't care.
Huy: Then say you're sorry to miss such a special day, that you'll be thinking of them, and offer to take them to dinner when they're back from their honeymoon.
Lan: That's much better. And I won't go into the reason. Explaining too much always sounds like an excuse.
? c | Why doesn't Lan want to say they're busy? | *It sounds as if they have better things to do | It isn't true | Huy said it last time | Lan explains. | That sounds as if we have better things to do.
? c | What does Huy suggest offering? | *Dinner after the honeymoon | A large gift | A phone call during the wedding | Huy suggests it. | offer to take them to dinner when they're back from their honeymoon.
? c | Why won't Lan explain the reason? | *Explaining too much sounds like an excuse | The reason is secret | The cousin already knows | Lan explains. | Explaining too much always sounds like an excuse.
? t | Lan wants to decline without seeming not to care. | T | Lan says so. | I want to decline without suggesting we don't care.

## Where satire stops | CO
Host: Satire mocks the powerful. But where are its limits?
Comedian: My rule is to punch up, not down. Mocking a president is satire. Mocking someone because they're poor or ill is just cruelty dressed as comedy.
Host: Some say comedy shouldn't have rules at all.
Comedian: Comedy has always had rules. They just used to be the audience's rules rather than the comedian's. If nobody laughs, you've broken one.
Host: And when you get it wrong?
Comedian: You say so. The worst comedians are the ones who mistake every complaint for censorship.
? c | What is the comedian's rule? | *Punch up, not down | Never mock anyone | Mock everyone equally | The comedian explains. | My rule is to punch up, not down.
? c | What does the comedian call mocking the poor or ill? | *Cruelty dressed as comedy | Brave satire | Harmless fun | The comedian explains. | just cruelty dressed as comedy.
? c | According to the comedian, whose rules did comedy follow before? | *The audience's | The government's | Nobody's | The comedian explains. | They just used to be the audience's rules rather than the comedian's.
? t | The comedian thinks every complaint is censorship. | F | The comedian criticises comedians who think so. | The worst comedians are the ones who mistake every complaint for censorship.

## Housing and the generations | HF
Economist: In many cities, people over sixty own a large share of homes, often with spare bedrooms, while younger people struggle to rent a single room.
Interviewer: Should older people be pushed to downsize?
Economist: Pushed, no. Many are attached to their homes, and moving is costly and stressful. But we could make it easier: smaller homes in the same neighbourhood, help with moving, lower taxes on the sale.
Interviewer: Is it only about older owners?
Economist: Not at all. The deeper problem is that we haven't built enough homes for decades. Blaming one generation is easier than fixing planning rules.
? c | What imbalance does the economist describe? | *Older people own many homes with spare rooms while younger people struggle | Young people own most homes | Homes are empty everywhere | The economist explains. | people over sixty own a large share of homes, often with spare bedrooms
? c | What does the economist think about pushing older people to downsize? | *They should not be pushed, but it could be made easier | They should be forced | It is impossible | The economist explains. | Pushed, no.
? c | What is the deeper problem? | *Too few homes have been built for decades | Older people are selfish | Rents are too low | The economist explains. | The deeper problem is that we haven't built enough homes for decades.
? t | The economist blames one generation for the problem. | F | Blaming one generation is easier than fixing planning. | Blaming one generation is easier than fixing planning rules.

## When experts disagree | ED
Student: If the experts disagree, how am I supposed to know who's right?
Professor: First, check whether they really disagree, or whether they're answering slightly different questions. Often it's the second.
Student: And if they truly disagree?
Professor: Look at the strength of the evidence each relies on, not the confidence of the speaker. And notice whether someone's position could ever change. A good expert can tell you what evidence would change their mind.
Student: And if nobody can?
Professor: Then hold your view lightly. Being unsure is not the same as being ignorant.
? c | What should you check first? | *Whether they are answering different questions | Who is more famous | Who spoke first | The professor advises. | check whether they really disagree, or whether they're answering slightly different questions.
? c | What should you focus on when experts truly disagree? | *The strength of the evidence | The confidence of the speaker | The number of followers | The professor advises. | Look at the strength of the evidence each relies on, not the confidence of the speaker.
? c | What can a good expert tell you? | *What evidence would change their mind | Exactly what will happen | Who is wrong | The professor explains. | A good expert can tell you what evidence would change their mind.
? t | The professor equates being unsure with being ignorant. | F | They are not the same. | Being unsure is not the same as being ignorant.

## Can happiness be measured? | MS
Presenter: Some governments now measure national wellbeing alongside economic growth. Is happiness really measurable?
Statistician: Imperfectly. We ask people how satisfied they are with their lives on a scale from nought to ten. It sounds crude, but the answers are surprisingly consistent and relate to things you'd expect, like health and relationships.
Presenter: What do the figures show?
Statistician: Beyond a certain income, extra money adds less and less to life satisfaction, while loneliness and long commutes take away a great deal.
Presenter: Should that change policy?
Statistician: It should at least change the questions politicians ask.
? c | How is life satisfaction measured? | *On a scale from nought to ten | By income | By hours worked | The statistician explains. | on a scale from nought to ten.
? c | What does the statistician say about the answers? | *They are surprisingly consistent | They are random | They are always high | The statistician explains. | the answers are surprisingly consistent
? c | What do the figures show about money? | *Beyond a certain income, extra money adds less | More money always means more happiness | Money has no effect | The statistician explains. | Beyond a certain income, extra money adds less and less to life satisfaction
? t | Loneliness and long commutes reduce life satisfaction a great deal. | T | The statistician says so. | loneliness and long commutes take away a great deal.
"""


def parse(level, block, first_id):
    lessons, n = [], first_id
    for chunk in filter(None, (c.strip() for c in block.strip().split("## "))):
        head, *rows = [r.strip() for r in chunk.splitlines() if r.strip()]
        title, topic = (part.strip() for part in head.split(" | "))
        lines, questions = [], []
        for row in rows:
            if row.startswith("? "):
                kind, prompt, *rest = (part.strip() for part in row[2:].split(" | "))
                explanation, evidence = rest[-2], rest[-1]
                q = {"id": f"l{n}q{len(questions) + 1}", "prompt": prompt, "explanation": explanation,
                     "evidence": evidence}
                if kind == "c":
                    options = [o.lstrip("*") for o in rest[:-2]]
                    answers = [o.lstrip("*") for o in rest[:-2] if o.startswith("*")]
                    assert len(answers) == 1 and len(set(options)) == len(options) >= 3, (title, prompt)
                    q.update(type="choice", options=options, answers=answers)
                elif kind == "b":
                    assert "____" in prompt, (title, prompt)
                    q.update(type="blank", answers=[a.strip() for a in rest[0].split(" / ")])
                else:
                    q.update(type="tfng", answers=[TFNG[rest[0]]])
                questions.append(q)
            else:
                speaker, text = row.split(": ", 1)
                lines.append({"speaker": speaker, "text": text})
        script = " ".join(line["text"] for line in lines)
        for q in questions:
            assert q["evidence"] in script, (title, q["evidence"])
        assert 4 <= len(questions) <= 5 and lines, title
        lessons.append({"id": f"l{n}", "title": title, "level": level, "topic": TOPICS[topic],
                        "lines": lines, "questions": [{k: q[k] for k in
                        ("id", "type", "prompt", "options", "answers", "explanation", "evidence") if k in q}
                        for q in questions]})
        n += 1
    return lessons


def main():
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "listening.json"
    out = [l for l in json.loads(path.read_text(encoding="utf-8")) if int(l["id"][1:]) <= 24]
    for level, block in LESSONS.items():
        out += parse(level, block, len(out) + 1)
    titles = [l["title"].lower() for l in out]
    assert len(set(titles)) == len(titles), sorted({t for t in titles if titles.count(t) > 1})
    counts = {lv: sum(1 for l in out if l["level"] == lv) for lv in LEVELS}
    for level in LESSONS:
        assert counts[level] == 50, counts
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "lessons", counts)


main()

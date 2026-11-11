"""Writes src/data/reading.json: the six earlier passages (r1-r6) plus passages written for EnglishUp
on 2026-11-11 so that every level from A1 to C2 has 50 reading lessons.

Format, one passage after another:
    ## Title | topic code
    Paragraph text (blank lines separate paragraphs)
    ? c | question | *right option | other option | ... | explanation | evidence
    ? s | question | accepted answer / another accepted answer | explanation | evidence
    ? t | statement | T, F or N (True, False, Not Given) | explanation | evidence
Each passage has 150-350 words and exactly five questions, and every evidence must be an exact
part of the passage; the script refuses a passage otherwise. Run: python scripts/create-reading-passages.py
"""
import json
import pathlib
import re

TOPICS = {
    "DL": "Daily life", "TR": "Travel", "WK": "Work", "FD": "Food", "HE": "Health", "TE": "Technology",
    "EN": "Environment", "ED": "Education", "SH": "Shopping", "CO": "Communication", "PF": "People and family",
    "HS": "Hobbies and sport", "TP": "Transport", "NW": "Nature and weather", "HF": "Home and furniture",
    "PT": "Places in town", "MS": "Money and shopping", "AN": "Animals",
}
TFNG = {"T": "True", "F": "False", "N": "Not Given"}
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

PASSAGES = {}

PASSAGES["A1"] = """
## My new neighbours | PF
A new family moved into the house next to mine last week. Their name is Tran. There is a father, a mother and a little girl. The girl's name is An, and she is seven years old.

On Saturday, I went to their house with my mother. We took a cake and some flowers. Mrs. Tran was very happy. She made tea for us, and we sat in the garden. Their garden is small, but it has many flowers and a big mango tree.

An showed me her room. It is pink, and there are many books on the shelves. She likes animals, and she has a small brown rabbit. Its name is Coco. An says Coco eats carrots and apples every day.

Next week, An is going to start at my school. I am going to walk with her in the morning, because she does not know the way yet. I think we will be good friends.
? c | How old is An? | *Seven | Six | Eight | The passage gives her age. | she is seven years old.
? t | The narrator visited the Tran family on Sunday. | F | The visit was on Saturday. | On Saturday, I went to their house with my mother.
? s | What is the name of An's rabbit? | Coco | The rabbit's name is in the third paragraph. | Its name is Coco.
? t | There is a mango tree in the Trans' garden. | T | The garden has a big mango tree. | it has many flowers and a big mango tree.
? c | Why will the narrator walk with An? | *She does not know the way yet | She is afraid of dogs | Her mother is busy | The last paragraph explains. | because she does not know the way yet.

## A day at the zoo | AN
Last Sunday, my family went to the city zoo. We went by bus, and the trip took forty minutes. The zoo opens at eight o'clock, and we arrived at nine.

First, we saw the elephants. There are three elephants at the zoo: a mother, a father and a baby. The baby elephant was very funny. It played with water and made everyone laugh. Then we saw the monkeys. They jumped from tree to tree and ate bananas.

At twelve o'clock, we had lunch near the lake. My mother made rice, chicken and vegetables. After lunch, my little brother wanted to see the lions. The lions were sleeping in the sun, so we did not see them move.

In the afternoon, we visited the bird house. There were many beautiful birds with red, green and yellow feathers. My favourite was a big blue parrot. It could say "hello"!

We went home at four o'clock. We were tired, but we were very happy.
? s | How long did the bus trip take? | forty minutes / 40 minutes / forty / 40 | The first paragraph gives the time. | the trip took forty minutes.
? c | How many elephants are there at the zoo? | *Three | Two | Four | The passage counts them. | There are three elephants at the zoo
? t | The lions were very active. | F | They were sleeping. | The lions were sleeping in the sun
? c | What was the narrator's favourite bird? | *A big blue parrot | A small red bird | A yellow duck | The narrator says so. | My favourite was a big blue parrot.
? t | The family had lunch near the lake. | T | The third paragraph says so. | we had lunch near the lake.

## The school canteen | ED
My school has a big canteen. It is on the ground floor, next to the sports hall. More than three hundred students eat there every day.

Lunch starts at half past eleven. We stand in a line and take a tray. Every day there is rice, soup and two kinds of meat or fish. There is also a vegetarian dish for students who do not eat meat. On Fridays, there is fruit or yoghurt for dessert.

Lunch is not expensive. It costs one dollar fifty. Some students bring food from home, and they can eat in the canteen too.

The canteen is clean, but it is very noisy. Everybody talks and laughs at the same time. My friends and I always sit at the table near the window, because it is a little quieter there.

After lunch, we put our trays on a table near the kitchen. Then we have thirty minutes to play outside before afternoon classes start.
? c | Where is the canteen? | *Next to the sports hall | Next to the library | On the top floor | The first paragraph says where. | It is on the ground floor, next to the sports hall.
? s | What time does lunch start? | half past eleven / 11:30 / eleven thirty | The second paragraph gives the time. | Lunch starts at half past eleven.
? t | There is dessert every day. | F | Dessert is on Fridays. | On Fridays, there is fruit or yoghurt for dessert.
? t | Students who bring food from home can eat in the canteen. | T | The passage says they can. | they can eat in the canteen too.
? c | Why do the narrator and friends sit near the window? | *It is a little quieter | It is warmer | The food is better there | The passage explains. | because it is a little quieter there.

## A letter from my pen friend | CO
Dear Linh,

Thank you for your letter and the photos of Ha Long Bay. It looks beautiful!

My name is Emma, and I live in a small town in the north of England. I am twelve years old. I have one brother. His name is Jack, and he is fifteen. We have a dog called Max.

My town is quiet. There is a river, a park and a small castle. Many tourists come to see the castle in the summer. In winter, it is very cold here, and sometimes it snows.

At school, my favourite subject is art. I love drawing animals. I do not like maths very much, because it is difficult for me. After school, I play the piano or go swimming with my friends.

What do you do at the weekend? What is the weather like in Viet Nam now? Please write soon and send more photos.

Your friend,
Emma
? c | Where does Emma live? | *In a small town in England | In a big city in England | In Ha Long Bay | Emma describes her home. | I live in a small town in the north of England.
? s | How old is Emma's brother? | fifteen / 15 | Emma gives his age. | he is fifteen.
? t | Many tourists visit the castle in winter. | F | They come in the summer. | Many tourists come to see the castle in the summer.
? c | What is Emma's favourite subject? | *Art | Maths | Music | Emma says so. | my favourite subject is art.
? t | Emma has a cat. | F | Emma has a dog called Max. | We have a dog called Max.

## The shop on our street | SH
There is a small shop at the end of our street. It belongs to Mr. and Mrs. Hoang. They opened it twenty years ago, and they still work there every day.

The shop sells many things. You can buy bread, milk, eggs, rice and fruit. There are also pens, notebooks and small toys for children. In the summer, they sell ice cream, and it is very popular.

The shop opens at six o'clock in the morning and closes at ten o'clock at night. Mr. Hoang works in the morning, and Mrs. Hoang works in the afternoon and evening. On Sundays, their son helps them.

I go to the shop almost every day. Sometimes my mother sends me to buy bread for breakfast. Mrs. Hoang always smiles and asks about my school.

There is a big supermarket in the town centre now, but many people on our street still like the small shop. It is near, it is friendly, and you never wait long.
? s | How many years ago did the Hoangs open the shop? | twenty / 20 / twenty years / 20 years | The first paragraph says so. | They opened it twenty years ago
? c | What is very popular in the summer? | *Ice cream | Bread | Toys | The second paragraph says so. | they sell ice cream, and it is very popular.
? c | Who helps on Sundays? | *Their son | Their daughter | The narrator | The third paragraph explains. | On Sundays, their son helps them.
? t | The shop closes at nine o'clock at night. | F | It closes at ten o'clock. | closes at ten o'clock at night.
? t | The narrator's mother sometimes sends the narrator to buy bread. | T | The fourth paragraph says so. | Sometimes my mother sends me to buy bread for breakfast.

## Sunday at the beach | TR
Every summer, my family goes to the beach on the first Sunday of July. The beach is one hour from our house by car.

This year, we left home at seven o'clock in the morning. My father drove, and my mother sat next to him. My sister and I sat in the back and sang songs.

The weather was sunny and hot. The sea was blue and warm. My sister and I swam for a long time, and my father built a big sandcastle with us. My mother read a book under a big umbrella.

For lunch, we ate at a small restaurant near the beach. We had fresh fish, rice and a salad. The fish was delicious. After lunch, we were tired, so we slept under the umbrella for an hour.

In the late afternoon, we walked along the beach and looked for shells. I found a big white shell, and now it is on my desk at home.

We drove home at six o'clock. It was a perfect day.
? c | When does the family go to the beach? | *On the first Sunday of July | Every weekend | In August | The first paragraph says so. | on the first Sunday of July.
? s | How long does it take to drive to the beach? | one hour / an hour / 1 hour | The first paragraph gives the time. | The beach is one hour from our house by car.
? t | The narrator's mother swam all day. | F | She read a book under an umbrella. | My mother read a book under a big umbrella.
? c | What did they eat for lunch? | *Fresh fish, rice and a salad | Chicken and noodles | Sandwiches | The fourth paragraph describes lunch. | We had fresh fish, rice and a salad.
? t | The narrator keeps the shell on a desk at home. | T | The fifth paragraph says so. | now it is on my desk at home.

## The town library | PT
Our town library is in an old building in the centre of town. It is open from Tuesday to Saturday, from nine in the morning to six in the evening. It is closed on Sundays and Mondays.

The library is free for everyone. To borrow books, you need a library card. The card is free too. You can borrow six books for three weeks.

On the ground floor, there are books for adults, newspapers and computers. On the first floor, there is a big room for children. It has colourful chairs, picture books and games. Every Saturday at ten o'clock, a librarian reads stories to young children.

There is also a quiet room for students. Many students study there after school, because it is calm and there is free internet.

I go to the library every Saturday with my little brother. He listens to the stories, and I choose new books. My favourite books are adventure stories.
? c | When is the library closed? | *On Sundays and Mondays | On Saturdays | Every afternoon | The first paragraph says so. | It is closed on Sundays and Mondays.
? s | How many books can you borrow? | six / 6 / six books | The second paragraph says so. | You can borrow six books for three weeks.
? t | You must pay for a library card. | F | The card is free. | The card is free too.
? c | What happens every Saturday at ten o'clock? | *A librarian reads stories to children | The library closes | Students take tests | The third paragraph says so. | Every Saturday at ten o'clock, a librarian reads stories to young children.
? t | The narrator likes adventure stories best. | T | The last paragraph says so. | My favourite books are adventure stories.

## A rainy day at home | NW
It rained all day on Saturday, so my family stayed at home. In the morning, it was dark and cold, and we could not go to the park.

My mother said, "Let's cook something together." We made pancakes for breakfast. My little sister put too much sugar on hers, and we all laughed.

After breakfast, my father found an old box of photos. We sat on the floor and looked at them. There were photos of my parents when they were young. My father had long hair, and my mother wore big glasses. They looked very different!

In the afternoon, my sister and I played a board game. I won the first game, and she won the second. Then we watched a film about a family of bears.

In the evening, the rain stopped. We opened the window, and the air smelled fresh and clean. I was surprised, because it was a very nice day, even with the rain.
? c | Why did the family stay at home? | *It rained all day | They were ill | The park was closed | The first paragraph explains. | It rained all day on Saturday, so my family stayed at home.
? s | What did they make for breakfast? | pancakes | The second paragraph says so. | We made pancakes for breakfast.
? t | In old photos, the narrator's father had short hair. | F | He had long hair. | My father had long hair
? c | Who won the second board game? | *The narrator's sister | The narrator | The father | The fourth paragraph says so. | she won the second.
? t | The rain stopped in the evening. | T | The last paragraph says so. | In the evening, the rain stopped.

## My cat Mimi | AN
I have a cat. Her name is Mimi, and she is four years old. She is grey and white, and she has big green eyes.

Mimi sleeps a lot. She sleeps on my bed at night, and in the day she sleeps on the sofa or near the window, in the sun. My mother says Mimi sleeps sixteen hours a day!

Every morning, I give Mimi her breakfast before I go to school. She eats cat food and drinks water. She does not like milk. In the evening, she eats again at six o'clock.

Mimi likes playing with a small ball and a piece of string. She runs after the ball and jumps very high. She does not like dogs, and she hides under the bed when our neighbour's dog barks.

When I come home from school, Mimi always waits for me at the door. I think she is happy to see me. She is my best friend at home.
? s | How old is Mimi? | four / 4 / four years old | The first paragraph gives her age. | she is four years old.
? c | What colour are Mimi's eyes? | *Green | Blue | Brown | The first paragraph describes her. | she has big green eyes.
? t | Mimi likes milk. | F | She does not like milk. | She does not like milk.
? c | What does Mimi do when the neighbour's dog barks? | *Hides under the bed | Runs outside | Barks back | The fourth paragraph explains. | she hides under the bed when our neighbour's dog barks.
? t | Mimi waits at the door when the narrator comes home. | T | The last paragraph says so. | Mimi always waits for me at the door.

## A visit to the doctor | HE
Last Tuesday, I did not feel well. I had a sore throat and a headache, and I was very hot. My mother took me to the doctor in the afternoon.

The doctor's office is near the market. We waited for twenty minutes, and then a nurse called my name. The doctor was a kind woman with grey hair. She looked at my throat and listened to my chest.

"You have a cold and a small fever," she said. "You need to rest at home for three days. Drink a lot of water and warm tea with honey."

She gave my mother some medicine for me. I took it three times a day, after meals. I did not go to school on Wednesday, Thursday or Friday. I stayed in bed and read books.

On Saturday, I felt much better. My throat did not hurt, and I was not hot. On Monday, I went back to school and saw my friends again.
? c | What was wrong with the narrator? | *A sore throat, a headache and a fever | A broken arm | A stomach ache | The first paragraph describes it. | I had a sore throat and a headache, and I was very hot.
? s | How long did they wait at the doctor's office? | twenty minutes / 20 minutes / twenty / 20 | The second paragraph says so. | We waited for twenty minutes
? t | The doctor was a young man. | F | She was a woman with grey hair. | The doctor was a kind woman with grey hair.
? c | How many days did the narrator rest at home? | *Three | Two | Five | The doctor says so. | You need to rest at home for three days.
? t | The narrator felt better on Saturday. | T | The last paragraph says so. | On Saturday, I felt much better.

## Minh's birthday party | PF
Yesterday was my friend Minh's birthday. He is now eleven years old. His parents had a party for him at their house.

Ten children came to the party. We played games in the garden. My favourite game was a race with eggs on spoons. I dropped my egg, but it was fun!

At four o'clock, Minh's mother brought a big chocolate cake with eleven candles. We sang "Happy Birthday", and Minh blew out the candles. Then we ate the cake. It was delicious.

Minh got many presents. His parents gave him a new bike. His grandmother gave him a book about dinosaurs. I gave him a football, because he loves football. He said it was his favourite present, and he wanted to play with it right away.

At the end of the party, Minh's father took photos of all the children. Then our parents came to take us home. It was a great party, and I want a party like that for my birthday too.
? s | How old is Minh now? | eleven / 11 | The first paragraph says so. | He is now eleven years old.
? c | How many children came to the party? | *Ten | Eleven | Twenty | The second paragraph says so. | Ten children came to the party.
? t | The narrator won the egg race. | N | The narrator dropped the egg, but the passage does not say who won. | I dropped my egg, but it was fun!
? c | What did the narrator give Minh? | *A football | A book about dinosaurs | A new bike | The fourth paragraph says so. | I gave him a football, because he loves football.
? t | Minh's father took photos of the children. | T | The last paragraph says so. | Minh's father took photos of all the children.

## Our football team | HS
I play in a football team at my school. There are fourteen players in the team, and we are all eleven or twelve years old. Our coach is Mr. Lam. He is a PE teacher.

We practise two times a week, on Tuesday and Thursday after school. Practice starts at half past four and finishes at six. First we run around the field, and then we practise passing and shooting. At the end, we play a short match.

On Saturdays, we sometimes play against other schools. Last Saturday, we played against Green Hill School. It was a difficult match, but we won two goals to one. I scored the first goal!

Mr. Lam says the most important thing is to work as a team. He says we must help each other and never get angry with a teammate.

After the match, our parents bought us ice cream. I was very tired, but very happy.
? s | How many players are in the team? | fourteen / 14 | The first paragraph says so. | There are fourteen players in the team
? c | When does the team practise? | *Tuesday and Thursday after school | Every day | Saturday morning | The second paragraph says so. | on Tuesday and Thursday after school.
? c | What was the score against Green Hill School? | *Two goals to one | One goal to one | Three goals to two | The third paragraph says so. | we won two goals to one.
? t | The narrator scored the second goal. | F | The narrator scored the first goal. | I scored the first goal!
? t | Mr. Lam teaches PE. | T | The first paragraph says so. | He is a PE teacher.

## A new bike | TP
For my twelfth birthday, my parents gave me a new bike. It is red and black, and it has a bell and a small basket at the front.

Before, I walked to school every day. It took twenty-five minutes. Now I ride my bike, and it only takes ten minutes. I leave home later and I can sleep a little longer in the morning!

My father taught me some rules. I must always wear a helmet. I must ride on the right side of the road, and I must stop at red lights. At night, I must turn on the lights on my bike.

On Sundays, I ride with my father to the lake. It is about five kilometres from our house. We ride around the lake, and then we have a drink at a small café.

I take care of my bike. Every week, I clean it, and I check the tyres. I want to keep it for a long time.
? c | What is at the front of the bike? | *A small basket | A big box | A light only | The first paragraph describes the bike. | it has a bell and a small basket at the front.
? s | How long does the ride to school take? | ten minutes / 10 minutes / ten / 10 | The second paragraph says so. | it only takes ten minutes.
? t | The narrator does not need a helmet. | F | The narrator must always wear a helmet. | I must always wear a helmet.
? c | How far is the lake from the house? | *About five kilometres | About ten kilometres | One kilometre | The fourth paragraph says so. | It is about five kilometres from our house.
? t | The narrator cleans the bike every week. | T | The last paragraph says so. | Every week, I clean it

## The night market | SH
Every Friday and Saturday evening, there is a night market in the centre of our town. It opens at six o'clock and closes at eleven.

The market is in a long street. There are more than one hundred stalls. Some stalls sell clothes, bags and shoes. Other stalls sell toys, phone cases and souvenirs for tourists. The prices are cheap, and you can ask for a lower price.

The best part of the market is the food. There are stalls with grilled meat, noodle soup, spring rolls and sweet cakes. There are also fruit drinks in many colours. My favourite is mango juice.

The market is always busy, and there is music in the street. Many tourists visit it, and many local families come too. Children love the small games, where you can win a toy.

Last Friday, I went to the market with my cousin. We ate spring rolls and drank mango juice. I bought a blue phone case. It was a great evening.
? c | When is the night market open? | *Every Friday and Saturday evening | Every evening | Only on Sundays | The first paragraph says so. | Every Friday and Saturday evening
? s | What time does the market close? | eleven / 11 / eleven o'clock / 11 pm | The first paragraph says so. | It opens at six o'clock and closes at eleven.
? t | You cannot ask for a lower price at the market. | F | You can ask for a lower price. | you can ask for a lower price.
? c | What is the narrator's favourite drink? | *Mango juice | Orange juice | Coconut water | The third paragraph says so. | My favourite is mango juice.
? t | The narrator bought a bag. | F | The narrator bought a blue phone case. | I bought a blue phone case.

## Visiting the city | TR
Last month, I visited Ha Noi with my parents for three days. It was my first time in a big city.

On the first day, we walked around Hoan Kiem Lake. There were many people walking and doing exercise. We saw a small red bridge and an old temple on the lake.

On the second day, we visited a museum. It had old clothes, tools and photos. I learned a lot about the history of the city. In the afternoon, we drank egg coffee in a small café. It was sweet and creamy, and I loved it.

On the third day, we went shopping in the Old Quarter. The streets were narrow and very busy, with a lot of motorbikes. Each street sold different things, like shoes, silk or paper.

The city was noisy, but it was very interesting. I want to go back one day and see more places.
? s | How many days was the visit? | three / 3 / three days | The first paragraph says so. | for three days.
? c | What did they see on the lake? | *A small red bridge and an old temple | A big ship | A swimming pool | The second paragraph describes it. | We saw a small red bridge and an old temple on the lake.
? c | What did the narrator drink in the café? | *Egg coffee | Green tea | Orange juice | The third paragraph says so. | we drank egg coffee in a small café.
? t | The streets in the Old Quarter were wide and quiet. | F | They were narrow and very busy. | The streets were narrow and very busy
? t | The narrator wants to visit the city again. | T | The last paragraph says so. | I want to go back one day

## Learning to swim | HS
When I was eight, I could not swim. I was afraid of the water. My mother said, "Everybody needs to learn to swim. It is important." So she took me to swimming lessons at the sports centre.

The lessons were on Saturday mornings at nine o'clock. My teacher was a young man called Huy. He was very patient. In the first lesson, we only played in the small pool. The water was not deep, and I could stand up.

Every week, I learned something new. First, I learned to put my face in the water. Then I learned to kick my legs. After two months, I could swim across the small pool.

After six months, I could swim in the big pool. I was so happy! Now I am eleven, and I love swimming. I go to the pool every week with my friends.

I am not afraid of water now. I want to learn to swim in the sea next summer.
? s | How old was the narrator then? | eight / 8 | The first paragraph says so. | When I was eight, I could not swim.
? c | When were the lessons? | *Saturday mornings at nine o'clock | Sunday afternoons | Every evening | The second paragraph says so. | The lessons were on Saturday mornings at nine o'clock.
? t | In the first lesson, the narrator swam in the big pool. | F | They played in the small pool. | In the first lesson, we only played in the small pool.
? c | After how long could the narrator swim in the big pool? | *Six months | Two months | One year | The fourth paragraph says so. | After six months, I could swim in the big pool.
? t | The narrator wants to swim in the sea next summer. | T | The last paragraph says so. | I want to learn to swim in the sea next summer.

## The school bus | TP
I go to school by school bus every day. The bus stops at the corner of my street at a quarter past seven. If I am late, I must walk, and it takes forty minutes!

The bus is yellow and big. It has forty seats. The driver is Mr. Phong. He is friendly, and he always says good morning to the children. He drives slowly and carefully.

There are many rules on the bus. We must sit down and wear a seat belt. We must not eat or drink. We must not shout. A teacher sits at the front and helps the younger children.

The trip takes twenty minutes. I always sit with my friend Lan. We talk about our homework or our favourite songs. Sometimes we read together.

In the afternoon, the bus takes us home at half past four. I like the school bus, because it is safe and I can see my friends.
? s | What time does the bus stop at the corner? | a quarter past seven / 7:15 / quarter past seven | The first paragraph says so. | at a quarter past seven.
? c | How many seats does the bus have? | *Forty | Twenty | Fifty | The second paragraph says so. | It has forty seats.
? t | Students can eat on the bus. | F | They must not eat or drink. | We must not eat or drink.
? c | Who sits at the front to help? | *A teacher | The narrator | A parent | The third paragraph says so. | A teacher sits at the front and helps the younger children.
? t | The narrator always sits with Lan. | T | The fourth paragraph says so. | I always sit with my friend Lan.

## Our English teacher | ED
Our English teacher is Ms. Hoa. She is about thirty years old, and she has short black hair and glasses. She is from Hue, but she studied in Australia for two years.

Ms. Hoa's lessons are never boring. She uses songs, games and videos. Every Monday, we learn a new English song. My favourite song is about the weather.

She always speaks English in class, but she speaks slowly and uses her hands to help us understand. When we make a mistake, she smiles and helps us. She says mistakes are a normal part of learning.

Every Friday, we have a short test with ten words. If we get all ten words right, we get a star. When we have five stars, we can choose a book from the class library.

I like Ms. Hoa very much. Before, English was difficult for me. Now it is my favourite subject, and I want to visit an English-speaking country one day.
? c | Where did Ms. Hoa study for two years? | *In Australia | In England | In Hue | The first paragraph says so. | she studied in Australia for two years.
? c | What do students learn every Monday? | *A new English song | Ten new words | A poem | The second paragraph says so. | Every Monday, we learn a new English song.
? t | Ms. Hoa gets angry when students make mistakes. | F | She smiles and helps. | When we make a mistake, she smiles and helps us.
? s | How many stars do students need to choose a book? | five / 5 / five stars | The fourth paragraph says so. | When we have five stars, we can choose a book
? t | English is now the narrator's favourite subject. | T | The last paragraph says so. | Now it is my favourite subject

## A family picnic | PF
On Sunday, my family had a picnic in the park near our house. The weather was warm and sunny, with a few small clouds.

We left home at ten o'clock. My father carried a big blanket, and my mother carried a basket with food. My brother and I carried a ball and some drinks.

We found a nice place under a big tree, near a small pond. We put the blanket on the grass. In the basket, there were sandwiches, boiled eggs, fruit and a cake. My grandmother made the cake. It was a banana cake, and it was very sweet.

After lunch, my brother and I played football. My parents sat on the blanket and talked. Later, we fed bread to the ducks in the pond. A man told us that bread is not good for ducks, so we stopped.

At three o'clock, it started to get cloudy, so we went home. It was a lovely day together.
? s | What time did they leave home? | ten / 10 / ten o'clock / 10 am | The second paragraph says so. | We left home at ten o'clock.
? c | Where did they sit? | *Under a big tree near a pond | Next to the road | On a bench | The third paragraph says so. | We found a nice place under a big tree, near a small pond.
? c | Who made the cake? | *The grandmother | The mother | The father | The third paragraph says so. | My grandmother made the cake.
? t | They kept feeding bread to the ducks all afternoon. | F | They stopped after a man spoke to them. | so we stopped.
? t | It got cloudy at three o'clock. | T | The last paragraph says so. | At three o'clock, it started to get cloudy

## At the hotel | TR
Welcome to the Sea View Hotel! We hope you enjoy your stay. Here is some information for our guests.

Breakfast is in the restaurant on the ground floor. It is from half past six to ten o'clock every morning. There is bread, eggs, noodles, fruit, coffee and tea.

The swimming pool is on the roof. It is open from seven in the morning to eight in the evening. Please wear a swimming cap in the pool. Children under ten must be with an adult.

There is free Wi-Fi in all rooms. The password is on the card in your room. If you need help, call reception by pressing nine on your room phone. Reception is open twenty-four hours a day.

Check-out time is twelve o'clock. If you want to leave your bags after check-out, you can leave them at reception for free.

We have bicycles for guests. You can borrow one for free for three hours. Please ask at reception.
? c | Where is the swimming pool? | *On the roof | On the ground floor | Next to the restaurant | The third paragraph says so. | The swimming pool is on the roof.
? s | What number do you press to call reception? | nine / 9 | The fourth paragraph says so. | call reception by pressing nine on your room phone.
? t | Children under ten can use the pool alone. | F | They must be with an adult. | Children under ten must be with an adult.
? c | What time is check-out? | *Twelve o'clock | Ten o'clock | Two o'clock | The fifth paragraph says so. | Check-out time is twelve o'clock.
? t | Guests must pay to borrow a bicycle. | F | They can borrow one for free. | You can borrow one for free for three hours.

## My bedroom | HF
My bedroom is small, but I love it. It is on the second floor of our house, and it has one big window. From the window, I can see the street and a tall tree.

The walls are light blue, and the floor is wooden. My bed is next to the window. On the bed, there is a blue blanket and two pillows. Under the bed, I keep my shoes and a box of old toys.

Next to the bed, there is a small table with a lamp and a clock. My desk is on the other side of the room. I do my homework there every evening. On the desk, there is a computer and a cup with many pens.

On the wall, there are some posters of my favourite football players. There is also a calendar with photos of animals.

I clean my room every Saturday morning. My mother says it is the tidiest room in the house! I am not sure that is true, but I try.
? c | What can the narrator see from the window? | *The street and a tall tree | The sea | A park | The first paragraph says so. | I can see the street and a tall tree.
? c | What colour are the walls? | *Light blue | White | Green | The second paragraph says so. | The walls are light blue
? s | What does the narrator keep under the bed? | shoes and a box of old toys / shoes and toys / shoes and old toys | The second paragraph says so. | I keep my shoes and a box of old toys.
? t | There are posters of singers on the wall. | F | The posters show football players. | there are some posters of my favourite football players.
? t | The narrator cleans the room every Saturday morning. | T | The last paragraph says so. | I clean my room every Saturday morning.

## The weather in my town | NW
My town is in the south of Viet Nam, so it is warm all year. We do not have four seasons like some countries. We have only two seasons: the dry season and the rainy season.

The dry season is from December to April. It is sunny almost every day, and it does not rain much. In March and April, it is very hot, sometimes thirty-five degrees. People drink a lot of cold drinks and stay inside in the middle of the day.

The rainy season is from May to November. It rains almost every afternoon, but usually not for a long time. The rain is very heavy, and sometimes the streets are full of water. After the rain, the air is cooler and fresh.

I like the dry season, because I can play outside after school. My sister likes the rainy season, because she loves the sound of the rain on the roof.

Tourists usually visit my town in the dry season.
? s | How many seasons does the town have? | two / 2 / two seasons | The first paragraph says so. | We have only two seasons
? c | When is the dry season? | *From December to April | From May to November | All year | The second paragraph says so. | The dry season is from December to April.
? t | It rains all day in the rainy season. | F | It rains almost every afternoon, usually not for long. | but usually not for a long time.
? c | Why does the narrator's sister like the rainy season? | *She loves the sound of the rain on the roof | She can play outside | It is very hot | The fourth paragraph says so. | she loves the sound of the rain on the roof.
? t | Most tourists come in the rainy season. | F | They usually come in the dry season. | Tourists usually visit my town in the dry season.

## A day on the farm | NW
My uncle has a farm in the countryside. Last summer, I stayed with him for one week.

Every day on the farm starts very early. My uncle gets up at five o'clock. First, he feeds the chickens and the pigs. Then he works in the rice field. I helped him with the chickens. I gave them food and found eggs. One morning, I found twelve eggs!

My aunt grows vegetables in a big garden next to the house. There are tomatoes, beans, cabbages and chillies. I helped her water the plants in the evening, when it was not too hot.

The farm also has two cows and a big dog called Den. Den is black, and he follows my uncle everywhere.

Life on the farm is quiet. There are no cars and no shops near the house. At night, the sky is very dark, and you can see many stars. I want to go back next summer.
? s | How long did the narrator stay on the farm? | one week / a week / 1 week | The first paragraph says so. | I stayed with him for one week.
? c | What time does the uncle get up? | *Five o'clock | Six o'clock | Seven o'clock | The second paragraph says so. | My uncle gets up at five o'clock.
? c | How many eggs did the narrator find one morning? | *Twelve | Ten | Twenty | The second paragraph says so. | One morning, I found twelve eggs!
? t | The aunt waters the plants at noon. | F | She waters them in the evening. | I helped her water the plants in the evening
? t | The farm has many shops nearby. | F | There are no shops near the house. | There are no cars and no shops near the house.

## Buying new clothes | SH
Next week, I am going to my cousin's wedding, so I need some new clothes. On Saturday, my mother and I went shopping at the shopping centre.

First, we went to a big clothes shop. There were many beautiful dresses, but they were too expensive. One dress cost one hundred dollars! My mother said, "That is too much."

Then we went to a smaller shop on the second floor. The clothes were cheaper there. I tried on a yellow dress and a green dress. The yellow dress was too big, but the green dress was perfect. It cost thirty-five dollars.

I also needed new shoes. We found white shoes in a shoe shop next to the café. They were comfortable and cost twenty dollars.

After shopping, we had ice cream in the café. My mother had chocolate, and I had strawberry. I was very happy with my new clothes. Now I am ready for the wedding!
? c | Why does the narrator need new clothes? | *To go to a cousin's wedding | To start a new school | For a holiday | The first paragraph explains. | I am going to my cousin's wedding
? t | The narrator bought a dress in the first shop. | F | The dresses there were too expensive. | they were too expensive.
? c | Why didn't the narrator buy the yellow dress? | *It was too big | It was too expensive | It was the wrong colour | The third paragraph explains. | The yellow dress was too big
? s | How much did the green dress cost? | thirty-five dollars / 35 dollars / $35 / thirty-five / 35 | The third paragraph gives the price. | It cost thirty-five dollars.
? t | The shoe shop is next to the café. | T | The fourth paragraph says so. | in a shoe shop next to the café.

## My father's job | WK
My father is a nurse. He works at the big hospital in our city. Many people think that nurses are always women, but my father says that is not true. In his team, there are six men and twenty women.

My father works in the children's part of the hospital. He looks after sick children and helps the doctors. He gives medicine, checks temperatures and talks to parents. He says talking to parents is a very important part of his job.

His job is not easy. Sometimes he works at night, from eight in the evening to eight in the morning. Then he sleeps in the day, and we must be quiet at home.

My father loves his job. He says the best moment is when a sick child gets better and goes home with a big smile.

When I grow up, I want to help people too. Maybe I will be a doctor.
? c | Where does the father work? | *At the big hospital in the city | At a school | At a small clinic | The first paragraph says so. | He works at the big hospital in our city.
? s | How many men are in his team? | six / 6 / six men | The first paragraph says so. | there are six men and twenty women.
? c | What does he say is very important? | *Talking to parents | Working at night | Wearing a uniform | The second paragraph says so. | He says talking to parents is a very important part of his job.
? t | The father never works at night. | F | Sometimes he works at night. | Sometimes he works at night
? t | The narrator wants to help people in the future. | T | The last paragraph says so. | When I grow up, I want to help people too.
"""

PASSAGES["A1"] += """
## A trip by train | TP
Last summer, my grandmother and I took the train from Ho Chi Minh City to Nha Trang. It was my first train trip, and I was very excited.

The train left the station at nine o'clock at night. We had a small room with four beds. Two other people slept in our room, a young woman and her son. The boy was six, and he was very friendly.

I slept in the top bed. It was a little small, but it was fun. I looked out of the window and saw lights from small towns. The train made a soft sound all night, and I slept very well.

In the morning, a man came with a trolley. He sold coffee, tea, bread and noodles. My grandmother had coffee, and I had noodles.

We arrived in Nha Trang at seven o'clock in the morning. From the window, I could see the blue sea. Now I always want to travel by train.
? c | Where did they travel to? | *Nha Trang | Ha Noi | Da Lat | The first paragraph says so. | from Ho Chi Minh City to Nha Trang.
? s | What time did the train leave? | nine o'clock at night / nine / 9 pm / 9 | The second paragraph says so. | The train left the station at nine o'clock at night.
? t | The narrator slept in the bottom bed. | F | The narrator slept in the top bed. | I slept in the top bed.
? c | What did the narrator have for breakfast? | *Noodles | Bread | Coffee | The fourth paragraph says so. | My grandmother had coffee, and I had noodles.
? t | The narrator slept badly on the train. | F | The narrator slept very well. | I slept very well.

## The new park | PT
There is a new park in our town. It opened in March, and now it is very popular with families.

The park is big. In the middle, there is a lake with ducks and fish. Around the lake, there is a path for walking and running. Many old people walk there early in the morning, and young people run there in the evening.

There is a playground for children with swings, slides and a sandpit. Next to the playground, there are tables and chairs where parents can sit. There is also a small café that sells drinks and ice cream.

On the north side of the park, there is a big field. On weekends, children play football there, and families have picnics. There are many trees, so it is cool even in the summer.

The park is clean, because there are many bins. Dogs are welcome, but they must be on a lead. The park opens at five in the morning and closes at ten at night.
? s | When did the park open? | March / in March | The first paragraph says so. | It opened in March
? c | What is in the middle of the park? | *A lake | A playground | A café | The second paragraph says so. | In the middle, there is a lake with ducks and fish.
? c | Who runs around the lake in the evening? | *Young people | Old people | Children | The second paragraph says so. | young people run there in the evening.
? t | Dogs can run freely in the park. | F | They must be on a lead. | they must be on a lead.
? t | The park closes at ten at night. | T | The last paragraph says so. | closes at ten at night.

## Cooking with my mum | FD
Every Sunday, I cook lunch with my mum. It is my favourite part of the week.

Last Sunday, we made fried rice with chicken and vegetables. First, we washed the vegetables: carrots, peas and green onions. My mum cut the chicken, because the knife is very sharp. I cut the carrots into small pieces. It was slow, but my mum said I did a good job.

Then my mum cooked the chicken in a big pan with a little oil. After five minutes, we added the vegetables and the rice. I mixed everything with a big spoon. Finally, we added two eggs and some fish sauce.

The kitchen smelled wonderful. My dad and my sister came into the kitchen and asked, "Is it ready?"

We ate lunch together at one o'clock. Everybody said the fried rice was delicious. I was very proud. Next Sunday, I want to make a vegetable soup, and my mum says I can try to cook it alone.
? c | When does the narrator cook with Mum? | *Every Sunday | Every day | Every Saturday | The first paragraph says so. | Every Sunday, I cook lunch with my mum.
? c | Who cut the chicken? | *The mum | The narrator | The dad | The second paragraph explains. | My mum cut the chicken, because the knife is very sharp.
? s | How many eggs did they add? | two / 2 / two eggs | The third paragraph says so. | we added two eggs and some fish sauce.
? t | The family ate lunch at twelve o'clock. | F | They ate at one o'clock. | We ate lunch together at one o'clock.
? t | Next Sunday, the narrator wants to make a vegetable soup. | T | The last paragraph says so. | Next Sunday, I want to make a vegetable soup

## An email from Tom | CO
Hi Nam,

How are you? I'm sorry I didn't write last week. I was very busy with exams at school. They finished on Friday, and now I'm on holiday for two weeks!

Next week, my family is going to the mountains. We are going to stay in a small wooden house near a lake. My dad wants to go fishing every morning. My mum wants to walk in the forest. I want to ride my bike and swim in the lake, but my mum says the water is very cold!

I have some news. We have a new dog! Her name is Bella, and she is three months old. She is very small and white, and she loves playing with my shoes. My mum is not happy about that!

When is your summer holiday? Are you going anywhere? Please write and tell me. And please send a photo of your new house.

Bye for now,
Tom
? c | Why didn't Tom write last week? | *He was busy with exams | He was ill | He was on holiday | Tom explains. | I was very busy with exams at school.
? s | How long is Tom's holiday? | two weeks / 2 weeks | Tom says so. | now I'm on holiday for two weeks!
? c | What does Tom's dad want to do? | *Go fishing | Walk in the forest | Swim in the lake | Tom explains. | My dad wants to go fishing every morning.
? t | Bella is a big black dog. | F | She is small and white. | She is very small and white
? t | Tom asks Nam for a photo of his new house. | T | Tom asks for it at the end. | please send a photo of your new house.

## The school concert | ED
Every year in December, our school has a concert for parents. This year, it was on Friday evening in the school hall.

Students from every class took part. The youngest children sang a song about animals. They wore funny animal hats, and everybody laughed and clapped. Then some older students played the guitar and the piano.

My class danced a traditional dance. We practised for three weeks after school. I was very nervous before we started, but when the music began, I felt better. I did not make any mistakes!

The best part of the evening was a song by our teachers. They sang in English, and they were not very good, but it was very funny. All the students sang with them.

After the concert, there were cakes and drinks for everyone. The headteacher said thank you to the students and the parents. My parents said they were proud of me. I can't wait for next year's concert.
? c | When is the concert every year? | *In December | In June | In September | The first paragraph says so. | Every year in December
? c | What did the youngest children wear? | *Funny animal hats | Traditional clothes | Football shirts | The second paragraph says so. | They wore funny animal hats
? s | How long did the narrator's class practise? | three weeks / 3 weeks | The third paragraph says so. | We practised for three weeks after school.
? t | The narrator made some mistakes in the dance. | F | The narrator made no mistakes. | I did not make any mistakes!
? t | The teachers sang in English. | T | The fourth paragraph says so. | They sang in English

## A lost dog | AN
On Tuesday afternoon, I was walking home from school when I saw a small dog in the street. It was brown, with one white ear, and it looked scared. It did not have a collar.

I stopped and spoke to it softly. After a few minutes, the dog came to me. I gave it some water from my bottle. Then I carried it home.

My mother said, "This dog has a family. Somebody is looking for it." We took a photo of the dog and put it on the neighbourhood group on her phone. We wrote, "Did you lose this dog? Please call us."

That evening, a woman called. She lived two streets away, and the dog's name was Peanut. Peanut ran out of her garden in the morning, and her children were very sad.

Thirty minutes later, the woman and her two children came to our house. When Peanut saw the children, it jumped and barked happily. The children thanked me many times and gave me a box of chocolates.
? c | What did the dog look like? | *Brown with one white ear | Black and white | Small and grey | The first paragraph describes it. | It was brown, with one white ear
? t | The dog had a collar. | F | It did not have a collar. | It did not have a collar.
? c | Where did they post the photo? | *In a neighbourhood group on the mother's phone | In a newspaper | On a tree | The third paragraph says so. | put it on the neighbourhood group on her phone.
? s | What was the dog's name? | Peanut | The fourth paragraph gives the name. | the dog's name was Peanut.
? t | The children gave the narrator a box of chocolates. | T | The last paragraph says so. | gave me a box of chocolates.

## Winter in Da Lat | TR
Da Lat is a city in the mountains in the south of Viet Nam. It is famous for its cool weather, flowers and pine trees. Last December, my family spent four days there.

In Ho Chi Minh City, it is always hot, so the weather in Da Lat was a big surprise for me. In the morning, it was only twelve degrees! I wore a jacket, a hat and gloves. In the afternoon, it was warmer, about twenty degrees.

We visited a flower garden with thousands of flowers in many colours. We also went to a strawberry farm. We picked strawberries and ate some of them. They were sweet and fresh.

In the evening, we went to the night market. We ate hot grilled sweet potatoes and drank hot soy milk. It was perfect in the cold weather.

I loved Da Lat. The air was fresh, and the city was quiet and beautiful. I want to go back next year.
? s | How many days did the family spend in Da Lat? | four / 4 / four days | The first paragraph says so. | my family spent four days there.
? c | What was the temperature in the morning? | *Twelve degrees | Twenty degrees | Thirty degrees | The second paragraph says so. | In the morning, it was only twelve degrees!
? c | What did they pick at the farm? | *Strawberries | Apples | Flowers | The third paragraph says so. | We picked strawberries
? t | They drank cold juice at the night market. | F | They drank hot soy milk. | drank hot soy milk.
? t | Da Lat is famous for its pine trees. | T | The first paragraph says so. | It is famous for its cool weather, flowers and pine trees.

## I love drawing | HS
My hobby is drawing. I started when I was six years old. Now I am twelve, and I draw almost every day.

I like drawing animals and people. My favourite animals to draw are cats and horses. Drawing horses is difficult, because their legs are long and thin. I practise a lot.

I usually draw with a pencil, but sometimes I use colour pencils or paint. My grandfather gave me a box of paints for my last birthday. It has twenty-four colours.

Every Saturday morning, I go to an art class at the culture centre. There are ten students in my class, and our teacher is a real artist. She shows us how to draw faces and how to use light and shadow.

Last month, I drew a picture of my cat sleeping in the sun. My teacher put it in a small exhibition at the culture centre. My family came to see it, and I was very proud. One day, I want to be an artist too.
? s | How old was the narrator when they started drawing? | six / 6 / six years old | The first paragraph says so. | I started when I was six years old.
? c | Why is drawing horses difficult? | *Their legs are long and thin | They move a lot | They are very big | The second paragraph explains. | because their legs are long and thin.
? c | Who gave the narrator a box of paints? | *The grandfather | The art teacher | The mother | The third paragraph says so. | My grandfather gave me a box of paints for my last birthday.
? t | There are twenty students in the art class. | F | There are ten students. | There are ten students in my class
? t | The narrator's picture of a cat was in an exhibition. | T | The last paragraph says so. | My teacher put it in a small exhibition at the culture centre.

## A visit to the history museum | ED
On Thursday, my class visited the history museum in the city. We went there by bus with our two teachers.

The museum is in a big old building with yellow walls. It has five rooms. Each room shows a different time in history. In the first room, there were very old tools made of stone. Our guide said they were more than three thousand years old!

In another room, we saw old clothes, coins and pictures of kings and queens. My friend Mai liked the beautiful old dresses. I liked the old coins, because some of them had holes in the middle.

We could not touch anything, and we could not take photos with a flash. But we could draw pictures in our notebooks. I drew an old boat.

At the end, we had lunch in the museum garden. Then we went back to school. Our homework was to write about our favourite thing in the museum. I wrote about the coins.
? s | How did the class travel to the museum? | by bus / bus | The first paragraph says so. | We went there by bus with our two teachers.
? c | How many rooms does the museum have? | *Five | Three | Ten | The second paragraph says so. | It has five rooms.
? c | What did Mai like? | *The old dresses | The stone tools | The coins | The third paragraph says so. | My friend Mai liked the beautiful old dresses.
? t | The students could take photos with a flash. | F | They could not use a flash. | we could not take photos with a flash.
? t | The narrator wrote about the coins for homework. | T | The last paragraph says so. | I wrote about the coins.

## Healthy food for children | HE
Children need good food to grow and to stay healthy. Here are some easy ideas for parents.

Breakfast is very important. A good breakfast gives children energy for school. Eggs, bread, milk and fruit are good choices. Try not to give children sweet cakes or sugary drinks in the morning.

Children should eat fruit and vegetables every day. They give us vitamins. Many children do not like vegetables, so make them fun. You can cut carrots into stars or make a face on the plate with vegetables.

Water is the best drink. Children should drink six to eight glasses of water every day, more when it is hot or when they play sport. Fizzy drinks have a lot of sugar, and they are bad for teeth.

Sweets and snacks are fine sometimes, but not every day. And try to eat together as a family. When parents eat healthy food, children often copy them.
? c | Why is breakfast important for children? | *It gives them energy for school | It helps them sleep | It makes them tall at once | The second paragraph explains. | A good breakfast gives children energy for school.
? c | What idea does the text give to make vegetables fun? | *Cutting carrots into stars | Adding sugar | Hiding them in cakes | The third paragraph suggests it. | You can cut carrots into stars
? s | What is the best drink? | water | The fourth paragraph says so. | Water is the best drink.
? t | Fizzy drinks are good for teeth. | F | They are bad for teeth. | they are bad for teeth.
? t | Children often copy their parents' eating habits. | T | The last paragraph says so. | children often copy them.

## A busy family | PF
There are five people in my family: my father, my mother, my two brothers and me. Every person in our family is very busy.

My father is a bus driver. He starts work at six o'clock in the morning, so he leaves home very early. My mother works in a bank. She takes us to school before she goes to work.

My older brother, Long, is sixteen. He studies a lot, because he has big exams next year. In the evening, he also works in a café for three hours. My younger brother, Bao, is eight. He plays football after school every day.

I am twelve. After school, I have English lessons on Monday and Wednesday and piano lessons on Friday.

Because everybody is busy, we only have dinner together on Sunday. On Sunday evening, we cook together, eat and talk about our week. It is my favourite time of the week, and nobody uses a phone at the table.
? s | How many people are there in the family? | five / 5 | The first paragraph says so. | There are five people in my family
? c | What is the father's job? | *A bus driver | A bank worker | A teacher | The second paragraph says so. | My father is a bus driver.
? c | Why does Long study a lot? | *He has big exams next year | He wants to work in a café | He likes books | The third paragraph explains. | because he has big exams next year.
? t | The narrator has piano lessons on Monday. | F | Piano lessons are on Friday. | piano lessons on Friday.
? t | The family has dinner together every evening. | F | Only on Sunday. | we only have dinner together on Sunday.

## The new student | ED
On Monday, a new student came to our class. Her name is Yuki, and she is from Japan. Her father has a new job in Viet Nam, so the family moved here last month.

Yuki speaks Japanese and English, but she does not speak Vietnamese yet. On her first day, she looked a little sad and quiet. Our teacher asked me to help her, because I speak English quite well.

I showed Yuki the school: the library, the canteen and the sports field. At lunch, she sat with me and my friends. She told us about her old school in Osaka. In Japan, students clean their classroom every day!

Now Yuki is learning Vietnamese. Every day, I teach her five new words. She can already say "hello", "thank you" and "delicious".

Yuki is very good at maths and drawing. Last week, she drew a picture of our class, and the teacher put it on the wall. I think Yuki is happy now.
? c | Where is Yuki from? | *Japan | Korea | China | The first paragraph says so. | she is from Japan.
? c | Why did Yuki's family move? | *Her father has a new job in Viet Nam | They wanted a holiday | Her mother is a teacher | The first paragraph explains. | Her father has a new job in Viet Nam
? t | Yuki speaks Vietnamese well. | F | She does not speak Vietnamese yet. | she does not speak Vietnamese yet.
? s | How many new words does the narrator teach Yuki every day? | five / 5 / five words | The fourth paragraph says so. | Every day, I teach her five new words.
? t | In Yuki's old school, students cleaned their classroom every day. | T | Yuki explained this. | In Japan, students clean their classroom every day!

## My village | PT
I live in a small village near a river. About five hundred people live here. Most people are farmers. They grow rice and vegetables, and some families have fish ponds.

The village has one primary school, one small health centre and a market. The market is open every morning from five to ten o'clock. People sell vegetables, fish, meat and fruit there.

There is no big supermarket in the village. If people want to buy clothes or electronics, they go to the town. The town is fifteen kilometres away, and there is a bus three times a day.

In the evening, the village is very quiet. Children play near the river, and old people sit and talk under the big banyan tree near the school.

I love my village because the people are friendly and the air is clean. But when I finish school, I want to study in the city. Maybe one day I will come back and work here.
? s | About how many people live in the village? | five hundred / 500 | The first paragraph says so. | About five hundred people live here.
? c | When is the market open? | *Every morning from five to ten | All day | Only at weekends | The second paragraph says so. | The market is open every morning from five to ten o'clock.
? c | How far is the town? | *Fifteen kilometres | Five kilometres | Fifty kilometres | The third paragraph says so. | The town is fifteen kilometres away
? t | There is a big supermarket in the village. | F | There is no big supermarket. | There is no big supermarket in the village.
? t | Old people sit under a banyan tree in the evening. | T | The fourth paragraph says so. | old people sit and talk under the big banyan tree

## Sports day at school | HS
Every year in April, our school has a sports day. All the students go to the big field behind the school. Parents can come and watch.

This year, the weather was perfect: sunny but not too hot. The day started at eight o'clock with music and a parade. Each class had a team colour. My class was the green team.

There were many races. There was a running race, a sack race and a race with eggs on spoons. There was also a tug of war between the teachers and the oldest students. The students won, and everybody cheered!

I ran in the hundred-metre race. I came second. My best friend Lan came first. She is very fast. I was a little sad, but I got a silver medal, and my parents took a photo of me.

At the end of the day, the green team had the most points. We won a big cup! Our teacher bought us all cold drinks to say well done.
? c | When is sports day? | *In April | In June | In December | The first paragraph says so. | Every year in April
? s | What colour was the narrator's team? | green / the green team | The second paragraph says so. | My class was the green team.
? c | Who won the tug of war? | *The students | The teachers | Nobody | The third paragraph says so. | The students won, and everybody cheered!
? t | The narrator won the hundred-metre race. | F | The narrator came second. | I came second.
? t | The green team won a cup. | T | The last paragraph says so. | We won a big cup!

## A camping trip | NW
Last month, my father and I went camping in a national park. It was my first time sleeping in a tent.

We drove for three hours to get there. We put up our tent near a small river. It was not easy! The wind was strong, and the tent moved a lot. After forty minutes, it was ready.

In the afternoon, we walked in the forest. We saw monkeys in the trees and a big blue butterfly. My father knows the names of many birds, and he taught me some of them.

In the evening, we made a small fire and cooked sausages and corn. Then we sat by the fire and looked at the stars. There were so many! In the city, I can only see a few stars.

At night, I heard strange noises outside the tent. I was a little scared, but my father said they were only frogs. In the morning, we swam in the river. The water was cold but clean.
? s | How long was the drive to the park? | three hours / 3 hours | The second paragraph says so. | We drove for three hours to get there.
? c | Why was it difficult to put up the tent? | *The wind was strong | It was raining | It was dark | The second paragraph explains. | The wind was strong, and the tent moved a lot.
? c | What did they cook in the evening? | *Sausages and corn | Fish and rice | Noodles | The fourth paragraph says so. | cooked sausages and corn.
? t | The noises at night were from monkeys. | F | The father said they were frogs. | my father said they were only frogs.
? t | The narrator swam in the river in the morning. | T | The last paragraph says so. | In the morning, we swam in the river.

## My first phone | TE
For my thirteenth birthday, my parents gave me my first phone. It is not new; it was my mother's old phone. But I was very happy.

My parents made some rules. I can use the phone for one hour a day after I finish my homework. I cannot use it at the dinner table. At night, the phone stays in the kitchen, not in my bedroom.

I use my phone to talk to my friends and my grandparents. My grandparents live in another city, so now I can video call them every Sunday. My grandmother always asks, "Are you eating well?"

I also use my phone to listen to music and to learn English with an app. Every day, I learn ten new words. I like the app because it has games.

At first, I thought the rules were too strict. But now I understand them. Some of my friends use their phones all night, and they are always tired at school.
? c | What kind of phone did the narrator get? | *The mother's old phone | A brand-new phone | The father's phone | The first paragraph says so. | it was my mother's old phone.
? s | How long can the narrator use the phone each day? | one hour / an hour / 1 hour | The second paragraph says so. | I can use the phone for one hour a day
? t | The phone stays in the bedroom at night. | F | It stays in the kitchen. | At night, the phone stays in the kitchen, not in my bedroom.
? c | When does the narrator video call the grandparents? | *Every Sunday | Every evening | On birthdays | The third paragraph says so. | now I can video call them every Sunday.
? t | The narrator now understands the rules. | T | The last paragraph says so. | But now I understand them.

## The café on the corner | FD
There is a small café on the corner of my street. It is called Morning Sun. It opens at half past six every morning, and it is always busy before work and school.

The owner is a woman called Mrs. Thu. She is about fifty years old, and she makes very good coffee. Her son helps her at the weekend.

The café is small. There are only six tables inside, but there are more chairs outside on the pavement. Many people like to sit outside and watch the street.

The most popular drink is iced coffee with milk. It costs one dollar. Mrs. Thu also sells fruit juice, tea and fresh bread with eggs. On Sundays, she makes a special banana cake, and it is often sold out by ten o'clock.

My father goes to Morning Sun every morning before work. He drinks a coffee and reads the news. He says Mrs. Thu knows the name of every customer.
? s | What is the café called? | Morning Sun | The first paragraph gives the name. | It is called Morning Sun.
? c | How many tables are inside? | *Six | Ten | Two | The third paragraph says so. | There are only six tables inside
? c | What is the most popular drink? | *Iced coffee with milk | Fruit juice | Tea | The fourth paragraph says so. | The most popular drink is iced coffee with milk.
? t | The banana cake is sold every day. | F | It is made on Sundays. | On Sundays, she makes a special banana cake
? t | The father reads the news at the café. | T | The last paragraph says so. | He drinks a coffee and reads the news.

## At the dentist | HE
I went to the dentist yesterday. I go twice a year, in January and in July. I do not really like the dentist, but my mother says it is important.

The dentist's name is Dr. Nam. He is friendly and he always tells jokes. First, he looked at my teeth with a small mirror. Then he cleaned them with a special brush. It made a loud noise, but it did not hurt.

"Your teeth are very good," he said, "but you have a small problem here." He showed me a tooth at the back. It had a small black spot. "You eat too many sweets," he said with a smile.

Dr. Nam fixed the tooth. It took fifteen minutes, and I was a little scared, but it was OK. He told me to brush my teeth two times a day, for two minutes each time, and to eat fewer sweets.

At the end, he gave me a sticker and a new toothbrush. I want to have healthy teeth, so I will listen to him.
? c | How often does the narrator go to the dentist? | *Twice a year | Once a month | Every week | The first paragraph says so. | I go twice a year, in January and in July.
? c | What does Dr. Nam always do? | *Tell jokes | Give sweets | Sing songs | The second paragraph says so. | he always tells jokes.
? t | Cleaning the teeth hurt a lot. | F | It made a noise but did not hurt. | It made a loud noise, but it did not hurt.
? s | How long did it take to fix the tooth? | fifteen minutes / 15 minutes | The fourth paragraph says so. | It took fifteen minutes
? t | Dr. Nam gave the narrator a new toothbrush. | T | The last paragraph says so. | he gave me a sticker and a new toothbrush.

## Planting trees at school | EN
Last Friday was a special day at our school. Every class planted a tree in the school garden.

Our teacher told us why trees are important. Trees give us shade on hot days, and they make the air clean. Birds and insects live in them too.

My class planted a small mango tree. First, we dug a big hole. It was hard work, because the ground was dry. Then we put the tree in the hole and covered the roots with soil. Finally, we gave it a lot of water.

Each class made a small sign with the class name and the date. Our sign says "Class 6A, March 2026". Every week, two students from our class must water the tree. This week, it is my turn with my friend Bao.

Our teacher says that in about four years, the tree will have mangoes. By then, we will be in high school, but we can come back and eat them!
? c | What did every class do last Friday? | *Planted a tree | Painted a wall | Cleaned the classroom | The first paragraph says so. | Every class planted a tree in the school garden.
? c | Which is a reason trees are important? | *They make the air clean | They make noise | They need a lot of water | The second paragraph explains. | they make the air clean.
? t | Digging the hole was easy. | F | It was hard work. | It was hard work, because the ground was dry.
? s | What kind of tree did the narrator's class plant? | mango / a mango tree / mango tree | The third paragraph says so. | My class planted a small mango tree.
? t | The tree will have mangoes in about four years. | T | The teacher says so. | in about four years, the tree will have mangoes.

## My grandmother | PF
My grandmother is seventy-five years old, but she is very active. She lives with my family, and everybody loves her.

Every morning, she gets up at five o'clock and goes to the park. She does exercise with a group of old women. They move slowly to music. My grandmother says it keeps her healthy.

After that, she goes to the market and buys fresh food. She is the best cook in our family. Her fish soup is famous! Many neighbours ask for her recipe, but she never tells them everything.

In the afternoon, she sleeps for one hour. Then she works in our small garden. She grows herbs, chillies and beautiful flowers.

In the evening, she tells me stories about her life. When she was young, there was no electricity in her village, and she walked two hours to school. I like her stories very much. She says I must study hard, because she did not have that chance.
? s | How old is the grandmother? | seventy-five / 75 | The first paragraph says so. | My grandmother is seventy-five years old
? c | What does she do in the park? | *Exercise with a group to music | Sell vegetables | Read books | The second paragraph explains. | She does exercise with a group of old women.
? c | What dish is she famous for? | *Fish soup | Fried rice | Spring rolls | The third paragraph says so. | Her fish soup is famous!
? t | She gives the full recipe to her neighbours. | F | She never tells them everything. | she never tells them everything.
? t | When she was young, she walked two hours to school. | T | The last paragraph says so. | she walked two hours to school.

## Going to the cinema | HS
On Saturday, I went to the cinema with my two cousins. It was my cousin Lan's birthday, and her parents paid for the tickets.

The cinema is in the new shopping centre. We arrived at half past two, and the film started at three. Before the film, we bought popcorn and three cold drinks. The popcorn was very salty, but we ate all of it.

The film was an animated film about a little fox who wanted to find his family. It was funny and a little sad. At the end, the fox found his mother, and my cousin cried! The film was about one hour and forty minutes long.

The cinema was very cold, so I was happy I had a jacket. The seats were big and comfortable.

After the film, we walked around the shopping centre and looked at the shops. Then Lan's mother picked us up. We all agreed that it was a great film, and we want to see the next one together.
? c | Why did they go to the cinema? | *It was Lan's birthday | It was a holiday | The film was free | The first paragraph explains. | It was my cousin Lan's birthday
? s | What time did the film start? | three / 3 / three o'clock / 3 pm | The second paragraph says so. | the film started at three.
? c | What was the film about? | *A little fox looking for his family | A dog in the city | Two children at school | The third paragraph says so. | a little fox who wanted to find his family.
? t | The cinema was very hot. | F | It was very cold. | The cinema was very cold
? t | They want to see the next film together. | T | The last paragraph says so. | we want to see the next one together.

## Shopping at the fish market | SH
My mother and I go to the fish market every Saturday morning. It is near the sea, and the fish there are very fresh.

We leave home at six o'clock, because the best fish are sold early. The market is noisy and wet. People shout the prices, and there are big boxes of ice everywhere.

There are many kinds of fish and seafood: big tuna, small silver fish, crabs, prawns and squid. My mother always buys from the same woman. Her name is Mrs. Lien, and she gives us a good price.

Last Saturday, my mother bought two kilos of prawns and one big fish. The prawns cost ten dollars a kilo. The fish cost eight dollars. Mrs. Lien cleaned the fish for us.

I like the fish market, but I do not like the smell! After shopping, we always have a bowl of noodle soup at a small stall near the market. Then we go home and put the fish in the fridge.
? c | When do they go to the fish market? | *Every Saturday morning | Every Sunday afternoon | Every day | The first paragraph says so. | every Saturday morning.
? c | Why do they leave home at six o'clock? | *The best fish are sold early | The market closes at seven | It is cooler | The second paragraph explains. | because the best fish are sold early.
? s | How much did the prawns cost per kilo? | ten dollars / 10 dollars / $10 / ten / 10 | The fourth paragraph says so. | The prawns cost ten dollars a kilo.
? t | Mrs. Lien cleaned the fish. | T | The fourth paragraph says so. | Mrs. Lien cleaned the fish for us.
? t | The narrator loves the smell of the market. | F | The narrator does not like the smell. | I do not like the smell!

## The flower festival | DL
Every year in January, our city has a flower festival. It is one of the most popular events of the year, and thousands of people visit it.

The festival is in the big park in the city centre. There are flowers everywhere: red, yellow, pink, white and purple. Some flowers are made into big shapes, like animals, hearts and even a train!

Many people come to take photos. They wear their best clothes, and some young women wear traditional dresses. It is very crowded at the weekend, so my family always goes on a weekday evening, when it is quieter.

At night, the park is beautiful, because there are lights in the trees. There is also music, and people sell food and drinks.

This year, my favourite thing was a big peacock made of thousands of flowers. Its tail was blue and green. My little sister wanted to touch it, but my mother said no. The festival lasts for ten days.
? c | When is the flower festival? | *In January | In April | In August | The first paragraph says so. | Every year in January
? c | Where is the festival? | *In the big park in the city centre | At the beach | In a school | The second paragraph says so. | The festival is in the big park in the city centre.
? t | The narrator's family goes at the weekend. | F | They go on a weekday evening. | my family always goes on a weekday evening
? s | What was the narrator's favourite thing this year? | a peacock / a big peacock made of flowers / peacock | The last paragraph says so. | my favourite thing was a big peacock made of thousands of flowers.
? t | The festival lasts for ten days. | T | The last paragraph says so. | The festival lasts for ten days.

## My morning routine | DL
I am a student, and my mornings are always busy. Here is my routine on school days.

My alarm rings at six o'clock. I do not like getting up early, so I usually stay in bed for five more minutes. Then I get up, wash my face and brush my teeth.

At a quarter past six, I put on my school uniform. My uniform is a white shirt and dark blue trousers. Then I go to the kitchen. My mother makes breakfast for the family. I usually eat bread with eggs and drink a glass of milk.

After breakfast, I check my school bag. I make sure I have all my books, my pens and my homework. Once I forgot my maths homework, and my teacher was not happy!

At a quarter to seven, my father takes me to school on his motorbike. The trip takes fifteen minutes. School starts at seven o'clock, so I always have a few minutes to talk with my friends before class.
? s | What time does the alarm ring? | six / 6 / six o'clock / 6 am | The second paragraph says so. | My alarm rings at six o'clock.
? c | What does the school uniform look like? | *A white shirt and dark blue trousers | A blue shirt and black trousers | A red T-shirt | The third paragraph says so. | My uniform is a white shirt and dark blue trousers.
? c | What does the narrator usually have for breakfast? | *Bread with eggs and milk | Rice and soup | Noodles | The third paragraph says so. | I usually eat bread with eggs and drink a glass of milk.
? t | The narrator once forgot their maths homework. | T | The fourth paragraph says so. | Once I forgot my maths homework
? t | The narrator walks to school. | F | The father takes the narrator by motorbike. | my father takes me to school on his motorbike.

## My piggy bank | MS
When I was eight, my grandfather gave me a piggy bank. It is pink and made of plastic, and it has a small hole on its back for coins.

Every week, my parents give me some pocket money. I can spend some of it, but I always put half of it in my piggy bank. Sometimes my grandparents give me money for my birthday or at Tet, and I put it in the piggy bank too.

Last year, I wanted to buy a new skateboard. It cost forty dollars. I saved my money for six months. Every month, I opened the piggy bank and counted the money. It was slow, but I did not give up.

In December, I finally had forty dollars. I went to the sports shop with my father and bought the skateboard. I was so proud, because I bought it with my own money.

Now I am saving for a new bike. It will take a long time, but I know I can do it.
? c | Who gave the narrator the piggy bank? | *The grandfather | The father | The mother | The first paragraph says so. | my grandfather gave me a piggy bank.
? c | How much of the pocket money does the narrator save? | *Half | All of it | None | The second paragraph says so. | I always put half of it in my piggy bank.
? s | How much did the skateboard cost? | forty dollars / 40 dollars / $40 / forty / 40 | The third paragraph says so. | It cost forty dollars.
? t | The narrator's father paid for the skateboard. | F | The narrator bought it with their own money. | because I bought it with my own money.
? t | The narrator is now saving for a bike. | T | The last paragraph says so. | Now I am saving for a new bike.
"""

PASSAGES["A2"] = """
## A summer at the camp | WK
Last summer, I worked as a helper at a children's camp in the mountains. I was seventeen, and it was my first real job.

The camp was for children between eight and twelve years old. There were sixty children and twelve helpers. Each helper looked after a group of five children. My group was five boys who were all ten years old. They were noisy and full of energy, but they were also very funny.

Every day started at seven o'clock with breakfast. Then we did activities: swimming in the lake, climbing, painting and making things from wood. In the evening, we sat around a fire, sang songs and told stories.

The job was harder than I expected. I was tired every night, and I had to be patient when the boys argued. One boy was homesick for the first three days and cried every night. I talked to him a lot, and by the end of the week he was the happiest child in the group.

I earned some money, but the best thing was the experience. I learned how to work in a team and how to solve problems quickly. I am going to work at the camp again next summer.
? c | How old were the boys in the narrator's group? | *Ten | Eight | Twelve | The second paragraph says so. | five boys who were all ten years old.
? s | How many helpers were there? | twelve / 12 / twelve helpers | The second paragraph says so. | There were sixty children and twelve helpers.
? t | The job was easier than the narrator expected. | F | It was harder. | The job was harder than I expected.
? c | What happened to the homesick boy? | *He became the happiest child in the group | He went home early | He changed groups | The fourth paragraph explains. | he was the happiest child in the group.
? t | The narrator plans to work at the camp again. | T | The last paragraph says so. | I am going to work at the camp again next summer.

## My balcony garden | HS
Six months ago, I started a new hobby: gardening. I live in a small flat on the fifth floor, so I don't have a garden. But I have a balcony, and it gets sun all afternoon.

At first, I didn't know anything about plants. I bought three plants from the market: basil, mint and a small tomato plant. The basil and mint grew very quickly, but the tomato plant died after two weeks. I gave it too much water.

Then I watched some videos online and read a book from the library. I learned that every plant needs different amounts of water and sun. Now I check the soil with my finger before I water the plants.

Today, I have fifteen pots on my balcony. I grow herbs, chillies, lettuce and some flowers. Last month, I picked my first tomatoes from a new plant. They were small, but they tasted better than the tomatoes in the supermarket.

Gardening helps me relax after work. I spend about thirty minutes on my balcony every evening. My neighbours sometimes ask me for advice, and I give them herbs. It is a great way to meet people.
? c | Why doesn't the narrator have a garden? | *The narrator lives in a flat on the fifth floor | The narrator lives in the city centre | The narrator has no time | The first paragraph explains. | I live in a small flat on the fifth floor
? c | Why did the first tomato plant die? | *It got too much water | It got too little sun | It was too cold | The second paragraph explains. | I gave it too much water.
? s | How many pots are on the balcony today? | fifteen / 15 | The fourth paragraph says so. | Today, I have fifteen pots on my balcony.
? t | The narrator's tomatoes tasted worse than supermarket tomatoes. | F | They tasted better. | they tasted better than the tomatoes in the supermarket.
? t | The narrator gives herbs to neighbours. | T | The last paragraph says so. | I give them herbs.

## The day I missed the bus | TP
Last Monday was a terrible morning. My alarm didn't ring, because I forgot to charge my phone. I woke up at a quarter to eight, and my first class started at eight thirty.

I got dressed quickly and ran out of the house without breakfast. When I arrived at the bus stop, I saw my bus leaving. The next bus was in twenty minutes, so I decided to walk.

It was raining, and I didn't have an umbrella. After ten minutes, I was wet and cold. Then a car stopped next to me. It was my classmate Duc and his father. "Get in!" Duc said. "We're going to school too."

I arrived at school at twenty-five past eight, five minutes before class. I was wet, but I was on time. My teacher looked at me and smiled. She lent me a towel from the staff room.

That evening, I bought a cheap alarm clock. Now I don't need my phone to wake up, and I always have an umbrella in my bag.
? c | Why didn't the alarm ring? | *The phone wasn't charged | The alarm was broken | The narrator turned it off | The first paragraph explains. | because I forgot to charge my phone.
? s | How long was the wait for the next bus? | twenty minutes / 20 minutes | The second paragraph says so. | The next bus was in twenty minutes
? c | Who gave the narrator a lift? | *A classmate and his father | A teacher | A neighbour | The third paragraph explains. | It was my classmate Duc and his father.
? t | The narrator was late for class. | F | The narrator arrived five minutes early. | five minutes before class.
? t | The narrator bought an alarm clock. | T | The last paragraph says so. | That evening, I bought a cheap alarm clock.

## Life in a big city | PT
Two years ago, my family moved from a small town to Ho Chi Minh City. My father got a new job there. At first, I didn't like the city at all.

Everything was different. In my town, I walked everywhere, and the streets were quiet. In the city, there were thousands of motorbikes, and the noise never stopped. The air was not as clean, and the summer felt hotter. I missed my old friends, too.

But slowly, I started to enjoy city life. There are many things to do here. There are cinemas, museums, big libraries and parks. On weekends, I go to English clubs where I can practise speaking with people from other countries.

The food is another good thing. There are restaurants from all over the world. Last month, I tried Indian food for the first time, and now it is one of my favourites.

I still miss my town sometimes, and I visit my grandparents there every summer. But now I think the city is my home. There are more opportunities here, and I have made many new friends.
? c | Why did the family move to the city? | *The father got a new job | The narrator started university | The town was too expensive | The first paragraph explains. | My father got a new job there.
? t | At first, the narrator liked the city very much. | F | At first the narrator didn't like it. | At first, I didn't like the city at all.
? c | Where does the narrator practise speaking English? | *At English clubs | At school only | With grandparents | The third paragraph says so. | I go to English clubs
? s | What food did the narrator try for the first time last month? | Indian / Indian food | The fourth paragraph says so. | I tried Indian food for the first time
? t | The narrator visits the grandparents every summer. | T | The last paragraph says so. | I visit my grandparents there every summer.

## An email to a hotel | TR
Dear Sir or Madam,

I would like to book a room at your hotel for my family. We are planning to visit Hoi An next month, from the twelfth to the fifteenth of June. That is three nights.

There are four of us: my husband, me and our two children. Our son is nine, and our daughter is five. Do you have a family room with one big bed and two small beds? If not, two rooms next to each other would also be fine.

I have some questions. Is breakfast included in the price? Is there a swimming pool? Our children love swimming. Also, we are arriving by train, and the station is quite far from the town. Can you help us book a taxi from the station?

Finally, could you tell me the total price for three nights? We would like to pay by credit card when we arrive.

I look forward to hearing from you.

Best regards,
Nguyen Thi Mai
? s | How many nights does Mai want to stay? | three / 3 / three nights | The first paragraph says so. | That is three nights.
? c | How old is Mai's daughter? | *Five | Nine | Seven | The second paragraph says so. | our daughter is five.
? c | What would be acceptable if there is no family room? | *Two rooms next to each other | One small room | A room in another hotel | The second paragraph says so. | two rooms next to each other would also be fine.
? t | The family is arriving by plane. | F | They are arriving by train. | we are arriving by train
? t | Mai wants to pay by credit card on arrival. | T | The fourth paragraph says so. | We would like to pay by credit card when we arrive.

## My grandparents' village, then and now | PF
My grandparents have lived in the same village for more than fifty years. When I visit them, they often tell me how much the village has changed.

When they were young, there was no electricity. In the evening, people used oil lamps, and everyone went to bed early. There was no road, only a narrow path, and the nearest town was a three-hour walk away. Children helped their parents in the rice fields after school.

Today, the village is very different. Every house has electricity, and most families have a television and a motorbike. A new road connects the village to the town, and the trip takes only twenty minutes. There is a modern school and a small health centre.

But some things have not changed. People still grow rice, and neighbours still help each other. When someone builds a house or has a wedding, everyone comes to help.

My grandmother says life is easier now, but she misses the quiet evenings. "We talked more when there was no television," she says. I think she is right.
? s | How long have the grandparents lived in the village? | more than fifty years / over fifty years / fifty years | The first paragraph says so. | for more than fifty years.
? c | What did people use in the evening in the past? | *Oil lamps | Electric lights | Candles only | The second paragraph says so. | people used oil lamps
? c | How long does the trip to town take now? | *Twenty minutes | Three hours | One hour | The third paragraph says so. | the trip takes only twenty minutes.
? t | Neighbours in the village no longer help each other. | F | They still help each other. | neighbours still help each other.
? t | The grandmother misses the quiet evenings. | T | The last paragraph says so. | she misses the quiet evenings.

## How I learned to cook | FD
Until I was twenty, I couldn't cook at all. My mother always cooked for the family, and I only knew how to make instant noodles. Then I moved to another city for university, and I had a problem.

For the first month, I ate in cheap restaurants every day. It was expensive, and the food was often too oily. I gained three kilos and spent most of my money. I knew I had to learn to cook.

I started with simple dishes. I called my mother every evening, and she explained her recipes step by step. My first dish was an omelette. It was a little burnt, but I ate it anyway.

After a few weeks, I could cook rice, vegetables and simple soups. Then I tried more difficult dishes, like braised pork with eggs. I made mistakes, but each time the food was better.

Now I cook almost every day, and I spend half as much money on food. My friends often come to my flat for dinner. Cooking has become one of my favourite activities, and my mother is very proud of me.
? c | What was the only thing the narrator could make before? | *Instant noodles | Fried rice | Omelettes | The first paragraph says so. | I only knew how to make instant noodles.
? s | How many kilos did the narrator gain? | three / 3 / three kilos | The second paragraph says so. | I gained three kilos
? c | How did the narrator learn recipes? | *By calling the mother every evening | By taking a cooking class | By watching TV | The third paragraph explains. | I called my mother every evening
? t | The narrator's first omelette was perfect. | F | It was a little burnt. | It was a little burnt
? t | The narrator now spends less money on food. | T | Half as much. | I spend half as much money on food.

## A weekend in the countryside | NW
Last weekend, my friends and I left the city and went to the countryside. We wanted a break from work and traffic.

We stayed in a small homestay near a river. The owner was a friendly farmer called Mr. Tam. His house was made of wood, and it had a big garden with fruit trees. We slept on mats on the floor, under mosquito nets.

On Saturday, Mr. Tam took us to his rice fields. He showed us how to plant rice. It looked easy, but it was very hard! Our backs hurt after only thirty minutes, and our feet were covered in mud. Mr. Tam laughed and said we did well for city people.

In the afternoon, we rode bicycles along the river and swam in a quiet place. In the evening, Mr. Tam's wife cooked dinner with vegetables from the garden and fish from the river. It was simple but delicious.

On Sunday morning, we woke up to the sound of birds, not motorbikes. We felt relaxed and happy. We are planning to go back in the autumn.
? c | Why did the friends go to the countryside? | *To get a break from work and traffic | To visit family | To buy land | The first paragraph explains. | We wanted a break from work and traffic.
? c | What was Mr. Tam's house made of? | *Wood | Stone | Bricks | The second paragraph says so. | His house was made of wood
? t | Planting rice was easy for the friends. | F | It was very hard. | It looked easy, but it was very hard!
? s | Where did the fish for dinner come from? | the river / from the river / river | The fourth paragraph says so. | fish from the river.
? t | The friends plan to go back in the autumn. | T | The last paragraph says so. | We are planning to go back in the autumn.

## A school exchange | ED
In March, our school had an exchange with a school in Australia. Fifteen Australian students came to our city for two weeks, and each one stayed with a Vietnamese family.

My family hosted a girl called Chloe. She was fourteen, the same age as me. On the first day, she was shy and tired after the long flight. But after a few days, she was more relaxed and talked a lot.

Chloe came to my school with me every day. She joined my English and art classes, and she also learned some Vietnamese words. Our classmates loved her, and she taught us some Australian songs.

At the weekends, my parents took us to the beach and to a traditional village. Chloe tried many Vietnamese dishes. She loved spring rolls, but she didn't like durian at all! She said it smelled terrible.

When Chloe left, we both cried at the airport. We still message each other every week. Next year, I am going to Australia to stay with her family. I'm already very excited.
? s | How many Australian students came? | fifteen / 15 | The first paragraph says so. | Fifteen Australian students came to our city
? c | How old was Chloe? | *Fourteen | Fifteen | Twelve | The second paragraph says so. | She was fourteen, the same age as me.
? c | What did Chloe teach the classmates? | *Some Australian songs | How to surf | English grammar | The third paragraph says so. | she taught us some Australian songs.
? t | Chloe liked durian. | F | She didn't like it at all. | she didn't like durian at all!
? t | The narrator will go to Australia next year. | T | The last paragraph says so. | Next year, I am going to Australia to stay with her family.

## The wrong size | SH
Last month, I bought a pair of trainers online. They were on sale for forty dollars, half the normal price. I chose my usual size and paid by card.

The trainers arrived after five days. I was excited, but when I tried them on, they were too small. The size on the box was correct, but this brand makes small shoes.

I went to the website and read the return policy. I could return the shoes within thirty days, but they had to be clean and in the original box. I put them back in the box and took the parcel to the post office. Sending them back cost me three dollars.

A week later, I still didn't have my money. I wrote an email to the shop. The next day, a man called me. He said sorry and told me there was a problem with their system. He sent my money back the same day and gave me a ten percent discount for my next order.

I learned a lesson: before buying shoes online, always read the reviews about the size.
? s | How much did the trainers cost? | forty dollars / 40 dollars / $40 / forty / 40 | The first paragraph says so. | They were on sale for forty dollars
? c | What was the problem with the trainers? | *They were too small | They were the wrong colour | They were damaged | The second paragraph explains. | they were too small.
? c | What did the return policy require? | *Clean shoes in the original box | A photo of the shoes | A visit to the shop | The third paragraph says so. | they had to be clean and in the original box.
? t | The return was free. | F | It cost three dollars. | Sending them back cost me three dollars.
? t | The shop gave the narrator a discount for the next order. | T | Ten percent. | gave me a ten percent discount for my next order.

## A healthier me | HE
A year ago, I felt tired all the time. I worked in an office for nine hours a day, I ate fast food for lunch, and I never did any exercise. I decided to make some changes.

First, I started walking to work. It takes thirty-five minutes, but it is better than sitting on a crowded bus. In the beginning, my legs hurt, but after two weeks it felt easy.

Second, I changed my lunch. Instead of fast food, I take food from home. I usually have rice, vegetables and some chicken or tofu. It is cheaper and much healthier.

Third, I go to bed earlier. Before, I watched videos on my phone until one o'clock in the morning. Now I put my phone away at ten thirty and read a book instead.

The results are amazing. I have more energy, I sleep better, and I have lost five kilos. My friends say I look happier. The changes were small, but together they made a big difference.
? s | How many hours a day did the narrator work in the office? | nine / 9 / nine hours | The first paragraph says so. | I worked in an office for nine hours a day
? c | How long does the walk to work take? | *Thirty-five minutes | Fifteen minutes | One hour | The second paragraph says so. | It takes thirty-five minutes
? t | The walk was easy from the first day. | F | At first the narrator's legs hurt. | In the beginning, my legs hurt
? c | What does the narrator do instead of watching videos at night? | *Reads a book | Goes for a run | Listens to music | The fourth paragraph says so. | Now I put my phone away at ten thirty and read a book instead.
? t | The narrator has lost five kilos. | T | The last paragraph says so. | I have lost five kilos.

## The best present | PF
When I was ten, I really wanted a computer game for my birthday. All my friends had it, and I talked about it every day. My parents said it was too expensive.

On my birthday, I opened my present from my parents. It was not the game. It was a big box with a telescope inside. I was very disappointed, and I didn't say thank you. My father looked sad, but he didn't say anything.

That night, he took me to the roof of our building. He set up the telescope and showed me the moon. I couldn't believe it. I could see mountains and big holes on the moon! Then he showed me Jupiter and four of its moons. They looked like tiny stars next to it.

After that night, we looked at the sky together every clear evening. My father bought a book about stars, and we learned the names of many of them.

Now I am studying science at university, and I still have that telescope. It was the best present I ever got, even if I didn't know it at first.
? c | What did the narrator want for the tenth birthday? | *A computer game | A telescope | A bike | The first paragraph says so. | I really wanted a computer game for my birthday.
? t | The narrator thanked the parents right away. | F | The narrator didn't say thank you. | I didn't say thank you.
? c | Where did the father set up the telescope? | *On the roof of the building | In the garden | At school | The third paragraph says so. | he took me to the roof of our building.
? s | How many of Jupiter's moons did they see? | four / 4 | The third paragraph says so. | Jupiter and four of its moons.
? t | The narrator is studying science at university now. | T | The last paragraph says so. | Now I am studying science at university

## Saturdays at the animal shelter | AN
Every Saturday morning, I volunteer at an animal shelter on the edge of the city. The shelter looks after about eighty dogs and forty cats. Most of them were found on the street, and some were given away by owners who couldn't keep them.

I started volunteering six months ago. On my first day, I was nervous, because some of the dogs barked a lot. But the staff explained that most dogs are just scared, not dangerous.

My main job is walking the dogs. Each dog needs to go out at least once a day, and there are not enough staff. I also clean the cages and give the animals fresh water. It is hard work, and my clothes are always dirty when I go home!

The best part is when an animal finds a new home. Last month, a family adopted an old dog called Bim. He was at the shelter for two years, and nobody wanted him because he was old. When the family took him home, all the volunteers were happy and some of us cried.

The shelter always needs more volunteers. If you love animals, it is a great way to help.
? s | How many dogs does the shelter look after? | about eighty / eighty / 80 | The first paragraph says so. | about eighty dogs and forty cats.
? c | Why was the narrator nervous on the first day? | *Some dogs barked a lot | The narrator was late | It was raining | The second paragraph explains. | some of the dogs barked a lot.
? c | What is the narrator's main job? | *Walking the dogs | Feeding the cats | Answering the phone | The third paragraph says so. | My main job is walking the dogs.
? t | Bim stayed at the shelter for two months. | F | Two years. | He was at the shelter for two years
? t | The shelter needs more volunteers. | T | The last paragraph says so. | The shelter always needs more volunteers.

## My first job at a supermarket | WK
When I was eighteen, I got my first job. I worked at a supermarket near my house three evenings a week and on Saturdays.

On my first day, the manager showed me how to use the cash register. It looked easy, but there were so many buttons! I was very slow, and a long line of customers waited at my till. One old man was angry because I made a mistake with his change. I said sorry and fixed it, but I felt terrible.

My colleague Hanh helped me a lot. She had worked there for three years, and she knew everything. She told me, "Don't worry. Everybody is slow on the first day."

After a few weeks, I was much faster. I also learned to put products on the shelves, check prices and help customers find things. I liked talking to the regular customers, especially an old woman who came every evening to buy bread and milk.

I worked at the supermarket for one year. The money helped me pay for my driving lessons. But more importantly, the job taught me to be patient and polite, even when I was tired.
? c | When did the narrator work? | *Three evenings a week and on Saturdays | Every morning | Only on Sundays | The first paragraph says so. | three evenings a week and on Saturdays.
? c | Why was the old man angry? | *The narrator made a mistake with his change | The supermarket had no bread | He waited too long outside | The second paragraph explains. | because I made a mistake with his change.
? s | How long had Hanh worked there? | three years / 3 years | The third paragraph says so. | She had worked there for three years
? t | The narrator worked at the supermarket for two years. | F | One year. | I worked at the supermarket for one year.
? t | The money helped pay for driving lessons. | T | The last paragraph says so. | The money helped me pay for my driving lessons.

## The neighbours upstairs | HF
I live in a flat on the third floor. For two years, everything was quiet. Then, last spring, a young couple moved into the flat above mine.

At first, there were no problems. But soon the noise started. Every evening, they moved furniture and walked around in hard shoes. On Fridays, they had parties with loud music until two o'clock in the morning. I couldn't sleep, and I was tired at work.

I didn't know what to do. I didn't want to have a fight with them. My friend told me to write a polite note, so I did. I explained that the noise was a problem for me and asked them to be quieter after eleven o'clock.

The next day, the couple knocked on my door. They were very embarrassed. They didn't know the floors were so thin. They said sorry and gave me a box of cakes. They also bought soft rugs for their floor.

Now we are friends. Last month, they invited me to their party, and I went! The music finished at eleven.
? s | Which floor does the narrator live on? | the third floor / third / 3rd | The first paragraph says so. | I live in a flat on the third floor.
? c | Until what time were the parties on Fridays? | *Two o'clock in the morning | Midnight | Eleven o'clock | The second paragraph says so. | until two o'clock in the morning.
? c | What did the narrator do about the noise? | *Wrote a polite note | Called the police | Moved out | The third paragraph explains. | I explained that the noise was a problem for me
? t | The couple knew the floors were thin. | F | They didn't know. | They didn't know the floors were so thin.
? t | The neighbours bought soft rugs. | T | The fourth paragraph says so. | They also bought soft rugs for their floor.

## My first concert | HS
Last month, I went to my first big concert. My favourite band was playing in our city, and my sister bought tickets for my sixteenth birthday.

The concert was in the national stadium, which holds about forty thousand people. We arrived two hours early, because we wanted to stand near the stage. There was already a very long line outside.

At eight o'clock, the lights went off and everybody screamed. Then the band came on stage. The music was so loud that I could feel it in my chest. The singer talked to the audience in Vietnamese, and everybody cheered. They played for two hours, and I knew the words to almost every song.

The best moment was the last song. Everyone turned on the lights on their phones, and the stadium looked like a sky full of stars. I will never forget it.

After the concert, the buses were very crowded, so we walked home. It took one hour, and my feet hurt. But I didn't care. It was the best night of my life.
? c | Who bought the tickets? | *The narrator's sister | The narrator | The parents | The first paragraph says so. | my sister bought tickets for my sixteenth birthday.
? s | About how many people does the stadium hold? | forty thousand / 40,000 / 40000 | The second paragraph says so. | which holds about forty thousand people.
? c | Why did they arrive early? | *To stand near the stage | To buy food | To meet the band | The second paragraph explains. | because we wanted to stand near the stage.
? t | The band played for one hour. | F | They played for two hours. | They played for two hours
? t | They walked home after the concert. | T | The buses were crowded. | so we walked home.

## Free things to do in our city | PT
Visiting a city can be expensive, but there are many free things to do in our city. Here are some ideas.

The city park is a great place to start. In the morning, you can watch people doing exercise, dancing and playing badminton. On Sundays, there is free music near the lake from four to six in the afternoon.

The old market is free to enter, and it is full of colour and life. Even if you don't buy anything, it is interesting to walk around and see the fruit, flowers and street food. Go early in the morning, when it is busiest.

Many museums are free on the first Sunday of every month. The art museum has paintings by famous Vietnamese artists, and the history museum has old objects from many centuries.

Finally, walk along the river at sunset. The view is beautiful, and many local families come here to relax. There are often street performers too.

With a little planning, you can enjoy the city without spending much money. Just bring comfortable shoes and a bottle of water.
? c | When is there free music near the lake? | *On Sundays from four to six | Every evening | On Saturdays at noon | The second paragraph says so. | On Sundays, there is free music near the lake from four to six in the afternoon.
? c | When is the old market busiest? | *Early in the morning | At lunchtime | In the evening | The third paragraph says so. | Go early in the morning, when it is busiest.
? t | Museums are free every day. | F | They are free on the first Sunday of every month. | Many museums are free on the first Sunday of every month.
? s | When is the best time to walk along the river? | at sunset / sunset | The fifth paragraph says so. | walk along the river at sunset.
? t | The text says you need a lot of money to enjoy the city. | F | You can enjoy it without spending much. | you can enjoy the city without spending much money.

## News from the language school | ED
Dear students,

We have some important news about next term.

First, classes will start on Monday the fifth of September, not on the first as we said before. We are painting the classrooms, and the work will not be finished in time.

Second, we are opening two new courses. There will be a conversation class for adults on Tuesday and Thursday evenings, and an exam preparation class on Saturday mornings. Each class will have a maximum of twelve students, so please register early.

Third, our library now has more than five hundred new books, including easy readers for beginners. Students can borrow up to three books at a time for two weeks.

Finally, the price of our courses will stay the same this year. Students who register before the twentieth of August will get a ten percent discount.

If you have any questions, please contact the office by phone or email. The office is open from eight in the morning to six in the evening, Monday to Friday.

Best wishes,
The Sunrise Language School
? c | Why will classes start later? | *The classrooms are being painted | A teacher is ill | It is a holiday | The second paragraph explains. | We are painting the classrooms
? s | What is the maximum number of students in each new class? | twelve / 12 | The third paragraph says so. | Each class will have a maximum of twelve students
? c | How many books can students borrow at a time? | *Up to three | Up to five | Only one | The fourth paragraph says so. | Students can borrow up to three books at a time
? t | Course prices will go up this year. | F | They will stay the same. | the price of our courses will stay the same this year.
? t | Early registration gives a ten percent discount. | T | Before the twentieth of August. | will get a ten percent discount.

## Losing my phone | TE
Last Friday, I lost my phone. I was on a crowded bus, and when I got off, I put my hand in my pocket. My phone wasn't there.

I felt sick. My whole life was on that phone: my photos, my contacts, my bank app and my notes for my exam the next week. I ran to the bus company office, but nobody had found it.

When I got home, I used my laptop to log into my account. I could see my phone on a map! It was still on the bus, which was now on the other side of the city. I called the bus company again and told them the bus number and the seat. Thirty minutes later, they called me back. The driver had found the phone under a seat.

The next morning, I picked it up from the bus station. I was so relieved. I bought the driver a coffee to say thank you.

After that day, I made some changes. I back up my photos every week, and I always keep my phone in my bag, not in my pocket.
? c | Where did the narrator lose the phone? | *On a crowded bus | In a café | At school | The first paragraph says so. | I was on a crowded bus
? c | How did the narrator find where the phone was? | *By seeing it on a map on the laptop | By calling it | By asking the police | The third paragraph explains. | I could see my phone on a map!
? s | Where did the driver find the phone? | under a seat / under the seat | The third paragraph says so. | The driver had found the phone under a seat.
? t | The narrator gave the driver some money. | F | The narrator bought the driver a coffee. | I bought the driver a coffee to say thank you.
? t | The narrator now backs up photos every week. | T | The last paragraph says so. | I back up my photos every week

## Saving for a trip to Japan | MS
For two years, my dream was to visit Japan. I wanted to see the cherry blossoms in spring and try real Japanese food. But the trip was expensive. I needed about two thousand dollars.

I made a plan. First, I opened a savings account and put in one hundred dollars every month from my salary. Second, I stopped buying coffee every morning. I made coffee at home instead, and I saved about thirty dollars a month.

I also started selling things I didn't need. I sold old clothes, books and a guitar I never played. That gave me two hundred dollars.

It wasn't always easy. Sometimes my friends went to expensive restaurants, and I stayed at home. But I kept looking at photos of Japan to stay motivated.

Finally, after eighteen months, I had enough money. Last April, I spent ten days in Japan. I saw the cherry blossoms in Kyoto, ate fresh sushi and stayed in a traditional house. It was even better than I imagined, and I was proud that I saved for it myself.
? s | How much money did the narrator need? | about two thousand dollars / two thousand dollars / $2000 / 2000 | The first paragraph says so. | I needed about two thousand dollars.
? c | How did the narrator save on coffee? | *Made coffee at home | Drank tea instead | Stopped drinking coffee | The second paragraph explains. | I made coffee at home instead
? c | How much did selling old things give the narrator? | *Two hundred dollars | One hundred dollars | Thirty dollars | The third paragraph says so. | That gave me two hundred dollars.
? t | Saving was always easy. | F | It wasn't always easy. | It wasn't always easy.
? t | The narrator saw cherry blossoms in Kyoto. | T | The last paragraph says so. | I saw the cherry blossoms in Kyoto

## A wet weekend in Sa Pa | NW
Last October, my friends and I went to Sa Pa for a weekend of hiking. We booked a guide and planned to walk to some villages in the mountains.

Unfortunately, the weather was terrible. It rained heavily on Saturday morning, and the paths were very muddy. Our guide, a young woman called Mai, said it was too dangerous to walk the long route. We were disappointed, but we agreed.

Instead, Mai took us to her village by car. We visited her family's house, and her grandmother showed us how to make traditional cloth. It took her many hours to make a small piece, and the colours were beautiful. I bought a scarf to take home.

In the afternoon, the rain stopped for a while. We walked for an hour through rice terraces. The clouds moved across the mountains, and the view was amazing.

On Sunday, it rained again, so we spent the day in cafés in the town. The trip was not what we planned, but it was still wonderful. Sometimes bad weather gives you different experiences.
? c | What did the friends plan to do in Sa Pa? | *Hike to villages in the mountains | Go skiing | Visit museums | The first paragraph says so. | planned to walk to some villages in the mountains.
? c | Why didn't they walk the long route? | *It was too dangerous because of rain and mud | The guide was ill | They were too tired | The second paragraph explains. | it was too dangerous to walk the long route.
? s | What did the narrator buy? | a scarf / scarf | The third paragraph says so. | I bought a scarf to take home.
? t | It was sunny all day on Sunday. | F | It rained again on Sunday. | On Sunday, it rained again
? t | The narrator still enjoyed the trip. | T | It was still wonderful. | it was still wonderful.

## My favourite teacher | ED
The teacher I remember best is Mr. Quang. He taught us history when I was in grade nine. Before his class, I thought history was boring. It was just dates and names that I had to remember for tests.

Mr. Quang changed that. He didn't just read from the textbook. He told stories about real people from the past, how they lived, what they ate and what they were afraid of. Sometimes he brought old objects to class, like coins or letters, and let us hold them.

He also asked us to interview our grandparents about their lives. I talked to my grandfather for three hours about his childhood. I learned things about my family that I never knew.

Mr. Quang was strict about homework, but he was always fair. If we didn't understand something, he explained it again with a smile.

Thanks to him, I chose to study history at university. Last year, I became a history teacher myself. I try to teach my students the way Mr. Quang taught me.
? c | What did the narrator think of history before Mr. Quang's class? | *It was boring | It was exciting | It was very difficult | The first paragraph says so. | I thought history was boring.
? c | What did Mr. Quang sometimes bring to class? | *Old objects like coins or letters | Films | Maps only | The second paragraph says so. | Sometimes he brought old objects to class, like coins or letters
? s | How long did the narrator talk to the grandfather? | three hours / 3 hours | The third paragraph says so. | I talked to my grandfather for three hours
? t | Mr. Quang was not strict about homework. | F | He was strict about homework. | Mr. Quang was strict about homework
? t | The narrator is now a history teacher. | T | The last paragraph says so. | Last year, I became a history teacher myself.

## A street food tour | FD
When my friend Sarah visited Viet Nam, I took her on a street food tour in my city. I wanted to show her that the best food is often not in expensive restaurants.

We started at six in the evening at a small stall that sells grilled pork with rice noodles. Sarah loved it, but she said the chilli sauce was very hot! Next, we tried banh xeo, a crispy pancake with prawns and bean sprouts. You eat it with lettuce and dip it in fish sauce.

Then we walked to a famous dessert stall. We had che, a sweet dessert with beans, coconut milk and ice. Sarah said it was strange at first, but she finished the whole glass.

Our last stop was a coffee shop on the pavement. We sat on tiny plastic chairs and drank iced coffee with milk. Sarah laughed, because the chairs were so small.

The whole tour cost less than fifteen dollars for both of us. Sarah said it was her favourite evening in Viet Nam, and she took photos of every dish.
? s | What time did the tour start? | six in the evening / six / 6 pm / 6 | The second paragraph says so. | We started at six in the evening
? c | What did Sarah say about the chilli sauce? | *It was very hot | It was sweet | It was too salty | The second paragraph says so. | she said the chilli sauce was very hot!
? c | What is che? | *A sweet dessert with beans, coconut milk and ice | A crispy pancake | A type of coffee | The third paragraph explains. | a sweet dessert with beans, coconut milk and ice.
? t | The tour cost more than fifty dollars. | F | Less than fifteen dollars for both. | The whole tour cost less than fifteen dollars for both of us.
? t | Sarah took photos of every dish. | T | The last paragraph says so. | she took photos of every dish.

## The city's new bikes | TP
Last year, our city started a bike-sharing scheme. There are now three hundred blue bicycles at forty stations around the city centre.

Using the bikes is easy. You download an app, register with your phone number and add some money. Then you scan the code on a bike, and it unlocks. When you finish, you leave the bike at any station.

The price is low. The first thirty minutes cost only fifty cents, and every extra thirty minutes costs another fifty cents. Students get a fifty percent discount.

Many people use the bikes to go to work or school. Tourists also like them, because they can visit different parts of the city easily. Some people say the bikes are better than taxis for short trips, because they don't get stuck in traffic.

However, there are some problems. Some stations are always empty in the morning, and others are full in the evening. The city is planning to add more stations next year. It also wants to build more bike lanes, because many riders say the roads are dangerous.
? s | How many bicycles are there? | three hundred / 300 | The first paragraph says so. | There are now three hundred blue bicycles
? c | How do you unlock a bike? | *Scan the code with the app | Use a key | Pay at a machine | The second paragraph explains. | you scan the code on a bike, and it unlocks.
? c | How much do the first thirty minutes cost? | *Fifty cents | One dollar | They are free | The third paragraph says so. | The first thirty minutes cost only fifty cents
? t | Students pay the full price. | F | They get a fifty percent discount. | Students get a fifty percent discount.
? t | Some riders think the roads are dangerous. | T | The last paragraph says so. | many riders say the roads are dangerous.
"""

PASSAGES["A2"] += """
## Working at a hotel reception | WK
After I finished high school, I got a job at the reception desk of a hotel in Da Nang. The hotel has eighty rooms, and most of the guests are tourists from other countries.

My job is to welcome guests, check them in and out, and answer their questions. I work in shifts. One week I work from six in the morning to two in the afternoon, and the next week I work from two to ten in the evening.

The job is never boring. Guests ask me about everything: the best beaches, cheap restaurants, how to get to the airport and where to buy medicine. I have learned a lot about my own city because of their questions.

My English has improved a lot too. At first, I was nervous when I spoke to foreign guests. Now I feel much more confident. I am also learning some Korean, because many of our guests come from Korea.

The hardest part is when guests are angry. Last month, a man shouted at me because his room was not ready. I stayed calm, said sorry and gave him a free drink while he waited. Later, he came back and thanked me.
? s | How many rooms does the hotel have? | eighty / 80 / eighty rooms | The first paragraph says so. | The hotel has eighty rooms
? c | What are the narrator's working hours? | *Shifts that change every week | Nine to five every day | Only at night | The second paragraph explains. | I work in shifts.
? c | Why is the narrator learning Korean? | *Many guests come from Korea | The manager asked | The narrator wants to move to Korea | The fourth paragraph explains. | because many of our guests come from Korea.
? t | The narrator got angry with the guest who shouted. | F | The narrator stayed calm. | I stayed calm
? t | The angry guest later thanked the narrator. | T | The last paragraph says so. | Later, he came back and thanked me.

## Learning to drive | TP
I started driving lessons three months ago, when I was eighteen. My father wanted to teach me, but after one lesson we argued, so I decided to go to a driving school.

My instructor is called Mr. Bao. He is very patient and never shouts, even when I make mistakes. In the first lessons, we practised in a large empty car park. I learned how to start the car, change gears and stop smoothly.

After a month, we started driving on real roads. It was very scary! There were motorbikes everywhere, and I had to watch all the mirrors at the same time. Once, I stopped the engine in the middle of a busy junction, and everyone behind me started using their horns.

The most difficult thing for me is parking. I have practised it many times, but I still need three or four tries to park between two cars.

My driving test is next month. There is a theory test on a computer and a practical test on the road. I am nervous, but Mr. Bao says I am ready. If I pass, my parents will let me drive their car at the weekend.
? c | Why did the narrator go to a driving school? | *The narrator and the father argued during a lesson | The father was too busy | It was cheaper | The first paragraph explains. | after one lesson we argued, so I decided to go to a driving school.
? c | Where did the first lessons take place? | *In a large empty car park | On the motorway | In the city centre | The second paragraph says so. | we practised in a large empty car park.
? t | Mr. Bao often shouts at the narrator. | F | He never shouts. | He is very patient and never shouts
? s | What is the most difficult thing for the narrator? | parking | The fourth paragraph says so. | The most difficult thing for me is parking.
? t | The driving test has two parts. | T | A theory test and a practical test. | There is a theory test on a computer and a practical test on the road.

## My cousin's wedding | PF
Last Saturday, I went to my cousin Lan's wedding. It was the biggest party I have ever been to. More than three hundred guests came.

In the morning, there was a small traditional ceremony at the bride's house. Only close family members were there. The groom's family brought gifts on red trays: fruit, cakes, tea and betel leaves. Then the couple prayed in front of the family altar.

In the evening, there was a big party at a restaurant. The bride wore a beautiful white dress, and the groom wore a dark suit. There were ten courses of food, including seafood, roast chicken and a huge wedding cake.

During the party, the couple walked to every table to thank the guests. Many people gave money in red envelopes as a wedding present. There was also live music, and my uncle sang an old love song. He was not a good singer, but everybody clapped.

The party finished at ten o'clock. I was very tired, but I was happy to see my cousin so happy. Next year, it's my sister's turn to get married!
? s | How many guests came? | more than three hundred / over three hundred / three hundred / 300 | The first paragraph says so. | More than three hundred guests came.
? c | Who was at the morning ceremony? | *Only close family members | All the guests | Only the couple | The second paragraph says so. | Only close family members were there.
? c | How many courses of food were there? | *Ten | Five | Twenty | The third paragraph says so. | There were ten courses of food
? t | The narrator's uncle sang very well. | F | He was not a good singer. | He was not a good singer
? t | The narrator's sister will get married next year. | T | The last paragraph says so. | Next year, it's my sister's turn to get married!

## Floods in our street | NW
Every year in October, the rainy season brings heavy rain to our city. This year, the rain was the worst for many years.

On Tuesday afternoon, it started to rain very hard. It rained for six hours without stopping. By the evening, the water in our street was almost knee-high. Motorbikes stopped working in the water, and people had to push them home.

Our house is a little higher than the street, so the water didn't come inside. But our neighbours were not so lucky. The water entered their living room, and they had to move their furniture upstairs. My father and I went to help them. We carried their sofa, their television and some boxes up the stairs.

The next morning, the water went down. The street was full of mud and rubbish. Everyone on our street came out to clean it together. Some people brought brooms, and others brought buckets of clean water.

The city says it will build bigger drains next year. I hope it helps, because the floods are getting worse every year.
? c | When does the rainy season bring heavy rain? | *Every year in October | Every year in June | Only this year | The first paragraph says so. | Every year in October
? s | How long did it rain without stopping? | six hours / 6 hours | The second paragraph says so. | It rained for six hours without stopping.
? t | The water came into the narrator's house. | F | The house is higher than the street. | so the water didn't come inside.
? c | What did the narrator and father carry upstairs? | *The neighbours' sofa, television and boxes | Their own furniture | Bags of rice | The third paragraph says so. | We carried their sofa, their television and some boxes up the stairs.
? t | The city plans to build bigger drains. | T | The last paragraph says so. | The city says it will build bigger drains next year.

## A charity run | HS
Last Sunday, I ran my first five-kilometre race. It was a charity run to raise money for a children's hospital. About two thousand people took part.

I started training two months before the race. At first, I could only run for ten minutes without stopping. I followed a plan from an app. I ran three times a week, a little longer each time. After six weeks, I could run five kilometres.

On the day of the race, I woke up at five o'clock. The race started at six thirty, before it got too hot. There were runners of all ages, from children to grandparents. Some people wore funny costumes. One man ran dressed as a banana!

I finished the race in thirty-four minutes. I wasn't fast, but I didn't stop once, and I was very proud of myself. At the finish line, volunteers gave us water and a medal.

The race raised more than fifty thousand dollars for the hospital. My friends and family gave me two hundred dollars. Now I'm planning to run ten kilometres next year.
? c | What was the race for? | *To raise money for a children's hospital | To choose a national team | To celebrate a festival | The first paragraph says so. | to raise money for a children's hospital.
? c | How often did the narrator train? | *Three times a week | Every day | Once a week | The second paragraph says so. | I ran three times a week
? s | How long did it take the narrator to finish? | thirty-four minutes / 34 minutes | The fourth paragraph says so. | I finished the race in thirty-four minutes.
? t | The narrator stopped several times during the race. | F | The narrator didn't stop once. | I didn't stop once
? t | The narrator plans to run ten kilometres next year. | T | The last paragraph says so. | Now I'm planning to run ten kilometres next year.

## Choosing a university | ED
Next year, I will finish high school, and I need to choose a university. It is a big decision, and I am not sure what to do.

My parents want me to study medicine. My mother is a doctor, and she says it is a stable job that helps people. But I am not very good at biology, and I faint when I see blood!

I am more interested in graphic design. I love drawing, and I spend hours designing posters and logos on my computer. Last year, I won a design competition at my school. But my father worries that it is difficult to find a good job in design.

Last month, I visited two universities. At the design school, the students showed me their projects, and I was very excited. At the medical school, the buildings were modern, but I didn't feel the same excitement.

My teacher gave me good advice. She said, "Choose something you enjoy, because you will study it for four or five years." I am going to talk to my parents again this weekend and show them my design work.
? c | What do the narrator's parents want the narrator to study? | *Medicine | Design | Business | The second paragraph says so. | My parents want me to study medicine.
? c | Why is medicine difficult for the narrator? | *The narrator faints at the sight of blood | It is too expensive | The narrator doesn't like the school | The second paragraph explains. | I faint when I see blood!
? t | The narrator won a design competition last year. | T | The third paragraph says so. | Last year, I won a design competition at my school.
? s | How many universities did the narrator visit? | two / 2 | The fourth paragraph says so. | Last month, I visited two universities.
? t | The teacher advised choosing the subject with the best salary. | F | She advised choosing something enjoyable. | Choose something you enjoy

## A cooking class in Hoi An | FD
When I visited Hoi An last spring, I took a cooking class. It was the best thing I did on my holiday.

The class started at eight in the morning at the local market. Our teacher, Mrs. Phuong, showed us how to choose fresh vegetables, herbs and fish. She told us that local people go to the market every day, because they like to cook with fresh food.

Then we took a small boat along the river to her cooking school. It was in a beautiful garden full of herbs. There were eight students in the class, from five different countries.

We cooked four dishes: spring rolls, a green papaya salad, fish in a clay pot and a soup. Mrs. Phuong explained every step, and she helped us when we made mistakes. My spring rolls were not very pretty, but they tasted good!

At the end, we sat together and ate everything we cooked. Mrs. Phuong gave us a small book with all the recipes. Since I came home, I have made the fish in a clay pot three times for my family.
? c | Where did the class start? | *At the local market | At the cooking school | On a boat | The second paragraph says so. | The class started at eight in the morning at the local market.
? c | How did they get to the cooking school? | *By boat along the river | By bus | On foot | The third paragraph says so. | we took a small boat along the river to her cooking school.
? s | How many dishes did they cook? | four / 4 / four dishes | The fourth paragraph says so. | We cooked four dishes
? t | The narrator's spring rolls looked perfect. | F | They were not very pretty. | My spring rolls were not very pretty
? t | The narrator has cooked fish in a clay pot at home. | T | Three times. | I have made the fish in a clay pot three times for my family.

## The second-hand shop | SH
There is a second-hand shop near my university. It sells used clothes, books, furniture and kitchen things. Everything in the shop was given by people who didn't need it any more.

I discovered the shop when I moved into my first flat. I needed a lot of things, but I didn't have much money. In the shop, I found a small table for five dollars, two chairs for eight dollars and a set of plates for three dollars. Everything was clean and in good condition.

The shop is run by volunteers. The money goes to a charity that helps old people who live alone. So when you buy something, you also help other people.

Now I go there almost every month. Last week, I bought a warm winter jacket for six dollars. In a normal shop, it would cost more than fifty. I also give things to the shop, like clothes that are too small for me.

Some of my friends think second-hand things are dirty or old-fashioned. I don't agree. Buying second-hand saves money, and it is good for the environment, because fewer things are thrown away.
? c | Where do the things in the shop come from? | *People who didn't need them any more | Factories | Other countries | The first paragraph says so. | Everything in the shop was given by people who didn't need it any more.
? s | How much did the small table cost? | five dollars / 5 dollars / $5 / five / 5 | The second paragraph says so. | I found a small table for five dollars
? c | Who does the shop's money help? | *Old people who live alone | Students | Animals | The third paragraph says so. | a charity that helps old people who live alone.
? t | The winter jacket cost more than fifty dollars. | F | It cost six dollars. | I bought a warm winter jacket for six dollars.
? t | The narrator thinks buying second-hand is good for the environment. | T | The last paragraph says so. | it is good for the environment

## A note for my new flatmate | HF
Hi Jenny,

Welcome to the flat! I'm sorry I'm not here today. I'm visiting my parents, and I'll be back on Sunday evening. Here are some things you need to know.

Your room is the one at the end of the hall, next to the bathroom. I cleaned it yesterday, and there are clean sheets on the bed. The window is a little difficult to open, so push it hard.

The kitchen is for both of us. Your shelf in the fridge is the bottom one. Please wash your dishes after you use them. I hate a full sink!

The rubbish goes out on Tuesday and Friday mornings. Please put plastic and paper in the blue bin and food in the green bin.

The Wi-Fi password is on a card next to the TV. If the internet stops working, turn the router off and on again. It usually works.

There is a good supermarket two minutes away, on the left after the traffic lights. I've left some milk and bread for you.

See you on Sunday!
Mai
? c | Why isn't Mai at the flat? | *Mai is visiting her parents | Mai is working | Mai is on holiday abroad | The first paragraph explains. | I'm visiting my parents
? c | Where is Jenny's room? | *At the end of the hall, next to the bathroom | Next to the kitchen | Upstairs | The second paragraph says so. | Your room is the one at the end of the hall, next to the bathroom.
? s | Which shelf in the fridge is Jenny's? | the bottom one / bottom / the bottom shelf | The third paragraph says so. | Your shelf in the fridge is the bottom one.
? t | Food goes in the blue bin. | F | Food goes in the green bin. | food in the green bin.
? t | Mai has left some milk and bread for Jenny. | T | The last paragraph says so. | I've left some milk and bread for you.

## Recycling in our building | EN
Our apartment building has two hundred flats. Until last year, all the rubbish went into one big room on the ground floor. It smelled terrible, and nothing was recycled.

Then a group of residents decided to change things. They had a meeting with the building manager and suggested a recycling system. The manager agreed, and now there are four different bins: one for paper, one for plastic, one for glass and metal, and one for food waste.

At first, many people didn't use the new bins correctly. They put plastic bags in the paper bin and food in the plastic bin. So the group made colourful posters with pictures and put them in the lifts. They also knocked on every door to explain the system.

Now, after one year, most people recycle. The amount of normal rubbish has gone down by almost half. The food waste is made into compost, and the building uses it in the small garden on the roof.

My mother is part of the recycling group. She says the biggest change is not the bins, but the way neighbours talk to each other now.
? s | How many flats are in the building? | two hundred / 200 | The first paragraph says so. | Our apartment building has two hundred flats.
? c | How many different bins are there now? | *Four | Two | Six | The second paragraph says so. | now there are four different bins
? c | Where did the group put the posters? | *In the lifts | On the front door only | In every flat | The third paragraph says so. | put them in the lifts.
? t | The amount of normal rubbish has doubled. | F | It has gone down by almost half. | The amount of normal rubbish has gone down by almost half.
? t | Compost from food waste is used in a roof garden. | T | The fourth paragraph says so. | the building uses it in the small garden on the roof.

## A day without my phone | TE
Last Saturday, I tried an experiment. I didn't use my phone for a whole day. I wanted to see how much I really needed it.

In the morning, I felt strange. I usually check my messages before I get out of bed. Instead, I opened the window and listened to the birds. At breakfast, I talked to my parents instead of reading the news on my phone. My mother was surprised. "You're very chatty today," she said.

In the afternoon, I wanted to meet my friend Long. I couldn't send him a message, so I walked to his house. He was at home, and we played chess for two hours. We laughed a lot.

The hardest moment was in the evening. I wanted to know the result of a football match, and I felt very nervous about missing news. But I read a book and went to bed early.

The next day, I had forty messages. Most of them were not important at all. I learned that I don't need my phone as much as I think. Now I try to have one phone-free afternoon every week.
? c | What did the narrator do instead of checking messages in the morning? | *Opened the window and listened to the birds | Read the news | Went running | The second paragraph says so. | I opened the window and listened to the birds.
? c | Why did the narrator walk to Long's house? | *The narrator couldn't send a message | Long was ill | The bus was late | The third paragraph explains. | I couldn't send him a message, so I walked to his house.
? s | How long did they play chess? | two hours / 2 hours | The third paragraph says so. | we played chess for two hours.
? t | Most of the forty messages were important. | F | Most were not important. | Most of them were not important at all.
? t | The narrator now has one phone-free afternoon a week. | T | The last paragraph says so. | Now I try to have one phone-free afternoon every week.

## The town festival | DL
Every year in September, my town has a festival to celebrate the end of the harvest. It lasts for three days, and people come from nearby villages to join the fun.

On the first day, there is a parade through the main street. Farmers decorate their carts with rice, fruit and flowers, and children in traditional clothes walk behind them playing drums.

On the second day, there are competitions. There is a cooking competition, a boat race on the river and a contest for the biggest pumpkin. Last year, my grandfather's pumpkin won second prize. It weighed more than forty kilos!

On the last evening, everybody meets in the town square. There is a big dinner with long tables, and families share food with each other. After dinner, there is music and dancing, and at ten o'clock there are fireworks over the river.

I love the festival because the whole town feels like one big family. Even people who moved to the city come back for it. This year, I am going to help my grandfather grow an even bigger pumpkin.
? s | How long does the festival last? | three days / 3 days | The first paragraph says so. | It lasts for three days
? c | What happens on the first day? | *A parade through the main street | A boat race | Fireworks | The second paragraph says so. | On the first day, there is a parade through the main street.
? c | What prize did the grandfather's pumpkin win? | *Second prize | First prize | No prize | The third paragraph says so. | my grandfather's pumpkin won second prize.
? t | The fireworks are at midnight. | F | They are at ten o'clock. | at ten o'clock there are fireworks over the river.
? t | People who moved to the city come back for the festival. | T | The last paragraph says so. | Even people who moved to the city come back for it.

## Visiting a friend in hospital | HE
Last week, my best friend Nam broke his leg playing football. He had an operation and had to stay in hospital for five days.

On Wednesday after school, I went to visit him with two classmates. We weren't sure what to bring. Flowers seemed strange for a boy, so we bought some fruit, a comic book and a card that everyone in our class signed.

The hospital was big and busy. A nurse at the front desk told us Nam was in room 302 on the third floor. When we arrived, he was watching TV and looked bored. His leg was in a white cast from his foot to his knee.

He was very happy to see us. We told him about everything that happened at school, and he laughed at our stories about the new maths teacher. We also wrote jokes and drew pictures on his cast.

After an hour, a nurse came in and said Nam needed to rest. Before we left, he asked us to bring his homework next time. That really surprised us! Nam says he will be back at school in two weeks, using crutches.
? c | How did Nam break his leg? | *Playing football | Falling off a bike | In a car accident | The first paragraph says so. | broke his leg playing football.
? c | Why didn't they bring flowers? | *Flowers seemed strange for a boy | Flowers were too expensive | The hospital didn't allow them | The second paragraph explains. | Flowers seemed strange for a boy
? s | Which floor was Nam's room on? | the third floor / third / 3rd | The third paragraph says so. | Nam was in room 302 on the third floor.
? t | The visitors wrote jokes on Nam's cast. | T | The fourth paragraph says so. | We also wrote jokes and drew pictures on his cast.
? t | Nam asked them not to talk about homework. | F | He asked them to bring it. | he asked us to bring his homework next time.

## My uncle's restaurant | WK
My uncle opened a small restaurant ten years ago. It serves noodle soup, and it is famous in our neighbourhood. Every morning, people wait in line to eat there.

My uncle's day starts at three in the morning. He makes the soup himself, and it takes six hours to cook the broth with beef bones, onions and spices. He says this is the secret: you can't make good soup quickly.

The restaurant opens at six and closes at two in the afternoon, when the soup is finished. There are four workers: my uncle, my aunt and two young cooks. My aunt takes the orders and the money, and she remembers what every regular customer likes.

During the summer holidays, I help at the restaurant. I wash bowls, clean tables and bring drinks to customers. It's hard work, and my uncle is strict. But he pays me well, and I eat a free bowl of soup every day!

My uncle works very hard, but he loves his job. He says the best moment is when a customer finishes the soup and says, "Delicious."
? s | How long ago did the uncle open the restaurant? | ten years ago / ten years / 10 years | The first paragraph says so. | My uncle opened a small restaurant ten years ago.
? c | How long does it take to cook the broth? | *Six hours | Two hours | All day | The second paragraph says so. | it takes six hours to cook the broth
? c | When does the restaurant close? | *At two in the afternoon | At midnight | At six in the evening | The third paragraph says so. | closes at two in the afternoon, when the soup is finished.
? t | The narrator works at the restaurant all year. | F | Only during the summer holidays. | During the summer holidays, I help at the restaurant.
? t | The narrator gets a free bowl of soup every day. | T | The fourth paragraph says so. | I eat a free bowl of soup every day!

## Lost in Bangkok | TR
On the second day of my holiday in Bangkok, I decided to explore the city alone. My hotel was near the river, and I wanted to visit a famous temple about two kilometres away.

I didn't take a map because I thought my phone was enough. But after one hour, my phone battery died. I was in a small street full of shops, and I didn't know where I was. Every street looked the same.

I tried to ask for directions, but many people didn't speak English, and I didn't speak Thai. Then I saw a small café. The owner was a young woman who spoke a little English. I showed her the name of my hotel on the hotel card in my wallet.

She drew a simple map on a napkin and pointed the way. She also let me charge my phone for twenty minutes while I drank an iced tea. It was the best iced tea I have ever had!

I found the temple that afternoon, and I got back to my hotel before dark. Now I always carry a small battery and the hotel card when I travel.
? c | Where did the narrator want to go? | *A famous temple | A shopping centre | The airport | The first paragraph says so. | I wanted to visit a famous temple about two kilometres away.
? c | What happened to the phone? | *The battery died | It was stolen | It fell in the river | The second paragraph says so. | my phone battery died.
? s | What did the café owner draw the map on? | a napkin / napkin | The fourth paragraph says so. | She drew a simple map on a napkin
? t | The narrator didn't find the temple. | F | The narrator found it that afternoon. | I found the temple that afternoon
? t | The narrator now carries a small battery when travelling. | T | The last paragraph says so. | Now I always carry a small battery and the hotel card when I travel.

## The old cinema | PT
In the centre of our town, there is an old cinema called The Star. It opened in 1965, and for many years it was the most popular place in town.

When my parents were young, they went to The Star every Saturday night. Tickets were cheap, and the cinema had nine hundred seats. My father says it was always full, and people sometimes sat on the stairs.

But twenty years ago, a modern cinema opened in the new shopping centre. It had comfortable seats and the newest films. Fewer and fewer people went to The Star, and in 2010 it closed.

For many years, the building was empty. Then, last year, a group of young people bought it. They cleaned it, repaired the roof and painted the walls. Now it is open again, but it is different. It shows old films and films by young local directors. There is also a café and a small room for concerts.

My parents went there last month for the first time in thirty years. My mother said she felt young again. The building is old, but now it is full of life.
? s | When did The Star open? | 1965 / in 1965 | The first paragraph says so. | It opened in 1965
? c | How many seats did the cinema have? | *Nine hundred | Three hundred | Two thousand | The second paragraph says so. | the cinema had nine hundred seats.
? c | Why did fewer people go to The Star? | *A modern cinema opened in the shopping centre | Tickets became expensive | The roof was broken | The third paragraph explains. | a modern cinema opened in the new shopping centre.
? t | The new owners show only the newest films. | F | They show old films and local films. | It shows old films and films by young local directors.
? t | The narrator's mother felt young again at the cinema. | T | The last paragraph says so. | My mother said she felt young again.

## Adopting a cat | AN
For a long time, I wanted a pet, but my flat is small, and I work all day. A dog needs a lot of time and walks, so I decided to adopt a cat.

I didn't want to buy a cat from a shop. There are many cats without homes, so I went to an animal rescue centre. The centre had more than thirty cats, from small kittens to old cats.

I wanted a kitten at first, but a volunteer told me that kittens need a lot of attention and can damage furniture. She showed me an adult cat called Pepper. Pepper was four years old, black and very calm. She came to me and sat on my feet. I knew she was the right cat.

Before I could take Pepper home, the centre asked me many questions about my flat and my job. They also visited my flat to check it was safe. Adopting her cost thirty dollars, and that included her vaccinations.

Pepper has lived with me for six months now. She sleeps most of the day, and when I come home from work, she runs to the door. She has made my small flat feel like a real home.
? c | Why did the narrator choose a cat, not a dog? | *A dog needs a lot of time and walks | The narrator is afraid of dogs | Dogs are not allowed | The first paragraph explains. | A dog needs a lot of time and walks
? s | How many cats did the centre have? | more than thirty / over thirty / thirty / 30 | The second paragraph says so. | The centre had more than thirty cats
? c | Why did the volunteer not recommend a kitten? | *Kittens need a lot of attention and can damage furniture | Kittens are expensive | Kittens are often ill | The third paragraph explains. | kittens need a lot of attention and can damage furniture.
? t | Adopting Pepper was free. | F | It cost thirty dollars. | Adopting her cost thirty dollars
? t | The centre visited the narrator's flat. | T | The fourth paragraph says so. | They also visited my flat to check it was safe.

## A weekend job at the market | MS
Every Saturday and Sunday, I work at my aunt's fruit stall at the market. I started last year, when I was fifteen. I wanted to earn my own money.

The market opens at five in the morning, so I have to get up at half past four. It's hard, especially in winter, when it's still dark and cold. My aunt drives us to the market in her small truck full of fruit.

My job is to arrange the fruit, help customers and weigh the fruit on the scales. At first, I was slow with the money, and I made mistakes. Now I can calculate the change in my head very quickly. My maths teacher says my mental maths has improved a lot!

I earn twenty dollars each weekend. I save half of it in the bank, and I spend the other half on things I like, such as books and going out with friends.

The job has taught me a lot. I talk to many different people, and I've learned that customers come back when you are friendly and honest. My aunt says that when I finish school, I can help her with the business.
? c | Why did the narrator start working? | *To earn their own money | Because the aunt was ill | For a school project | The first paragraph explains. | I wanted to earn my own money.
? s | What time does the narrator get up? | half past four / 4:30 / four thirty | The second paragraph says so. | I have to get up at half past four.
? t | The narrator was fast with money from the start. | F | At first the narrator was slow. | At first, I was slow with the money
? c | How much does the narrator earn each weekend? | *Twenty dollars | Ten dollars | Fifty dollars | The fourth paragraph says so. | I earn twenty dollars each weekend.
? t | The narrator saves half of the money. | T | The fourth paragraph says so. | I save half of it in the bank

## My English diary | ED
Six months ago, my English teacher gave our class some advice. She said, "Write a diary in English. Write just five sentences every day." Most of my classmates forgot about it after a week, but I continued.

At first, it was difficult. I didn't know many words, and my sentences were very simple: "Today I went to school. I ate rice. It was hot." I often used a dictionary, and it took me twenty minutes to write five sentences.

After a few weeks, it became easier. I started to write about my feelings and my plans, not only about what I did. I also started to use new words and phrases from my lessons. Sometimes I wrote a whole page!

Every Friday, I showed my diary to my teacher. She didn't correct every mistake. Instead, she underlined two or three mistakes and wrote a short comment. That helped me a lot.

Now my writing is much better, and I got the highest mark in my class in the last writing test. I also understand myself better, because writing helps me think. I'm going to keep my diary for as long as I can.
? s | How many sentences did the teacher suggest writing every day? | five / 5 / five sentences | The first paragraph says so. | Write just five sentences every day.
? c | What happened to most classmates? | *They forgot after a week | They wrote every day | They wrote in Vietnamese | The first paragraph says so. | Most of my classmates forgot about it after a week
? c | How long did five sentences take at first? | *Twenty minutes | Five minutes | One hour | The second paragraph says so. | it took me twenty minutes to write five sentences.
? t | The teacher corrected every mistake. | F | She underlined two or three. | She didn't correct every mistake.
? t | The narrator got the highest mark in the last writing test. | T | The last paragraph says so. | I got the highest mark in my class in the last writing test.

## Moving to a new flat | HF
Last month, my family moved to a new flat. Our old flat was very small, with only two rooms for five people. My brother and I slept in the living room.

The new flat is on the eighth floor of a modern building. It has three bedrooms, a kitchen, a living room and two bathrooms. Now I have my own room for the first time! It's small, but I can decorate it as I like. I painted one wall light green and put photos of my friends on it.

Moving was hard work. We packed everything into about sixty boxes. My father rented a van, and some friends helped us carry the furniture. The lift in the new building was broken on moving day, so we carried everything up eight floors. We were exhausted!

There are some things I miss about our old home. The old neighbourhood was full of small shops, and I knew everyone. Here, the neighbours are friendly, but I don't know them yet.

The best thing about the new flat is the view. From my window, I can see the river and the whole city at night.
? s | How many rooms did the old flat have? | two / 2 / two rooms | The first paragraph says so. | with only two rooms for five people.
? c | Which floor is the new flat on? | *The eighth floor | The second floor | The tenth floor | The second paragraph says so. | The new flat is on the eighth floor
? c | Why did they carry everything up the stairs? | *The lift was broken | The van was too small | The flat was on the ground floor | The third paragraph explains. | The lift in the new building was broken on moving day
? t | The narrator knows all the new neighbours well. | F | The narrator doesn't know them yet. | I don't know them yet.
? t | The narrator can see the river from the window. | T | The last paragraph says so. | I can see the river and the whole city at night.

## Too much sugar | HE
Many people eat much more sugar than they think. Sugar is not only in sweets and cakes. It is also in many other foods, like bread, sauces, yoghurt and breakfast cereals.

Drinks are one of the biggest problems. A can of cola contains about seven teaspoons of sugar. Many fruit juices and milk teas contain even more. Doctors say adults should eat less than six teaspoons of added sugar a day, and children even less.

Too much sugar is bad for our health. It can damage our teeth and make us gain weight. Over many years, it can also cause serious illnesses, like diabetes.

There are some easy ways to eat less sugar. First, drink water instead of sweet drinks. Second, read the labels on food packets. Sugar sometimes has different names, like glucose or syrup. Third, eat fresh fruit when you want something sweet. Fruit has natural sugar, but it also has fibre and vitamins.

You don't need to stop eating sweets completely. Just eat them less often, and enjoy them as a special treat.
? c | Which food can contain sugar, according to the text? | *Bread and sauces | Only sweets | Only cakes | The first paragraph lists them. | It is also in many other foods, like bread, sauces, yoghurt and breakfast cereals.
? s | How many teaspoons of sugar are in a can of cola? | about seven / seven / 7 | The second paragraph says so. | A can of cola contains about seven teaspoons of sugar.
? t | Doctors say adults should eat less than six teaspoons of added sugar a day. | T | The second paragraph says so. | adults should eat less than six teaspoons of added sugar a day
? c | Which name for sugar does the text mention? | *Syrup | Salt | Starch | The fourth paragraph says so. | like glucose or syrup.
? t | The text says you must stop eating sweets completely. | F | Just eat them less often. | You don't need to stop eating sweets completely.

## A bus trip to the mountains | TP
Last month, I took a night bus from Ha Noi to Ha Giang, a province in the mountains in the far north of Viet Nam. The trip took about seven hours.

The bus was a sleeper bus. Instead of seats, there were small beds in two levels. I had a bed on the top level next to the window. Everyone had to take off their shoes and put them in a plastic bag.

The bus left at nine in the evening. At first, the road was flat and straight, and I fell asleep quickly. But after midnight, the road went up into the mountains. It had many sharp turns, and the bus moved from side to side. I woke up many times.

At half past four in the morning, the bus arrived in Ha Giang. It was still dark and quite cold. I had a hot bowl of noodle soup at a small stall near the bus station.

When the sun came up, I saw the mountains for the first time. They were tall and green, and there were clouds below me. The difficult trip was worth it.
? s | How long did the trip take? | about seven hours / seven hours / 7 hours | The first paragraph says so. | The trip took about seven hours.
? c | What did passengers have to do with their shoes? | *Put them in a plastic bag | Leave them at the station | Wear them all the time | The second paragraph explains. | put them in a plastic bag.
? c | Why did the narrator wake up many times? | *The mountain road had many sharp turns | It was too noisy | The bed was broken | The third paragraph explains. | It had many sharp turns, and the bus moved from side to side.
? t | The bus arrived at noon. | F | It arrived at half past four in the morning. | At half past four in the morning, the bus arrived in Ha Giang.
? t | The narrator thinks the trip was worth it. | T | The last paragraph says so. | The difficult trip was worth it.

## My brother's football dream | HS
My younger brother Khoa is fourteen, and he has one big dream: to play football for the national team. He has loved football since he was four years old.

Every day after school, he practises for two hours with his club. At the weekend, he plays matches. Even when it rains, he goes to practise. He says great players never miss training.

Last year, a coach from a famous football academy watched one of his matches. After the match, the coach talked to my parents. He invited Khoa to try out for the academy. Only twenty young players out of three hundred were chosen, and Khoa was one of them!

Now he lives at the academy during the week. He trains every day and studies normal school subjects too. The academy says that school is very important, because only a few players become professionals.

My parents miss him, but they are very proud. Every Sunday, we go to watch him play. I don't know if his dream will come true, but I admire how hard he works.
? s | How old is Khoa? | fourteen / 14 | The first paragraph says so. | My younger brother Khoa is fourteen
? c | How long does Khoa practise after school? | *Two hours | One hour | Four hours | The second paragraph says so. | he practises for two hours with his club.
? c | How many young players were chosen for the academy? | *Twenty | Three hundred | Fifty | The third paragraph says so. | Only twenty young players out of three hundred were chosen
? t | Students at the academy do not study school subjects. | F | They study normal school subjects too. | studies normal school subjects too.
? t | The family watches Khoa play every Sunday. | T | The last paragraph says so. | Every Sunday, we go to watch him play.

## A thank-you letter to my teacher | CO
Dear Mrs. Huong,

I am writing to say thank you before I leave school next month. You were my English teacher for three years, and you changed my life.

When I started in your class, I was very shy. I never answered questions, because I was afraid of making mistakes. You noticed this. You didn't force me to speak in front of the class. Instead, you asked me to help you with small things, like giving out papers. Slowly, I became more confident.

I remember the day you asked me to read my story to the class. My hands were shaking, but when I finished, everybody clapped. That was the first time I felt proud of myself at school.

You also gave me books to read in the holidays and always asked me what I thought about them. Because of you, I love reading in English.

Next year, I am going to study English at university. I want to become a teacher like you.

With many thanks,
Thao
? s | How many years was Mrs. Huong Thao's teacher? | three years / three / 3 | The first paragraph says so. | You were my English teacher for three years
? c | Why didn't Thao answer questions at first? | *Thao was afraid of making mistakes | Thao didn't understand English | Thao was often absent | The second paragraph explains. | because I was afraid of making mistakes.
? c | How did Mrs. Huong help Thao become confident? | *By asking for help with small things | By making Thao speak every day | By giving extra homework | The second paragraph explains. | you asked me to help you with small things, like giving out papers.
? t | The class laughed when Thao read the story. | F | Everybody clapped. | everybody clapped.
? t | Thao wants to become a teacher. | T | The last paragraph says so. | I want to become a teacher like you.
"""

PASSAGES["B1"] = """
## Working from anywhere | WK
When Thanh started her small design company five years ago, all six employees worked in the same office. Then, during a long period when people had to stay at home, the company moved online. Something surprising happened: the work did not get worse. In fact, some projects were finished faster.

When the office reopened, Thanh asked her team what they wanted. Most of them preferred a mix: two days in the office and three days at home. One designer, Long, wanted to work from his hometown, three hundred kilometres away, so he could look after his elderly parents.

Thanh agreed, but she made some rules. Everyone had to be online between ten and three, and there was a video meeting every Monday morning. Once a month, the whole team met in person for a day of planning and a long lunch together.

The new system has advantages for the company too. Thanh moved to a smaller office and now pays forty percent less rent. She has also hired two new designers who live in other cities.

There are some difficulties. New employees sometimes feel lonely, and it is harder to share quick ideas. But Thanh says she will never go back to the old way. "People work better when they have some control over their lives," she says.
? c | What happened when the company moved online? | *The work did not get worse | Several employees left | The company lost clients | The first paragraph explains. | the work did not get worse.
? c | Why did Long want to work from his hometown? | *To look after his elderly parents | Because rent there is cheaper | To start his own company | The second paragraph explains. | so he could look after his elderly parents.
? s | Between what times must everyone be online? | between ten and three / ten and three / 10 and 3 | The third paragraph says so. | Everyone had to be online between ten and three
? t | The company now pays less rent. | T | It pays forty percent less. | now pays forty percent less rent.
? t | Thanh plans to return to the old way of working. | F | She says she will never go back. | Thanh says she will never go back to the old way.

## Why I sold my car | TP
For ten years, I drove to work every day. I thought I couldn't live without a car. Then, last year, my car broke down and the repair was going to cost almost a thousand dollars. I decided to try living without it for one month before I paid for the repair.

The first week was difficult. I had to learn the bus routes, and the bus to my office took forty-five minutes, fifteen minutes longer than driving. But I soon discovered that I could read on the bus. In one month, I finished three books, something I hadn't done for years.

For short trips, I bought a second-hand bicycle. I started cycling to the market and to visit friends. After a few weeks, I felt fitter, and I slept better at night.

I also calculated how much my car really cost me. With petrol, parking, insurance and repairs, it was about three hundred dollars a month. Now I spend about sixty dollars on transport.

At the end of the month, I didn't repair the car. I sold it. There are times when I miss it, especially when it rains or when I need to carry heavy things. For those times, I rent a car or take a taxi. Overall, my life is cheaper, healthier and less stressful.
? c | Why did the writer stop driving at first? | *The car broke down and the repair was expensive | The writer moved closer to work | The writer lost their licence | The first paragraph explains. | my car broke down and the repair was going to cost almost a thousand dollars.
? s | How many books did the writer finish in the first month? | three / 3 / three books | The second paragraph says so. | In one month, I finished three books
? c | How much did the car cost the writer each month? | *About three hundred dollars | About sixty dollars | About a thousand dollars | The fourth paragraph says so. | it was about three hundred dollars a month.
? t | The writer never misses the car. | F | The writer sometimes misses it. | There are times when I miss it
? t | The writer sometimes rents a car. | T | The last paragraph says so. | For those times, I rent a car or take a taxi.

## The Thursday English club | ED
Every Thursday evening, about twenty people meet in a room above a café in the city centre. They are students, office workers, a retired doctor and even a taxi driver. They have one thing in common: they all want to speak better English.

The English club was started two years ago by Minh, a university student. He noticed that many people studied English for years but were still afraid to speak. "In class, we learn grammar and take tests," he says. "But we rarely practise real conversation."

The club is free, and there is no teacher. Each week, one member chooses a topic, such as travel, food or technology. Members sit in small groups of four or five and talk for an hour. Then each group shares the most interesting ideas with everyone. Sometimes foreign visitors join the club, and everyone enjoys the chance to talk with them.

The most important rule is that nobody laughs at mistakes. Minh believes that people learn faster when they feel relaxed.

Hoa, a nurse, has come every week for a year. "When I started, I could only say a few sentences," she says. "Last month, I helped a foreign patient at the hospital in English. I was so proud."
? c | What do all the club members have in common? | *They want to speak better English | They are all students | They all work in the city centre | The first paragraph explains. | they all want to speak better English.
? c | Why did Minh start the club? | *People rarely practise real conversation in class | He wanted to earn money | His teacher asked him | The second paragraph explains. | we rarely practise real conversation.
? t | Members have to pay a small fee. | F | The club is free. | The club is free
? s | What is the most important rule? | nobody laughs at mistakes / no laughing at mistakes | The fourth paragraph says so. | The most important rule is that nobody laughs at mistakes.
? t | Hoa used English to help a patient. | T | The last paragraph says so. | I helped a foreign patient at the hospital in English.

## The town without plastic bags | EN
Three years ago, a small coastal town decided to stop using plastic bags. Shops were no longer allowed to give them to customers, and people had to bring their own bags or buy a cloth bag.

The idea came from a group of high school students. They organised a beach clean-up and collected more than two hundred kilos of rubbish in one morning. Most of it was plastic bags. The students took photos and showed them at a town meeting. Many people were shocked.

At first, some shop owners were worried. They thought customers would be angry and go to shop in other towns. A few customers did complain, especially older people who were used to plastic bags. But most people changed their habits quickly. Several local women started a business making colourful bags from old clothes, and tourists love buying them as souvenirs.

Today, the beach is much cleaner, and fishermen say they find less plastic in their nets. Other towns in the region are now thinking about doing the same thing.

The students who started the campaign are now at university. One of them, Lan, is studying environmental science. "We showed that young people can change things," she says.
? c | Where did the idea come from? | *A group of high school students | The town mayor | Local fishermen | The second paragraph explains. | The idea came from a group of high school students.
? s | How much rubbish did the students collect in one morning? | more than two hundred kilos / two hundred kilos / 200 kilos | The second paragraph says so. | collected more than two hundred kilos of rubbish in one morning.
? c | What were shop owners worried about at first? | *Customers would shop in other towns | Bags would be too expensive | Tourists would stop coming | The third paragraph explains. | They thought customers would be angry and go to shop in other towns.
? t | All customers were happy with the change from the beginning. | F | Some complained. | A few customers did complain
? t | Fishermen find less plastic in their nets now. | T | The fourth paragraph says so. | fishermen say they find less plastic in their nets.

## Learning a language at fifty | ED
Many people believe that adults cannot learn a new language well. Mrs. Lan, a fifty-two-year-old accountant, disagrees. Two years ago, she started learning Japanese, and today she can have a simple conversation and read short stories.

She decided to learn because her son moved to Japan for work and married a Japanese woman. "I wanted to talk to my daughter-in-law and, one day, to my grandchildren," she explains.

At first, it was very hard. She found the writing system especially difficult. She also worried that she was too old and that her memory was not good enough. But she discovered some advantages too. As an adult, she was more organised and more motivated than when she was a student.

Her method is simple. She studies for thirty minutes every morning before work. She uses an app for vocabulary, listens to Japanese podcasts while she cooks and has an online lesson with a teacher in Osaka every Saturday.

Last spring, she visited her son in Japan for three weeks. She ordered food in restaurants, asked for directions and talked with her daughter-in-law's parents. "They were very surprised," she laughs. "Now they are learning Vietnamese!"
? c | Why did Mrs. Lan start learning Japanese? | *To talk with her son's Japanese family | For her job | To travel around Japan | The second paragraph explains. | I wanted to talk to my daughter-in-law
? c | What did she find especially difficult? | *The writing system | Pronunciation | Listening | The third paragraph says so. | She found the writing system especially difficult.
? s | How long does she study every morning? | thirty minutes / 30 minutes | The fourth paragraph says so. | She studies for thirty minutes every morning before work.
? t | Mrs. Lan has online lessons with a teacher in Tokyo. | F | The teacher is in Osaka. | has an online lesson with a teacher in Osaka every Saturday.
? t | Her daughter-in-law's parents are now learning Vietnamese. | T | The last paragraph says so. | Now they are learning Vietnamese!

## Three generations of bakers | WK
The Hong Phat bakery has been in the same street for over sixty years. It was opened by Mr. Phat in 1962, and today it is run by his granddaughter, Vy.

When Mr. Phat started, he baked only one kind of bread, the long crispy loaf that is popular all over Viet Nam. He got up at two o'clock every morning to bake, and he sold the bread from a wooden cart.

His son, Vy's father, expanded the business. In the 1990s, he opened a real shop and started making cakes for weddings and birthdays. The bakery became famous in the neighbourhood for its coconut cake.

When Vy took over five years ago, the bakery was having problems. Big chain bakeries had opened nearby, and young customers were buying from them instead. Vy, who studied business, made some changes. She started selling online, created a website with photos of the cakes and added healthier options, like wholemeal bread.

But she did not change everything. The bread is still made with her grandfather's recipe, and older customers still come every morning. "Our customers trust us because some things stay the same," Vy says. Her grandfather, now ninety, still visits the shop on Sundays to check the bread.
? s | When was the bakery opened? | 1962 / in 1962 | The first paragraph says so. | It was opened by Mr. Phat in 1962
? c | How did Mr. Phat sell his bread? | *From a wooden cart | In a big shop | Online | The second paragraph says so. | he sold the bread from a wooden cart.
? c | What was the bakery famous for in the 1990s? | *Its coconut cake | Its wholemeal bread | Its wedding flowers | The third paragraph says so. | The bakery became famous in the neighbourhood for its coconut cake.
? t | Vy changed the recipe for the bread. | F | It is still made with the grandfather's recipe. | The bread is still made with her grandfather's recipe
? t | Vy studied business. | T | The fourth paragraph says so. | Vy, who studied business, made some changes.

## The night market economy | SH
Every evening at six o'clock, an empty car park in the city centre changes completely. Dozens of stalls appear, lights are turned on, and the smell of grilled food fills the air. By eight o'clock, thousands of people are walking between the stalls.

For many families, the night market is an important source of income. Mrs. Hien has sold grilled corn there for twelve years. During the day, she works as a cleaner. The money from the market helps her pay for her children's school fees. "It's tiring to work day and night," she says, "but this is how we built our life."

The market is also good for young people starting a business. Renting a stall costs much less than renting a shop. Duy, a twenty-three-year-old graphic designer, sells T-shirts with his own designs. If his designs sell well at the market, he plans to open an online shop.

However, the market also creates problems. Residents nearby complain about noise and rubbish, and traffic is terrible on weekend nights. Last year, the city introduced new rules: the market must close at eleven, and every stall must take its rubbish away.

Most people agree that the market is worth keeping. It brings life to the city and gives many people a chance to earn a living.
? c | What is the place used for during the day? | *A car park | A school | A football field | The first paragraph says so. | an empty car park in the city centre changes completely.
? s | How long has Mrs. Hien sold grilled corn at the market? | twelve years / 12 years | The second paragraph says so. | Mrs. Hien has sold grilled corn there for twelve years.
? c | Why is the market good for young people starting a business? | *A stall costs much less than a shop | They get free training | The city gives them money | The third paragraph explains. | Renting a stall costs much less than renting a shop.
? t | Duy already has an online shop. | F | He plans to open one. | he plans to open an online shop.
? t | Stalls must now take their rubbish away. | T | It is one of the new rules. | every stall must take its rubbish away.

## Sleep and learning | HE
Many students believe that studying late into the night is the best way to prepare for an exam. But scientists say this is often a mistake. Sleep plays an important role in learning and memory.

While we sleep, the brain is not resting completely. It organises the information we learned during the day and moves important memories to long-term storage. Studies show that students who sleep well after studying remember more than students who stay awake.

Lack of sleep also affects concentration. A tired brain finds it harder to focus and solve problems. People who sleep less than six hours a night often make more mistakes and feel more stressed.

Teenagers need eight to ten hours of sleep a night, but many get much less. One reason is screens. The light from phones and computers makes the brain think it is still daytime, so it becomes harder to fall asleep.

Experts give some simple advice. Try to go to bed and wake up at the same time every day, even at weekends. Stop using screens an hour before bed. And if you have an exam, study in the afternoon or early evening, then get a good night's sleep. Your brain will do the rest.
? c | According to scientists, what is often a mistake? | *Studying late into the night before an exam | Studying in the afternoon | Sleeping more than eight hours | The first paragraph explains. | studying late into the night is the best way to prepare for an exam. But scientists say this is often a mistake.
? c | What does the brain do during sleep? | *Organises information and stores important memories | Forgets everything | Rests completely | The second paragraph explains. | It organises the information we learned during the day
? s | How many hours of sleep do teenagers need? | eight to ten hours / eight to ten / 8 to 10 | The fourth paragraph says so. | Teenagers need eight to ten hours of sleep a night
? t | Screen light helps the brain fall asleep. | F | It makes the brain think it is daytime. | makes the brain think it is still daytime
? t | Experts advise the same sleep times at weekends. | T | The last paragraph says so. | even at weekends.

## A year in New Zealand | TR
After I finished university, I didn't start working immediately. Instead, I went to New Zealand on a working holiday visa. It allowed me to stay for one year and work to pay for my travels.

For the first three months, I worked on a fruit farm picking apples. The work was physically hard, and I had to start at six in the morning. But I worked with people from all over the world: Germany, Chile, Japan and France. We lived together in a big wooden house, and in the evenings we cooked dishes from our countries.

With the money I saved, I travelled around the country for two months. I hiked in national parks, saw glaciers and swam with dolphins. The landscape was more beautiful than anything I had seen before.

Then I got a job in a café in Wellington. My English improved enormously, because I talked to customers all day. I also learned to make very good coffee!

The year changed me. Before, I was shy and depended on my parents for everything. In New Zealand, I had to solve problems alone, like finding a place to live and opening a bank account. When I came home, I felt more confident, and I found a job in tourism quickly.
? c | What did the visa allow the writer to do? | *Stay for one year and work | Study at a university | Stay for five years | The first paragraph explains. | It allowed me to stay for one year and work to pay for my travels.
? s | What fruit did the writer pick? | apples | The second paragraph says so. | I worked on a fruit farm picking apples.
? c | Where did the writer work after travelling? | *In a café in Wellington | On a dolphin boat | In a hotel | The fourth paragraph says so. | Then I got a job in a café in Wellington.
? t | The writer was confident before the trip. | F | The writer was shy before. | Before, I was shy and depended on my parents for everything.
? t | The writer found a job in tourism after returning. | T | The last paragraph says so. | I found a job in tourism quickly.

## The real cost of cheap clothes | SH
Clothes have never been cheaper. Today, you can buy a T-shirt for the price of a cup of coffee. Many people buy new clothes every month and throw away clothes after wearing them only a few times. This is often called fast fashion.

But cheap clothes have hidden costs. Making clothes uses huge amounts of water. Producing one cotton T-shirt can use more than two thousand litres. Factories also use chemicals to colour fabrics, and in some countries these chemicals end up in rivers.

There are also human costs. Many clothes are made in factories where workers earn very low wages and work long hours. Some factories are not safe.

What can we do? Experts suggest a few simple steps. First, buy fewer clothes, but choose better quality ones that last longer. Second, take care of your clothes: wash them at lower temperatures and repair them when they are damaged. Third, try buying second-hand clothes or swapping clothes with friends.

Some young people are leading the change. In many cities, there are now clothes-swapping events where people bring clothes they don't wear and take something new home. It's free, it's fun, and it's better for the planet.
? c | What is fast fashion? | *Buying many cheap clothes and throwing them away quickly | Making clothes very quickly by hand | Clothes for sport | The first paragraph explains. | Many people buy new clothes every month and throw away clothes after wearing them only a few times.
? s | How much water can one cotton T-shirt use? | more than two thousand litres / two thousand litres / 2000 litres | The second paragraph says so. | Producing one cotton T-shirt can use more than two thousand litres.
? t | All clothes factories are unsafe. | F | Some factories are not safe. | Some factories are not safe.
? c | What do experts suggest? | *Buying fewer, better-quality clothes | Buying only new clothes | Washing clothes at high temperatures | The fourth paragraph says so. | buy fewer clothes, but choose better quality ones that last longer.
? t | Clothes-swapping events are free. | T | The last paragraph says so. | It's free, it's fun, and it's better for the planet.

## A street that shares | PT
On Hoa Binh Street, nobody needs to buy a ladder. If you need one, you just borrow it from Mr. Tuan at number fourteen. Need a drill? Ask Mrs. Mai. A big pot for a family party? Number twenty-two has one.

It all started two years ago, when a resident named Linh created an online group for the street. At first, people used it to share news, like water cuts or lost cats. Then Linh had an idea. She asked everyone to make a list of things they owned but rarely used. Soon, the group had a list of more than a hundred items, from tents to sewing machines.

The system is simple. If you want to borrow something, you post a message in the group, and the owner replies. Things are always returned within a week. Nobody pays money, but people often give a small gift, like fruit or homemade cakes.

The project has saved residents money, but Linh says the biggest benefit is something else. "Before, we didn't know our neighbours. Now we stop and talk in the street," she says.

Recently, a local newspaper wrote about Hoa Binh Street, and three other streets in the city have started their own sharing groups.
? c | What can you borrow from Mr. Tuan? | *A ladder | A drill | A big pot | The first paragraph says so. | you just borrow it from Mr. Tuan at number fourteen.
? c | What did people first use the online group for? | *Sharing news like water cuts or lost cats | Selling things | Organising parties | The second paragraph explains. | people used it to share news, like water cuts or lost cats.
? s | Within how long must things be returned? | a week / within a week / one week | The third paragraph says so. | Things are always returned within a week.
? t | Borrowers pay a small fee. | F | Nobody pays money. | Nobody pays money
? t | Other streets have started sharing groups. | T | Three other streets have. | three other streets in the city have started their own sharing groups.

## Should children have smartphones? | TE
At what age should children get their first smartphone? This question causes many arguments in families. Some parents give phones to children at eight or nine; others wait until fourteen or later.

Parents who give phones early often say it is about safety. With a phone, children can call their parents at any time, and parents can see where their children are. Some also say that children need to learn to use technology, because it will be important in their future.

However, many experts are worried. They say young children who spend a lot of time on phones may sleep less, play outside less and have more problems concentrating at school. Social media can also make children feel bad about themselves when they compare their lives with others.

Some families have found a middle way. They give young children a simple phone that can only make calls and send messages. When children are older, they get a smartphone, but with rules, such as no phones at the dinner table or in the bedroom at night.

Most experts agree that the age is less important than how the phone is used. Talking openly with children about the risks is the most important step.
? c | Why do some parents give phones early? | *For safety | To save money | Because schools require it | The second paragraph explains. | Parents who give phones early often say it is about safety.
? c | Which worry do experts mention? | *Children may sleep less and concentrate less | Phones are too expensive | Children will lose their phones | The third paragraph explains. | young children who spend a lot of time on phones may sleep less
? t | All families give smartphones to young children. | F | Some give simple phones. | They give young children a simple phone that can only make calls and send messages.
? s | What is one rule some families use? | no phones at the dinner table / no phones in the bedroom at night | The fourth paragraph gives examples. | no phones at the dinner table or in the bedroom at night.
? t | Most experts think how the phone is used matters more than the age. | T | The last paragraph says so. | the age is less important than how the phone is used.

## Life on the night shift | HE
When most people go to sleep, Hanh goes to work. She is a nurse in the emergency department of a big hospital, and she works nights, from eight in the evening to eight in the morning, four nights a week.

Night shifts are often busy. There are car accidents, people with sudden pains and older patients who fall at home. With fewer doctors in the hospital at night, nurses have to make quick decisions. "You need to stay calm and think clearly, even at four in the morning," Hanh says.

The hardest part is the effect on her body. Sleeping during the day is difficult, because of noise and light. She uses thick curtains and earplugs, but she still sleeps only five or six hours. She also finds it hard to eat at normal times.

Her social life has changed too. She often misses family dinners and parties with friends. Her husband works during the day, so sometimes they only see each other for an hour.

So why does she do it? Night shifts pay more, and she likes the strong teamwork. "At night, we really depend on each other," she says. "And when a patient goes home well, I know my work matters."
? s | How many nights a week does Hanh work? | four / 4 / four nights | The first paragraph says so. | four nights a week.
? c | Why must nurses make quick decisions at night? | *There are fewer doctors | There are fewer patients | The hospital is closed | The second paragraph explains. | With fewer doctors in the hospital at night, nurses have to make quick decisions.
? c | What does Hanh use to sleep in the day? | *Thick curtains and earplugs | Sleeping pills | A special bed | The third paragraph says so. | She uses thick curtains and earplugs
? t | Hanh sleeps eight hours during the day. | F | Only five or six hours. | she still sleeps only five or six hours.
? t | Night shifts pay more. | T | The last paragraph says so. | Night shifts pay more

## On a cooking show | FD
Last year, Phong, a twenty-six-year-old office worker, did something he never expected: he took part in a national TV cooking competition.

Phong had always loved cooking, but he had never studied it. He learned from his grandmother and from online videos. His friends told him to apply for the show, and he sent a video of himself cooking his grandmother's fish soup. A week later, the producers called.

The competition was much harder than it looked on TV. Each episode, the contestants had to cook a dish in sixty minutes, and sometimes they didn't know the ingredients until the clock started. There were cameras everywhere, and the judges were strict. In the third episode, Phong burned his sauce and almost went home.

But he learned quickly. He discovered that the judges valued simple, well-cooked food more than complicated dishes. In the final, he cooked a modern version of his grandmother's fish soup. He didn't win, but he came second out of twenty contestants.

The show changed his life. After it was broadcast, a restaurant owner offered him a job as a junior chef. Phong left his office job, and now he is working towards his dream of opening his own restaurant.
? c | How did Phong learn to cook? | *From his grandmother and online videos | At a cooking school | At a restaurant | The second paragraph explains. | He learned from his grandmother and from online videos.
? s | How long did contestants have to cook each dish? | sixty minutes / 60 minutes / an hour / one hour | The third paragraph says so. | the contestants had to cook a dish in sixty minutes
? c | What did the judges value? | *Simple, well-cooked food | Complicated dishes | Expensive ingredients | The fourth paragraph explains. | the judges valued simple, well-cooked food more than complicated dishes.
? t | Phong won the competition. | F | He came second. | He didn't win, but he came second out of twenty contestants.
? t | Phong now works as a junior chef. | T | A restaurant owner offered him the job. | a restaurant owner offered him a job as a junior chef.

## Bringing an old house back to life | HF
When Duc and Thu bought an old house in Hoi An, their friends thought they were crazy. The house was more than a hundred years old. The roof leaked, the wooden walls were damaged by insects, and there was no modern kitchen.

The couple wanted to keep the character of the old house while making it comfortable to live in. They found a local carpenter, Mr. Sang, who had repaired many traditional houses. He told them that the main wooden structure was still strong. Only some parts needed to be replaced.

The work took eighteen months, much longer than they expected. Finding the right wood was difficult, and the rainy season stopped the work for several weeks. The cost was also higher than planned. They spent almost all their savings.

But the result is beautiful. The house keeps its old wooden doors, carved windows and roof tiles. Inside, there is a modern kitchen and a bathroom, hidden behind wooden panels. The house stays cool in summer without air conditioning, because of its high ceilings and thick walls.

Now tourists often stop to take photos. Duc and Thu are proud that they saved a piece of history. "New houses are easy to build," says Thu. "Old houses, once lost, never come back."
? s | How old is the house? | more than a hundred years old / over a hundred years / a hundred years / 100 years | The first paragraph says so. | The house was more than a hundred years old.
? c | What did Mr. Sang say about the wooden structure? | *It was still strong | It had to be replaced | It was damaged by water | The second paragraph says so. | the main wooden structure was still strong.
? c | How long did the work take? | *Eighteen months | Six months | Three years | The third paragraph says so. | The work took eighteen months
? t | The house needs air conditioning in summer. | F | It stays cool without it. | The house stays cool in summer without air conditioning
? t | The work cost more than the couple planned. | T | The third paragraph says so. | The cost was also higher than planned.

## The return of vinyl | HS
Not long ago, many people thought vinyl records would disappear forever. First came CDs, then digital downloads, and finally streaming, which lets you listen to millions of songs on your phone. But in the last few years, something surprising has happened: vinyl records have become popular again.

Many of the buyers are young people who grew up with streaming. Why are they interested in an old technology? Some say the sound is warmer and more natural. Others like the large album covers, which they see as works of art.

For many, it is about the experience. With streaming, people often skip songs after a few seconds. With a record, you choose an album, take it out carefully and listen from beginning to end. "It makes me really listen," says Bao, a twenty-year-old student who owns about forty records.

Record shops are opening again in many cities. Some also sell coffee and host small concerts, becoming meeting places for music fans.

However, vinyl is not cheap. A new record can cost three or four times more than a monthly streaming subscription. Most fans still use streaming every day and buy records only of their favourite albums.
? c | Who are many of the new vinyl buyers? | *Young people who grew up with streaming | Older collectors only | Professional musicians | The second paragraph says so. | Many of the buyers are young people who grew up with streaming.
? c | What do some buyers say about the sound? | *It is warmer and more natural | It is louder | It is clearer than streaming | The second paragraph says so. | Some say the sound is warmer and more natural.
? s | About how many records does Bao own? | about forty / forty / 40 | The third paragraph says so. | who owns about forty records.
? t | Most vinyl fans have stopped using streaming. | F | Most still use streaming every day. | Most fans still use streaming every day
? t | Some record shops host small concerts. | T | The fourth paragraph says so. | Some also sell coffee and host small concerts

## Diary of a new city cyclist | TP
Monday: Today I cycled to work for the first time. The route is seven kilometres, and it took me forty minutes. Motorbikes passed very close to me, and I was scared at every junction. I arrived wet with sweat and had to change my shirt in the office toilet.

Wednesday: Second ride. I found a quieter route along the river. It is one kilometre longer, but much safer and more pleasant. I left home earlier, at half past six, when it is cooler and the traffic is lighter.

Friday: My legs hurt a lot today. A colleague who cycles every day gave me some advice: drink plenty of water, don't ride too fast at the beginning, and keep a spare shirt at work. Good idea!

Two weeks later: Cycling is getting easier. The trip now takes only thirty-two minutes. I feel more awake when I arrive at work, and I have saved money on petrol.

One month later: I have lost two kilos without changing my diet. My manager has noticed that three other colleagues have started cycling too. She is now asking the company to install a safe place to park bicycles and a shower for cyclists. I think I have started something!
? s | How long is the first route? | seven kilometres / 7 km / seven km | The Monday entry says so. | The route is seven kilometres
? c | Why did the writer change to the river route? | *It is safer and more pleasant | It is shorter | It has no traffic lights | The Wednesday entry explains. | but much safer and more pleasant.
? c | What advice did the colleague give? | *Drink water, start slowly and keep a spare shirt | Buy an expensive bike | Ride at night | The Friday entry says so. | drink plenty of water, don't ride too fast at the beginning, and keep a spare shirt at work.
? t | After two weeks, the trip took longer than at first. | F | It took only thirty-two minutes. | The trip now takes only thirty-two minutes.
? t | The manager wants a shower for cyclists. | T | She is asking the company for one. | a safe place to park bicycles and a shower for cyclists.

## Saving the river turtles | AN
Ten years ago, a rare species of turtle was almost extinct in a river in central Viet Nam. Fishermen often caught the turtles by accident in their nets, and people took their eggs from the sandy riverbanks to eat or sell.

A small conservation group decided to act. Instead of simply making rules, they worked with the local community. They paid fishermen to report turtle nests and to release turtles they caught. They also trained local young people to guard the nests during the nesting season.

One of these guards is Lam, a twenty-four-year-old from the village. Every night from April to July, he walks along the riverbanks looking for nests. When he finds one, he puts a fence around it to protect the eggs from animals and people. "My grandfather ate turtle eggs," he says. "Now I protect them. Times have changed."

The project has been successful. Last year, more than eight hundred baby turtles hatched and returned to the river, compared with fewer than fifty ten years ago.

Schools in the area also teach children about the turtles. Every year, students help release baby turtles into the river. Many of them say they want to work in conservation when they grow up.
? c | How did fishermen harm the turtles? | *They caught them by accident in their nets | They hunted them for sport | They polluted the river | The first paragraph explains. | Fishermen often caught the turtles by accident in their nets
? c | What did the conservation group do? | *Worked with the local community and paid fishermen to report nests | Banned all fishing | Moved the turtles to a zoo | The second paragraph explains. | They paid fishermen to report turtle nests and to release turtles they caught.
? s | When does Lam guard the nests? | from April to July / April to July | The third paragraph says so. | Every night from April to July
? t | Fewer baby turtles hatched last year than ten years ago. | F | More than eight hundred hatched, compared with fewer than fifty. | more than eight hundred baby turtles hatched
? t | Lam's grandfather ate turtle eggs. | T | Lam says so. | My grandfather ate turtle eggs

## What makes a good manager? | WK
A large company recently asked its employees a simple question: what makes a good manager? More than two thousand people answered. The results surprised the company's directors.

Many directors expected employees to want managers with excellent technical skills. But this was not at the top of the list. The most popular answer was "a manager who listens". Employees wanted to feel that their ideas and problems were taken seriously.

The second most popular answer was clear communication. Employees said they worked better when they understood their goals and when the manager explained the reasons behind decisions. Many complained about managers who changed plans without telling them why.

Third on the list was fairness. Employees wanted managers who treated everyone equally and gave credit to the person who did the work. One employee wrote, "My worst manager presented my ideas to the director as his own."

Interestingly, very few people mentioned salary or rewards. The company has now started a training programme for its managers, focusing on listening skills and feedback. After six months, a new survey showed that employees felt more positive about their work and fewer people had left the company.
? s | How many people answered the question? | more than two thousand / two thousand / 2000 | The first paragraph says so. | More than two thousand people answered.
? c | What was the most popular answer? | *A manager who listens | Excellent technical skills | A high salary | The second paragraph says so. | The most popular answer was "a manager who listens".
? c | What did many employees complain about? | *Managers who changed plans without explaining why | Long working hours | Small offices | The third paragraph explains. | Many complained about managers who changed plans without telling them why.
? t | Many employees mentioned salary. | F | Very few mentioned it. | very few people mentioned salary or rewards.
? t | Fewer people left the company after the training. | T | The last paragraph says so. | fewer people had left the company.

## Travelling on a small budget | MS
Many young people dream of travelling but think it is too expensive. With some planning, however, it is possible to see the world without spending a lot of money.

The biggest cost is usually transport. Booking flights early, travelling on weekdays and being flexible with dates can save a lot. Overnight buses and trains are also useful, because you save the cost of one night's accommodation.

For accommodation, hostels are much cheaper than hotels, and they are a good place to meet other travellers. Some hostels have kitchens, so you can cook your own meals instead of eating in restaurants every day. Another option is staying with local families, which also helps you learn about the culture.

Food doesn't have to be expensive either. Street food and local markets are often cheaper and more delicious than tourist restaurants. A good rule is to eat where local people eat.

Finally, plan free activities. Many cities have free walking tours, where you pay the guide only what you want at the end. Parks, beaches, markets and many temples are free to visit.

Of course, it's important to have some emergency money and travel insurance. Saving money is good, but staying safe is more important.
? c | What is usually the biggest cost of travelling? | *Transport | Food | Souvenirs | The second paragraph says so. | The biggest cost is usually transport.
? c | Why are overnight buses and trains useful? | *They save the cost of one night's accommodation | They are faster | They are more comfortable | The second paragraph explains. | because you save the cost of one night's accommodation.
? s | Where does the text suggest eating? | where local people eat | The fourth paragraph gives a rule. | A good rule is to eat where local people eat.
? t | On free walking tours, you must pay a fixed price at the start. | F | You pay what you want at the end. | you pay the guide only what you want at the end.
? t | The text says staying safe is more important than saving money. | T | The last paragraph says so. | staying safe is more important.

## The storm on the island | NW
Last September, I was on holiday on a small island when a big storm arrived. The weather forecast had warned about it, but I didn't think it would be so strong.

In the afternoon, the sky turned dark grey and the wind began to blow hard. The hotel staff told all guests to stay inside and close the windows. They also told us that the ferries to the mainland were cancelled for at least two days.

By evening, the storm was very strong. The wind was so loud that we couldn't hear each other talk. Trees fell in the street, and the electricity went off at about nine o'clock. The hotel had a generator, but it only worked for the kitchen and a few lights.

The staff were amazing. They cooked dinner for everyone by candlelight and told stories about other storms they had experienced. Some guests played cards, and a child played the guitar. It was frightening, but also a strange kind of adventure.

The next morning, the sun came out. The island looked terrible, with branches and rubbish everywhere. Guests and staff worked together to clean the hotel garden. I stayed two more days than planned, and I left with new friends and a lot of respect for the island's people.
? c | What did the hotel staff tell the guests to do? | *Stay inside and close the windows | Leave the island | Go to the beach | The second paragraph explains. | The hotel staff told all guests to stay inside and close the windows.
? s | For how long were the ferries cancelled? | at least two days / two days / 2 days | The second paragraph says so. | the ferries to the mainland were cancelled for at least two days.
? t | The generator powered the whole hotel. | F | Only the kitchen and a few lights. | it only worked for the kitchen and a few lights.
? c | How did the writer describe the night? | *Frightening but also an adventure | Boring | Completely relaxing | The fourth paragraph says so. | It was frightening, but also a strange kind of adventure.
? t | The writer left the island earlier than planned. | F | The writer stayed two more days. | I stayed two more days than planned
"""

PASSAGES["B1"] += """
## Grandma goes online | PF
When my grandmother turned seventy-five, my cousins and I gave her a tablet. She looked at it nervously and said, "I'm too old for this. I'll break it." We promised to teach her.

The first lessons were slow. She didn't understand why the screen changed when she touched it by accident, and she was afraid of pressing the wrong button. We wrote simple instructions on a piece of paper: how to turn it on, how to answer a video call and how to look at photos.

After a few weeks, something changed. She started calling us herself. She discovered that she could watch old Vietnamese films and listen to music from her youth. Then she joined an online group for people from her home village, and she found two friends she hadn't seen for fifty years.

Now she uses the tablet every day. She reads the news, looks for recipes and sends us messages with a lot of emojis. She even taught her friend next door how to make video calls.

Of course, there are some problems. Once she almost gave her bank details to a stranger who sent her a message. Now we have taught her to be careful online. But overall, the tablet has made her life richer. "I'm not lonely any more," she says.
? s | How old was the grandmother when she got the tablet? | seventy-five / 75 | The first paragraph says so. | When my grandmother turned seventy-five
? c | What did the grandchildren write on paper? | *Simple instructions | Her passwords | A list of films | The second paragraph says so. | We wrote simple instructions on a piece of paper
? c | What did she find in the online group? | *Two friends she hadn't seen for fifty years | A new job | A doctor | The third paragraph says so. | she found two friends she hadn't seen for fifty years.
? t | The grandmother gave her bank details to a stranger. | F | She almost did. | Once she almost gave her bank details to a stranger
? t | The grandmother taught a neighbour to make video calls. | T | The fourth paragraph says so. | She even taught her friend next door how to make video calls.

## The library on wheels | ED
In many villages in the mountains, there are no libraries, and children have very few books at home. Two years ago, a young teacher named Thao decided to do something about it.

Thao bought an old van, painted it bright yellow and filled it with more than a thousand children's books. Most of the books were donated by people in the city after she posted about her idea online.

Every Saturday and Sunday, Thao drives the van to a different village. When the children hear the music from the van, they run to meet it. They can borrow up to three books each, and Thao returns two weeks later to collect them and lend new ones.

Thao also reads stories to the younger children and organises games. For many children, it is the first time they have chosen a book themselves. "At first, some children only looked at the pictures," Thao says. "Now they ask me for longer stories."

The project is not easy. The roads are often bad, especially in the rainy season, and the van has broken down several times. Thao pays for petrol with her own money and donations. But she has no plans to stop. Next year, she hopes to buy a second van and find another driver.
? c | Why did Thao start the project? | *Village children had very few books | She wanted to sell books | Her school asked her to | The first paragraph explains. | children have very few books at home.
? s | How many books are in the van? | more than a thousand / over a thousand / a thousand / 1000 | The second paragraph says so. | filled it with more than a thousand children's books.
? c | How many books can each child borrow? | *Up to three | Only one | Up to ten | The third paragraph says so. | They can borrow up to three books each
? t | The government pays for the petrol. | F | Thao pays with her own money and donations. | Thao pays for petrol with her own money and donations.
? t | Thao hopes to buy a second van. | T | The last paragraph says so. | she hopes to buy a second van and find another driver.

## The farmers' market | FD
Every Sunday morning, a car park near the university becomes a farmers' market. About forty farmers from the surrounding countryside come to sell their products directly to customers.

The market started five years ago with only eight stalls. The organiser, Mr. Hai, wanted to help small farmers earn more money. When farmers sell to supermarkets, they often receive a very low price. At the market, they set their own prices and keep all the money.

Customers like the market because the food is very fresh. Most vegetables are picked the day before, and many farmers grow them without chemicals. You can also talk to the farmers and ask how the food was grown. Mrs. Tam, who sells mushrooms, says, "My customers know my name and my farm. That trust is important."

However, prices are sometimes higher than in supermarkets. Mr. Hai explains that small farms cannot produce as much as big farms, so their costs are higher. But many customers are happy to pay a little more for quality.

The market has also become a social event. There are live music, cooking demonstrations and activities for children. Many families now spend their whole Sunday morning there.
? s | How many farmers come to the market? | about forty / forty / 40 | The first paragraph says so. | About forty farmers from the surrounding countryside come
? c | Why did Mr. Hai start the market? | *To help small farmers earn more money | To sell his own food | To help the university | The second paragraph explains. | Mr. Hai, wanted to help small farmers earn more money.
? c | What does Mrs. Tam sell? | *Mushrooms | Tomatoes | Rice | The third paragraph says so. | Mrs. Tam, who sells mushrooms
? t | Prices are always lower than in supermarkets. | F | They are sometimes higher. | prices are sometimes higher than in supermarkets.
? t | There are cooking demonstrations at the market. | T | The last paragraph says so. | There are live music, cooking demonstrations and activities for children.

## Getting ready for an interview | WK
A job interview can be stressful, but good preparation makes a big difference. Here are some tips from recruiters.

First, research the company. Look at its website and read recent news about it. Interviewers often ask, "Why do you want to work here?" A good answer shows that you know what the company does and why it interests you.

Second, prepare examples from your experience. Instead of saying "I'm a good team player," describe a real situation where you worked in a team and what you achieved. Specific stories are more convincing than general words.

Third, think about your appearance and arrive on time. Plan your route the day before and aim to arrive ten minutes early. Being late gives a very bad first impression.

During the interview, listen carefully and don't be afraid to take a moment before you answer. It is better to think for a few seconds than to give a confused answer.

At the end, the interviewer will usually ask if you have any questions. Always prepare one or two. Asking about the team or the training shows that you are really interested. Finally, send a short thank-you email after the interview. Many candidates forget this simple step.
? c | What question do interviewers often ask? | *Why do you want to work here? | How old are you? | Where do you live? | The second paragraph says so. | Interviewers often ask, "Why do you want to work here?"
? c | What is more convincing than general words? | *Specific stories from real situations | A long CV | Expensive clothes | The third paragraph says so. | Specific stories are more convincing than general words.
? s | How early should you aim to arrive? | ten minutes early / ten minutes / 10 minutes | The fourth paragraph says so. | aim to arrive ten minutes early.
? t | You should answer every question immediately. | F | It is better to think for a few seconds. | It is better to think for a few seconds than to give a confused answer.
? t | Many candidates forget to send a thank-you email. | T | The last paragraph says so. | Many candidates forget this simple step.

## Volunteering at the children's hospital | HE
Every Wednesday afternoon, Mai, a university student, goes to the children's hospital. She is not a doctor or a nurse. She is a volunteer who plays with children who have to stay in hospital for a long time.

Mai joined the volunteer programme a year ago. Before she started, she had two days of training. She learned how to wash her hands properly, how to talk to sick children and their parents, and what to do if a child becomes upset.

In the playroom, Mai and other volunteers read stories, draw pictures and play board games with the children. Some children are too ill to leave their beds, so the volunteers visit them in their rooms. "For a few hours, they can forget that they are sick," Mai says.

The volunteers also help parents. Many parents stay at the hospital all day and are very tired. When a volunteer plays with their child, they can take a short break, have a coffee or make a phone call.

Sometimes the work is sad. Mai remembers a little boy who was very ill. But many children recover and go home. Last month, a girl who had been in hospital for six months sent Mai a drawing with the words "Thank you for playing with me."
? c | What does Mai do at the hospital? | *Plays with children who stay a long time | Works as a nurse | Cleans the rooms | The first paragraph explains. | She is a volunteer who plays with children who have to stay in hospital for a long time.
? s | How long was the training? | two days / 2 days | The second paragraph says so. | she had two days of training.
? c | How do volunteers help parents? | *They let parents take a short break | They pay hospital bills | They cook meals | The fourth paragraph explains. | When a volunteer plays with their child, they can take a short break
? t | All the children can leave their beds. | F | Some are too ill. | Some children are too ill to leave their beds
? t | A girl sent Mai a drawing. | T | The last paragraph says so. | a girl who had been in hospital for six months sent Mai a drawing

## A noisy city | PT
If you ask people what they dislike about living in a big city, many will say the same thing: noise. Traffic, construction, karaoke and loud music from shops can continue from early morning until late at night.

Noise is not only annoying. Doctors say that living with a lot of noise can cause stress, sleep problems and headaches. Over many years, it may even increase the risk of heart disease. Children who go to school near busy roads may find it harder to concentrate.

Some cities are trying to reduce noise. They plant trees along busy roads, which can absorb some sound. They also build quieter road surfaces and create pedestrian zones where cars are not allowed. In some places, construction work is not allowed after ten at night.

Individuals can also make small changes. Thick curtains and double windows help keep noise out of homes. Many people use earplugs or play soft background sounds, like rain, to help them sleep.

But some experts say the best solution is to change our habits. If fewer people used motorbikes and cars and more people used public transport or bicycles, cities would be much quieter. That would also make the air cleaner.
? c | What do many people dislike about living in a big city? | *Noise | Prices | Weather | The first paragraph says so. | many will say the same thing: noise.
? c | What can noise cause, according to doctors? | *Stress, sleep problems and headaches | Better concentration | Lower blood pressure | The second paragraph says so. | living with a lot of noise can cause stress, sleep problems and headaches.
? s | After what time is construction not allowed in some places? | after ten at night / ten at night / 10 pm / ten | The third paragraph says so. | construction work is not allowed after ten at night.
? t | Trees along roads can absorb some sound. | T | The third paragraph says so. | which can absorb some sound.
? t | The experts say earplugs are the best solution. | F | They say changing habits is best. | some experts say the best solution is to change our habits.

## The bird on the balcony | AN
One rainy morning, I found a small bird on my balcony. It was sitting very still, and one of its wings was hanging down. I think it had hit the window in the storm.

I didn't know what to do, so I called a wildlife rescue centre. A volunteer told me not to give the bird food or water, because this can be dangerous. Instead, she told me to put it gently in a cardboard box with small holes and a soft towel, and to keep it in a quiet, dark place.

That afternoon, I took the box to the rescue centre. A vet examined the bird and said its wing was not broken, just hurt. It needed rest for about two weeks.

During those two weeks, the centre sent me photos of the bird. It was eating well and slowly started to move its wing again. The vet told me that many birds hit windows, especially big glass windows that reflect the sky.

When the bird was ready, the centre invited me to help release it. We opened the box in a park near my home, and the bird flew straight up into a tree. Since then, I have put stickers on my windows to help birds see the glass.
? c | Why was the bird hurt? | *It probably hit the window in the storm | A cat attacked it | It was very old | The first paragraph explains. | I think it had hit the window in the storm.
? c | What did the volunteer say not to do? | *Give the bird food or water | Touch the box | Call a vet | The second paragraph says so. | not to give the bird food or water, because this can be dangerous.
? t | The bird's wing was broken. | F | It was not broken, just hurt. | its wing was not broken, just hurt.
? s | How long did the bird need to rest? | about two weeks / two weeks / 2 weeks | The third paragraph says so. | It needed rest for about two weeks.
? t | The writer put stickers on the windows. | T | The last paragraph says so. | I have put stickers on my windows to help birds see the glass.

## The step challenge | TE
Last spring, the company where I work started a step challenge. Everyone downloaded the same fitness app, and teams of five competed to walk the most steps in a month.

At the beginning, I walked about four thousand steps a day, mostly between my car and my desk. Our team was in last place after the first week. So we made a plan. We parked further from the office, used the stairs instead of the lift and went for a walk together after lunch.

The competition became very exciting. People checked the scores every morning, and some colleagues started walking around the office during phone calls. One team even walked to a restaurant five kilometres away for a team dinner.

By the end of the month, I was walking more than ten thousand steps a day. Our team finished in third place out of twelve. The winning team walked over two million steps in total.

The challenge was fun, but the real benefits were bigger. I sleep better, and I have more energy in the afternoon. I also know my colleagues better, because we talked a lot on our walks. The challenge has finished, but our team still goes for a walk after lunch every day.
? s | How many people were in each team? | five / 5 | The first paragraph says so. | teams of five competed
? c | How many steps did the writer walk at the beginning? | *About four thousand a day | About ten thousand a day | About two thousand a day | The second paragraph says so. | I walked about four thousand steps a day
? c | What did one team do? | *Walked five kilometres to a restaurant | Ran a marathon | Cheated with the app | The third paragraph says so. | One team even walked to a restaurant five kilometres away
? t | The writer's team won the challenge. | F | They finished third. | Our team finished in third place out of twelve.
? t | The team still walks after lunch. | T | The last paragraph says so. | our team still goes for a walk after lunch every day.

## My first budget | MS
When I moved into my first flat at twenty-two, I had a job, a salary and, for the first time, no parents to help me with money. After two months, I had a problem: I didn't know where my money went. At the end of each month, my bank account was almost empty.

A friend advised me to make a budget. I wrote down everything I spent for one month, even small things like coffee and snacks. The results were shocking. I spent more on eating out and food delivery than on rent!

So I made a plan using a simple rule. Fifty percent of my salary goes to needs, like rent, bills and food. Thirty percent goes to wants, like eating out, clothes and entertainment. And twenty percent goes to savings.

The first months were difficult. I had to say no to some evenings out, and I learned to cook cheap meals. But I also found free activities, like walking in the park and going to free concerts.

After a year, I had saved enough money for an emergency fund of three months' living costs. When my laptop broke last month, I could buy a new one without borrowing money. That felt wonderful.
? s | How old was the writer when moving into the first flat? | twenty-two / 22 | The first paragraph says so. | When I moved into my first flat at twenty-two
? c | What did the writer spend more on than rent? | *Eating out and food delivery | Clothes | Transport | The second paragraph says so. | I spent more on eating out and food delivery than on rent!
? c | What percentage of the salary goes to savings? | *Twenty percent | Thirty percent | Fifty percent | The third paragraph explains. | twenty percent goes to savings.
? t | The writer borrowed money to buy a new laptop. | F | No borrowing was needed. | I could buy a new one without borrowing money.
? t | The writer found free activities. | T | The fourth paragraph says so. | I also found free activities

## The school garden | EN
Two years ago, there was an empty piece of land behind our school. It was full of rubbish and weeds. Our biology teacher, Mr. Long, had an idea: why not turn it into a garden?

The students in my class agreed to help. First, we cleaned the land. It took three weekends to remove all the rubbish. Then parents donated tools, seeds and young plants. A local farmer came to teach us how to prepare the soil and plant vegetables.

Now the garden has vegetables, herbs, fruit trees and flowers. Each class is responsible for one part of the garden. Students water the plants before school and remove weeds during break time.

The garden is also used for lessons. In biology, we study plants and insects. In maths, we measure how fast the plants grow. Some vegetables are used in the school canteen, and students who never liked vegetables now eat them, because they grew them themselves!

Last month, the garden won a prize in a competition for green schools in the city. The prize money will be used to build a small greenhouse. Mr. Long says the most important result is that students now understand where their food comes from.
? c | What was behind the school two years ago? | *An empty piece of land full of rubbish | A football field | A car park | The first paragraph says so. | there was an empty piece of land behind our school.
? s | How many weekends did it take to remove the rubbish? | three weekends / three / 3 | The second paragraph says so. | It took three weekends to remove all the rubbish.
? c | How is the garden used in maths lessons? | *Students measure how fast the plants grow | Students count the visitors | Students sell vegetables | The fourth paragraph says so. | In maths, we measure how fast the plants grow.
? t | The garden won a prize last month. | T | The last paragraph says so. | the garden won a prize in a competition for green schools in the city.
? t | The prize money will be used to buy new books. | F | It will build a greenhouse. | The prize money will be used to build a small greenhouse.

## Three days in Hue | TR
Hue was the capital of Viet Nam for more than a hundred years, and it is full of history. Last month, I spent three days there, and it was one of my best trips.

On the first day, I visited the Imperial City. It is a huge area with palaces, gates and gardens, surrounded by walls and a moat. Some buildings were damaged during the war, but many have been restored. I spent five hours walking around and still didn't see everything.

On the second day, I rented a bicycle and visited some royal tombs outside the city. Each tomb is different. My favourite was in a quiet garden with a lake and pine trees. It was peaceful, and there were few tourists.

In the evening, I took a boat trip on the Perfume River. Local singers performed traditional music on the boat, and we released small paper lanterns onto the water.

Hue is also famous for its food. I tried bun bo Hue, a spicy beef noodle soup, and many small cakes made from rice flour. The food is spicier than in other parts of Viet Nam.

I left Hue feeling that I understood my country's history much better.
? c | What was Hue in the past? | *The capital of Viet Nam | A fishing village | A university town | The first paragraph says so. | Hue was the capital of Viet Nam for more than a hundred years
? s | How long did the writer spend in the Imperial City? | five hours / 5 hours | The second paragraph says so. | I spent five hours walking around
? c | How did the writer visit the royal tombs? | *By bicycle | By bus | On foot | The third paragraph says so. | I rented a bicycle and visited some royal tombs
? t | The writer's favourite tomb was crowded with tourists. | F | There were few tourists. | there were few tourists.
? t | Food in Hue is spicier than in other parts of Viet Nam. | T | The fifth paragraph says so. | The food is spicier than in other parts of Viet Nam.

## Treasure hunting with a phone | HS
Have you heard of geocaching? It is a hobby that combines technology, walking and a little adventure. Millions of people around the world do it.

The idea is simple. People hide small containers, called caches, in interesting places, such as parks, forests or near old buildings. They then post the location online using GPS coordinates. Other players use an app on their phones to find the caches.

Inside each cache, there is usually a small notebook where finders write their names and the date. Some caches also contain small objects, like keyrings or toys. The rule is that if you take something, you must leave something of equal or greater value.

My friend Quang started geocaching last year. "I love it because it takes me to places I never knew existed," he says. In our city alone, there are more than three hundred caches. Some are easy to find, but others are very well hidden and can take hours.

There are also some important rules. You should never damage nature or private property, and you should be careful that other people don't see you, so the cache stays secret. Quang says the hobby has made him more patient and more observant, and he has met many other players at events.
? c | What are caches? | *Small hidden containers | Phone apps | Old buildings | The second paragraph explains. | People hide small containers, called caches
? c | What is usually inside a cache? | *A small notebook | Money | A map | The third paragraph says so. | there is usually a small notebook where finders write their names and the date.
? s | How many caches are there in the city? | more than three hundred / over three hundred / three hundred / 300 | The fourth paragraph says so. | there are more than three hundred caches.
? t | If you take an object, you don't need to leave anything. | F | You must leave something of equal or greater value. | you must leave something of equal or greater value.
? t | Quang has met other players at events. | T | The last paragraph says so. | he has met many other players at events.

## Can you trust online reviews? | SH
Before buying a product or choosing a restaurant, most people read online reviews. Reviews can be very useful, but not all of them can be trusted.

Some companies pay people to write positive reviews about their products. Others write negative reviews about their competitors. Experts think that a significant number of reviews on some websites are fake.

How can you spot a fake review? There are some warning signs. Be careful if many reviews are posted on the same day, or if they all use similar words and phrases. Very short reviews with only five stars and no details are also suspicious. Real reviews usually mention specific details, both good and bad.

It is also useful to look at the reviewer's profile. If a person has written hundreds of reviews in a short time, or only gives five stars, they may not be a real customer.

Another tip is to read the middle reviews, with three or four stars. These are often the most honest and balanced. They tell you both what is good and what could be better.

Finally, don't depend on reviews alone. Ask friends and family for their opinions too. Personal recommendations are still one of the best ways to make a good choice.
? c | Why can't all reviews be trusted? | *Some are written by people who are paid | Reviews are always negative | Reviewers never use the products | The second paragraph explains. | Some companies pay people to write positive reviews about their products.
? c | Which is a warning sign of fake reviews? | *Many reviews posted on the same day | Reviews with details | Reviews with three stars | The third paragraph says so. | if many reviews are posted on the same day
? t | Real reviews usually mention specific details. | T | The third paragraph says so. | Real reviews usually mention specific details, both good and bad.
? s | Which reviews are often the most honest? | the middle reviews / three or four stars / middle reviews with three or four stars | The fifth paragraph says so. | read the middle reviews, with three or four stars.
? t | The text says you should depend only on reviews. | F | Ask friends and family too. | don't depend on reviews alone.

## Grandma's recipe book | FD
When my grandmother died two years ago, she left a small notebook. Inside were more than eighty recipes written in her neat handwriting, some of them over fifty years old.

Many of the recipes were for dishes I remembered from my childhood: her sweet and sour soup, her braised fish and the sticky rice cakes she made for Tet. But some recipes were missing important information. She often wrote "a little salt" or "cook until it smells right," because she cooked from experience, not exact measurements.

I decided to try to cook every recipe in the book. It took me more than a year. For the difficult ones, I asked my mother and my aunts for help. They remembered how Grandma made them and helped me find the right amounts.

Some dishes failed many times. My first rice cakes were too hard, and my braised fish was too salty. But slowly, the food started to taste like Grandma's.

Last Tet, I cooked a big meal using her recipes for the whole family. My mother cried when she tasted the soup. Now I am typing all the recipes with clear measurements, so my children can cook them one day. I also added notes about the memories each dish brings back.
? s | How many recipes were in the notebook? | more than eighty / over eighty / eighty / 80 | The first paragraph says so. | more than eighty recipes
? c | Why were some recipes missing information? | *The grandmother cooked from experience, not exact measurements | Pages were lost | They were written in another language | The second paragraph explains. | she cooked from experience, not exact measurements.
? c | Who helped the writer with difficult recipes? | *The mother and aunts | A professional chef | Friends from school | The third paragraph says so. | I asked my mother and my aunts for help.
? t | The writer's first rice cakes were perfect. | F | They were too hard. | My first rice cakes were too hard
? t | The writer is typing the recipes with clear measurements. | T | The last paragraph says so. | Now I am typing all the recipes with clear measurements

## When the lights went out | HF
Last Tuesday evening, there was a power cut in our whole neighbourhood. It started at seven o'clock, just as my family was starting dinner, and it lasted for almost five hours.

At first, everyone was annoyed. My brother was in the middle of an online game, and my father was watching football. The fridge stopped working, and it was very hot without the fan. We looked for candles and found three in a kitchen drawer.

We finished dinner by candlelight. Without the TV or phones, we started talking. My father told us stories about his childhood in the countryside, when there was no electricity at all. My brother and I had never heard many of these stories before.

After dinner, we went outside, because it was cooler. Many neighbours were sitting outside too. Children played games in the street, and the adults chatted. An old man played the guitar, and some people sang along.

When the power came back at midnight, everyone cheered, but some people looked a little disappointed. The next day, my mother said, "Maybe we should have an evening without electricity once a month." We all laughed, but I think she was half serious.
? s | How long did the power cut last? | almost five hours / five hours / 5 hours | The first paragraph says so. | it lasted for almost five hours.
? c | How many candles did they find? | *Three | Five | One | The second paragraph says so. | found three in a kitchen drawer.
? c | What did the father talk about? | *His childhood without electricity | Football | His job | The third paragraph says so. | My father told us stories about his childhood in the countryside
? t | The neighbours stayed inside their houses. | F | Many sat outside. | Many neighbours were sitting outside too.
? t | The mother suggested an evening without electricity every month. | T | The last paragraph says so. | Maybe we should have an evening without electricity once a month.

## First weeks in Melbourne | ED
Three months ago, I moved to Melbourne, Australia, to study for a master's degree. I had studied English for years, but the first weeks were still a shock.

The biggest surprise was the Australian accent. People spoke quickly and used words I had never heard, like "arvo" for afternoon. In the first lectures, I recorded everything so I could listen again at home.

The teaching style was also very different. In Viet Nam, I was used to listening to the teacher and taking notes. Here, students are expected to discuss, ask questions and even disagree with the lecturer. At first, I was too nervous to speak. My tutor encouraged me, saying that my opinion was valuable.

Daily life brought other challenges. Rent is very expensive, so I share a house with four other students. Food is expensive too, so I cook most of my meals. I found an Asian supermarket where I can buy rice and fish sauce.

The weather surprised me most. Melbourne can have four seasons in one day: sunny in the morning, cold and rainy in the afternoon.

Now things are getting easier. I have made friends from many countries, and last week I asked a question in a lecture for the first time.
? c | Why did the writer move to Melbourne? | *To study for a master's degree | To work | To visit family | The first paragraph says so. | to study for a master's degree.
? c | What does "arvo" mean? | *Afternoon | Breakfast | Weekend | The second paragraph explains. | like "arvo" for afternoon.
? t | In Melbourne, students are expected to listen without speaking. | F | They are expected to discuss and ask questions. | students are expected to discuss, ask questions and even disagree with the lecturer.
? s | How many other students does the writer share a house with? | four / 4 | The fourth paragraph says so. | I share a house with four other students.
? t | The writer recently asked a question in a lecture. | T | The last paragraph says so. | last week I asked a question in a lecture for the first time.

## The charity shop | SH
On a busy street in the city centre, there is a shop that looks like any other clothes shop. But everything inside has been donated, and all the profits go to help homeless people.

The shop opened four years ago. It is run by a manager and about twenty volunteers, most of them retired people and students. They sort the donations, wash and repair clothes, and arrange them in the shop.

People donate all kinds of things: clothes, shoes, books, toys and kitchen items. Some donations are almost new. Last month, someone donated a wedding dress that had never been worn. It sold for two hundred dollars in one day.

Prices are low, so the shop is popular with students and families who don't have much money. But many customers come simply because they like finding unusual things. "Every visit is different," says one regular customer. "You never know what you'll find."

Last year, the shop raised about thirty thousand dollars. The money paid for meals, warm blankets and job training for homeless people.

The manager says the shop also helps the environment. Thousands of items that would have been thrown away are used again. "Our motto is simple: give, buy, help," she says.
? c | Where do the shop's profits go? | *To help homeless people | To the volunteers | To a school | The first paragraph says so. | all the profits go to help homeless people.
? s | About how many volunteers work at the shop? | about twenty / twenty / 20 | The second paragraph says so. | about twenty volunteers
? c | What happened to the wedding dress? | *It sold in one day | It was given away | It was kept by a volunteer | The third paragraph says so. | It sold for two hundred dollars in one day.
? t | The shop is popular only with people who have little money. | F | Many come to find unusual things. | many customers come simply because they like finding unusual things.
? t | The shop raised about thirty thousand dollars last year. | T | The fifth paragraph says so. | Last year, the shop raised about thirty thousand dollars.

## Coffee culture in Viet Nam | FD
Coffee is a big part of daily life in Viet Nam. In cities and small towns, there are cafés on almost every street, and people of all ages meet there to talk, work or simply watch the world go by.

Coffee was brought to Viet Nam in the nineteenth century. Today, the country is one of the largest coffee producers in the world. Most of the coffee is grown in the Central Highlands, where the climate is perfect for it.

Vietnamese coffee is strong and is usually made with a small metal filter that sits on top of the cup. The most famous drink is iced coffee with sweetened condensed milk. It is sweet, strong and very refreshing on a hot day.

There are also some unusual coffee drinks. Egg coffee, made with egg yolk, sugar and coffee, was invented in Ha Noi when fresh milk was difficult to find. Coconut coffee and salt coffee are also popular.

Cafés are not only about drinks. For many people, they are places to meet friends, have business meetings or study. Some cafés open very early, at five in the morning, for workers who want a coffee before work. Visiting a café is one of the best ways to understand daily life in Viet Nam.
? c | Where is most Vietnamese coffee grown? | *In the Central Highlands | In the Mekong Delta | Near Ha Noi | The second paragraph says so. | Most of the coffee is grown in the Central Highlands
? c | What is used to make Vietnamese coffee? | *A small metal filter | A large machine | A paper bag | The third paragraph says so. | usually made with a small metal filter that sits on top of the cup.
? s | Where was egg coffee invented? | Ha Noi / in Ha Noi | The fourth paragraph says so. | was invented in Ha Noi
? t | Egg coffee was invented because fresh milk was difficult to find. | T | The fourth paragraph says so. | when fresh milk was difficult to find.
? t | All cafés open at noon. | F | Some open at five in the morning. | Some cafés open very early, at five in the morning

## Masks and dirty air | HE
On some days, the air in our city is so polluted that you can't see the tall buildings in the distance. The air looks grey, and many people wear masks when they go outside.

The main causes of air pollution in big cities are traffic, factories, construction and burning rubbish or crop waste. The pollution is often worse in winter, when there is less wind and cold air traps the dirty air close to the ground.

Polluted air contains tiny particles that can enter deep into the lungs. Over time, they can cause breathing problems, heart disease and other illnesses. Children, older people and people with asthma are most at risk.

Not all masks protect equally. Simple cloth masks stop dust but not the smallest particles. Special masks that fit tightly around the face are much more effective. It is also a good idea to check the air quality on an app before going out and to avoid exercising outdoors on very polluted days.

However, masks only protect individuals. To really solve the problem, cities need cleaner public transport, more green spaces and stricter rules for factories. Many people hope that, in the future, children will not need masks to walk to school.
? c | Which is a main cause of air pollution in cities? | *Traffic | Rain | Trees | The second paragraph lists the causes. | The main causes of air pollution in big cities are traffic, factories, construction and burning rubbish or crop waste.
? c | Why is pollution often worse in winter? | *There is less wind and cold air traps it | Factories work more | People drive more | The second paragraph explains. | when there is less wind and cold air traps the dirty air close to the ground.
? t | Simple cloth masks stop the smallest particles. | F | They do not. | Simple cloth masks stop dust but not the smallest particles.
? s | Who is most at risk? | children, older people and people with asthma / children and older people | The third paragraph says so. | Children, older people and people with asthma are most at risk.
? t | The text says masks alone can solve the problem. | F | Masks only protect individuals. | masks only protect individuals.

## The piano next door | HF
When I moved into my new flat, I discovered that my neighbour was a piano teacher. Every afternoon from three to seven, students came to her flat for lessons. Every evening, she practised for two more hours.

At first, I enjoyed it. The music was beautiful, and it felt like having a free concert. But after a few weeks, it became difficult. I worked from home, and the sound of beginners playing the same notes again and again made it hard to concentrate.

I didn't want to complain, because she seemed very nice. Instead, I tried to solve the problem myself. I moved my desk to the other side of the flat and bought noise-cancelling headphones. It helped a little, but not enough.

Finally, I decided to talk to her. I knocked on her door and explained the situation politely. She was very understanding. She hadn't realised that the walls were so thin. She moved her piano away from our shared wall and put a thick carpet under it. She also agreed to stop playing at nine in the evening.

Now we are good friends. Sometimes she invites me for tea, and she has even offered to teach me piano. I said I would think about it!
? s | How many hours does the neighbour practise each evening? | two hours / two / 2 hours | The first paragraph says so. | she practised for two more hours.
? c | Why did the music become a problem? | *The writer worked from home and couldn't concentrate | The music was too sad | The neighbour played at three in the morning | The second paragraph explains. | it hard to concentrate.
? c | What did the writer buy? | *Noise-cancelling headphones | A piano | Thick curtains | The third paragraph says so. | bought noise-cancelling headphones.
? t | The neighbour was angry when the writer complained. | F | She was very understanding. | She was very understanding.
? t | The neighbour offered to teach the writer piano. | T | The last paragraph says so. | she has even offered to teach me piano.

## Learning to say no | WK
Hoa has worked as an accountant for three years. She is talented and hardworking, and her colleagues like her. But last year, she felt exhausted. She often stayed at the office until nine at night and worked at weekends.

The problem was that Hoa found it impossible to say no. When colleagues asked for help, she always agreed, even when she was already busy. When her manager gave her extra tasks, she accepted them without question. She was afraid that people would think she was lazy or unfriendly.

Eventually, she made a serious mistake in an important report, because she was too tired. Her manager called her into a meeting. To Hoa's surprise, he wasn't angry. He asked her why she was working so much.

After that conversation, Hoa started to change. She learned to say things like, "I'd like to help, but I can't finish it today. Can it wait until Thursday?" She also started telling her manager when she had too much work.

At first, it felt uncomfortable. But people respected her decisions. Now Hoa leaves the office at six most days, she sleeps better and, surprisingly, she is more productive. "Saying no to some things means saying yes to doing my best work," she says.
? s | How long has Hoa worked as an accountant? | three years / 3 years | The first paragraph says so. | Hoa has worked as an accountant for three years.
? c | Why did Hoa always say yes? | *She was afraid people would think she was lazy or unfriendly | She wanted more money | Her manager forced her | The second paragraph explains. | She was afraid that people would think she was lazy or unfriendly.
? c | What happened because Hoa was too tired? | *She made a serious mistake in a report | She lost her job | She became ill | The third paragraph says so. | she made a serious mistake in an important report
? t | Hoa's manager was very angry. | F | He wasn't angry. | he wasn't angry.
? t | Hoa is now more productive. | T | The last paragraph says so. | she is more productive.

## The ferry to Cat Ba | TP
Cat Ba is the largest island in Ha Long Bay. There is no bridge, so most visitors arrive by ferry. Last summer, I took the ferry for the first time with my family.

We drove from Hai Phong to the ferry port early in the morning. The ferry left every hour, but in summer there were long queues of cars and motorbikes. We waited for almost two hours before we could get on.

The journey itself was short, only about twenty minutes, but it was beautiful. The water was green and calm, and huge limestone rocks rose from the sea. Small fishing boats moved slowly between the islands. My little sister counted the rocks, but she stopped after fifty.

On the ferry, there were people selling snacks and drinks. Many passengers stood at the side to take photos. The wind was strong, and my father's hat flew into the sea!

When we arrived on the island, we drove along a winding road through the forest to the main town. The view of the bay from the road was amazing.

Next time, we plan to take the ferry on a weekday, when it is less crowded, or arrive very early in the morning.
? c | Why do most visitors arrive by ferry? | *There is no bridge | The ferry is free | It is faster than driving | The first paragraph explains. | There is no bridge, so most visitors arrive by ferry.
? s | How long did the family wait for the ferry? | almost two hours / two hours / 2 hours | The second paragraph says so. | We waited for almost two hours
? c | How long was the ferry journey? | *About twenty minutes | About two hours | About an hour | The third paragraph says so. | The journey itself was short, only about twenty minutes
? t | The father's hat flew into the sea. | T | The fourth paragraph says so. | my father's hat flew into the sea!
? t | Next time, the family plans to travel at the weekend. | F | They plan to go on a weekday. | we plan to take the ferry on a weekday

## The lost wallet | DL
Last Friday, I found a wallet on the pavement outside my office. Inside there was some money, a bank card, an ID card and a photo of a little girl.

My first thought was to give it to the police. But the police station was far away, and I was in a hurry. Then I noticed a business card in the wallet with a phone number. I decided to call.

A man answered. His name was Mr. Binh, and he sounded very worried. He had lost the wallet that morning and had already cancelled his bank card. When I told him I had found it, he was so happy that he could hardly speak.

We met an hour later in a café near my office. He checked the wallet, and everything was there. He tried to give me some money as a reward, but I refused. Instead, he insisted on paying for my coffee.

He told me that the photo was of his daughter, who had died two years before. It was the only copy he had. "The money doesn't matter," he said. "But this photo means everything to me."

I went back to work feeling very glad that I had made that phone call.
? c | Where did the writer find the wallet? | *On the pavement outside the office | In a café | On a bus | The first paragraph says so. | I found a wallet on the pavement outside my office.
? c | How did the writer contact the owner? | *By calling the number on a business card | Through the police | Through social media | The second paragraph explains. | I noticed a business card in the wallet with a phone number. I decided to call.
? t | Mr. Binh had already cancelled his bank card. | T | The third paragraph says so. | had already cancelled his bank card.
? s | What did Mr. Binh pay for? | the writer's coffee / coffee / my coffee | The fourth paragraph says so. | he insisted on paying for my coffee.
? t | The writer accepted a money reward. | F | The writer refused. | I refused.

## Bees on the roof | AN
On the roof of a tall office building in the city centre, there are five beehives. They belong to a company that started keeping bees three years ago to help the environment.

Bees are very important. They pollinate many of the fruits and vegetables we eat. But in many countries, bee numbers are falling because of pesticides, disease and the loss of flowers.

At first, some employees were afraid of being stung. The company invited a professional beekeeper to give a talk. He explained that bees are usually calm if people move slowly and don't disturb them. He also showed how to take care of the hives safely.

Now about fifteen employees are volunteer beekeepers. Wearing special suits, they check the hives every two weeks. City bees find flowers in parks, gardens and balconies, and they produce more honey than many people expect.

Last year, the bees produced about sixty kilos of honey. The company gives jars of it to employees and visitors. Each jar has a label explaining the importance of bees.

Other companies in the city are now interested in the idea. The beekeeper says it is a small action, but if many buildings did the same, it could make a real difference.
? s | How many beehives are on the roof? | five / 5 | The first paragraph says so. | there are five beehives.
? c | Why are bee numbers falling? | *Pesticides, disease and the loss of flowers | Too many beekeepers | Cold weather | The second paragraph explains. | because of pesticides, disease and the loss of flowers.
? c | Why did the company invite a professional beekeeper? | *Some employees were afraid of being stung | To sell honey | To build the hives | The third paragraph explains. | some employees were afraid of being stung.
? t | The bees produced about sixty kilos of honey last year. | T | The fifth paragraph says so. | the bees produced about sixty kilos of honey.
? t | The company sells the honey to make a profit. | F | It gives the jars to employees and visitors. | The company gives jars of it to employees and visitors.

## Running up a mountain | HS
Last October, Duy ran his first mountain marathon: forty-two kilometres up and down mountain paths in the north of Viet Nam. It was the hardest thing he had ever done.

Duy started running three years ago to lose weight. At first, he ran short distances in the park. Then he joined a running club, where he heard about mountain races. He was excited but also nervous.

He trained for six months. Three times a week he ran in the city, and every weekend he drove two hours to the hills to practise running uphill and downhill. Running downhill was more difficult than he expected, because it is easy to fall.

On race day, the weather was cold and foggy. The race started at five in the morning, and the first part was a steep climb. In some places, runners had to use their hands. Duy's legs hurt badly after thirty kilometres, and he walked for a while. But other runners encouraged him.

He finished in nine hours and twenty minutes. He wasn't fast, but he wasn't last either. "At the finish line, I cried," he says. "I never thought I could do it." He is already planning his next race.
? s | How long was the race? | forty-two kilometres / 42 km / forty-two km | The first paragraph says so. | forty-two kilometres up and down mountain paths
? c | Why did Duy start running? | *To lose weight | To win prizes | To join his friends | The second paragraph explains. | Duy started running three years ago to lose weight.
? c | What was more difficult than expected in training? | *Running downhill | Running in the city | Running at night | The third paragraph says so. | Running downhill was more difficult than he expected
? t | The weather on race day was hot and sunny. | F | It was cold and foggy. | the weather was cold and foggy.
? t | Duy is planning another race. | T | The last paragraph says so. | He is already planning his next race.

## Talking to a friend in Brazil | CO
A year ago, I joined a language exchange website. I wanted to practise English, and I was matched with Lucas, a university student in Brazil who wanted to practise English too and was interested in Vietnamese culture.

We decided to have a video call every Sunday. Because of the time difference, it is nine in the evening for me and eleven in the morning for him. We speak only English, and we correct each other's mistakes gently.

At first, our conversations were short and a little awkward. We talked about simple topics, like our families and our studies. But soon we found many things in common. We both love football, cooking and old films.

We have learned a lot about each other's countries. Lucas told me about the carnival in Rio, and I told him about Tet. He was amazed that people clean their houses completely before the new year. Once, we both cooked a dish from each other's country during our call. My Brazilian bean stew was not very good, but his spring rolls were worse!

My English has improved a lot, especially my listening and speaking. More importantly, I have a real friend on the other side of the world. We are planning to meet in person one day.
? c | Why did the writer join the website? | *To practise English | To find a job | To learn Portuguese | The first paragraph says so. | I wanted to practise English
? s | What time is the call for the writer? | nine in the evening / nine / 9 pm / 9 | The second paragraph says so. | it is nine in the evening for me
? c | What do the writer and Lucas have in common? | *Football, cooking and old films | Music and dancing | Mountain climbing | The third paragraph says so. | We both love football, cooking and old films.
? t | The writer's Brazilian dish was excellent. | F | It was not very good. | My Brazilian bean stew was not very good
? t | They plan to meet in person one day. | T | The last paragraph says so. | We are planning to meet in person one day.

## A new bus line | TP
Last month, the city opened a new bus line that connects the airport with the city centre. Before, travellers had to take a taxi or a slow local bus with many stops.

The new buses are modern and air-conditioned, with space for large suitcases. There is free Wi-Fi and USB chargers at every seat. Announcements are made in Vietnamese and English, which is helpful for foreign visitors.

The bus runs every fifteen minutes from five in the morning until midnight. The journey takes about forty minutes, depending on traffic. A ticket costs one dollar, which is much cheaper than a taxi.

In the first month, more than one hundred thousand passengers used the new line. Many of them are airport workers who live in the city. "Before, I spent a lot of money on motorbike taxis," says Linh, who works at a café in the airport. "Now I save almost a hundred dollars a month."

Some passengers have complained that the bus gets very crowded at busy times. The city says it will add more buses next year. It is also planning a special lane, so that the buses don't get stuck in traffic.
? c | What does the new bus line connect? | *The airport and the city centre | Two universities | The city and the beach | The first paragraph says so. | connects the airport with the city centre.
? c | How often does the bus run? | *Every fifteen minutes | Every hour | Every five minutes | The third paragraph says so. | The bus runs every fifteen minutes
? s | How much does a ticket cost? | one dollar / 1 dollar / $1 | The third paragraph says so. | A ticket costs one dollar
? t | Linh saves almost a hundred dollars a month. | T | Linh says so. | Now I save almost a hundred dollars a month.
? t | The bus is never crowded. | F | It gets very crowded at busy times. | the bus gets very crowded at busy times.
"""

PASSAGES["B2"] = """
## The four-day week experiment | WK
For more than a century, the five-day working week has been the norm in most countries. Recently, however, a growing number of companies have experimented with a four-day week, without reducing salaries.

The idea is not simply to give employees an extra day off. Supporters argue that people are more productive when they are well rested, and that much of a typical working week is lost to unnecessary meetings and distractions. In one large trial involving dozens of companies, most firms reported that productivity stayed the same or even improved. Employees reported less stress, better sleep and more time for their families.

The results were not positive everywhere. Businesses that need staff available every day, such as hospitals and shops, found the system harder to organise. Some employees also felt they had to work more intensely to finish their tasks in four days, which created a different kind of pressure.

There are also questions about whether the early results will last. In a trial, people know they are being observed, and they may work harder than usual. Critics argue that only long-term studies will show the real effects.

Nevertheless, after the trials ended, the majority of participating companies decided to keep the four-day week. For many managers, the main benefit was unexpected: it became much easier to attract and keep talented staff.
? c | What do supporters of the four-day week argue? | *Well-rested people are more productive | People should earn less | Meetings are essential | The second paragraph explains. | people are more productive when they are well rested
? c | Which businesses found the system harder to organise? | *Those that need staff every day, like hospitals and shops | Small offices | Technology companies | The third paragraph explains. | Businesses that need staff available every day, such as hospitals and shops
? t | Some employees felt more pressure to finish their work. | T | They had to work more intensely. | Some employees also felt they had to work more intensely
? s | According to critics, what will show the real effects? | long-term studies / only long-term studies | The fourth paragraph says so. | Critics argue that only long-term studies will show the real effects.
? c | What unexpected benefit did many managers notice? | *It became easier to attract and keep staff | Profits doubled | Offices became cheaper | The last paragraph explains. | it became much easier to attract and keep talented staff.

## Why we put things off | HE
Almost everyone has delayed an important task, scrolling through their phone instead of writing a report or cleaning the house. Procrastination is often seen as a sign of laziness or poor time management, but psychologists increasingly see it differently.

According to recent research, procrastination is mainly an emotional problem. We avoid tasks that make us feel bored, anxious, confused or afraid of failure. Doing something more pleasant, like watching videos, gives us immediate relief. The problem is that the relief is temporary, and the stress returns, often stronger, as the deadline approaches.

This explains why simply making a better schedule often doesn't work. If the real cause is fear of doing the task badly, a detailed plan doesn't address that feeling. Instead, experts recommend strategies that reduce the emotional barrier. One is to make the first step very small: rather than "write the essay", the goal becomes "write the first sentence". Once people start, the task usually feels less unpleasant than they imagined.

Another strategy is self-compassion. Studies have found that students who forgave themselves for procrastinating on one exam were less likely to procrastinate before the next one. Being hard on yourself, it seems, only increases the negative feelings that caused the delay in the first place.

Finally, removing temptations helps. Putting your phone in another room is a simple but surprisingly effective way to protect your attention.
? c | How do psychologists increasingly see procrastination? | *Mainly as an emotional problem | As laziness | As a lack of intelligence | The second paragraph explains. | procrastination is mainly an emotional problem.
? c | Why doesn't a better schedule often work? | *It doesn't address the feeling behind the delay | Schedules are too long | People lose their schedules | The third paragraph explains. | a detailed plan doesn't address that feeling.
? s | What first step do experts suggest instead of "write the essay"? | write the first sentence / writing the first sentence | The third paragraph gives the example. | the goal becomes "write the first sentence".
? t | Students who forgave themselves procrastinated more before the next exam. | F | They were less likely to procrastinate. | were less likely to procrastinate before the next one.
? t | The text suggests putting your phone in another room. | T | The last paragraph says so. | Putting your phone in another room is a simple but surprisingly effective way

## Why cities are getting hotter | EN
On a summer afternoon, the centre of a large city can be several degrees hotter than the countryside around it. This is known as the urban heat island effect, and it is becoming a serious problem as cities grow and the climate warms.

The main reason is the materials cities are built from. Concrete, asphalt and dark roofs absorb the sun's heat during the day and release it slowly at night. As a result, cities stay warm even after sunset, giving people little chance to cool down. Heat from air conditioners, cars and factories adds to the problem. Ironically, the more people use air conditioning, the hotter the streets outside become.

The consequences can be serious. High temperatures increase the risk of heatstroke, especially among older people and outdoor workers. They also raise electricity use and can make air pollution worse.

Fortunately, there are solutions. Trees are among the most effective, because they provide shade and release water vapour that cools the air. Some cities have started planting thousands of trees along streets. Others encourage green roofs, which are covered with plants, or paint roofs white to reflect sunlight. Parks, lakes and fountains can also create cooler areas within the city.

Experts say these measures work best when they are combined and planned carefully. A single park helps its neighbourhood, but a network of green spaces connected across the city can lower temperatures far more widely.
? c | What is the urban heat island effect? | *City centres being hotter than the surrounding countryside | Islands near cities becoming hotter | Hot weather on islands | The first paragraph explains. | the centre of a large city can be several degrees hotter than the countryside around it.
? c | Why do cities stay warm after sunset? | *Concrete and asphalt release heat slowly at night | There are more people at night | Factories work at night | The second paragraph explains. | absorb the sun's heat during the day and release it slowly at night.
? t | Using more air conditioning makes the streets outside cooler. | F | It makes them hotter. | the more people use air conditioning, the hotter the streets outside become.
? s | Which two groups face a higher risk of heatstroke? | older people and outdoor workers / older people / outdoor workers | The third paragraph says so. | especially among older people and outdoor workers.
? c | According to experts, when do the measures work best? | *When they are combined and planned carefully | When they are cheap | When they are used in one park | The last paragraph explains. | these measures work best when they are combined and planned carefully.

## Too many visitors in the hills | TR
Ten years ago, a small mountain village in northern Viet Nam received only a few hundred visitors a year. Then photos of its rice terraces went viral on social media. Today, more than two hundred thousand tourists arrive every year.

At first, the change brought clear benefits. Families opened homestays, young people found jobs as guides, and farmers sold local products to visitors. For the first time, many families could afford to send their children to university in the city.

But the rapid growth also created problems. New hotels were built quickly, sometimes without permission, and some of them block the famous views. The village's water supply struggles to meet demand in the high season, and rubbish collection has not kept pace with the number of visitors. Some residents complain that traditional festivals have become performances for tourists rather than community events.

There are also economic tensions. Investors from the city now own many of the largest hotels, so a significant share of the profits leaves the village. Land prices have risen so much that young local couples can no longer afford to build a house.

The local government is now trying to find a balance. It has stopped issuing permits for large hotels and introduced a small entrance fee, which pays for rubbish collection. Some residents believe these steps came too late, but others hope the village can still protect what made it special in the first place.
? s | How many tourists visit the village every year now? | more than two hundred thousand / two hundred thousand / 200,000 | The first paragraph says so. | more than two hundred thousand tourists arrive every year.
? c | Which benefit of tourism is mentioned? | *Families could send their children to university | The roads became quieter | Land became cheaper | The second paragraph explains. | many families could afford to send their children to university in the city.
? t | All new hotels were built with permission. | F | Some were built without permission. | sometimes without permission
? c | Why does a significant share of the profits leave the village? | *Investors from the city own many large hotels | Tourists pay online | Taxes are very high | The fourth paragraph explains. | Investors from the city now own many of the largest hotels
? c | What does the entrance fee pay for? | *Rubbish collection | New hotels | Guides' salaries | The last paragraph says so. | introduced a small entrance fee, which pays for rubbish collection.

## The promise and limits of online learning | ED
When online courses first became popular, some people predicted that they would replace traditional universities. Anyone with an internet connection could watch lectures by world-class professors, often for free. Education, it seemed, was about to become available to everyone.

The reality has been more complicated. Millions of people have signed up for online courses, but completion rates are often very low. In many free courses, fewer than one in ten students finish. Researchers have found that the students who succeed are usually those who already have good study habits and a university degree. In other words, online learning has often helped the people who needed help least.

One reason is motivation. In a classroom, teachers notice when students fall behind, and classmates create a sense of commitment. Alone in front of a screen, it is easy to postpone a lesson until it is forgotten. Many learners also miss the discussions and personal feedback that make learning meaningful.

However, online learning has clear strengths. It allows people to study while working or caring for family, and to repeat difficult parts of a lecture as many times as necessary. For learners in remote areas, it may be the only option.

Many educators now believe the best approach combines both worlds. In "blended" courses, students watch short videos at home and use class time for discussion, problem-solving and group work. Early studies suggest this combination produces better results than either method alone.
? c | What did some people predict about online courses? | *They would replace traditional universities | They would be very expensive | They would disappear quickly | The first paragraph explains. | some people predicted that they would replace traditional universities.
? s | In many free courses, how many students finish? | fewer than one in ten / less than one in ten / one in ten | The second paragraph says so. | fewer than one in ten students finish.
? c | Who usually succeeds in online courses? | *People who already have good study habits and a degree | Young children | People with no previous education | The second paragraph explains. | the students who succeed are usually those who already have good study habits and a university degree.
? t | The text says online learning has no advantages. | F | It has clear strengths. | online learning has clear strengths.
? c | What happens in blended courses? | *Students watch videos at home and discuss in class | Students only study online | Classes are only lectures | The last paragraph explains. | students watch short videos at home and use class time for discussion

## Sharing instead of owning | MS
Why buy a drill you will use for ten minutes a year, when you could borrow one from a neighbour? This simple idea is at the heart of the sharing economy, a system in which people share or rent things instead of owning them.

The sharing economy has grown rapidly thanks to smartphones and apps. Today, people rent spare rooms to tourists, share car rides with strangers and borrow everything from tools to evening dresses. Supporters say this makes better use of resources. A car, for example, is parked for most of the day; sharing it means fewer cars are needed overall.

There are also financial benefits. Owners can earn extra income from things they rarely use, and users save money. For young people in expensive cities, sharing can make life more affordable.

However, the sharing economy has its critics. In many popular cities, renting apartments to tourists has reduced the number of homes available for local residents and pushed up rents. Some people who work for ride-sharing or delivery apps say they have few rights, unstable incomes and no protection if they are injured or ill.

Governments are now trying to update their laws. Some cities limit how many nights a year an apartment can be rented to tourists. Others require platforms to provide insurance for workers. The challenge is to keep the benefits of sharing while protecting communities and workers from its negative effects.
? c | What is the sharing economy? | *A system where people share or rent things instead of owning them | A type of bank | Free public services | The first paragraph explains. | a system in which people share or rent things instead of owning them.
? c | What has helped the sharing economy grow? | *Smartphones and apps | Lower taxes | Bigger houses | The second paragraph says so. | The sharing economy has grown rapidly thanks to smartphones and apps.
? t | Critics say renting apartments to tourists has lowered rents for locals. | F | It has pushed up rents. | pushed up rents.
? s | What do some cities limit? | how many nights a year an apartment can be rented to tourists / nights an apartment can be rented | The last paragraph says so. | Some cities limit how many nights a year an apartment can be rented to tourists.
? c | What is the challenge for governments? | *Keeping the benefits while protecting communities and workers | Banning sharing apps | Making sharing compulsory | The last paragraph explains. | The challenge is to keep the benefits of sharing while protecting communities and workers

## Can young people spot fake news? | TE
Young people are often called "digital natives" because they grew up with the internet. Many adults assume this means they are good at judging online information. However, studies suggest otherwise.

In one well-known study, researchers asked thousands of secondary school and university students to evaluate online content. The results were worrying. Many students could not tell the difference between a news article and an advertisement labelled "sponsored content". Others trusted a photo shared on social media without asking where it came from or whether it had been edited.

The problem is not a lack of intelligence. Most students were never taught how to check information. Schools often teach students to look at whether a website looks professional, but fake sites can look very professional. Professional fact-checkers use a different approach. Instead of reading a single website carefully from top to bottom, they quickly open new tabs to see what other reliable sources say about it. This technique, called lateral reading, is fast and much more effective.

Some countries have started teaching media literacy from primary school. Students learn to ask simple questions: Who created this? What is their purpose? What evidence do they provide? What do other sources say?

Experts emphasise that the goal is not to make young people distrust everything. A healthy approach involves curiosity and careful checking, not cynicism. In a world full of information, knowing how to find reliable sources is an essential skill.
? c | What do many adults assume about young people? | *They are good at judging online information | They don't use the internet | They prefer newspapers | The first paragraph explains. | Many adults assume this means they are good at judging online information.
? c | What could many students not tell apart? | *A news article and an advertisement | Two languages | Photos and videos | The second paragraph explains. | Many students could not tell the difference between a news article and an advertisement
? s | What is the fact-checkers' technique called? | lateral reading | The third paragraph names it. | This technique, called lateral reading, is fast and much more effective.
? t | The problem is that students are not intelligent enough. | F | The problem is not a lack of intelligence. | The problem is not a lack of intelligence.
? c | What is the goal of media literacy, according to experts? | *Curiosity and careful checking, not cynicism | Distrusting everything | Avoiding the internet | The last paragraph explains. | A healthy approach involves curiosity and careful checking, not cynicism.

## Bringing a river back to life | EN
For decades, the river that runs through the centre of the city was hidden. In the 1970s, it was covered with concrete to make room for a busy road. Below the traffic, the river became a dark, polluted channel, and most residents forgot it existed.

Fifteen years ago, the city made a bold decision: to remove the road and uncover the river. Many people opposed the plan. Business owners feared that traffic would become chaotic, and some residents thought the project was a waste of money.

The work took three years. Engineers removed the concrete, cleaned the riverbed and built new walls. They also planted trees and created walking paths along both sides. To manage traffic, the city improved bus services and built new roads further away.

The results surprised even the project's supporters. Within a few years, fish and birds returned to the river. In summer, the area around the river is several degrees cooler than nearby streets. The paths became a popular place for walking, jogging and relaxing, and property values along the river increased.

Not everything was positive. Some small shops lost customers during the construction and were forced to close, and rising property prices have made the area more expensive for older residents. Nevertheless, the project is now seen as a model for other cities. It shows that urban planning can reverse past decisions and give nature a place in the heart of a city.
? s | When was the river covered with concrete? | in the 1970s / the 1970s / 1970s | The first paragraph says so. | In the 1970s, it was covered with concrete
? c | Why did business owners oppose the plan? | *They feared traffic would become chaotic | They wanted a bigger road | They disliked trees | The second paragraph explains. | Business owners feared that traffic would become chaotic
? c | How long did the work take? | *Three years | Fifteen years | One year | The third paragraph says so. | The work took three years.
? t | The area around the river is now cooler in summer. | T | It is several degrees cooler. | the area around the river is several degrees cooler than nearby streets.
? c | Which negative effect is mentioned? | *Rising property prices make the area more expensive for older residents | More pollution | Fewer tourists | The last paragraph explains. | rising property prices have made the area more expensive for older residents.

## The return of board games | HS
In an age of smartphones and online games, you might expect board games to be disappearing. In fact, the opposite is true. Over the past decade, sales of board games have grown significantly, and board game cafés have opened in cities around the world.

What explains this revival? One reason is the desire for real social contact. After spending hours looking at screens for work and entertainment, many people want an activity that brings them face to face with friends. Board games require players to sit together, talk, laugh and sometimes argue.

Another reason is that modern board games are very different from the classic games many people remember. Today's games often involve strategy, cooperation and storytelling. In some popular games, players work together against the game itself, which appeals to people who dislike direct competition.

The internet has also helped, rather than harmed, the hobby. Game designers raise money through crowdfunding websites, and online videos explain the rules of complex games, making them easier to learn.

Board game cafés have become popular meeting places. For a small fee, customers can choose from hundreds of games, and staff help explain the rules. Some cafés host regular events for beginners, and others are used by teachers and psychologists, who believe games can develop skills such as planning, patience and communication.

For many fans, the appeal is simple. "A board game is a reason to spend an evening together without phones," says one café owner.
? c | What has happened to board game sales over the past decade? | *They have grown significantly | They have fallen | They have stayed the same | The first paragraph says so. | sales of board games have grown significantly
? c | What is one reason for the revival? | *The desire for real social contact | Cheaper prices | Better television | The second paragraph explains. | One reason is the desire for real social contact.
? t | In some modern games, players work together against the game. | T | The third paragraph says so. | players work together against the game itself
? s | How do game designers raise money? | through crowdfunding websites / crowdfunding | The fourth paragraph says so. | Game designers raise money through crowdfunding websites
? t | The internet has harmed the board game hobby. | F | It has helped. | The internet has also helped, rather than harmed, the hobby.

## Why languages disappear | CO
There are about seven thousand languages in the world today, but linguists believe that around half of them could disappear by the end of this century. On average, a language dies every few weeks, when its last fluent speaker passes away.

Languages rarely disappear suddenly. Usually, the process takes several generations. It often begins when a community comes into contact with a more powerful language used in schools, government and business. Parents may decide that their children will have better opportunities if they speak the dominant language. Over time, young people use the traditional language less and less, until only older people speak it.

Why does this matter? Each language contains unique knowledge: words for local plants and animals, traditional medicine, stories and ways of seeing the world. When a language disappears, much of this knowledge is lost with it. For the communities themselves, losing their language can also mean losing an important part of their identity.

Fortunately, some endangered languages are being revived. In New Zealand, the Maori language was in serious decline in the twentieth century. Communities created "language nests", preschools where young children are surrounded by Maori-speaking elders. Today, the number of speakers is growing.

Technology also offers new possibilities. Linguists record speakers and create online dictionaries, and some communities use social media and apps to teach their languages to young people. Experts agree, however, that the key to survival is simple: children must grow up speaking the language at home.
? s | About how many languages are there in the world today? | about seven thousand / seven thousand / 7000 | The first paragraph says so. | There are about seven thousand languages in the world today
? c | How does the process of language loss often begin? | *A community comes into contact with a more powerful language | A government bans the language | Speakers forget words | The second paragraph explains. | It often begins when a community comes into contact with a more powerful language
? c | What is lost when a language disappears? | *Unique knowledge and part of a community's identity | Only some songs | Nothing important | The third paragraph explains. | Each language contains unique knowledge
? t | The number of Maori speakers is still falling. | F | It is growing. | Today, the number of speakers is growing.
? c | According to experts, what is the key to a language's survival? | *Children growing up speaking it at home | Online dictionaries | Government money | The last paragraph says so. | children must grow up speaking the language at home.

## The psychology of shopping | SH
When you walk into a supermarket, almost nothing is there by accident. Shops use psychology carefully to encourage customers to spend more.

Consider the layout. Essential products, such as milk and bread, are often placed at the back of the store, so customers have to walk past many other products to reach them. Along the way, they often pick up items they did not plan to buy. The most profitable products are usually placed at eye level, while cheaper brands are on the lowest shelves.

Prices are also designed to influence us. A price of $9.99 feels significantly cheaper than $10, even though the difference is tiny, because we tend to read the first number. Offers such as "buy two, get one free" encourage people to buy more than they need, and much of the extra food is later thrown away.

Even the atmosphere matters. Studies have shown that slow music makes customers walk more slowly and spend more time in the store. The smell of freshly baked bread can make people feel hungry, and hungry customers buy more.

Online shops use their own techniques. Messages like "only two left in stock" create a sense of urgency, and recommendations based on previous purchases encourage further spending.

Knowing these tricks can help consumers make better decisions. Experts recommend making a shopping list, never shopping when hungry and asking yourself whether you would buy a product if it were not on special offer.
? c | Why are milk and bread often at the back of the store? | *So customers walk past many other products | Because they need cold air | Because they are cheap | The second paragraph explains. | so customers have to walk past many other products to reach them.
? c | Why does $9.99 feel cheaper than $10? | *We tend to read the first number | It is much cheaper | Shops say so | The third paragraph explains. | because we tend to read the first number.
? s | What effect does slow music have? | customers walk more slowly and spend more time / people walk more slowly | The fourth paragraph says so. | slow music makes customers walk more slowly and spend more time in the store.
? t | Messages like "only two left" create a sense of urgency. | T | The fifth paragraph says so. | create a sense of urgency
? c | What do experts recommend? | *Never shopping when hungry | Shopping only online | Buying everything on offer | The last paragraph says so. | never shopping when hungry

## Eating more plants | FD
In many countries, more people are choosing to eat less meat. Some have become vegetarians or vegans, while others simply try to have several meat-free days a week. Supermarkets now offer a wide range of plant-based products, from burgers made of beans to milk made from oats.

People change their diets for different reasons. Some are concerned about animal welfare. Others are motivated by health. Research suggests that diets rich in vegetables, fruit, beans and whole grains are linked to lower risks of heart disease and some types of cancer.

The environment is another major reason. Producing meat, especially beef, requires large amounts of land and water and produces significant greenhouse gas emissions. According to many studies, reducing meat consumption is one of the most effective ways an individual can lower their environmental impact.

However, plant-based diets are not automatically healthy. Many processed vegan products contain high levels of salt, sugar and fat. People who stop eating meat also need to make sure they get enough protein, iron and vitamin B12, which is mainly found in animal products. A doctor or nutritionist can help plan a balanced diet.

Cultural traditions also play a role. In many countries, meat is central to celebrations and family meals, and changing these habits can be difficult.

Experts suggest that small steps are often more realistic than dramatic changes. Trying one vegetarian dinner a week, or replacing half of the meat in a recipe with beans, can make a real difference over time.
? c | What do some people do without becoming vegetarian? | *Have several meat-free days a week | Eat only fish | Stop eating vegetables | The first paragraph explains. | others simply try to have several meat-free days a week.
? c | Which meat requires the most resources, according to the text? | *Beef | Chicken | Fish | The third paragraph mentions it. | especially beef
? t | All plant-based products are healthy. | F | Many processed vegan products contain a lot of salt, sugar and fat. | plant-based diets are not automatically healthy.
? s | Which vitamin is mainly found in animal products? | vitamin B12 / B12 | The fourth paragraph says so. | vitamin B12, which is mainly found in animal products.
? c | What do experts suggest? | *Small steps are more realistic | Changing everything at once | Avoiding all processed food | The last paragraph explains. | small steps are often more realistic than dramatic changes.

## Working in the gig economy | WK
Ten years ago, few people had heard the term "gig economy". Today, millions of people earn money through short-term jobs found on apps: delivering food, driving passengers, cleaning homes or designing websites for clients they never meet.

For many workers, the main attraction is flexibility. They can choose when and how much to work. Students fit shifts around their classes, parents work while children are at school, and some people use gig work to earn extra money alongside a full-time job.

However, flexibility has a price. Gig workers are usually classified as independent contractors rather than employees. This means they typically do not receive sick pay, holiday pay or pension contributions. Their income can change from week to week, depending on demand and on the app's pay rates, which can be changed without negotiation.

There is also the question of control. Although gig workers are officially independent, apps often track their performance closely. A delivery rider whose ratings fall too low may find that they receive fewer orders, or are removed from the platform altogether, sometimes without a clear explanation.

In several countries, courts have ruled that some gig workers should be treated as employees with basic rights. Companies argue that this would increase costs and reduce the flexibility that workers value.

The debate is likely to continue. Many experts believe a middle path is possible: keeping flexible working hours while guaranteeing minimum protections, such as insurance against accidents.
? c | What is the main attraction of gig work for many people? | *Flexibility | High pay | Free training | The second paragraph says so. | the main attraction is flexibility.
? c | What do gig workers usually not receive? | *Sick pay and holiday pay | Payment for their work | Customers | The third paragraph explains. | they typically do not receive sick pay, holiday pay or pension contributions.
? t | A rider with low ratings may receive fewer orders. | T | The fourth paragraph says so. | may find that they receive fewer orders
? s | What have courts in several countries ruled? | some gig workers should be treated as employees / that some gig workers are employees | The fifth paragraph says so. | courts have ruled that some gig workers should be treated as employees with basic rights.
? c | What middle path do many experts suggest? | *Flexible hours with minimum protections | Banning gig apps | Paying workers only by the hour | The last paragraph explains. | keeping flexible working hours while guaranteeing minimum protections

## Let children be bored | PF
Many parents today feel that their children should always be busy. After school, children go to music lessons, sports training and extra classes. At home, screens provide constant entertainment. Silence and empty time are often seen as problems to be solved.

But some psychologists argue that boredom is actually good for children. When there is nothing to do, children are forced to find their own activities. They may invent games, build things from boxes, draw or simply daydream. These experiences help develop creativity, imagination and the ability to entertain themselves.

Boredom also teaches an important life skill: dealing with uncomfortable feelings. Adults regularly face boring tasks and quiet moments. Children who have never experienced boredom may find these situations very difficult and reach for their phones automatically.

This does not mean that structured activities are bad. Learning an instrument or playing a sport can teach discipline and teamwork. The problem arises when a child's schedule leaves no time for free play. Some studies suggest that children with less free time may find it harder to plan and organise their own activities later in life.

Experts suggest some practical steps. Parents can keep some afternoons free, limit screen time and resist the urge to solve boredom immediately. When a child says "I'm bored," a parent might reply, "What could you do?" At first, children may complain. But many parents report that, after a few days, their children become surprisingly inventive.
? c | How do many parents see empty time? | *As a problem to be solved | As essential | As a reward | The first paragraph explains. | Silence and empty time are often seen as problems to be solved.
? c | What can boredom help children develop? | *Creativity and imagination | Mathematical skills | Physical strength | The second paragraph explains. | These experiences help develop creativity, imagination
? t | The text says structured activities are bad for children. | F | They can teach discipline and teamwork. | This does not mean that structured activities are bad.
? s | What might a parent reply when a child says "I'm bored"? | What could you do? | The last paragraph gives an example. | a parent might reply, "What could you do?"
? t | Many parents report their children become more inventive after a few days. | T | The last paragraph says so. | after a few days, their children become surprisingly inventive.

## Electric motorbikes on city streets | TP
In Vietnamese cities, motorbikes are everywhere. They are cheap, fast and practical in narrow streets. But they also produce a large share of urban air pollution and noise. Electric motorbikes are often presented as a solution.

Sales of electric two-wheelers have increased rapidly in recent years. They are quiet, produce no exhaust fumes and are cheap to run. Charging an electric motorbike costs much less than filling a petrol tank, and they need less maintenance because they have fewer moving parts.

However, many buyers remain hesitant. The most common concern is range: many models can travel only around eighty kilometres on a full charge, which may not be enough for long journeys. Charging stations are still limited, and many people live in apartment buildings without a place to charge. Batteries can also be expensive to replace after several years.

There are environmental questions too. An electric motorbike is only as clean as the electricity that charges it. If that electricity comes mainly from coal power plants, the overall benefit is smaller, although cities still gain from cleaner air on the streets. Batteries also need to be recycled properly to avoid pollution.

Some manufacturers are experimenting with battery-swapping stations, where riders exchange an empty battery for a full one in a few minutes. Several cities are also considering limits on petrol motorbikes in central areas. If these efforts succeed, the sound of city traffic could change dramatically in the next decade.
? c | Why are electric motorbikes cheap to run? | *Charging costs less than petrol and they need less maintenance | They are free to buy | They never need batteries | The second paragraph explains. | Charging an electric motorbike costs much less than filling a petrol tank
? s | About how far can many models travel on a full charge? | around eighty kilometres / eighty kilometres / 80 km | The third paragraph says so. | many models can travel only around eighty kilometres on a full charge
? t | Charging stations are now available everywhere. | F | They are still limited. | Charging stations are still limited
? c | When is the environmental benefit smaller? | *When the electricity comes mainly from coal | When riders go fast | When it rains | The fourth paragraph explains. | If that electricity comes mainly from coal power plants, the overall benefit is smaller
? c | What happens at battery-swapping stations? | *Riders exchange an empty battery for a full one | Batteries are recycled | Motorbikes are repaired | The last paragraph explains. | riders exchange an empty battery for a full one in a few minutes.

## Is handwriting still important? | ED
In many classrooms, keyboards and touchscreens are replacing pens and paper. Students type their notes, submit homework online and take exams on computers. Some schools have reduced the time they spend teaching handwriting. Is this a problem?

Researchers have found some reasons to keep handwriting. Studies of young children suggest that writing letters by hand helps them recognise letters and learn to read more quickly than typing does. The physical movements involved seem to strengthen the connection between the shape of a letter and its sound.

For older students, the way notes are taken also matters. Students who type notes in lectures can often write down almost every word the lecturer says. Students who write by hand cannot keep up, so they have to listen, select the most important ideas and summarise them in their own words. Several studies have found that this deeper processing helps them understand and remember the material better.

On the other hand, typing has clear advantages. It is faster, easier to edit and essential for most jobs. For students with certain learning difficulties, such as dyslexia, typing can make writing much more accessible.

Most experts do not argue for a choice between the two. Instead, they recommend teaching handwriting well in the early years and introducing typing gradually. For note-taking, the key is not the tool but the method: whether by hand or on a laptop, students learn best when they summarise ideas rather than copying everything.
? c | What have some schools done? | *Reduced the time spent teaching handwriting | Banned computers | Stopped teaching reading | The first paragraph says so. | Some schools have reduced the time they spend teaching handwriting.
? c | How does handwriting help young children? | *They recognise letters and learn to read more quickly | They write faster | They make fewer spelling mistakes | The second paragraph explains. | writing letters by hand helps them recognise letters and learn to read more quickly
? c | Why do handwritten notes help understanding? | *Students have to select and summarise ideas | They are neater | They are shorter to read | The third paragraph explains. | they have to listen, select the most important ideas and summarise them in their own words.
? t | Typing can help students with dyslexia. | T | The fourth paragraph says so. | typing can make writing much more accessible.
? s | According to experts, what matters most for note-taking? | the method / not the tool but the method / summarising ideas | The last paragraph says so. | the key is not the tool but the method

## Plastic we cannot see | EN
When people think of plastic pollution in the ocean, they often imagine floating bottles and bags. But some of the most worrying pollution is invisible. Microplastics are tiny pieces of plastic, smaller than five millimetres, and they have been found almost everywhere scientists have looked: in deep oceans, Arctic ice, drinking water and even the air.

Some microplastics come from larger plastic items that break down slowly in sunlight and waves. Others are produced directly. Synthetic clothes, such as those made of polyester, release thousands of tiny fibres every time they are washed. Car tyres also release particles as they wear down on roads.

Marine animals often mistake microplastics for food. Fish, shellfish and even tiny plankton eat them, and the particles can move up the food chain. Researchers are still studying the effects on human health. So far, the evidence is unclear, but many scientists believe it is wise to reduce exposure where possible.

Cleaning microplastics from the ocean is almost impossible because the particles are so small and widely spread. For this reason, experts focus on prevention. Some countries have banned tiny plastic beads in cosmetics. Engineers are developing filters for washing machines that catch fibres before they enter wastewater.

Individuals can help too. Washing synthetic clothes less often and at lower temperatures reduces the number of fibres released. Choosing natural materials, reducing single-use plastic and supporting better waste management all help address the problem at its source.
? s | How small are microplastics? | smaller than five millimetres / less than five millimetres / 5 mm | The first paragraph says so. | smaller than five millimetres
? c | How do synthetic clothes produce microplastics? | *They release tiny fibres when washed | They melt in the sun | They are thrown into the sea | The second paragraph explains. | release thousands of tiny fibres every time they are washed.
? t | Scientists have proven that microplastics seriously harm human health. | F | The evidence is still unclear. | So far, the evidence is unclear
? c | Why do experts focus on prevention? | *Cleaning microplastics from the ocean is almost impossible | Prevention is cheaper than nothing | Fish prefer clean water | The fourth paragraph explains. | Cleaning microplastics from the ocean is almost impossible
? c | What can individuals do? | *Wash synthetic clothes less often and at lower temperatures | Buy more synthetic clothes | Wash clothes every day | The last paragraph says so. | Washing synthetic clothes less often and at lower temperatures reduces the number of fibres released.

## The bilingual advantage | ED
More than half of the world's population speaks at least two languages. For a long time, some people believed that growing up with two languages might confuse children or slow their development. Today, research paints a very different picture.

Bilingual children may mix languages when they are very young, but this is a normal part of learning, not a sign of confusion. By school age, most can separate their languages easily and switch between them depending on who they are talking to.

Some studies suggest that managing two languages may strengthen certain mental skills. Because bilingual people constantly choose which language to use, they practise focusing attention and ignoring distractions. However, scientists disagree about how large these benefits are, and some recent studies have found smaller effects than earlier research suggested.

What is clearer are the social and practical benefits. Bilingual people can communicate with a wider range of people, access more information and often find it easier to understand different cultures. In many careers, speaking more than one language is a valuable advantage. For children of immigrant families, keeping their parents' language also helps them maintain close relationships with grandparents and relatives.

Experts advise parents who want to raise bilingual children to be consistent. One common approach is for each parent to speak a different language to the child. Another is to use one language at home and another outside. Above all, children need plenty of real, enjoyable experiences in both languages: stories, songs and conversations, not just lessons.
? c | What did some people once believe about growing up with two languages? | *It might confuse children | It was the best way to learn | It was impossible | The first paragraph explains. | growing up with two languages might confuse children or slow their development.
? t | Mixing languages at a young age is a sign of confusion. | F | It is a normal part of learning. | this is a normal part of learning, not a sign of confusion.
? c | What do scientists disagree about? | *How large the mental benefits are | Whether bilingual people exist | Whether languages can be learned | The third paragraph explains. | scientists disagree about how large these benefits are
? s | For children of immigrant families, who does keeping their parents' language help them stay close to? | grandparents and relatives / grandparents | The fourth paragraph says so. | maintain close relationships with grandparents and relatives.
? c | What do children need above all? | *Plenty of real, enjoyable experiences in both languages | Many grammar lessons | Only one language at home | The last paragraph explains. | children need plenty of real, enjoyable experiences in both languages

## Working in a coworking space | WK
Not long ago, people who worked independently had two main choices: work from home or rent a small private office. Today, there is a popular third option, the coworking space.

A coworking space is a shared office where people from different companies work side by side. Members pay a monthly fee, which is usually much lower than renting a private office. In return, they get a desk, fast internet, meeting rooms and often free coffee. Some spaces also offer extras such as events, workshops and even yoga classes.

Many members say the biggest benefit is not the facilities but the people. Freelancers who work at home often feel isolated. In a coworking space, they can chat during breaks, share ideas and find new clients. A designer might meet a programmer who needs help with a website, for example.

There are also downsides. Open spaces can be noisy, and it can be hard to concentrate when people are on the phone nearby. Some members also worry about privacy when they discuss confidential information.

Interestingly, coworking spaces are no longer used only by freelancers. Large companies now rent desks for small teams or for employees who live far from the main office. As more companies adopt flexible working, many experts expect coworking spaces to become a normal part of working life, especially in big cities where office rents are high.
? c | What is a coworking space? | *A shared office for people from different companies | A café | A private office for one company | The second paragraph explains. | A coworking space is a shared office where people from different companies work side by side.
? c | What do many members say is the biggest benefit? | *The people | The free coffee | The yoga classes | The third paragraph says so. | the biggest benefit is not the facilities but the people.
? t | Coworking spaces are always quiet. | F | They can be noisy. | Open spaces can be noisy
? s | Besides freelancers, who now rents desks in coworking spaces? | large companies / big companies | The last paragraph says so. | Large companies now rent desks for small teams
? t | Experts expect coworking spaces to become more common. | T | The last paragraph says so. | many experts expect coworking spaces to become a normal part of working life

## Does volunteer travel help? | TR
Every year, thousands of young people travel abroad to volunteer. They teach in schools, build houses or care for animals, often paying organisations for the experience. This "voluntourism" is presented as a way to travel while helping others. But does it really help?

Supporters say that, when it is well organised, volunteer travel can make a positive difference. Volunteers with professional skills, such as doctors or engineers, can share knowledge with local people. Money paid by volunteers can fund projects that local communities have chosen themselves. Many volunteers also return home with a deeper understanding of global problems.

Critics, however, point to serious problems. Many projects use unskilled volunteers for work that local people could do, such as building schools, which takes jobs away from the community. Some organisations care more about making money from volunteers than about local needs.

Programmes involving children are especially controversial. Some orphanages, critics say, keep children in poor conditions because they attract donations and volunteers. Children may also form emotional attachments to volunteers who leave after a few weeks.

Experts suggest that people considering volunteer travel should ask some key questions. Does the project respond to needs identified by the local community? Are the volunteers' skills actually useful? How is the money spent? And does the project avoid direct, short-term work with vulnerable children?

For many people, the best way to help may be to donate to well-run local organisations or to travel responsibly as a tourist, spending money in locally owned businesses.
? c | What do volunteers often pay for? | *The experience offered by organisations | Their flights only | Local schools | The first paragraph explains. | often paying organisations for the experience.
? c | According to supporters, which volunteers can make a positive difference? | *Volunteers with professional skills | All volunteers | Volunteers who stay one day | The second paragraph explains. | Volunteers with professional skills, such as doctors or engineers, can share knowledge
? t | Building schools with unskilled volunteers can take jobs from local people. | T | The third paragraph says so. | which takes jobs away from the community.
? c | Why are programmes involving children especially controversial? | *Children may form attachments to volunteers who leave | Children don't like foreigners | They are too expensive | The fourth paragraph explains. | Children may also form emotional attachments to volunteers who leave after a few weeks.
? s | Where does the text suggest spending money as a tourist? | in locally owned businesses / locally owned businesses | The last paragraph says so. | spending money in locally owned businesses.

## When antibiotics stop working | HE
Antibiotics are among the most important discoveries in medical history. Before they were introduced in the 1940s, a small cut or a simple infection could be deadly. Today, however, doctors are increasingly worried that antibiotics are losing their power.

The problem is called antibiotic resistance. Bacteria can change, or evolve, over time. When antibiotics are used, most bacteria are killed, but a few may survive because of small genetic differences. These survivors multiply and pass on their resistance. The more often antibiotics are used, the faster this process happens.

A major cause is the unnecessary use of antibiotics. Many people take antibiotics for colds and flu, which are caused by viruses, not bacteria, so the medicine has no effect on them. Some patients also stop taking antibiotics as soon as they feel better, instead of finishing the full course. In many countries, antibiotics are also widely used in farming to make animals grow faster.

The consequences are serious. Infections that were once easy to treat are becoming harder to cure, and some bacteria resist almost all available drugs. Without effective antibiotics, routine operations and cancer treatments would become much riskier.

Solving the problem requires action at many levels. Doctors need to prescribe antibiotics only when necessary, and governments need to control their use in agriculture. Scientists are searching for new types of antibiotics, but this research is slow and expensive. Individuals can help by never demanding antibiotics for viral infections and by following medical advice carefully.
? s | When were antibiotics introduced? | in the 1940s / the 1940s / 1940s | The first paragraph says so. | Before they were introduced in the 1940s
? c | Why do some bacteria survive antibiotics? | *Small genetic differences | They hide in food | Antibiotics are too weak | The second paragraph explains. | a few may survive because of small genetic differences.
? c | Why are antibiotics useless against colds and flu? | *These illnesses are caused by viruses | The doses are too small | Patients don't take them | The third paragraph explains. | which are caused by viruses, not bacteria
? t | In some countries, antibiotics are used to make animals grow faster. | T | The third paragraph says so. | antibiotics are also widely used in farming to make animals grow faster.
? c | Why is research into new antibiotics difficult? | *It is slow and expensive | Bacteria no longer exist | Governments ban it | The last paragraph explains. | this research is slow and expensive.

## Smart homes and privacy | TE
Imagine a home where the lights turn on when you enter a room, the heating adjusts automatically and you can ask a speaker to play music or order groceries. For millions of people, this smart home is already reality.

Smart devices offer clear benefits. They can save energy by turning off lights and heating when nobody is home. They can make life easier for older people or people with disabilities, who can control their homes with their voice. Security cameras and smart locks allow owners to check their homes from anywhere.

However, these devices also collect large amounts of data. A smart speaker listens for its wake word and may record conversations. Smart TVs can track what you watch, and some devices share information with advertisers. Experts warn that this data can reveal a great deal about our daily routines: when we wake up, when we leave home and even when we argue.

Security is another concern. Like computers, smart devices can be hacked. In some cases, criminals have gained access to home cameras or used poorly protected devices to attack websites. Many devices are sold with weak default passwords that owners never change.

Experts recommend some simple precautions. Before buying a device, check what data it collects and how it is used. Change default passwords, install updates regularly and turn off features you do not need, such as microphones. Smart homes can be convenient, but it is important to stay in control of the information they collect.
? c | How can smart devices save energy? | *By turning off lights and heating when nobody is home | By using solar panels | By making homes smaller | The second paragraph explains. | turning off lights and heating when nobody is home.
? c | What can data from smart devices reveal? | *Our daily routines | Our bank passwords only | Nothing important | The third paragraph explains. | this data can reveal a great deal about our daily routines
? t | Smart devices cannot be hacked. | F | They can be hacked. | smart devices can be hacked.
? s | What do many devices come with that owners never change? | weak default passwords / default passwords | The fourth paragraph says so. | Many devices are sold with weak default passwords that owners never change.
? c | Which precaution do experts recommend? | *Changing default passwords and installing updates | Never using the internet | Buying more devices | The last paragraph says so. | Change default passwords, install updates regularly

## Farms with members | FD
In a typical supermarket, shoppers have no idea who grew their vegetables or how far they have travelled. Community-supported agriculture, often called CSA, offers a different model that connects consumers directly with local farmers.

The system works like a subscription. At the beginning of the growing season, members pay the farmer in advance for a share of the harvest. Then, every week, they receive a box of fresh vegetables and sometimes fruit, eggs or honey. The contents change with the seasons, so members eat what is fresh and local.

For farmers, the advance payment is extremely valuable. It provides money at the start of the season, when they need to buy seeds and equipment, and reduces their dependence on banks and supermarkets. It also means that members share some of the risk. If bad weather destroys part of the harvest, everyone receives a little less.

Members say they enjoy knowing where their food comes from. Many CSA farms invite members to visit, help with the harvest or attend seasonal festivals. Children in particular learn how food is grown.

The model is not for everyone. Members cannot choose exactly what they receive, so they may get a lot of a vegetable they rarely eat. Some people find it hard to pay several months in advance.

Nevertheless, CSA farms have spread to many countries. Supporters see them as a way to build stronger relationships between cities and the countryside, while supporting small farms and more sustainable agriculture.
? c | How does community-supported agriculture work? | *Members pay in advance for a share of the harvest | Farmers sell to supermarkets | Members grow their own food | The second paragraph explains. | members pay the farmer in advance for a share of the harvest.
? c | Why is the advance payment valuable for farmers? | *It provides money when they need seeds and equipment | It is a gift | It replaces all other income | The third paragraph explains. | It provides money at the start of the season, when they need to buy seeds and equipment
? t | If bad weather damages the harvest, members still receive the full amount. | F | Everyone receives a little less. | everyone receives a little less.
? s | What can members do when they visit CSA farms? | help with the harvest / attend seasonal festivals / visit | The fourth paragraph says so. | help with the harvest or attend seasonal festivals.
? c | What is one disadvantage of the model? | *Members cannot choose exactly what they receive | The food is not fresh | The farms are far away | The fifth paragraph explains. | Members cannot choose exactly what they receive
"""

PASSAGES["B2"] += """
## The art of apologising | CO
Everyone makes mistakes, but not everyone knows how to apologise. A poor apology can make a situation worse, while a good one can repair even a seriously damaged relationship.

Researchers who study apologies have identified several key elements. The first is a clear acknowledgement of responsibility. Phrases like "I'm sorry if you were offended" are often seen as weak, because they suggest the problem lies with the other person's reaction rather than with the speaker's behaviour. A stronger apology says, "I'm sorry I did this."

The second element is showing that you understand the harm caused. Explaining how your actions affected the other person shows empathy. However, long explanations of why you behaved badly can sound like excuses.

Third, an effective apology often includes an offer to repair the damage, if this is possible. In one study, this element was rated as one of the most important by people receiving apologies. Finally, a promise to change behaviour in the future gives the apology credibility, but only if the promise is kept.

Timing also matters. An apology that comes too quickly may seem automatic and insincere, while one that comes too late may seem forced. Some researchers suggest that people often feel more satisfied when they have had a chance to express their feelings first.

Of course, apologising requires humility, which is why many people find it difficult. Yet the benefits are significant. A sincere apology can restore trust, reduce anger and, often, strengthen a relationship rather than weaken it.
? c | Why is "I'm sorry if you were offended" seen as weak? | *It suggests the problem is the other person's reaction | It is too long | It is too formal | The second paragraph explains. | they suggest the problem lies with the other person's reaction rather than with the speaker's behaviour.
? c | What can long explanations of bad behaviour sound like? | *Excuses | Empathy | Promises | The third paragraph says so. | long explanations of why you behaved badly can sound like excuses.
? t | In one study, offering to repair the damage was rated as one of the most important elements. | T | The fourth paragraph says so. | this element was rated as one of the most important by people receiving apologies.
? s | What gives an apology credibility, if it is kept? | a promise to change behaviour / a promise to change | The fourth paragraph says so. | a promise to change behaviour in the future gives the apology credibility
? c | What can happen if an apology comes too quickly? | *It may seem automatic and insincere | It always works better | It seems forced | The fifth paragraph explains. | An apology that comes too quickly may seem automatic and insincere

## Living with less | DL
In recent years, a growing number of people have decided to own fewer things. This lifestyle, known as minimalism, has become popular through books, documentaries and social media, where people share photos of tidy, almost empty rooms.

Minimalists argue that owning fewer things can make life simpler and happier. They say that possessions take up not only space but also time and energy: we have to clean them, repair them, organise them and worry about them. By removing items they do not use or truly value, many people report feeling calmer and more focused.

Minimalism can also have financial and environmental benefits. People who buy less save money and produce less waste. Some use the money they save to work fewer hours, travel or pay off debts.

However, the movement has its critics. Some point out that minimalism is easier for people who are already wealthy. If you can afford to replace something whenever you need it, it is easy to give things away. For families with less money, keeping items "just in case" may be a sensible strategy rather than a bad habit. Others note the irony of minimalist products being sold at high prices.

Supporters respond that minimalism is not about owning a specific number of things or having a white, empty home. Rather, it is about being intentional, asking whether each purchase genuinely adds value to your life.

Whether or not people adopt the lifestyle fully, many agree that the question it raises is useful: how much do we really need?
? c | According to minimalists, what do possessions take up? | *Space, time and energy | Only space | Only money | The second paragraph explains. | possessions take up not only space but also time and energy
? t | Some minimalists use the money they save to work fewer hours. | T | The third paragraph says so. | Some use the money they save to work fewer hours
? c | What do critics point out? | *Minimalism is easier for people who are already wealthy | Minimalism is too cheap | Minimalism damages the environment | The fourth paragraph explains. | minimalism is easier for people who are already wealthy.
? s | According to supporters, what is minimalism really about? | being intentional / being intentional about purchases | The fifth paragraph says so. | it is about being intentional
? c | What irony do some critics note? | *Minimalist products are sold at high prices | Minimalists own many houses | Minimalism is popular on social media | The fourth paragraph explains. | the irony of minimalist products being sold at high prices.

## An ageing society | PF
Across the world, people are living longer and having fewer children. As a result, the proportion of older people in the population is growing rapidly. In some countries, more than a quarter of the population is already over sixty-five.

Longer lives are a remarkable achievement, made possible by better healthcare, nutrition and living conditions. But an ageing population also creates challenges. With fewer young people entering the workforce, there are fewer workers paying taxes to support pensions and healthcare for a growing number of retirees.

Healthcare systems face particular pressure. Older people are more likely to have long-term conditions such as diabetes, heart disease and dementia, which require ongoing care. Many countries already lack enough nurses and carers.

Families are also affected. In many cultures, adult children traditionally care for their elderly parents. But as families become smaller and more young people move to cities or abroad for work, this is becoming harder.

Governments are responding in different ways. Some are raising the retirement age so that people work longer. Others encourage immigration to fill labour shortages, or invest in technology, such as robots that help with care tasks.

There are also positive perspectives. Many older people remain healthy and active for years after retirement. They volunteer, care for grandchildren and share their experience with younger generations. Some experts argue that societies should stop seeing older people mainly as a burden and instead create more opportunities for them to contribute.
? c | Why is the proportion of older people growing? | *People live longer and have fewer children | More people move abroad | Healthcare is worse | The first paragraph explains. | people are living longer and having fewer children.
? c | What problem does a smaller workforce cause? | *Fewer workers pay taxes to support pensions and healthcare | Too many jobs disappear | Wages fall | The second paragraph explains. | there are fewer workers paying taxes to support pensions and healthcare
? t | Many countries already lack enough nurses and carers. | T | The third paragraph says so. | Many countries already lack enough nurses and carers.
? s | What are some governments raising? | the retirement age / retirement age | The fifth paragraph says so. | Some are raising the retirement age so that people work longer.
? c | What do some experts argue? | *Societies should create more opportunities for older people to contribute | Older people should stop working | Families should be larger | The last paragraph explains. | create more opportunities for them to contribute.

## Losing the dark | NW
For most of human history, people could look up at night and see thousands of stars. Today, about eighty percent of the world's population lives under skies affected by light pollution, and many children have never seen the Milky Way.

Light pollution is caused by artificial light that shines where it is not needed: street lamps that light the sky as well as the road, bright advertising screens and buildings that stay lit all night. The glow from cities can be seen from hundreds of kilometres away.

The loss of dark skies is not only a problem for astronomers. Many animals depend on natural patterns of light and darkness. Migrating birds can become confused by city lights and crash into buildings. Newly hatched sea turtles, which find the sea by moving towards the brightest horizon, may crawl towards roads instead. Insects are drawn to lights in huge numbers, which affects the animals that depend on them for food.

Humans may be affected too. Our bodies produce a hormone called melatonin in darkness, which helps regulate sleep. Exposure to bright light at night may disrupt this process.

Unlike many environmental problems, light pollution is relatively easy to reduce. Lights can be shielded so they point downwards, switched off when not needed or replaced with warmer, less intense colours. Some places have created "dark sky reserves", where lighting is carefully controlled. These areas have become popular with tourists who want to experience a truly dark night.
? s | About what percentage of the world's population lives under light-polluted skies? | about eighty percent / eighty percent / 80% / 80 percent | The first paragraph says so. | about eighty percent of the world's population
? c | What causes light pollution? | *Artificial light that shines where it is not needed | The moon | Fires | The second paragraph explains. | Light pollution is caused by artificial light that shines where it is not needed
? c | Why may sea turtles crawl towards roads? | *They move towards the brightest horizon | They look for food | They are afraid of the sea | The third paragraph explains. | which find the sea by moving towards the brightest horizon
? t | Melatonin is produced in bright light. | F | It is produced in darkness. | Our bodies produce a hormone called melatonin in darkness
? t | Light pollution is relatively easy to reduce. | T | The last paragraph says so. | light pollution is relatively easy to reduce.

## Esports goes mainstream | HS
Twenty years ago, video games were seen by many as a hobby for teenagers in their bedrooms. Today, professional video gaming, known as esports, fills stadiums and attracts online audiences of millions.

Major esports tournaments offer prize money worth millions of dollars, and top players are treated like celebrities. Professional teams have coaches, analysts and even psychologists. Players often train for eight hours or more a day, studying strategies and practising reactions.

The industry's growth has been driven by streaming platforms, where fans can watch games live and interact with players. Sponsors, including major brands, have invested heavily, and some universities now offer scholarships for talented gamers.

Despite its popularity, esports faces questions. Is it really a sport? Supporters argue that it requires skill, strategy, teamwork and extremely fast reactions, just like traditional sports. Critics reply that it lacks physical exercise, which they see as essential to the definition of sport.

There are also concerns about players' wellbeing. Long training hours can lead to physical problems, such as wrist and back pain, as well as stress and burnout. Many professional careers are short, and some players retire before the age of twenty-five, often without qualifications for other jobs.

As a result, some teams now include physical exercise in training schedules, limit practice hours and encourage players to continue their education. Whatever people think about its status, esports is clearly here to stay, and its audience continues to grow.
? c | How were video games seen twenty years ago? | *As a hobby for teenagers in their bedrooms | As a professional sport | As an Olympic event | The first paragraph explains. | video games were seen by many as a hobby for teenagers in their bedrooms.
? s | How long do players often train each day? | eight hours or more / eight hours / 8 hours | The second paragraph says so. | Players often train for eight hours or more a day
? c | What has driven the industry's growth? | *Streaming platforms | Television news | Newspapers | The third paragraph explains. | The industry's growth has been driven by streaming platforms
? t | Critics say esports is a sport because it requires skill. | F | Critics say it lacks physical exercise. | Critics reply that it lacks physical exercise
? c | What have some teams done to protect players? | *Included exercise, limited practice and encouraged education | Increased training hours | Banned streaming | The last paragraph explains. | some teams now include physical exercise in training schedules, limit practice hours and encourage players to continue their education.

## Towards a cashless society | MS
In many cities, it is now possible to go for weeks without touching a coin or a banknote. People pay for coffee with their phones, transfer money to friends through apps and shop online with saved card details. Some countries are moving rapidly towards becoming cashless societies.

Digital payments offer clear advantages. They are fast and convenient, and they make it easier to track spending. Businesses save time and money on handling cash, and the risk of robbery is lower. Governments also benefit, because digital payments are easier to trace, which can reduce tax evasion and crime.

However, a cashless society also has disadvantages. Older people and those who are less comfortable with technology may find digital payments difficult. People without bank accounts, often those with the lowest incomes, risk being excluded from basic services.

There are also concerns about privacy. Every digital payment leaves a record, revealing where people go, what they buy and who they pay. Some people worry about how this information might be used by companies or governments.

Another issue is resilience. If payment systems fail because of technical problems, power cuts or cyberattacks, people may be unable to buy essential goods. Cash, by contrast, works without electricity or internet connections.

Because of these concerns, some countries that were moving quickly away from cash have changed course. They now require banks and shops to continue accepting cash, at least for essential services, so that everyone can still take part in the economy.
? c | Why do governments benefit from digital payments? | *They are easier to trace, reducing tax evasion and crime | They are free | They create jobs | The second paragraph explains. | digital payments are easier to trace, which can reduce tax evasion and crime.
? c | Who risks being excluded in a cashless society? | *People without bank accounts | Young people | Shop owners | The third paragraph explains. | People without bank accounts, often those with the lowest incomes, risk being excluded
? t | Every digital payment leaves a record. | T | The fourth paragraph says so. | Every digital payment leaves a record
? s | What does cash work without? | electricity or internet connections / electricity / internet | The fifth paragraph says so. | Cash, by contrast, works without electricity or internet connections.
? c | What have some countries done? | *Required banks and shops to keep accepting cash | Banned cash completely | Stopped digital payments | The last paragraph explains. | They now require banks and shops to continue accepting cash

## The trouble with open-plan offices | WK
In the past few decades, many companies have removed walls and private offices, replacing them with large open-plan spaces where employees sit together at long rows of desks. The idea was to encourage communication, teamwork and creativity, while also saving money on space.

However, research has produced some surprising results. In one study, researchers measured how employees interacted before and after their company moved to an open-plan office. Instead of increasing, face-to-face conversations fell by around seventy percent. Employees sent more emails and messages instead.

Why would this happen? One explanation is that people feel a lack of privacy when everyone can see and hear them. To protect their concentration and personal space, many put on headphones and avoid conversations. Noise is another problem. Phone calls and nearby discussions make it difficult to focus on complex tasks, and studies have linked noisy environments to lower productivity and higher stress.

Open-plan offices may also spread illness more easily. Some research has found that employees in open offices take more sick days than those in private offices.

This does not mean that all open offices are bad. They can work well for teams whose tasks require constant collaboration. The problem is that most jobs require both collaboration and quiet, focused work.

As a result, many companies are now adopting more flexible designs. These offer a mix of spaces: open areas for teamwork, quiet rooms for concentration and small booths for phone calls, allowing employees to choose the environment that suits each task.
? c | What was the idea behind open-plan offices? | *To encourage communication and save money on space | To reduce teamwork | To give everyone a private office | The first paragraph explains. | The idea was to encourage communication, teamwork and creativity, while also saving money on space.
? s | By how much did face-to-face conversations fall in one study? | around seventy percent / seventy percent / 70% / 70 percent | The second paragraph says so. | face-to-face conversations fell by around seventy percent.
? c | Why do many employees put on headphones? | *To protect their concentration and personal space | To listen to music for fun | Because managers require it | The third paragraph explains. | To protect their concentration and personal space, many put on headphones
? t | Some research has found employees in open offices take fewer sick days. | F | They take more sick days. | employees in open offices take more sick days than those in private offices.
? c | What do flexible office designs offer? | *A mix of spaces for different tasks | Only open areas | Only private offices | The last paragraph explains. | These offer a mix of spaces

## Gardens on the roof | HF
Look down on many modern cities from above, and you might be surprised to see green. On rooftops once covered with concrete or metal, gardens are growing: grass, flowers, vegetables and even small trees.

Green roofs have a long history, but they have become increasingly popular as cities search for ways to deal with heat, flooding and pollution. A green roof is made of several layers, including a waterproof base, a drainage layer, soil and plants.

The benefits are numerous. Plants absorb heat, so buildings with green roofs stay cooler in summer and need less air conditioning. In winter, the extra layers provide insulation. Green roofs also absorb rainwater, which reduces the pressure on city drains during heavy storms and lowers the risk of flooding.

They also support nature. Bees, butterflies and birds find food and shelter on green roofs, creating small habitats in the middle of the city. Some green roofs are used to grow food for restaurants or local communities, and others provide pleasant spaces where office workers can relax.

There are challenges, however. Green roofs are more expensive to build than ordinary roofs, and not every building is strong enough to support the extra weight of wet soil. They also require regular maintenance, such as watering and removing weeds.

To encourage their use, some cities offer financial support or require green roofs on new large buildings. Supporters argue that, over time, the energy savings and environmental benefits more than justify the initial cost.
? c | Why have green roofs become more popular? | *Cities are looking for ways to deal with heat, flooding and pollution | They are cheaper than normal roofs | They need no maintenance | The second paragraph explains. | as cities search for ways to deal with heat, flooding and pollution.
? c | How do green roofs reduce flooding? | *They absorb rainwater | They make drains bigger | They stop rain falling | The third paragraph explains. | Green roofs also absorb rainwater, which reduces the pressure on city drains
? t | Every building can support a green roof. | F | Not every building is strong enough. | not every building is strong enough to support the extra weight of wet soil.
? s | What do some cities require on new large buildings? | green roofs | The last paragraph says so. | require green roofs on new large buildings.
? c | What do supporters argue about the cost? | *Savings and benefits justify the initial cost over time | It is too high to justify | It is the same as ordinary roofs | The last paragraph explains. | the energy savings and environmental benefits more than justify the initial cost.

## The placebo effect | HE
In medical trials, researchers often compare a new drug with a placebo, a pill that looks the same but contains no active medicine. Surprisingly, many patients who receive the placebo report that they feel better. This is known as the placebo effect.

The effect is particularly strong for conditions that involve subjective experiences, such as pain, nausea, tiredness and anxiety. In some studies, a significant proportion of patients receiving placebos experienced real improvements in their symptoms.

How can a pill with no medicine work? Scientists believe expectation plays a major role. When patients believe they are receiving treatment, the brain may release natural chemicals that reduce pain. The ritual of treatment, such as a visit to a doctor or the experience of taking a pill, may also influence how people feel.

Interestingly, details matter. Studies have found that two placebo pills can be more effective than one, that injections may work better than pills and that expensive placebos can work better than cheap ones. Even the colour of the pill can make a difference.

The placebo effect has limits. It cannot cure infections, mend broken bones or shrink tumours. Its effects are mainly on symptoms, not on the underlying disease.

The effect raises ethical questions. Is it acceptable for doctors to give placebos if patients believe they are real medicine? Recent research has found that placebos can sometimes help even when patients know they are taking them. This suggests that the experience of care itself may have healing power.
? c | What is a placebo? | *A pill that looks real but contains no active medicine | A new drug | A strong painkiller | The first paragraph explains. | a pill that looks the same but contains no active medicine.
? c | For which conditions is the placebo effect particularly strong? | *Pain, nausea, tiredness and anxiety | Broken bones | Infections | The second paragraph says so. | such as pain, nausea, tiredness and anxiety.
? s | What do scientists believe plays a major role in the effect? | expectation | The third paragraph says so. | Scientists believe expectation plays a major role.
? t | Placebos can shrink tumours. | F | They cannot. | It cannot cure infections, mend broken bones or shrink tumours.
? t | Placebos can sometimes help even when patients know they are taking them. | T | The last paragraph says so. | placebos can sometimes help even when patients know they are taking them.

## Citizen scientists | EN
You don't need a laboratory or a university degree to contribute to science. Around the world, millions of ordinary people take part in "citizen science" projects, collecting data that helps researchers answer important questions.

Citizen science projects cover a wide range of subjects. Volunteers count birds in their gardens, record when flowers bloom, photograph insects, measure rainfall or monitor water quality in local rivers. Others work online, classifying images of galaxies, transcribing old documents or identifying animals in thousands of photos taken by hidden cameras.

For scientists, the benefits are enormous. Some projects require data from huge areas or over many years, which would be impossible for a small team of researchers to collect. Volunteers can provide observations from thousands of locations at the same time. Bird counts, for example, have helped scientists track how climate change is affecting migration patterns.

Data quality is sometimes a concern, because volunteers may make mistakes. Researchers address this by training participants, using simple methods and checking unusual results. With large numbers of observations, individual errors often have little effect on overall patterns.

Volunteers benefit too. Many say that taking part helps them learn about science and notice nature more carefully. For schools, citizen science offers a practical way for students to experience real research.

Some projects have led to remarkable discoveries, including new planets and previously unknown species. Perhaps most importantly, citizen science helps people feel connected to the world around them and to the scientific process.
? c | What is citizen science? | *Ordinary people collecting data for research | Scientists working in cities | A type of university degree | The first paragraph explains. | ordinary people take part in "citizen science" projects, collecting data that helps researchers answer important questions.
? c | Why are volunteers valuable to scientists? | *They can provide observations from thousands of locations | They are cheaper than computers | They know more than scientists | The third paragraph explains. | Volunteers can provide observations from thousands of locations at the same time.
? s | What have bird counts helped scientists track? | how climate change is affecting migration patterns / migration patterns | The third paragraph says so. | Bird counts, for example, have helped scientists track how climate change is affecting migration patterns.
? t | Individual errors always ruin citizen science data. | F | With large numbers, they often have little effect. | individual errors often have little effect on overall patterns.
? t | Citizen science projects have led to the discovery of new species. | T | The last paragraph says so. | including new planets and previously unknown species.

## Ride-hailing and the city | TP
Within a few years, ride-hailing apps have transformed transport in cities around the world. With a few taps on a smartphone, passengers can book a car or motorbike, see the price in advance and track the driver's arrival.

For passengers, the advantages are clear. Ride-hailing is often cheaper and more convenient than traditional taxis, and the fixed price removes the worry of being overcharged. Ratings for drivers and passengers encourage good behaviour, and the record of every trip can increase safety.

For drivers, the apps offer flexible work. Many people drive part-time to supplement other income. However, drivers often complain about falling earnings, as companies take a significant commission from each ride and competition between drivers increases.

The impact on cities is complex. Early supporters predicted that ride-hailing would reduce car ownership and traffic. In some places, fewer young people now buy cars. However, several studies have found that ride-hailing has increased traffic in city centres, because cars often drive around empty while waiting for passengers, and some people use ride-hailing instead of buses or walking.

Traditional taxi drivers have also been affected. In many cities, they have protested, arguing that ride-hailing companies do not follow the same rules and licences.

Cities are responding with new regulations, such as limits on the number of vehicles, extra fees in busy areas and requirements for driver insurance. The challenge is to keep the convenience that passengers value while supporting public transport and reducing congestion.
? c | What removes the worry of being overcharged? | *The fixed price | Driver ratings | Cash payments | The second paragraph explains. | the fixed price removes the worry of being overcharged.
? c | What do drivers often complain about? | *Falling earnings | Too few passengers ever | Long training | The third paragraph explains. | drivers often complain about falling earnings
? t | Several studies found ride-hailing has reduced traffic in all city centres. | F | It has increased traffic in city centres. | ride-hailing has increased traffic in city centres
? s | Why do cars add to traffic while waiting? | they drive around empty / cars often drive around empty | The fourth paragraph explains. | cars often drive around empty while waiting for passengers
? c | What have traditional taxi drivers argued? | *Ride-hailing companies do not follow the same rules | Ride-hailing is too slow | Passengers prefer taxis | The fifth paragraph explains. | arguing that ride-hailing companies do not follow the same rules and licences.

## Waste on the plate | FD
Every year, restaurants throw away enormous amounts of food. Some of it is food that customers leave on their plates, but much is wasted before it ever reaches a table: ingredients that go bad, dishes prepared but not sold and vegetables rejected because they do not look perfect.

Food waste is not only a waste of money. Producing food requires land, water and energy, and when it ends up in landfill, it releases methane, a powerful greenhouse gas. Experts estimate that food waste is responsible for a significant share of global emissions.

Some restaurants have found creative ways to reduce waste. They plan menus more carefully, using the same ingredients in several dishes. Vegetable peels and leftover bread may become soups, sauces or stocks. Some chefs design dishes specifically to use parts of vegetables or animals that are usually thrown away.

Portion size is another factor. When portions are too large, customers often leave food behind. Several restaurants now offer smaller portions or allow customers to choose the size. Others encourage diners to take leftovers home.

Technology is also helping. Apps connect restaurants and bakeries with customers who can buy surplus food at a discount at the end of the day. Some businesses use smart scales to measure what is thrown away, helping chefs identify where waste happens.

Food that cannot be sold can often be donated to charities or composted. Reducing waste requires effort, but many restaurants find that it also reduces costs, making it good for both the environment and business.
? c | Where is much restaurant food wasted? | *Before it reaches a table | Only on customers' plates | In delivery trucks | The first paragraph explains. | much is wasted before it ever reaches a table
? s | What gas does food in landfill release? | methane | The second paragraph says so. | it releases methane, a powerful greenhouse gas.
? c | What may vegetable peels and leftover bread become? | *Soups, sauces or stocks | Animal food only | Decorations | The third paragraph says so. | Vegetable peels and leftover bread may become soups, sauces or stocks.
? t | Some apps let customers buy surplus food at a discount. | T | The fifth paragraph says so. | customers who can buy surplus food at a discount at the end of the day.
? t | Reducing waste always increases a restaurant's costs. | F | Many find it reduces costs. | many restaurants find that it also reduces costs

## The influencer economy | SH
A decade ago, the word "influencer" was rarely used. Today, influencers, people with large followings on social media, are a major force in marketing. Brands pay them to promote products, from clothes and cosmetics to holidays and financial services.

Companies value influencers because their followers often trust them more than traditional advertisements. Influencers share their daily lives, and followers may feel they know them personally. A recommendation from someone who seems like a friend can be very persuasive.

Interestingly, influencers do not always need millions of followers. So-called micro-influencers, with smaller audiences of a few thousand people, often have closer relationships with their followers and higher levels of engagement. For brands, they may also be much cheaper.

However, the industry faces criticism. In many cases, followers cannot tell whether a post is a genuine recommendation or a paid advertisement. Many countries now require influencers to label sponsored content clearly, but these rules are not always followed.

There are also concerns about the effects on young people. Influencers often present carefully edited images of perfect lives, bodies and possessions. Some studies suggest that constantly comparing oneself with these images can lower self-esteem and encourage excessive spending.

On the other hand, some influencers use their platforms positively, sharing educational content, promoting mental health awareness or supporting social causes. Experts encourage followers, especially young people, to think critically about what they see: Who benefits from this post? Is it an advertisement? Does it show reality?
? c | Why do companies value influencers? | *Followers often trust them more than traditional advertisements | They are always cheap | They make the products | The second paragraph explains. | their followers often trust them more than traditional advertisements.
? c | What is an advantage of micro-influencers? | *Closer relationships with followers and higher engagement | Millions of followers | Television shows | The third paragraph explains. | often have closer relationships with their followers and higher levels of engagement.
? t | Rules on labelling sponsored content are always followed. | F | They are not always followed. | these rules are not always followed.
? s | What can constant comparison with edited images lower? | self-esteem | The fifth paragraph says so. | can lower self-esteem and encourage excessive spending.
? c | What do experts encourage followers to do? | *Think critically about what they see | Stop using social media | Become influencers | The last paragraph explains. | Experts encourage followers, especially young people, to think critically about what they see

## Learning from failure | WK
In many cultures, failure is seen as something shameful. Students fear bad grades, employees hide mistakes from their managers, and entrepreneurs whose businesses close may be seen as losers. Yet some of the most successful companies and individuals argue that failure is an essential part of success.

Consider the world of start-ups. Most new businesses fail within a few years. However, research suggests that entrepreneurs who have failed before are often more successful in their next attempts. They have learned what does not work, built networks and developed resilience.

Some organisations now actively encourage employees to share failures. A few companies even hold regular meetings where teams discuss projects that did not succeed and what they learned. The aim is to create an environment where people feel safe enough to take risks and admit mistakes early, before small problems become large ones.

This idea is sometimes called psychological safety. Studies of teams have found that the most effective ones are not those that make the fewest mistakes, but those where members feel comfortable talking openly about errors. In hospitals, for example, teams that report mistakes more often may actually be safer, because problems are identified and corrected.

Of course, learning from failure does not mean celebrating carelessness. The value of a failure depends on what we do afterwards: reflecting honestly, understanding the causes and changing our approach.

Educators are also applying these ideas, encouraging students to see mistakes as opportunities to learn rather than signs of a lack of ability.
? c | How is failure seen in many cultures? | *As something shameful | As a reason to celebrate | As unimportant | The first paragraph explains. | In many cultures, failure is seen as something shameful.
? c | Why are entrepreneurs who have failed often more successful next time? | *They have learned what doesn't work and developed resilience | They have more money | They are older | The second paragraph explains. | They have learned what does not work, built networks and developed resilience.
? s | What is the idea of feeling safe to admit mistakes called? | psychological safety | The fourth paragraph names it. | This idea is sometimes called psychological safety.
? t | The most effective teams make the fewest mistakes. | F | They talk openly about errors. | the most effective ones are not those that make the fewest mistakes
? t | Learning from failure means celebrating carelessness. | F | It does not. | learning from failure does not mean celebrating carelessness.

## Connected but lonely? | TE
Social media was designed to connect people. Today, billions of users share photos, send messages and follow the lives of friends and strangers. Yet many people, especially young adults, report feeling lonely. Could social media be part of the problem?

The relationship is complex. Some studies have found that people who spend a lot of time on social media are more likely to feel lonely and anxious. However, this does not necessarily mean that social media causes loneliness. It is also possible that lonely people spend more time online looking for connection.

Researchers have found that how people use social media matters more than how much. Active use, such as messaging friends, commenting thoughtfully and organising meetings, tends to be linked with positive feelings. Passive use, such as endlessly scrolling through other people's posts, is more often linked with negative feelings.

One reason may be social comparison. Social media often shows the highlights of other people's lives: holidays, celebrations and achievements. Comparing our ordinary lives with these carefully selected moments can make us feel that we are missing out.

Social media can also replace rather than support face-to-face interaction. Time spent online may reduce time spent with friends in person, which research suggests is particularly important for wellbeing.

On the other hand, social media can be a lifeline for people who feel isolated, such as those with rare illnesses or those living far from family. Experts suggest a balanced approach: using social media to strengthen real relationships, not to replace them.
? c | What do many people report despite social media? | *Feeling lonely | Feeling more connected than ever | Having more friends in person | The first paragraph explains. | many people, especially young adults, report feeling lonely.
? t | Studies prove social media causes loneliness. | F | It does not necessarily mean that. | this does not necessarily mean that social media causes loneliness.
? c | Which use of social media is linked with positive feelings? | *Active use, like messaging friends | Endless scrolling | Watching advertisements | The third paragraph explains. | Active use, such as messaging friends, commenting thoughtfully and organising meetings, tends to be linked with positive feelings.
? s | What can comparing our lives with others' highlights make us feel? | that we are missing out / missing out | The fourth paragraph says so. | can make us feel that we are missing out.
? c | For whom can social media be a lifeline? | *People who feel isolated | People with many friends | Professional influencers | The last paragraph explains. | social media can be a lifeline for people who feel isolated

## Museums go digital | ED
Not long ago, visiting a famous museum meant travelling to it. Today, many of the world's great collections can be explored from a laptop or phone. Museums have put millions of images online, created virtual tours and even developed apps that use augmented reality.

Digitisation has clear benefits. People who cannot travel because of cost, distance or disability can now see artworks and historical objects in high detail. Students and researchers can study collections without visiting archives in person. Online images often allow viewers to zoom in on details that would be impossible to see in a crowded gallery.

Museums also use technology to attract new audiences. Interactive exhibitions, online games and social media campaigns appeal to younger visitors who might otherwise find museums boring.

Some people worried that putting collections online would reduce the number of visitors. In fact, many museums report the opposite. Seeing objects online often makes people want to experience them in person. A photograph, however detailed, cannot fully reproduce the scale, texture or atmosphere of an original artwork.

Digitisation also raises questions. Creating and maintaining digital collections is expensive, and smaller museums may lack the resources. There are debates about copyright and about whether museums should charge for high-quality images.

Despite these challenges, most experts see digital technology as an opportunity. Rather than replacing the museum experience, it extends it, allowing museums to reach people far beyond their walls and to preserve records of fragile objects for future generations.
? c | Who benefits from digitisation? | *People who cannot travel, students and researchers | Only museum staff | Only tourists | The second paragraph explains. | People who cannot travel because of cost, distance or disability can now see artworks
? c | Why do museums use interactive exhibitions and online games? | *To attract younger visitors | To reduce costs | To replace their buildings | The third paragraph explains. | appeal to younger visitors who might otherwise find museums boring.
? t | Putting collections online has reduced visitor numbers at many museums. | F | Many report the opposite. | many museums report the opposite.
? s | What can a photograph not fully reproduce? | the scale, texture or atmosphere / scale, texture and atmosphere | The fourth paragraph says so. | cannot fully reproduce the scale, texture or atmosphere of an original artwork.
? c | What challenge do smaller museums face? | *They may lack the resources | They have too many visitors | They cannot use social media | The fifth paragraph explains. | smaller museums may lack the resources.

## Living with heatwaves | NW
Heatwaves, periods of unusually hot weather lasting several days, are becoming more frequent and more intense in many parts of the world. Scientists link this trend to climate change, and they warn that extreme heat is one of the deadliest weather hazards.

Unlike storms or floods, heatwaves cause little visible damage, so their dangers are often underestimated. Yet extreme heat can be life-threatening. When the body cannot cool down, people may suffer heat exhaustion or heatstroke. Older people, young children, outdoor workers and people with health conditions are especially at risk.

Cities are particularly vulnerable because of the urban heat island effect. Buildings and roads absorb heat during the day and release it at night, so temperatures stay high even after sunset, preventing people from recovering.

Many cities have created heat action plans. These include early warning systems that alert residents before heatwaves, and cooling centres, air-conditioned public buildings where people can rest. Some cities send volunteers to check on older people living alone, because many heat-related deaths happen at home.

Long-term solutions focus on design. Planting trees, creating parks, using reflective materials on roofs and roads and designing buildings with better ventilation can all reduce temperatures.

Individuals can protect themselves too. Experts recommend drinking water regularly, avoiding strenuous activity during the hottest hours, wearing light clothing and keeping homes cool by closing curtains during the day. Checking on neighbours, especially elderly ones, is also a simple action that can save lives.
? c | Why are the dangers of heatwaves often underestimated? | *They cause little visible damage | They are very short | They happen only in deserts | The second paragraph explains. | heatwaves cause little visible damage, so their dangers are often underestimated.
? c | Why do temperatures in cities stay high after sunset? | *Buildings and roads release heat at night | There is no wind | People use more cars | The third paragraph explains. | Buildings and roads absorb heat during the day and release it at night
? s | What are cooling centres? | air-conditioned public buildings / air-conditioned public buildings where people can rest | The fourth paragraph explains. | cooling centres, air-conditioned public buildings where people can rest.
? t | Many heat-related deaths happen at home. | T | The fourth paragraph says so. | many heat-related deaths happen at home.
? c | What do experts recommend? | *Closing curtains during the day | Exercising at noon | Wearing dark clothes | The last paragraph says so. | keeping homes cool by closing curtains during the day.

## Pets and wellbeing | AN
Many pet owners say their animals make them happier, and research increasingly supports this view. Studies have linked pet ownership with lower stress, reduced feelings of loneliness and even better physical health.

Dogs, in particular, encourage physical activity. Owners who walk their dogs regularly are more likely to meet recommended levels of exercise. Walking a dog also creates social opportunities, as owners often stop to chat with neighbours and other dog walkers.

Pets can also provide emotional support. Stroking an animal has been shown to lower heart rate and blood pressure in some studies. For people who live alone, a pet can offer companionship and a reason to keep a daily routine. Some hospitals and care homes now use therapy animals to comfort patients and residents.

However, researchers caution against simple conclusions. Some studies have found no clear difference in wellbeing between pet owners and non-owners. It is also possible that people who are already healthier and happier are more likely to own pets.

Pet ownership also brings responsibilities and costs. Animals require time, attention, food and veterinary care. When people underestimate these demands, pets may be neglected or given up. Animal shelters receive many animals from owners who could no longer care for them.

Experts advise people considering a pet to think carefully about their lifestyle, budget and living space. The right pet, chosen thoughtfully, can bring great joy, but the decision should be made with the animal's wellbeing in mind as well as the owner's.
? c | What do studies link pet ownership with? | *Lower stress and less loneliness | Higher stress | More illness | The first paragraph explains. | lower stress, reduced feelings of loneliness and even better physical health.
? c | How do dogs create social opportunities? | *Owners chat with others on walks | Dogs make phone calls | Owners join clubs automatically | The second paragraph explains. | owners often stop to chat with neighbours and other dog walkers.
? s | Where are therapy animals used? | hospitals and care homes / in hospitals and care homes | The third paragraph says so. | Some hospitals and care homes now use therapy animals
? t | All studies show pet owners are happier than non-owners. | F | Some found no clear difference. | Some studies have found no clear difference in wellbeing between pet owners and non-owners.
? c | What should people think about before getting a pet? | *Lifestyle, budget and living space | Only the pet's colour | The price of the pet only | The last paragraph says so. | think carefully about their lifestyle, budget and living space.

## Schools that look different | ED
Most people imagine a classroom as rows of desks facing a board at the front. This design has changed little in over a century. However, some architects and educators believe that the physical environment of a school has a significant effect on how students learn.

Research supports some of these ideas. Studies have found that natural light, good air quality and comfortable temperatures can improve concentration and test results. In one study of classrooms, factors such as light, temperature and air quality were linked to noticeable differences in students' progress.

New school designs often replace traditional classrooms with flexible spaces. Furniture can be moved easily, allowing students to work individually, in small groups or as a whole class. Some schools include quiet corners for reading, outdoor learning areas and large shared spaces where different classes can work together.

Supporters argue that these designs encourage collaboration, creativity and independence, skills that are important in modern workplaces. Students can choose the environment that suits each task.

Critics, however, warn that open, flexible spaces can be noisy and distracting, especially for students who need quiet to concentrate. Changing the building alone is not enough. Teachers need training and support to use new spaces effectively, otherwise they may simply teach in the traditional way in a new room.

Most experts agree that the best school buildings combine good basic conditions, such as light, fresh air and quiet, with flexibility. The building, they say, should support good teaching rather than replace it.
? c | How long has the traditional classroom design changed little? | *Over a century | About ten years | Since last year | The first paragraph says so. | This design has changed little in over a century.
? c | Which factors were linked to students' progress? | *Light, temperature and air quality | Desk colours | The number of teachers | The second paragraph says so. | factors such as light, temperature and air quality were linked to noticeable differences in students' progress.
? t | In flexible spaces, furniture can be moved easily. | T | The third paragraph says so. | Furniture can be moved easily
? s | What do teachers need to use new spaces effectively? | training and support | The fifth paragraph says so. | Teachers need training and support to use new spaces effectively
? c | What do most experts agree about school buildings? | *They should support good teaching, not replace it | They should all be open spaces | They are unimportant | The last paragraph explains. | The building, they say, should support good teaching rather than replace it.

## The city after dark | PT
When the offices close and the sun goes down, many cities do not sleep. Restaurants, bars, theatres, cinemas, night markets, delivery services and hospitals keep running. Together, these activities form what planners call the night-time economy.

In many large cities, the night-time economy is worth billions of dollars and employs a significant number of people. It also contributes to a city's identity and attractiveness. Lively evening streets draw tourists and make cities more appealing places to live, especially for young people.

However, managing the city at night presents challenges. Residents living near busy entertainment areas often complain about noise, litter and anti-social behaviour. Public transport may stop running late at night, leaving workers and visitors with limited options to get home safely. Night-shift workers, such as cleaners, nurses and security guards, may face long and expensive journeys.

Some cities have appointed a "night mayor", an official responsible for night-time issues. This person works with businesses, residents, police and transport providers to find solutions. Measures may include night buses, better street lighting, rules on noise and opening hours, and programmes to make venues safer.

Experts also encourage cities to diversify night-time activities. Instead of focusing only on bars and alcohol, they suggest late opening of museums, libraries, shops and sports facilities. This can attract a wider range of people, including families and older residents, and create a safer, more welcoming atmosphere.

Planned well, the night-time economy can benefit the whole city, not only those who enjoy going out late.
? c | What does the night-time economy include? | *Restaurants, theatres, delivery services and hospitals at night | Only bars | Only offices | The first paragraph lists it. | Restaurants, bars, theatres, cinemas, night markets, delivery services and hospitals keep running.
? c | What do residents near busy entertainment areas complain about? | *Noise, litter and anti-social behaviour | Too few shops | High taxes | The third paragraph explains. | Residents living near busy entertainment areas often complain about noise, litter and anti-social behaviour.
? s | What is the official responsible for night-time issues called? | a night mayor / night mayor | The fourth paragraph says so. | Some cities have appointed a "night mayor"
? t | Experts suggest focusing only on bars at night. | F | They suggest diversifying activities. | Instead of focusing only on bars and alcohol
? c | Which activity do experts suggest opening late? | *Museums and libraries | Schools | Banks | The fifth paragraph says so. | they suggest late opening of museums, libraries, shops and sports facilities.

## A second career | WK
In the past, many people expected to stay in the same profession for their whole working lives. Today, career changes are increasingly common. People retrain as nurses after years in banking, leave office jobs to become teachers or start businesses in completely new fields, sometimes in their forties or fifties.

There are many reasons for these changes. Some people feel that their work lacks meaning. Others are affected by technology, as automation changes or eliminates certain jobs. Longer working lives also play a role. If people work until their late sixties or seventies, a career that began at twenty-two may not remain satisfying for over forty years.

Changing careers can be challenging. It may involve returning to education, accepting a lower salary at first and starting at a junior level. Some people worry about competing with younger colleagues or about whether employers will value their age.

However, career changers often bring valuable strengths. Skills developed in one field, such as communication, management and problem-solving, can be useful in another. Experience of life and work can also make people more patient and confident.

Experts offer some advice. Before making a big change, it can help to try the new field through volunteering, short courses or conversations with people who already work in it. Financial planning is also important, especially if retraining will take time.

Perhaps most importantly, career changers need to accept that the transition may take time. For many, however, the reward of doing work they genuinely enjoy makes the effort worthwhile.
? c | What did people in the past expect? | *To stay in the same profession their whole lives | To change careers often | To retire at forty | The first paragraph explains. | many people expected to stay in the same profession for their whole working lives.
? c | Which reason for career changes is mentioned? | *Technology changing or eliminating jobs | Shorter working lives | Higher salaries everywhere | The second paragraph explains. | Others are affected by technology, as automation changes or eliminates certain jobs.
? t | Changing careers may involve accepting a lower salary at first. | T | The third paragraph says so. | accepting a lower salary at first
? s | Name one way to try a new field before changing. | volunteering / short courses / conversations with people in the field | The fifth paragraph lists ways. | try the new field through volunteering, short courses or conversations with people who already work in it.
? c | What do career changers need to accept? | *The transition may take time | They will earn more immediately | They must change again soon | The last paragraph explains. | career changers need to accept that the transition may take time.

## Corridors for wildlife | AN
As cities, roads and farms expand, natural habitats are increasingly divided into small, isolated pieces. For many animals, this is a serious problem. Populations trapped in small areas may struggle to find food, mates and new territory, and they become more vulnerable to disease and inbreeding.

One solution is the wildlife corridor, a strip of habitat that connects separate natural areas. Corridors can take many forms: belts of forest between parks, hedges along fields, tunnels under roads or bridges covered with plants that allow animals to cross busy motorways safely.

Research suggests that corridors can be effective. In some regions, wildlife bridges over highways have significantly reduced collisions between vehicles and large animals such as deer, which also makes roads safer for drivers. Cameras have recorded many species using these crossings, from bears to small mammals.

Corridors also help species adapt to climate change. As temperatures rise, many plants and animals need to move to cooler areas. Without connected habitats, they may be unable to do so.

Creating corridors is not always easy. It requires cooperation between governments, landowners and communities, and land for corridors can be expensive. Some critics question whether corridors work equally well for all species.

Nevertheless, many conservation experts see connectivity as essential. Protecting individual parks is important, they argue, but nature also needs pathways between them. Even small actions, such as planting native trees along rivers or leaving gaps in fences, can help create a network that allows wildlife to move and survive.
? c | What problem do animals in small, isolated areas face? | *Difficulty finding food, mates and territory | Too much food | Fewer predators | The first paragraph explains. | may struggle to find food, mates and new territory
? s | What is a wildlife corridor? | a strip of habitat that connects separate natural areas / a strip of habitat connecting natural areas | The second paragraph explains. | a strip of habitat that connects separate natural areas.
? t | Wildlife bridges have increased collisions with deer. | F | They have significantly reduced them. | wildlife bridges over highways have significantly reduced collisions
? c | How do corridors help with climate change? | *They allow species to move to cooler areas | They lower temperatures | They stop rain | The fourth paragraph explains. | many plants and animals need to move to cooler areas.
? c | Which small action can help, according to the text? | *Planting native trees along rivers | Building more fences | Removing all hedges | The last paragraph says so. | planting native trees along rivers or leaving gaps in fences

## Small homes, big ideas | HF
As house prices rise in many cities, some people are choosing to live in very small homes. The tiny house movement promotes homes of often less than thirty square metres, sometimes built on wheels so they can be moved.

Supporters are attracted by several advantages. Tiny houses cost much less to build or buy than conventional homes, allowing owners to avoid large mortgages. They use less energy for heating and cooling, and their small size encourages owners to buy fewer possessions. Many tiny house owners say they value the freedom this lifestyle gives them, including more time and money for travel and hobbies.

Design is crucial. Clever use of space allows tiny houses to include everything needed for daily life. Beds may be placed in lofts, tables may fold away and stairs may contain storage drawers.

However, tiny living is not for everyone. Families with children may find the space too limited, and sharing such a small area can create tension. Finding land can also be difficult. In many places, planning rules do not allow people to live permanently in tiny houses, or require minimum home sizes.

Critics also argue that tiny houses are not a real solution to housing shortages in cities, where land is the main cost. Some suggest that well-designed small apartments in dense buildings may be more practical.

Nevertheless, the movement has encouraged a wider debate about how much space people really need. Its ideas, efficient design and less consumption, influence the design of homes of all sizes.
? s | How big are tiny houses often? | less than thirty square metres / under thirty square metres / thirty square metres | The first paragraph says so. | homes of often less than thirty square metres
? c | Why do tiny house owners avoid large mortgages? | *Tiny houses cost much less | Banks refuse loans | They rent instead | The second paragraph explains. | Tiny houses cost much less to build or buy than conventional homes, allowing owners to avoid large mortgages.
? c | How do designers save space? | *Beds in lofts and folding tables | Bigger windows | Fewer doors | The third paragraph explains. | Beds may be placed in lofts, tables may fold away
? t | Planning rules everywhere allow people to live permanently in tiny houses. | F | In many places they do not. | In many places, planning rules do not allow people to live permanently in tiny houses
? c | What do critics argue? | *Tiny houses are not a real solution to city housing shortages | Tiny houses are too big | Tiny houses use too much energy | The fifth paragraph explains. | tiny houses are not a real solution to housing shortages in cities

## The slow travel movement | TR
Many holidays follow a familiar pattern: several cities in a few days, a long list of famous sights and many photos. The slow travel movement suggests a different approach: staying longer in fewer places and experiencing them more deeply.

Slow travellers might spend weeks in a single town or region, renting an apartment rather than staying in hotels. They shop at local markets, learn a few words of the language and take time to get to know residents. Instead of rushing between attractions, they explore neighbourhoods on foot and visit places that are not in guidebooks.

The movement often favours slower forms of transport, such as trains, buses, bicycles or walking. Supporters say the journey itself becomes part of the experience, offering views and encounters that flights cannot provide. Avoiding short flights also reduces travellers' carbon emissions.

Slow travel can benefit local communities too. Travellers who stay longer tend to spend money in local shops, cafés and guesthouses rather than in large international chains. Spreading visitors throughout the year and across less famous areas can also reduce the pressure of overtourism in popular destinations.

Of course, slow travel requires time, which many people do not have. Most workers have limited holidays, and long trips can be expensive. However, supporters argue that the principles can apply to shorter trips: visiting fewer places, avoiding over-planning and leaving space for unexpected experiences.

As one slow traveller put it, "The goal is not to see everything, but to really see something."
? c | What does slow travel suggest? | *Staying longer in fewer places | Visiting as many cities as possible | Travelling only by plane | The first paragraph explains. | staying longer in fewer places and experiencing them more deeply.
? c | Which transport does the movement often favour? | *Trains, buses, bicycles or walking | Planes | Cruise ships | The third paragraph says so. | such as trains, buses, bicycles or walking.
? t | Travellers who stay longer tend to spend money in local businesses. | T | The fourth paragraph says so. | Travellers who stay longer tend to spend money in local shops, cafés and guesthouses
? s | What do many people not have for slow travel? | time | The fifth paragraph says so. | slow travel requires time, which many people do not have.
? c | According to the last quote, what is the goal? | *To really see something | To see everything | To take many photos | The last paragraph quotes a traveller. | The goal is not to see everything, but to really see something.

## Why teenagers sleep late | HE
Parents often complain that teenagers stay up late at night and find it almost impossible to get up in the morning. It is easy to blame phones or laziness, but scientists say biology plays an important role.

During adolescence, the body's internal clock shifts. The release of melatonin, the hormone that makes us feel sleepy, begins later in the evening than it does in children or adults. As a result, many teenagers genuinely find it difficult to fall asleep before eleven o'clock, even if they go to bed earlier.

At the same time, teenagers need a lot of sleep, around eight to ten hours a night. When school starts early, many get far less. Sleep deprivation has been linked to poorer concentration, lower grades, mood problems and an increased risk of accidents.

Technology can make the situation worse. The light from screens delays the release of melatonin further, and social media and games keep the brain active.

Some schools have responded by starting the school day later. In several studies, a later start of even thirty to sixty minutes led to longer sleep, better attendance and improved mood. However, changing school times can be complicated, because it affects transport, parents' working schedules and after-school activities.

Experts also suggest steps families can take: keeping regular sleep times, even at weekends; limiting screens in the hour before bed; and keeping phones out of the bedroom at night. Understanding that teenagers' sleep patterns are partly biological may also help reduce conflict at home.
? c | What do scientists say plays an important role in teenagers' late sleeping? | *Biology | Laziness | Diet | The first paragraph explains. | scientists say biology plays an important role.
? c | What happens to melatonin release during adolescence? | *It begins later in the evening | It stops completely | It begins earlier | The second paragraph explains. | begins later in the evening than it does in children or adults.
? s | How much sleep do teenagers need? | around eight to ten hours / eight to ten hours / 8 to 10 hours | The third paragraph says so. | around eight to ten hours a night.
? t | A later school start led to worse attendance in studies. | F | It led to better attendance. | led to longer sleep, better attendance and improved mood.
? c | What do experts suggest families do? | *Keep phones out of the bedroom at night | Let teenagers sleep until noon on school days | Remove all screens from the house | The last paragraph says so. | keeping phones out of the bedroom at night.
"""

PASSAGES["C1"] = """
## The paradox of choice | SH
Modern consumers enjoy an almost unlimited range of options. A single supermarket may stock dozens of varieties of yoghurt, and online shops offer thousands of nearly identical products. It seems obvious that more choice should make people happier, since everyone can find exactly what suits them. Yet a growing body of research suggests that the relationship between choice and satisfaction is far more complicated.

In a frequently cited experiment, shoppers were offered samples of jam at a supermarket stand. When twenty-four varieties were displayed, more people stopped to taste them, but far fewer actually made a purchase than when only six varieties were available. The researchers concluded that an abundance of options can lead to "choice overload", in which people feel overwhelmed and postpone or avoid decisions altogether.

Even when people do choose, a wide range of alternatives can reduce their satisfaction. With so many possibilities, it is easy to imagine that a different option might have been better, and this sense of missed opportunity can turn a good decision into a source of regret. Psychologists distinguish between "maximisers", who search exhaustively for the best possible option, and "satisficers", who settle for one that is good enough. Studies indicate that maximisers often achieve objectively better outcomes but feel less content with them.

It would be wrong, however, to conclude that choice is undesirable. Subsequent studies have not always reproduced the jam experiment's dramatic results, and the effect seems to depend on how options are presented and how much people already know. Well-organised categories, clear comparisons and trusted recommendations can make large selections manageable.

The practical lesson may be that freedom of choice is valuable, but only when combined with the means to navigate it.
? c | What happened when twenty-four varieties of jam were displayed? | *More people tasted but fewer bought | More people bought jam | Nobody stopped at the stand | The second paragraph describes the result. | more people stopped to taste them, but far fewer actually made a purchase
? s | What term describes feeling overwhelmed by too many options? | choice overload | The second paragraph names it. | an abundance of options can lead to "choice overload"
? c | How do maximisers differ from satisficers? | *They search exhaustively for the best option | They choose quickly | They avoid all decisions | The third paragraph explains. | who search exhaustively for the best possible option
? t | Maximisers usually feel more content with their decisions. | F | They often feel less content. | Studies indicate that maximisers often achieve objectively better outcomes but feel less content with them.
? c | What does the final paragraph suggest? | *Choice is valuable when people can navigate it | Choice should be limited by law | People should never compare options | The writer concludes. | freedom of choice is valuable, but only when combined with the means to navigate it.

## Money for nothing? | MS
The idea of a universal basic income, a regular payment made by the state to every citizen regardless of whether they work, has moved from the margins of political debate towards the mainstream. Its supporters come from surprisingly different backgrounds, and so do its critics.

Advocates argue that a basic income would provide security in an economy increasingly shaped by automation and unstable employment. Unlike traditional welfare systems, which often require complex applications and can penalise people for taking low-paid work, a universal payment would be simple and unconditional. Proponents claim this would reduce bureaucracy, eliminate the stigma attached to benefits and give people the freedom to retrain, care for relatives or start businesses.

Opponents raise two main objections. The first concerns cost: paying a meaningful amount to every adult would require substantial tax increases or cuts to other public services. The second is behavioural. Critics fear that guaranteed income would discourage work, weakening the economy and the sense of contribution that employment provides.

Evidence from pilot schemes offers a mixed picture. In several trials, recipients did not significantly reduce their working hours; some used the security to look for better jobs or pursue training. Many reported lower stress and improved health. However, most trials have been small, temporary and limited to particular groups, which makes it difficult to predict how a permanent, nationwide scheme would affect an entire economy.

As a result, the debate often reflects deeper differences in values: about what citizens owe one another, and about whether security or incentive is the more effective foundation for a productive society.
? c | What distinguishes a universal basic income from traditional welfare? | *It is simple and unconditional | It is paid only to the unemployed | It requires complex applications | The second paragraph explains. | a universal payment would be simple and unconditional.
? c | What is the behavioural objection to basic income? | *It might discourage people from working | It would be too complicated | It would increase bureaucracy | The third paragraph explains. | Critics fear that guaranteed income would discourage work
? t | In several trials, recipients significantly reduced their working hours. | F | They did not significantly reduce them. | recipients did not significantly reduce their working hours
? s | Why is it hard to predict the effects of a permanent scheme? | most trials have been small, temporary and limited / trials were small and temporary | The fourth paragraph explains. | most trials have been small, temporary and limited to particular groups
? c | According to the final paragraph, what does the debate often reflect? | *Deeper differences in values | Disagreements about statistics only | Technical problems | The last paragraph says so. | the debate often reflects deeper differences in values

## Who should the car protect? | TE
Self-driving cars promise to transform transport. Because human error contributes to the vast majority of road accidents, removing the driver could, in theory, save many lives. Yet the prospect of machines making life-or-death decisions has raised difficult ethical questions.

The most widely discussed is a modern version of a classic philosophical puzzle. Imagine a self-driving car whose brakes fail. It can continue straight and hit a group of pedestrians, or swerve and hit a wall, killing its passenger. How should the car be programmed to respond? A large international online survey asked millions of people versions of this question. Most respondents preferred that cars minimise the total number of deaths. However, many also said they would rather not buy a car programmed to sacrifice its own passengers.

Some engineers argue that such dramatic dilemmas are largely theoretical. In practice, they say, the priority is to design cars that avoid dangerous situations altogether by driving cautiously and reacting faster than humans can. Critics respond that even routine decisions, such as how much space to leave cyclists or how aggressively to merge into traffic, involve value judgements about acceptable risk.

There are also questions of responsibility. When a self-driving car causes an accident, who is to blame: the manufacturer, the software developer, the owner or the government that approved the technology? Existing laws were written for human drivers, and legal systems are still adapting.

What is clear is that these decisions cannot be left to engineers alone. Transparent public debate and clear regulation will be needed to ensure that the values programmed into machines reflect those of the societies that use them.
? c | Why could self-driving cars save lives in theory? | *Human error contributes to most accidents | They are slower | They have stronger brakes | The first paragraph explains. | human error contributes to the vast majority of road accidents
? c | What contradiction did the survey reveal? | *People preferred minimising deaths but wouldn't buy cars that sacrifice passengers | People wanted cars to protect only pedestrians | People refused to answer | The second paragraph explains. | many also said they would rather not buy a car programmed to sacrifice its own passengers.
? t | Some engineers consider the dramatic dilemmas largely theoretical. | T | The third paragraph says so. | Some engineers argue that such dramatic dilemmas are largely theoretical.
? s | What were existing laws written for? | human drivers | The fourth paragraph says so. | Existing laws were written for human drivers
? c | What does the writer conclude? | *The decisions need public debate and regulation, not only engineers | Engineers should decide alone | Self-driving cars should be banned | The last paragraph explains. | these decisions cannot be left to engineers alone.

## The myth of multitasking | WK
Many people take pride in their ability to multitask: answering emails during meetings, checking messages while studying or listening to podcasts while writing reports. In fast-paced workplaces, multitasking is often seen as a sign of efficiency. Neuroscience, however, suggests that this confidence is largely misplaced.

Strictly speaking, the human brain cannot focus on two demanding tasks at once. What we call multitasking is usually rapid task-switching: moving our attention back and forth between activities. Each switch carries a cost. The brain must disengage from one set of rules and goals and load another, a process that takes time and increases the likelihood of errors. Researchers estimate that frequent switching can significantly reduce productivity, even if each individual switch seems to take only a fraction of a second.

Interestingly, studies have found that people who multitask most often are not better at it. In some experiments, heavy media multitaskers performed worse on tests requiring them to filter out irrelevant information. They appeared more easily distracted, perhaps because constant switching had become a habit.

There are exceptions. People can combine an automatic activity, such as walking, with a cognitive one, such as conversation, because the automatic task demands little attention. Problems arise when both tasks require conscious thought.

The implications for work and study are significant. Experts recommend structuring the day into blocks of focused time, disabling non-essential notifications and grouping similar tasks, such as replying to emails, into designated periods. Some organisations have experimented with "meeting-free" days to allow uninterrupted work. Although these strategies require discipline, they often produce better results in less time than the illusion of doing everything at once.
? c | What is multitasking usually, according to neuroscience? | *Rapid task-switching | True parallel focus | A rare talent | The second paragraph explains. | What we call multitasking is usually rapid task-switching
? c | What did experiments find about heavy media multitaskers? | *They were more easily distracted | They were better at filtering information | They worked faster | The third paragraph explains. | They appeared more easily distracted
? t | People can combine walking with conversation without much difficulty. | T | The automatic task demands little attention. | because the automatic task demands little attention.
? s | What have some organisations experimented with? | meeting-free days / "meeting-free" days | The last paragraph says so. | Some organisations have experimented with "meeting-free" days
? c | What is the writer's overall view of multitasking? | *It is largely an illusion that reduces productivity | It is the key to efficiency | It works for most demanding tasks | The writer concludes. | they often produce better results in less time than the illusion of doing everything at once.

## Growing food in the city | EN
More than half of the world's population now lives in cities, and that proportion is expected to grow. Feeding these urban populations depends on long supply chains that transport food across countries and continents. In recent years, interest has grown in producing more food within cities themselves.

Urban agriculture takes many forms: community gardens on vacant land, vegetables grown on rooftops, fish farms combined with plant cultivation, and high-tech indoor farms in which crops grow under artificial light in stacked layers. Supporters claim that these initiatives reduce transport emissions, provide fresh food in neighbourhoods where healthy options are scarce, and reconnect city dwellers with the origins of what they eat.

The social benefits are often as significant as the agricultural ones. Community gardens can bring together neighbours from different backgrounds, offer educational opportunities for children and provide therapeutic activity for people experiencing stress or isolation.

Nevertheless, the potential of urban agriculture should not be overstated. Land in cities is expensive and limited, and most staple crops, such as rice and wheat, require far more space than urban areas can provide. Indoor vertical farms can produce leafy greens efficiently, but their reliance on artificial lighting makes them energy-intensive, and their environmental benefits depend heavily on the source of that energy. Soil in former industrial areas may also be contaminated, requiring careful testing.

Most researchers therefore see urban agriculture as a complement to rural farming rather than a replacement for it. Its greatest value may lie less in the quantity of food produced than in strengthening communities, improving access to fresh produce and making cities more resilient to disruptions in global supply chains.
? c | What does urban food production depend on today? | *Long supply chains | Local farms only | Imported water | The first paragraph explains. | Feeding these urban populations depends on long supply chains
? c | Which is a social benefit of community gardens? | *Bringing neighbours from different backgrounds together | Producing all staple crops | Lowering land prices | The third paragraph explains. | Community gardens can bring together neighbours from different backgrounds
? t | Vertical farms use little energy. | F | They are energy-intensive. | their reliance on artificial lighting makes them energy-intensive
? s | What may soil in former industrial areas be? | contaminated | The fourth paragraph says so. | Soil in former industrial areas may also be contaminated
? c | How do most researchers see urban agriculture? | *As a complement to rural farming | As a replacement for rural farming | As unnecessary | The last paragraph explains. | as a complement to rural farming rather than a replacement for it.

## How habits form | HE
Much of what we do each day is not the result of conscious decisions but of habit. Researchers estimate that a large proportion of daily behaviour is performed almost automatically, from the route we take to work to the moment we reach for our phones. Understanding how habits form can therefore help people change behaviour more effectively than relying on willpower alone.

Psychologists often describe habits as loops consisting of three elements: a cue, a routine and a reward. The cue is a trigger, such as a time of day, a location or an emotion. The routine is the behaviour itself, and the reward is the benefit the brain associates with it. Over time, the connection between cue and routine strengthens until the behaviour occurs with little thought.

A popular belief holds that it takes twenty-one days to form a habit. Research does not support this precise figure. In one study, participants took anywhere from eighteen to more than two hundred days to make a new behaviour automatic, depending on the person and the complexity of the habit. Missing a single day, however, did not significantly harm the process.

Several strategies appear to help. Attaching a new habit to an existing routine, such as doing stretches after brushing your teeth, provides a reliable cue. Making the desired behaviour easier, for example by placing a book on your pillow, reduces the effort required. Conversely, adding friction to unwanted habits, such as keeping snacks out of sight, can weaken them.

Perhaps most importantly, research suggests that people who seem to have strong self-control often succeed not by resisting temptation constantly, but by designing environments in which temptation rarely arises.
? c | Why can understanding habits help people change behaviour? | *Much daily behaviour is automatic | Willpower always works | Habits are rare | The first paragraph explains. | a large proportion of daily behaviour is performed almost automatically
? s | What are the three elements of the habit loop? | a cue, a routine and a reward / cue, routine and reward | The second paragraph names them. | a cue, a routine and a reward.
? t | Research confirms that habits always take twenty-one days to form. | F | It does not support the figure. | Research does not support this precise figure.
? c | What is an example of adding friction to an unwanted habit? | *Keeping snacks out of sight | Placing a book on your pillow | Stretching after brushing teeth | The fourth paragraph gives the example. | keeping snacks out of sight
? c | How do people with strong self-control often succeed? | *By designing environments where temptation rarely arises | By resisting temptation constantly | By setting strict punishments | The last paragraph explains. | by designing environments in which temptation rarely arises.

## Does language shape thought? | CO
For centuries, philosophers and linguists have debated whether the language we speak influences the way we think. In its strongest form, the idea suggests that language determines thought, so that speakers of different languages perceive the world in fundamentally different ways. Few researchers accept this extreme version today, but a growing body of evidence supports a weaker claim: that language can subtly shape attention, memory and perception.

Consider the way languages describe space. Some languages rely on relative terms such as "left" and "right", while others use absolute directions like north and south, even for small objects on a table. Studies of speakers of such languages have found that they maintain a remarkable sense of orientation, apparently because their language requires constant awareness of direction.

Colour offers another example. Languages divide the colour spectrum differently. Speakers of languages that have separate basic words for light and dark blue have been shown to distinguish between these shades slightly faster than speakers of languages that use a single word.

Grammar may also play a role. Languages differ in whether they require speakers to mark the gender of nouns, the timing of events or whether information was directly witnessed. Some researchers argue that such requirements encourage speakers to notice particular aspects of experience.

Critics caution that many of these effects are small and can disappear when people are given time to think or are taught new categories. Bilingual speakers often shift their perceptions depending on the language they are using, which suggests flexibility rather than fixed limits.

The emerging consensus is that language does not imprison thought, but it does provide habitual tools that make certain distinctions easier to notice.
? c | Which version of the idea do few researchers accept today? | *That language determines thought | That language influences attention | That languages differ | The first paragraph explains. | Few researchers accept this extreme version today
? c | What do speakers of languages using absolute directions maintain? | *A remarkable sense of orientation | Better colour vision | Faster reading | The second paragraph explains. | they maintain a remarkable sense of orientation
? t | Some speakers distinguish shades of blue slightly faster if their language has separate words for them. | T | The third paragraph says so. | have been shown to distinguish between these shades slightly faster
? s | What do bilingual speakers often shift depending on the language? | their perceptions / perceptions | The fifth paragraph says so. | Bilingual speakers often shift their perceptions depending on the language they are using
? c | What is the emerging consensus? | *Language provides tools that make certain distinctions easier to notice | Language imprisons thought | Language has no effect on thinking | The last paragraph explains. | it does provide habitual tools that make certain distinctions easier to notice.

## The doctor will see you online | HE
Not long ago, consulting a doctor almost always meant travelling to a clinic and waiting in a crowded room. Today, video consultations, remote monitoring devices and health apps are changing how healthcare is delivered. Telemedicine, once a niche service, has become part of mainstream medical practice in many countries.

The advantages are considerable. For patients in remote areas, telemedicine can eliminate long and expensive journeys. People with mobility difficulties or chronic conditions can receive regular follow-up care from home, and wearable devices can transmit data such as heart rate or blood sugar levels directly to medical teams, allowing problems to be detected earlier. For health systems under pressure, virtual consultations can reduce waiting times and free up clinic space.

However, telemedicine has clear limitations. Many diagnoses depend on physical examination, which cannot be performed through a screen. Doctors may miss subtle signs that would be obvious in person, and some patients find it harder to discuss sensitive issues remotely.

There are also concerns about inequality. Telemedicine requires a reliable internet connection, a suitable device and a degree of digital literacy. Older patients and those on low incomes, who often have the greatest health needs, may be the least able to benefit. Without careful planning, the shift to digital care could widen existing health gaps.

Privacy is another issue. Health data is highly sensitive, and the growing number of apps and devices increases the risk of data breaches.

Most experts envisage a hybrid model, in which digital tools handle routine follow-ups and monitoring while in-person care remains available for examinations and complex cases. The challenge will be to ensure that convenience does not come at the expense of quality or equity.
? c | Who benefits especially from telemedicine? | *Patients in remote areas | Doctors who prefer travelling | Only young people | The second paragraph explains. | For patients in remote areas, telemedicine can eliminate long and expensive journeys.
? c | What is a key limitation of telemedicine? | *Many diagnoses need a physical examination | It is always more expensive | It cannot use video | The third paragraph explains. | Many diagnoses depend on physical examination, which cannot be performed through a screen.
? t | Older and low-income patients are always the first to benefit from telemedicine. | F | They may be the least able to benefit. | may be the least able to benefit.
? s | What does the growing number of apps and devices increase the risk of? | data breaches | The fifth paragraph says so. | increases the risk of data breaches.
? c | What model do most experts envisage? | *A hybrid of digital and in-person care | Fully digital healthcare | No digital tools at all | The last paragraph explains. | Most experts envisage a hybrid model

## The price of renewal | PT
When artists, students and young professionals move into a run-down urban neighbourhood, attracted by low rents, the area often begins to change. New cafés and galleries open, old buildings are renovated and property values rise. This process, known as gentrification, is one of the most contested issues in urban policy.

Supporters emphasise the benefits. Investment can improve housing quality, reduce crime and bring new businesses and jobs. Local governments gain higher tax revenues, which can fund better services. Long-term residents who own their homes may see the value of their property increase significantly.

Critics, however, focus on who benefits and who pays. As rents rise, many long-standing residents, particularly tenants on low incomes, are forced to move elsewhere, often far from their jobs, schools and social networks. Small family businesses may be replaced by expensive shops that cater to newcomers. Even residents who remain can feel like strangers in their own neighbourhood as its character and community life change.

Researchers disagree about the scale of displacement. Some studies have found that low-income residents in gentrifying areas are not necessarily more likely to move than those elsewhere, while others document significant losses of affordable housing. The effects appear to vary greatly depending on local housing markets and policies.

Cities have experimented with various responses, including rent controls, requirements for affordable units in new developments, and community land trusts, which keep land under collective ownership to preserve affordability.

Ultimately, the debate is less about whether neighbourhoods should improve than about ensuring that improvement benefits existing residents rather than replacing them.
? c | What often begins the process of gentrification? | *Artists and young professionals moving in for low rents | Factories opening | Governments building motorways | The first paragraph explains. | When artists, students and young professionals move into a run-down urban neighbourhood, attracted by low rents
? c | Which group is most affected by rising rents, according to critics? | *Tenants on low incomes | Home owners | Local governments | The third paragraph explains. | particularly tenants on low incomes
? t | All researchers agree that displacement is very large. | F | Researchers disagree about the scale. | Researchers disagree about the scale of displacement.
? s | What do community land trusts keep under collective ownership? | land | The fifth paragraph says so. | which keep land under collective ownership to preserve affordability.
? c | What is the debate ultimately about, according to the writer? | *Ensuring improvement benefits existing residents | Whether neighbourhoods should improve at all | Stopping all investment | The last paragraph explains. | ensuring that improvement benefits existing residents rather than replacing them.

## What are the humanities for? | ED
In many countries, the number of students choosing subjects such as history, philosophy and literature has declined, while enrolment in science, technology and business has grown. Governments and universities, under pressure to demonstrate economic returns, have sometimes reduced funding for the humanities, arguing that they offer weaker career prospects.

Defenders of the humanities challenge this view on several grounds. First, they argue that the skills these subjects develop, such as critical thinking, clear writing, interpretation of complex texts and the ability to construct arguments, are highly valued by employers in many sectors. Graduates in the humanities, they point out, often build successful careers in law, media, public service and business, even if their starting salaries are lower.

Second, supporters contend that the value of education cannot be measured only in economic terms. The humanities help people understand human experience, examine moral questions and engage with cultures different from their own. In democratic societies, the ability to evaluate evidence, recognise manipulation and debate respectfully is arguably as important as technical expertise.

Third, many of the most pressing challenges of the modern world, from the ethics of artificial intelligence to climate policy, involve questions that technology alone cannot answer. Decisions about how new tools should be used require understanding of history, values and human behaviour.

Critics respond that students, often burdened with debt, are entitled to consider employability, and that universities have a duty to provide clear information about outcomes.

Increasingly, some institutions are seeking to bridge the divide, encouraging scientists to study ethics and humanities students to develop data skills, in the belief that the most valuable graduates will combine both perspectives.
? c | Why have some governments reduced funding for the humanities? | *They are under pressure to show economic returns | Students prefer them | They are too popular | The first paragraph explains. | under pressure to demonstrate economic returns
? c | Which skill do defenders say the humanities develop? | *Critical thinking and clear writing | Laboratory techniques | Programming | The second paragraph lists them. | such as critical thinking, clear writing, interpretation of complex texts and the ability to construct arguments
? t | Defenders argue that education should be measured only economically. | F | They argue it cannot be measured only in economic terms. | the value of education cannot be measured only in economic terms.
? s | Name one modern challenge the text says technology alone cannot answer. | the ethics of artificial intelligence / climate policy | The fourth paragraph gives examples. | from the ethics of artificial intelligence to climate policy
? c | How are some institutions bridging the divide? | *Encouraging scientists to study ethics and humanities students to learn data skills | Closing humanities departments | Banning business degrees | The last paragraph explains. | encouraging scientists to study ethics and humanities students to develop data skills

## Paying to pollute? | EN
Carbon offsetting allows individuals and companies to compensate for their greenhouse gas emissions by funding projects that reduce or remove carbon dioxide elsewhere. A traveller might pay a small fee when booking a flight, for example, to support tree-planting or renewable energy projects in another country. In principle, the emissions from the flight are balanced by the reductions achieved through the project.

The appeal is obvious. Offsetting offers a way to take responsibility for emissions that are difficult to avoid, and it channels money into projects that may bring additional benefits, such as protecting forests or providing clean cooking stoves to households that would otherwise burn wood.

However, offsetting has attracted serious criticism. One problem is additionality: would the project have happened anyway, even without the payment? If a forest was never at risk of being cut down, paying to protect it does not reduce emissions. Another issue is permanence. Trees planted today may be destroyed by fire, disease or illegal logging decades later, releasing the stored carbon back into the atmosphere. Investigations have also found that some projects significantly overstated the emissions they prevented.

Critics further argue that offsetting can encourage complacency, allowing companies and consumers to continue polluting while claiming to be "carbon neutral". The priority, they insist, should be to reduce emissions directly.

In response, standards for verifying offset projects have been tightened, and some organisations now favour "carbon removal" methods with more measurable results. Many experts conclude that offsets can play a limited role, but only as a final step after every feasible effort has been made to cut emissions at their source.
? c | What does carbon offsetting allow people to do? | *Compensate for emissions by funding reduction projects elsewhere | Stop flying | Pay lower taxes | The first paragraph explains. | compensate for their greenhouse gas emissions by funding projects that reduce or remove carbon dioxide elsewhere.
? s | What is the term for whether a project would have happened anyway? | additionality | The third paragraph names it. | One problem is additionality
? c | Why is permanence a problem with planted trees? | *They may later be destroyed, releasing carbon | They grow too slowly | They need too much water | The third paragraph explains. | Trees planted today may be destroyed by fire, disease or illegal logging decades later
? t | Investigations found some projects overstated the emissions they prevented. | T | The third paragraph says so. | some projects significantly overstated the emissions they prevented.
? c | How do many experts see offsets? | *As a final step after cutting emissions at their source | As the main solution | As useless in all cases | The last paragraph explains. | only as a final step after every feasible effort has been made to cut emissions at their source.

## Paying with attention | TE
Many of the most popular digital services, from social media platforms to search engines and video sites, are free to use. Yet they generate enormous revenues. The explanation lies in what some economists call the attention economy: users pay not with money but with their time and data, which companies sell to advertisers.

In this model, the more time users spend on a platform, the more advertisements they see and the more data they generate. Platforms therefore have strong incentives to maximise engagement. Features such as infinite scrolling, autoplay videos and personalised notifications are designed to keep users returning and remaining online for as long as possible.

Some former technology designers have openly acknowledged that these features draw on psychological research into habit and reward. Unpredictable rewards, such as not knowing whether new messages or likes will appear, are particularly powerful at encouraging repeated checking.

Critics argue that the attention economy has significant social costs. They link excessive use to reduced concentration, poorer sleep and anxiety, particularly among young people. Because algorithms tend to promote content that provokes strong emotional reactions, they may also amplify outrage and misinformation.

Defenders point out that users derive genuine value from these services, which provide communication, information and entertainment at no direct cost. They also note that the research on harms is still developing and that effects vary widely between individuals.

Proposed solutions range from individual strategies, such as turning off notifications, to regulatory measures, including restrictions on designs aimed at children and greater transparency about how algorithms rank content. Some designers advocate "humane technology" that respects users' time rather than exploiting it.
? c | How do users pay for free digital services in the attention economy? | *With their time and data | With subscriptions | With donations | The first paragraph explains. | users pay not with money but with their time and data
? c | Why do platforms try to maximise engagement? | *More time means more advertisements and data | Users demand it by law | It reduces costs | The second paragraph explains. | the more time users spend on a platform, the more advertisements they see and the more data they generate.
? t | Unpredictable rewards are particularly effective at encouraging repeated checking. | T | The third paragraph says so. | are particularly powerful at encouraging repeated checking.
? s | What kind of content do algorithms tend to promote? | content that provokes strong emotional reactions / emotional content | The fourth paragraph says so. | algorithms tend to promote content that provokes strong emotional reactions
? c | What do some designers advocate? | *Technology that respects users' time | More advertisements | Banning social media | The last paragraph explains. | Some designers advocate "humane technology" that respects users' time rather than exploiting it.

## When a city is loved too much | TR
Venice, Barcelona and Kyoto share an unusual problem: they are too popular. Each year, millions of visitors crowd their historic streets, and in peak seasons residents can feel outnumbered in their own neighbourhoods. The phenomenon has become known as overtourism.

Tourism brings undeniable economic benefits, supporting jobs in hotels, restaurants, transport and retail. Yet when visitor numbers exceed what a place can sustainably absorb, the costs become increasingly visible. Narrow streets become congested, public transport overcrowded and fragile monuments damaged. Perhaps most significantly, the conversion of residential apartments into short-term rentals reduces the housing available to locals and pushes up rents, gradually hollowing out historic centres.

Several factors have contributed to the problem. Cheaper flights, the growth of cruise tourism and online rental platforms have made travel more accessible than ever. Social media has concentrated visitors at a limited number of photogenic locations, sometimes overwhelming previously quiet places within months.

Cities have responded with a variety of measures. Some have introduced tourist taxes or entry fees for day visitors at peak times. Others have restricted new hotels or short-term rentals in central districts, limited the number of cruise ships and redirected tour groups. Several destinations have launched campaigns encouraging visitors to explore lesser-known areas or travel outside peak seasons.

These policies are not without controversy. Businesses fear lost revenue, and critics argue that fees may turn historic cities into exclusive destinations for the wealthy. Nevertheless, there is growing consensus that unmanaged tourism risks destroying the very qualities that attract visitors in the first place. The challenge is to ensure that cities remain places to live, not merely places to visit.
? c | What is overtourism? | *Too many visitors for a place to absorb sustainably | A lack of tourists | Tourism in the countryside | The first and second paragraphs explain. | when visitor numbers exceed what a place can sustainably absorb
? c | How do short-term rentals affect historic centres? | *They reduce housing for locals and push up rents | They lower rents | They create more homes | The second paragraph explains. | reduces the housing available to locals and pushes up rents
? s | What has concentrated visitors at a limited number of locations? | social media | The third paragraph says so. | Social media has concentrated visitors at a limited number of photogenic locations
? t | All businesses support the new policies. | F | Businesses fear lost revenue. | Businesses fear lost revenue
? c | According to the writer, what is the challenge? | *Ensuring cities remain places to live | Attracting more cruise ships | Building more hotels | The last paragraph explains. | The challenge is to ensure that cities remain places to live, not merely places to visit.

## A gentle push | MS
Traditional economic theory assumes that people make rational decisions, carefully weighing costs and benefits to maximise their own interests. Behavioural economics, which combines insights from psychology and economics, challenges this assumption. It shows that human decisions are influenced by habits, emotions, social norms and the way choices are presented.

One of the field's most influential ideas is the "nudge": a change in the way options are presented that predictably alters behaviour without restricting choice or significantly changing financial incentives. A classic example concerns pension savings. When employees must actively sign up for a workplace pension scheme, many never do, even if they intend to. When they are automatically enrolled but free to opt out, participation rises dramatically. The options are identical; only the default has changed.

Governments have used nudges in areas ranging from tax collection to public health. Letters telling taxpayers that most of their neighbours pay on time have increased compliance. Placing healthy foods at eye level in canteens has encouraged better diets.

Critics, however, raise concerns. Some argue that nudges can be manipulative, influencing people without their awareness. Others worry that governments may use nudges to avoid more effective but politically difficult policies, such as regulation or taxation. A nudge to recycle, for instance, may achieve less than reforming how packaging is produced.

Supporters respond that every presentation of choices influences behaviour in some way; there is no neutral option. The question is whether that influence serves people's own interests. Most agree that nudges should be transparent, easy to avoid and subject to public scrutiny, so that citizens retain control over their choices.
? c | What does behavioural economics challenge? | *The assumption that people decide rationally | The existence of markets | The value of money | The first paragraph explains. | challenges this assumption.
? c | What happened when employees were automatically enrolled in pensions? | *Participation rose dramatically | Participation fell | Nobody noticed | The second paragraph explains. | When they are automatically enrolled but free to opt out, participation rises dramatically.
? t | Letters about neighbours paying on time increased tax compliance. | T | The third paragraph says so. | Letters telling taxpayers that most of their neighbours pay on time have increased compliance.
? s | What do some critics say nudges can be? | manipulative | The fourth paragraph says so. | Some argue that nudges can be manipulative
? c | What do most people agree nudges should be? | *Transparent, easy to avoid and open to scrutiny | Secret and permanent | Compulsory | The last paragraph explains. | nudges should be transparent, easy to avoid and subject to public scrutiny

## Trusting strangers online | TE
Every day, millions of people do something that would have seemed reckless a generation ago: they get into cars driven by strangers, sleep in strangers' homes and buy expensive items from people they have never met. Digital platforms have made this possible by creating systems designed to build trust between people who have no prior relationship.

Central to these systems are ratings and reviews. After each transaction, both parties evaluate each other, creating a public record of reputation. A host with hundreds of positive reviews or a driver with a high rating appears trustworthy, and users rely heavily on these signals when making decisions. Platforms also verify identities, process payments securely and offer guarantees if something goes wrong.

Research suggests these mechanisms work remarkably well. Most transactions occur without problems, and reputation systems create strong incentives for good behaviour, since a few negative reviews can seriously damage a person's income.

Yet reputation systems have weaknesses. Ratings tend to be inflated, with the vast majority of reviews clustered at the highest levels, which makes it difficult to distinguish between good and excellent service. Fear of retaliation may discourage honest negative feedback. Fake reviews remain a persistent problem.

There are also concerns about fairness. Studies have found evidence that users with certain names or profile photos may receive fewer bookings or lower ratings, reflecting biases that reputation systems can reproduce or even amplify. For workers whose livelihoods depend on ratings, a few unfair reviews can have serious consequences.

As platforms play an ever larger role in economic life, the design of trust systems has become an important question, not only for companies but also for regulators concerned with transparency and discrimination.
? c | What have digital platforms created? | *Systems to build trust between strangers | Free transport | Private clubs | The first paragraph explains. | creating systems designed to build trust between people who have no prior relationship.
? c | Why do reputation systems encourage good behaviour? | *Negative reviews can damage a person's income | Users are paid for reviews | Reviews are anonymous | The third paragraph explains. | since a few negative reviews can seriously damage a person's income.
? t | Ratings are usually spread evenly from low to high. | F | Most cluster at the highest levels. | the vast majority of reviews clustered at the highest levels
? s | What may discourage honest negative feedback? | fear of retaliation | The fourth paragraph says so. | Fear of retaliation may discourage honest negative feedback.
? c | What fairness concern do studies raise? | *Biases linked to names or photos may affect bookings and ratings | All users are treated identically | Reviews are too long | The fifth paragraph explains. | users with certain names or profile photos may receive fewer bookings or lower ratings

## The education gap | ED
Education is often described as the great equaliser, the means by which children from any background can improve their prospects. In practice, however, educational outcomes remain strongly linked to family income in many countries. Children from wealthier households are more likely to complete secondary school, attend university and obtain well-paid jobs.

The gap often appears early. By the time children start school, those from disadvantaged backgrounds may already lag behind in vocabulary and early literacy, partly because of differences in access to books, educational activities and high-quality early childcare. Without targeted support, these early disadvantages can widen over time.

Resources outside school also play a role. Wealthier families can afford private tutoring, extracurricular activities and quiet study spaces, all of which can improve performance. During long school holidays, children from low-income families may lose more of what they have learned, a phenomenon researchers call the "summer slide".

Schools themselves can reinforce inequality. In many places, schools in wealthy areas have more funding, experienced teachers and better facilities, while schools serving poorer communities struggle to recruit and retain staff.

Nevertheless, research identifies interventions that make a difference. High-quality early childhood education has shown long-term benefits, particularly for disadvantaged children. Small-group tutoring, well-trained teachers and programmes that involve parents can also narrow gaps. Some countries have reduced inequality by directing additional funding to schools with greater needs.

Education alone cannot eliminate wider social and economic inequalities. But evidence suggests that well-designed policies can ensure a child's prospects depend less on the circumstances of their birth.
? c | What remains strongly linked to educational outcomes in many countries? | *Family income | Height | Birth month | The first paragraph explains. | educational outcomes remain strongly linked to family income in many countries.
? c | When does the gap often first appear? | *Before children start school | At university | After graduation | The second paragraph explains. | By the time children start school, those from disadvantaged backgrounds may already lag behind
? s | What do researchers call the learning loss during long holidays? | the summer slide / summer slide | The third paragraph names it. | a phenomenon researchers call the "summer slide".
? t | Schools in poorer communities usually find it easier to recruit teachers. | F | They struggle to recruit and retain staff. | schools serving poorer communities struggle to recruit and retain staff.
? c | Which intervention has shown long-term benefits? | *High-quality early childhood education | Longer summer holidays | Larger classes | The fifth paragraph says so. | High-quality early childhood education has shown long-term benefits

## The decline of local news | CO
Over the past two decades, thousands of local newspapers have closed or drastically reduced their staff. The causes are well known: advertising revenue, once the foundation of the newspaper business, has moved to online platforms, and many readers now expect news to be free.

The consequences, however, are less widely appreciated. Local newspapers do more than report events. They attend council meetings, examine public budgets and investigate local businesses and institutions. When they disappear, communities can lose their main source of information about the decisions that most directly affect their lives.

Research has begun to measure these effects. Studies in several countries have found that after local newspapers close, fewer candidates stand in local elections, voter participation falls and public borrowing costs can rise, possibly because reduced scrutiny allows inefficiency or corruption to go unnoticed.

The decline also affects social cohesion. Local news covers schools, sports teams, community events and obituaries, creating a shared sense of place. Without it, residents may rely more on national media and social networks, where local issues receive little attention and misinformation can spread easily.

Various models are being tried to fill the gap. Some newspapers have become non-profit organisations supported by donations and foundations. Others rely on reader subscriptions or membership schemes. In some countries, public funds support local reporting, though this raises questions about independence.

None of these approaches has yet replaced the lost revenue on a large scale. But the experiments reflect a growing recognition that local journalism is not merely a commercial product but a public good, essential to the functioning of democracy at the community level.
? c | What has caused many local newspapers to close? | *Advertising revenue moving online and readers expecting free news | Too many journalists | Expensive paper | The first paragraph explains. | has moved to online platforms, and many readers now expect news to be free.
? c | What did studies find after local newspapers close? | *Fewer candidates and lower voter participation | More candidates | Lower public borrowing costs | The third paragraph explains. | fewer candidates stand in local elections, voter participation falls
? t | Local news coverage of community events contributes to a shared sense of place. | T | The fourth paragraph says so. | creating a shared sense of place.
? s | What question does public funding of local reporting raise? | independence / questions about independence | The fifth paragraph says so. | though this raises questions about independence.
? c | How is local journalism increasingly seen, according to the writer? | *As a public good essential to democracy | As purely a commercial product | As unnecessary | The last paragraph explains. | local journalism is not merely a commercial product but a public good

## Sport and the nation | HS
Few events unite a country as powerfully as international sport. When a national team plays in a major tournament, streets empty, strangers celebrate together and flags appear on balconies. Sport has become one of the most visible expressions of national identity in the modern world.

Historians note that this connection is relatively recent. Many modern sports were codified in the nineteenth century, and international competitions grew alongside the development of nation-states and mass media. Governments soon recognised sport's potential to build national pride and project an image abroad. Hosting major events such as the Olympic Games has often been seen as a way for countries to signal their economic development and global status.

The effects can be positive. Sporting success can foster a sense of belonging and shared purpose, bringing together citizens across social, regional and ethnic divisions. National teams that include players from diverse backgrounds can challenge narrow definitions of national identity.

However, sport can also amplify division. Rivalries between nations sometimes reflect political tensions, and nationalist sentiment can turn into hostility towards opponents or even towards players whose performance is judged a failure. Athletes from minority backgrounds have at times faced abuse after defeats, revealing the conditional nature of their acceptance.

The economic case for hosting major events is also contested. Studies frequently find that the costs of new stadiums and infrastructure exceed the long-term benefits, leaving some host cities with expensive, underused facilities.

Sport, therefore, mirrors the societies in which it is played. It can express inclusive pride and solidarity, but it can also reveal underlying tensions about who truly belongs.
? c | According to historians, when did the connection between sport and nation develop? | *Relatively recently, alongside nation-states and mass media | In ancient times | Only in this century | The second paragraph explains. | Historians note that this connection is relatively recent.
? c | Why have countries hosted major events? | *To signal economic development and global status | To reduce costs | To discourage tourism | The second paragraph explains. | a way for countries to signal their economic development and global status.
? t | Diverse national teams can challenge narrow definitions of national identity. | T | The third paragraph says so. | can challenge narrow definitions of national identity.
? s | What do studies frequently find about the costs of hosting major events? | they exceed the long-term benefits / costs exceed benefits | The fifth paragraph says so. | the costs of new stadiums and infrastructure exceed the long-term benefits
? c | What does sport mirror, according to the writer? | *The societies in which it is played | Only government policy | Nothing beyond the game | The last paragraph explains. | Sport, therefore, mirrors the societies in which it is played.

## Machines and the future of work | WK
Predictions that machines will make human workers obsolete are not new. In the nineteenth century, textile workers destroyed mechanical looms, fearing for their livelihoods. Yet in the long run, technological change created more jobs than it destroyed, as rising productivity generated new industries and occupations.

Today, advances in artificial intelligence and robotics have revived these fears. Unlike earlier machines, which mainly replaced physical labour, modern technologies can perform cognitive tasks such as analysing documents, translating languages and diagnosing diseases from medical images. Some estimates suggest that a substantial proportion of current jobs could be significantly affected within the coming decades.

Economists, however, emphasise that automation usually transforms jobs rather than eliminating them entirely. Most occupations consist of many different tasks, only some of which can be automated. Bank tellers, for example, did not disappear when cash machines were introduced; instead, their role shifted towards customer service and sales.

The more serious concern may be distribution. Workers in routine middle-skill jobs are often most exposed, while highly skilled professionals may benefit from new tools that increase their productivity. Without intervention, technological change could widen inequality and leave many workers struggling to adapt.

This has led to calls for major investment in education and lifelong learning, enabling workers to retrain throughout their careers. Some also propose strengthening social safety nets to support those whose jobs disappear.

The future of work, in other words, is not determined by technology alone. It will depend on choices made by governments, businesses and societies about how the benefits of automation are shared.
? c | What happened in the long run after earlier technological changes? | *More jobs were created than destroyed | All workers lost their jobs | Productivity fell | The first paragraph explains. | technological change created more jobs than it destroyed
? c | How do modern technologies differ from earlier machines? | *They can perform cognitive tasks | They only replace physical labour | They are cheaper | The second paragraph explains. | modern technologies can perform cognitive tasks
? t | Bank tellers disappeared when cash machines were introduced. | F | Their role shifted. | Bank tellers, for example, did not disappear
? s | Which workers are often most exposed to automation? | workers in routine middle-skill jobs / routine middle-skill workers | The fourth paragraph says so. | Workers in routine middle-skill jobs are often most exposed
? c | What will the future of work depend on, according to the writer? | *Choices about how the benefits of automation are shared | Technology alone | The weather | The last paragraph explains. | It will depend on choices made by governments, businesses and societies

## The water challenge | EN
Water covers most of the Earth's surface, yet only a tiny fraction is fresh water accessible for human use. As populations grow, cities expand and the climate changes, pressure on this limited resource is increasing. Many experts consider water scarcity one of the most serious challenges of the twenty-first century.

Agriculture accounts for the largest share of global freshwater use, mostly for irrigation. In many regions, farmers pump groundwater faster than it can be naturally replenished, causing water tables to fall. Some major rivers no longer reach the sea for parts of the year because so much water is extracted upstream.

Climate change is intensifying the problem. Rising temperatures increase evaporation, and changing rainfall patterns bring longer droughts in some areas and more intense floods in others. Glaciers that supply water to hundreds of millions of people during dry seasons are shrinking.

Scarcity is not only a matter of physical supply. In many places, the problem is economic or political: water exists but infrastructure to deliver it safely is lacking, or access is unequal. Poorer communities often pay more for water, sometimes buying it from private vendors at high prices.

Solutions exist, though they require investment and cooperation. Efficient irrigation techniques, such as drip systems, can substantially reduce agricultural use. Repairing leaking pipes can save significant amounts in cities. Treated wastewater can be reused for industry or irrigation, and some countries rely increasingly on desalination, though it is energy-intensive.

Because rivers and aquifers often cross national borders, cooperation between countries is also essential. Managing water fairly and sustainably may become one of the defining tests of international collaboration.
? c | Which sector uses the largest share of global fresh water? | *Agriculture | Industry | Households | The second paragraph says so. | Agriculture accounts for the largest share of global freshwater use
? c | How is climate change intensifying water scarcity? | *Higher evaporation and changing rainfall patterns | More glaciers forming | Less evaporation | The third paragraph explains. | Rising temperatures increase evaporation, and changing rainfall patterns bring longer droughts
? t | Poorer communities often pay less for water. | F | They often pay more. | Poorer communities often pay more for water
? s | What water source is energy-intensive? | desalination | The fifth paragraph says so. | some countries rely increasingly on desalination, though it is energy-intensive.
? c | Why is international cooperation essential? | *Rivers and aquifers often cross national borders | Water is sold internationally | Rain falls everywhere equally | The last paragraph explains. | Because rivers and aquifers often cross national borders

## Rethinking the zoo | AN
Zoos have existed in various forms for thousands of years, but their purpose has changed considerably. Early menageries displayed exotic animals as symbols of wealth and power. Modern zoos, by contrast, typically describe their mission in terms of conservation, education and research.

Supporters point to genuine achievements. Several species that became extinct in the wild have survived thanks to breeding programmes in zoos, and some have been successfully reintroduced into their natural habitats. Zoos also fund conservation projects in the wild and contribute to scientific understanding of animal behaviour, health and reproduction. For many visitors, especially children, seeing live animals can inspire a lasting interest in wildlife.

Critics, however, question whether these benefits justify keeping animals in captivity. They note that most animals kept in zoos are not endangered and that breeding programmes often involve species chosen for their appeal to visitors rather than their conservation needs. Some animals, particularly large, wide-ranging species such as elephants and whales, may suffer in captivity, showing signs of stress or repetitive behaviour.

The educational value of zoos is also debated. While zoos claim to raise awareness, studies have produced mixed results about whether visits lead to lasting changes in knowledge or behaviour.

In response, many modern zoos have redesigned enclosures to resemble natural habitats, focused on species with genuine conservation needs and stopped keeping animals that are particularly unsuited to captivity. Some advocates argue that resources should increasingly shift towards protecting habitats in the wild.

The debate reflects a broader question: how should humans balance their fascination with wildlife against the welfare of individual animals and the survival of species?
? c | How did early menageries differ from modern zoos? | *They displayed animals as symbols of wealth and power | They focused on conservation | They released animals | The first paragraph explains. | Early menageries displayed exotic animals as symbols of wealth and power.
? c | What achievement do supporters point to? | *Some species survived through zoo breeding programmes | All zoo animals are endangered | Zoos have no costs | The second paragraph explains. | Several species that became extinct in the wild have survived thanks to breeding programmes in zoos
? t | Critics say most zoo animals are endangered. | F | Most are not endangered. | most animals kept in zoos are not endangered
? s | Which large species may suffer most in captivity? | elephants and whales / elephants / whales | The third paragraph gives examples. | such as elephants and whales
? c | What have many modern zoos done in response? | *Redesigned enclosures and focused on species with conservation needs | Closed permanently | Increased the number of large animals | The fifth paragraph explains. | redesigned enclosures to resemble natural habitats, focused on species with genuine conservation needs

## A burger in every city | FD
In almost any major city in the world, it is possible to find the same burgers, fried chicken and coffee served under the same familiar logos. The global spread of fast-food chains is often cited as a symbol of globalisation and of the homogenisation of culture.

Critics argue that the expansion of these chains threatens local food traditions. Small family restaurants and street vendors may struggle to compete with the marketing power and efficiency of multinational companies. Diets high in processed food, sugar and fat have been linked to rising rates of obesity and related diseases in many countries undergoing rapid economic change.

Yet the picture is more nuanced than simple cultural replacement. Global chains frequently adapt their menus to local tastes, offering rice dishes in Asia, spicy flavours in Latin America or vegetarian options in countries where many people do not eat beef. Sociologists use the term "glocalisation" to describe this blending of global and local elements.

Moreover, the influence does not run in only one direction. Dishes once considered local specialities, such as sushi, tacos and Vietnamese pho, have themselves become global, served in cities far from their origins. In many places, a renewed interest in traditional and regional cuisine has emerged partly as a reaction to standardised fast food.

For consumers, fast-food chains offer convenience, predictability and often affordable prices, which help explain their popularity, particularly among young urban populations.

Ultimately, the globalisation of food reflects broader patterns of cultural exchange. It brings both opportunities for diversity and risks of uniformity, and the outcome depends partly on how communities value and support their own culinary traditions.
? c | What do critics say fast-food chains threaten? | *Local food traditions | Global trade | Tourism | The second paragraph explains. | the expansion of these chains threatens local food traditions.
? s | What term describes blending global and local elements? | glocalisation | The third paragraph names it. | Sociologists use the term "glocalisation"
? c | How do global chains often adapt? | *By changing menus to local tastes | By lowering prices only | By closing local branches | The third paragraph explains. | Global chains frequently adapt their menus to local tastes
? t | Local dishes like pho have become global. | T | The fourth paragraph says so. | Dishes once considered local specialities, such as sushi, tacos and Vietnamese pho, have themselves become global
? c | What does the outcome of food globalisation partly depend on? | *How communities value their own culinary traditions | The size of restaurants | Government advertising | The last paragraph explains. | the outcome depends partly on how communities value and support their own culinary traditions.

## Designing happier cities | PT
Urban planners have traditionally focused on practical concerns: housing enough people, moving traffic efficiently and providing essential services. Increasingly, however, researchers and designers are asking a different question: how can cities make people happier?

Evidence suggests that the design of urban environments significantly affects wellbeing. Access to green spaces is one of the most consistent findings. People living near parks report lower stress and better mental health, and even brief exposure to trees and water appears to have restorative effects.

Social connection is another key factor. Neighbourhoods with lively streets, small shops, benches and public squares encourage spontaneous encounters between residents. By contrast, environments dominated by highways and large car parks can discourage walking and isolate people from one another. Some research suggests that long commutes are among the most consistently unpleasant parts of people's days, which strengthens the case for compact, mixed-use neighbourhoods where homes, workplaces and services are close together.

Noise, pollution and a sense of insecurity also undermine wellbeing. Narrower streets, slower traffic and good lighting can make public spaces feel safer and more inviting.

Critics caution that happiness is shaped by many factors beyond design, including income, employment and relationships, and that improvements to neighbourhoods can raise property prices, potentially displacing the residents they were intended to benefit.

Nevertheless, a growing number of cities now consider wellbeing explicitly in planning decisions, measuring not only economic output but also residents' satisfaction, health and sense of community. The underlying idea is simple but powerful: cities should be designed around the needs of people rather than vehicles.
? c | What have urban planners traditionally focused on? | *Practical concerns like housing and traffic | Happiness only | Art and culture | The first paragraph explains. | Urban planners have traditionally focused on practical concerns
? c | Which finding about green spaces is described as consistent? | *People near parks report lower stress | Parks increase noise | Parks reduce property values | The second paragraph explains. | People living near parks report lower stress and better mental health
? t | Long commutes are among the most pleasant parts of people's days. | F | They are among the most unpleasant. | long commutes are among the most consistently unpleasant parts of people's days
? s | What can neighbourhood improvements raise, potentially displacing residents? | property prices | The fifth paragraph says so. | improvements to neighbourhoods can raise property prices
? c | What is the underlying idea of wellbeing-focused planning? | *Cities should be designed around people rather than vehicles | Cities should grow as fast as possible | Cars should have priority | The last paragraph explains. | cities should be designed around the needs of people rather than vehicles.

## The unreliable witness | HE
We tend to think of memory as a recording device that stores experiences accurately, ready to be replayed. Decades of psychological research suggest otherwise. Memory is reconstructive: each time we recall an event, we rebuild it from fragments, filling gaps with expectations, general knowledge and information acquired later.

This process is usually efficient, but it makes memory vulnerable to distortion. In a series of influential experiments, participants watched videos of car accidents and were later asked how fast the cars were going when they "smashed" or "hit" each other. Those who heard the word "smashed" estimated higher speeds and were more likely to report seeing broken glass, although there was none in the video.

Researchers have even shown that it is possible to create memories of events that never occurred. When participants were repeatedly encouraged to imagine a childhood experience, such as being lost in a shopping centre, a significant minority came to believe it had really happened.

These findings have important implications for the legal system. Eyewitness testimony can be highly persuasive in court, yet studies of wrongful convictions later overturned through DNA evidence have found that mistaken eyewitness identification was a contributing factor in many cases. Stress, the presence of a weapon and leading questions from investigators can all reduce accuracy.

In response, some police forces have changed procedures, for example by ensuring that the officer conducting an identification does not know which person is the suspect, and by recording witnesses' confidence immediately.

None of this means memory is generally worthless. But it does suggest that confidence and accuracy are not the same, and that even vivid memories should be treated with caution.
? c | How does research describe memory? | *As reconstructive | As an exact recording | As permanent and unchanging | The first paragraph explains. | Memory is reconstructive
? c | What happened to participants who heard the word "smashed"? | *They estimated higher speeds and some recalled broken glass | They remembered less | They refused to answer | The second paragraph explains. | Those who heard the word "smashed" estimated higher speeds
? t | Researchers have shown it is possible to create memories of events that never happened. | T | The third paragraph says so. | it is possible to create memories of events that never occurred.
? s | What evidence overturned many wrongful convictions? | DNA evidence / DNA | The fourth paragraph says so. | wrongful convictions later overturned through DNA evidence
? c | What does the writer conclude about confidence and accuracy? | *They are not the same | They are always linked | Confidence guarantees accuracy | The last paragraph explains. | it does suggest that confidence and accuracy are not the same
"""

PASSAGES["C1"] += """
## Can money buy happiness? | MS
For decades, governments have measured national progress primarily through economic growth. A rising gross domestic product has been treated as evidence that citizens' lives are improving. Yet a growing number of economists and psychologists question whether income is a reliable measure of wellbeing.

Research presents a nuanced picture. Within countries, richer people tend to report higher life satisfaction than poorer people, particularly when incomes are low and additional money helps meet basic needs such as food, housing and healthcare. However, as incomes rise, each additional increase appears to contribute less to happiness. Some studies suggest that beyond a certain level, extra income has only a modest effect on day-to-day emotional wellbeing.

Over time, the relationship becomes even more puzzling. In several wealthy countries, average incomes have increased substantially over recent decades, while reported happiness has remained relatively stable. One explanation is that people compare themselves with others; if everyone becomes richer, relative position changes little. Another is adaptation: people quickly become accustomed to higher living standards, and new possessions soon lose their power to delight.

Other factors appear to matter greatly. Strong relationships, good health, meaningful work, trust in institutions and a sense of control over one's life are consistently associated with wellbeing. Unemployment, loneliness and long commutes are associated with lower satisfaction, often more strongly than differences in income.

In response, some countries have begun to supplement economic indicators with measures of wellbeing, using surveys to assess life satisfaction, health and social connection. Critics warn that happiness is difficult to measure and could be used to justify neglecting material needs. Supporters argue that such measures encourage policies focused on what people actually value.
? c | When does additional money help happiness most? | *When incomes are low and basic needs are unmet | When people are already rich | Never | The second paragraph explains. | particularly when incomes are low and additional money helps meet basic needs
? c | What has happened in several wealthy countries over recent decades? | *Incomes rose while reported happiness stayed stable | Happiness doubled | Incomes fell | The third paragraph explains. | average incomes have increased substantially over recent decades, while reported happiness has remained relatively stable.
? s | What is the term for people quickly becoming used to higher living standards? | adaptation | The third paragraph says so. | Another is adaptation
? t | Loneliness is associated with lower satisfaction. | T | The fourth paragraph says so. | Unemployment, loneliness and long commutes are associated with lower satisfaction
? c | What do critics warn about wellbeing measures? | *Happiness is difficult to measure and could justify neglecting material needs | They are too cheap | They are already perfect | The last paragraph explains. | Critics warn that happiness is difficult to measure and could be used to justify neglecting material needs.

## The quiet decline of insects | AN
Insects rarely attract the attention given to large, charismatic animals such as tigers or whales. Yet they are among the most important organisms on the planet. They pollinate crops and wild plants, recycle nutrients, control pests and form the basis of food chains for birds, fish and mammals.

In recent years, a series of studies has suggested that insect populations in many regions are declining. Some long-term surveys have recorded dramatic falls in the total mass of flying insects in protected areas. Researchers caution, however, that data are uneven: long-term records exist mainly for parts of Europe and North America, and trends vary between species and places. Some insects are thriving, while others are disappearing.

The causes are multiple and interconnected. The conversion of natural habitats into farmland and urban areas removes the plants and nesting sites insects depend on. Intensive agriculture often involves pesticides, some of which harm beneficial insects as well as pests. Climate change alters temperatures and the timing of seasons, and artificial light at night disrupts the behaviour of many nocturnal species.

The consequences could be far-reaching. A large share of crops depends at least partly on animal pollination, and declines in pollinators could affect food production and prices. Birds that feed on insects are also likely to suffer.

Encouragingly, insect populations can recover relatively quickly when conditions improve, because many species reproduce rapidly. Measures such as planting native flowers, reducing pesticide use, leaving areas of gardens and farmland less tidy and protecting habitats can make a significant difference. Scientists emphasise that better monitoring is also needed to understand where and why declines are occurring.
? c | Why are insects described as important? | *They pollinate plants, recycle nutrients and support food chains | They are large and charismatic | They are easy to study | The first paragraph explains. | They pollinate crops and wild plants, recycle nutrients, control pests and form the basis of food chains
? c | What do researchers caution about the data? | *Long-term records exist mainly for parts of Europe and North America | The data are complete everywhere | Insects are increasing everywhere | The second paragraph explains. | long-term records exist mainly for parts of Europe and North America
? t | Some insect species are thriving. | T | The second paragraph says so. | Some insects are thriving, while others are disappearing.
? s | What at night disrupts many nocturnal species? | artificial light / artificial light at night | The third paragraph says so. | artificial light at night disrupts the behaviour of many nocturnal species.
? c | Why can insect populations recover relatively quickly? | *Many species reproduce rapidly | Insects never die | Pesticides help them | The last paragraph explains. | because many species reproduce rapidly.

## The science of persuasion | CO
Advertisers, politicians, salespeople and fundraisers all share a common goal: to persuade people to think or act in particular ways. Psychological research has identified several principles that make persuasion more effective, many of which operate largely outside our conscious awareness.

One is reciprocity. People feel obliged to return favours, even small ones. Charities that include a small gift with a request for donations often receive more money, and customers who receive a free sample may feel inclined to buy.

Another is social proof. When people are uncertain, they look at what others are doing. Messages stating that most guests reuse their hotel towels have been found to increase towel reuse more than messages about environmental benefits alone.

Authority also plays a role. People are more likely to follow advice from individuals perceived as experts, which is why advertisements often feature doctors or scientists. Scarcity is similarly powerful: products described as limited or available for a short time appear more desirable.

Commitment and consistency form a further principle. Once people have made a small commitment, such as signing a petition, they are more likely to agree to larger requests that seem consistent with it.

These principles can be used ethically, for example to encourage healthier behaviour or charitable giving. But they can also be exploited, creating artificial urgency or false impressions of popularity. Understanding them can help people recognise when they are being influenced and make more deliberate decisions. As one researcher noted, the goal is not to become immune to persuasion, which is part of normal social life, but to ensure that our choices genuinely reflect our own interests.
? s | What principle describes feeling obliged to return favours? | reciprocity | The second paragraph names it. | One is reciprocity.
? c | What increased towel reuse in hotels more effectively? | *Messages that most guests reuse their towels | Messages about environmental benefits alone | Free towels | The third paragraph explains. | Messages stating that most guests reuse their hotel towels have been found to increase towel reuse
? c | Why do advertisements often feature doctors or scientists? | *People follow advice from perceived experts | Doctors are cheap to hire | It is required by law | The fourth paragraph explains. | People are more likely to follow advice from individuals perceived as experts
? t | After a small commitment, people are less likely to agree to larger requests. | F | They are more likely. | they are more likely to agree to larger requests
? c | According to the researcher, what is the goal? | *Ensuring choices reflect our own interests | Becoming immune to persuasion | Never trusting anyone | The last paragraph explains. | to ensure that our choices genuinely reflect our own interests.

## Opening up science | ED
Much scientific research is funded by the public, through government grants and universities. Yet for decades, the results have often been published in journals that charge high subscription fees, making them inaccessible to many researchers, teachers, journalists and members of the public. The open science movement seeks to change this.

At its core, open science aims to make research publications, data and methods freely available. Open access journals allow anyone to read articles without payment. Researchers increasingly share their raw data and computer code, enabling others to check their findings or use the data for new studies.

Supporters argue that openness accelerates progress. When data are shared, scientists can build on each other's work more quickly and avoid duplicating experiments. During major public health emergencies, the rapid sharing of genetic data and early results has allowed researchers around the world to collaborate at unprecedented speed.

Openness may also strengthen reliability. In several fields, attempts to reproduce published results have failed surprisingly often. Making data and methods available allows independent researchers to identify errors, and the practice of registering study plans in advance discourages selective reporting of positive results.

However, the transition raises challenges. Many open access journals cover their costs by charging authors fees, which can be prohibitive for researchers in poorer countries or less well-funded fields. Sharing data involving human participants requires careful protection of privacy. Some researchers also worry that others may benefit from data they spent years collecting without receiving appropriate credit.

Despite these difficulties, funding agencies increasingly require the research they support to be openly available, suggesting that open science is becoming the norm rather than the exception.
? c | Why were many research results inaccessible? | *Journals charged high subscription fees | They were secret | They were not written down | The first paragraph explains. | published in journals that charge high subscription fees
? c | What does open science aim to make freely available? | *Publications, data and methods | Only equipment | Only funding | The second paragraph explains. | open science aims to make research publications, data and methods freely available.
? t | Attempts to reproduce published results have always succeeded. | F | They have failed surprisingly often. | attempts to reproduce published results have failed surprisingly often.
? s | Who may find author fees prohibitive? | researchers in poorer countries / researchers in poorer countries or less well-funded fields | The fifth paragraph says so. | can be prohibitive for researchers in poorer countries or less well-funded fields.
? c | What suggests open science is becoming the norm? | *Funding agencies increasingly require open availability | Journals are closing | Scientists refuse to share | The last paragraph explains. | funding agencies increasingly require the research they support to be openly available

## Watching the smart city | TE
Across the world, cities are installing networks of sensors, cameras and data systems to manage traffic, energy, waste and public safety more efficiently. These so-called smart cities promise cleaner air, shorter journeys and better services. Traffic lights can adjust to real-time congestion, bins can signal when they need emptying and streetlights can dim when streets are empty.

The benefits can be substantial. Data on traffic flows can help planners redesign dangerous junctions, and monitoring of water networks can detect leaks quickly. In some cities, smart systems have reduced energy consumption and response times for emergency services.

However, the same technologies raise serious concerns about privacy and surveillance. Cameras equipped with facial recognition can identify individuals in public spaces, and data from transport cards, phones and sensors can reveal detailed patterns of people's movements. Critics warn that such information could be misused by authorities to monitor protesters or by companies to target advertising.

There are also questions about control. Smart city projects are often developed in partnership with large technology companies. Citizens may not know what data is collected, how long it is stored or who has access to it. If critical infrastructure depends on systems owned by private firms, cities may become dependent on those companies.

Several cities have responded by adopting principles of data governance. These include collecting only the data necessary for a specific purpose, anonymising information where possible, publishing details of how systems work and involving residents in decisions. Some have banned facial recognition by public agencies altogether.

The debate highlights a broader point: technology can make cities more efficient, but whether it makes them better places to live depends on democratic choices about how it is used.
? c | What can smart traffic lights do? | *Adjust to real-time congestion | Issue fines automatically | Turn off at night | The first paragraph explains. | Traffic lights can adjust to real-time congestion
? c | What privacy concern do critics raise? | *Data could reveal detailed patterns of movement and be misused | Sensors are too expensive | Cameras break easily | The third paragraph explains. | can reveal detailed patterns of people's movements.
? t | Citizens always know what data is collected about them. | F | They may not know. | Citizens may not know what data is collected
? s | What have some cities banned public agencies from using? | facial recognition | The fifth paragraph says so. | Some have banned facial recognition by public agencies altogether.
? c | According to the writer, what determines whether technology makes cities better? | *Democratic choices about its use | The number of sensors | Private companies alone | The last paragraph explains. | depends on democratic choices about how it is used.

## Small loans, big hopes | MS
For much of history, people living in poverty have had little access to formal banking. Without collateral or credit histories, they could not obtain loans from banks and often relied on informal moneylenders who charged extremely high interest rates. In the late twentieth century, microfinance emerged as a potential solution.

Microfinance institutions provide small loans, often to women, to start or expand small businesses such as tailoring, food stalls or livestock farming. Many programmes rely on group lending, in which borrowers form small groups and share responsibility for repayment. Social pressure and mutual support within the group help ensure high repayment rates, even without collateral.

Early enthusiasm was enormous. Microfinance was celebrated as a way to lift millions out of poverty while remaining financially sustainable, and its pioneers received international recognition.

Subsequent research, however, has produced more modest conclusions. Several rigorous studies comparing communities with and without access to microloans found that, while borrowers often invested in businesses and gained flexibility in managing their finances, average increases in income and consumption were small. Microfinance did not, on its own, transform the lives of most borrowers.

Problems have also emerged. In some regions, rapid commercial expansion led to over-indebtedness, with borrowers taking multiple loans to repay earlier ones. High interest rates charged by some lenders attracted criticism.

Nevertheless, microfinance has had important benefits. Access to savings accounts and insurance can help poor households cope with emergencies, and some evidence suggests that financial services can strengthen women's economic independence. Many experts now view microfinance as one useful tool among many, rather than a cure for poverty.
? c | Why could people in poverty not get bank loans? | *They lacked collateral and credit histories | Banks were closed | They didn't want loans | The first paragraph explains. | Without collateral or credit histories, they could not obtain loans from banks
? s | What lending model has borrowers share responsibility in groups? | group lending | The second paragraph names it. | Many programmes rely on group lending
? c | What did rigorous studies find about average income increases? | *They were small | They were enormous | Incomes fell sharply | The fourth paragraph explains. | average increases in income and consumption were small.
? t | Rapid commercial expansion led to over-indebtedness in some regions. | T | The fifth paragraph says so. | rapid commercial expansion led to over-indebtedness
? c | How do many experts now view microfinance? | *As one useful tool among many | As a cure for poverty | As completely useless | The last paragraph explains. | as one useful tool among many, rather than a cure for poverty.

## A tired society | HE
Sleep is often the first thing people sacrifice when life becomes busy. Long working hours, commuting, family responsibilities and evening screen use all compete with time in bed. Surveys in many countries suggest that a substantial proportion of adults regularly sleep less than the seven hours that health experts generally recommend.

The consequences extend far beyond feeling tired. Research has linked chronic sleep deprivation to a range of health problems, including obesity, diabetes, cardiovascular disease and weakened immunity. Sleep also plays a vital role in mental health and cognitive function. During sleep, the brain consolidates memories and clears metabolic waste, and insufficient sleep impairs attention, judgement and emotional regulation.

The effects are not only individual. Tired workers are less productive and more prone to errors, and drowsy driving contributes to a significant number of road accidents. Some economic analyses estimate that insufficient sleep costs countries considerable sums in lost productivity.

Part of the problem is cultural. In many workplaces, long hours and constant availability are associated with commitment, while sleep may be seen as a sign of weakness. Technology has blurred the boundaries between work and home, with emails and messages arriving late at night.

Changing this requires action at multiple levels. Individuals can adopt consistent sleep schedules, limit caffeine later in the day and reduce exposure to bright screens before bed. Employers can discourage out-of-hours communication and offer flexible working. Some health experts argue that sleep should be treated as a public health priority, alongside nutrition and exercise, rather than as a luxury.
? s | How many hours of sleep do health experts generally recommend? | seven hours / seven / 7 | The first paragraph says so. | less than the seven hours that health experts generally recommend.
? c | Which health problems has chronic sleep deprivation been linked to? | *Obesity, diabetes and cardiovascular disease | Broken bones | Better immunity | The second paragraph explains. | including obesity, diabetes, cardiovascular disease and weakened immunity.
? c | What does the brain do during sleep? | *Consolidates memories and clears metabolic waste | Stops working completely | Produces more stress | The second paragraph explains. | the brain consolidates memories and clears metabolic waste
? t | In many workplaces, sleep may be seen as a sign of weakness. | T | The fourth paragraph says so. | sleep may be seen as a sign of weakness.
? c | How do some health experts argue sleep should be treated? | *As a public health priority | As a luxury | As a private matter only | The last paragraph explains. | sleep should be treated as a public health priority

## Letting nature return | EN
For much of the twentieth century, conservation focused on protecting particular species and carefully managing habitats. In recent decades, a different approach has gained popularity: rewilding. Instead of intensively managing landscapes, rewilding aims to restore natural processes and allow ecosystems to regulate themselves.

Rewilding projects take many forms. Some involve reintroducing species that have disappeared from an area, such as beavers, wolves or bison. Others focus on removing dams so rivers can flow freely, allowing farmland to return to forest, or reconnecting fragmented habitats.

Supporters point to striking results. Beavers, for example, build dams that slow water flow, create wetlands and reduce flooding downstream, while providing habitats for many other species. In some areas, the return of large predators has altered the behaviour of grazing animals, allowing vegetation to recover.

Rewilding also promises benefits for people. Restored wetlands and forests can store carbon, improve water quality and attract nature tourism, providing new economic opportunities for rural communities.

However, rewilding is controversial. Farmers worry about predators attacking livestock and about losing productive land. Some communities feel that rewilding projects are imposed by outsiders who do not depend on the land for their livelihoods. Scientists also debate how far ecosystems can return to a "natural" state, given that landscapes have been shaped by humans for thousands of years and the climate is changing.

Successful projects increasingly emphasise collaboration with local communities, compensation for losses and clear long-term goals. Rewilding, its advocates argue, is not about excluding people from nature but about creating landscapes where both can thrive.
? c | What does rewilding aim to do? | *Restore natural processes so ecosystems regulate themselves | Manage every species closely | Build more farms | The first paragraph explains. | rewilding aims to restore natural processes and allow ecosystems to regulate themselves.
? c | How do beavers help reduce flooding? | *Their dams slow water flow and create wetlands | They drink a lot of water | They remove trees from rivers | The third paragraph explains. | build dams that slow water flow, create wetlands and reduce flooding downstream
? t | Restored wetlands and forests can store carbon. | T | The fourth paragraph says so. | Restored wetlands and forests can store carbon
? s | What do farmers worry about regarding predators? | predators attacking livestock / attacks on livestock | The fifth paragraph says so. | Farmers worry about predators attacking livestock
? c | What do successful projects increasingly emphasise? | *Collaboration with local communities | Excluding people from nature | Removing all farms | The last paragraph explains. | Successful projects increasingly emphasise collaboration with local communities

## Reading our genes | HE
A few decades ago, sequencing a single human genome required years of work and enormous sums of money. Today, consumers can send a saliva sample to a company and receive information about their ancestry and certain genetic health risks within weeks, often for a modest fee.

Genetic testing offers real benefits. For people with a family history of certain conditions, tests can identify inherited risks, allowing earlier screening and preventive measures. Genetic information can also help doctors choose medications more likely to work for a particular patient, an approach known as personalised medicine.

However, the growth of genetic testing raises complex questions. Many conditions are influenced by numerous genes as well as lifestyle and environmental factors. A test may indicate a slightly increased risk without providing clear guidance, leading to anxiety or false reassurance. Without professional interpretation, consumers may misunderstand results.

Privacy is another major concern. Genetic data is uniquely personal and also reveals information about relatives, who have not consented to testing. Questions arise about how companies store data, whether they share it with researchers or other organisations, and how it could be used by insurers or employers. Some countries have introduced laws preventing genetic discrimination, but protections vary considerably.

There are also ethical dilemmas within families. Should people be told about genetic risks for which no treatment exists? Should parents test children for conditions that may only appear in adulthood?

Experts generally recommend that people consider these issues before testing, read privacy policies carefully and seek advice from genetic counsellors, who can help interpret results and support individuals in making informed decisions.
? c | How has genetic testing changed over recent decades? | *It has become fast and relatively cheap | It has become slower | It is now illegal | The first paragraph explains. | consumers can send a saliva sample to a company
? s | What is the approach of choosing medications based on genetics called? | personalised medicine | The second paragraph names it. | an approach known as personalised medicine.
? c | Why might test results cause anxiety or false reassurance? | *Many conditions depend on many genes and lifestyle factors | Tests are always wrong | Doctors refuse to explain them | The third paragraph explains. | Many conditions are influenced by numerous genes as well as lifestyle and environmental factors.
? t | Genetic data reveals information only about the person tested. | F | It also reveals information about relatives. | also reveals information about relatives
? c | Who can help interpret results, according to experts? | *Genetic counsellors | Insurance companies | Employers | The last paragraph explains. | seek advice from genetic counsellors

## Meat without animals | FD
Global demand for meat continues to rise as populations grow and incomes increase. Yet livestock farming has a substantial environmental footprint, using large areas of land and water and contributing significantly to greenhouse gas emissions. It also raises concerns about animal welfare. In response, scientists and companies are developing alternatives, including meat grown from animal cells.

Cultivated meat is produced by taking a small sample of cells from an animal and growing them in nutrient-rich conditions in large containers called bioreactors. The cells multiply and can be formed into products such as minced meat or chicken pieces. Because no animals need to be raised and slaughtered, supporters believe the technology could dramatically reduce land use and animal suffering.

Several challenges remain, however. Producing cultivated meat at scale is technically difficult and currently expensive. The process requires significant energy, and its environmental benefits depend heavily on whether that energy comes from renewable sources. Some life-cycle analyses suggest that, if powered by fossil fuels, cultivated meat could have a larger climate impact than some conventional meat.

Recreating the texture and flavour of whole cuts, such as steak, is particularly challenging, because these involve complex structures of muscle, fat and connective tissue.

Consumer acceptance is also uncertain. Surveys show mixed attitudes: some people are enthusiastic, while others are uneasy about eating food produced in laboratories or doubt that it is natural.

Regulators in a few countries have approved the sale of cultivated meat products. Many experts see it as one part of a broader transition that may also include plant-based alternatives and reduced meat consumption, rather than a single solution.
? c | What is cultivated meat grown in? | *Bioreactors | Fields | Greenhouses | The second paragraph explains. | in large containers called bioreactors.
? c | What do supporters believe the technology could reduce? | *Land use and animal suffering | The price of vegetables | Water in rivers | The second paragraph explains. | could dramatically reduce land use and animal suffering.
? t | If powered by fossil fuels, cultivated meat could have a larger climate impact than some conventional meat. | T | The third paragraph says so. | if powered by fossil fuels, cultivated meat could have a larger climate impact than some conventional meat.
? s | Why are whole cuts like steak particularly challenging? | they involve complex structures of muscle, fat and connective tissue / complex structures | The fourth paragraph explains. | these involve complex structures of muscle, fat and connective tissue.
? c | How do many experts see cultivated meat? | *As one part of a broader transition | As the only solution | As a failure | The last paragraph explains. | as one part of a broader transition

## Cities of newcomers | PT
Cities have always been shaped by migration. Throughout history, people have moved from the countryside to urban centres, and from one country to another, in search of work, safety and opportunity. Today, many of the world's largest cities have significant populations born elsewhere.

Migrants contribute to urban life in many ways. They fill labour shortages in sectors such as healthcare, construction, hospitality and agriculture, and they are often more likely than native-born residents to start businesses. Neighbourhoods shaped by migration frequently become centres of cultural exchange, known for their restaurants, markets and festivals.

Migration also creates challenges. Rapid population growth can strain housing, schools and public services. Newcomers may face language barriers, discrimination and difficulties in having their qualifications recognised, which can force skilled professionals into low-paid work. In some cities, migrants become concentrated in poorer neighbourhoods with limited opportunities.

Public attitudes vary widely and can be shaped by economic conditions, media coverage and political debate. Research suggests that direct contact between different groups, through workplaces, schools and community activities, tends to reduce prejudice.

Many cities have developed integration policies. These include language classes, programmes to recognise foreign qualifications, support for migrant entrepreneurs and efforts to ensure fair access to housing. Some cities also involve migrant communities directly in local decision-making.

Integration is increasingly understood as a two-way process. It requires newcomers to adapt to their new society, but also requires that society to adjust, ensuring that institutions are accessible and that diversity is recognised as a source of strength rather than a threat.
? c | In which sectors do migrants often fill labour shortages? | *Healthcare, construction, hospitality and agriculture | Only technology | Only government | The second paragraph lists them. | such as healthcare, construction, hospitality and agriculture
? c | Why may skilled migrants end up in low-paid work? | *Their qualifications may not be recognised | They prefer it | They lack experience | The third paragraph explains. | difficulties in having their qualifications recognised, which can force skilled professionals into low-paid work.
? t | Research suggests contact between different groups tends to increase prejudice. | F | It tends to reduce prejudice. | tends to reduce prejudice.
? s | Name one integration policy mentioned. | language classes / programmes to recognise foreign qualifications / support for migrant entrepreneurs | The fifth paragraph lists them. | These include language classes, programmes to recognise foreign qualifications
? c | How is integration increasingly understood? | *As a two-way process | As the newcomers' job alone | As unnecessary | The last paragraph explains. | Integration is increasingly understood as a two-way process.

## Does homework help? | ED
Few aspects of school life generate as much debate among parents, teachers and students as homework. Supporters argue that it reinforces learning, develops independent study skills and allows parents to see what their children are learning. Critics argue that it causes stress, reduces time for play and family life, and widens inequality.

Research suggests that the answer depends heavily on age. For secondary school students, moderate amounts of homework are generally associated with higher achievement, although the benefits appear to diminish beyond a certain point. For younger children, the evidence of academic benefit is much weaker. Some researchers argue that in primary school, reading for pleasure and play may be more valuable than worksheets.

The type of homework also matters. Tasks that are meaningful, clearly linked to classroom learning and appropriately challenging appear more effective than repetitive exercises assigned out of habit. Feedback is important too: homework that is never checked or discussed may do little to improve learning.

Homework can also reinforce inequality. Students from wealthier families often have quiet places to study, access to technology and parents able to help, while others may care for siblings, work part-time or lack internet access. When homework counts heavily towards grades, these differences can affect results.

Some schools have responded by reducing homework, especially for younger pupils, or by providing supervised study time at school. Others have shifted to "flipped" approaches, in which students watch short explanations at home and practise skills in class with teacher support.

Most researchers conclude that the question is not whether homework is good or bad, but how much, what kind and for whom.
? c | According to research, what does the effect of homework depend heavily on? | *Age | The colour of the paper | The time of year | The second paragraph explains. | Research suggests that the answer depends heavily on age.
? c | What may be more valuable than worksheets in primary school? | *Reading for pleasure and play | More exams | Longer school days | The second paragraph explains. | reading for pleasure and play may be more valuable than worksheets.
? t | Homework that is never checked may do little to improve learning. | T | The third paragraph says so. | homework that is never checked or discussed may do little to improve learning.
? s | What approach has students watch explanations at home and practise in class? | flipped / flipped approaches / the flipped approach | The fifth paragraph names it. | Others have shifted to "flipped" approaches
? c | What do most researchers conclude? | *The question is how much, what kind and for whom | Homework should be banned | Homework always helps | The last paragraph explains. | how much, what kind and for whom.

## Switching off | TE
For many people, the smartphone is the first thing they check in the morning and the last thing they see at night. Constant connectivity offers convenience, information and social contact, but it has also prompted a growing interest in "digital detox", deliberately reducing or temporarily stopping the use of digital devices.

Advocates argue that time away from screens can improve sleep, concentration and relationships. Some people report feeling calmer and more present after spending a weekend without notifications. Retreats, holidays and apps that block distracting websites have emerged to meet demand.

Research on the effects of digital detox is mixed. Some studies have found improvements in wellbeing when participants reduced social media use, particularly when they had previously used it heavily. Others have found little lasting effect, or that abrupt abstinence led to anxiety about missing important information. The benefits seem to depend on how people use technology and why they want to reduce it.

Critics of the detox concept argue that framing technology as a toxin to be periodically removed is unhelpful. Digital tools are deeply integrated into work, education and social life, and complete withdrawal is unrealistic for most people. Short breaks may simply be followed by a return to the same habits.

Many experts therefore favour a more sustainable approach sometimes called digital wellbeing. This involves examining which uses of technology add value and which cause stress, and making ongoing changes: turning off non-essential notifications, keeping phones out of bedrooms, scheduling time for focused work and prioritising face-to-face interaction.

The aim is not to reject technology but to use it intentionally, so that it serves people's goals rather than controlling their attention.
? c | What is a digital detox? | *Deliberately reducing or stopping the use of digital devices | Cleaning a phone | Buying a new device | The first paragraph explains. | deliberately reducing or temporarily stopping the use of digital devices.
? c | What did some studies find about abrupt abstinence? | *It led to anxiety about missing information | It always improved wellbeing | It had no effect on anyone | The third paragraph explains. | abrupt abstinence led to anxiety about missing important information.
? t | Critics consider complete withdrawal realistic for most people. | F | They consider it unrealistic. | complete withdrawal is unrealistic for most people.
? s | What is the more sustainable approach called? | digital wellbeing | The fifth paragraph names it. | sometimes called digital wellbeing.
? c | What is the aim, according to the writer? | *To use technology intentionally | To reject technology | To use technology more | The last paragraph explains. | The aim is not to reject technology but to use it intentionally

## Creativity in later life | PF
Popular culture often associates creativity and innovation with youth. Stories of young entrepreneurs and prodigies dominate the media, and many people assume that creative abilities decline with age. Research, however, presents a more varied picture.

Studies of scientists, inventors and artists suggest that creativity can peak at very different ages depending on the type of work. Fields that reward bold conceptual leaps, such as theoretical mathematics, may favour younger people. By contrast, fields that depend on accumulated knowledge and experience, such as history, philosophy and many forms of writing, often see significant achievements later in life.

Some researchers distinguish between two types of creators. "Conceptual" innovators make sudden, radical breakthroughs, often early in their careers. "Experimental" innovators work through gradual trial and error, refining their ideas over many years, and their most important work frequently comes later.

Ageing also brings cognitive changes. While processing speed and some aspects of memory may decline, knowledge, vocabulary and the ability to see connections between different areas often continue to develop. Older adults may also be less concerned with others' opinions, allowing them to take creative risks.

Engaging in creative activities appears to benefit older people themselves. Programmes involving music, painting, writing or dance have been associated with improved mood, social connection and cognitive health.

Societies are ageing rapidly, and these findings challenge assumptions that older people are primarily recipients of care. Many continue to contribute ideas, art and innovation well into their seventies and beyond, provided they have opportunities and encouragement to do so.
? c | What does popular culture often associate with creativity? | *Youth | Old age | Wealth | The first paragraph explains. | Popular culture often associates creativity and innovation with youth.
? c | In which fields are significant achievements often later in life? | *Fields depending on accumulated knowledge, like history | Theoretical mathematics | Sports | The second paragraph explains. | fields that depend on accumulated knowledge and experience, such as history, philosophy and many forms of writing
? s | What kind of innovators work through gradual trial and error? | experimental innovators / experimental | The third paragraph names them. | "Experimental" innovators work through gradual trial and error
? t | Knowledge and vocabulary usually decline quickly with age. | F | They often continue to develop. | knowledge, vocabulary and the ability to see connections between different areas often continue to develop.
? c | What have creative programmes for older people been associated with? | *Improved mood, social connection and cognitive health | Higher stress | Lower social contact | The fifth paragraph explains. | have been associated with improved mood, social connection and cognitive health.

## Science needs failure | ED
Scientific progress is often presented as a series of brilliant discoveries. Textbooks and news reports highlight breakthroughs, while the many experiments that failed are rarely mentioned. Yet failure is not an unfortunate side effect of science; it is central to how science works.

The scientific method depends on testing ideas that may turn out to be wrong. A hypothesis is valuable precisely because it can be disproved. When an experiment fails to produce the expected result, it can reveal flaws in theories, prompt new questions and lead researchers in unexpected directions. Several important discoveries, including some medicines, emerged from experiments designed for entirely different purposes.

However, the culture of research does not always value failure. Academic careers often depend on publishing in prestigious journals, which have traditionally favoured positive and surprising results. Studies that find no effect are less likely to be published, a problem known as publication bias. As a result, the scientific record may overstate the evidence for certain findings, and other researchers may waste time repeating experiments that have already failed.

Pressure to produce positive results can also encourage questionable practices, such as selectively reporting data or analysing results in multiple ways until something appears significant.

In response, reforms are spreading. Some journals now accept studies based on their methods before results are known, guaranteeing publication regardless of outcome. Databases allow researchers to register studies in advance and report negative findings. Some funders actively support replication studies.

Recognising the value of failure, advocates argue, would make science more honest, efficient and ultimately more successful.
? c | Why is a hypothesis valuable, according to the text? | *It can be disproved | It is always correct | It is easy to publish | The second paragraph explains. | A hypothesis is valuable precisely because it can be disproved.
? s | What is the problem of studies with no effect being less likely to be published called? | publication bias | The third paragraph names it. | a problem known as publication bias.
? c | What can pressure to produce positive results encourage? | *Questionable practices like selective reporting | More honest research | Fewer publications | The fourth paragraph explains. | can also encourage questionable practices, such as selectively reporting data
? t | Some journals now accept studies based on their methods before results are known. | T | The fifth paragraph says so. | Some journals now accept studies based on their methods before results are known
? c | What do advocates argue recognising failure would do? | *Make science more honest, efficient and successful | Slow science down | Reduce funding | The last paragraph explains. | would make science more honest, efficient and ultimately more successful.

## The right to repair | SH
When a smartphone screen cracks or a washing machine stops working, many consumers face a frustrating choice: pay a high price for official repairs or replace the product entirely. Increasingly, people are demanding a "right to repair", the ability to fix the products they own or have them fixed by independent repairers at reasonable cost.

Advocates argue that many modern products are deliberately difficult to repair. Components may be glued rather than screwed together, special tools may be required, and manufacturers may restrict access to spare parts, manuals and diagnostic software. Some products contain software that prevents unofficial replacement parts from working.

These practices have environmental consequences. Electronic waste is one of the fastest-growing waste streams in the world, and much of it is not properly recycled. Extending the life of products through repair reduces the need for new manufacturing, which consumes energy and raw materials.

Manufacturers have raised several objections. They argue that unauthorised repairs could compromise safety, for example with batteries, and that sharing technical information could expose intellectual property or create security risks. They also note that official repair networks guarantee quality.

Nevertheless, the right-to-repair movement has achieved significant progress. Several jurisdictions have passed laws requiring manufacturers to make spare parts and repair information available for a certain number of years. Some companies now sell repair kits directly to consumers, and repair scores rating how easily products can be fixed have been introduced in some markets.

The movement reflects a broader shift in attitudes towards consumption, away from disposability and towards products designed to last.
? c | What does the right to repair mean? | *Being able to fix your products or use independent repairers at reasonable cost | Free products | Returning products for any reason | The first paragraph explains. | the ability to fix the products they own or have them fixed by independent repairers at reasonable cost.
? c | How may products be made difficult to repair? | *Components glued and access to parts restricted | Using bright colours | Selling them cheaply | The second paragraph explains. | Components may be glued rather than screwed together
? t | Electronic waste is one of the fastest-growing waste streams. | T | The third paragraph says so. | Electronic waste is one of the fastest-growing waste streams in the world
? s | What safety concern do manufacturers raise about unauthorised repairs? | batteries / safety with batteries | The fourth paragraph gives the example. | for example with batteries
? c | What does the movement reflect? | *A shift away from disposability towards durable products | More consumption | Less interest in technology | The last paragraph explains. | away from disposability and towards products designed to last.

## Travelling alone | TR
Solo travel, once considered unusual, has become increasingly popular. Travel companies report growing numbers of people booking trips alone, from students taking gap years to retirees exploring new countries. Women make up a significant share of solo travellers.

People travel alone for many reasons. Some simply cannot find companions whose schedules, budgets or interests match their own. Others actively choose independence, valuing the freedom to set their own pace, change plans spontaneously and pursue their own interests without compromise.

Many solo travellers describe the experience as transformative. Without a companion to rely on, they must navigate unfamiliar places, solve problems and make decisions independently, which can build confidence and resilience. Travelling alone also often makes people more open to meeting others, whether fellow travellers or local residents.

There are, however, challenges. Loneliness can be a problem, particularly during long trips or at mealtimes. Solo travellers often pay more, since accommodation is frequently priced per room rather than per person. Safety is a significant concern, especially for women travelling in some destinations, and solo travellers lack someone to help in emergencies.

The industry has responded with services designed for solo travellers, including group tours for people travelling alone, accommodation without supplements for single occupancy and social events in hostels. Online communities allow travellers to share advice and arrange to meet.

Experienced solo travellers recommend careful preparation: researching destinations, sharing itineraries with family or friends, keeping digital copies of important documents and trusting instincts in unfamiliar situations. Many argue that, with sensible precautions, the rewards of travelling alone far outweigh the risks.
? c | Why do some people travel alone? | *They cannot find companions with matching schedules or interests | They are not allowed to travel with others | It is always cheaper | The second paragraph explains. | Some simply cannot find companions whose schedules, budgets or interests match their own.
? c | How can solo travel build confidence? | *Travellers must solve problems and make decisions independently | Travellers follow a guide all the time | Travellers stay at home | The third paragraph explains. | they must navigate unfamiliar places, solve problems and make decisions independently
? t | Solo travellers often pay less for accommodation. | F | They often pay more. | Solo travellers often pay more
? s | What do experienced solo travellers recommend sharing with family or friends? | itineraries / their itineraries | The last paragraph says so. | sharing itineraries with family or friends
? c | What do many solo travellers argue? | *The rewards outweigh the risks with sensible precautions | Solo travel is too dangerous | Solo travel is boring | The last paragraph explains. | the rewards of travelling alone far outweigh the risks.

## Doing well by doing good? | WK
In the past, many people believed that the sole responsibility of a business was to make profits for its shareholders while obeying the law. Today, companies are increasingly expected to consider their impact on employees, communities and the environment. This expectation is often described as corporate social responsibility.

Companies engage in social responsibility in many ways: reducing carbon emissions, ensuring fair working conditions in supply chains, supporting local charities or encouraging employees to volunteer. Many publish annual reports describing their environmental and social performance.

Supporters argue that responsible behaviour benefits companies themselves. Consumers, particularly younger ones, increasingly prefer brands that share their values. Employees may be more motivated and loyal when they believe their employer contributes positively to society. Investors are paying growing attention to environmental and social risks, which can affect long-term profitability.

Critics, however, question how much of this activity reflects genuine commitment. Some companies are accused of "greenwashing", promoting minor environmental initiatives while continuing harmful practices elsewhere. Social responsibility reports are often voluntary and difficult to verify, and companies may highlight positive stories while omitting negative ones.

Others argue that relying on voluntary corporate action is insufficient. They contend that serious problems, such as climate change and labour exploitation, require binding regulations rather than goodwill.

In response, some governments are introducing mandatory reporting requirements and due diligence laws, obliging companies to identify and address human rights and environmental risks in their supply chains. The debate increasingly centres not on whether companies have social responsibilities, but on how they can be held accountable for meeting them.
? c | What was the traditional view of business responsibility? | *To make profits for shareholders while obeying the law | To support charities | To protect the environment | The first paragraph explains. | the sole responsibility of a business was to make profits for its shareholders while obeying the law.
? c | Why might responsible behaviour benefit companies? | *Consumers and employees prefer companies that share their values | It reduces taxes | It is required everywhere | The third paragraph explains. | Consumers, particularly younger ones, increasingly prefer brands that share their values.
? s | What is promoting minor environmental initiatives while continuing harmful practices called? | greenwashing | The fourth paragraph names it. | Some companies are accused of "greenwashing"
? t | Social responsibility reports are always independently verified. | F | They are often voluntary and difficult to verify. | Social responsibility reports are often voluntary and difficult to verify
? c | What does the debate increasingly centre on? | *How companies can be held accountable | Whether companies have social responsibilities | Whether profits matter | The last paragraph explains. | how they can be held accountable for meeting them.

## When species invade | AN
When a plant, animal or microorganism is introduced to an area outside its natural range, it usually fails to establish itself. Occasionally, however, a newcomer thrives, spreading rapidly and causing significant ecological and economic harm. Such organisms are known as invasive species.

Invasive species are often introduced by human activity, sometimes deliberately and sometimes by accident. Plants have been imported for gardens, animals released as pets or for hunting, and countless organisms carried unintentionally in the ballast water of ships, in shipments of timber or on travellers' clothing. Global trade and travel have greatly increased the frequency of such introductions.

Once established, invasive species can outcompete native species for food and space, prey on animals that have no evolved defences or introduce diseases. On islands, where wildlife has often evolved in isolation, the effects can be particularly severe; introduced predators such as rats and cats have contributed to the extinction of numerous bird species.

The economic costs are also substantial. Invasive insects can devastate crops and forests, aquatic plants can block waterways and certain species damage infrastructure. Estimates suggest the global costs run into many billions of dollars each year.

Preventing introductions is generally far cheaper than controlling established populations. Many countries inspect imported goods, regulate the trade in plants and animals and require ships to treat ballast water. Early detection programmes, often involving members of the public, can identify new invasions before they spread.

Once a species is widespread, eradication is often impossible, and management focuses on limiting its impact. Some successful eradications, particularly of rats on islands, have allowed native wildlife to recover dramatically.
? c | What happens to most introduced species? | *They usually fail to establish themselves | They always spread rapidly | They become native | The first paragraph explains. | it usually fails to establish itself.
? c | How have many organisms been introduced unintentionally? | *In ships' ballast water and timber shipments | Through radio signals | Through rain | The second paragraph explains. | carried unintentionally in the ballast water of ships, in shipments of timber
? t | Introduced predators have contributed to the extinction of island birds. | T | The third paragraph says so. | have contributed to the extinction of numerous bird species.
? s | What is generally far cheaper than controlling established populations? | preventing introductions / prevention | The fifth paragraph says so. | Preventing introductions is generally far cheaper than controlling established populations.
? c | What has happened after some eradications of rats on islands? | *Native wildlife has recovered dramatically | New invasions followed | Nothing changed | The last paragraph explains. | have allowed native wildlife to recover dramatically.

## The limits of human performance | HS
World records in athletics continue to fall, though more slowly than in the past. Sports scientists have long debated whether there are ultimate limits to human physical performance and how close athletes are to reaching them.

Over the twentieth century, performance improved dramatically. Part of this progress reflected better nutrition, training methods and medical care, as well as the professionalisation of sport, which allowed athletes to train full-time. Increased participation also mattered: as more people around the world took up sport, the chances of discovering exceptionally talented individuals grew.

Technology has played an important role too. Improvements in tracks, shoes, swimsuits and equipment have enhanced performance, sometimes controversially. In several sports, governing bodies have banned or restricted equipment considered to offer an unfair advantage, raising questions about where the boundary lies between human achievement and technological assistance.

Some researchers have analysed historical data and suggested that improvements in many events are levelling off, indicating that athletes may be approaching biological limits. Human physiology imposes constraints on factors such as the speed at which muscles contract and the body's capacity to deliver oxygen.

However, predictions about limits have often been proved wrong. Barriers once thought impossible to break, such as running a mile in under four minutes, have been surpassed. Advances in understanding genetics, recovery and psychology may unlock further improvements.

The question also raises ethical concerns. As margins of victory narrow, the temptation to use prohibited substances may grow. Ensuring fair competition while recognising the role of science and technology remains one of the central challenges facing modern sport.
? c | What contributed to performance improvements in the twentieth century? | *Better nutrition, training methods and medical care | Fewer competitions | Smaller stadiums | The second paragraph explains. | Part of this progress reflected better nutrition, training methods and medical care
? c | Why did increased participation matter? | *More chances of discovering exceptional talent | Fewer injuries | Cheaper tickets | The second paragraph explains. | the chances of discovering exceptionally talented individuals grew.
? t | Governing bodies have banned some equipment considered unfair. | T | The third paragraph says so. | governing bodies have banned or restricted equipment considered to offer an unfair advantage
? s | Which barrier, once thought impossible, has been surpassed? | running a mile in under four minutes / the four-minute mile | The fifth paragraph gives the example. | such as running a mile in under four minutes
? c | What ethical concern does the question raise? | *Narrow margins may increase the temptation to use prohibited substances | Records are too easy | Athletes train too little | The last paragraph explains. | the temptation to use prohibited substances may grow.

## Alone in a connected world | PF
In an era of instant communication and social media, it might seem paradoxical that loneliness is described by some health experts as a growing public health concern. Yet surveys in many countries suggest that substantial numbers of people report feeling lonely often or always.

Loneliness is not the same as being alone. It refers to the painful feeling that one's social relationships are insufficient in number or quality. People can feel lonely in a crowd or within a marriage, while others live alone contentedly.

Research has linked chronic loneliness to a range of health problems, including depression, cardiovascular disease, weakened immunity and cognitive decline. Some studies suggest that its effects on mortality may be comparable to those of other well-known risk factors.

Loneliness affects all age groups. Older adults may experience it after retirement, bereavement or reduced mobility. Surprisingly, several surveys have found high levels of loneliness among young adults, who may face transitions such as moving away for study or work, and who sometimes compare their social lives unfavourably with others online.

Several social changes may contribute, including smaller households, greater geographic mobility and longer working hours that reduce time for relationships and community activities.

Responses have emerged at many levels. Some governments have appointed officials responsible for addressing loneliness. Doctors in some countries can refer patients to community activities, such as walking groups, art classes or volunteering, an approach known as social prescribing. Neighbourhood initiatives, intergenerational programmes and well-designed public spaces can also encourage connection.

Ultimately, addressing loneliness may require recognising social connection not as a private matter, but as an essential component of health and wellbeing.
? c | What does loneliness refer to? | *The feeling that one's relationships are insufficient | Living alone | Having no phone | The second paragraph explains. | the painful feeling that one's social relationships are insufficient in number or quality.
? t | People who live alone are always lonely. | F | Some live alone contentedly. | while others live alone contentedly.
? c | What have several surveys found surprisingly? | *High levels of loneliness among young adults | No loneliness among older people | That loneliness is rare | The fourth paragraph explains. | several surveys have found high levels of loneliness among young adults
? s | What is referring patients to community activities called? | social prescribing | The sixth paragraph names it. | an approach known as social prescribing.
? c | What may addressing loneliness ultimately require? | *Recognising social connection as essential to health | Banning social media | Larger houses | The last paragraph explains. | recognising social connection not as a private matter, but as an essential component of health and wellbeing.

## Buildings that bend | HF
Earthquakes themselves rarely kill people directly. Most deaths and injuries occur when buildings collapse. As a result, the design of earthquake-resistant structures is one of the most important tools for reducing the toll of seismic disasters.

Engineers have developed a range of strategies. Modern building codes in earthquake-prone regions typically require structures to be flexible enough to absorb and dissipate seismic energy, rather than rigid. Reinforced concrete and steel frames allow buildings to bend without breaking, giving occupants time to escape.

More advanced techniques isolate buildings from ground movement. Base isolation systems place flexible bearings, often made of layers of rubber and steel, between a building and its foundations. When the ground shakes, the bearings absorb much of the movement, so the building above moves far less. Some tall buildings contain large dampers, heavy weights or fluid-filled devices that counteract swaying.

Traditional architecture also offers lessons. In several earthquake-prone regions, historic wooden temples and houses have survived centuries of seismic activity thanks to flexible joints and lightweight construction.

The greatest challenge is often not technology but implementation. Many deaths occur in older buildings constructed before modern codes, or in rapidly growing cities where regulations are poorly enforced. Retrofitting existing buildings can be expensive, and in poorer regions resources are limited.

Simple, low-cost solutions can help. Engineers have developed techniques for strengthening masonry homes with affordable materials, and training local builders in safer methods can significantly reduce vulnerability. Experts emphasise that investing in safer construction before disasters is far more effective, and ultimately less costly, than responding afterwards.
? c | What causes most earthquake deaths and injuries? | *Building collapses | The ground opening | Fires only | The first paragraph explains. | Most deaths and injuries occur when buildings collapse.
? c | Why do building codes favour flexibility? | *Flexible buildings absorb and dissipate seismic energy | Flexible buildings are cheaper | Rigid buildings are illegal | The second paragraph explains. | to be flexible enough to absorb and dissipate seismic energy, rather than rigid.
? s | What are base isolation bearings often made of? | layers of rubber and steel / rubber and steel | The third paragraph says so. | often made of layers of rubber and steel
? t | Many deaths occur in buildings constructed after modern codes. | F | They occur in older buildings or where codes are poorly enforced. | Many deaths occur in older buildings constructed before modern codes
? c | What do experts emphasise? | *Investing in safer construction before disasters is more effective | Responding after disasters is cheaper | Technology alone solves the problem | The last paragraph explains. | investing in safer construction before disasters is far more effective

## Laws against waste | FD
Roughly a third of the food produced in the world is lost or wasted, according to widely cited estimates. In wealthier countries, a significant share of this waste occurs in shops and homes, while in poorer countries more food is lost during harvesting, storage and transport.

Some governments have turned to legislation. Certain countries now prohibit large supermarkets from destroying unsold food that is still safe to eat, requiring them instead to donate it to charities or use it for animal feed or compost. Supporters argue that such laws have significantly increased food donations and raised public awareness.

Other measures target date labels. Many consumers discard food when it passes a "best before" date, although this label indicates quality rather than safety. Some retailers have removed such labels from fresh produce, and campaigns encourage people to use their senses to judge whether food is still good.

Businesses are also innovating. Apps connect restaurants and shops with customers who can buy surplus food at reduced prices. Some supermarkets sell "imperfect" fruit and vegetables that would previously have been rejected for cosmetic reasons.

Critics caution that donation laws can shift responsibility to charities, which may lack the capacity to store and distribute large quantities of perishable food. Others argue that reducing overproduction, rather than redistributing surplus, should be the priority.

Nevertheless, food waste has become a recognised policy issue. Reducing it is seen as a way to save money, conserve resources and lower greenhouse gas emissions, since food decomposing in landfill produces methane, a powerful greenhouse gas.
? c | Where does much food waste occur in wealthier countries? | *In shops and homes | During harvesting | During transport | The first paragraph explains. | In wealthier countries, a significant share of this waste occurs in shops and homes
? c | What do some countries require large supermarkets to do? | *Donate unsold safe food instead of destroying it | Lower all prices | Close at night | The second paragraph explains. | requiring them instead to donate it to charities
? t | A "best before" date indicates that food is unsafe after that date. | F | It indicates quality rather than safety. | this label indicates quality rather than safety.
? s | What do critics say charities may lack? | the capacity to store and distribute food / capacity | The fifth paragraph says so. | which may lack the capacity to store and distribute large quantities of perishable food.
? c | Why is reducing food waste linked to lower emissions? | *Food in landfill produces methane | Food waste stops rain | Food waste uses electricity | The last paragraph explains. | food decomposing in landfill produces methane

## Predicting the weather | NW
Weather forecasts are so familiar that it is easy to forget how remarkable they are. Using observations from satellites, weather balloons, ships and thousands of ground stations, meteorologists can predict conditions days in advance with considerable accuracy. A five-day forecast today is roughly as reliable as a one-day forecast was several decades ago.

Modern forecasting relies on numerical weather prediction. The atmosphere is divided into a three-dimensional grid, and powerful supercomputers use the laws of physics to calculate how temperature, pressure, humidity and wind will change at each point over time.

Despite these advances, forecasts can never be perfect. The atmosphere is a chaotic system, meaning that tiny differences in initial conditions can grow into large differences over time. Because observations can never capture every detail of the atmosphere, small errors inevitably exist, and their effects grow, limiting how far ahead weather can be predicted precisely.

To address this uncertainty, forecasters use ensemble forecasting. Instead of running a single simulation, they run many slightly different versions. If most produce similar results, forecasters can be confident; if they diverge widely, the forecast is less certain. This approach allows forecasts to be expressed as probabilities, such as a seventy percent chance of rain.

Communicating uncertainty remains a challenge. Many people misunderstand probability forecasts, and forecasters must balance the risk of false alarms against the danger of failing to warn about severe weather.

Accurate forecasts have enormous value. They save lives by warning of storms and floods, help farmers plan planting and harvesting, and support industries from aviation to energy.
? c | How does a five-day forecast today compare with the past? | *It is roughly as reliable as a one-day forecast decades ago | It is less reliable | It is perfect | The first paragraph explains. | A five-day forecast today is roughly as reliable as a one-day forecast was several decades ago.
? s | What is modern forecasting based on? | numerical weather prediction | The second paragraph names it. | Modern forecasting relies on numerical weather prediction.
? c | Why can forecasts never be perfect? | *The atmosphere is chaotic and small errors grow | Computers are too slow | Satellites are unreliable | The third paragraph explains. | The atmosphere is a chaotic system
? t | In ensemble forecasting, forecasters run a single simulation. | F | They run many slightly different versions. | Instead of running a single simulation, they run many slightly different versions.
? c | What balance must forecasters strike? | *Between false alarms and failing to warn of severe weather | Between cost and speed | Between satellites and balloons | The fifth paragraph explains. | balance the risk of false alarms against the danger of failing to warn about severe weather.

## The library reinvented | ED
With so much information available online, some predicted that public libraries would become obsolete. Instead, many libraries have reinvented themselves, and in some communities they are busier than ever.

Libraries still lend books, but their role has expanded considerably. Many provide free internet access and computers, which remain essential for people who cannot afford devices or connections at home. Librarians help users apply for jobs, access government services and develop digital skills.

Libraries have also become community spaces. They host language classes, homework clubs, reading groups for children and talks by local experts. Some offer "makerspaces" with 3D printers and tools, while others lend unusual items such as musical instruments or gardening equipment. For many people, particularly older residents and young families, libraries are one of the few public places where they can spend time without being expected to buy anything.

Their role in combating misinformation has also grown. Librarians are trained to evaluate sources and can help users distinguish reliable information from misleading content.

Nevertheless, libraries face serious challenges. In many places, budgets have been cut, leading to reduced opening hours, fewer staff and closures. Some libraries rely increasingly on volunteers. Digital lending raises complex issues, as publishers often charge libraries higher prices for e-books than consumers pay.

Supporters argue that libraries represent a rare democratic institution, open to everyone regardless of income, age or background. As societies become more digital and, in some ways, more divided, they contend that libraries' importance is increasing rather than declining.
? c | What did some people predict about libraries? | *They would become obsolete | They would become more expensive | They would replace schools | The first paragraph explains. | some predicted that public libraries would become obsolete.
? c | Why is free internet access at libraries essential? | *Some people cannot afford devices or connections | It is faster than at home | It is required by law | The second paragraph explains. | which remain essential for people who cannot afford devices or connections at home.
? s | What spaces with 3D printers and tools do some libraries offer? | makerspaces | The third paragraph names them. | Some offer "makerspaces" with 3D printers and tools
? t | Publishers often charge libraries less for e-books than consumers pay. | F | They often charge higher prices. | publishers often charge libraries higher prices for e-books than consumers pay.
? c | How do supporters describe libraries? | *A rare democratic institution open to everyone | An outdated service | A business | The last paragraph explains. | libraries represent a rare democratic institution

## Whose treasures? | ED
The world's great museums hold vast collections of objects from other cultures, many acquired during periods of colonial rule. In recent years, there have been growing demands for the return of cultural artefacts to the countries and communities from which they were taken.

Advocates of return, often called restitution, argue that many objects were acquired through conquest, theft or under conditions in which meaningful consent was impossible. For source communities, these artefacts may have profound religious, historical or cultural significance, and their absence represents a continuing loss. Returning them, supporters argue, is a matter of justice and an opportunity to acknowledge historical wrongs.

Museums have traditionally offered several counterarguments. Some have claimed that objects are safer in their care, with better conservation facilities and security. Others argue that "universal museums" allow millions of visitors to see artefacts from many cultures side by side, promoting understanding of shared human history. Legal restrictions in some countries also prevent national collections from being permanently transferred.

These arguments have been increasingly challenged. Many countries seeking returns have built modern museums capable of caring for artefacts, and critics note that the idea of universal access is undermined when people from source countries cannot easily obtain visas to visit the museums holding their heritage.

In recent years, several museums and governments have returned significant collections, and others have launched research into the origins of their holdings. Alternative arrangements, including long-term loans, joint exhibitions and digital sharing, have also been explored.

The debate raises fundamental questions about ownership, memory and the role of museums. Increasingly, the conversation is shifting from whether objects should be returned to how restitution can be carried out fairly and collaboratively.
? s | What is the return of cultural artefacts often called? | restitution | The second paragraph names it. | often called restitution
? c | Why do advocates argue for return? | *Many objects were taken through conquest or without real consent | Museums are too full | Objects are damaged | The second paragraph explains. | many objects were acquired through conquest, theft or under conditions in which meaningful consent was impossible.
? c | What do "universal museums" claim to offer? | *A chance to see artefacts from many cultures side by side | Free entry | Better weather | The third paragraph explains. | allow millions of visitors to see artefacts from many cultures side by side
? t | Critics note that people from source countries can easily get visas to visit these museums. | F | They cannot easily obtain visas. | when people from source countries cannot easily obtain visas
? c | How is the conversation shifting? | *From whether to return objects to how to do it fairly | From museums to schools | Away from the topic entirely | The last paragraph explains. | the conversation is shifting from whether objects should be returned to how restitution can be carried out fairly and collaboratively.
"""

# MORE LEVELS


def parse(level, block, first_id):
    passages, n = [], first_id
    for chunk in filter(None, (c.strip() for c in block.strip().split("\n## "))):
        chunk = chunk.removeprefix("## ")
        head, _, body = chunk.partition("\n")
        title, topic = (part.strip() for part in head.split(" | "))
        text_lines, questions = [], []
        for row in body.splitlines():
            if row.startswith("? "):
                kind, prompt, *rest = (part.strip() for part in row[2:].split(" | "))
                q = {"id": f"r{n}q{len(questions) + 1}", "prompt": prompt, "explanation": rest[-2],
                     "evidence": rest[-1]}
                if kind == "c":
                    options = [o.lstrip("*") for o in rest[:-2]]
                    answers = [o.lstrip("*") for o in rest[:-2] if o.startswith("*")]
                    assert len(answers) == 1 and len(set(options)) == len(options) >= 3, (title, prompt)
                    q.update(type="choice", options=options, answers=answers)
                elif kind == "s":
                    q.update(type="short", answers=[a.strip() for a in rest[0].split(" / ")])
                else:
                    q.update(type="tfng", answers=[TFNG[rest[0]]])
                questions.append(q)
            else:
                text_lines.append(row.strip())
        text = re.sub(r"\n{3,}", "\n\n", "\n".join(text_lines).strip())
        words = len(text.split())
        assert 150 <= words <= 350, (title, words)
        assert len(questions) == 5, (title, len(questions))
        for q in questions:
            assert q["evidence"] in text, (title, q["evidence"])
        passages.append({"id": f"r{n}", "title": title, "level": level, "topic": TOPICS[topic], "text": text,
                         "questions": [{k: q[k] for k in
                                        ("id", "type", "prompt", "options", "answers", "explanation", "evidence")
                                        if k in q} for q in questions]})
        n += 1
    return passages


def main():
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "reading.json"
    out = [r for r in json.loads(path.read_text(encoding="utf-8")) if int(r["id"][1:]) <= 6]
    for level, block in PASSAGES.items():
        out += parse(level, block, len(out) + 1)
    titles = [r["title"].lower() for r in out]
    assert len(set(titles)) == len(titles), sorted({t for t in titles if titles.count(t) > 1})
    counts = {lv: sum(1 for r in out if r["level"] == lv) for lv in LEVELS}
    for level in PASSAGES:
        assert counts[level] == 50, counts
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(out), "passages", counts)


main()

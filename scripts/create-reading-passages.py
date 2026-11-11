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

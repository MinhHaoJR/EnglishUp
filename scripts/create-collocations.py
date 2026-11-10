"""Writes src/data/vocabulary-collocations.json: 150 IELTS Writing collocations in 15 themes (10 each).

The headwords and themes follow a common IELTS Writing study list that the user shared (10/11/2026).
The Vietnamese meanings, English definitions, example sentences and levels are written for EnglishUp;
no wording is copied from that list. Every example contains the headword exactly, so the app can
highlight it. IPA stays empty until reviewed. Run: python scripts/create-collocations.py
"""
import json
import pathlib
import re

# theme -> [(headword, level, Vietnamese meaning, English definition, example)]
THEMES = {
    "Education": [
        ("access to education", "B2", "cơ hội được đi học", "the chance to attend school or study", "Girls in remote villages still have limited access to education."),
        ("receive a formal education", "B2", "được học hành chính quy", "to study at school, college or university in an organised way", "Not everyone who succeeds in business has had the chance to receive a formal education."),
        ("acquire practical skills", "B2", "học được kỹ năng thực tế", "to gain abilities that are useful in real situations", "Work placements let students acquire practical skills before they graduate."),
        ("develop critical thinking skills", "B2", "phát triển tư duy phản biện", "to improve the ability to judge ideas and evidence carefully", "Group projects help pupils develop critical thinking skills."),
        ("improve academic performance", "B2", "nâng cao kết quả học tập", "to get better marks and results at school", "A quiet place to study can improve academic performance."),
        ("meet students' needs", "B2", "đáp ứng nhu cầu của học sinh", "to provide what different learners require", "Schools need more teaching assistants to meet students' needs."),
        ("place pressure on students", "B2", "tạo áp lực cho học sinh", "to make learners feel stressed or worried", "Ranking pupils by test scores can place pressure on students."),
        ("allocate funding to education", "C1", "dành ngân sách cho giáo dục", "to decide that public money will be spent on schools", "The province plans to allocate funding to education in poorer districts."),
        ("reduce educational inequality", "C1", "thu hẹp bất bình đẳng trong giáo dục", "to make learning opportunities fairer between groups", "Free textbooks are one way to reduce educational inequality."),
        ("provide equal learning opportunities", "B2", "mang lại cơ hội học tập như nhau", "to give every learner the same chance to study", "A good school system should provide equal learning opportunities for all children."),
    ],
    "Technology": [
        ("technological advances", "B2", "những tiến bộ về công nghệ", "new developments in science and machines", "Technological advances have made banking much faster."),
        ("automate routine tasks", "C1", "tự động hoá việc lặp đi lặp lại", "to let machines do simple jobs that are repeated", "Software can automate routine tasks such as sorting emails."),
        ("artificial intelligence", "B2", "trí tuệ nhân tạo", "computer systems that can learn and make decisions", "Hospitals use artificial intelligence to read X-ray images."),
        ("excessive screen time", "B2", "dùng thiết bị điện tử quá nhiều", "too many hours spent looking at phones, computers or TV", "Doctors link excessive screen time to poor sleep."),
        ("breach of privacy", "C1", "sự xâm phạm quyền riêng tư", "a failure to protect someone's personal information", "Sharing customer data without consent is a breach of privacy."),
        ("bridge the digital divide", "C1", "thu hẹp khoảng cách số", "to reduce the gap between people with and without technology", "Free public Wi-Fi can help bridge the digital divide."),
        ("cybercrime prevention", "C1", "phòng chống tội phạm mạng", "action taken to stop crime committed online", "Banks spend heavily on cybercrime prevention."),
        ("facilitate remote learning", "C1", "tạo điều kiện cho việc học từ xa", "to make it easier to study online from home", "Recorded lectures facilitate remote learning for working adults."),
        ("reliance on smartphones", "B2", "sự lệ thuộc vào điện thoại thông minh", "a strong need to use mobile phones for everyday tasks", "Our reliance on smartphones grows every year."),
        ("driverless vehicles", "B2", "xe tự lái", "cars or buses that drive themselves without a person", "Several cities are testing driverless vehicles on quiet roads."),
    ],
    "Environment": [
        ("combat climate change", "B2", "chống biến đổi khí hậu", "to take action against the warming of the planet", "Planting trees is one small way to combat climate change."),
        ("greenhouse gas emissions", "B2", "lượng khí thải nhà kính", "gases released into the air that trap heat", "Coal power stations produce large greenhouse gas emissions."),
        ("renewable energy sources", "B2", "các nguồn năng lượng tái tạo", "power from sun, wind or water that will not run out", "Vietnam is investing in renewable energy sources such as solar farms."),
        ("deplete natural resources", "C1", "làm cạn kiệt tài nguyên thiên nhiên", "to use up water, minerals or forests faster than they recover", "Overfishing can deplete natural resources within a decade."),
        ("conserve endangered species", "C1", "bảo tồn các loài có nguy cơ tuyệt chủng", "to protect animals and plants that may soon disappear", "National parks help conserve endangered species."),
        ("carbon footprint", "B2", "lượng khí thải carbon của một người hay hoạt động", "the amount of carbon dioxide produced by a person or activity", "Flying less is the quickest way to cut your carbon footprint."),
        ("environmental degradation", "C1", "sự suy thoái môi trường", "damage to land, water and air over time", "Illegal mining has caused serious environmental degradation."),
        ("dispose of hazardous waste", "C1", "xử lý chất thải nguy hại", "to get rid of dangerous waste in a safe way", "Hospitals must dispose of hazardous waste with great care."),
        ("raise environmental awareness", "B2", "nâng cao ý thức về môi trường", "to help people understand environmental problems", "School gardens raise environmental awareness among young children."),
        ("deforestation rates", "C1", "tốc độ phá rừng", "how fast forests are being cut down", "Satellite images show that deforestation rates fell last year."),
    ],
    "Health": [
        ("sedentary lifestyle", "B2", "lối sống ít vận động", "a way of life with little physical activity", "Office work often leads to a sedentary lifestyle."),
        ("adhere to a balanced diet", "C1", "giữ chế độ ăn cân bằng", "to keep eating healthy amounts of different foods", "Athletes adhere to a balanced diet during training."),
        ("prevent chronic diseases", "B2", "phòng ngừa bệnh mãn tính", "to stop long-lasting illnesses from developing", "Walking every day can help prevent chronic diseases."),
        ("strain healthcare systems", "C1", "gây quá tải cho hệ thống y tế", "to put too much pressure on hospitals and medical services", "Flu outbreaks in winter strain healthcare systems."),
        ("mental health issues", "B2", "các vấn đề về sức khỏe tinh thần", "problems such as stress, anxiety or depression", "Many students face mental health issues during exams."),
        ("childhood obesity", "B2", "béo phì ở trẻ em", "the condition of children being much too heavy", "Sugary drinks are a major cause of childhood obesity."),
        ("promote physical activity", "B2", "khuyến khích vận động thể chất", "to encourage people to exercise more", "Cycle lanes promote physical activity in cities."),
        ("life expectancy", "B2", "tuổi thọ trung bình", "the average number of years people are expected to live", "Clean water has raised life expectancy in many countries."),
        ("subsidise healthcare costs", "C1", "trợ giá chi phí y tế", "to pay part of the cost of medical care with public money", "The government should subsidise healthcare costs for the elderly."),
        ("nutritional deficiency", "C1", "sự thiếu hụt dinh dưỡng", "a lack of the vitamins or minerals the body needs", "Pale skin can be a sign of nutritional deficiency."),
    ],
    "Work": [
        ("work-life balance", "B2", "cân bằng giữa công việc và cuộc sống", "a healthy division of time between your job and private life", "Working from home has improved my work-life balance."),
        ("job satisfaction", "B2", "sự hài lòng với công việc", "the pleasure people get from their jobs", "Friendly colleagues add a lot to job satisfaction."),
        ("telecommuting arrangements", "C1", "chế độ làm việc từ xa", "agreements that let staff work away from the office", "The company offers telecommuting arrangements two days a week."),
        ("career advancement opportunities", "C1", "cơ hội thăng tiến", "chances to move to a higher position at work", "Young engineers look for career advancement opportunities."),
        ("competitive salary packages", "C1", "mức lương và phúc lợi hấp dẫn", "pay and benefits that are as good as or better than others", "Tech firms use competitive salary packages to keep staff."),
        ("suffer from burnout", "B2", "bị kiệt sức vì công việc", "to become exhausted from too much work or stress", "Nurses on long shifts often suffer from burnout."),
        ("job security", "B2", "sự ổn định của công việc", "the confidence that you will not lose your job", "Many workers value job security more than high pay."),
        ("pursue a career path", "B2", "theo đuổi một con đường sự nghiệp", "to follow a particular type of work over time", "She decided to pursue a career path in medicine."),
        ("labour market demands", "C1", "nhu cầu của thị trường lao động", "the skills and workers that employers need", "Training courses should follow labour market demands."),
        ("foster team collaboration", "C1", "thúc đẩy làm việc nhóm", "to encourage people to work together well", "Shared goals foster team collaboration."),
    ],
    "Government and public services": [
        ("allocate public funds", "C1", "phân bổ ngân sách công", "to decide how government money is spent", "Councils must allocate public funds fairly between districts."),
        ("subsidise public transport", "C1", "trợ giá phương tiện công cộng", "to pay part of the cost of buses and trains", "Cities that subsidise public transport often have cleaner air."),
        ("enact strict legislation", "C1", "ban hành luật nghiêm ngặt", "to pass firm laws", "Some countries enact strict legislation against plastic bags."),
        ("provide basic necessities", "B2", "cung cấp nhu yếu phẩm thiết yếu", "to supply food, water and shelter", "Aid workers provide basic necessities after a flood."),
        ("national security", "B2", "an ninh quốc gia", "the safety of a country against threats", "The new law was passed for reasons of national security."),
        ("alleviate poverty", "C1", "giảm nghèo", "to make the problems of being poor less severe", "Microloans can alleviate poverty in rural areas."),
        ("implement social policies", "C1", "thực hiện chính sách xã hội", "to put government plans for society into action", "It takes years to implement social policies across a whole country."),
        ("upgrade civic infrastructure", "C1", "nâng cấp hạ tầng công cộng", "to improve public roads, bridges and buildings", "The town needs to upgrade civic infrastructure before the population grows."),
        ("taxpayer money", "B2", "tiền thuế của người dân", "public money that comes from taxes", "Voters want to know how taxpayer money is spent."),
        ("deliver essential services", "B2", "cung cấp các dịch vụ thiết yếu", "to provide services people cannot live without, such as water and health care", "Local governments deliver essential services such as rubbish collection."),
    ],
    "Crime and justice": [
        ("deter criminal behaviour", "C1", "răn đe hành vi phạm tội", "to make people decide not to commit crimes", "Street lighting can deter criminal behaviour at night."),
        ("juvenile delinquency", "C1", "tình trạng phạm pháp ở trẻ vị thành niên", "crime committed by young people", "Youth clubs help reduce juvenile delinquency."),
        ("rehabilitate offenders", "C1", "cải tạo người phạm tội", "to help criminals return to a normal, lawful life", "Education in prison helps rehabilitate offenders."),
        ("reintegrate into society", "C1", "tái hòa nhập cộng đồng", "to become part of normal community life again", "Former prisoners need jobs to reintegrate into society."),
        ("capital punishment", "C1", "án tử hình", "the legal killing of a person as punishment for a crime", "Many countries have abolished capital punishment."),
        ("commit petty crimes", "B2", "phạm những tội nhỏ", "to do minor illegal acts such as shoplifting", "Bored teenagers sometimes commit petty crimes."),
        ("enforce law and order", "C1", "duy trì luật pháp và trật tự", "to make sure people obey laws and stay safe", "Extra police were sent to enforce law and order during the festival."),
        ("custodial sentence", "C1", "án tù giam", "a punishment that sends someone to prison", "The judge gave the driver a custodial sentence of two years."),
        ("recidivism rates", "C1", "tỷ lệ tái phạm", "how often people commit crimes again after punishment", "Job training has lowered recidivism rates in the region."),
        ("prevent illegal activities", "B2", "ngăn chặn hoạt động phi pháp", "to stop actions that break the law", "Border checks prevent illegal activities such as smuggling."),
    ],
    "Media and advertising": [
        ("target young consumers", "B2", "nhắm vào người tiêu dùng trẻ", "to aim products or adverts at young buyers", "Fast-food adverts often target young consumers."),
        ("sensationalise news stories", "C1", "giật gân hóa tin tức", "to report news in a shocking way to attract attention", "Some websites sensationalise news stories to get clicks."),
        ("spread false information", "B2", "lan truyền thông tin sai lệch", "to share untrue facts with many people", "Fake accounts spread false information during elections."),
        ("shape public opinion", "C1", "định hướng dư luận", "to influence what most people think", "Television debates can shape public opinion."),
        ("celebrity endorsement", "C1", "việc người nổi tiếng quảng bá sản phẩm", "a famous person publicly supporting a product", "The new drink sold well thanks to celebrity endorsement."),
        ("unrealistic beauty standards", "B2", "tiêu chuẩn sắc đẹp phi thực tế", "ideas about appearance that few real people can reach", "Edited photos create unrealistic beauty standards."),
        ("curb misleading advertisements", "C1", "hạn chế quảng cáo gây hiểu lầm", "to control adverts that give a false idea of a product", "New rules aim to curb misleading advertisements for diet pills."),
        ("influence purchasing habits", "C1", "tác động đến thói quen mua sắm", "to change how and what people buy", "Online reviews strongly influence purchasing habits."),
        ("independent journalism", "C1", "báo chí độc lập", "news reporting that is free from government or owner control", "A healthy democracy needs independent journalism."),
        ("censor inappropriate content", "C1", "kiểm duyệt nội dung không phù hợp", "to remove material that is unsuitable, especially for children", "Video platforms censor inappropriate content for young viewers."),
    ],
    "Transport": [
        ("ease traffic congestion", "B2", "giảm ùn tắc giao thông", "to make roads less crowded with vehicles", "A new metro line should ease traffic congestion downtown."),
        ("commute to work", "B1", "đi làm hằng ngày", "to travel regularly between home and your workplace", "Many people commute to work by motorbike in Hanoi."),
        ("high-speed rail networks", "B2", "mạng lưới đường sắt cao tốc", "systems of very fast trains between cities", "China has built huge high-speed rail networks."),
        ("pedestrian-friendly zones", "B2", "khu vực thân thiện với người đi bộ", "areas designed for people walking rather than cars", "The old quarter has become one of the city's pedestrian-friendly zones."),
        ("encourage bicycle usage", "B2", "khuyến khích sử dụng xe đạp", "to persuade more people to ride bikes", "Bike-sharing schemes encourage bicycle usage."),
        ("fossil fuel consumption", "C1", "lượng nhiên liệu hóa thạch tiêu thụ", "the amount of coal, oil and gas used", "Electric buses cut fossil fuel consumption."),
        ("improve road safety", "B2", "nâng cao an toàn giao thông", "to make roads less dangerous", "Speed cameras improve road safety near schools."),
        ("peak travel hours", "B2", "giờ cao điểm", "the busiest times for journeys", "Trains are packed during peak travel hours."),
        ("reliable transit infrastructure", "C1", "hạ tầng giao thông công cộng đáng tin cậy", "public transport systems that work well and on time", "Investors prefer cities with reliable transit infrastructure."),
        ("reduce reliance on cars", "B2", "giảm phụ thuộc vào ô tô", "to make people need cars less", "Good bus services reduce reliance on cars."),
    ],
    "Urban life and housing": [
        ("skyrocketing house prices", "C1", "giá nhà tăng vọt", "house prices that rise very fast", "Skyrocketing house prices force young couples to rent."),
        ("affordable housing projects", "B2", "các dự án nhà ở giá phải chăng", "building schemes that offer homes people can pay for", "The city has launched affordable housing projects for factory workers."),
        ("rapid urban sprawl", "C1", "sự mở rộng đô thị ồ ạt", "the fast spread of a city into the countryside", "Rapid urban sprawl has swallowed nearby rice fields."),
        ("substandard living conditions", "C1", "điều kiện sống dưới mức tiêu chuẩn", "housing that is not good enough to be healthy or safe", "Migrant workers often live in substandard living conditions."),
        ("high cost of living", "B2", "chi phí sinh hoạt cao", "the large amount of money needed for everyday needs", "The high cost of living makes big cities hard for students."),
        ("gentrify historic neighbourhoods", "C1", "làm 'thượng lưu hóa' các khu phố cổ", "to renovate old areas so that richer people move in", "Developers gentrify historic neighbourhoods and push out long-time residents."),
        ("ample green spaces", "C1", "nhiều không gian xanh", "plenty of parks and areas with trees and grass", "A healthy city offers ample green spaces."),
        ("population density", "B2", "mật độ dân số", "the number of people living in an area", "Hanoi's old quarter has a very high population density."),
        ("urban renewal programs", "C1", "các chương trình chỉnh trang đô thị", "plans to rebuild and improve run-down parts of a city", "Urban renewal programs turned old warehouses into flats."),
        ("sense of community", "B2", "tinh thần cộng đồng", "a feeling of belonging to a group of neighbours", "Street festivals build a sense of community."),
    ],
    "Family and society": [
        ("nuclear family structure", "C1", "mô hình gia đình hạt nhân", "a family made up of parents and their children only", "Moving to cities has spread the nuclear family structure."),
        ("bridge generation gaps", "C1", "thu hẹp khoảng cách thế hệ", "to help old and young people understand each other", "Shared hobbies can bridge generation gaps."),
        ("balance family responsibilities", "B2", "cân bằng trách nhiệm gia đình", "to manage duties at home alongside other duties", "Single parents must balance family responsibilities with work."),
        ("social cohesion", "C1", "sự gắn kết xã hội", "the bonds that hold a society together", "Public libraries support social cohesion."),
        ("parental guidance", "B2", "sự hướng dẫn của cha mẹ", "advice and supervision from parents", "Some films are suitable only with parental guidance."),
        ("care for elderly relatives", "B2", "chăm sóc người thân lớn tuổi", "to look after old family members", "Many women leave work to care for elderly relatives."),
        ("instil moral values", "C1", "khắc sâu các giá trị đạo đức", "to teach principles of right and wrong over time", "Grandparents often instil moral values through stories."),
        ("income disparity", "C1", "sự chênh lệch thu nhập", "the difference in earnings between groups", "Income disparity between cities and villages is growing."),
        ("gender equality", "B2", "bình đẳng giới", "the same rights and chances for men and women", "Equal pay is a key step towards gender equality."),
        ("ageing population", "B2", "dân số già hóa", "a population with a growing share of old people", "An ageing population needs more nurses and care homes."),
    ],
    "Culture and traditions": [
        ("preserve cultural heritage", "B2", "gìn giữ di sản văn hóa", "to protect the buildings, art and traditions of the past", "Museums help preserve cultural heritage for future visitors."),
        ("traditional customs", "B2", "phong tục truyền thống", "old ways of behaving that a community still follows", "Tet is full of traditional customs such as giving lucky money."),
        ("threaten indigenous cultures", "C1", "đe dọa văn hóa bản địa", "to put the ways of life of native peoples at risk", "Large dams can threaten indigenous cultures in the mountains."),
        ("embrace cultural diversity", "C1", "đón nhận sự đa dạng văn hóa", "to welcome many different cultures", "International schools embrace cultural diversity."),
        ("historical landmarks", "B2", "các công trình lịch sử nổi tiếng", "famous old buildings or places", "Hue is full of historical landmarks."),
        ("loss of cultural identity", "C1", "sự mai một bản sắc văn hóa", "losing the traditions and values that make a group distinct", "Some elders fear a loss of cultural identity among the young."),
        ("pass down through generations", "C1", "truyền qua nhiều thế hệ", "to be given from older family members to younger ones", "Weaving skills pass down through generations in this village."),
        ("intangible cultural heritage", "C1", "di sản văn hóa phi vật thể", "traditions such as music, crafts and festivals rather than objects", "Ca tru singing is recognised as intangible cultural heritage."),
        ("cultural assimilation", "C1", "sự đồng hóa văn hóa", "the process of a group adopting the culture of another", "Learning the local language speeds up cultural assimilation."),
        ("foster intercultural understanding", "C1", "thúc đẩy hiểu biết giữa các nền văn hóa", "to help people from different cultures understand each other", "Student exchanges foster intercultural understanding."),
    ],
    "Globalisation": [
        ("cross-border trade", "B2", "thương mại xuyên biên giới", "buying and selling goods between countries", "New roads have boosted cross-border trade with Laos."),
        ("interconnected global economy", "C1", "nền kinh tế toàn cầu gắn kết chặt chẽ", "a world economy where countries depend on each other", "In an interconnected global economy, one crisis spreads quickly."),
        ("multinational corporations", "B2", "các tập đoàn đa quốc gia", "large companies that operate in many countries", "Multinational corporations have opened factories near Hai Phong."),
        ("cultural homogenisation", "C1", "sự đồng nhất hóa văn hóa", "the process of cultures becoming more and more alike", "Global fast-food chains add to cultural homogenisation."),
        ("international cooperation", "B2", "sự hợp tác quốc tế", "countries working together on shared problems", "Fighting disease requires international cooperation."),
        ("outsourcing production", "C1", "thuê ngoài việc sản xuất", "having goods made by another company, often abroad", "Outsourcing production saves money but can cost local jobs."),
        ("brain drain phenomenon", "C1", "hiện tượng chảy máu chất xám", "the movement of skilled people to other countries", "Higher salaries abroad drive the brain drain phenomenon."),
        ("facilitate foreign investment", "C1", "tạo thuận lợi cho đầu tư nước ngoài", "to make it easier for overseas companies to invest", "Simple licensing rules facilitate foreign investment."),
        ("global supply chains", "C1", "chuỗi cung ứng toàn cầu", "the networks that move parts and goods around the world", "The pandemic exposed weaknesses in global supply chains."),
        ("worldwide mobility", "C1", "khả năng di chuyển khắp thế giới", "the ease with which people travel and move between countries", "Cheap flights have increased worldwide mobility."),
    ],
    "Science and research": [
        ("conduct scientific experiments", "B2", "tiến hành thí nghiệm khoa học", "to carry out tests in order to discover something", "Students conduct scientific experiments in the new laboratory."),
        ("breakthrough discoveries", "C1", "những phát hiện mang tính đột phá", "important new findings that change our understanding", "Breakthrough discoveries in medicine have saved millions of lives."),
        ("fund academic research", "C1", "tài trợ cho nghiên cứu học thuật", "to pay for studies carried out at universities", "Private companies increasingly fund academic research."),
        ("ethical considerations", "C1", "những cân nhắc về đạo đức", "questions of right and wrong that must be thought about", "Testing on animals raises ethical considerations."),
        ("commercialise scientific findings", "C1", "thương mại hóa kết quả nghiên cứu", "to turn research results into products that are sold", "Start-ups help universities commercialise scientific findings."),
        ("foster technological innovation", "C1", "thúc đẩy đổi mới công nghệ", "to encourage the creation of new technology", "Tax breaks foster technological innovation in small firms."),
        ("space exploration missions", "B2", "các sứ mệnh thám hiểm không gian", "journeys to study space, the moon or planets", "Space exploration missions cost billions of dollars."),
        ("rigorous scientific methodology", "C1", "phương pháp khoa học chặt chẽ", "careful and strict ways of doing research", "Reliable results depend on rigorous scientific methodology."),
        ("clinical trials", "B2", "thử nghiệm lâm sàng", "tests of new medicines or treatments on people", "The vaccine passed three stages of clinical trials."),
        ("advance scientific knowledge", "C1", "mở rộng tri thức khoa học", "to increase what science knows and understands", "Open data helps advance scientific knowledge."),
    ],
    "Economy and development": [
        ("stimulate economic growth", "C1", "kích thích tăng trưởng kinh tế", "to help an economy grow faster", "Lower interest rates can stimulate economic growth."),
        ("curb inflation rates", "C1", "kiềm chế lạm phát", "to stop prices rising too quickly", "The central bank acted to curb inflation rates."),
        ("foster entrepreneurship", "C1", "khuyến khích tinh thần khởi nghiệp", "to encourage people to start their own businesses", "Business incubators foster entrepreneurship among graduates."),
        ("attract foreign direct investment", "C1", "thu hút vốn đầu tư trực tiếp nước ngoài", "to bring overseas companies to build and invest locally", "Industrial parks attract foreign direct investment."),
        ("sustainable development", "B2", "phát triển bền vững", "growth that meets present needs without harming the future", "Sustainable development balances jobs and nature."),
        ("combat income inequality", "C1", "chống bất bình đẳng thu nhập", "to reduce the gap between rich and poor", "A higher minimum wage can combat income inequality."),
        ("boost domestic consumption", "C1", "kích cầu tiêu dùng trong nước", "to make people at home spend more", "Holiday bonuses boost domestic consumption."),
        ("alleviate financial strain", "C1", "giảm bớt gánh nặng tài chính", "to make money worries less severe", "Free school meals alleviate financial strain on poor families."),
        ("emerging market economies", "C1", "các nền kinh tế mới nổi", "fast-growing economies that are becoming more developed", "Investors are turning to emerging market economies in Asia."),
        ("create employment opportunities", "B2", "tạo ra việc làm", "to make new jobs available", "Tourism can create employment opportunities in rural areas."),
    ],
}

# Vietnamese names for the topics, which the app shows as "Collocation: <name>".
VI = {
    "Education": "Giáo dục", "Technology": "Công nghệ", "Environment": "Môi trường", "Health": "Sức khỏe",
    "Work": "Công việc", "Government and public services": "Chính phủ và dịch vụ công",
    "Crime and justice": "Tội phạm và công lý", "Media and advertising": "Truyền thông và quảng cáo",
    "Transport": "Giao thông", "Urban life and housing": "Đô thị và nhà ở", "Family and society": "Gia đình và xã hội",
    "Culture and traditions": "Văn hóa và truyền thống", "Globalisation": "Toàn cầu hóa",
    "Science and research": "Khoa học và nghiên cứu", "Economy and development": "Kinh tế và phát triển",
}


def main():
    out, seen = [], set()
    for theme, items in THEMES.items():
        assert len(items) == 10, theme
        for word, level, meaning, definition, example in items:
            assert word not in seen, word
            seen.add(word)
            assert word in example.lower(), word
            assert len(example.split()) >= 4 and len(definition.split()) >= 2, word
            out.append({
                "id": "v-col-" + re.sub(r"[^a-z]+", "-", word).strip("-"),
                "word": word,
                "ipa": "",
                "pos": "collocation",
                "meaning": meaning,
                "definition": definition,
                "examples": [example],
                "level": level,
                "topic": f"Writing: {theme}",
            })
    assert len(out) == 150 and len({w["id"] for w in out}) == 150
    path = pathlib.Path(__file__).resolve().parent.parent / "src" / "data" / "vocabulary-collocations.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    levels = {lv: sum(1 for x in out if x["level"] == lv) for lv in ["B1", "B2", "C1"]}
    print(f"{len(out)} collocations in {len(THEMES)} topics: {levels}")
    print("topics:", json.dumps({f"Writing: {t}": f"Collocation: {VI[t]}" for t in THEMES}, ensure_ascii=False))


if __name__ == "__main__":
    main()

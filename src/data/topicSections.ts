export const topicSections = [
  {
    id: 'everyday',
    vi: 'Hằng ngày',
    en: 'Everyday',
    topics: [
      'Daily life',
      'Travel',
      'Food',
      'Health',
      'Shopping',
      'People and family',
      'Home and furniture',
      'Fruit and vegetables',
      'Drinks and cooking',
      'Clothes and accessories',
      'Body and health',
      'Everyday verbs',
      'Common adjectives',
      'Places in town',
      'Time and calendar',
      'Nature and weather',
      'Animals',
      'Transport',
      'Hobbies and sport',
      'Money and shopping',
      'Essential expressions',
      'Numbers and colors',
    ],
  },
  {
    id: 'work',
    vi: 'Công việc & học tập',
    en: 'Work & study',
    topics: [
      'Work',
      'Technology',
      'Environment',
      'Education',
      'Communication',
      'School and language',
      'Ideas and relationships',
    ],
  },
  {
    id: 'specialist',
    vi: 'Chuyên ngành',
    en: 'Specialist',
    topics: [
      'Marketing: Strategy',
      'Marketing: Digital',
      'Economics: Macroeconomics',
      'Economics: Markets',
      'Finance: Investing',
      'Law: Contracts',
      'Healthcare: Clinical work',
      'Hospitality: Service',
      'IT: Programming',
      'IT: Web development',
      'IT: Databases',
      'IT: Networking',
      'IT: Security',
      'IT: Testing and deployment',
    ],
  },
  {
    id: 'exam',
    vi: 'Ôn thi nâng cao',
    en: 'Advanced exam',
    topics: [
      'Exam: Academic argument',
      'Exam: Evidence and research',
      'Exam: Society and policy',
      'Exam: Language and nuance',
    ],
  },
] as const;

export type TopicSectionId = (typeof topicSections)[number]['id'] | 'custom';
export function topicSectionFor(topic: string): TopicSectionId {
  return (
    topicSections.find((section) => (section.topics as readonly string[]).includes(topic))?.id ??
    'custom'
  );
}

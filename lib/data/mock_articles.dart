import '../models/article.dart';

final List<Article> mockArticles = [
  Article(
    id: 'a1',
    title: 'New AI tools are changing how developers build software',
    source: 'TechCrunch',
    topic: 'Artificial Intelligence',
    summary: 'A look at the latest AI tools and their impact on software engineering.',
    content: 'Full article content here...',
    publishedAt: DateTime.now().subtract(const Duration(hours: 2)),
    readingTime: 5,
  ),
  Article(
    id: 'a2',
    title: 'SpaceX successfully launches new satellite constellation',
    source: 'Wired',
    topic: 'Science',
    summary: 'The latest mission puts 60 new satellites into orbit.',
    content: 'Full article content here...',
    publishedAt: DateTime.now().subtract(const Duration(hours: 5)),
    readingTime: 4,
  ),
  Article(
    id: 'a3',
    title: 'Global markets rally as tech stocks surge',
    source: 'Bloomberg',
    topic: 'Business',
    summary: 'Technology companies lead the stock market to record highs.',
    content: 'Full article content here...',
    publishedAt: DateTime.now().subtract(const Duration(hours: 1)),
    readingTime: 3,
  ),
];

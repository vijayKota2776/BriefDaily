import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Fix Article model
article_model = """class Article {
  final String id;
  final String title;
  final String summary;
  final String content;
  final String source;
  final String topic;
  final String? author;
  final int readingTime;
  final String? imageUrl;
  final String? url;
  final DateTime publishedAt;

  Article({
    required this.id,
    required this.title,
    required this.summary,
    required this.content,
    required this.source,
    required this.topic,
    this.author,
    required this.readingTime,
    this.imageUrl,
    this.url,
    required this.publishedAt,
  });

  factory Article.fromJson(Map<String, dynamic> json, String topicName) {
    return Article(
      id: json['url'] ?? DateTime.now().toString(),
      title: json['title'] ?? 'No Title',
      summary: json['description'] ?? 'No summary available.',
      content: json['content'] ?? 'No content available.',
      source: json['source']?['name'] ?? 'Unknown Source',
      topic: topicName,
      author: json['author'],
      readingTime: ((json['content']?.length ?? 0) / 1000).ceil().clamp(1, 10).toInt(),
      imageUrl: json['urlToImage'],
      url: json['url'],
      publishedAt: json['publishedAt'] != null 
          ? DateTime.tryParse(json['publishedAt']) ?? DateTime.now() 
          : DateTime.now(),
    );
  }
}
"""
with open('lib/models/article.dart', 'w') as f:
    f.write(article_model)

# 2. Fix withOpacity
replace_in_file('lib/features/article/article_detail_screen.dart', '.withOpacity(0.2)', '.withValues(alpha: 0.2)')
replace_in_file('lib/features/article/article_detail_screen.dart', '.withOpacity(0.5)', '.withValues(alpha: 0.5)')
replace_in_file('lib/features/digest/widgets/article_card.dart', '.withOpacity(0.3)', '.withValues(alpha: 0.3)')
replace_in_file('lib/features/digest/widgets/article_card.dart', '.withOpacity(0.6)', '.withValues(alpha: 0.6)')

# 3. Fix braces in string interpolations
replace_in_file('lib/services/news_service.dart', 
    "final url = Uri.parse('${_baseUrl}/everything?q=${query}&language=en&sortBy=publishedAt&pageSize=10&apiKey=${_apiKey}');",
    "final url = Uri.parse('$_baseUrl/everything?q=$query&language=en&sortBy=publishedAt&pageSize=10&apiKey=$_apiKey');")

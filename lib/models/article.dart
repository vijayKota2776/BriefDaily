class Article {
  final String id;
  final String title;
  final String source;
  final String topic;
  final String? imageUrl;
  final String summary;
  final String content;
  final DateTime publishedAt;
  final String? author;
  final String? url;
  final int readingTime;

  const Article({
    required this.id,
    required this.title,
    required this.source,
    required this.topic,
    this.imageUrl,
    required this.summary,
    required this.content,
    required this.publishedAt,
    this.author,
    this.url,
    required this.readingTime,
  });
}

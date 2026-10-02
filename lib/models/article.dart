class Article {
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
      readingTime: ((json['content']?.length ?? 0) / 1000)
          .ceil()
          .clamp(1, 10)
          .toInt(),
      imageUrl: json['urlToImage'],
      url: json['url'],
      publishedAt: json['publishedAt'] != null
          ? DateTime.tryParse(json['publishedAt']) ?? DateTime.now()
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'summary': summary,
      'content': content,
      'source': source,
      'topic': topic,
      'author': author,
      'readingTime': readingTime,
      'imageUrl': imageUrl,
      'url': url,
      'publishedAt': publishedAt.toIso8601String(),
    };
  }

  factory Article.fromStore(Map<String, dynamic> json) {
    return Article(
      id: json['id'],
      title: json['title'],
      summary: json['summary'],
      content: json['content'],
      source: json['source'],
      topic: json['topic'],
      author: json['author'],
      readingTime: json['readingTime'],
      imageUrl: json['imageUrl'],
      url: json['url'],
      publishedAt: DateTime.parse(json['publishedAt']),
    );
  }
}

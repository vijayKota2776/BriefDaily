import 'package:flutter_test/flutter_test.dart';
import 'package:briefdaily/models/article.dart';

void main() {
  group('Article Model Tests', () {
    test('Article.fromJson creates valid Article', () {
      final json = {
        'title': 'Test Title',
        'description': 'Test Description',
        'content': 'Test Content',
        'url': 'https://example.com',
        'urlToImage': 'https://example.com/image.jpg',
        'publishedAt': '2023-10-01T12:00:00Z',
        'source': {'name': 'Test Source'},
      };

      final article = Article.fromJson(json, 'Technology');

      expect(article.title, 'Test Title');
      expect(article.summary, 'Test Description');
      expect(article.topic, 'Technology');
      expect(article.imageUrl, 'https://example.com/image.jpg');
      expect(article.source, 'Test Source');
    });

    test('Article readingTime calculation is correct', () {
      final content = 'Word ' * 6000; // 6000 chars roughly
      final json = {
        'title': 'Test Title',
        'content': content,
        'publishedAt': '2023-10-01T12:00:00Z',
      };
      
      final article = Article.fromJson(json, 'topic');

      // length is 30,000 / 1000 = 30, clamped to max 10
      expect(article.readingTime, 10);
    });
  });
}

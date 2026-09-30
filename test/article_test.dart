import 'package:flutter_test/flutter_test.dart';
import 'package:briefdaily/models/article.dart';

void main() {
  test('Article creation', () {
    final article = Article(
      id: '1',
      title: 'Test',
      source: 'Source',
      topic: 'Tech',
      summary: 'Summary',
      content: 'Content',
      publishedAt: DateTime(2023, 1, 1),
      readingTime: 5,
    );

    expect(article.id, '1');
    expect(article.title, 'Test');
  });
}

import 'package:flutter_test/flutter_test.dart';
import 'package:briefdaily/models/article.dart';

// Very basic test for sorting
void main() {
  test('Sort articles test', () {
    final a1 = Article(
      id: '1',
      title: 'Old',
      source: 'S',
      topic: 'T',
      summary: 'S',
      content: 'C',
      publishedAt: DateTime(2023, 1, 1),
      readingTime: 1,
    );
    final a2 = Article(
      id: '2',
      title: 'New',
      source: 'S',
      topic: 'T',
      summary: 'S',
      content: 'C',
      publishedAt: DateTime(2023, 1, 2),
      readingTime: 1,
    );

    var list = [a1, a2];
    list.sort((a, b) => b.publishedAt.compareTo(a.publishedAt));

    expect(list.first.id, '2');
  });
}

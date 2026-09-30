import '../../models/article.dart';
import '../mock_articles.dart';

class ArticleRepository {
  Future<List<Article>> getArticles() async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));
    return mockArticles;
  }
}

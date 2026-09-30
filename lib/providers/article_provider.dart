import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/article.dart';
import '../data/repositories/article_repository.dart';
import 'topic_provider.dart';

final articleRepositoryProvider = Provider<ArticleRepository>((ref) {
  return ArticleRepository();
});

final allArticlesProvider = FutureProvider<List<Article>>((ref) async {
  final repository = ref.watch(articleRepositoryProvider);
  return repository.getArticles();
});

final digestProvider = Provider<AsyncValue<List<Article>>>((ref) {
  final articlesAsync = ref.watch(allArticlesProvider);
  final selectedTopics = ref.watch(selectedTopicsProvider);

  return articlesAsync.whenData((articles) {
    List<Article> filtered = articles;
    if (selectedTopics.isNotEmpty) {
      filtered = articles
          .where((a) => selectedTopics.contains(a.topic))
          .toList();
    }
    // Sort by newest
    filtered.sort((a, b) => b.publishedAt.compareTo(a.publishedAt));
    return filtered;
  });
});

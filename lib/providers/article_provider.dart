import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/article.dart';
import '../services/news_service.dart';
import 'preferences_provider.dart';

final newsServiceProvider = Provider((ref) => NewsService());

final allArticlesProvider = FutureProvider<List<Article>>((ref) async {
  final prefs = ref.watch(preferencesProvider);
  final service = ref.read(newsServiceProvider);
  
  final topics = prefs.selectedTopics;
  if (topics.isEmpty) return [];

  return await service.fetchTopHeadlines(topics);
});

final digestProvider = FutureProvider<List<Article>>((ref) async {
  final allArticles = await ref.watch(allArticlesProvider.future);
  return allArticles;
});

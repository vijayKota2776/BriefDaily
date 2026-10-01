import os

# 1. Rewrite news_service.dart
news_service = """import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/article.dart';

class NewsService {
  static const String _apiKey = '96d4841970994aeca6abd3ea7663d8db';
  static const String _baseUrl = 'https://newsapi.org/v2';

  Future<List<Article>> fetchTopHeadlines(List<String> topics) async {
    List<Article> allArticles = [];

    if (topics.isEmpty) {
      topics = ['general'];
    }

    final targetTopics = topics.take(2).toList();

    try {
      for (var topic in targetTopics) {
        final query = topic.toLowerCase();
        final url = Uri.parse('$_baseUrl/everything?q=$query&language=en&sortBy=publishedAt&pageSize=10&apiKey=$_apiKey');
        final response = await http.get(url);

        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          final articles = data['articles'] as List;

          for (var articleJson in articles) {
            if (articleJson['title'] != '[Removed]') {
              allArticles.add(Article.fromJson(articleJson, topic));
            }
          }
        }
      }

      allArticles.shuffle();
      return allArticles;
    } catch (e) {
      return [];
    }
  }

  Future<List<Article>> searchArticles(String query) async {
    if (query.trim().isEmpty) return [];
    final url = Uri.parse('$_baseUrl/everything?q=$query&language=en&sortBy=publishedAt&pageSize=20&apiKey=$_apiKey');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        final List<dynamic> articlesJson = data['articles'];

        return articlesJson.map((json) => Article.fromJson(json, 'Search Result')).toList();
      } else {
        throw Exception('Failed to load search results');
      }
    } catch (e) {
      throw Exception('Failed to search: $e');
    }
  }
}
"""
with open('lib/services/news_service.dart', 'w') as f:
    f.write(news_service)


# 2. Rewrite article_provider.dart
article_provider = """import 'package:flutter_riverpod/flutter_riverpod.dart';
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

final searchProvider = FutureProvider.family<List<Article>, String>((ref, query) async {
  if (query.isEmpty) return [];
  final newsService = ref.read(newsServiceProvider);
  return newsService.searchArticles(query);
});

final digestProvider = FutureProvider<List<Article>>((ref) async {
  final allArticles = await ref.watch(allArticlesProvider.future);
  return allArticles;
});
"""
with open('lib/providers/article_provider.dart', 'w') as f:
    f.write(article_provider)


# 3. Fix router.dart
router_dart = """import 'package:flutter/material.dart';
import '../navigation/main_scaffold.dart';
import '../features/onboarding/welcome_screen.dart';
import '../features/onboarding/topic_selection_screen.dart';
import '../features/onboarding/personalization_screen.dart';
import '../features/article/article_detail_screen.dart';
import '../features/profile/edit_interests_screen.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const MainScaffold());
      case '/welcome':
        return MaterialPageRoute(builder: (_) => const WelcomeScreen());
      case '/topic_selection':
        return MaterialPageRoute(builder: (_) => const TopicSelectionScreen());
      case '/personalization':
        return MaterialPageRoute(builder: (_) => const PersonalizationScreen());
      case '/edit_interests':
        return MaterialPageRoute(builder: (_) => const EditInterestsScreen());
      case '/article':
        return MaterialPageRoute(
          builder: (_) => const ArticleDetailScreen(),
          settings: settings,
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for ${settings.name}')),
          ),
        );
    }
  }
}
"""
with open('lib/app/router.dart', 'w') as f:
    f.write(router_dart)


# 4. Add bookmarkedArticlesProvider to bookmark_provider.dart
bookmark_provider = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/repositories/bookmark_repository.dart';
import '../models/article.dart';
import 'article_provider.dart';

final bookmarkRepositoryProvider = Provider<BookmarkRepository>((ref) {
  return BookmarkRepository();
});

class BookmarkNotifier extends Notifier<List<String>> {
  @override
  List<String> build() {
    return ref.watch(bookmarkRepositoryProvider).getBookmarkedArticleIds();
  }

  Future<void> toggleBookmark(String articleId) async {
    final repository = ref.read(bookmarkRepositoryProvider);
    if (state.contains(articleId)) {
      await repository.removeBookmark(articleId);
      state = state.where((id) => id != articleId).toList();
    } else {
      await repository.addBookmark(articleId);
      state = [...state, articleId];
    }
  }
}

final bookmarkProvider = NotifierProvider<BookmarkNotifier, List<String>>(() {
  return BookmarkNotifier();
});

final bookmarkedArticlesProvider = Provider<List<Article>>((ref) {
  final bookmarkedIds = ref.watch(bookmarkProvider);
  final allArticlesAsync = ref.watch(allArticlesProvider);
  
  if (allArticlesAsync.hasValue) {
    return allArticlesAsync.value!.where((a) => bookmarkedIds.contains(a.id)).toList();
  }
  return [];
});
"""
with open('lib/providers/bookmark_provider.dart', 'w') as f:
    f.write(bookmark_provider)


# 5. Fix ArticleDetailScreen String interpolation warnings (L301)
def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file('lib/features/article/article_detail_screen.dart',
                'onPressed: () => _speak(article.title + ". " + article.summary + ". " + article.content),',
                "onPressed: () => _speak('${article.title}. ${article.summary}. ${article.content}'),")

print("Fixed errors")

import os
import subprocess

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

# 1. Update NewsService (API Key & Sorting)
news_service = read_file('lib/services/news_service.dart')
news_service = news_service.replace(
    "static const String _apiKey = '96d4841970994aeca6abd3ea7663d8db';",
    "static const String _apiKey = String.fromEnvironment('NEWS_API_KEY', defaultValue: '96d4841970994aeca6abd3ea7663d8db');"
)
news_service = news_service.replace(
    "allArticles.shuffle();",
    "allArticles.sort((a, b) => b.publishedAt.compareTo(a.publishedAt));"
)
write_file('lib/services/news_service.dart', news_service)

# 2. Update Article Model (toJson, fromStore)
article_code = read_file('lib/models/article.dart')
if 'toJson' not in article_code:
    insertion = """
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
"""
    article_code = article_code.replace('}\n', insertion)
    write_file('lib/models/article.dart', article_code)

# 3. Update BookmarkRepository to store JSON
repo_code = """import 'dart:convert';
import 'package:hive/hive.dart';
import '../../models/article.dart';

class BookmarkRepository {
  static const String _boxName = 'bookmarks';

  Future<void> init() async {
    await Hive.openBox<String>(_boxName);
  }

  List<Article> getBookmarkedArticles() {
    final box = Hive.box<String>(_boxName);
    return box.values.map((v) => Article.fromStore(json.decode(v))).toList();
  }

  Future<void> addBookmark(Article article) async {
    final box = Hive.box<String>(_boxName);
    await box.put(article.id, json.encode(article.toJson()));
  }

  Future<void> removeBookmark(String articleId) async {
    final box = Hive.box<String>(_boxName);
    if (box.containsKey(articleId)) {
      await box.delete(articleId);
    }
  }
}
"""
write_file('lib/data/repositories/bookmark_repository.dart', repo_code)

# 4. Update BookmarkProvider to use Article list
provider_code = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/repositories/bookmark_repository.dart';
import '../models/article.dart';

final bookmarkRepositoryProvider = Provider<BookmarkRepository>((ref) {
  return BookmarkRepository();
});

class BookmarkNotifier extends Notifier<List<Article>> {
  @override
  List<Article> build() {
    return ref.watch(bookmarkRepositoryProvider).getBookmarkedArticles();
  }

  Future<void> toggleBookmark(Article article) async {
    final repository = ref.read(bookmarkRepositoryProvider);
    final exists = state.any((a) => a.id == article.id);
    if (exists) {
      await repository.removeBookmark(article.id);
      state = state.where((a) => a.id != article.id).toList();
    } else {
      await repository.addBookmark(article);
      state = [...state, article];
    }
  }
}

final bookmarkProvider = NotifierProvider<BookmarkNotifier, List<Article>>(() {
  return BookmarkNotifier();
});

final bookmarkedArticlesProvider = Provider<List<Article>>((ref) {
  return ref.watch(bookmarkProvider);
});
"""
write_file('lib/providers/bookmark_provider.dart', provider_code)

# 5. Fix ArticleCard to pass entire article and show publish time
card_code = read_file('lib/features/digest/widgets/article_card.dart')
if "timeago" not in card_code:
    card_code = "import 'package:timeago/timeago.dart' as timeago;\n" + card_code

# Fix the toggleBookmark call to pass article instead of article.id
card_code = card_code.replace("toggleBookmark(article.id)", "toggleBookmark(article)")
# Fix isBookmarked check
card_code = card_code.replace(
    "final bookmarkedIds = ref.watch(bookmarkProvider);",
    "final bookmarkedArticles = ref.watch(bookmarkProvider);"
)
card_code = card_code.replace(
    "final isBookmarked = bookmarkedIds.contains(article.id);",
    "final isBookmarked = bookmarkedArticles.any((a) => a.id == article.id);"
)

# Add timeago string to the UI
card_code = card_code.replace(
    "Text(\n                    '${article.source} · ${article.readingTime} min',",
    "Text(\n                    '${article.source} · ${timeago.format(article.publishedAt)} · ${article.readingTime} min',"
)
write_file('lib/features/digest/widgets/article_card.dart', card_code)

detail_code = read_file('lib/features/article/article_detail_screen.dart')
detail_code = detail_code.replace(
    "final bookmarkedIds = ref.watch(bookmarkProvider);",
    "final bookmarkedArticles = ref.watch(bookmarkProvider);"
)
detail_code = detail_code.replace(
    "final isBookmarked = bookmarkedIds.contains(article.id);",
    "final isBookmarked = bookmarkedArticles.any((a) => a.id == article.id);"
)
detail_code = detail_code.replace("toggleBookmark(article.id)", "toggleBookmark(article)")
write_file('lib/features/digest/article_detail_screen.dart', detail_code)

b_card_code = read_file('lib/features/bookmarks/widgets/bookmark_card.dart')
if "timeago" not in b_card_code:
    b_card_code = "import 'package:timeago/timeago.dart' as timeago;\n" + b_card_code
b_card_code = b_card_code.replace(
    "final bookmarkedIds = ref.watch(bookmarkProvider);",
    "final bookmarkedArticles = ref.watch(bookmarkProvider);"
)
b_card_code = b_card_code.replace(
    "final isBookmarked = bookmarkedIds.contains(article.id);",
    "final isBookmarked = bookmarkedArticles.any((a) => a.id == article.id);"
)
b_card_code = b_card_code.replace("toggleBookmark(article.id)", "toggleBookmark(article)")
b_card_code = b_card_code.replace(
    "Text(\n                    '${article.source} · ${article.readingTime} min',",
    "Text(\n                    '${article.source} · ${timeago.format(article.publishedAt)} · ${article.readingTime} min',"
)
write_file('lib/features/bookmarks/widgets/bookmark_card.dart', b_card_code)

print("Audit script finished.")

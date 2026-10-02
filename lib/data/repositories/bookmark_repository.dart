import 'dart:convert';
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

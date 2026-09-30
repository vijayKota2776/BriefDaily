import 'package:hive/hive.dart';

class BookmarkRepository {
  static const String _boxName = 'bookmarks';

  Future<void> init() async {
    await Hive.openBox<String>(_boxName);
  }

  List<String> getBookmarkedArticleIds() {
    final box = Hive.box<String>(_boxName);
    return box.values.toList();
  }

  Future<void> addBookmark(String articleId) async {
    final box = Hive.box<String>(_boxName);
    if (!box.values.contains(articleId)) {
      await box.add(articleId);
    }
  }

  Future<void> removeBookmark(String articleId) async {
    final box = Hive.box<String>(_boxName);
    final key = box.keys.firstWhere(
      (k) => box.get(k) == articleId,
      orElse: () => null,
    );
    if (key != null) {
      await box.delete(key);
    }
  }
}

import 'package:flutter_riverpod/flutter_riverpod.dart';

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
    return allArticlesAsync.value!
        .where((a) => bookmarkedIds.contains(a.id))
        .toList();
  }
  return [];
});

import 'package:flutter_riverpod/flutter_riverpod.dart';

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

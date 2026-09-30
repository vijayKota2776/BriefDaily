import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/repositories/bookmark_repository.dart';

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

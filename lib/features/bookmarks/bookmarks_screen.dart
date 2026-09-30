import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../providers/bookmark_provider.dart';
import '../../providers/article_provider.dart';
import '../digest/widgets/article_card.dart';

class BookmarksScreen extends ConsumerWidget {
  const BookmarksScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bookmarkedIds = ref.watch(bookmarkProvider);
    final allArticlesAsync = ref.watch(allArticlesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Saved Stories')),
      body: allArticlesAsync.when(
        data: (articles) {
          final bookmarkedArticles = articles
              .where((a) => bookmarkedIds.contains(a.id))
              .toList();

          if (bookmarkedArticles.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('🔖', style: TextStyle(fontSize: 48)),
                  SizedBox(height: 16),
                  Text(
                    'Nothing saved yet',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Articles you bookmark\nwill appear here.',
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          }

          return ListView.builder(
            itemCount: bookmarkedArticles.length,
            itemBuilder: (context, index) {
              final article = bookmarkedArticles[index];
              return Dismissible(
                key: Key(article.id),
                direction: DismissDirection.endToStart,
                background: Container(
                  color: Colors.red,
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: 20),
                  child: const Icon(Icons.delete, color: Colors.white),
                ),
                onDismissed: (direction) {
                  ref
                      .read(bookmarkProvider.notifier)
                      .toggleBookmark(article.id);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: const Text('Bookmark removed'),
                      action: SnackBarAction(
                        label: 'UNDO',
                        onPressed: () {
                          ref
                              .read(bookmarkProvider.notifier)
                              .toggleBookmark(article.id);
                        },
                      ),
                    ),
                  );
                },
                child: ArticleCard(article: article),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }
}

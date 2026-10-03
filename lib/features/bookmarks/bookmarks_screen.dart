import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter/services.dart';

import '../../providers/bookmark_provider.dart';
import '../digest/widgets/article_card.dart';

class BookmarksScreen extends ConsumerWidget {
  const BookmarksScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bookmarkedArticles = ref.watch(bookmarkedArticlesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Saved Stories'), elevation: 0),
      body: bookmarkedArticles.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.bookmark_border,
                    size: 80,
                    color: Theme.of(context).colorScheme.primary
                        .withValues(alpha: 0.5),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Nothing saved yet',
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Articles you bookmark will appear here.',
                    style: Theme.of(context).textTheme.bodyLarge
                        ?.copyWith(color: Colors.grey),
                  ),
                ],
              ).animate().fadeIn(delay: 200.ms),
            )
          : ListView.builder(
              itemCount: bookmarkedArticles.length,
              itemBuilder: (context, index) {
                final article = bookmarkedArticles[index];
                return Dismissible(
                  key: Key(article.id),
                  background: Container(
                    color: Colors.red,
                    alignment: Alignment.centerRight,
                    padding: const EdgeInsets.only(right: 20.0),
                    child: const Icon(Icons.delete, color: Colors.white),
                  ),
                  direction: DismissDirection.endToStart,
                  onDismissed: (direction) {
                    HapticFeedback.lightImpact();
                    ref.read(bookmarkProvider.notifier).toggleBookmark(article);

                    ScaffoldMessenger.of(context).clearSnackBars();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: const Text('Bookmark removed'),
                        behavior: SnackBarBehavior.floating,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                        action: SnackBarAction(
                          label: 'UNDO',
                          onPressed: () {
                            ref
                                .read(bookmarkProvider.notifier)
                                .toggleBookmark(article);
                          },
                        ),
                      ),
                    );
                  },
                  child: ArticleCard(article: article)
                      .animate()
                      .fadeIn(duration: 400.ms, delay: (index * 100).ms)
                      .slideX(begin: 0.1),
                );
              },
            ),
    );
  }
}

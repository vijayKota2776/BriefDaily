import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../models/article.dart';
import '../../../providers/bookmark_provider.dart';
import '../../../app/theme/app_spacing.dart';

class ArticleCard extends ConsumerWidget {
  final Article article;

  const ArticleCard({super.key, required this.article});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bookmarkedIds = ref.watch(bookmarkProvider);
    final isBookmarked = bookmarkedIds.contains(article.id);

    return InkWell(
      onTap: () {
        Navigator.pushNamed(context, '/article', arguments: article);
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.s16,
          vertical: AppSpacing.s12,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(
                  article.topic.toUpperCase(),
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    color: Theme.of(context).colorScheme.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Spacer(),
                IconButton(
                  icon: Icon(
                    isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                  ),
                  color: isBookmarked
                      ? Theme.of(context).colorScheme.primary
                      : null,
                  onPressed: () {
                    ref
                        .read(bookmarkProvider.notifier)
                        .toggleBookmark(article.id);
                  },
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.s4),
            Text(article.title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: AppSpacing.s8),
            Row(
              children: [
                Text(
                  article.source,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Theme.of(context).colorScheme.onSurface
                        .withValues(alpha: 0.6),
                  ),
                ),
                const SizedBox(width: AppSpacing.s8),
                Text(
                  '·',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Theme.of(context).colorScheme.onSurface
                        .withValues(alpha: 0.6),
                  ),
                ),
                const SizedBox(width: AppSpacing.s8),
                Text(
                  '\${article.readingTime} min read',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Theme.of(context).colorScheme.onSurface
                        .withValues(alpha: 0.6),
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.s16),
            const Divider(),
          ],
        ),
      ),
    );
  }
}

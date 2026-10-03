import 'package:timeago/timeago.dart' as timeago;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cached_network_image/cached_network_image.dart';

import '../../../models/article.dart';
import '../../../providers/bookmark_provider.dart';
import '../../../providers/preferences_provider.dart';
import '../../../app/theme/app_spacing.dart';

class ArticleCard extends ConsumerWidget {
  final Article article;

  const ArticleCard({super.key, required this.article});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bookmarkedArticles = ref.watch(bookmarkProvider);
    final isBookmarked = bookmarkedArticles.any((a) => a.id == article.id);

    return InkWell(
      onTap: () {
        ref.read(preferencesProvider.notifier).recordArticleRead();
        Navigator.pushNamed(context, '/article', arguments: article);
      },
      child: Container(
        margin: const EdgeInsets.symmetric(
          horizontal: AppSpacing.s16,
          vertical: AppSpacing.s8,
        ),
        padding: const EdgeInsets.all(AppSpacing.s12),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          color: Theme.of(context).colorScheme.surfaceContainerHighest
              .withValues(alpha: 0.3),
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            if (article.imageUrl != null)
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: CachedNetworkImage(
                  imageUrl: article.imageUrl!,
                  height: 60,
                  width: 60,
                  fit: BoxFit.cover,
                  placeholder: (context, url) => Container(
                    height: 60,
                    width: 60,
                    color: Theme.of(context)
                        .colorScheme
                        .surfaceContainerHighest,
                  ),
                  errorWidget: (context, url, error) => Container(
                    height: 60,
                    width: 60,
                    color: Theme.of(context)
                        .colorScheme
                        .surfaceContainerHighest,
                    child: const Icon(Icons.broken_image, size: 24),
                  ),
                ),
              ),
            const SizedBox(width: AppSpacing.s16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    article.title,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: Theme.of(context).textTheme.titleSmall
                        ?.copyWith(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${article.source} · ${article.topic.toUpperCase()} · ${timeago.format(article.publishedAt)} · ${article.readingTime} min',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Theme.of(context).colorScheme.onSurface
                          .withValues(alpha: 0.6),
                    ),
                  ),
                ],
              ),
            ),
            IconButton(
              icon: Icon(
                isBookmarked ? Icons.favorite : Icons.favorite_border,
                size: 20,
              ),
              color: isBookmarked
                  ? Colors.red
                  : Theme.of(context).colorScheme.onSurface
                        .withValues(alpha: 0.6),
              onPressed: () {
                HapticFeedback.lightImpact();
                ref.read(bookmarkProvider.notifier).toggleBookmark(article);
              },
            ),
          ],
        ),
      ),
    );
  }
}

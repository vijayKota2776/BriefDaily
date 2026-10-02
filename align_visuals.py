import os

def update_file(filepath, callback):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}")
        return
    with open(filepath, 'r') as f:
        content = f.read()
    content = callback(content)
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Update article_card.dart to match Figma (small list tile)
article_card_code = """import 'package:flutter/material.dart';
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
    final bookmarkedIds = ref.watch(bookmarkProvider);
    final isBookmarked = bookmarkedIds.contains(article.id);

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
                    color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  ),
                  errorWidget: (context, url, error) => Container(
                    height: 60,
                    width: 60,
                    color: Theme.of(context).colorScheme.surfaceContainerHighest,
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
                    '${article.source} · ${article.readingTime} min',
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
              color: isBookmarked ? Colors.red : Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.6),
              onPressed: () {
                HapticFeedback.lightImpact();
                ref.read(bookmarkProvider.notifier).toggleBookmark(article.id);
              },
            ),
          ],
        ),
      ),
    );
  }
}
"""

with open('lib/features/digest/widgets/article_card.dart', 'w') as f:
    f.write(article_card_code)


# 2. Update bookmark icon everywhere else (like article_detail_screen)
def fix_bookmark_icons(content):
    content = content.replace("Icons.bookmark_border", "Icons.favorite_border")
    content = content.replace("Icons.bookmark", "Icons.favorite")
    return content

update_file('lib/features/digest/article_detail_screen.dart', fix_bookmark_icons)
update_file('lib/features/bookmarks/widgets/bookmark_card.dart', fix_bookmark_icons)

print("Visual alignment updated")

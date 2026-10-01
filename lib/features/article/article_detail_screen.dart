import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../../models/article.dart';
import '../../providers/bookmark_provider.dart';
import '../../app/theme/app_spacing.dart';

class ArticleDetailScreen extends ConsumerWidget {
  final Article article;

  const ArticleDetailScreen({super.key, required this.article});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bookmarkedIds = ref.watch(bookmarkProvider);
    final isBookmarked = bookmarkedIds.contains(article.id);

    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            icon: Icon(isBookmarked ? Icons.bookmark : Icons.bookmark_border),
            onPressed: () {
              ref.read(bookmarkProvider.notifier).toggleBookmark(article.id);
            },
          ),
          IconButton(icon: const Icon(Icons.share), onPressed: () {}),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppSpacing.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              article.topic.toUpperCase(),
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                color: Theme.of(context).colorScheme.primary,
                fontWeight: FontWeight.bold,
              ),
            ).animate().fadeIn().slideY(begin: -0.2),
            const SizedBox(height: AppSpacing.s8),
            Text(
              article.title,
              style: Theme.of(context).textTheme.headlineMedium,
            ).animate(delay: 100.ms).fadeIn().slideY(begin: 0.1),
            const SizedBox(height: AppSpacing.s16),
            Row(
              children: [
                const CircleAvatar(
                  radius: 16,
                  child: Icon(Icons.person, size: 16),
                ),
                const SizedBox(width: AppSpacing.s8),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      article.author ?? article.source,
                      style: Theme.of(context).textTheme.bodyMedium
                          ?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      '${article.readingTime} min read',
                      style: Theme.of(context).textTheme.labelSmall,
                    ),
                  ],
                ),
              ],
            ).animate(delay: 200.ms).fadeIn(),
            const SizedBox(height: AppSpacing.s24),
            Text(
              article.summary,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                fontWeight: FontWeight.w500,
                fontStyle: FontStyle.italic,
              ),
            ).animate(delay: 300.ms).fadeIn().slideY(begin: 0.1),
            const SizedBox(height: AppSpacing.s24),
            Text(
              article.content,
              style: Theme.of(context).textTheme.bodyLarge
                  ?.copyWith(height: 1.6),
            ).animate(delay: 400.ms).fadeIn(duration: 600.ms),
            const SizedBox(height: AppSpacing.s48),
          ],
        ),
      ),
    );
  }
}

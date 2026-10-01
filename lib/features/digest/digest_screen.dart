import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../../providers/article_provider.dart';
import '../../providers/preferences_provider.dart';
import 'widgets/article_card.dart';

class DigestScreen extends ConsumerWidget {
  const DigestScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final digestAsync = ref.watch(digestProvider);
    final prefs = ref.watch(preferencesProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Brief'),
        actions: [
          if (prefs.streakCount > 0)
            Padding(
              padding: const EdgeInsets.only(right: 8.0),
              child: Chip(
                avatar: const Text('🔥', style: TextStyle(fontSize: 14)),
                label: Text(
                  '${prefs.streakCount}',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                backgroundColor: Theme.of(context).colorScheme.primaryContainer
                    .withValues(alpha: 0.5),
                side: BorderSide.none,
              ),
            ),
          IconButton(icon: const Icon(Icons.search), onPressed: () {}),
        ],
      ),
      body: digestAsync.when(
        data: (articles) {
          if (articles.isEmpty) {
            return const Center(
              child: Text('No articles found for your topics.'),
            );
          }
          return RefreshIndicator(
            onRefresh: () async {
              // ignore: unused_result
              ref.refresh(allArticlesProvider);
            },
            child: ListView.builder(
              itemCount: articles.length,
              itemBuilder: (context, index) {
                final article = articles[index];
                return ArticleCard(article: article)
                    .animate()
                    .fadeIn(duration: 400.ms, delay: (index * 100).ms)
                    .slideX(
                      begin: 0.1,
                      duration: 400.ms,
                      curve: Curves.easeOutQuad,
                    );
              },
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }
}

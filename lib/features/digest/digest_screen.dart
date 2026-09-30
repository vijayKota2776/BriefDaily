import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../providers/article_provider.dart';
import 'widgets/article_card.dart';

class DigestScreen extends ConsumerWidget {
  const DigestScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final digestAsync = ref.watch(digestProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Brief'),
        actions: [IconButton(icon: const Icon(Icons.search), onPressed: () {})],
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
                return ArticleCard(article: article);
              },
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: \$err')),
      ),
    );
  }
}

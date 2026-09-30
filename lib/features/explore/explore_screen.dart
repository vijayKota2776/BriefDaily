import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../providers/article_provider.dart';
import '../../data/mock_topics.dart';
import '../digest/widgets/article_card.dart';
import '../../app/theme/app_spacing.dart';

class ExploreScreen extends ConsumerStatefulWidget {
  const ExploreScreen({super.key});

  @override
  ConsumerState<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends ConsumerState<ExploreScreen> {
  String _searchQuery = '';

  @override
  Widget build(BuildContext context) {
    final allArticlesAsync = ref.watch(allArticlesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Explore')),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(
            padding: const EdgeInsets.all(AppSpacing.s16),
            child: TextField(
              decoration: const InputDecoration(
                hintText: 'Search BriefDaily...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                setState(() {
                  _searchQuery = value;
                });
              },
            ),
          ),
          if (_searchQuery.isEmpty) ...[
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s16),
              child: Text(
                'Topics',
                style: Theme.of(context).textTheme.titleLarge,
              ),
            ),
            const SizedBox(height: AppSpacing.s16),
            Expanded(
              child: GridView.builder(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s16),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  childAspectRatio: 2.5,
                  crossAxisSpacing: AppSpacing.s8,
                  mainAxisSpacing: AppSpacing.s8,
                ),
                itemCount: mockTopics.length,
                itemBuilder: (context, index) {
                  final topic = mockTopics[index];
                  return Card(
                    elevation: 0,
                    color: Theme.of(context)
                        .colorScheme
                        .surfaceContainerHighest,
                    child: Center(
                      child: Text(
                        '${topic.icon} ${topic.name}',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                  );
                },
              ),
            ),
          ] else ...[
            Expanded(
              child: allArticlesAsync.when(
                data: (articles) {
                  final results = articles.where((a) {
                    final q = _searchQuery.toLowerCase();
                    return a.title.toLowerCase().contains(q) ||
                        a.summary.toLowerCase().contains(q);
                  }).toList();

                  if (results.isEmpty) {
                    return const Center(child: Text('No stories found'));
                  }

                  return ListView.builder(
                    itemCount: results.length,
                    itemBuilder: (context, index) =>
                        ArticleCard(article: results[index]),
                  );
                },
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, stack) => Center(child: Text('Error: $err')),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

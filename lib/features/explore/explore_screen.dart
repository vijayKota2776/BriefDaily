import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../../providers/article_provider.dart';
import '../digest/widgets/article_card.dart';

class ExploreScreen extends ConsumerStatefulWidget {
  const ExploreScreen({super.key});

  @override
  ConsumerState<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends ConsumerState<ExploreScreen> {
  String _searchQuery = '';
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Explore'), elevation: 0),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _controller,
              decoration: InputDecoration(
                hintText: 'Search the web for news...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _searchQuery.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _controller.clear();
                          setState(() {
                            _searchQuery = '';
                          });
                        },
                      )
                    : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(16),
                  borderSide: BorderSide.none,
                ),
                filled: true,
                fillColor: Theme.of(context).colorScheme.surfaceContainerHighest
                    .withValues(alpha: 0.5),
              ),
              onSubmitted: (value) {
                setState(() {
                  _searchQuery = value;
                });
              },
            ),
          ).animate().slideY(begin: -0.2).fadeIn(),

          Expanded(
            child: _searchQuery.isEmpty
                ? _buildEmptyState()
                : _buildSearchResults(),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.travel_explore,
            size: 80,
            color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.5),
          ),
          const SizedBox(height: 16),
          Text(
            'Discover Stories',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text(
            'Search for any topic worldwide.',
            style: Theme.of(context).textTheme.bodyLarge
                ?.copyWith(color: Colors.grey),
          ),
        ],
      ).animate().fadeIn(delay: 200.ms),
    );
  }

  Widget _buildSearchResults() {
    final searchAsync = ref.watch(searchProvider(_searchQuery));

    return searchAsync.when(
      data: (articles) {
        if (articles.isEmpty) {
          return const Center(child: Text('No stories found for this query.'));
        }
        return ListView.builder(
          itemCount: articles.length,
          itemBuilder: (context, index) {
            return ArticleCard(article: articles[index])
                .animate()
                .fadeIn(duration: 300.ms, delay: (index * 50).ms)
                .slideX(begin: 0.1);
          },
        );
      },
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Error: $err')),
    );
  }
}

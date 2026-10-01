import os

files = {
    'lib/features/onboarding/welcome_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../app/theme/app_spacing.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.s24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              Icon(
                Icons.article_outlined,
                size: 80,
                color: Theme.of(context).colorScheme.primary,
              ).animate()
                .scale(duration: 600.ms, curve: Curves.easeOutBack)
                .fadeIn(),
              const SizedBox(height: AppSpacing.s32),
              Text(
                'BriefDaily',
                style: Theme.of(context).textTheme.displayLarge,
                textAlign: TextAlign.center,
              ).animate(delay: 200.ms)
                .slideY(begin: 0.5, duration: 500.ms, curve: Curves.easeOutQuad)
                .fadeIn(),
              const SizedBox(height: AppSpacing.s16),
              Text(
                'Your news.\\nYour interests.\\nYour daily brief.',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.7),
                      fontWeight: FontWeight.normal,
                    ),
                textAlign: TextAlign.center,
              ).animate(delay: 400.ms)
                .slideY(begin: 0.5, duration: 500.ms, curve: Curves.easeOutQuad)
                .fadeIn(),
              const Spacer(),
              FilledButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/topic_selection');
                },
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: AppSpacing.s16),
                ),
                child: const Text('Get Started', style: TextStyle(fontSize: 18)),
              ).animate(delay: 600.ms)
                .fadeIn(duration: 500.ms)
                .scale(begin: const Offset(0.9, 0.9)),
              const SizedBox(height: AppSpacing.s24),
            ],
          ),
        ),
      ),
    );
  }
}
""",
    'lib/features/digest/digest_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
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
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {},
          )
        ],
      ),
      body: digestAsync.when(
        data: (articles) {
          if (articles.isEmpty) {
            return const Center(child: Text('No articles found for your topics.'));
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
                  .slideX(begin: 0.1, duration: 400.ms, curve: Curves.easeOutQuad);
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
""",
    'lib/features/explore/explore_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
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
      appBar: AppBar(
        title: const Text('Explore'),
      ),
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
              child: Text('Topics', style: Theme.of(context).textTheme.titleLarge)
                .animate().fadeIn().slideX(begin: -0.1),
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
                    color: Theme.of(context).colorScheme.surfaceContainerHighest,
                    child: Center(
                      child: Text('\${topic.icon} \${topic.name}', style: const TextStyle(fontWeight: FontWeight.bold)),
                    ),
                  )
                  .animate()
                  .fadeIn(duration: 400.ms, delay: (index * 50).ms)
                  .scale(begin: const Offset(0.8, 0.8), curve: Curves.easeOutBack);
                },
              ),
            ),
          ] else ...[
            Expanded(
              child: allArticlesAsync.when(
                data: (articles) {
                  final results = articles.where((a) {
                    final q = _searchQuery.toLowerCase();
                    return a.title.toLowerCase().contains(q) || a.summary.toLowerCase().contains(q);
                  }).toList();

                  if (results.isEmpty) {
                    return const Center(child: Text('No stories found'));
                  }

                  return ListView.builder(
                    itemCount: results.length,
                    itemBuilder: (context, index) => ArticleCard(article: results[index]),
                  );
                },
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, stack) => Center(child: Text('Error: \$err')),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
""",
    'lib/features/article/article_detail_screen.dart': """import 'package:flutter/material.dart';
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
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {},
          ),
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
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      '\${article.readingTime} min read',
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
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(height: 1.6),
            ).animate(delay: 400.ms).fadeIn(duration: 600.ms),
            const SizedBox(height: AppSpacing.s48),
          ],
        ),
      ),
    );
  }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

print("Phase 5 Files created.")

import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Update news_service.dart to add search
news_service_update = """
  Future<List<Article>> searchArticles(String query) async {
    final url = Uri.parse('$_baseUrl/everything?q=$query&language=en&sortBy=publishedAt&pageSize=20&apiKey=$_apiKey');
    
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);
      final List<dynamic> articlesJson = data['articles'];
      
      return articlesJson.map((json) => Article.fromJson(json, 'Search Result')).toList();
    } else {
      throw Exception('Failed to load search results');
    }
  }
}
"""
replace_in_file('lib/services/news_service.dart', '}\n', news_service_update)


# 2. Add searchProvider to article_provider.dart
article_provider_update = """
final searchProvider = FutureProvider.family<List<Article>, String>((ref, query) async {
  if (query.isEmpty) return [];
  final newsService = ref.read(newsServiceProvider);
  return newsService.searchArticles(query);
});
"""
replace_in_file('lib/providers/article_provider.dart', '});\n', '});\n' + article_provider_update)


# 3. Update ExploreScreen to use the new Live Search
explore_screen = """import 'package:flutter/material.dart';
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
      appBar: AppBar(
        title: const Text('Explore'),
        elevation: 0,
      ),
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
                fillColor: Theme.of(context).colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
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
          Icon(Icons.travel_explore, size: 80, color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.5)),
          const SizedBox(height: 16),
          Text('Discover Stories', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          Text('Search for any topic worldwide.', style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: Colors.grey)),
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
"""
with open('lib/features/explore/explore_screen.dart', 'w') as f:
    f.write(explore_screen)


# 4. Update ArticleDetailScreen to include Text-to-Speech
replace_in_file('lib/features/article/article_detail_screen.dart', 
                "import 'package:cached_network_image/cached_network_image.dart';",
                "import 'package:cached_network_image/cached_network_image.dart';\nimport 'package:flutter_tts/flutter_tts.dart';")

tts_code = """
class ArticleDetailScreen extends ConsumerStatefulWidget {
  const ArticleDetailScreen({super.key});

  @override
  ConsumerState<ArticleDetailScreen> createState() => _ArticleDetailScreenState();
}

class _ArticleDetailScreenState extends ConsumerState<ArticleDetailScreen> {
  final FlutterTts flutterTts = FlutterTts();
  bool isPlaying = false;
  
  @override
  void dispose() {
    flutterTts.stop();
    super.dispose();
  }

  Future<void> _speak(String text) async {
    if (isPlaying) {
      await flutterTts.stop();
      setState(() => isPlaying = false);
    } else {
      await flutterTts.setLanguage("en-US");
      await flutterTts.setSpeechRate(0.5);
      await flutterTts.setVolume(1.0);
      await flutterTts.setPitch(1.0);
      
      setState(() => isPlaying = true);
      
      flutterTts.setCompletionHandler(() {
        if (mounted) setState(() => isPlaying = false);
      });
      
      await flutterTts.speak(text);
    }
  }

  @override
  Widget build(BuildContext context) {
    final article = ModalRoute.of(context)!.settings.arguments as Article;
"""

# Replace the class definition in article_detail_screen
# I need to be careful with the replacement. It's better to just rewrite the whole file for safety.

article_detail_screen = """import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'dart:ui';
import '../../models/article.dart';
import '../../providers/bookmark_provider.dart';

class ArticleDetailScreen extends ConsumerStatefulWidget {
  const ArticleDetailScreen({super.key});

  @override
  ConsumerState<ArticleDetailScreen> createState() => _ArticleDetailScreenState();
}

class _ArticleDetailScreenState extends ConsumerState<ArticleDetailScreen> {
  final FlutterTts flutterTts = FlutterTts();
  bool isPlaying = false;
  
  @override
  void dispose() {
    flutterTts.stop();
    super.dispose();
  }

  Future<void> _speak(String text) async {
    if (isPlaying) {
      await flutterTts.stop();
      setState(() => isPlaying = false);
    } else {
      await flutterTts.setLanguage("en-US");
      await flutterTts.setSpeechRate(0.5);
      
      setState(() => isPlaying = true);
      
      flutterTts.setCompletionHandler(() {
        if (mounted) setState(() => isPlaying = false);
      });
      
      await flutterTts.speak(text);
    }
  }

  @override
  Widget build(BuildContext context) {
    final article = ModalRoute.of(context)!.settings.arguments as Article;
    final bookmarkedIds = ref.watch(bookmarkProvider);
    final isBookmarked = bookmarkedIds.contains(article.id);

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 350.0,
            floating: false,
            pinned: true,
            stretch: true,
            backgroundColor: Theme.of(context).colorScheme.surface,
            leading: Padding(
              padding: const EdgeInsets.all(8.0),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                  child: Container(
                    color: Theme.of(context).colorScheme.surface.withValues(alpha: 0.2),
                    child: IconButton(
                      icon: const Icon(Icons.arrow_back),
                      onPressed: () => Navigator.pop(context),
                    ),
                  ),
                ),
              ),
            ),
            actions: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                    child: Container(
                      color: Theme.of(context).colorScheme.surface.withValues(alpha: 0.2),
                      child: IconButton(
                        icon: Icon(isBookmarked ? Icons.bookmark : Icons.bookmark_border),
                        color: isBookmarked ? Theme.of(context).colorScheme.primary : null,
                        onPressed: () {
                          HapticFeedback.heavyImpact();
                          ref.read(bookmarkProvider.notifier).toggleBookmark(article.id);
                          if (!isBookmarked) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: const Text('Article saved to bookmarks!'),
                                behavior: SnackBarBehavior.floating,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                              ),
                            );
                          }
                        },
                      ),
                    ),
                  ),
                ),
              ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              stretchModes: const [StretchMode.zoomBackground],
              background: article.imageUrl != null
                  ? CachedNetworkImage(
                      imageUrl: article.imageUrl!,
                      fit: BoxFit.cover,
                    )
                  : Container(
                      color: Theme.of(context).colorScheme.primaryContainer,
                      child: const Icon(Icons.article, size: 100),
                    ),
            ),
          ),
          SliverToBoxAdapter(
            child: Container(
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surface,
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(32),
                  topRight: Radius.circular(32),
                ),
              ),
              transform: Matrix4.translationValues(0.0, -30.0, 0.0),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.primaryContainer,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            article.topic.toUpperCase(),
                            style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                  color: Theme.of(context).colorScheme.onPrimaryContainer,
                                  fontWeight: FontWeight.bold,
                                ),
                          ),
                        ),
                        const Spacer(),
                        Text(
                          '${article.readingTime} min read',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: Theme.of(context).colorScheme.onSurfaceVariant,
                              ),
                        ),
                      ],
                    ).animate().fadeIn(duration: 400.ms).slideY(begin: 0.2),
                    const SizedBox(height: 24),
                    Text(
                      article.title,
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontWeight: FontWeight.w900,
                            height: 1.2,
                          ),
                    ).animate().fadeIn(duration: 500.ms, delay: 100.ms).slideY(begin: 0.1),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        CircleAvatar(
                          backgroundColor: Theme.of(context).colorScheme.secondaryContainer,
                          child: Text(article.source[0]),
                        ),
                        const SizedBox(width: 12),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              article.source,
                              style: const TextStyle(fontWeight: FontWeight.bold),
                            ),
                            Text(
                              article.author ?? 'Unknown Author',
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                          ],
                        ),
                      ],
                    ).animate().fadeIn(duration: 500.ms, delay: 200.ms),
                    const SizedBox(height: 32),
                    
                    // AI Summary Section
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            Theme.of(context).colorScheme.primaryContainer.withValues(alpha: 0.5),
                            Theme.of(context).colorScheme.secondaryContainer.withValues(alpha: 0.3),
                          ],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(
                          color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.1),
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(Icons.auto_awesome, color: Theme.of(context).colorScheme.primary),
                              const SizedBox(width: 8),
                              Text('AI Summary', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Text(
                            article.summary,
                            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                              height: 1.5,
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ],
                      ),
                    ).animate().fadeIn(duration: 600.ms, delay: 300.ms).scale(begin: const Offset(0.95, 0.95)),
                    
                    const SizedBox(height: 32),
                    Text(
                      article.content,
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            height: 1.8,
                            fontSize: 18,
                          ),
                    ).animate().fadeIn(duration: 800.ms, delay: 400.ms),
                    const SizedBox(height: 100), // Padding for FAB
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _speak(article.title + ". " + article.summary + ". " + article.content),
        icon: Icon(isPlaying ? Icons.stop : Icons.volume_up),
        label: Text(isPlaying ? 'Stop' : 'Listen'),
      ).animate().scale(delay: 500.ms, duration: 300.ms),
    );
  }
}
"""
with open('lib/features/article/article_detail_screen.dart', 'w') as f:
    f.write(article_detail_screen)

print("Phase 8 done")

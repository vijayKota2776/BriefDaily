import os

files = {
    'lib/models/article.dart': """class Article {
  final String id;
  final String title;
  final String summary;
  final String content;
  final String source;
  final String topic;
  final String? author;
  final int readingTime;
  final String? imageUrl;
  final String? url;

  Article({
    required this.id,
    required this.title,
    required this.summary,
    required this.content,
    required this.source,
    required this.topic,
    this.author,
    required this.readingTime,
    this.imageUrl,
    this.url,
  });

  factory Article.fromJson(Map<String, dynamic> json, String topicName) {
    return Article(
      id: json['url'] ?? DateTime.now().toString(),
      title: json['title'] ?? 'No Title',
      summary: json['description'] ?? 'No summary available.',
      content: json['content'] ?? 'No content available.',
      source: json['source']?['name'] ?? 'Unknown Source',
      topic: topicName,
      author: json['author'],
      readingTime: ((json['content']?.length ?? 0) / 1000).ceil().clamp(1, 10).toInt(),
      imageUrl: json['urlToImage'],
      url: json['url'],
    );
  }
}
""",
    'lib/services/news_service.dart': """import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/article.dart';

class NewsService {
  static const String _apiKey = '96d4841970994aeca6abd3ea7663d8db';
  static const String _baseUrl = 'https://newsapi.org/v2';

  Future<List<Article>> fetchTopHeadlines(List<String> topics) async {
    List<Article> allArticles = [];
    
    if (topics.isEmpty) {
      topics = ['general'];
    }

    final targetTopics = topics.take(2).toList();

    try {
      for (var topic in targetTopics) {
        final query = topic.toLowerCase();
        final url = Uri.parse('${_baseUrl}/everything?q=${query}&language=en&sortBy=publishedAt&pageSize=10&apiKey=${_apiKey}');
        final response = await http.get(url);

        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          final articles = data['articles'] as List;
          
          for (var articleJson in articles) {
            if (articleJson['title'] != '[Removed]') {
              allArticles.add(Article.fromJson(articleJson, topic));
            }
          }
        }
      }
      
      allArticles.shuffle();
      return allArticles;
    } catch (e) {
      return [];
    }
  }
}
""",
    'lib/providers/article_provider.dart': """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/article.dart';
import '../services/news_service.dart';
import 'preferences_provider.dart';

final newsServiceProvider = Provider((ref) => NewsService());

final allArticlesProvider = FutureProvider<List<Article>>((ref) async {
  final prefs = ref.watch(preferencesProvider);
  final service = ref.read(newsServiceProvider);
  
  final topics = prefs.selectedTopics;
  if (topics.isEmpty) return [];

  return await service.fetchTopHeadlines(topics);
});

final digestProvider = FutureProvider<List<Article>>((ref) async {
  final allArticles = await ref.watch(allArticlesProvider.future);
  return allArticles;
});
""",
    'lib/features/digest/widgets/article_card.dart': """import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cached_network_image/cached_network_image.dart';
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
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: AppSpacing.s16, vertical: AppSpacing.s8),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          color: Theme.of(context).colorScheme.surfaceContainerHighest.withOpacity(0.3),
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (article.imageUrl != null)
              CachedNetworkImage(
                imageUrl: article.imageUrl!,
                height: 200,
                width: double.infinity,
                fit: BoxFit.cover,
                placeholder: (context, url) => Container(
                  height: 200,
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  child: const Center(child: CircularProgressIndicator()),
                ),
                errorWidget: (context, url, error) => Container(
                  height: 200,
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  child: const Icon(Icons.broken_image, size: 50),
                ),
              ),
            Padding(
              padding: const EdgeInsets.all(AppSpacing.s16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Theme.of(context).colorScheme.primaryContainer,
                          borderRadius: BorderRadius.circular(8),
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
                      IconButton(
                        icon: Icon(isBookmarked ? Icons.bookmark : Icons.bookmark_border),
                        color: isBookmarked ? Theme.of(context).colorScheme.primary : null,
                        onPressed: () {
                          HapticFeedback.lightImpact();
                          ref.read(bookmarkProvider.notifier).toggleBookmark(article.id);
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.s8),
                  Text(
                    article.title,
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: AppSpacing.s8),
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          article.source,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: Theme.of(context).colorScheme.onSurface.withOpacity(0.6),
                              ),
                        ),
                      ),
                      const SizedBox(width: AppSpacing.s8),
                      Text('·', style: TextStyle(color: Theme.of(context).colorScheme.onSurface.withOpacity(0.6))),
                      const SizedBox(width: AppSpacing.s8),
                      Text(
                        '${article.readingTime} min read',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              color: Theme.of(context).colorScheme.onSurface.withOpacity(0.6),
                            ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
""",
    'lib/features/article/article_detail_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'dart:ui';
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
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 300,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: article.imageUrl != null
                  ? CachedNetworkImage(
                      imageUrl: article.imageUrl!,
                      fit: BoxFit.cover,
                    )
                  : Container(color: Theme.of(context).colorScheme.surfaceContainerHighest),
            ),
            actions: [
              ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                  child: Container(
                    color: Colors.black.withOpacity(0.2),
                    child: IconButton(
                      icon: Icon(isBookmarked ? Icons.bookmark : Icons.bookmark_border, color: Colors.white),
                      onPressed: () {
                        ref.read(bookmarkProvider.notifier).toggleBookmark(article.id);
                      },
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                  child: Container(
                    color: Colors.black.withOpacity(0.2),
                    child: IconButton(
                      icon: const Icon(Icons.share, color: Colors.white),
                      onPressed: () {},
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 16),
            ],
          ),
          SliverToBoxAdapter(
            child: Padding(
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
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              article.author ?? article.source,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: Theme.of(context).textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold),
                            ),
                            Text(
                              '${article.readingTime} min read',
                              style: Theme.of(context).textTheme.labelSmall,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ).animate(delay: 200.ms).fadeIn(),
                  const SizedBox(height: AppSpacing.s24),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.secondaryContainer.withOpacity(0.5),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Theme.of(context).colorScheme.secondary.withOpacity(0.2)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.auto_awesome, size: 16, color: Theme.of(context).colorScheme.secondary),
                            const SizedBox(width: 8),
                            Text('AI Summary', style: TextStyle(fontWeight: FontWeight.bold, color: Theme.of(context).colorScheme.secondary)),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          article.summary,
                          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                                fontWeight: FontWeight.w500,
                              ),
                        ),
                      ],
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
          ),
        ],
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

print("Phase 6 Files created.")

import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Update user_preferences.dart
user_prefs = """enum ThemePreference { system, light, dark }

class UserPreferences {
  final bool onboardingCompleted;
  final List<String> selectedTopics;
  final ThemePreference themePreference;
  final int streakCount;
  final DateTime? lastReadDate;

  UserPreferences({
    this.onboardingCompleted = false,
    this.selectedTopics = const [],
    this.themePreference = ThemePreference.system,
    this.streakCount = 0,
    this.lastReadDate,
  });

  UserPreferences copyWith({
    bool? onboardingCompleted,
    List<String>? selectedTopics,
    ThemePreference? themePreference,
    int? streakCount,
    DateTime? lastReadDate,
  }) {
    return UserPreferences(
      onboardingCompleted: onboardingCompleted ?? this.onboardingCompleted,
      selectedTopics: selectedTopics ?? this.selectedTopics,
      themePreference: themePreference ?? this.themePreference,
      streakCount: streakCount ?? this.streakCount,
      lastReadDate: lastReadDate ?? this.lastReadDate,
    );
  }
}
"""
with open('lib/models/user_preferences.dart', 'w') as f:
    f.write(user_prefs)

# 2. Update preferences_provider.dart
prefs_provider = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../models/user_preferences.dart';

class PreferencesNotifier extends Notifier<UserPreferences> {
  late Box _box;

  @override
  UserPreferences build() {
    _box = Hive.box('preferencesBox');
    return _loadPreferences();
  }

  UserPreferences _loadPreferences() {
    final onboardingCompleted = _box.get('onboardingCompleted', defaultValue: false);
    final selectedTopics = List<String>.from(_box.get('selectedTopics', defaultValue: []));
    final themeString = _box.get('themePreference', defaultValue: 'system');
    final streakCount = _box.get('streakCount', defaultValue: 0);
    
    final lastReadDateString = _box.get('lastReadDate');
    DateTime? lastReadDate;
    if (lastReadDateString != null) {
      lastReadDate = DateTime.tryParse(lastReadDateString);
    }
    
    ThemePreference theme = ThemePreference.system;
    if (themeString == 'light') theme = ThemePreference.light;
    if (themeString == 'dark') theme = ThemePreference.dark;

    return UserPreferences(
      onboardingCompleted: onboardingCompleted,
      selectedTopics: selectedTopics,
      themePreference: theme,
      streakCount: streakCount,
      lastReadDate: lastReadDate,
    );
  }

  Future<void> completeOnboarding() async {
    await _box.put('onboardingCompleted', true);
    state = state.copyWith(onboardingCompleted: true);
  }

  Future<void> updateTopics(List<String> topics) async {
    await _box.put('selectedTopics', topics);
    state = state.copyWith(selectedTopics: topics);
  }

  Future<void> updateTheme(ThemePreference theme) async {
    await _box.put('themePreference', theme.name);
    state = state.copyWith(themePreference: theme);
  }
  
  Future<void> recordArticleRead() async {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    
    int newStreak = state.streakCount;
    DateTime? newLastRead = state.lastReadDate;

    if (newLastRead == null) {
      newStreak = 1;
    } else {
      final lastReadDay = DateTime(newLastRead.year, newLastRead.month, newLastRead.day);
      final difference = today.difference(lastReadDay).inDays;

      if (difference == 1) {
        // Read on consecutive day, increment streak
        newStreak += 1;
      } else if (difference > 1) {
        // Streak broken
        newStreak = 1;
      }
      // If difference == 0, they already read today, keep streak as is
    }

    await _box.put('streakCount', newStreak);
    await _box.put('lastReadDate', now.toIso8601String());
    state = state.copyWith(streakCount: newStreak, lastReadDate: now);
  }
}

final preferencesProvider = NotifierProvider<PreferencesNotifier, UserPreferences>(() {
  return PreferencesNotifier();
});
"""
with open('lib/providers/preferences_provider.dart', 'w') as f:
    f.write(prefs_provider)

# 3. Update digest_screen.dart (Add Streak to AppBar)
digest_screen = """import 'package:flutter/material.dart';
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
                label: Text('${prefs.streakCount}', style: const TextStyle(fontWeight: FontWeight.bold)),
                backgroundColor: Theme.of(context).colorScheme.primaryContainer.withValues(alpha: 0.5),
                side: BorderSide.none,
              ),
            ),
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
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }
}
"""
replace_in_file('lib/features/digest/digest_screen.dart', digest_screen, digest_screen) 
# wait, actually let's just write to it to ensure no mismatches
with open('lib/features/digest/digest_screen.dart', 'w') as f:
    f.write(digest_screen)


# 4. Update article_card.dart (Call recordArticleRead)
article_card = """import 'package:flutter/material.dart';
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
        margin: const EdgeInsets.symmetric(horizontal: AppSpacing.s16, vertical: AppSpacing.s8),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          color: Theme.of(context).colorScheme.surfaceContainerHighest.withValues(alpha: 0.3),
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
                                color: Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.6),
                              ),
                        ),
                      ),
                      const SizedBox(width: AppSpacing.s8),
                      Text('·', style: TextStyle(color: Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.6))),
                      const SizedBox(width: AppSpacing.s8),
                      Text(
                        '${article.readingTime} min read',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              color: Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.6),
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
"""
with open('lib/features/digest/widgets/article_card.dart', 'w') as f:
    f.write(article_card)

print("Phase 7 files created.")

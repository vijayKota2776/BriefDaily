import os

files = {
    'lib/features/bookmarks/bookmarks_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/bookmark_provider.dart';
import '../../providers/article_provider.dart';
import '../digest/widgets/article_card.dart';

class BookmarksScreen extends ConsumerWidget {
  const BookmarksScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bookmarkedIds = ref.watch(bookmarkProvider);
    final allArticlesAsync = ref.watch(allArticlesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Saved Stories')),
      body: allArticlesAsync.when(
        data: (articles) {
          final bookmarkedArticles = articles.where((a) => bookmarkedIds.contains(a.id)).toList();

          if (bookmarkedArticles.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('🔖', style: TextStyle(fontSize: 48)),
                  SizedBox(height: 16),
                  Text('Nothing saved yet', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Text('Articles you bookmark\\nwill appear here.', textAlign: TextAlign.center),
                ]
              )
            );
          }

          return ListView.builder(
            itemCount: bookmarkedArticles.length,
            itemBuilder: (context, index) {
              final article = bookmarkedArticles[index];
              return Dismissible(
                key: Key(article.id),
                direction: DismissDirection.endToStart,
                background: Container(
                  color: Colors.red,
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: 20),
                  child: const Icon(Icons.delete, color: Colors.white),
                ),
                onDismissed: (direction) {
                  ref.read(bookmarkProvider.notifier).toggleBookmark(article.id);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: const Text('Bookmark removed'),
                      action: SnackBarAction(
                        label: 'UNDO',
                        onPressed: () {
                          ref.read(bookmarkProvider.notifier).toggleBookmark(article.id);
                        },
                      ),
                    ),
                  );
                },
                child: ArticleCard(article: article),
              );
            },
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
              child: Text('Topics', style: Theme.of(context).textTheme.titleLarge),
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
    'lib/features/profile/profile_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/preferences_provider.dart';
import '../../models/user_preferences.dart';
import '../../app/theme/app_spacing.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final prefs = ref.watch(preferencesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Profile & Settings')),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.s16),
        children: [
          ListTile(
            leading: const Icon(Icons.interests),
            title: const Text('Edit Interests'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              Navigator.pushNamed(context, '/edit_interests');
            },
          ),
          const Divider(),
          const Padding(
            padding: EdgeInsets.symmetric(vertical: AppSpacing.s8, horizontal: AppSpacing.s16),
            child: Text('Appearance', style: TextStyle(fontWeight: FontWeight.bold)),
          ),
          RadioListTile<ThemePreference>(
            title: const Text('System Default'),
            value: ThemePreference.system,
            groupValue: prefs.themePreference,
            onChanged: (val) {
              if (val != null) ref.read(preferencesProvider.notifier).updateTheme(val);
            },
          ),
          RadioListTile<ThemePreference>(
            title: const Text('Light'),
            value: ThemePreference.light,
            groupValue: prefs.themePreference,
            onChanged: (val) {
              if (val != null) ref.read(preferencesProvider.notifier).updateTheme(val);
            },
          ),
          RadioListTile<ThemePreference>(
            title: const Text('Dark'),
            value: ThemePreference.dark,
            groupValue: prefs.themePreference,
            onChanged: (val) {
              if (val != null) ref.read(preferencesProvider.notifier).updateTheme(val);
            },
          ),
        ],
      ),
    );
  }
}
""",
    'lib/features/profile/edit_interests_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../app/theme/app_spacing.dart';
import '../../data/mock_topics.dart';
import '../../providers/preferences_provider.dart';

class EditInterestsScreen extends ConsumerStatefulWidget {
  const EditInterestsScreen({super.key});

  @override
  ConsumerState<EditInterestsScreen> createState() => _EditInterestsScreenState();
}

class _EditInterestsScreenState extends ConsumerState<EditInterestsScreen> {
  late Set<String> _selectedTopics;

  @override
  void initState() {
    super.initState();
    _selectedTopics = ref.read(preferencesProvider).selectedTopics.toSet();
  }

  void _toggleTopic(String topicName) {
    setState(() {
      if (_selectedTopics.contains(topicName)) {
        _selectedTopics.remove(topicName);
      } else {
        _selectedTopics.add(topicName);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Interests'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(AppSpacing.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Wrap(
                  spacing: AppSpacing.s8,
                  runSpacing: AppSpacing.s12,
                  children: mockTopics.map((topic) {
                    final isSelected = _selectedTopics.contains(topic.name);
                    return FilterChip(
                      label: Text('\${topic.icon} \${topic.name}'),
                      selected: isSelected,
                      onSelected: (_) => _toggleTopic(topic.name),
                      labelStyle: TextStyle(
                        color: isSelected 
                            ? Theme.of(context).colorScheme.onPrimary 
                            : Theme.of(context).colorScheme.onSurface,
                      ),
                      selectedColor: Theme.of(context).colorScheme.primary,
                      showCheckmark: false,
                    );
                  }).toList(),
                ),
              ),
            ),
            FilledButton(
              onPressed: () async {
                await ref.read(preferencesProvider.notifier).updateTopics(_selectedTopics.toList());
                if (context.mounted) {
                  Navigator.pop(context);
                }
              },
              style: FilledButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.s16),
              ),
              child: const Text('Save Changes', style: TextStyle(fontSize: 18)),
            ),
            const SizedBox(height: AppSpacing.s24),
          ],
        ),
      ),
    );
  }
}
""",
    'lib/navigation/main_scaffold.dart': """import 'package:flutter/material.dart';
import '../features/digest/digest_screen.dart';
import '../features/explore/explore_screen.dart';
import '../features/bookmarks/bookmarks_screen.dart';
import '../features/profile/profile_screen.dart';

class MainScaffold extends StatefulWidget {
  const MainScaffold({super.key});

  @override
  State<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const DigestScreen(),
    const ExploreScreen(),
    const BookmarksScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Digest',
          ),
          NavigationDestination(
            icon: Icon(Icons.explore_outlined),
            selectedIcon: Icon(Icons.explore),
            label: 'Explore',
          ),
          NavigationDestination(
            icon: Icon(Icons.bookmark_outline),
            selectedIcon: Icon(Icons.bookmark),
            label: 'Saved',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}
""",
    'lib/app/router.dart': """import 'package:flutter/material.dart';
import '../navigation/main_scaffold.dart';
import '../features/onboarding/welcome_screen.dart';
import '../features/onboarding/topic_selection_screen.dart';
import '../features/onboarding/personalization_screen.dart';
import '../features/article/article_detail_screen.dart';
import '../features/profile/edit_interests_screen.dart';
import '../models/article.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const MainScaffold());
      case '/welcome':
        return MaterialPageRoute(builder: (_) => const WelcomeScreen());
      case '/topic_selection':
        return MaterialPageRoute(builder: (_) => const TopicSelectionScreen());
      case '/personalization':
        return MaterialPageRoute(builder: (_) => const PersonalizationScreen());
      case '/edit_interests':
        return MaterialPageRoute(builder: (_) => const EditInterestsScreen());
      case '/article':
        final article = settings.arguments as Article;
        return MaterialPageRoute(builder: (_) => ArticleDetailScreen(article: article));
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for \${settings.name}')),
          ),
        );
    }
  }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

print("Phase 4 Files created.")

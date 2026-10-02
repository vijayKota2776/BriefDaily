import os
import subprocess

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Update MainScaffold to use NavigationRail on tablets
main_scaffold = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../features/digest/home_screen.dart';
import '../features/explore/explore_screen.dart';
import '../features/bookmarks/bookmarks_screen.dart';
import '../features/profile/profile_screen.dart';

class MainScaffold extends ConsumerStatefulWidget {
  const MainScaffold({super.key});

  @override
  ConsumerState<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends ConsumerState<MainScaffold> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeScreen(),
    ExploreScreen(),
    BookmarksScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final isTablet = MediaQuery.sizeOf(context).width > 600;

    return Scaffold(
      body: isTablet
          ? Row(
              children: [
                NavigationRail(
                  selectedIndex: _currentIndex,
                  onDestinationSelected: (index) {
                    setState(() {
                      _currentIndex = index;
                    });
                  },
                  labelType: NavigationRailLabelType.all,
                  destinations: const [
                    NavigationRailDestination(
                      icon: Icon(Icons.home_outlined),
                      selectedIcon: Icon(Icons.home),
                      label: Text('Digest'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.explore_outlined),
                      selectedIcon: Icon(Icons.explore),
                      label: Text('Explore'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.bookmark_outline),
                      selectedIcon: Icon(Icons.bookmark),
                      label: Text('Saved'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.person_outline),
                      selectedIcon: Icon(Icons.person),
                      label: Text('Profile'),
                    ),
                  ],
                ),
                const VerticalDivider(thickness: 1, width: 1),
                Expanded(child: _screens[_currentIndex]),
              ],
            )
          : _screens[_currentIndex],
      bottomNavigationBar: isTablet
          ? null
          : NavigationBar(
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
"""
with open('lib/navigation/main_scaffold.dart', 'w') as f:
    f.write(main_scaffold)


# 2. Add some automated tests for Phase 9
os.makedirs('test/models', exist_ok=True)
os.makedirs('test/providers', exist_ok=True)

article_test = """import 'package:flutter_test/flutter_test.dart';
import 'package:briefdaily/models/article.dart';

void main() {
  group('Article Model Tests', () {
    test('Article.fromJson creates valid Article', () {
      final json = {
        'title': 'Test Title',
        'description': 'Test Description',
        'content': 'Test Content',
        'url': 'https://example.com',
        'urlToImage': 'https://example.com/image.jpg',
        'publishedAt': '2023-10-01T12:00:00Z',
        'source': {'name': 'Test Source'},
      };

      final article = Article.fromJson(json, 'Technology');

      expect(article.title, 'Test Title');
      expect(article.summary, 'Test Description');
      expect(article.topic, 'Technology');
      expect(article.imageUrl, 'https://example.com/image.jpg');
      expect(article.publisher, 'Test Source');
    });

    test('Article readTime calculation is correct', () {
      final article = Article(
        id: '1',
        title: 'Title',
        summary: 'Summary',
        content: 'Word ' * 600, // 600 words
        imageUrl: 'url',
        url: 'url',
        publishedAt: DateTime.now(),
        publisher: 'publisher',
        topic: 'topic',
      );

      // 600 words / 200 words per minute = 3 minutes
      expect(article.readTimeMinutes, 3);
    });
  });
}
"""
with open('test/models/article_test.dart', 'w') as f:
    f.write(article_test)

user_prefs_test = """import 'package:flutter_test/flutter_test.dart';
import 'package:briefdaily/models/user_preferences.dart';

void main() {
  group('UserPreferences Model Tests', () {
    test('Default values are correct', () {
      final prefs = UserPreferences();

      expect(prefs.onboardingCompleted, false);
      expect(prefs.isAuthenticated, false);
      expect(prefs.selectedTopics, isEmpty);
      expect(prefs.themePreference, ThemePreference.system);
      expect(prefs.streakCount, 0);
    });

    test('copyWith updates fields', () {
      final prefs = UserPreferences().copyWith(
        onboardingCompleted: true,
        streakCount: 5,
        themePreference: ThemePreference.dark,
      );

      expect(prefs.onboardingCompleted, true);
      expect(prefs.streakCount, 5);
      expect(prefs.themePreference, ThemePreference.dark);
      expect(prefs.isAuthenticated, false); // Unchanged
    });
  });
}
"""
with open('test/models/user_preferences_test.dart', 'w') as f:
    f.write(user_prefs_test)

print("Tablet UI and Phase 9 Tests created.")

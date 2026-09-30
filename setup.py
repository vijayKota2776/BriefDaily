import os

files = {
    'lib/app/theme/app_colors.dart': """import 'package:flutter/material.dart';

class AppColors {
  static const Color lightBackground = Color(0xFFF9F9F9);
  static const Color lightSurface = Colors.white;
  static const Color lightPrimary = Color(0xFF0F2C59);
  static const Color lightText = Color(0xFF1E1E1E);
  static const Color lightSecondaryText = Color(0xFF757575);

  static const Color darkBackground = Color(0xFF121212);
  static const Color darkSurface = Color(0xFF1E1E1E);
  static const Color darkPrimary = Color(0xFF4A90E2);
  static const Color darkText = Color(0xFFF5F5F5);
  static const Color darkSecondaryText = Color(0xFFAAAAAA);
}
""",
    'lib/app/theme/app_typography.dart': """import 'package:flutter/material.dart';

class AppTypography {
  static const String fontFamily = 'Roboto';

  static const TextTheme lightTextTheme = TextTheme(
    displayLarge: TextStyle(fontFamily: fontFamily, fontSize: 32, fontWeight: FontWeight.bold, color: Colors.black87),
    headlineMedium: TextStyle(fontFamily: fontFamily, fontSize: 24, fontWeight: FontWeight.w700, color: Colors.black87),
    titleLarge: TextStyle(fontFamily: fontFamily, fontSize: 20, fontWeight: FontWeight.w600, color: Colors.black87),
    bodyLarge: TextStyle(fontFamily: fontFamily, fontSize: 16, fontWeight: FontWeight.normal, color: Colors.black87),
    bodyMedium: TextStyle(fontFamily: fontFamily, fontSize: 14, fontWeight: FontWeight.normal, color: Colors.black87),
    labelSmall: TextStyle(fontFamily: fontFamily, fontSize: 12, fontWeight: FontWeight.w500, color: Colors.black54),
  );

  static const TextTheme darkTextTheme = TextTheme(
    displayLarge: TextStyle(fontFamily: fontFamily, fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
    headlineMedium: TextStyle(fontFamily: fontFamily, fontSize: 24, fontWeight: FontWeight.w700, color: Colors.white),
    titleLarge: TextStyle(fontFamily: fontFamily, fontSize: 20, fontWeight: FontWeight.w600, color: Colors.white),
    bodyLarge: TextStyle(fontFamily: fontFamily, fontSize: 16, fontWeight: FontWeight.normal, color: Colors.white),
    bodyMedium: TextStyle(fontFamily: fontFamily, fontSize: 14, fontWeight: FontWeight.normal, color: Colors.white70),
    labelSmall: TextStyle(fontFamily: fontFamily, fontSize: 12, fontWeight: FontWeight.w500, color: Colors.white54),
  );
}
""",
    'lib/app/theme/app_spacing.dart': """class AppSpacing {
  static const double s4 = 4.0;
  static const double s8 = 8.0;
  static const double s12 = 12.0;
  static const double s16 = 16.0;
  static const double s20 = 20.0;
  static const double s24 = 24.0;
  static const double s32 = 32.0;
  static const double s40 = 40.0;
  static const double s48 = 48.0;
}
""",
    'lib/app/theme/app_theme.dart': """import 'package:flutter/material.dart';
import 'app_colors.dart';
import 'app_typography.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: const ColorScheme.light(
        primary: AppColors.lightPrimary,
        surface: AppColors.lightSurface,
        onSurface: AppColors.lightText,
      ).copyWith(surface: AppColors.lightBackground),
      scaffoldBackgroundColor: AppColors.lightBackground,
      textTheme: AppTypography.lightTextTheme,
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.lightSurface,
        foregroundColor: AppColors.lightText,
        elevation: 0,
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.darkPrimary,
        surface: AppColors.darkSurface,
        onSurface: AppColors.darkText,
      ).copyWith(surface: AppColors.darkBackground),
      scaffoldBackgroundColor: AppColors.darkBackground,
      textTheme: AppTypography.darkTextTheme,
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.darkSurface,
        foregroundColor: AppColors.darkText,
        elevation: 0,
      ),
    );
  }
}
""",
    'lib/models/article.dart': """class Article {
  final String id;
  final String title;
  final String source;
  final String topic;
  final String? imageUrl;
  final String summary;
  final String content;
  final DateTime publishedAt;
  final String? author;
  final String? url;
  final int readingTime;

  const Article({
    required this.id,
    required this.title,
    required this.source,
    required this.topic,
    this.imageUrl,
    required this.summary,
    required this.content,
    required this.publishedAt,
    this.author,
    this.url,
    required this.readingTime,
  });
}
""",
    'lib/models/topic.dart': """class Topic {
  final String id;
  final String name;
  final String icon;

  const Topic({
    required this.id,
    required this.name,
    required this.icon,
  });
}
""",
    'lib/models/user_preferences.dart': """enum ThemePreference { system, light, dark }

class UserPreferences {
  final List<String> selectedTopics;
  final ThemePreference themePreference;
  final bool onboardingCompleted;

  const UserPreferences({
    this.selectedTopics = const [],
    this.themePreference = ThemePreference.system,
    this.onboardingCompleted = false,
  });

  UserPreferences copyWith({
    List<String>? selectedTopics,
    ThemePreference? themePreference,
    bool? onboardingCompleted,
  }) {
    return UserPreferences(
      selectedTopics: selectedTopics ?? this.selectedTopics,
      themePreference: themePreference ?? this.themePreference,
      onboardingCompleted: onboardingCompleted ?? this.onboardingCompleted,
    );
  }
}
""",
    'lib/data/mock_topics.dart': """import '../models/topic.dart';

const List<Topic> mockTopics = [
  Topic(id: '1', name: 'Technology', icon: '💻'),
  Topic(id: '2', name: 'Artificial Intelligence', icon: '🤖'),
  Topic(id: '3', name: 'Startups', icon: '🚀'),
  Topic(id: '4', name: 'Business', icon: '💼'),
  Topic(id: '5', name: 'Science', icon: '🔬'),
  Topic(id: '6', name: 'Sports', icon: '⚽'),
  Topic(id: '7', name: 'World', icon: '🌍'),
];
""",
    'lib/data/mock_articles.dart': """import '../models/article.dart';

final List<Article> mockArticles = [
  Article(
    id: 'a1',
    title: 'New AI tools are changing how developers build software',
    source: 'TechCrunch',
    topic: 'Artificial Intelligence',
    summary: 'A look at the latest AI tools and their impact on software engineering.',
    content: 'Full article content here...',
    publishedAt: DateTime.now().subtract(const Duration(hours: 2)),
    readingTime: 5,
  ),
  Article(
    id: 'a2',
    title: 'SpaceX successfully launches new satellite constellation',
    source: 'Wired',
    topic: 'Science',
    summary: 'The latest mission puts 60 new satellites into orbit.',
    content: 'Full article content here...',
    publishedAt: DateTime.now().subtract(const Duration(hours: 5)),
    readingTime: 4,
  ),
  Article(
    id: 'a3',
    title: 'Global markets rally as tech stocks surge',
    source: 'Bloomberg',
    topic: 'Business',
    summary: 'Technology companies lead the stock market to record highs.',
    content: 'Full article content here...',
    publishedAt: DateTime.now().subtract(const Duration(hours: 1)),
    readingTime: 3,
  ),
];
""",
    'lib/data/repositories/article_repository.dart': """import '../../models/article.dart';
import '../mock_articles.dart';

class ArticleRepository {
  Future<List<Article>> getArticles() async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));
    return mockArticles;
  }
}
""",
    'lib/data/repositories/bookmark_repository.dart': """import 'package:hive/hive.dart';

class BookmarkRepository {
  static const String _boxName = 'bookmarks';
  
  Future<void> init() async {
    await Hive.openBox<String>(_boxName);
  }

  List<String> getBookmarkedArticleIds() {
    final box = Hive.box<String>(_boxName);
    return box.values.toList();
  }

  Future<void> addBookmark(String articleId) async {
    final box = Hive.box<String>(_boxName);
    if (!box.values.contains(articleId)) {
      await box.add(articleId);
    }
  }

  Future<void> removeBookmark(String articleId) async {
    final box = Hive.box<String>(_boxName);
    final key = box.keys.firstWhere((k) => box.get(k) == articleId, orElse: () => null);
    if (key != null) {
      await box.delete(key);
    }
  }
}
""",
    'lib/data/repositories/preferences_repository.dart': """import 'package:hive/hive.dart';
import '../../models/user_preferences.dart';

class PreferencesRepository {
  static const String _boxName = 'preferences';
  static const String _topicsKey = 'selected_topics';
  static const String _themeKey = 'theme_preference';

  Future<void> init() async {
    await Hive.openBox(_boxName);
  }

  UserPreferences getPreferences() {
    final box = Hive.box(_boxName);
    final topics = box.get(_topicsKey, defaultValue: <String>[]) as List<dynamic>;
    final themeIndex = box.get(_themeKey, defaultValue: ThemePreference.system.index) as int;
    
    return UserPreferences(
      selectedTopics: topics.cast<String>(),
      themePreference: ThemePreference.values[themeIndex],
    );
  }

  Future<void> savePreferences(UserPreferences prefs) async {
    final box = Hive.box(_boxName);
    await box.put(_topicsKey, prefs.selectedTopics);
    await box.put(_themeKey, prefs.themePreference.index);
  }
}
""",
    'lib/providers/theme_provider.dart': """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/material.dart';
import '../models/user_preferences.dart';
import 'preferences_provider.dart';

final themeProvider = Provider<ThemeMode>((ref) {
  final prefs = ref.watch(preferencesProvider);
  switch (prefs.themePreference) {
    case ThemePreference.light:
      return ThemeMode.light;
    case ThemePreference.dark:
      return ThemeMode.dark;
    case ThemePreference.system:
    default:
      return ThemeMode.system;
  }
});
""",
    'lib/providers/preferences_provider.dart': """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user_preferences.dart';
import '../data/repositories/preferences_repository.dart';

final preferencesRepositoryProvider = Provider<PreferencesRepository>((ref) {
  return PreferencesRepository();
});

class PreferencesNotifier extends StateNotifier<UserPreferences> {
  final PreferencesRepository _repository;

  PreferencesNotifier(this._repository) : super(_repository.getPreferences());

  Future<void> updateTopics(List<String> topics) async {
    state = state.copyWith(selectedTopics: topics);
    await _repository.savePreferences(state);
  }

  Future<void> updateTheme(ThemePreference theme) async {
    state = state.copyWith(themePreference: theme);
    await _repository.savePreferences(state);
  }
}

final preferencesProvider = StateNotifierProvider<PreferencesNotifier, UserPreferences>((ref) {
  return PreferencesNotifier(ref.watch(preferencesRepositoryProvider));
});
""",
    'lib/providers/topic_provider.dart': """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'preferences_provider.dart';

final selectedTopicsProvider = Provider<List<String>>((ref) {
  return ref.watch(preferencesProvider).selectedTopics;
});
""",
    'lib/providers/article_provider.dart': """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/article.dart';
import '../data/repositories/article_repository.dart';
import 'topic_provider.dart';

final articleRepositoryProvider = Provider<ArticleRepository>((ref) {
  return ArticleRepository();
});

final allArticlesProvider = FutureProvider<List<Article>>((ref) async {
  final repository = ref.watch(articleRepositoryProvider);
  return repository.getArticles();
});

final digestProvider = Provider<AsyncValue<List<Article>>>((ref) {
  final articlesAsync = ref.watch(allArticlesProvider);
  final selectedTopics = ref.watch(selectedTopicsProvider);

  return articlesAsync.whenData((articles) {
    List<Article> filtered = articles;
    if (selectedTopics.isNotEmpty) {
      filtered = articles.where((a) => selectedTopics.contains(a.topic)).toList();
    }
    // Sort by newest
    filtered.sort((a, b) => b.publishedAt.compareTo(a.publishedAt));
    return filtered;
  });
});
""",
    'lib/providers/bookmark_provider.dart': """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/repositories/bookmark_repository.dart';

final bookmarkRepositoryProvider = Provider<BookmarkRepository>((ref) {
  return BookmarkRepository();
});

class BookmarkNotifier extends StateNotifier<List<String>> {
  final BookmarkRepository _repository;

  BookmarkNotifier(this._repository) : super(_repository.getBookmarkedArticleIds());

  Future<void> toggleBookmark(String articleId) async {
    if (state.contains(articleId)) {
      await _repository.removeBookmark(articleId);
      state = state.where((id) => id != articleId).toList();
    } else {
      await _repository.addBookmark(articleId);
      state = [...state, articleId];
    }
  }
}

final bookmarkProvider = StateNotifierProvider<BookmarkNotifier, List<String>>((ref) {
  return BookmarkNotifier(ref.watch(bookmarkRepositoryProvider));
});
""",
    'lib/app/router.dart': """import 'package:flutter/material.dart';
import '../features/digest/digest_shell.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const DigestShell());
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for ${settings.name}')),
          ),
        );
    }
  }
}
""",
    'lib/features/digest/digest_shell.dart': """import 'package:flutter/material.dart';
import '../../app/theme/app_spacing.dart';

class DigestShell extends StatelessWidget {
  const DigestShell({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('BriefDaily'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Your news.',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: AppSpacing.s8),
            Text(
              'Your interests.',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: AppSpacing.s8),
            Text(
              'Your daily brief.',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: AppSpacing.s32),
            Text(
              'Foundation initialized successfully.',
              style: Theme.of(context).textTheme.bodyLarge,
            ),
          ],
        ),
      ),
    );
  }
}
""",
    'lib/app/app.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'theme/app_theme.dart';
import 'router.dart';
import '../providers/theme_provider.dart';

class BriefDailyApp extends ConsumerWidget {
  const BriefDailyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeProvider);

    return MaterialApp(
      title: 'BriefDaily',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      initialRoute: '/',
      onGenerateRoute: AppRouter.generateRoute,
      debugShowCheckedModeBanner: false,
    );
  }
}
""",
    'lib/main.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'app/app.dart';
import 'data/repositories/bookmark_repository.dart';
import 'data/repositories/preferences_repository.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  try {
    await Hive.initFlutter();
    
    // Initialize repositories
    final prefsRepo = PreferencesRepository();
    await prefsRepo.init();
    
    final bookmarkRepo = BookmarkRepository();
    await bookmarkRepo.init();

    runApp(
      const ProviderScope(
        child: BriefDailyApp(),
      ),
    );
  } catch (e) {
    runApp(
      MaterialApp(
        home: Scaffold(
          body: Center(
            child: Text('Initialization failed: \$e'),
          ),
        ),
      )
    );
  }
}
""",
    'test/article_test.dart': """import 'package:flutter_test/flutter_test.dart';
import 'package:briefdaily/models/article.dart';

void main() {
  test('Article creation', () {
    final article = Article(
      id: '1',
      title: 'Test',
      source: 'Source',
      topic: 'Tech',
      summary: 'Summary',
      content: 'Content',
      publishedAt: DateTime(2023, 1, 1),
      readingTime: 5,
    );

    expect(article.id, '1');
    expect(article.title, 'Test');
  });
}
""",
    'test/digest_provider_test.dart': """import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:briefdaily/models/article.dart';
import 'package:briefdaily/providers/article_provider.dart';
import 'package:briefdaily/providers/topic_provider.dart';

// Very basic test for sorting
void main() {
  test('Sort articles test', () {
    final a1 = Article(id: '1', title: 'Old', source: 'S', topic: 'T', summary: 'S', content: 'C', publishedAt: DateTime(2023, 1, 1), readingTime: 1);
    final a2 = Article(id: '2', title: 'New', source: 'S', topic: 'T', summary: 'S', content: 'C', publishedAt: DateTime(2023, 1, 2), readingTime: 1);

    var list = [a1, a2];
    list.sort((a, b) => b.publishedAt.compareTo(a.publishedAt));

    expect(list.first.id, '2');
  });
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

print("Files created.")

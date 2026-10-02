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
  final bool isAuthenticated;
  final List<String> selectedTopics;
  final ThemePreference themePreference;
  final int streakCount;
  final DateTime? lastReadDate;

  UserPreferences({
    this.onboardingCompleted = false,
    this.isAuthenticated = false,
    this.selectedTopics = const [],
    this.themePreference = ThemePreference.system,
    this.streakCount = 0,
    this.lastReadDate,
  });

  UserPreferences copyWith({
    bool? onboardingCompleted,
    bool? isAuthenticated,
    List<String>? selectedTopics,
    ThemePreference? themePreference,
    int? streakCount,
    DateTime? lastReadDate,
  }) {
    return UserPreferences(
      onboardingCompleted: onboardingCompleted ?? this.onboardingCompleted,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
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

# 2. Update preferences_repository.dart
prefs_repo = """import 'package:hive/hive.dart';
import '../../models/user_preferences.dart';

class PreferencesRepository {
  static const String _boxName = 'preferences';
  static const String _topicsKey = 'selected_topics';
  static const String _themeKey = 'theme_preference';
  static const String _onboardingKey = 'onboarding_completed';
  static const String _authKey = 'is_authenticated';
  static const String _streakKey = 'streak_count';
  static const String _lastReadKey = 'last_read_date';

  Future<void> init() async {
    await Hive.openBox(_boxName);
  }

  UserPreferences getPreferences() {
    final box = Hive.box(_boxName);
    final topics = box.get(_topicsKey, defaultValue: <String>[]) as List<dynamic>;
    final themeIndex = box.get(_themeKey, defaultValue: ThemePreference.system.index) as int;
    final onboardingCompleted = box.get(_onboardingKey, defaultValue: false) as bool;
    final isAuthenticated = box.get(_authKey, defaultValue: false) as bool;
    final streakCount = box.get(_streakKey, defaultValue: 0) as int;
    final lastReadString = box.get(_lastReadKey) as String?;
    
    DateTime? lastReadDate;
    if (lastReadString != null) {
      lastReadDate = DateTime.tryParse(lastReadString);
    }

    return UserPreferences(
      selectedTopics: topics.cast<String>(),
      themePreference: ThemePreference.values[themeIndex],
      onboardingCompleted: onboardingCompleted,
      isAuthenticated: isAuthenticated,
      streakCount: streakCount,
      lastReadDate: lastReadDate,
    );
  }

  Future<void> savePreferences(UserPreferences prefs) async {
    final box = Hive.box(_boxName);
    await box.put(_topicsKey, prefs.selectedTopics);
    await box.put(_themeKey, prefs.themePreference.index);
    await box.put(_onboardingKey, prefs.onboardingCompleted);
    await box.put(_authKey, prefs.isAuthenticated);
    await box.put(_streakKey, prefs.streakCount);
    if (prefs.lastReadDate != null) {
      await box.put(_lastReadKey, prefs.lastReadDate!.toIso8601String());
    }
  }
}
"""
with open('lib/data/repositories/preferences_repository.dart', 'w') as f:
    f.write(prefs_repo)

# 3. Update preferences_provider.dart
prefs_provider = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user_preferences.dart';
import '../data/repositories/preferences_repository.dart';

class PreferencesNotifier extends Notifier<UserPreferences> {
  final PreferencesRepository _repository = PreferencesRepository();

  @override
  UserPreferences build() {
    return _repository.getPreferences();
  }

  Future<void> login() async {
    final newState = state.copyWith(isAuthenticated: true);
    await _repository.savePreferences(newState);
    state = newState;
  }

  Future<void> logout() async {
    final newState = state.copyWith(isAuthenticated: false);
    await _repository.savePreferences(newState);
    state = newState;
  }

  Future<void> completeOnboarding() async {
    final newState = state.copyWith(onboardingCompleted: true);
    await _repository.savePreferences(newState);
    state = newState;
  }

  Future<void> updateTopics(List<String> topics) async {
    final newState = state.copyWith(selectedTopics: topics);
    await _repository.savePreferences(newState);
    state = newState;
  }

  Future<void> updateTheme(ThemePreference theme) async {
    final newState = state.copyWith(themePreference: theme);
    await _repository.savePreferences(newState);
    state = newState;
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
        newStreak += 1;
      } else if (difference > 1) {
        newStreak = 1;
      }
    }

    final newState = state.copyWith(streakCount: newStreak, lastReadDate: now);
    await _repository.savePreferences(newState);
    state = newState;
  }
}

final preferencesProvider = NotifierProvider<PreferencesNotifier, UserPreferences>(() {
  return PreferencesNotifier();
});
"""
with open('lib/providers/preferences_provider.dart', 'w') as f:
    f.write(prefs_provider)

# 4. Create Login Screen
os.makedirs('lib/features/auth', exist_ok=True)
login_screen = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../providers/preferences_provider.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  void _handleLogin() async {
    setState(() => _isLoading = true);
    // Simulate network delay
    await Future.delayed(const Duration(seconds: 2));
    if (mounted) {
      ref.read(preferencesProvider.notifier).login();
      Navigator.pushReplacementNamed(context, '/welcome');
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 60),
              Icon(
                Icons.menu_book_rounded,
                size: 80,
                color: Theme.of(context).colorScheme.primary,
              ).animate().scale(duration: 500.ms, curve: Curves.easeOutBack),
              const SizedBox(height: 24),
              Text(
                'Welcome to BriefDaily',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.2),
              const SizedBox(height: 8),
              Text(
                'Sign in to sync your personalized news digest across devices.',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
              ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.2),
              const SizedBox(height: 48),
              
              TextField(
                controller: _emailController,
                decoration: InputDecoration(
                  labelText: 'Email Address',
                  prefixIcon: const Icon(Icons.email_outlined),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                keyboardType: TextInputType.emailAddress,
              ).animate().fadeIn(delay: 400.ms).slideX(begin: -0.1),
              
              const SizedBox(height: 16),
              
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(
                  labelText: 'Password',
                  prefixIcon: const Icon(Icons.lock_outline),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                obscureText: true,
              ).animate().fadeIn(delay: 500.ms).slideX(begin: -0.1),
              
              const SizedBox(height: 32),
              
              FilledButton(
                onPressed: _isLoading ? null : _handleLogin,
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                child: _isLoading 
                    ? const SizedBox(
                        height: 24, 
                        width: 24, 
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)
                      )
                    : const Text('Sign In', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ).animate().fadeIn(delay: 600.ms).scale(),
              
              const SizedBox(height: 24),
              
              TextButton(
                onPressed: () {},
                child: const Text('Don\\'t have an account? Sign Up'),
              ).animate().fadeIn(delay: 700.ms),
            ],
          ),
        ),
      ),
    );
  }
}
"""
with open('lib/features/auth/login_screen.dart', 'w') as f:
    f.write(login_screen)

# 5. Update router.dart
router_dart = """import 'package:flutter/material.dart';
import '../navigation/main_scaffold.dart';
import '../features/onboarding/welcome_screen.dart';
import '../features/onboarding/topic_selection_screen.dart';
import '../features/onboarding/personalization_screen.dart';
import '../features/article/article_detail_screen.dart';
import '../features/profile/edit_interests_screen.dart';
import '../features/auth/login_screen.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const MainScaffold());
      case '/login':
        return MaterialPageRoute(builder: (_) => const LoginScreen());
      case '/welcome':
        return MaterialPageRoute(builder: (_) => const WelcomeScreen());
      case '/topic_selection':
        return MaterialPageRoute(builder: (_) => const TopicSelectionScreen());
      case '/personalization':
        return MaterialPageRoute(builder: (_) => const PersonalizationScreen());
      case '/edit_interests':
        return MaterialPageRoute(builder: (_) => const EditInterestsScreen());
      case '/article':
        return MaterialPageRoute(
          builder: (_) => const ArticleDetailScreen(),
          settings: settings,
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for ${settings.name}')),
          ),
        );
    }
  }
}
"""
with open('lib/app/router.dart', 'w') as f:
    f.write(router_dart)


# 6. Update app.dart
app_dart = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'theme/app_theme.dart';
import 'router.dart';
import '../providers/theme_provider.dart';
import '../providers/preferences_provider.dart';

class BriefDailyApp extends ConsumerWidget {
  const BriefDailyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeProvider);
    final prefs = ref.watch(preferencesProvider);

    String initialRoute;
    if (!prefs.isAuthenticated) {
      initialRoute = '/login';
    } else if (!prefs.onboardingCompleted) {
      initialRoute = '/welcome';
    } else {
      initialRoute = '/';
    }

    return MaterialApp(
      title: 'BriefDaily',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      initialRoute: initialRoute,
      onGenerateRoute: AppRouter.generateRoute,
      debugShowCheckedModeBanner: false,
    );
  }
}
"""
with open('lib/app/app.dart', 'w') as f:
    f.write(app_dart)

print("Phase 9 files created.")

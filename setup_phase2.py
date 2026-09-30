import os

files = {
    'lib/data/repositories/preferences_repository.dart': """import 'package:hive/hive.dart';
import '../../models/user_preferences.dart';

class PreferencesRepository {
  static const String _boxName = 'preferences';
  static const String _topicsKey = 'selected_topics';
  static const String _themeKey = 'theme_preference';
  static const String _onboardingKey = 'onboarding_completed';

  Future<void> init() async {
    await Hive.openBox(_boxName);
  }

  UserPreferences getPreferences() {
    final box = Hive.box(_boxName);
    final topics = box.get(_topicsKey, defaultValue: <String>[]) as List<dynamic>;
    final themeIndex = box.get(_themeKey, defaultValue: ThemePreference.system.index) as int;
    final onboardingCompleted = box.get(_onboardingKey, defaultValue: false) as bool;
    
    return UserPreferences(
      selectedTopics: topics.cast<String>(),
      themePreference: ThemePreference.values[themeIndex],
      onboardingCompleted: onboardingCompleted,
    );
  }

  Future<void> savePreferences(UserPreferences prefs) async {
    final box = Hive.box(_boxName);
    await box.put(_topicsKey, prefs.selectedTopics);
    await box.put(_themeKey, prefs.themePreference.index);
    await box.put(_onboardingKey, prefs.onboardingCompleted);
  }
}
""",
    'lib/providers/preferences_provider.dart': """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user_preferences.dart';
import '../data/repositories/preferences_repository.dart';

final preferencesRepositoryProvider = Provider<PreferencesRepository>((ref) {
  return PreferencesRepository();
});

class PreferencesNotifier extends Notifier<UserPreferences> {
  @override
  UserPreferences build() {
    return ref.watch(preferencesRepositoryProvider).getPreferences();
  }

  Future<void> updateTopics(List<String> topics) async {
    state = state.copyWith(selectedTopics: topics);
    await ref.read(preferencesRepositoryProvider).savePreferences(state);
  }

  Future<void> updateTheme(ThemePreference theme) async {
    state = state.copyWith(themePreference: theme);
    await ref.read(preferencesRepositoryProvider).savePreferences(state);
  }

  Future<void> completeOnboarding() async {
    state = state.copyWith(onboardingCompleted: true);
    await ref.read(preferencesRepositoryProvider).savePreferences(state);
  }
}

final preferencesProvider = NotifierProvider<PreferencesNotifier, UserPreferences>(() {
  return PreferencesNotifier();
});
""",
    'lib/app/router.dart': """import 'package:flutter/material.dart';
import '../features/digest/digest_shell.dart';
import '../features/onboarding/welcome_screen.dart';
import '../features/onboarding/topic_selection_screen.dart';
import '../features/onboarding/personalization_screen.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const DigestShell());
      case '/welcome':
        return MaterialPageRoute(builder: (_) => const WelcomeScreen());
      case '/topic_selection':
        return MaterialPageRoute(builder: (_) => const TopicSelectionScreen());
      case '/personalization':
        return MaterialPageRoute(builder: (_) => const PersonalizationScreen());
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
    'lib/app/app.dart': """import 'package:flutter/material.dart';
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
    final onboardingCompleted = ref.watch(preferencesProvider.select((p) => p.onboardingCompleted));

    return MaterialApp(
      title: 'BriefDaily',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      initialRoute: onboardingCompleted ? '/' : '/welcome',
      onGenerateRoute: AppRouter.generateRoute,
      debugShowCheckedModeBanner: false,
    );
  }
}
""",
    'lib/features/onboarding/welcome_screen.dart': """import 'package:flutter/material.dart';
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
              ),
              const SizedBox(height: AppSpacing.s32),
              Text(
                'BriefDaily',
                style: Theme.of(context).textTheme.displayLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.s16),
              Text(
                'Your news.\\nYour interests.\\nYour daily brief.',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                      fontWeight: FontWeight.normal,
                    ),
                textAlign: TextAlign.center,
              ),
              const Spacer(),
              FilledButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/topic_selection');
                },
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: AppSpacing.s16),
                ),
                child: const Text('Get Started', style: TextStyle(fontSize: 18)),
              ),
              const SizedBox(height: AppSpacing.s24),
            ],
          ),
        ),
      ),
    );
  }
}
""",
    'lib/features/onboarding/topic_selection_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../app/theme/app_spacing.dart';
import '../../data/mock_topics.dart';
import '../../providers/preferences_provider.dart';

class TopicSelectionScreen extends ConsumerStatefulWidget {
  const TopicSelectionScreen({super.key});

  @override
  ConsumerState<TopicSelectionScreen> createState() => _TopicSelectionScreenState();
}

class _TopicSelectionScreenState extends ConsumerState<TopicSelectionScreen> {
  final Set<String> _selectedTopics = {};

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
        title: const Text('Choose Topics'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(AppSpacing.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'What are you interested in?',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: AppSpacing.s8),
            Text(
              'Select the topics you care about to personalize your daily brief.',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                  ),
            ),
            const SizedBox(height: AppSpacing.s24),
            Expanded(
              child: SingleChildScrollView(
                child: Wrap(
                  spacing: AppSpacing.s8,
                  runSpacing: AppSpacing.s12,
                  children: mockTopics.map((topic) {
                    final isSelected = _selectedTopics.contains(topic.name);
                    return FilterChip(
                      label: Text('${topic.icon} ${topic.name}'),
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
              onPressed: _selectedTopics.isEmpty
                  ? null
                  : () async {
                      await ref
                          .read(preferencesProvider.notifier)
                          .updateTopics(_selectedTopics.toList());
                      if (context.mounted) {
                        Navigator.pushReplacementNamed(context, '/personalization');
                      }
                    },
              style: FilledButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.s16),
              ),
              child: const Text('Continue', style: TextStyle(fontSize: 18)),
            ),
            const SizedBox(height: AppSpacing.s24),
          ],
        ),
      ),
    );
  }
}
""",
    'lib/features/onboarding/personalization_screen.dart': """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../app/theme/app_spacing.dart';
import '../../providers/preferences_provider.dart';

class PersonalizationScreen extends ConsumerStatefulWidget {
  const PersonalizationScreen({super.key});

  @override
  ConsumerState<PersonalizationScreen> createState() => _PersonalizationScreenState();
}

class _PersonalizationScreenState extends ConsumerState<PersonalizationScreen> {
  @override
  void initState() {
    super.initState();
    _startPersonalization();
  }

  Future<void> _startPersonalization() async {
    // Simulate loading for 1.5 seconds
    await Future.delayed(const Duration(milliseconds: 1500));
    if (mounted) {
      await ref.read(preferencesProvider.notifier).completeOnboarding();
      if (mounted) {
        Navigator.pushReplacementNamed(context, '/');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(),
            const SizedBox(height: AppSpacing.s24),
            Text(
              'Personalizing your brief...',
              style: Theme.of(context).textTheme.titleLarge,
            ),
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

print("Phase 2 Files created.")

import os

# 1. Update preferences_repository.dart
prefs_repo = """import 'package:hive/hive.dart';
import '../../models/user_preferences.dart';

class PreferencesRepository {
  static const String _boxName = 'preferences';
  static const String _topicsKey = 'selected_topics';
  static const String _themeKey = 'theme_preference';
  static const String _onboardingKey = 'onboarding_completed';
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
      streakCount: streakCount,
      lastReadDate: lastReadDate,
    );
  }

  Future<void> savePreferences(UserPreferences prefs) async {
    final box = Hive.box(_boxName);
    await box.put(_topicsKey, prefs.selectedTopics);
    await box.put(_themeKey, prefs.themePreference.index);
    await box.put(_onboardingKey, prefs.onboardingCompleted);
    await box.put(_streakKey, prefs.streakCount);
    if (prefs.lastReadDate != null) {
      await box.put(_lastReadKey, prefs.lastReadDate!.toIso8601String());
    }
  }
}
"""
with open('lib/data/repositories/preferences_repository.dart', 'w') as f:
    f.write(prefs_repo)

# 2. Update preferences_provider.dart
prefs_provider = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user_preferences.dart';
import '../data/repositories/preferences_repository.dart';

class PreferencesNotifier extends Notifier<UserPreferences> {
  final PreferencesRepository _repository = PreferencesRepository();

  @override
  UserPreferences build() {
    return _repository.getPreferences();
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

print("Bug fixed.")

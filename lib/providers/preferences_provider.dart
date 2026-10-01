import 'package:flutter_riverpod/flutter_riverpod.dart';
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
    final onboardingCompleted = _box.get(
      'onboardingCompleted',
      defaultValue: false,
    );
    final selectedTopics = List<String>.from(
      _box.get('selectedTopics', defaultValue: []),
    );
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
      final lastReadDay = DateTime(
        newLastRead.year,
        newLastRead.month,
        newLastRead.day,
      );
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

final preferencesProvider =
    NotifierProvider<PreferencesNotifier, UserPreferences>(() {
      return PreferencesNotifier();
    });

import 'package:flutter_riverpod/flutter_riverpod.dart';

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
      final lastReadDay = DateTime(
        newLastRead.year,
        newLastRead.month,
        newLastRead.day,
      );
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

final preferencesProvider =
    NotifierProvider<PreferencesNotifier, UserPreferences>(() {
      return PreferencesNotifier();
    });

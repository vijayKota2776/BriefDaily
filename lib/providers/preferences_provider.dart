import 'package:flutter_riverpod/flutter_riverpod.dart';

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

final preferencesProvider =
    NotifierProvider<PreferencesNotifier, UserPreferences>(() {
      return PreferencesNotifier();
    });

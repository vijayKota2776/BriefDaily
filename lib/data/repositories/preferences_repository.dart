import 'package:hive/hive.dart';

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
    final topics =
        box.get(_topicsKey, defaultValue: <String>[]) as List<dynamic>;
    final themeIndex =
        box.get(_themeKey, defaultValue: ThemePreference.system.index) as int;
    final onboardingCompleted =
        box.get(_onboardingKey, defaultValue: false) as bool;

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

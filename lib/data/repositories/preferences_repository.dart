import 'package:hive/hive.dart';

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
    final topics =
        box.get(_topicsKey, defaultValue: <String>[]) as List<dynamic>;
    final themeIndex =
        box.get(_themeKey, defaultValue: ThemePreference.system.index) as int;
    final onboardingCompleted =
        box.get(_onboardingKey, defaultValue: false) as bool;
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

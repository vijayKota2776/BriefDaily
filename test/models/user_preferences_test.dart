import 'package:flutter_test/flutter_test.dart';
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

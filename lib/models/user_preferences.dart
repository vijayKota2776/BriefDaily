enum ThemePreference { system, light, dark }

class UserPreferences {
  final bool onboardingCompleted;
  final List<String> selectedTopics;
  final ThemePreference themePreference;
  final int streakCount;
  final DateTime? lastReadDate;

  UserPreferences({
    this.onboardingCompleted = false,
    this.selectedTopics = const [],
    this.themePreference = ThemePreference.system,
    this.streakCount = 0,
    this.lastReadDate,
  });

  UserPreferences copyWith({
    bool? onboardingCompleted,
    List<String>? selectedTopics,
    ThemePreference? themePreference,
    int? streakCount,
    DateTime? lastReadDate,
  }) {
    return UserPreferences(
      onboardingCompleted: onboardingCompleted ?? this.onboardingCompleted,
      selectedTopics: selectedTopics ?? this.selectedTopics,
      themePreference: themePreference ?? this.themePreference,
      streakCount: streakCount ?? this.streakCount,
      lastReadDate: lastReadDate ?? this.lastReadDate,
    );
  }
}

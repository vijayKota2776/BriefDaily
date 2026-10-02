enum ThemePreference { system, light, dark }

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

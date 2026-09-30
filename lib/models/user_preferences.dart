enum ThemePreference { system, light, dark }

class UserPreferences {
  final List<String> selectedTopics;
  final ThemePreference themePreference;
  final bool onboardingCompleted;

  const UserPreferences({
    this.selectedTopics = const [],
    this.themePreference = ThemePreference.system,
    this.onboardingCompleted = false,
  });

  UserPreferences copyWith({
    List<String>? selectedTopics,
    ThemePreference? themePreference,
    bool? onboardingCompleted,
  }) {
    return UserPreferences(
      selectedTopics: selectedTopics ?? this.selectedTopics,
      themePreference: themePreference ?? this.themePreference,
      onboardingCompleted: onboardingCompleted ?? this.onboardingCompleted,
    );
  }
}

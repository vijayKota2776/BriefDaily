import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/material.dart';

import '../models/user_preferences.dart';
import 'preferences_provider.dart';

final themeProvider = Provider<ThemeMode>((ref) {
  final prefs = ref.watch(preferencesProvider);
  switch (prefs.themePreference) {
    case ThemePreference.light:
      return ThemeMode.light;
    case ThemePreference.dark:
      return ThemeMode.dark;
    case ThemePreference.system:
      return ThemeMode.system;
  }
});

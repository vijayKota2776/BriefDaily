import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'theme/app_theme.dart';
import 'router.dart';
import '../providers/theme_provider.dart';
import '../providers/preferences_provider.dart';

class BriefDailyApp extends ConsumerWidget {
  const BriefDailyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeProvider);
    final prefs = ref.watch(preferencesProvider);

    String initialRoute;
    if (!prefs.isAuthenticated) {
      initialRoute = '/login';
    } else if (!prefs.onboardingCompleted) {
      initialRoute = '/welcome';
    } else {
      initialRoute = '/';
    }

    return MaterialApp(
      title: 'BriefDaily',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      initialRoute: initialRoute,
      onGenerateRoute: AppRouter.generateRoute,
      debugShowCheckedModeBanner: false,
    );
  }
}

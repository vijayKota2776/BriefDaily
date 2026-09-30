import 'package:flutter/material.dart';

import '../features/digest/digest_shell.dart';
import '../features/onboarding/welcome_screen.dart';
import '../features/onboarding/topic_selection_screen.dart';
import '../features/onboarding/personalization_screen.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const DigestShell());
      case '/welcome':
        return MaterialPageRoute(builder: (_) => const WelcomeScreen());
      case '/topic_selection':
        return MaterialPageRoute(builder: (_) => const TopicSelectionScreen());
      case '/personalization':
        return MaterialPageRoute(builder: (_) => const PersonalizationScreen());
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for ${settings.name}')),
          ),
        );
    }
  }
}

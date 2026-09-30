import 'package:flutter/material.dart';

import '../navigation/main_scaffold.dart';
import '../features/onboarding/welcome_screen.dart';
import '../features/onboarding/topic_selection_screen.dart';
import '../features/onboarding/personalization_screen.dart';
import '../features/article/article_detail_screen.dart';
import '../features/profile/edit_interests_screen.dart';
import '../models/article.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const MainScaffold());
      case '/welcome':
        return MaterialPageRoute(builder: (_) => const WelcomeScreen());
      case '/topic_selection':
        return MaterialPageRoute(builder: (_) => const TopicSelectionScreen());
      case '/personalization':
        return MaterialPageRoute(builder: (_) => const PersonalizationScreen());
      case '/edit_interests':
        return MaterialPageRoute(builder: (_) => const EditInterestsScreen());
      case '/article':
        final article = settings.arguments as Article;
        return MaterialPageRoute(
          builder: (_) => ArticleDetailScreen(article: article),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for ${settings.name}')),
          ),
        );
    }
  }
}

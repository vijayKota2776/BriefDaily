import os

def update_file(path, callback):
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        content = f.read()
    content = callback(content)
    with open(path, 'w') as f:
        f.write(content)

# 1. Update article_card.dart to add topic tag
def update_card(content):
    return content.replace(
        "Text(\n                    '${article.source} · ${timeago.format(article.publishedAt)} · ${article.readingTime} min',",
        "Text(\n                    '${article.source} · ${article.topic.toUpperCase()} · ${timeago.format(article.publishedAt)} · ${article.readingTime} min',"
    )
update_file('lib/features/digest/widgets/article_card.dart', update_card)


# 2. Update news_service.dart
def update_news_service(content):
    # Remove fallback API key
    content = content.replace(
        "static const String _apiKey = String.fromEnvironment('NEWS_API_KEY', defaultValue: '96d4841970994aeca6abd3ea7663d8db');",
        "static const String _apiKey = String.fromEnvironment('NEWS_API_KEY');"
    )
    # Use all topics instead of just take(2)
    content = content.replace(
        "final targetTopics = topics.take(2).toList();",
        "final targetTopics = topics;"
    )
    return content
update_file('lib/services/news_service.dart', update_news_service)


# 3. Add Logout to profile_screen.dart
def update_profile(content):
    if "FirebaseAuth.instance.signOut" not in content:
        content = "import 'package:firebase_auth/firebase_auth.dart';\n" + content
        # Add Logout button at the end of the ListView
        replacement = """          // ignore: deprecated_member_use
          RadioListTile<ThemePreference>(
            title: const Text('Dark'),
            value: ThemePreference.dark,
            // ignore: deprecated_member_use
            groupValue: prefs.themePreference,
            // ignore: deprecated_member_use
            onChanged: (val) {
              if (val != null) {
                ref.read(preferencesProvider.notifier).updateTheme(val);
              }
            },
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text('Log Out', style: TextStyle(color: Colors.red)),
            onTap: () async {
              await FirebaseAuth.instance.signOut();
              await ref.read(preferencesProvider.notifier).logout();
              Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
            },
          ),
"""
        content = content.replace("""          // ignore: deprecated_member_use
          RadioListTile<ThemePreference>(
            title: const Text('Dark'),
            value: ThemePreference.dark,
            // ignore: deprecated_member_use
            groupValue: prefs.themePreference,
            // ignore: deprecated_member_use
            onChanged: (val) {
              if (val != null) {
                ref.read(preferencesProvider.notifier).updateTheme(val);
              }
            },
          ),""", replacement)
    return content

update_file('lib/features/profile/profile_screen.dart', update_profile)
print("Applied final audit fixes")

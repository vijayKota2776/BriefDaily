import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../providers/preferences_provider.dart';
import '../../models/user_preferences.dart';
import '../../app/theme/app_spacing.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final prefs = ref.watch(preferencesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Profile & Settings')),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.s16),
        children: [
          ListTile(
            leading: const Icon(Icons.interests),
            title: const Text('Edit Interests'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              Navigator.pushNamed(context, '/edit_interests');
            },
          ),
          const Divider(),
          const Padding(
            padding: EdgeInsets.symmetric(
              vertical: AppSpacing.s8,
              horizontal: AppSpacing.s16,
            ),
            child: Text(
              'Appearance',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          // ignore: deprecated_member_use
          RadioListTile<ThemePreference>(
            title: const Text('System Default'),
            value: ThemePreference.system,
            // ignore: deprecated_member_use
            groupValue: prefs.themePreference,
            // ignore: deprecated_member_use
            onChanged: (val) {
              if (val != null) {
                ref.read(preferencesProvider.notifier).updateTheme(val);
              }
            },
          ),
          // ignore: deprecated_member_use
          RadioListTile<ThemePreference>(
            title: const Text('Light'),
            value: ThemePreference.light,
            // ignore: deprecated_member_use
            groupValue: prefs.themePreference,
            // ignore: deprecated_member_use
            onChanged: (val) {
              if (val != null) {
                ref.read(preferencesProvider.notifier).updateTheme(val);
              }
            },
          ),
          // ignore: deprecated_member_use
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
              if (context.mounted) {
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/login',
                  (route) => false,
                );
              }
            },
          ),
        ],
      ),
    );
  }
}

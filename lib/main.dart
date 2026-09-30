import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'app/app.dart';
import 'data/repositories/bookmark_repository.dart';
import 'data/repositories/preferences_repository.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  try {
    await Hive.initFlutter();

    // Initialize repositories
    final prefsRepo = PreferencesRepository();
    await prefsRepo.init();

    final bookmarkRepo = BookmarkRepository();
    await bookmarkRepo.init();

    runApp(const ProviderScope(child: BriefDailyApp()));
  } catch (e) {
    runApp(
      MaterialApp(
        home: Scaffold(body: Center(child: Text('Initialization failed: \$e'))),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:firebase_core/firebase_core.dart';

import 'firebase_options.dart';

import 'app/app.dart';
import 'data/repositories/preferences_repository.dart';
import 'data/repositories/bookmark_repository.dart';
import 'services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  // Initialize Hive
  await Hive.initFlutter();

  // Initialize repositories
  final prefsRepo = PreferencesRepository();
  await prefsRepo.init();

  final bookmarkRepo = BookmarkRepository();
  await bookmarkRepo.init();

  // Initialize notifications
  final notificationService = NotificationService();
  await notificationService.init();
  await notificationService.requestPermissions();

  runApp(const ProviderScope(child: BriefDailyApp()));
}

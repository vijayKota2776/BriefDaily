import 'package:flutter/foundation.dart';

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  Future<void> init() async {
    debugPrint('Notifications initialized (Mocked)');
  }

  Future<void> requestPermissions() async {
    debugPrint('Notification Permissions requested (Mocked)');
  }

  Future<void> scheduleDailyBriefNotification() async {
    debugPrint('Scheduled daily brief notification (Mocked)');
  }
}

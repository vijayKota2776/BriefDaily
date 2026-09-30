import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'preferences_provider.dart';

final selectedTopicsProvider = Provider<List<String>>((ref) {
  return ref.watch(preferencesProvider).selectedTopics;
});

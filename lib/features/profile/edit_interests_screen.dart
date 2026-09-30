import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme/app_spacing.dart';
import '../../data/mock_topics.dart';
import '../../providers/preferences_provider.dart';

class EditInterestsScreen extends ConsumerStatefulWidget {
  const EditInterestsScreen({super.key});

  @override
  ConsumerState<EditInterestsScreen> createState() =>
      _EditInterestsScreenState();
}

class _EditInterestsScreenState extends ConsumerState<EditInterestsScreen> {
  late Set<String> _selectedTopics;

  @override
  void initState() {
    super.initState();
    _selectedTopics = ref.read(preferencesProvider).selectedTopics.toSet();
  }

  void _toggleTopic(String topicName) {
    setState(() {
      if (_selectedTopics.contains(topicName)) {
        _selectedTopics.remove(topicName);
      } else {
        _selectedTopics.add(topicName);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Your Interests')),
      body: Padding(
        padding: const EdgeInsets.all(AppSpacing.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Wrap(
                  spacing: AppSpacing.s8,
                  runSpacing: AppSpacing.s12,
                  children: mockTopics.map((topic) {
                    final isSelected = _selectedTopics.contains(topic.name);
                    return FilterChip(
                      label: Text('${topic.icon} ${topic.name}'),
                      selected: isSelected,
                      onSelected: (_) => _toggleTopic(topic.name),
                      labelStyle: TextStyle(
                        color: isSelected
                            ? Theme.of(context).colorScheme.onPrimary
                            : Theme.of(context).colorScheme.onSurface,
                      ),
                      selectedColor: Theme.of(context).colorScheme.primary,
                      showCheckmark: false,
                    );
                  }).toList(),
                ),
              ),
            ),
            FilledButton(
              onPressed: () async {
                await ref
                    .read(preferencesProvider.notifier)
                    .updateTopics(_selectedTopics.toList());
                if (context.mounted) {
                  Navigator.pop(context);
                }
              },
              style: FilledButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.s16),
              ),
              child: const Text('Save Changes', style: TextStyle(fontSize: 18)),
            ),
            const SizedBox(height: AppSpacing.s24),
          ],
        ),
      ),
    );
  }
}

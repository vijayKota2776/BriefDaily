import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme/app_spacing.dart';
import '../../data/mock_topics.dart';
import '../../providers/preferences_provider.dart';

class TopicSelectionScreen extends ConsumerStatefulWidget {
  const TopicSelectionScreen({super.key});

  @override
  ConsumerState<TopicSelectionScreen> createState() =>
      _TopicSelectionScreenState();
}

class _TopicSelectionScreenState extends ConsumerState<TopicSelectionScreen> {
  final Set<String> _selectedTopics = {};

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
      appBar: AppBar(title: const Text('Choose Topics')),
      body: Padding(
        padding: const EdgeInsets.all(AppSpacing.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'What are you interested in?',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: AppSpacing.s8),
            Text(
              'Select the topics you care about to personalize your daily brief.',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.7),
              ),
            ),
            const SizedBox(height: AppSpacing.s24),
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
              onPressed: _selectedTopics.isEmpty
                  ? null
                  : () async {
                      await ref
                          .read(preferencesProvider.notifier)
                          .updateTopics(_selectedTopics.toList());
                      if (context.mounted) {
                        Navigator.pushReplacementNamed(
                          context,
                          '/personalization',
                        );
                      }
                    },
              style: FilledButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.s16),
              ),
              child: const Text('Continue', style: TextStyle(fontSize: 18)),
            ),
            const SizedBox(height: AppSpacing.s24),
          ],
        ),
      ),
    );
  }
}

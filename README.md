# 📰 BriefDaily

### Personalized News Digest & Bookmark App

BriefDaily is a modern Flutter application that delivers a personalized daily news digest based on the user's selected interests. Users can choose topics, browse relevant headlines, open article details, bookmark stories for later, and manage their preferences.

The application is designed around a simple principle:

> **Your news. Your interests. Your daily brief.**

BriefDaily combines **Flutter**, **Dart**, **Riverpod**, **Material 3**, and **on-device persistence** to create a responsive, reactive, and polished news-reading experience.

---

# 📋 Table of Contents

* [Project Overview](#-project-overview)
* [Problem Statement](#-problem-statement)
* [Objectives](#-objectives)
* [Core Concept](#-core-concept)
* [Key Features](#-key-features)
* [User Journey](#-user-journey)
* [Application Screens](#-application-screens)
* [Technology Stack](#-technology-stack)
* [Architecture](#-architecture)
* [Project Structure](#-project-structure)
* [State Management](#-state-management)
* [Data Flow](#-data-flow)
* [Personalization Logic](#-personalization-logic)
* [Local Storage](#-local-storage)
* [UI & Design System](#-ui--design-system)
* [Responsive Design](#-responsive-design)
* [Navigation](#-navigation)
* [Article Model](#-article-model)
* [Topic System](#-topic-system)
* [Bookmark System](#-bookmark-system)
* [Loading & Error States](#-loading--error-states)
* [Accessibility](#-accessibility)
* [Figma Design](#-figma-design)
* [Testing](#-testing)
* [Installation](#-installation)
* [Running the Project](#-running-the-project)
* [Build Configuration](#-build-configuration)
* [Development Guidelines](#-development-guidelines)
* [Future Enhancements](#-future-enhancements)
* [Project Deliverables](#-project-deliverables)
* [Evaluation Mapping](#-evaluation-mapping)
* [Conclusion](#-conclusion)

---

# 🚀 Project Overview

BriefDaily is a personalized news digest application built with Flutter.

Instead of presenting users with an unfiltered stream of articles, BriefDaily allows users to explicitly select the topics they care about.

For example:

```text
User Interests

✓ Technology
✓ Artificial Intelligence
✓ Startups
✗ Sports
✗ Entertainment
```

The application uses these preferences to determine which articles should appear in the user's digest.

The application also provides:

* Article browsing
* Topic filtering
* Article sorting
* Bookmarking
* Persistent bookmarks
* Article details
* Search
* Explore topics
* Preference management
* Light and dark themes
* Responsive layouts
* Loading and error states
* Local data persistence

---

# 🎯 Problem Statement

Modern users are exposed to a large amount of news content every day.

Traditional news feeds often present users with hundreds of articles across unrelated subjects. This can create information overload and make it difficult for users to quickly find stories relevant to their interests.

BriefDaily addresses this problem by allowing users to:

1. Select topics they care about.
2. Receive a digest filtered around those topics.
3. View recent stories first.
4. Save interesting articles.
5. Return to saved stories later.
6. Change their interests whenever they want.

The application therefore focuses on **personalization, simplicity, and efficient information discovery**.

---

# 🎯 Objectives

The primary objectives of BriefDaily are:

### UI & Widgets

Build a functional news application using Flutter widgets including:

* `ListView`
* `GridView`
* `Card`
* `Icon`
* `Chip`
* `AppBar`
* `BottomNavigationBar`
* `NavigationBar`
* `Scaffold`
* `RefreshIndicator`
* `Dismissible`

### Styling & Theming

Implement a clean editorial design using:

* Material 3
* Custom typography
* Consistent spacing
* Editorial-style headlines
* Light mode
* Dark mode
* Responsive layouts

### Dart Logic

Use Dart and Riverpod to:

* Store selected topics.
* Filter articles.
* Sort articles.
* Manage bookmarks.
* Update the UI reactively.
* Maintain application state.

### Local Storage

Persist:

* Selected topics
* Bookmarked articles
* User preferences

### Figma

Design the complete user journey from:

```text
Onboarding
    ↓
Topic Selection
    ↓
Personalized Digest
    ↓
Article
    ↓
Bookmark
    ↓
Bookmarks
```

---

# 💡 Core Concept

The central BriefDaily experience is:

```text
Choose Interests
       ↓
Personalize Feed
       ↓
Browse Daily Digest
       ↓
Open Article
       ↓
Bookmark
       ↓
Read Later
```

The selected topics act as the foundation of the application's personalization system.

---

# ✨ Key Features

## 1. Personalized Topic Selection

Users can select the topics they are interested in.

Example:

```text
Technology
AI
Startups
Science
Business
Sports
World
Health
Finance
Gaming
Climate
Entertainment
```

Users can select multiple topics.

The selected topics are stored locally so preferences remain available between application sessions.

---

# 2. Personalized News Digest

The Home screen displays articles based on the user's selected topics.

Each article card contains:

* Headline
* Source
* Topic
* Published time
* Reading time
* Article image
* Bookmark action

Example:

```text
TECHNOLOGY

New AI tools are changing
how developers build software

TechCrunch · 2h ago

♡
```

---

# 3. Latest Articles First

Articles are sorted using their publication timestamp.

The most recently published articles appear first.

Conceptually:

```text
Article A → 10:30 AM
Article B → 09:45 AM
Article C → 08:20 AM
Article D → 07:10 AM
```

Result:

```text
A
B
C
D
```

---

# 4. Featured Story

The first or highest-priority article can be presented as a large featured story.

Example:

```text
┌─────────────────────────────┐
│                             │
│        ARTICLE IMAGE        │
│                             │
│  TRENDING                   │
│                             │
│  The technology shaping     │
│  the next decade            │
│                             │
│  Wired · 30 min ago      ♡  │
└─────────────────────────────┘
```

This creates stronger editorial hierarchy.

---

# 5. Article Details

Users can tap an article to open a dedicated article detail screen.

The screen contains:

* Hero image
* Topic
* Headline
* Source
* Author
* Published time
* Reading time
* Summary
* Article content
* Bookmark button
* External article link

---

# 6. Bookmarking

Users can bookmark an article directly from the digest or article detail screen.

Bookmark state:

```text
♡
```

becomes:

```text
♥
```

The UI updates immediately using Riverpod.

---

# 7. Persistent Bookmarks

Bookmarks are stored locally on the device.

Closing and reopening the application does not remove saved articles.

Data flow:

```text
User taps Bookmark
        ↓
Bookmark Provider
        ↓
Bookmark Repository
        ↓
Local Storage
```

---

# 8. Remove Bookmarks

Users can remove individual bookmarks.

Supported interactions include:

* Bookmark button
* Delete action
* Swipe-to-delete

Example:

```text
Article
   ← Swipe
      ↓
   Remove
```

---

# 9. Undo Bookmark Removal

When a bookmark is removed, the application can display a Snackbar:

```text
Article removed

                 UNDO
```

Selecting `UNDO` restores the article.

---

# 10. Explore

The Explore screen allows users to discover stories across available topics.

Example:

```text
Explore

Search stories...

Topics

Technology
AI
Business
Science
Startups
Sports
World
Health
Finance
Gaming
```

---

# 11. Edit Interests

Users can modify their selected topics after onboarding.

Example:

```text
Your Interests

✓ Technology
✓ AI
✓ Startups
○ Sports
○ Science
○ Finance

[Save Changes]
```

Updating interests automatically updates the digest.

---

# 12. Search

Users can search the local article dataset.

Example:

```text
Search BriefDaily

"artificial intelligence"

Results

New AI model released...
AI changes software development...
```

---

# 13. Pull to Refresh

The digest supports pull-to-refresh.

```text
↓ Pull

Refreshing your brief...

Updated
```

Flutter's `RefreshIndicator` can be used for this behavior.

---

# 14. Loading Skeletons

Instead of displaying a plain loading indicator, BriefDaily can display article skeleton cards.

Example:

```text
┌───────────────────────────┐
│ █████████████████         │
│                           │
│ ████████████████████      │
│ ███████████               │
│                           │
│ ███████     █████         │
└───────────────────────────┘
```

---

# 15. Empty States

The application provides meaningful empty states.

### No Bookmarks

```text
        🔖

Nothing saved yet

Articles you bookmark
will appear here.

[Explore Stories]
```

### No Search Results

```text
No stories found

Try another keyword.
```

### No Topics

```text
Choose your interests

Select topics to personalize
your daily brief.

[Choose Topics]
```

---

# 16. Dark Mode

BriefDaily supports:

* Light mode
* Dark mode
* System theme

Users can switch between them from Settings.

---

# 17. Responsive UI

The application is designed for different screen sizes.

Supported layouts include:

* Mobile
* Large phones
* Tablets

The layout adapts using:

* `LayoutBuilder`
* `MediaQuery`
* `Flexible`
* `Expanded`
* `GridView`
* Responsive spacing

---

# 🧭 User Journey

The primary user journey is:

```text
                         ┌───────────┐
                         │   Splash  │
                         └─────┬─────┘
                               ↓
                         ┌───────────┐
                         │  Welcome  │
                         └─────┬─────┘
                               ↓
                    ┌─────────────────────┐
                    │  Choose Your Topics │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Personalizing Brief │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │    Daily Digest     │
                    └──────────┬──────────┘
                               ↓
                       ┌───────┴───────┐
                       ↓               ↓
                 Article Detail     Explore
                       │
                       ↓
                  Bookmark
                       │
                       ↓
                  Bookmarks
                       │
                       ↓
                  Remove / Undo
                       │
                       ↓
                 Edit Interests
                       │
                       ↓
                  Updated Feed
```

---

# 📱 Application Screens

The planned application contains the following screens.

## Onboarding

1. Splash Screen
2. Welcome Screen
3. Onboarding Information
4. Topic Selection
5. Personalization Loading

## Main Application

6. Home / Daily Digest
7. Article Detail
8. Explore
9. Bookmarks
10. Profile / Settings

## Preference Management

11. Edit Topics
12. Theme Settings

## Supporting States

13. Loading State
14. Empty State
15. Error State
16. Bookmark Undo State

---

# 🛠 Technology Stack

## Frontend

**Flutter**

Flutter is used to build the cross-platform mobile application.

## Programming Language

**Dart**

Used for:

* UI logic
* Models
* Providers
* Repositories
* Application state
* Business logic

## State Management

**Riverpod**

Used for:

* Topic state
* Article state
* Bookmark state
* Preference state
* Reactive UI updates

## UI Framework

**Material 3**

Used for:

* Components
* Themes
* Typography
* Buttons
* Cards
* Navigation
* Color schemes

## Local Storage

Recommended:

**Hive / Hive CE**

Used to persist:

* Bookmarks
* Selected topics
* Preferences

## Design

**Figma**

Used to design:

* User flows
* Screens
* Components
* Responsive layouts
* Interactive prototype

---

# 🏗 Architecture

BriefDaily follows a feature-oriented architecture.

```text
┌─────────────────────────────┐
│            UI               │
│       Flutter Widgets       │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│          Riverpod           │
│       State Providers       │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│        Repositories         │
│     Data Access Layer       │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       Local / Mock Data     │
│       JSON / Hive           │
└─────────────────────────────┘
```

The UI should not directly manipulate persistent storage.

Instead:

```text
UI
 ↓
Provider
 ↓
Repository
 ↓
Storage
```

This keeps the code easier to maintain and test.

---

# 📁 Project Structure

Recommended structure:

```text
briefdaily/
│
├── android/
├── ios/
├── web/
├── macos/
├── windows/
├── linux/
│
├── assets/
│   ├── images/
│   ├── icons/
│   └── data/
│
├── lib/
│   │
│   ├── main.dart
│   │
│   ├── app/
│   │   ├── app.dart
│   │   ├── router.dart
│   │   └── theme/
│   │       ├── app_theme.dart
│   │       ├── app_colors.dart
│   │       ├── app_typography.dart
│   │       └── app_spacing.dart
│   │
│   ├── core/
│   │   ├── constants/
│   │   ├── extensions/
│   │   ├── utils/
│   │   ├── errors/
│   │   └── widgets/
│   │
│   ├── models/
│   │   ├── article.dart
│   │   ├── topic.dart
│   │   └── user_preferences.dart
│   │
│   ├── data/
│   │   ├── mock_articles.dart
│   │   ├── mock_topics.dart
│   │   └── repositories/
│   │       ├── article_repository.dart
│   │       ├── bookmark_repository.dart
│   │       └── preferences_repository.dart
│   │
│   ├── providers/
│   │   ├── article_provider.dart
│   │   ├── bookmark_provider.dart
│   │   ├── topic_provider.dart
│   │   ├── preferences_provider.dart
│   │   └── theme_provider.dart
│   │
│   ├── features/
│   │   │
│   │   ├── onboarding/
│   │   │   ├── welcome_screen.dart
│   │   │   ├── onboarding_screen.dart
│   │   │   ├── topic_selection_screen.dart
│   │   │   └── personalization_screen.dart
│   │   │
│   │   ├── digest/
│   │   │   ├── digest_screen.dart
│   │   │   ├── article_detail_screen.dart
│   │   │   └── widgets/
│   │   │       ├── article_card.dart
│   │   │       ├── featured_article_card.dart
│   │   │       ├── topic_chip.dart
│   │   │       ├── article_skeleton.dart
│   │   │       └── digest_header.dart
│   │   │
│   │   ├── explore/
│   │   │   ├── explore_screen.dart
│   │   │   └── widgets/
│   │   │       └── topic_grid.dart
│   │   │
│   │   ├── bookmarks/
│   │   │   ├── bookmarks_screen.dart
│   │   │   └── widgets/
│   │   │       └── bookmark_card.dart
│   │   │
│   │   └── profile/
│   │       ├── profile_screen.dart
│   │       ├── edit_topics_screen.dart
│   │       └── settings_screen.dart
│   │
│   └── navigation/
│       └── bottom_navigation.dart
│
├── test/
│   ├── models/
│   ├── providers/
│   ├── repositories/
│   └── widgets/
│
├── integration_test/
│
├── pubspec.yaml
├── analysis_options.yaml
├── README.md
└── .gitignore
```

---

# 🔄 State Management

Riverpod is responsible for the application's reactive state.

## Topic State

Responsible for:

* Selected topics
* Adding topics
* Removing topics
* Saving topics
* Loading saved topics

Conceptual provider:

```dart
selectedTopicsProvider
```

---

# 📰 Article State

Responsible for:

* Article collection
* Digest filtering
* Sorting
* Search
* Featured article
* Refreshing

Conceptual provider:

```dart
digestProvider
```

The digest depends on:

```text
Selected Topics
        ↓
Article Provider
        ↓
Filtered Articles
        ↓
Sorted Articles
```

---

# 🔖 Bookmark State

Responsible for:

* Bookmarking
* Removing bookmarks
* Checking bookmark state
* Loading saved bookmarks

Conceptual provider:

```dart
bookmarkProvider
```

---

# 🎨 Theme State

Responsible for:

* Light theme
* Dark theme
* System theme

Conceptual provider:

```dart
themeProvider
```

---

# 🔄 Data Flow

The main reactive data flow is:

```text
              USER SELECTS TOPIC
                       │
                       ↓
             Topic State Provider
                       │
                       ↓
              Selected Topic List
                       │
                       ↓
                Digest Provider
                       │
                       ↓
              Filter Article Data
                       │
                       ↓
              Sort By Published Time
                       │
                       ↓
                  UI Updates
```

No manual page refresh should be necessary.

---

# 🧠 Personalization Logic

BriefDaily does not require machine learning for its core personalization.

A rule-based approach is sufficient.

## Step 1 — Topic Match

Articles are filtered based on selected topics.

```text
Selected Topics:

AI
Technology
Startups
```

Only matching articles appear in the primary digest.

---

## Step 2 — Recency

Articles are sorted by:

```text
publishedAt DESC
```

Newest articles appear first.

---

## Step 3 — Optional Relevance Score

For an enhanced version, articles can receive a relevance score.

Example:

```text
Topic Match       +10
Recent Article     +5
Previously Saved   +3
Featured           +2
────────────────────
Total              20
```

Articles can then be ordered using the score.

This is intentionally a lightweight rule-based system rather than a machine-learning model.

---

# 🗃 Local Storage

Persistent data should be stored locally.

## Bookmarks

Each saved article should contain:

```text
id
title
source
topic
imageUrl
summary
publishedAt
author
url
readingTime
bookmarkedAt
```

## Preferences

Store:

```text
selectedTopics
themePreference
onboardingCompleted
```

---

# 🎨 UI & Design System

BriefDaily follows an editorial design language.

The design should feel closer to a modern digital magazine than a generic dashboard.

---

## Typography

Typography hierarchy:

```text
Display
↓
Large editorial headlines

Headline
↓
Article titles

Title
↓
Section titles

Body
↓
Descriptions

Label
↓
Metadata
```

Example:

```text
YOUR DAILY BRIEF

32px / Bold
```

Article headline:

```text
New AI tools are changing
how developers build software

24px / SemiBold
```

Metadata:

```text
TechCrunch · 2h ago

12px / Medium
```

---

# 🎨 Color System

The exact colors can be defined in Figma and Flutter theme files.

Recommended visual direction:

### Light Theme

```text
Background
Off-white

Surface
White

Primary
Deep Blue

Text
Dark Charcoal

Secondary Text
Muted Grey
```

### Dark Theme

```text
Background
Near Black

Surface
Dark Grey

Primary
Blue

Text
Off White

Secondary Text
Muted Grey
```

---

# 🧩 Reusable UI Components

The application should use reusable components rather than duplicating UI.

Important components:

```text
ArticleCard
FeaturedArticleCard
BookmarkButton
TopicChip
TopicCard
SearchBar
DigestHeader
EmptyState
ErrorState
LoadingSkeleton
PrimaryButton
SecondaryButton
BottomNavigation
```

---

# 📐 Responsive Design

BriefDaily should adapt to different screen sizes.

## Mobile

Primary layout:

```text
Single column
```

Example:

```text
┌──────────────────────┐
│ Header               │
├──────────────────────┤
│ Featured Article     │
├──────────────────────┤
│ Article              │
├──────────────────────┤
│ Article              │
├──────────────────────┤
│ Article              │
├──────────────────────┤
│ Bottom Navigation    │
└──────────────────────┘
```

---

## Tablet

Use a wider layout:

```text
┌───────────┬─────────────────────────┐
│           │                         │
│ Navigation│     News Digest         │
│           │                         │
│ Home      │ ┌────────┐ ┌────────┐  │
│ Explore   │ │ Story  │ │ Story  │  │
│ Saved     │ └────────┘ └────────┘  │
│ Settings  │                         │
└───────────┴─────────────────────────┘
```

---

# 🧭 Navigation

Recommended navigation:

```text
Home
Explore
Bookmarks
Profile
```

Using Material 3:

```dart
NavigationBar
```

Navigation should preserve the state of each major section where appropriate.

---

# 📰 Article Model

Example model:

```dart
class Article {
  final String id;
  final String title;
  final String source;
  final String topic;
  final String imageUrl;
  final String summary;
  final String content;
  final DateTime publishedAt;
  final String author;
  final String url;
  final int readingTime;

  const Article({
    required this.id,
    required this.title,
    required this.source,
    required this.topic,
    required this.imageUrl,
    required this.summary,
    required this.content,
    required this.publishedAt,
    required this.author,
    required this.url,
    required this.readingTime,
  });
}
```

---

# 🏷 Topic System

Suggested topics:

```text
Technology
Artificial Intelligence
Startups
Business
Finance
Science
Space
Health
Sports
World
Politics
Climate
Gaming
Entertainment
Design
Cybersecurity
```

Topics should be represented as structured data rather than hardcoded UI labels.

Example:

```dart
class Topic {
  final String id;
  final String name;
  final String icon;
}
```

---

# 🔖 Bookmark System

The bookmark workflow is:

```text
Article
   ↓
Tap Bookmark
   ↓
Bookmark Provider
   ↓
Check Existing Bookmark
   ↓
Add / Remove
   ↓
Persist Locally
   ↓
Update UI
```

Bookmark state should be reactive.

If an article is bookmarked from the article detail page, the bookmark state should immediately reflect on the digest when the user returns.

---

# ⏳ Loading States

The application should have clear loading states.

Recommended:

```text
Loading Skeleton
```

instead of displaying:

```text
Loading...
```

Skeleton components should resemble the final article card.

---

# ⚠️ Error States

If data loading fails:

```text
Couldn't load your digest

Something went wrong while
loading your stories.

[Try Again]
```

The error state should provide a recovery action.

---

# ♿ Accessibility

Accessibility should be considered throughout development.

The application should support:

* Semantic labels
* Screen readers
* Large touch targets
* Text scaling
* Good color contrast
* Meaningful button labels
* Non-color-dependent status indicators

Example:

```dart
Semantics(
  label: 'Bookmark article',
  button: true,
  child: ...
)
```

---

# 🎨 Figma Design

Figma should contain the complete product journey.

## Required Frames

```text
01 — Splash
02 — Welcome
03 — Onboarding
04 — Topic Selection
05 — Topic Selection Selected
06 — Personalization
07 — Daily Digest
08 — Article Detail
09 — Bookmark Interaction
10 — Bookmarks
11 — Remove Bookmark
12 — Explore
13 — Edit Topics
14 — Profile
15 — Settings
16 — Dark Mode
17 — Tablet Layout
```

---

# 🧱 Figma Component System

Create reusable Figma components for:

```text
Buttons
Cards
Article Cards
Featured Cards
Topic Chips
Topic Cards
Navigation
App Bars
Bookmark Buttons
Search
Snackbars
Empty States
Loading States
```

Use variants for:

```text
Default
Selected
Pressed
Disabled
Bookmarked
Unbookmarked
```

---

# 🧪 Testing

Testing should cover the most important application logic.

## Unit Tests

Test:

* Article sorting
* Topic filtering
* Bookmark logic
* Preference persistence
* Relevance scoring

Example:

```text
Given selected topic = AI

When digest is generated

Then only AI articles
should appear in the filtered feed.
```

---

# Widget Tests

Test:

* Article card rendering
* Bookmark button
* Topic selection
* Empty states
* Navigation
* Search UI

---

# Integration Tests

Important journey:

```text
Launch App
 ↓
Choose Topics
 ↓
Continue
 ↓
Open Digest
 ↓
Open Article
 ↓
Bookmark Article
 ↓
Open Bookmarks
 ↓
Verify Article
 ↓
Remove Article
```

---

# 📦 Installation

## Requirements

Install:

* Flutter SDK
* Dart SDK
* Android Studio or Xcode
* VS Code or Android Studio
* Git

Verify Flutter:

```bash
flutter doctor
```

---

# 📥 Clone Repository

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd briefdaily
```

---

# 📦 Install Dependencies

Run:

```bash
flutter pub get
```

---

# ▶️ Run Application

Run on the connected device:

```bash
flutter run
```

Or specify a device:

```bash
flutter devices
```

Then:

```bash
flutter run -d <device-id>
```

---

# 🧹 Code Formatting

Format the project:

```bash
dart format .
```

---

# 🔍 Static Analysis

Run:

```bash
flutter analyze
```

The project should have no analyzer errors before committing.

---

# 🧪 Run Tests

Run all tests:

```bash
flutter test
```

---

# 🏗 Build Android

Debug:

```bash
flutter build apk --debug
```

Release:

```bash
flutter build apk --release
```

---

# 🍎 Build iOS

On macOS:

```bash
flutter build ios
```

---

# 🌐 Build Web

If web support is enabled:

```bash
flutter build web
```

---

# 🔐 Environment Configuration

If a real news API is introduced later, API keys should not be hardcoded into source files.

Use environment configuration.

Example:

```text
NEWS_API_KEY
NEWS_API_BASE_URL
```

Never commit:

```text
.env
```

or API credentials to Git.

---

# 🧑‍💻 Development Guidelines

## 1. Keep Widgets Small

Avoid putting the entire application into a single screen.

Bad:

```text
digest_screen.dart
→ 1000+ lines
```

Preferred:

```text
digest_screen.dart

article_card.dart
featured_article_card.dart
topic_chip.dart
digest_header.dart
```

---

## 2. Keep Business Logic Outside UI

Avoid:

```dart
onPressed: () {
  // Large filtering logic
  // Storage logic
  // Sorting logic
}
```

Instead:

```text
UI
 ↓
Provider
 ↓
Repository
```

---

## 3. Use Immutable State

State should preferably be represented using immutable models and state objects.

---

## 4. Avoid Hardcoded Strings

Use centralized constants where appropriate.

---

## 5. Avoid Hardcoded Colors

Colors should come from the application theme.

Instead of:

```dart
Colors.blue
```

prefer:

```dart
Theme.of(context).colorScheme.primary
```

---

## 6. Use Reusable Components

If the same UI appears more than once, consider turning it into a reusable widget.

---

# 🔮 Future Enhancements

The current version can later evolve into a production news platform.

Potential improvements include:

## Real News API

Replace mock data with a real news service.

```text
News API
   ↓
Repository
   ↓
Riverpod
   ↓
Flutter UI
```

---

## Offline Mode

Cache articles locally and allow users to read previously loaded content without an internet connection.

---

## Push Notifications

Send:

```text
Your Morning Brief is Ready
```

or:

```text
5 new stories match your interests
```

---

## Advanced Personalization

Use reading behavior to improve recommendations.

Potential signals:

```text
Topics selected
Articles opened
Articles bookmarked
Reading time
Search history
```

---

## Reading History

Track recently opened articles.

```text
Recently Read

AI changes software development
30 minutes ago

The future of robotics
Yesterday
```

---

## Share Articles

Allow users to share stories.

```text
Share
```

using the platform's native share functionality.

---

## Deep Linking

Allow links such as:

```text
briefdaily://article/article_001
```

to open a specific article.

---

## Cloud Sync

Future versions could synchronize:

* Bookmarks
* Preferences
* Reading history
* User account

across devices.

---

# 📊 Project Deliverables

The final submission should contain:

## 1. Figma Design

Complete flow:

```text
Topic Selection
        ↓
Digest
        ↓
Article
        ↓
Bookmark
        ↓
Bookmarks
```

---

## 2. Flutter UI

Implemented:

* Topic picker
* Digest
* Article cards
* Article detail
* Bookmarks
* Explore
* Settings

---

## 3. Material 3 Theme

Includes:

* Editorial typography
* Light theme
* Dark theme
* Consistent spacing
* Component styling

---

## 4. Riverpod Logic

Includes:

* Topic state
* Digest filtering
* Article sorting
* Bookmark state
* Preference state

---

## 5. Local Storage

Persistent:

* Selected topics
* Bookmarks
* Preferences

---

## 6. Responsive Prototype

Supported:

* Mobile
* Tablet

---

# 📝 Evaluation Mapping

BriefDaily directly addresses the project requirements.

| Requirement          | BriefDaily Implementation         |
| -------------------- | --------------------------------- |
| Topic Selection      | Interactive topic cards/chips     |
| News Digest          | Personalized article feed         |
| Bookmarks            | Persistent bookmark system        |
| ListView             | Article lists                     |
| Card                 | Article cards                     |
| Icon                 | Bookmark/navigation/topic icons   |
| Material 3           | Application-wide Material 3 theme |
| Editorial Typography | Custom headline hierarchy         |
| Riverpod             | Reactive application state        |
| Topic Filtering      | Digest reacts to selected topics  |
| Persistent Bookmarks | Local storage                     |
| Remove Bookmarks     | Delete/swipe action               |
| Latest First         | Publication timestamp sorting     |
| Figma                | Complete guided user flow         |
| Responsive           | Mobile and tablet layouts         |

---

# 🏆 What Makes BriefDaily Stand Out

BriefDaily goes beyond the minimum assignment requirements by combining the required functionality into a coherent product experience.

The project demonstrates:

### Product Thinking

Users are guided through:

```text
Discover
→ Personalize
→ Read
→ Save
→ Return
```

### Reactive State Management

Changing a topic immediately changes the digest through Riverpod.

### Persistent State

Bookmarks and preferences survive application restarts.

### Editorial UI

The design emphasizes typography, hierarchy, whitespace, and content readability.

### Production-Oriented Architecture

The application separates:

```text
UI
State
Business Logic
Repositories
Storage
```

### Responsive Design

The same product adapts to mobile and tablet layouts.

### User Experience

The project includes:

* Loading states
* Empty states
* Error states
* Undo actions
* Swipe interactions
* Dark mode
* Search
* Article details
* Topic management

---

# 📌 Core Product Principle

The application should always prioritize:

```text
RELEVANCE
    +
SIMPLICITY
    +
READABILITY
    +
PERSONALIZATION
```

BriefDaily should not feel like a generic list of news articles.

It should feel like a **personal daily briefing**.

---

# 🗺️ Development Roadmap

## Phase 1 — Project Setup

* [x] Create Flutter project
* [x] Configure Material 3
* [x] Configure folder architecture
* [x] Add Riverpod
* [x] Add local storage
* [x] Configure theme

---

## Phase 2 — Data Layer

* [x] Create Article model
* [x] Create Topic model
* [x] Create mock article dataset (Replaced with live API)
* [x] Create repositories
* [x] Implement local storage (Migrated to Firebase)

---

## Phase 3 — Onboarding

* [x] Splash screen
* [x] Welcome screen
* [x] Onboarding
* [x] Topic selection
* [x] Topic persistence
* [x] Personalization screen

---

## Phase 4 — Digest

* [x] Home screen
* [x] Digest header
* [x] Featured article
* [x] Article cards
* [x] Topic filtering
* [x] Latest-first sorting
* [x] Pull-to-refresh

---

## Phase 5 — Article Experience

* [x] Article detail
* [x] Hero image
* [x] Article metadata
* [x] Reading time
* [x] Bookmark action
* [x] Reading progress

---

## Phase 6 — Bookmarks

* [x] Bookmark provider
* [x] Bookmark persistence
* [x] Bookmarks screen
* [x] Remove bookmark
* [x] Swipe-to-delete
* [x] Undo action
* [x] Empty state

---

## Phase 7 — Explore & Preferences

* [x] Explore screen
* [x] Search
* [x] Topic filtering
* [x] Edit interests
* [x] Settings
* [x] Theme switching

---

## Phase 8 — Polish

* [x] Loading skeletons
* [x] Error states
* [x] Animations
* [x] Accessibility
* [x] Responsive tablet UI
* [x] Dark mode
* [x] UI consistency

---

## Phase 9 — Testing

* [x] Model tests
* [x] Provider tests
* [x] Repository tests
* [x] Widget tests
* [x] Integration tests

---

## 🚀 Phase 11 & 12 — Extra Premium Features
* [x] **Real Cloud Backend (Firebase):** Live user Authentication (Login/Signup).
* [x] **Live Global News (NewsAPI):** Live global headlines instead of mock data.
* [x] **Text-to-Speech (TTS):** Article dictation for accessibility.
* [x] **Gamification:** Consecutive daily reading streak tracking.

---

## Phase 10 — Final Submission

* [ ] Final Figma prototype
* [x] README Updated
* [ ] Screenshots
* [ ] Demo video
* [ ] Source code
* [ ] APK
* [ ] Test results
* [ ] Project presentation

---



## 📸 Screenshots & Demo

Here is a look at the final application in action!

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
  <img src="docs/screenshot_1.png" width="200" />
  <img src="docs/screenshot_2.png" width="200" />
  <img src="docs/screenshot_3.png" width="200" />
  <img src="docs/screenshot_4.png" width="200" />
  <img src="docs/screenshot_5.png" width="200" />
  <img src="docs/screenshot_6.png" width="200" />
</div>

### 🎥 Demo Video & Documentation
- [Watch the Demo Video](docs/demo_video.mov)
- [View the Project Documentation (PDF)](docs/Briefdaily.pdf)


The final README can include screenshots for:

```text
01 — Welcome
02 — Topic Selection
03 — Personalized Digest
04 — Article Detail
05 — Bookmark
06 — Bookmarks
07 — Explore
08 — Edit Interests
09 — Dark Mode
10 — Tablet Layout
```

Example:

```markdown
![BriefDaily Digest](docs/screenshots/digest.png)
```

Recommended documentation structure:

```text
docs/
└── screenshots/
    ├── welcome.png
    ├── topics.png
    ├── digest.png
    ├── article.png
    ├── bookmarks.png
    ├── explore.png
    ├── settings.png
    ├── dark-mode.png
    └── tablet.png
```

---

# 📄 License

This project is created as a Flutter application project for educational and demonstration purposes.

License details can be updated depending on the final distribution requirements.

---

# 👨‍💻 Project Status

```text
Status: Completed / Ready for Production

UI:                ✅
Riverpod:          ✅
Local Storage:     ✅ (Migrated to Firebase)
Personalization:   ✅
Figma:             🚧 (Pending User Design)
Testing:           ✅
Documentation:     ✅
```

---

# 📰 BriefDaily

> **Your news. Your interests. Your daily brief.**

BriefDaily transforms a large collection of news stories into a focused, personalized reading experience.

The application demonstrates modern Flutter development through:

**Flutter + Dart + Riverpod + Material 3 + Local Persistence + Responsive UI + Editorial Design**

---

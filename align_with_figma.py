import os
import subprocess

def replace_in_file(filepath, old, new):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Update theme
theme_code = """import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // Figma matched colors
  static const Color primaryBlue = Color(0xFF2563EB);
  static const Color lightBackground = Color(0xFFF8FAFC);
  static const Color darkBackground = Color(0xFF0F172A);

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryBlue,
        brightness: Brightness.light,
        surface: lightBackground,
        primary: primaryBlue,
      ),
      textTheme: GoogleFonts.interTextTheme(ThemeData.light().textTheme),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: false,
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryBlue,
        brightness: Brightness.dark,
        surface: darkBackground,
        primary: primaryBlue,
      ),
      textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: false,
      ),
    );
  }
}
"""
os.makedirs('lib/app/theme', exist_ok=True)
with open('lib/app/theme/app_theme.dart', 'w') as f:
    f.write(theme_code)

# 2. Update home_screen to ensure Greeting & Streak match Figma
replace_in_file('lib/features/digest/home_screen.dart', 
    "title: const Text('BriefDaily', style: TextStyle(fontWeight: FontWeight.bold))",
    """title: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Good morning, User', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
              Text('Here is your daily brief', style: TextStyle(fontSize: 14, color: Colors.grey)),
            ],
          ),
          actions: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Row(
                children: [
                  const Icon(Icons.local_fire_department, color: Colors.orange),
                  const SizedBox(width: 4),
                  Text('5', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                ],
              ),
            ),
          ]"""
)

print("Figma alignment changes written.")

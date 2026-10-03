import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/article.dart';

class NewsService {
  static const String _apiKey = String.fromEnvironment('NEWS_API_KEY');
  static const String _baseUrl = 'https://newsapi.org/v2';

  Future<List<Article>> fetchTopHeadlines(List<String> topics) async {
    List<Article> allArticles = [];

    if (topics.isEmpty) {
      topics = ['general'];
    }

    final targetTopics = topics;

    try {
      for (var topic in targetTopics) {
        final query = topic.toLowerCase();
        final url = Uri.parse(
          '$_baseUrl/everything?q=$query&language=en&sortBy=publishedAt&pageSize=10&apiKey=$_apiKey',
        );
        final response = await http.get(url);

        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          final articles = data['articles'] as List;

          for (var articleJson in articles) {
            if (articleJson['title'] != '[Removed]') {
              allArticles.add(Article.fromJson(articleJson, topic));
            }
          }
        }
      }

      allArticles.sort((a, b) => b.publishedAt.compareTo(a.publishedAt));
      return allArticles;
    } catch (e) {
      return [];
    }
  }

  Future<List<Article>> searchArticles(String query) async {
    if (query.trim().isEmpty) return [];
    final url = Uri.parse(
      '$_baseUrl/everything?q=$query&language=en&sortBy=publishedAt&pageSize=20&apiKey=$_apiKey',
    );

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        final List<dynamic> articlesJson = data['articles'];

        return articlesJson
            .map((json) => Article.fromJson(json, 'Search Result'))
            .toList();
      } else {
        throw Exception('Failed to load search results');
      }
    } catch (e) {
      throw Exception('Failed to search: $e');
    }
  }
}

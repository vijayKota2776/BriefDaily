import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/article.dart';

class NewsService {
  static const String _apiKey = '96d4841970994aeca6abd3ea7663d8db';
  static const String _baseUrl = 'https://newsapi.org/v2';

  Future<List<Article>> fetchTopHeadlines(List<String> topics) async {
    List<Article> allArticles = [];
    
    if (topics.isEmpty) {
      topics = ['general'];
    }

    final targetTopics = topics.take(2).toList();

    try {
      for (var topic in targetTopics) {
        final query = topic.toLowerCase();
        final url = Uri.parse('$_baseUrl/everything?q=$query&language=en&sortBy=publishedAt&pageSize=10&apiKey=$_apiKey');
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
      
      allArticles.shuffle();
      return allArticles;
    } catch (e) {
      return [];
    }
  }
}

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class IngredientProvider extends ChangeNotifier {
  // List to store analysis results from backend
  List<Map<String, String>> _analysisResults = [];

  List<Map<String, String>> get analysisResults => _analysisResults;

  // Modified the method to accept Map<String, String> instead of String
  Future<void> analyzeIngredients(Map<String, String> ingredients) async {
    try {
      final response = await http.post(
        Uri.parse('http://your-backend-url/check_ingredients'),  // Replace with actual backend URL
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'ingredients': ingredients}),  // Pass the map directly
      );

      if (response.statusCode == 200) {
        final List<dynamic> results = jsonDecode(response.body);
        // Map the response to your list of analysis results
        _analysisResults = results.map((item) => {
          'ingredient': item['ingredient'].toString(),
          'status': item['status'].toString(),
        }).toList();
        notifyListeners();  // Notify listeners to update UI
      } else {
        print('Failed to analyze ingredients.');
      }
    } catch (e) {
      print('Error: $e');
    }
  }
}

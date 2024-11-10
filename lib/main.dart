import 'package:flutter/material.dart';
import 'package:provider/provider.dart';  // Importing the provider package
import 'screens/ocr_screen.dart';  // Importing the OCR screen
import 'providers/ingredient_provider.dart';  // Import the IngredientProvider

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => IngredientProvider(),  // Providing the IngredientProvider to the widget tree
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'SmartEats',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: OcrScreen(),  // The home screen is set to OcrScreen
      ),
    );
  }
}

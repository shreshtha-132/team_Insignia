import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import '../services/ocr_service.dart';
import '../providers/ingredient_provider.dart';

class OcrScreen extends StatefulWidget {
  @override
  _OcrScreenState createState() => _OcrScreenState();
}

class _OcrScreenState extends State<OcrScreen> {
  File? _image;
  Map<String, String>? _ocrResults;

  // Pick image from gallery
  Future<void> _pickImage() async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  // Send image to OCR service and analyze ingredients
  Future<void> _scanImage() async {
    if (_image != null) {
      final ocrText = await OcrService.scanImage(_image!);
      if (ocrText != null) {
        Provider.of<IngredientProvider>(context, listen: false).analyzeIngredients(ocrText);
        setState(() {
          _ocrResults = ocrText;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Center(child: Text("SmartEats"))),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _image != null ? Image.file(_image!) : Text("No image selected."),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: Text("Pick Image"),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _scanImage,
              child: Text("Scan Image"),
            ),
            SizedBox(height: 20),
            Consumer<IngredientProvider>(
              builder: (context, ingredientProvider, child) {
                return ingredientProvider.analysisResults.isNotEmpty
                    ? Expanded(
                  child: ListView.builder(
                    itemCount: ingredientProvider.analysisResults.length,
                    itemBuilder: (context, index) {
                      final result = ingredientProvider.analysisResults[index];
                      return ListTile(
                        title: Text(result['ingredient']!),
                        trailing: Text(result['status']!),
                      );
                    },
                  ),
                )
                    : Text("No health concerns found.");
              },
            ),
          ],
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import '../services/ocr_service.dart';
import '../providers/ingredient_provider.dart';
import 'package:provider/provider.dart';

class ImageCaptureScreen extends StatefulWidget {
  @override
  _ImageCaptureScreenState createState() => _ImageCaptureScreenState();
}

class _ImageCaptureScreenState extends State<ImageCaptureScreen> {
  final ImagePicker _picker = ImagePicker();
  File? _image;

  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await _picker.pickImage(source: source);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
      _analyzeImage();
    }
  }

  Future<void> _analyzeImage() async {
    if (_image == null) return;
    final ingredientProvider = Provider.of<IngredientProvider>(context, listen: false);
    final ocrText = await OcrService.scanImage(_image!);
    if (ocrText != null) {
      ingredientProvider.analyzeIngredients(ocrText);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Center(child: Text('Ingredient Safety Scanner'))),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_image != null) Image.file(_image!),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _pickImage(ImageSource.camera),
              child: Text('Capture Image'),
            ),
            ElevatedButton(
              onPressed: () => _pickImage(ImageSource.gallery),
              child: Text('Select from Gallery'),
            ),
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
                    : Text('No results to display.');
              },
            ),
          ],
        ),
      ),
    );
  }
}

import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

class OcrService {
  static const String apiUrl = 'http://192.168.0.204:5000/process-image';  // Update with backend URL



  static Future<Map<String, String>?> scanImage(File imageFile) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));
      request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));

      final response = await request.send();
      if (response.statusCode == 200) {
        final responseData = await response.stream.bytesToString();
        final parsedData = jsonDecode(responseData);
        return Map<String, String>.from(parsedData);  // Convert parsed data to a map
      } else {
        print('Failed to scan image.');
        return null;
      }
    } catch (e) {
      print('Error: $e');
      return null;
    }
  }
}

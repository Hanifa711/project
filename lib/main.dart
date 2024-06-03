import 'package:flutter/material.dart';
import 'package:ir_front/search_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: SearchScreen(),
      theme: ThemeData(),
    );
  }
}

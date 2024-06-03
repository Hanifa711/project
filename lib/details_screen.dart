import 'package:flutter/material.dart';

class DetailScreen extends StatelessWidget {
  final String title;
  final String description;

  DetailScreen({required this.title, required this.description});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Detail Screen',style:TextStyle(color:Colors.white)),
        backgroundColor: Colors.deepPurple,
        centerTitle: true,
        elevation: 0.5,
        ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
             Text(
              "Document ID : $title ",
              style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
            ),
            
            SizedBox(height: 16.0),
            Text("Content",style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),),
            SizedBox(height: 16.0),
            Expanded(
              child: SingleChildScrollView(
                child:Text(description),
              ),
            )
            
          ],
        ),
      ),
    );
  }
}

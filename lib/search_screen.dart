import 'package:flutter/material.dart';
import 'package:ir_front/controller.dart';
import 'package:ir_front/details_screen.dart';
import 'package:ir_front/shared.dart';

class SearchScreen extends StatefulWidget {
  @override
  _SearchScreenState createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  TextEditingController _searchController = TextEditingController();
  int datasetNumber=1;
  bool datasetOne=true;
  Controller myController=Controller();
  List<String> _searchSuggestions = [];
  List<String> filter1 = [];
  List<String> filter2 = [];

  Map _searchResults = {};
  List docIds=[];
  @override
  void initState() {
    super.initState();
    //SharedPreferencesHelper.clearList();
    _searchController.addListener(_onSearchChanged);
  }

  @override
  void dispose() {
    _searchController.removeListener(_onSearchChanged);
    _searchController.dispose();
    super.dispose();
  }

  void _onSearchChanged() async{
    List<String> historyList = await SharedPreferencesHelper.getStringList();
    
    String query = _searchController.text.toLowerCase();
    setState(() {
      if (query.isEmpty) {
        _searchSuggestions = [];
      } else {
       
        filter1 = (datasetNumber == 1 ? Controller.query1 : Controller.query2)
            .where((item) => item.toLowerCase().contains(query))
            .toList();
         filter2 = historyList
            .where((item) => item.toLowerCase().contains(query))
            .toList();   

         _searchSuggestions=filter1+filter2;    
      }
    });
  }

  void _performSearch(BuildContext context) async{
       _searchResults.clear();
       await myController.getSearchResult(datasetNumber: datasetNumber,query: _searchController.text);
       await myController.getCorrectedQuery(query: _searchController.text);
       myController.correctedQuery.isEmpty? null:await SharedPreferencesHelper.addItemToList(myController.correctedQuery);
    setState(() {
      _searchResults = myController.result;
      docIds=_searchResults.keys.toList();
      _searchSuggestions = []; 
       if(_searchResults.isEmpty){
         showAlertDialog(context);
      }
    });
  }

  void _onItemTap(String id,String content) {
    Navigator.push(
      context,
      MaterialPageRoute(
          builder: (context) =>
              DetailScreen(title: id, description: content)),
    );
  }

showAlertDialog(context) {    
  // set up the button
  Widget okButton = TextButton(
    child: Text("OK"),
    onPressed: () {
      Navigator.pop(context);
     },
  );

  // set up the AlertDialog
  AlertDialog alert = AlertDialog(
    
    title: Text("No data found"),
    content: Text("Try again with different query"),
    actions: [
      okButton,
    ],
  );

  // show the dialog
  showDialog(
    barrierDismissible: false,
    context: context,
    builder: (BuildContext context) {
      return alert;
    },
  );
}
 
  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: const Text('Search Screen',style:TextStyle(color:Colors.deepPurple),),
        backgroundColor: Colors.white,
        centerTitle: true,
        elevation: 0.5,
        
        ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Container(
          height: MediaQuery.of(context).size.height,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
        
                  SizedBox(
                    width: MediaQuery.of(context).size.width * 0.7,
                    child: TextField(
                      cursorColor:Colors.deepPurple ,
                      controller: _searchController,
                      decoration: InputDecoration(
                        hintText: 'Enter your search query',
                        filled: true,
                        fillColor: Colors.grey[100],
                        border: OutlineInputBorder(
                            borderSide: BorderSide(color: Colors.deepPurple),
                            borderRadius: BorderRadius.circular(8.0)),
                      focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(color: Colors.deepPurple),
                            borderRadius: BorderRadius.circular(8.0)),
                      ),
                      
                    ),
                  ),
                  const SizedBox(width: 20),
                  IconButton(
                    onPressed:()=> _performSearch(context),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                    ),
                    icon: Icon(Icons.search,color: Colors.deepPurple,),
                  ),
                SizedBox(width: 100,),
                Column(children: [
                   TextButton(onPressed: (){
                    setState(() {
                      _searchSuggestions.clear();
                      _searchController.clear();
                      datasetNumber=1;
                      datasetOne=true;
        
                    });
                   }, child: Text("Dataset 1",style:TextStyle(color:datasetOne?Colors.deepPurple:Colors.grey),)),
                    SizedBox(height: 10,),
                   TextButton(onPressed: (){
                    setState(() {
                      _searchSuggestions.clear();
                      _searchController.clear();
                      datasetNumber=2;
                      datasetOne=false;
                    });
                   }, child: Text("Dataset 2",style:TextStyle(color:!datasetOne?Colors.deepPurple:Colors.grey))),
                ],)
            
            ],
              ),
              _searchSuggestions.isNotEmpty
                  ? SizedBox(
                      width: MediaQuery.of(context).size.width * 0.7,
                      height: MediaQuery.of(context).size.height * 0.5,
                      child: Container(
                        color: Colors.grey[200],
                        child: ListView.builder(
                          shrinkWrap: true,
                          itemCount: _searchSuggestions.length,
                          itemBuilder: (context, index) {
                            return ListTile(
                              title: Text(_searchSuggestions[index]),
                              onTap: () {
                                _searchController.text =_searchSuggestions[index];
                                // _onItemTap(_searchSuggestions[index]);
                                _searchSuggestions = [];
                                     // Clear suggestions list; // Close suggestions list
                              },
                            );
                          },
                        ),
                      ),
                    )
                  : const SizedBox.shrink(),
              const SizedBox(height: 16.0),
              Expanded(
                child:Column(children: [
                myController.correctedQuery.isNotEmpty?
                TextButton(onPressed: (){
                  _searchController.text=myController.correctedQuery;
                  _searchResults.clear();
                },
                child: Text("Do you mean : ${myController.correctedQuery} ",style:TextStyle(color:Colors.deepPurple))):Container(),
                Expanded(
                child: ListView.builder(
                  itemCount: _searchResults.length,
                  itemBuilder: (context, index) {
                    return GestureDetector(
                      onTap: () {
                        String key = docIds[index];
                        String value = _searchResults[key]!;
                        _onItemTap(key,value);
                      } ,
                      child: Card(
                        elevation: 4.0,
                        margin: const EdgeInsets.symmetric(vertical: 8.0),
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Text(docIds[index]),
                        ),
                      ),
                    );
                  },
                ),
              ),
                ]) ,
              ),
             
            ],
          ),
        ),
      ),
    );
  }
}

import 'package:ir_front/controller.dart';
import 'package:shared_preferences/shared_preferences.dart';


class SharedPreferencesHelper {
  static const String _key = 'my_string_list';
  

  static Future<void> saveStringList(List<String> list) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setStringList(_key, list);
  }

  static Future<List<String>> getStringList() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getStringList(_key) ?? [];
  }

  static Future<void> addItemToList(String item) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    List<String> currentList = prefs.getStringList(_key) ?? [];
    if (!currentList.contains(item) && !Controller.query1.contains(item) && !Controller.query2.contains(item)) {
      currentList.add(item);
      await prefs.setStringList(_key, currentList);
    }
  }

  static Future<void> removeItemFromList(String item) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    List<String> currentList = prefs.getStringList(_key) ?? [];
    currentList.remove(item);
    await prefs.setStringList(_key, currentList);
  }

  static Future<void> clearList() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
  }
}

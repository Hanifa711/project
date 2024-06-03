class Normalization:
 
    @staticmethod
    def normalize(city):  
       us=["us army medical research acquisition activity ",
            "us army medical research materiel command ",
             " us army office surgeon general ",
               "us bioscience" ,
               "us biotest inc" ,
               "us committee refugees immigrants", 
               "us cosmeceutechs llc" ,
               "us department education", 
               "us epa human studies facility", 
               "us oncology research", 
               "us worldmeds llc" ,
               "us wound registry" 
               ]
       uni=["universitaire","universitas","universitat","universite","universiteit","universitet","universiti","universidad","universidade","universita","universitã","universitã©","universitaet","universitair","universiti","universiteit","universite","universitat","universitas","universitaire",'universitätsklinikum','universität']    
       madrid=["madrid community" ,"madrid/madrid","madrid / madrid","spain/madrid"]
       outside_us=["outside aus","outside u canada","outside usa" ,"outside us/canada/australia","outside u","outside u /canada"]
       sao_paulo=["saop paulo" ,"sã£o paulo state" ,"saãµ paulo" ,"sã£o paulo" ,"sã¢o paulo" ,"sao apaulo" ,"sã£o paulo/ sp","sp/brazil" , "sã£o paulo/mogi das cruzes","saop paulo","sao paulo brazil","sp - sao paulo" ,"sã£o paulo/sp" ,"sao paulo sp" , "sao paulo/sp"]
       if city.lower() == "syrian arab ":
        print(city)
        return "syria"
       if city.lower() == "palestinian territory" or city.lower() =="palestinian territories":
        print(city)
        return "palestine"
       if city.lower() == "virgin islands (u.s.)":
        print(city)
        return "virgin islands"
       if city.lower() == "holy see (vatican city state)" or city.lower() == "vatican city":
        print(city)
        return "holy see"
       if city.lower() == "central african":
        print(city)
        return "africa"
       if city.lower() == "russian federation":
        print(city)
        return "russia"  
       if city.lower() == "united arab emirates" :
        print(city)
        return "emirates"   
       if city.lower() == "dominican " :
        print(city)
        return "dominic" 
       if city.lower() == "federated states of micronesia" :
        print(city)
        return "micronesia"
       if city.lower() == "lao people's democratic " or city.lower() == "lao people":
        print(city)
        return "lao"   
       if city.lower() == "libyan arab jamahiriya":
        print(city)
        return "libya" 
       if city.lower() == "mi":
        print(city)
        return "michigan " 
       for item in sao_paulo:
        if item.lower() == city.lower():
          print(city)
          return "sao paulo"
       for item in madrid:
        if item.lower() == city.lower():
          print(city)
          return "madrid"   
       for item in outside_us:
        if item.lower() == city.lower():
          print(city)
          return "outside us"          
       if city.lower() == "nt/kln":
        print(city)
        return "hong kong"  
       if city.lower() == "c.p":
        print(city)
        return "connaught place delhi"   
       if city.lower() == "cz" or city.lower() == "czech republic" or city.lower() == "cze" :
        print(city) 
        return "czech"   
       if city.lower() == "portalex" or city.lower() == "portalix" :
        print(city) 
        return "portalix"    
       if city.lower() == "ts":
        print(city) 
        return "Teesside"    
       if city.lower() == "es" :
        print(city) 
        return "spain"     
       if city.lower() == "ar" :
        print(city) 
        return "arkansaa"
       for item in uni:
        if item.lower() in city.lower():
          print(city) 
          #return item.replace(item.lower(),'university') 
          return 'university'
       for item in us:
        if item.lower() == city.lower():
           print(city) 
           return item.replace('us','united states')
       if "prof " in city.lower():
          print(city) 
          return item.replace("prof",'professor')  
       if "covid " == city.lower() or "coronavirus " == city.lower():
          print(city) 
          return "covid"
      #  if "dr " in city.lower():
      #     print(city) 
      #     return item.replace("dr",'doctor')   
       else:
          return city.lower()
        
#aalborg aarhus abbott active
#normalized_city = Normalization.normalize_city(city)    
# city_name = "palestinian territories"  # Or any other city name
# normalized_city = Normalization.normalize(city_name)
# print(normalized_city)
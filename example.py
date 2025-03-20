
from abc import ABC, abstractmethod

# Tworzymy interfejs, który będzie dziedziczony przez konkretne klasy
class Localizer(ABC):
    @abstractmethod
    def localize(self, msg):
        pass

    
# Tworzymy konkretne klasy słowników
class PolishLocalizer(Localizer):
    # Konstruktor
    def __init__(self):
        self.translations = {
          "car": "samochód",
          "bike": "rower",
          "scooter": "skuter"
        }
        
    # Metoda wykonująca konkretną pracę
    def localize(self, msg):
        return self.translations.get(msg, msg)

class GermanLocalizer(Localizer):
    
    def __init__(self):
        self.translations = {
          "car": "das auto",
          "bike": "fahrrad",
          "scooter": "roller"
        }

    def localize(self, msg):
        return self.translations.get(msg, msg)

class EnglishLocalizer(Localizer):
    # To jest język oryginału, więc nic nie robimy
    def localize(self, msg):
        return msg
    

# Tutaj jest abstrakcyjna klasa tworząca (Creator)
# W zamysle tu będziemy tworzyć obiekt konkretnej klasy
class LocalizerFactory(ABC):
    
    @abstractmethod
    def create_localizer(self):
        pass
    
    
# Tutaj są implementacje konkretnych klas tworzących
class GermanLocalizerFactory(LocalizerFactory):
    
    def create_localizer(self):
        return GermanLocalizer()

class PolishLocalizerFactory(LocalizerFactory):
    
    def create_localizer(self):
        return PolishLocalizer()

class EnglishLocalizerFactory(LocalizerFactory):
    def create_localizer(self):
        return EnglishLocalizer()
  
    
# Tu wykorzystujemy obiekty
if __name__ == "__main__":
    
    f = GermanLocalizerFactory()
    e = EnglishLocalizerFactory()
    s = PolishLocalizerFactory()

    message = ["car", "bike", "scooter"]

    for msg in message:
        print(f.create_localizer().localize(msg))
        print(e.create_localizer().localize(msg))
        print(s.create_localizer().localize(msg))
        
        
# Alternatywnie:
    
#    def create_localizer(language="English"):
#    
#    localizers = {
#        "German": GermanLocalizer,
#        "English": EnglishLocalizer,
#        "Polish": PolishLocalizer,
#    }
#    return localizers[language]()

#if __name__ == "__main__":
#    german_localizer = create_localizer("German")
#    english_localizer = create_localizer("English")
#    polsih_localizer = create_localizer("Polish")

#    message = ["car", "bike", "scooter"]

#    for msg in message:
#        print(german_localizer.localize(msg))
#        print(english_localizer.localize(msg))
#        print(polish_localizer.localize(msg))
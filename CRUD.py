from abc import ABC, abstractmethod
import json
import csv
import xml.etree.ElementTree as ET

class obslugaPlikow(ABC):
    @abstractmethod
    def create(self,data):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self,data):
        pass

    @abstractmethod
    def delete(self,id):
        pass


class XMLHandler(obslugaPlikow):
    def __init__(self, filename):
        self.filename = filename

    def create(self, data):
        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("records")

        record = ET.SubElement(root, "record")
        for key, value in data.items():
            ET.SubElement(record, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(self.filename)

    def read(self):
        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()
            records = {}

            # Pobieramy pojedyncze wartości (legionName, homeworld, itp.)
            for child in root:
                if child.tag != "members":
                    records[child.tag] = child.text.strip() if child.text else None
                else:
                    if "members" not in records:
                        records["members"] = []
                    
                    # Przetwarzamy członków legionu
                    for member in root.findall("members"):
                        member_data = {}
                        battles = []

                        for element in member:
                            if element.tag == "battles":
                                battles.append(element.text.strip())
                            else:
                                member_data[element.tag] = element.text.strip() if element.text else None

                        member_data["battles"] = battles
                        records["members"].append(member_data)

            return records
        except (FileNotFoundError, ET.ParseError):
            return {}

    def update(self, updated_data):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        for record in root.findall("record"):
            if record.find("id").text == str(updated_data["id"]):
                for key, value in updated_data.items():
                    element = record.find(key)
                    if element is not None:
                        element.text = str(value)

        tree.write(self.filename)

    def delete(self, id):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        for record in root.findall("record"):
            if record.find("id").text == str(id):
                root.remove(record)

        tree.write(self.filename)

class CSVHandler(obslugaPlikow):
    def __init__(self, filename):
        self.filename = filename

    def create(self, data):
        file_exists = False
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.reader(file)
                file_exists = any(reader)  # Sprawdzamy, czy plik już istnieje
        except FileNotFoundError:
            pass  # Jeśli plik nie istnieje, utworzymy go później

        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            if not file_exists:
                writer.writeheader()  # Tylko jeśli plik nie istnieje, zapisz nagłówki
            
            writer.writerow(data)

    def read(self):
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []

    def update(self, updated_data):
        data = self.read()
        for row in data:
            if row["id"] == str(updated_data["id"]):  # CSV przechowuje ID jako string
                row.update(updated_data)

        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=updated_data.keys())
            writer.writeheader()
            writer.writerows(data)

    def delete(self, id):
        data = self.read()
        data = [row for row in data if row["id"] != str(id)]  # Usuwamy po ID

        with open(self.filename, "w", newline="") as file:
            if data:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

class JSONHandler(obslugaPlikow):
    def __init__(self, filename):
        self.filename = filename

    def create(self, data):
        try:
            with open(self.filename, "r") as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []
        
        existing_data.append(data)
        with open(self.filename, "w") as file:
            json.dump(existing_data, file, indent=4)

    def read(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update(self, updated_data):
        data = self.read()
        for record in data:
            if record.get("id") == updated_data.get("id"):
                record.update(updated_data)  # Aktualizujemy tylko znaleziony rekord

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def delete(self, id):
        data = self.read()
        data = [record for record in data if record.get("id") != id]  # Usuwamy po ID

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)


class FileHandlerFactory:
    @staticmethod
    def get_handler(filetype,filename):
        if filetype == "json":
                return JSONHandler(filename)
        elif filename == "csv":
            return CSVHandler(filename)
        elif filename == "xml":
            return XMLHandler(filename)
        else:
            raise ValueError("Nieobsługiwany format pliku")
        

handlerCSV = CSVHandler("Dane/marines_data.csv")
handlerJSON = JSONHandler("Dane/marines_data.json")
handlerXML = XMLHandler("Dane/marines_data.xml")





####################################################                         XML                         #############################################
filename = "Dane/marines_data.xml" 

try:
    tree = ET.parse(filename)
    root = tree.getroot()
    print("XML został wczytany poprawnie!")
    print("Root tag:", root.tag)
    print("Dzieci root:", [child.tag for child in root])
except ET.ParseError:
    print("BŁĄD: Plik XML jest uszkodzony!")
except FileNotFoundError:
    print("BŁĄD: Nie znaleziono pliku!")
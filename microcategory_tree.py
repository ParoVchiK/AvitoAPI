rawCategories = {
    "Бытовая электроника": {"Товары для компьютера", "Фототехника", "Телефоны", "Планшеты и электронные книги",
                            "Оргтехника и расходники", "Ноутбуки", "Настольные компьютеры",
                            "Игры, приставки и программы", "Аудио и видео"},
    "Готовый бизнес и оборудование": {"Готовый бизнес", "Оборудование для бизнеса"},
    "Для дома и дачи": {"Мебель и интерьер", "Ремонт и строительство", "Продукты питания", "Растения",
                        "Бытовая техника", "Посуда и товары для кухни"},
    "Животные": {"Другие животные", "Товары для животных", "Птицы", "Аквариум", "Кошки", "Собаки"},
    "Личные вещи": {"Детская одежда и обувь", "Одежда, обувь, аксессуары", "Товары для детей и игрушки",
                    "Часы и украшения", "Красота и здоровье"},
    "Недвижимость": {"Недвижимость за рубежом", "Квартиры", "Коммерческая недвижимость", "Гаражи и машиноместа",
                     "Земельные участки", "Дома, дачи, коттеджи", "Комнаты"},
    "Работа": {"Резюме", "Вакансии"},
    "Транспорт": {"Автомобили", "Запчасти и аксессуары", "Грузовики и спецтехника", "Водный транспорт",
                  "Мотоциклы и мототехника"},
    "Услуги": {"Предложения услуг"},
    "Хобби и отдых": {"Охота и рыбалка", "Спорт и отдых", "Коллекционирование", "Книги и журналы", "Велосипеды",
                      "Музыкальные инструменты", "Билеты и путешествия"},
}

categoryID = 0


class CategoryNode:
    ID = 0
    Name = ""
    Children = [0]
    Parent = None

    def __init__(self, ID, Name):
        self.Name = Name
        self.ID = ID
        self.Children = []

    def addChild(self, child):
        self.Children.append(child)
        child.Parent = self


categoryList = []


def newCategory(name) -> CategoryNode:
    global categoryID
    categoryID += 1
    return CategoryNode(categoryID, name)


def getCategoriesTree() -> CategoryNode:
    rootNode = newCategory("ROOT")
    categoryList.append(rootNode)

    for category in rawCategories:
        categoryNode = newCategory(category)
        categoryList.append(categoryNode)

        for subCategory in rawCategories[category]:
            subCategoryNode = newCategory(subCategory)
            categoryNode.addChild(subCategoryNode)
            categoryList.append(subCategoryNode)

        rootNode.addChild(categoryNode)

    return rootNode


mainNode = getCategoriesTree()
nodes_dict = {node.ID: node for node in categoryList}


def getCategoriesWithID(mID):

    all_ids = []
    curNode = nodes_dict.get(mID)

    while curNode:
        all_ids.append(curNode.ID)
        curNode = curNode.Parent

    if all_ids == []:
        all_ids.append(1)

    return all_ids


def getChildrenCategories(mID):
    children = []
    for child in nodes_dict.get(mID).Children:
        children.append({'Name': child.Name, 'ID': child.ID})
    return children


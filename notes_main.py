from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

app = QApplication([])

notes = {
    'Добро пожаловать!':{
        'текст': 'Это самое лучшее приложение длязаметок в мире!',
        'теги' : ['добро','инструкция']
    }
}
    
with open('notes_data.json', 'w') as file:
    json.dump(notes, file)

notes_win=QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)

#Виджеты
list_notes = QListWidget()
list_tag = QListWidget()
list_notes_label = QLabel('Список заметок')
list_tags_label = QLabel('Список тегов')

field_text = QTextEdit()

button_add = QPushButton('Создать заметку')
button_del = QPushButton('Удалить заметку')
button_save = QPushButton('Сохранить заметку')
button_add_tag = QPushButton('Добавить к зметке')
button_del_tag = QPushButton('Открепить от заметки')
button7 = QPushButton('Искать заметки по тегу')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')
# layout
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

col_3 = QHBoxLayout()
col_3.addWidget(button_add)
col_3.addWidget(button_del)
col_2.addLayout(col_3)

col_2.addWidget(button_save)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tag)
col_2.addWidget(field_tag)

col_4 = QHBoxLayout()
col_4.addWidget(button_add_tag)
col_4.addWidget(button_del_tag)
col_2.addLayout(col_4)
col_2.addWidget(button7)

layout_notes.addLayout(col_1,stretch=2)
layout_notes.addLayout(col_2,stretch=1)
notes_win.setLayout(layout_notes)

#Функционал приложения
def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tag.clear()
    list_tag.addItems(notes[name]['теги'])

#добавление заметки
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги': []}
        list_notes.addItem(note_name)

#удаление заметок
def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags_label.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана')

#Сохранение заметки
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для сохранения не выбрана')

#Добавление тегов
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tag.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
#Удаление тегов
def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print('Заметка для удаления не выбрана')
#Поиск заметок по тегу
def search_tag():
    tag = field_tag.text()
    if button7.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        button7.setText('Сбросить поиск')
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes_filtered)
    elif button7.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        button7.setText('Искать заметки по тегу')
    else:
        pass

        

#подключать обработку событий
list_notes.itemClicked.connect(show_note)
button_add.clicked.connect(add_note)
button_del.clicked.connect(del_note)
button_save.clicked.connect(save_note)
button_add_tag.clicked.connect(add_tag)
button_del_tag.clicked.connect(del_tag)
button7.clicked.connect(search_tag)
#запуск приложения
notes_win.show()

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)

#Конец
app.exec_()
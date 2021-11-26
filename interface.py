import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from database import *


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'login_window.ui')
        loadUi(path_to_ui, self)
        self.login_btn.clicked.connect(self.login_function)
        self.signup_btn.clicked.connect(self.sign_up)
        self.sign_in_dialog = None
        self.dialog_widget = None

    def login_function(self):
        email = self.email_input.text()
        password = self.password_input.text()
        is_authorised, user_id = user_authorisation(email, password)
        if is_authorised:
            account = Account(user_id)
            widget.addWidget(account)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.sign_in_dialog = SignInDialog()
            self.dialog_widget = QtWidgets.QStackedWidget()
            self.dialog_widget.addWidget(self.sign_in_dialog)
            self.dialog_widget.show()

    @staticmethod
    def sign_up():
        registration_window = RegistrationWindow()
        widget.addWidget(registration_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ImagesLabelWindow(QWidget):
    def __init__(self, dataset_name):
        super(ImagesLabelWindow, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'images_label_window.ui')
        loadUi(path_to_ui, self)
        fill_files_in_dataset(self.list_of_files, dataset_name)
        self.brush_colours.addItems(['red', 'blue', 'brown', 'darkgrey', 'gold', 'pink'])
        self.brush_types.addItems(['Rectangle', 'Ellipse'])
        self.dataset_name = dataset_name
        self.dataset_name_label.setText(self.dataset_name)
        self.list_of_files.setColumnWidth(0, 240)
        self.drawing = False
        self.list_of_files.selectionModel().selectionChanged.connect(
            lambda: fill_image_file_params(self.list_of_files.currentItem().text(), self.picture, self.x1_input,
                                           self.y1_input, self.x2_input, self.y2_input, self.class_input,
                                           self.brush_colours.currentText(), self.brush_types.currentText()))
        self.save_btn.clicked.connect(lambda: save_image_changes(self.list_of_files.currentItem().text(), self.x1_input,
                                                                 self.y1_input, self.x2_input, self.y2_input,
                                                                 self.class_input))
        self.save_btn.clicked.connect(
            lambda: fill_image_file_params(self.list_of_files.currentItem().text(), self.picture, self.x1_input,
                                           self.y1_input, self.x2_input, self.y2_input, self.class_input,
                                           self.brush_colours.currentText(), self.brush_types.currentText()))
        self.addnew_btn.clicked.connect(self.open_file)
        self.import_to_csv_btn.clicked.connect(lambda: import_to_csv(dataset_name))
        self.import_to_excel_btn.clicked.connect(lambda: import_to_excel(dataset_name))
        self.delete_btn.clicked.connect(lambda: delete_image_file(self.list_of_files.currentItem().text(),
                                                                  self.dataset_name))
        self.delete_btn.clicked.connect(lambda: fill_files_in_dataset(self.list_of_files, dataset_name))

    def open_file(self):
        try:
            file_name = QFileDialog.getOpenFileName()
            path = file_name[0]
            file_name = os.path.basename(path)
            save_image_to_dataset(file_name, self.dataset_name)
            fill_files_in_dataset(self.list_of_files, self.dataset_name)
        except:
            pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.x1_input.setText(str(event.pos().x() - 35))
            self.y1_input.setText(str(event.pos().y() - 35))

    def mouseMoveEvent(self, event):
        if event.button() == Qt.NoButton:
            self.x2_input.setText(str(event.pos().x() - 35))
            self.y2_input.setText(str(event.pos().y() - 35))
            save_image_changes(self.list_of_files.currentItem().text(), self.x1_input,
                               self.y1_input, self.x2_input, self.y2_input,
                               self.class_input)
            fill_image_file_params(self.list_of_files.currentItem().text(), self.picture, self.x1_input,
                                   self.y1_input, self.x2_input, self.y2_input, self.class_input,
                                   self.brush_colours.currentText(), self.brush_types.currentText())


class TextLabelWindow(QWidget):
    def __init__(self, dataset_name):
        super(TextLabelWindow, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'texts_label_window.ui')
        loadUi(path_to_ui, self)
        self.dataset_name = dataset_name
        self.dataset_name_label.setText(self.dataset_name)
        files_names = get_text_files_names(self.dataset_name)
        self.texts_list.addItems(files_names)
        fill_text_label_elements(self.list_of_labels, self.text, self.texts_list.currentText())
        self.texts_list.activated[str].connect(lambda: fill_text_label_elements(self.list_of_labels, self.text,
                                                                                self.texts_list.currentText()))
        self.text.selectionChanged.connect(lambda: self.fill_fields())
        self.addnew_btn.clicked.connect(self.open_file)
        self.save_btn.clicked.connect(lambda: save_text_label(self.texts_list.currentText(),
                                                              self.text_fragment_input,
                                                              self.position_input, self.label_input))
        self.save_btn.clicked.connect(lambda: fill_text_label_elements(self.list_of_labels,
                                                                       self.text,
                                                                       self.texts_list.currentText()))
        self.delete_btn.clicked.connect(lambda: delete_text_label(self.list_of_labels.currentItem().text()))
        self.delete_btn.clicked.connect(lambda: fill_text_label_elements(self.list_of_labels,
                                                                         self.text,
                                                                         self.texts_list.currentText()))
        self.import_to_csv_btn.clicked.connect(lambda: import_to_csv_text(self.dataset_name))
        self.delete_cur_text_btn.clicked.connect(self.delete_text_file)

    def delete_text_file(self):
        delete_text_file(self.texts_list.currentText(), self.dataset_name)
        self.texts_list.clear()
        self.texts_list.addItems(get_text_files_names(self.dataset_name))
        fill_text_label_elements(self.list_of_labels, self.text, self.texts_list.currentText())

    def open_file(self):
        try:
            file_name = QFileDialog.getOpenFileName()
            path = file_name[0]
            file_name = os.path.basename(path)
            with open(path) as f:
                file = f.readlines()
            add_text_file(file_name, file[0], self.dataset_name)
            added_file_name = get_text_files_names(self.dataset_name)
            added_file_name = added_file_name[-1]
            self.texts_list.addItem(added_file_name)
        except:
            pass

    def fill_fields(self):
        text = self.text.toPlainText()
        cursor = self.text.textCursor()
        self.text_fragment_input.setText(text[cursor.selectionStart():cursor.selectionEnd()])
        self.position_input.setText(str(cursor.selectionStart()))


class AddProject(QWidget):
    def __init__(self, workspace_name):
        super(AddProject, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'add_project_dialog.ui')
        loadUi(path_to_ui, self)
        self.save_btn.clicked.connect(self.add_project)
        self.workspace_name = workspace_name

    def add_project(self):
        add_dataset(self.dataset_name_input.text(), self.task_type_input.text(), self.description_input.text(),
                    self.workspace_name)
        self.dataset_name_input.setText("")
        self.task_type_input.setText("")
        self.description_input.setText("")


class InviteWindow(QWidget):
    def __init__(self, team_name, table_obj):
        super(InviteWindow, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'invite_dialog.ui')
        loadUi(path_to_ui, self)
        self.invite_btn.clicked.connect(lambda: add_member(self.email_input.text(), team_name))
        self.invite_btn.clicked.connect(lambda: fill_members(table_obj, team_name))


class AddWorkspaceWindow(QWidget):
    def __init__(self, team_name, workspace_names_cb):
        super(AddWorkspaceWindow, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'add_workspace_dialog.ui')
        loadUi(path_to_ui, self)
        self.team_name = team_name
        self.workspace_names_cb = workspace_names_cb
        self.save_btn.clicked.connect(self.add_workspace)

    def add_workspace(self):
        add_workspace(self.workspace_name_input.text(), self.description_input.text(), self.team_name)
        self.workspace_name_input.setText("")
        self.description_input.setText("")
        self.workspace_names_cb.addItem(self.workspace_name_input.text())



class AddTaskWindow(QWidget):
    def __init__(self, team_name):
        super(AddTaskWindow, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'add_task_dialog.ui')
        loadUi(path_to_ui, self)
        self.team_name = team_name
        self.save_btn.clicked.connect(self.add_task)

    def add_task(self):
        add_task(self.task_title_input.text(),self.task_text_input.text(), self.team_name)
        self.task_title_input.setText("")
        self.task_text_input.setText("")


class EditAccountWindow(QWidget):
    def __init__(self, user_id):
        super(EditAccountWindow, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'edit_account.ui')
        loadUi(path_to_ui, self)
        account_data = load_user_account(user_id)
        self.email_edit_line.setText(account_data[0])
        self.password_edit_line.setText(account_data[5])
        self.fname_edit_line.setText(account_data[1])
        self.phnumber_edit_line.setText(account_data[2])
        self.lname_edit_line.setText(account_data[3])
        self.gender_edit_line.setText(account_data[4])
        self.save_changes_btn.clicked.connect(
            lambda: save_account_changes(user_id, self.email_edit_line, self.password_edit_line,
                                         self.fname_edit_line, self.phnumber_edit_line, self.lname_edit_line,
                                         self.gender_edit_line))


class Note:
    def __init__(self, page, coordinates, title, task_text):
        # print(title, " ", task_text)
        self.frame = QtWidgets.QFrame(page)
        self.frame.setGeometry(QtCore.QRect(coordinates[0], coordinates[1], 230, 134))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.title_and_save_btn = QtWidgets.QPushButton(self.frame)
        self.title_and_save_btn.setGeometry(QtCore.QRect(0, 0, 230, 32))
        self.title_and_save_btn.setStyleSheet("QPushButton {\n"
                                              "background-color: rgb(78, 0, 234);\n"
                                              "color:rgb(243,247,254);\n"
                                              "border: 0px solid;\n"
                                              "border-top-left-radius: 15px;\n"
                                              "border-top-right-radius: 15px;\n"
                                              "font: 20pt \"Andale Mono\" ;\n"
                                              "\n"
                                              "}\n"
                                              "QPushButton:hover {\n"
                                              "background-color: rgb(254, 204, 102);\n"
                                              "color:rgb(59, 146, 212);\n"
                                              "}")
        self.title_and_save_btn.setText(title)
        self.title_and_save_btn.setObjectName("title_and_save_btn")
        self.note_text = QtWidgets.QTextEdit(self.frame)
        self.note_text.setGeometry(QtCore.QRect(0, 32, 230, 70))
        self.note_text.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.note_text.setPlainText(task_text)
        self.note_text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.note_text.setObjectName("note_text")
        self.finish_task_btn = QtWidgets.QPushButton(self.frame)
        self.finish_task_btn.setGeometry(QtCore.QRect(0, 102, 230, 32))
        self.finish_task_btn.setStyleSheet("QPushButton {\n"
                                           "background-color: rgb(78, 0, 234);\n"
                                           "color:rgb(243,247,254);\n"
                                           "border: 0px solid;\n"
                                           "border-bottom-left-radius: 15px;\n"
                                           "border-bottom-right-radius: 15px;\n"
                                           "font: 20pt \"Andale Mono\" ;\n"
                                           "\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "background-color: rgb(254, 204, 102);\n"
                                           "color:rgb(59, 146, 212);\n"
                                           "}")
        self.finish_task_btn.setText("Finish task")
        self.finish_task_btn.setObjectName("delete_btn")
        self.title_and_save_btn.clicked.connect(lambda: save_task_changes(self.title_and_save_btn.text(),
                                                                          self.note_text.toPlainText()))
        self.finish_task_btn.clicked.connect(lambda: finish_task(self.title_and_save_btn.text()))


class PlainWidget:
    def __init__(self, page, workflow_data, coordinates, stackedWidget, projects_page):
        print(workflow_data)
        self.plain_widget = QtWidgets.QWidget(page)
        self.plain_widget.setGeometry(QtCore.QRect(coordinates[0], coordinates[1], 230, 160))
        self.plain_widget.setObjectName("plain_widget")
        self.plain_widget.setStyleSheet("")
        self.button = QtWidgets.QPushButton(self.plain_widget)
        self.button.setGeometry(QtCore.QRect(0, 0, 230, 60))
        self.button.setStyleSheet("QPushButton {\n"
                                  "    background-color: rgb(78, 0, 234);\n"
                                  "    color:rgb(243,247,254);\n"
                                  "    border: 0px solid;\n"
                                  "    font: 20pt \"Andale Mono\";\n"
                                  "    border-top-left-radius: 15px;\n"
                                  "    border-top-right-radius: 15px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:hover {\n"
                                  "    background-color: rgb(254, 204, 102);\n"
                                  "    color:rgb(59, 146, 212);\n"
                                  "}")
        self.button.setText(workflow_data[0])
        self.button.setObjectName("button")
        self.button.clicked.connect(lambda: stackedWidget.setCurrentWidget(projects_page))
        self.button.clicked.connect(lambda: Account.is_clicked(workspace_name=workflow_data[0]))
        self.background_label = QtWidgets.QLabel(self.plain_widget)
        self.background_label.setGeometry(QtCore.QRect(0, 60, 230, 100))
        self.background_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "    font: 20pt \"Andale Mono\";\n"
                                            "border-bottom-right-radius: 15px;\n"
                                            "border-bottom-left-radius:  15px;")
        if workflow_data[1] is not None:
            self.background_label.setText(workflow_data[1])
        self.background_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.background_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.background_label.setObjectName("background_frame")


class Account(QMainWindow):
    def __init__(self, user_id):
        super(Account, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'main_window.ui')
        loadUi(path_to_ui, self)
        self.user_id = user_id
        self.label_window = None
        self.window_widget = None
        self.edit_window = None
        self.invite_window = None
        self.add_window = None
        self.workspace_window = None
        self.task_window = None
        user_data = load_user_account(user_id)
        self.user_photo1.setText(str(user_data[1][0] + user_data[3][0]))
        self.user_photo2.setText(str(user_data[1][0] + user_data[3][0]))
        self.user_photo3.setText(str(user_data[1][0] + user_data[3][0]))
        self.user_photo4.setText(str(user_data[1][0] + user_data[3][0]))
        self.user_photo5.setText(str(user_data[1][0] + user_data[3][0]))

        # Initial window settings
        team_names = get_team_names(user_id)
        self.team_name = team_names[0]
        self.tasks_data = get_tasks(self.team_name)
        self.team_names_cb.addItems(team_names)
        self.team_picture.setText(self.team_name[0])
        self.workspace_names, self.workspace_data = get_team_workflows(team_names[0])
        self.workspace_name = self.workspace_data[0][0]
        self.workspace_names_cb.addItems(self.workspace_names)
        self.workspace_picture.setText(self.workspace_name[0])
        fill_members(self.members_table, self.team_name)
        fill_projects(self.datasets_table, self.workspace_name)
        fill_image_files(self.image_files_table, self.workspace_name)
        fill_text_files(self.text_files_table, self.workspace_name)
        self.fill_tasks(self.tasks_data)
        self.image_files_table.setColumnWidth(0, 300)
        self.image_files_table.setColumnWidth(1, 280)
        self.text_files_table.setColumnWidth(0, 150)
        self.text_files_table.setColumnWidth(1, 350)
        self.text_files_table.setColumnWidth(2, 350)
        self.datasets_table.setColumnWidth(0, 250)
        self.datasets_table.setColumnWidth(1, 250)
        self.datasets_table.setColumnWidth(2, 259)
        self.members_table.setColumnWidth(0, 190)
        self.members_table.setColumnWidth(1, 190)
        self.members_table.setColumnWidth(2, 379)
        self.datasets_table.selectionModel().selectionChanged.connect(
            lambda: self.open_editor(self.datasets_table.currentItem().text()))
        # Changing workflow and team if changed
        self.team_names_cb.activated[str].connect(self.change_session_settings)
        self.workspace_names_cb.activated[str].connect(self.change_session_settings)

        # Changing workspace window
        self.fill_workspaces()

        # Pages buttons
        self.workspaces_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.workspaces_page))
        self.members_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.members_page))
        self.files_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.files_page))
        self.projects_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.projects_page))
        self.tasks_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.tasks_page))
        self.signout_btn1.clicked.connect(self.sign_out)
        self.signout_btn1.setShortcut("Ctrl+X")
        self.signout_btn2.clicked.connect(self.sign_out)
        self.signout_btn3.clicked.connect(self.sign_out)
        self.signout_btn4.clicked.connect(self.sign_out)
        self.signout_btn5.clicked.connect(self.sign_out)
        self.edit_btn1.clicked.connect(self.edit_account)
        self.edit_btn2.clicked.connect(self.edit_account)
        self.edit_btn3.clicked.connect(self.edit_account)
        self.edit_btn4.clicked.connect(self.edit_account)
        self.edit_btn5.clicked.connect(self.edit_account)
        self.invite_btn.clicked.connect(self.invite_user)
        self.workspace_add_btn.clicked.connect(self.add_workspace)
        self.add_task_btn.clicked.connect(self.add_task)
        self.search_btn.clicked.connect(lambda: fill_image_files(self.image_files_table, self.workspace_name,
                                                                 self.search_line.text()))
        self.search_btn.clicked.connect(lambda: fill_text_files(self.text_files_table, self.workspace_name,
                                                                self.search_line.text()))
        self.add_proj_btn.clicked.connect(self.add_project)
        self.search_btn3.clicked.connect(lambda: search_in_projects(self.datasets_table,
                                                                    self.proj_search_line.text(),
                                                                    self.workspace_name))
        self.proj_refresh_btn.clicked.connect(lambda: fill_projects(self.datasets_table, self.workspace_name))
        self.proj_delete_btn.clicked.connect(lambda: delete_project(self.datasets_table.currentItem().text(),
                                                                    self.workspace_name))
        self.proj_delete_btn.clicked.connect(lambda: fill_projects(self.datasets_table, self.workspace_name))
        # TODO self.datasets_table.itemChanged.connect(self.cell_changed)
        self.search_btn2.clicked.connect(lambda: search_in_members(self.members_table,
                                                                   self.members_search_line.text(),
                                                                   self.team_name))
        self.members_refresh_btn.clicked.connect(lambda: fill_members(self.members_table, self.team_name))
        self.members_delete_btn.clicked.connect(lambda: delete_member(self.members_table.currentItem().text(),
                                                                      self.team_name))
        self.members_delete_btn.clicked.connect(lambda: fill_members(self.members_table, self.team_name))
        self.files_refresh_btn.clicked.connect(lambda: fill_image_files(self.image_files_table, self.workspace_name))
        self.files_refresh_btn.clicked.connect(lambda: fill_text_files(self.text_files_table, self.workspace_name))

    def cell_changed(self, item):
        edit_project(item.row(), item.column(), self.datasets_table, self.workspace_name)

    def fill_workspaces(self, searched_workspaces=None):
        print('filled')
        if searched_workspaces is None:
            searched_workspaces = self.workspace_data
        bottom_margin = 100
        count = 0
        for i in range((len(searched_workspaces) // 3 + 1)):
            left_margin = 25
            for j in range(3):
                try:
                    plain_widget = PlainWidget(self.workspaces_page, searched_workspaces[count],
                                               [left_margin, bottom_margin],
                                               self.stackedWidget, self.projects_page)
                except IndexError:
                    break
                left_margin += 255
                count += 1
                if count >= len(searched_workspaces):
                    break
            bottom_margin += 185

    def fill_tasks(self, searched_tasks=None):
        if searched_tasks is None:
            searched_tasks = self.tasks_data
        bottom_margin = 100
        count = 0
        print(searched_tasks)
        for i in range((len(searched_tasks) // 3 + 1)):
            left_margin = 25
            for j in range(3):
                try:
                    note_widget = Note(self.tasks_page, [left_margin, bottom_margin],
                                       searched_tasks[count][0], searched_tasks[count][1])
                except IndexError:
                    break
                left_margin += 255
                count += 1
                if count >= len(searched_tasks):
                    break
            bottom_margin += 185

    '''def fill_tasks(self,):
        button = QPushButton("kindled")
        button2 = QPushButton("kindled")
        for i in range (10):
            frame = QtWidgets.QFrame()
            frame.setGeometry(QtCore.QRect(0, 0, 240, 130))
            frame.setMinimumSize(QtCore.QSize(240, 130))
            frame.setMaximumSize(QtCore.QSize(240, 130))
            frame.setStyleSheet("background-color: rgb(255, 255, 255);")
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)
            frame.setObjectName("frame")
            # self.grid.addWidget(button, 0, 0)
            # self.grid.addWidget(button2, 1, 1)
            self.grid.addWidget(frame, i, 1)
        # self.grid.addWidget(fr, 3, 1)'''

    def edit_account(self):
        self.edit_window = EditAccountWindow(self.user_id)
        self.window_widget = QtWidgets.QStackedWidget()
        self.window_widget.addWidget(self.edit_window)
        self.window_widget.show()

    def add_project(self):
        self.add_window = AddProject(self.workspace_name)
        self.window_widget = QtWidgets.QStackedWidget()
        self.window_widget.addWidget(self.add_window)
        self.window_widget.show()
        fill_projects(self.datasets_table, self.workspace_name)

    def open_editor(self, dataset_name):
        task_type = which_task_type(dataset_name)
        if task_type == 'image classification':
            self.label_window = ImagesLabelWindow(dataset_name)
            self.window_widget = QtWidgets.QStackedWidget()
            self.window_widget.addWidget(self.label_window)
            self.window_widget.show()
        elif task_type == 'text classification':
            self.label_window = TextLabelWindow(dataset_name)
            self.window_widget = QtWidgets.QStackedWidget()
            self.window_widget.addWidget(self.label_window)
            self.window_widget.show()
        else:
            pass

    def invite_user(self):
        self.invite_window = InviteWindow(self.team_name, self.members_table)
        self.window_widget = QtWidgets.QStackedWidget()
        self.window_widget.addWidget(self.invite_window)
        self.window_widget.show()

    def change_session_settings(self):
        self.team_name = self.team_names_cb.currentText()
        self.workspace_name = self.workspace_names_cb.currentText()
        self.team_picture.setText(self.team_name[0])
        self.workspace_picture.setText(self.workspace_name[0])
        fill_members(self.members_table, self.team_name)
        fill_projects(self.datasets_table, self.workspace_name)
        self.fill_workspaces()
        self.tasks_data = get_tasks(self.team_name)
        self.fill_tasks(self.tasks_data)

    def add_workspace(self):
        self.workspace_window = AddWorkspaceWindow(self.team_name, self.workspace_names_cb)
        self.window_widget = QtWidgets.QStackedWidget()
        self.window_widget.addWidget(self.workspace_window)
        self.window_widget.show()
        self.workspace_data = get_team_workflows(self.team_name)

    def add_task(self):
        self.task_window = AddTaskWindow(self.team_name)
        self.window_widget = QtWidgets.QStackedWidget()
        self.window_widget.addWidget(self.task_window)
        self.window_widget.show()
        self.workspace_data = get_team_workflows(self.team_name)

    @staticmethod
    def is_clicked(workspace_name):
        # self.change_current_workspace_name(workspace_name)
        print("Clicked: ", workspace_name)

    def change_current_workspace_name(self, workspace_name):
        self.self.workspace_name = workspace_name
        combo_box_index = self.workspace_names_cb.findText(workspace_name)
        self.workspace_names_cb.setCurrentIndex(combo_box_index)

    @staticmethod
    def sign_out():
        back_to_login = Login()
        widget.addWidget(back_to_login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class RegistrationWindow(QWidget):
    def __init__(self):
        super(RegistrationWindow, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'signup_window.ui')
        loadUi(path_to_ui, self)
        self.ahacc_btn.clicked.connect(self.close_window)
        self.create_acc_btn.clicked.connect(lambda:
                                            register(self.email_input_line.text(), self.password_input_line.text(),
                                                     self.fname_input_line.text(), self.phnumber_input_line.text(),
                                                     self.lname_input_line.text(), self.gender_input_line.text()))
        self.create_acc_btn.clicked.connect(self.close_window)

    @staticmethod
    def close_window():
        back_to_login = Login()
        widget.addWidget(back_to_login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class SignInDialog(QDialog):
    def __init__(self):
        super(SignInDialog, self).__init__()
        path_to_ui = Path(Path.cwd(), 'uis', 'dialog_window.ui')
        loadUi(path_to_ui, self)


app = QApplication(sys.argv)
MainWindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(MainWindow)
widget.show()
app.exec_()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

import psycopg2
from psycopg2 import Error


class CtextGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))

        return sm


class GameScreen(Screen):

    label_input_text = ObjectProperty()
    label_text = ObjectProperty()
    eventIndex = 1

    def change_text(self):
        self.textForMainLabel = CTableView().start_game(self.eventIndex)
        self.label_text.text = self.textForMainLabel[0]
        self.action_button1_interaction(self.textForMainLabel)

        print(self.textForMainLabel)

    def action_button1_interaction(self, resultIndex):
        self.textForButton = CTableView().result_parser(resultIndex[1])
        self.action_button1.text = self.textForButton[1]
        self.action_button2.text = self.textForButton[2]
        self.eventIndex = self.textForButton[2]

    def action_for_button1(self):
        pass




class SettingsScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class CTableView:
    def __init__(self):
        self.con = psycopg2.connect(
            database="game",
            user="postgres",
            password="1",
            host="127.0.0.1",
            port="5432"
        )
        self.cur = self.con.cursor()

    def start_game(self, index):
        try:
            self.cur.execute(f'''SELECT e_description, e_result_id1, e_result_id2 FROM events
                                WHERE e_id = '{index}'
                                ''')
            self.eventDescription = self.rowUnpacker(self.cur.fetchall())
            return self.eventDescription

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def result_parser(self, resultIndex):
        try:
            self.cur.execute(f'''SELECT r_description, r_name, r_event_id FROM results
                                WHERE r_id = '{resultIndex}' ''')
            self.row = self.rowUnpacker(self.cur.fetchall())

            return self.row
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def rowUnpacker(self, row):
        for unpackRow in row:
            pass
        return unpackRow

    def table_name_view(self):
        try:
            self.cur.execute('''SELECT table_name FROM information_schema.tables
                                WHERE table_schema NOT IN ('information_schema','pg_catalog');''')
            self.rows = self.cur.fetchall()

            self.namesOfTables = []

            for row in self.rows:
                for name in row:
                    self.namesOfTables.append(name)
            return self.namesOfTables
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def table_column_name(self):
        try:
            self.nameContainer = self.table_name_view()

            self.cur.execute(f'''SELECT column_name
                                FROM information_schema.columns
                                WHERE table_name = '{self.nameContainer[1]}'
                            ''')
            self.rows = self.cur.fetchall()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def connection_close(self):
        if self.con:
            self.cur.close()
            self.con.close()


if __name__ == '__main__':
    CtextGameApp().run()

"""
main.py

Kivy GUI wrapper for the Taixiu app. Loads the UI from tai_xiu.kv and uses backend.RootModel.
"""

import os
from backend import RootModel

try:
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    from kivy.properties import StringProperty, ListProperty
    from kivy.clock import mainthread
    from kivy.metrics import dp
except Exception as e:
    print("Kivy is not installed. To run the GUI locally, please install Kivy.")
    print("See https://kivy.org/docs/installation/ for instructions.")
    raise

KV_FILE = "tai_xiu.kv"
if os.path.exists(KV_FILE):
    Builder.load_file(KV_FILE)
else:
    KV_STR = """
BoxLayout:
    Label:
        text: 'Missing tai_xiu.kv'
"""
    Builder.load_string(KV_STR)

class RootWidget(BoxLayout):
    history = ListProperty([])
    history_text = StringProperty('')
    stats_text = StringProperty('')
    predict_text = StringProperty('Chưa có dữ liệu')
    info_text = StringProperty('Dữ liệu được lưu trên thiết bị.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_dir = App.get_running_app().user_data_dir
        self.model = RootModel(data_dir=model_dir)
        self.update_views()

    @mainthread
    def update_views(self):
        self.history = self.model.history
        self.history_text = ' '.join(self.history[:50]) if self.history else '(chưa có)'
        st = self.model.stats()
        if st['total'] > 0:
            self.stats_text = (
                f"Tổng: {st['total']}\n"
                f"Tài: {st['cnt_tai']} ({st['pct_tai']:.1f}%)\n"
                f"Xỉu: {st['cnt_xiu']} ({st['pct_xiu']:.1f}%)\n"
                f"Chuỗi Tài dài nhất: {st['longest_tai']}\n"
                f"Chuỗi Xỉu dài nhất: {st['longest_xiu']}"
            )
        else:
            self.stats_text = '(chưa có dữ liệu)'
        self.predict_text = self.model.predict_markov_string()

    def on_button(self, res: str) -> None:
        try:
            self.model.add_result(res)
            self.info_text = 'Đã thêm: ' + res
        except Exception as e:
            self.info_text = 'Lỗi: ' + str(e)
        self.update_views()

    def on_clear(self) -> None:
        self.model.clear_history()
        self.update_views()
        self.info_text = 'Đã xóa lịch sử.'

    def on_export(self) -> None:
        try:
            out = self.model.export_json()
            self.info_text = f'Xuất thành công: {out}'
        except Exception as e:
            self.info_text = f'Lỗi xuất: {e}'

class TaixiuApp(App):
    def build(self):
        self.title = "Phân tích Tài Xỉu"
        return RootWidget()

if __name__ == '__main__':
    TaixiuApp().run()

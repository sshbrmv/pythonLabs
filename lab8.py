Требуется написать ООП с графическим интерфейсом в соответствии со своим вариантом. 
Должны быть реализованы минимум один класс, три атрибута, четыре метода (функции). 
Ввод данных из файла с контролем правильности ввода. 
Базы данных не использовать. При необходимости сохранять информацию в файлах, разделяя значения запятыми (CSV файлы) или пробелами. Для GUI использовать библиотеку tkinter (mathplotlib не использовать).
Объекты – договоры на аренду недвижимости
Функции:	сегментация по видам объектов недвижимости полного списка договоров 
визуализация предыдущей функции в форме круговой диаграммы
сегментация по менеджерам полного списка договоров 
визуализация предыдущей функции в форме круговой диаграммы

import tkinter as tk
from tkinter import messagebox, filedialog, Text, Scrollbar
from collections import Counter
from math import pi, cos, sin
import csv

class LeaseContract:
    def __init__(self, contract_id, property_type, manager):
        self.contract_id = contract_id  #ID
        self.property_type = property_type  #Вид объекта
        self.manager = manager  #Менеджер

class LeaseManager:
    def __init__(self):
        self.contracts = []  # Список для хранения объектов по договору аренды

    #1 Загрузка данных из CSV-файла с проверкой введенных данных
    def load_from_file(self, filename):
        self.contracts.clear()
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 3:
                        raise ValueError("Недопустимый формат строки: ожидаемые 3 поля.")
                    try:
                        contract_id = int(row[0].strip())  # Проверка ID как целого числа
                        property_type = row[1].strip()  # Строка
                        manager = row[2].strip()  # Строка
                        if not property_type or not manager:
                            raise ValueError("Тип объекта или менеджер не могут быть пустыми.")
                        contract = LeaseContract(contract_id, property_type, manager)
                        self.contracts.append(contract)
                    except ValueError as e:
                        messagebox.showwarning("Ошибка проверки данных", f"Пропуск недопустимой строки: {row} - {str(e)}")
            if not self.contracts:
                messagebox.showinfo("Информация", "Не загружены действующие договоры.")
            else:
                messagebox.showinfo("Успешно", f"Загружено {len(self.contracts)} договор(а/ов).")
        except Exception as e:
            messagebox.showerror("Ошибка в файле", f"Ошибка загрузки файла: {str(e)}")

    #2 Сегментирование договоров по типу свойства (returns a Counter)
    def segment_by_property_type(self):
        if not self.contracts:
            raise ValueError("Договоры не загружены.")
        types = [contract.property_type for contract in self.contracts]
        return Counter(types)

    #3 Сегментация договоров в разбивке по менеджерам (returns a Counter)
    def segment_by_manager(self):
        if not self.contracts:
            raise ValueError("Договоры не загружены.")
        managers = [contract.manager for contract in self.contracts]
        return Counter(managers)

    #4 Визуализация сегментации в виде круговой диаграммы с помощью Tkinter Canvas
    def visualize_pie_chart(self, data, title):
        if not data:
            messagebox.showwarning("Нет данных", "Нет данных для визуализации.")
            return

        root = tk.Toplevel()
        root.title(title)
        canvas = tk.Canvas(root, width=400, height=400, bg="white")
        canvas.pack()

        total = sum(data.values())
        start_angle = 0
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "gray", "cyan"]
        color_index = 0

        # Legend frame
        legend_frame = tk.Frame(root)
        legend_frame.pack(side=tk.BOTTOM, pady=10)

        for key, value in data.items():
            extent = (value / total) * 360
            #Отрисовка сектора круговой диаграммы
            canvas.create_arc(50, 50, 350, 350, start=start_angle, extent=extent, fill=colors[color_index % len(colors)])
            # Вычисление позиции текстовой метки
            mid_angle = start_angle + extent / 2
            mid_angle_rad = mid_angle * (pi / 180)
            label_x = 200 + 100 * cos(mid_angle_rad)
            label_y = 200 - 100 * sin(mid_angle_rad)  # Y is inverted in canvas
            canvas.create_text(label_x, label_y, text=f"{key} ({value})", fill="black")
            start_angle += extent
            # Legend
            tk.Label(legend_frame, text=key, bg=colors[color_index % len(colors)], fg="white").pack(side=tk.LEFT, padx=5)
            color_index += 1

# GUI
class App:
    def __init__(self, root):
        self.manager = LeaseManager()
        self.root = root
        self.root.title("Менеджеры по договорам аренды")

        # Buttons
        load_button = tk.Button(root, text="Загрузить данные из файла", command=self.load_data)
        load_button.pack(pady=10)

        segment_type_button = tk.Button(root, text="Сегментация по видам", command=self.show_segment_by_type)
        segment_type_button.pack(pady=5)

        viz_type_button = tk.Button(root, text="Визуализация по видам", command=self.viz_by_type)
        viz_type_button.pack(pady=5)

        segment_manager_button = tk.Button(root, text="Сегментация по менеджерам", command=self.show_segment_by_manager)
        segment_manager_button.pack(pady=5)

        viz_manager_button = tk.Button(root, text="Визуализация по менеджерам", command=self.viz_by_manager)
        viz_manager_button.pack(pady=5)

        # Текстовая область для отображения сегментации
        self.text_area = Text(root, height=10, width=50)
        self.text_area.pack(pady=10)
        scrollbar = Scrollbar(root, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

    def load_data(self):
        filename = filedialog.askopenfilename(title="Выбрать csv файл", filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.manager.load_from_file(filename)

    def show_segment_by_type(self):
        try:
            segments = self.manager.segment_by_property_type()
            self.display_segments(segments, "Сегментация по видам")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def viz_by_type(self):
        try:
            segments = self.manager.segment_by_property_type()
            self.manager.visualize_pie_chart(segments, "Круговая диаграмма по типу объекта")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def show_segment_by_manager(self):
        try:
            segments = self.manager.segment_by_manager()
            self.display_segments(segments, "Сегментация по менеджерам")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def viz_by_manager(self):
        try:
            segments = self.manager.segment_by_manager()
            self.manager.visualize_pie_chart(segments, "Круговая диаграмма по менеджерам")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def display_segments(self, segments, title):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"{title}:\n\n")
        for key, value in segments.items():
            self.text_area.insert(tk.END, f"{key}: {value}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

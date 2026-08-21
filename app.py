"""
مروق ايكو الخارق - التطبيق الرئيسي
Mrook Echo - Main Application
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import json
import os

from components import StyledFrame, ValidationEntry, StatusBar


class MrookEcho:
    """فئة التطبيق الرئيسية - تطبيق إدارة الوقت والطاقة"""

    def __init__(self, root):
        self.root = root
        self.root.title("مروق ايكو الخارق | Mrook Echo")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)

        # تحميل الإعدادات
        self.settings = self.load_settings()

        # المتغيرات
        self.time_var = tk.StringVar(value="0")
        self.energy_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="في حالة انتظار...")

        # تطبيق التنسيق
        self.setup_styles()

        # بناء الواجهة
        self.build_ui()

        # تحديث أولي
        self.update_status("جاهز للاستخدام")

    def setup_styles(self):
        """إعداد تنسيقات ttk"""
        style = ttk.Style()
        style.theme_use('clam')

        # تنسيق الإطارات
        style.configure("TFrame", background="#f0f4f8")
        style.configure("Card.TFrame", background="#ffffff", relief="raised")

        # تنسيق العناوين
        style.configure("Title.TLabel", 
                       font=("Segoe UI", 18, "bold"),
                       foreground="#1a365d",
                       background="#f0f4f8",
                       padding=10)

        style.configure("Header.TLabel",
                       font=("Segoe UI", 12, "bold"),
                       foreground="#2c5282",
                       background="#f0f4f8")

        style.configure("TLabel", 
                       font=("Segoe UI", 10),
                       foreground="#2d3748",
                       background="#f0f4f8")

        # تنسيق الحقول
        style.configure("TEntry", 
                       font=("Segoe UI", 11),
                       padding=5)

        # تنسيق الأزرار
        style.configure("Primary.TButton",
                       font=("Segoe UI", 10, "bold"),
                       foreground="#ffffff",
                       background="#3182ce",
                       padding=8)
        style.map("Primary.TButton",
                 background=[("active", "#2b6cb0"), ("pressed", "#2c5282")])

        style.configure("Success.TButton",
                       font=("Segoe UI", 10, "bold"),
                       foreground="#ffffff",
                       background="#38a169",
                       padding=8)
        style.map("Success.TButton",
                 background=[("active", "#2f855a"), ("pressed", "#276749")])

        # شريط الحالة
        style.configure("Status.TLabel",
                       font=("Segoe UI", 9),
                       foreground="#718096",
                       background="#edf2f7",
                       padding=5)

    def build_ui(self):
        """بناء واجهة المستخدم"""
        # الإطار الرئيسي
        main_frame = StyledFrame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # العنوان
        title_label = ttk.Label(main_frame, text="⚡ مروق ايكو الخارق", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        # بطاقة الوقت
        time_card = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        time_card.pack(fill=tk.X, pady=5)

        ttk.Label(time_card, text="⏱️ الوقت (دقائق):", style="Header.TLabel").pack(anchor=tk.W)

        time_input_frame = ttk.Frame(time_card)
        time_input_frame.pack(fill=tk.X, pady=(5, 0))

        self.entry_time = ValidationEntry(time_input_frame, textvariable=self.time_var, 
                                          validate_type="int", width=20)
        self.entry_time.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(time_input_frame, text="تحديث الوقت", 
                  command=self.update_time, style="Primary.TButton").pack(side=tk.LEFT)

        # بطاقة الطاقة
        energy_card = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        energy_card.pack(fill=tk.X, pady=5)

        ttk.Label(energy_card, text="🔋 الطاقة (%):", style="Header.TLabel").pack(anchor=tk.W)

        energy_input_frame = ttk.Frame(energy_card)
        energy_input_frame.pack(fill=tk.X, pady=(5, 0))

        self.entry_energy = ValidationEntry(energy_input_frame, textvariable=self.energy_var,
                                            validate_type="int", width=20)
        self.entry_energy.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(energy_input_frame, text="تحديث الطاقة", 
                  command=self.update_energy, style="Primary.TButton").pack(side=tk.LEFT)

        # بطاقة الإجراءات
        actions_card = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        actions_card.pack(fill=tk.X, pady=5)

        ttk.Label(actions_card, text="🚀 الإجراءات السريعة:", style="Header.TLabel").pack(anchor=tk.W)

        buttons_frame = ttk.Frame(actions_card)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(buttons_frame, text="حفظ الإعدادات", 
                  command=self.save_settings, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="إعادة تعيين", 
                  command=self.reset_values).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="عرض البيانات", 
                  command=self.show_data).pack(side=tk.LEFT, padx=5)

        # شريط الحالة
        self.status_bar = StatusBar(main_frame, textvariable=self.status_var)
        self.status_bar.pack(fill=tk.X, pady=(20, 0), side=tk.BOTTOM)

    def validate_input(self, value, field_name):
        """
        التحقق من صحة إدخال المستخدم

        Args:
            value: القيمة المدخلة
            field_name: اسم الحقل (لرسائل الخطأ)

        Returns:
            int: القيمة الصحيحة أو None في حالة الخطأ
        """
        # التحقق من القيمة الفارغة
        if value is None or str(value).strip() == "":
            messagebox.showwarning("تنبيه", f"حقل '{field_name}' فارغ! يرجى إدخال قيمة.")
            return None

        try:
            num_val = int(value)
        except ValueError:
            messagebox.showerror("خطأ", f"قيمة '{field_name}' يجب أن تكون رقماً صحيحاً!")
            return None

        # التحقق من القيم السالبة
        if num_val < 0:
            messagebox.showerror("خطأ", f"قيمة '{field_name}' لا يمكن أن تكون سالبة!")
            return None

        return num_val

    def update_time(self):
        """تحديث قيمة الوقت مع التحقق من الصحة"""
        try:
            time_val = self.validate_input(self.time_var.get(), "الوقت")
            if time_val is None:
                return

            # تحديث الواجهة
            self.entry_time.delete(0, tk.END)
            self.entry_time.insert(0, str(time_val))

            self.update_status(f"✅ تم تحديث الوقت: {time_val} دقيقة")

        except Exception as e:
            messagebox.showerror("خطأ غير متوقع", f"حدث خطأ: {str(e)}")
            self.update_status("❌ خطأ في تحديث الوقت")

    def update_energy(self):
        """تحديث قيمة الطاقة مع التحقق من الصحة"""
        try:
            energy_val = self.validate_input(self.energy_var.get(), "الطاقة")
            if energy_val is None:
                return

            # التحقق من أن الطاقة لا تتجاوز 100%
            if energy_val > 100:
                messagebox.showwarning("تنبيه", "الطاقة لا يمكن أن تتجاوز 100%!")
                energy_val = 100
                self.energy_var.set("100")

            # تحديث الواجهة
            self.entry_energy.delete(0, tk.END)
            self.entry_energy.insert(0, str(energy_val))

            self.update_status(f"✅ تم تحديث الطاقة: {energy_val}%")

        except Exception as e:
            messagebox.showerror("خطأ غير متوقع", f"حدث خطأ: {str(e)}")
            self.update_status("❌ خطأ في تحديث الطاقة")

    def save_settings(self):
        """حفظ الإعدادات في ملف JSON"""
        try:
            settings = {
                "time": self.time_var.get(),
                "energy": self.energy_var.get(),
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            self.update_status("💾 تم حفظ الإعدادات بنجاح!")
            messagebox.showinfo("نجاح", "تم حفظ الإعدادات في ملف settings.json")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل حفظ الإعدادات: {str(e)}")

    def load_settings(self):
        """تحميل الإعدادات من ملف JSON"""
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def reset_values(self):
        """إعادة تعيين القيم إلى الافتراضية"""
        self.time_var.set("0")
        self.energy_var.set("0")
        self.entry_time.delete(0, tk.END)
        self.entry_time.insert(0, "0")
        self.entry_energy.delete(0, tk.END)
        self.entry_energy.insert(0, "0")
        self.update_status("🔄 تم إعادة التعيين")

    def show_data(self):
        """عرض البيانات من ملف data.json"""
        try:
            if os.path.exists("data.json"):
                with open("data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                # عرض البيانات في نافذة منبثقة
                data_window = tk.Toplevel(self.root)
                data_window.title("📊 بيانات الميزات والملاحظات")
                data_window.geometry("500x400")

                text_widget = tk.Text(data_window, wrap=tk.WORD, padx=10, pady=10,
                                     font=("Segoe UI", 10))
                text_widget.pack(fill=tk.BOTH, expand=True)

                text_widget.insert(tk.END, json.dumps(data, ensure_ascii=False, indent=2))
                text_widget.config(state=tk.DISABLED)

                self.update_status("📊 تم عرض البيانات")
            else:
                messagebox.showinfo("معلومات", "ملف data.json غير موجود!")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل قراءة البيانات: {str(e)}")

    def update_status(self, message):
        """تحديث شريط الحالة"""
        self.status_var.set(message)
        self.root.update_idletasks()


def main():
    """نقطة الدخول الرئيسية"""
    root = tk.Tk()
    app = MrookEcho(root)
    root.mainloop()


if __name__ == "__main__":
    main()

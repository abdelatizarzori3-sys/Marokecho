"""
مكونات واجهة المستخدم المخصصة
Custom UI Components for Mrook Echo
"""

import re
import tkinter as tk
from tkinter import ttk


class StyledFrame(ttk.Frame):
    """إطار مُنسق بشكل احترافي"""

    def __init__(self, parent, padding=10, **kwargs):
        super().__init__(parent, padding=padding, **kwargs)
        # يمكن إضافة تأثيرات إضافية هنا


class ValidationEntry(ttk.Entry):
    """
    حقل إدخال مع التحقق من الصحة
    يدعم: أعداد صحيحة، عشرية، نصوص
    """

    def __init__(self, parent, validate_type="any", **kwargs):
        """
        Args:
            validate_type: نوع التحقق ("int", "float", "text", "any")
        """
        self.validate_type = validate_type
        self.var = kwargs.get("textvariable", tk.StringVar())

        # إذا لم يتم تمرير textvariable، نستخدم المتغير الذي أنشأناه
        if "textvariable" not in kwargs:
            kwargs["textvariable"] = self.var

        super().__init__(parent, **kwargs)

        # تسجيل دالة التحقق
        vcmd = (parent.register(self.validate), "%P")
        self.config(validate="key", validatecommand=vcmd)

    def validate(self, value):
        """
        التحقق من القيمة المدخلة

        Args:
            value: القيمة الجديدة

        Returns:
            bool: True إذا كانت القيمة صالحة
        """
        if value == "":
            return True

        if self.validate_type == "int":
            return value.isdigit() or (value.startswith("-") and value[1:].isdigit())

        elif self.validate_type == "float":
            try:
                float(value)
                return True
            except ValueError:
                return False

        elif self.validate_type == "text":
            return bool(re.match(r"^[\w\s؀-ۿ]+$", value))

        return True

    def get_value(self):
        """الحصول على القيمة"""
        return self.var.get()

    def set_value(self, value):
        """تعيين القيمة"""
        self.var.set(value)


class StatusBar(ttk.Frame):
    """شريط حالة احترافي"""

    def __init__(self, parent, textvariable=None, **kwargs):
        super().__init__(parent, **kwargs)

        # خط فاصل
        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=(0, 5))

        # تسمية الحالة
        self.label = ttk.Label(
            self, textvariable=textvariable, style="Status.TLabel", anchor=tk.W
        )
        self.label.pack(fill=tk.X)

        # مؤشر النشاط
        self.activity_var = tk.StringVar(value="●")
        self.activity_label = ttk.Label(
            self,
            textvariable=self.activity_var,
            foreground="#48bb78",
            font=("Segoe UI", 8),
        )
        self.activity_label.pack(side=tk.RIGHT, padx=5)

    def set_busy(self):
        """تعيين حالة مشغول"""
        self.activity_var.set("◐")
        self.activity_label.config(foreground="#ed8936")

    def set_ready(self):
        """تعيين حالة جاهز"""
        self.activity_var.set("●")
        self.activity_label.config(foreground="#48bb78")

    def set_error(self):
        """تعيين حالة خطأ"""
        self.activity_var.set("●")
        self.activity_label.config(foreground="#f56565")


class ProgressCard(ttk.Frame):
    """بطاقة تقدم دائرية/خطية"""

    def __init__(self, parent, title="", maximum=100, **kwargs):
        super().__init__(parent, padding=15, **kwargs)

        self.maximum = maximum

        # العنوان
        ttk.Label(self, text=title, style="Header.TLabel").pack(anchor=tk.W)

        # شريط التقدم
        self.progress = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=300, mode="determinate", maximum=maximum
        )
        self.progress.pack(fill=tk.X, pady=(10, 5))

        # النسبة المئوية
        self.percent_var = tk.StringVar(value="0%")
        ttk.Label(
            self, textvariable=self.percent_var, font=("Segoe UI", 10, "bold")
        ).pack(anchor=tk.E)

    def set_value(self, value):
        """تعيين قيمة التقدم"""
        self.progress["value"] = value
        percent = min(100, int((value / self.maximum) * 100))
        self.percent_var.set(f"{percent}%")


class InfoTooltip:
    """تلميح معلومات"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        """عرض التلميح"""
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(
            self.tooltip,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padding=5,
            font=("Segoe UI", 9),
        )
        label.pack()

    def hide(self, event=None):
        """إخفاء التلميح"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

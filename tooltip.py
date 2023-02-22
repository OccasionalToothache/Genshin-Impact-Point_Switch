import tkinter as tk


class Tooltip:
    def __init__(self, widget, text, topmost=False):
        self.topmost = topmost
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.tooltip_visible = False

    def show_tooltip(self, event=None):
        if not self.tooltip_visible:
            self.tooltip_visible = True
            x = self.widget.winfo_rootx() + 10
            y = self.widget.winfo_rooty() - 40
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry("+{}+{}".format(x, y))
            self.tooltip.configure(background="#ffffe0", borderwidth=1,highlightthickness=0, relief="solid")
            self.tooltip_label = tk.Label(self.tooltip, text=self.text,font=("黑体", "10", "normal"),background="#ffffe0", padx=2, pady=2)
            self.tooltip_label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_visible:
            self.tooltip_visible = False
            self.tooltip.destroy()
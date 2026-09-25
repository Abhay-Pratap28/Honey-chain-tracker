
# HONEY CHAIN - FINAL GUI
# Digital Honey Traceability System

import tkinter as tk
from tkinter import messagebox
from honey_chain import honey_chain


# =========================================================
# COLORS
# =========================================================

BG = "#F7F3EA"
CARD = "#FFFFFF"
DARK = "#3E2723"
HONEY = "#D99A00"
HONEY_LIGHT = "#FFF3CD"
GREEN = "#2E7D32"
GREEN_LIGHT = "#E8F5E9"
RED = "#C62828"
RED_LIGHT = "#FFEBEE"
TEXT = "#333333"
MUTED = "#777777"
BORDER = "#E0D6C5"


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def style_entry(entry):
    entry.configure(
        font=("Segoe UI", 11),
        relief="solid",
        bd=1
    )


def make_label(parent, text, size=11, bold=False, color=TEXT):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", size, "bold" if bold else "normal"),
        bg=parent.cget("bg"),
        fg=color
    )


def create_button(parent, text, command, width=20):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        height=2,
        font=("Segoe UI", 10, "bold"),
        bg=HONEY,
        fg="white",
        activebackground="#B57C00",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        bd=0
    )


# =========================================================
# REGISTER BATCH
# =========================================================

def register_batch_window():

    window = tk.Toplevel(root)
    window.title("Register New Honey Batch")
    window.geometry("520x560")
    window.configure(bg=BG)
    window.resizable(False, False)

    make_label(
        window,
        "🍯  REGISTER NEW BATCH",
        20,
        True,
        DARK
    ).pack(pady=(25, 5))

    make_label(
        window,
        "Create a new traceable honey batch",
        10,
        False,
        MUTED
    ).pack(pady=(0, 20))

    form = tk.Frame(window, bg=CARD, padx=30, pady=25)
    form.pack(padx=30, fill="x")

    # Batch ID
    make_label(form, "Batch ID", 10, True).pack(anchor="w")

    batch_id_entry = tk.Entry(form, width=42)
    style_entry(batch_id_entry)
    batch_id_entry.pack(pady=(5, 15), ipady=5)

    # Beekeeper
    make_label(form, "Beekeeper / Farm Name", 10, True).pack(anchor="w")

    beekeeper_entry = tk.Entry(form, width=42)
    style_entry(beekeeper_entry)
    beekeeper_entry.pack(pady=(5, 15), ipady=5)

    # Location
    make_label(form, "Harvest Location", 10, True).pack(anchor="w")

    location_entry = tk.Entry(form, width=42)
    style_entry(location_entry)
    location_entry.pack(pady=(5, 15), ipady=5)

    # Quantity
    make_label(form, "Quantity", 10, True).pack(anchor="w")

    quantity_entry = tk.Entry(form, width=42)
    style_entry(quantity_entry)
    quantity_entry.pack(pady=(5, 20), ipady=5)

    def register():

        batch_id = batch_id_entry.get().strip()
        beekeeper = beekeeper_entry.get().strip()
        location = location_entry.get().strip()
        quantity = quantity_entry.get().strip()

        if not batch_id or not beekeeper or not location or not quantity:
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        if honey_chain.find_batch(batch_id):
            messagebox.showwarning(
                "Duplicate Batch",
                "This batch already exists."
            )
            return

        honey_chain.register_batch(
            batch_id,
            beekeeper,
            location,
            quantity
        )

        messagebox.showinfo(
            "Batch Registered",
            f"Batch {batch_id} has been successfully registered."
        )

        window.destroy()

    create_button(
        window,
        "REGISTER BATCH",
        register,
        25
    ).pack(pady=25)


# =========================================================
# UPDATE BATCH
# =========================================================

def update_batch_window():

    window = tk.Toplevel(root)
    window.title("Update Honey Batch")
    window.geometry("560x650")
    window.configure(bg=BG)
    window.resizable(False, False)

    make_label(
        window,
        "🔄  UPDATE BATCH",
        20,
        True,
        DARK
    ).pack(pady=(25, 5))

    make_label(
        window,
        "Move the batch to its next supply-chain stage",
        10,
        False,
        MUTED
    ).pack(pady=(0, 20))

    form = tk.Frame(window, bg=CARD, padx=30, pady=20)
    form.pack(padx=30, fill="x")

    # Batch ID
    make_label(form, "Batch ID", 10, True).pack(anchor="w")

    batch_id_entry = tk.Entry(form, width=45)
    style_entry(batch_id_entry)
    batch_id_entry.pack(pady=(5, 15), ipady=5)

    # Stage
    make_label(form, "Next Supply Chain Stage", 10, True).pack(anchor="w")

    stage_var = tk.StringVar()
    stage_var.set("extracted")

    stages = [
        "extracted",
        "processed",
        "packaged",
        "dispatched"
    ]

    stage_menu = tk.OptionMenu(
        form,
        stage_var,
        *stages
    )

    stage_menu.config(
        width=35,
        font=("Segoe UI", 10),
        bg="white",
        relief="solid",
        bd=1
    )

    stage_menu.pack(pady=(5, 15))

    # Location
    make_label(form, "Current Location", 10, True).pack(anchor="w")

    location_entry = tk.Entry(form, width=45)
    style_entry(location_entry)
    location_entry.pack(pady=(5, 15), ipady=5)

    # Handler
    make_label(form, "Handler / Unit Name", 10, True).pack(anchor="w")

    handler_entry = tk.Entry(form, width=45)
    style_entry(handler_entry)
    handler_entry.pack(pady=(5, 15), ipady=5)

    optional_frame = tk.Frame(form, bg=CARD)
    optional_frame.pack(fill="x")

    quality_frame = tk.Frame(
        optional_frame,
        bg=CARD
    )

    seal_frame = tk.Frame(
        optional_frame,
        bg=CARD
    )

    quality_label = tk.Label(
        quality_frame,
        text="Quality / Test Status",
        font=("Segoe UI", 10, "bold"),
        bg=CARD,
        fg=TEXT
    )

    quality_entry = tk.Entry(
        quality_frame,
        width=45
    )
    style_entry(quality_entry)

    seal_label = tk.Label(
        seal_frame,
        text="Seal ID",
        font=("Segoe UI", 10, "bold"),
        bg=CARD,
        fg=TEXT
    )

    seal_entry = tk.Entry(
        seal_frame,
        width=45
    )
    style_entry(seal_entry)

    def change_stage(*args):

        quality_frame.pack_forget()
        seal_frame.pack_forget()

        if stage_var.get() == "processed":

            quality_frame.pack(fill="x", pady=5)

            quality_label.pack(anchor="w")
            quality_entry.pack(pady=(5, 10), ipady=5)

        elif stage_var.get() == "packaged":

            seal_frame.pack(fill="x", pady=5)

            seal_label.pack(anchor="w")
            seal_entry.pack(pady=(5, 10), ipady=5)

    stage_var.trace_add("write", change_stage)

    def update():

        batch_id = batch_id_entry.get().strip()
        stage = stage_var.get().strip()
        location = location_entry.get().strip()
        handler = handler_entry.get().strip()

        quality = None
        seal_id = None

        if not batch_id:

            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter Batch ID."
            )
            return

        if not location:

            messagebox.showwarning(
                "Missing Location",
                "Please enter the current location."
            )
            return

        if not handler:

            messagebox.showwarning(
                "Missing Handler",
                "Please enter the handler/unit name."
            )
            return

        if stage == "processed":

            quality = quality_entry.get().strip()

            if not quality:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter Quality / Test Status."
                )
                return

        if stage == "packaged":

            seal_id = seal_entry.get().strip()

            if not seal_id:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter Seal ID."
                )
                return

        if not honey_chain.find_batch(batch_id):

            messagebox.showerror(
                "Batch Not Found",
                f"Batch {batch_id} does not exist."
            )
            return

        honey_chain.update_batch(
            batch_id,
            stage,
            location,
            handler,
            quality,
            seal_id
        )

        messagebox.showinfo(
            "Batch Updated",
            f"Batch {batch_id} moved to {stage.upper()}.\n\n"
            "A new QR code has been generated."
        )

        window.destroy()

    create_button(
        window,
        "UPDATE BATCH",
        update,
        28
    ).pack(pady=25)


# =========================================================
# VERIFY BATCH
# =========================================================

def verify_batch_window():

    window = tk.Toplevel(root)
    window.title("Verify Honey Batch")
    window.geometry("780x680")
    window.configure(bg=BG)

    make_label(
        window,
        "✓  VERIFY BATCH",
        20,
        True,
        DARK
    ).pack(pady=(25, 5))

    make_label(
        window,
        "Verify the integrity of the blockchain record",
        10,
        False,
        MUTED
    ).pack(pady=(0, 15))

    top = tk.Frame(window, bg=CARD, padx=25, pady=15)
    top.pack(padx=30, fill="x")

    make_label(
        top,
        "Enter Batch ID",
        10,
        True
    ).pack(side="left")

    batch_id_entry = tk.Entry(top, width=30)
    style_entry(batch_id_entry)
    batch_id_entry.pack(
        side="left",
        padx=15,
        ipady=5
    )

    result_frame = tk.Frame(window, bg=CARD)
    result_box = tk.Text(
        result_frame,
        width=85,
        height=29,
        font=("Consolas", 10),
        bg="#FAFAFA",
        fg=TEXT,
        relief="flat",
        padx=15,
        pady=15
    )

    scrollbar = tk.Scrollbar(
        result_frame,
        command=result_box.yview
    )

    result_box.configure(
        yscrollcommand=scrollbar.set
    )

    def verify():

        batch_id = batch_id_entry.get().strip()

        if not batch_id:
            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter Batch ID."
            )
            return

        history = honey_chain.find_batch(batch_id)

        if not history:
            messagebox.showerror(
                "Batch Not Found",
                f"Batch {batch_id} does not exist."
            )
            return

        result_frame.pack(
            padx=30,
            pady=15,
            fill="both",
            expand=True
        )

        result_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        result_box.delete("1.0", tk.END)

        first_record = history[0].data

        result_box.insert(
            tk.END,
            "🍯  HONEY CHAIN - VERIFICATION REPORT\n"
        )

        result_box.insert(
            tk.END,
            "=" * 65 + "\n\n"
        )

        result_box.insert(
            tk.END,
            f"Batch ID       : {first_record['batch_id']}\n"
        )

        result_box.insert(
            tk.END,
            f"Beekeeper      : {first_record['beekeeper']}\n"
        )

        result_box.insert(
            tk.END,
            f"Quantity       : {first_record['quantity']}\n"
        )

        result_box.insert(
            tk.END,
            f"Harvest Site   : {first_record['location']}\n\n"
        )

        result_box.insert(
            tk.END,
            "SUPPLY CHAIN JOURNEY\n"
        )

        result_box.insert(
            tk.END,
            "-" * 65 + "\n"
        )

        for number, block in enumerate(history, start=1):

            data = block.data

            result_box.insert(
                tk.END,
                f"\nSTEP {number}  |  {data.get('stage', '').upper()}\n"
            )

            result_box.insert(
                tk.END,
                f"Location : {data.get('location', '')}\n"
            )

            if data.get("handler"):
                result_box.insert(
                    tk.END,
                    f"Handler  : {data.get('handler')}\n"
                )

            if data.get("quality"):
                result_box.insert(
                    tk.END,
                    f"Quality  : {data.get('quality')}\n"
                )

            if data.get("seal_id"):
                result_box.insert(
                    tk.END,
                    f"Seal ID  : {data.get('seal_id')}\n"
                )

            result_box.insert(
                tk.END,
                f"Time     : {block.timestamp}\n"
            )

            result_box.insert(
                tk.END,
                "-" * 65 + "\n"
            )

        status = honey_chain.is_valid(batch_id)

        result_box.insert(
            tk.END,
            "\n"
        )

        if status:

            result_box.insert(
                tk.END,
                "  ✓ BLOCKCHAIN STATUS: VALID\n"
            )

            result_box.insert(
                tk.END,
                "  The recorded journey has not been altered.\n"
            )

        else:

            result_box.insert(
                tk.END,
                "  ⚠ BLOCKCHAIN STATUS: TAMPERED\n"
            )

            result_box.insert(
                tk.END,
                "  The stored record does not match its blockchain hash.\n"
            )

    create_button(
        top,
        "VERIFY",
        verify,
        12
    ).pack(side="left")

    window.bind(
        "<Return>",
        lambda event: verify()
    )


# =========================================================
# TRACK BATCH
# =========================================================

def track_batch_window():

    window = tk.Toplevel(root)
    window.title("Track Honey Batch")
    window.geometry("780x680")
    window.configure(bg=BG)

    make_label(
        window,
        "📍  TRACK BATCH",
        20,
        True,
        DARK
    ).pack(pady=(25, 5))

    make_label(
        window,
        "View the complete journey of a honey batch",
        10,
        False,
        MUTED
    ).pack(pady=(0, 15))

    top = tk.Frame(
        window,
        bg=CARD,
        padx=25,
        pady=15
    )
    top.pack(
        padx=30,
        fill="x"
    )

    make_label(
        top,
        "Enter Batch ID",
        10,
        True
    ).pack(side="left")

    batch_id_entry = tk.Entry(
        top,
        width=30
    )

    style_entry(batch_id_entry)

    batch_id_entry.pack(
        side="left",
        padx=15,
        ipady=5
    )

    result_frame = tk.Frame(
        window,
        bg=CARD
    )

    result_box = tk.Text(
        result_frame,
        width=85,
        height=29,
        font=("Consolas", 10),
        bg="#FAFAFA",
        fg=TEXT,
        relief="flat",
        padx=15,
        pady=15
    )

    scrollbar = tk.Scrollbar(
        result_frame,
        command=result_box.yview
    )

    result_box.configure(
        yscrollcommand=scrollbar.set
    )

    def track():

        batch_id = batch_id_entry.get().strip()

        if not batch_id:

            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter Batch ID."
            )
            return

        history = honey_chain.find_batch(batch_id)

        if not history:

            messagebox.showerror(
                "Batch Not Found",
                f"Batch {batch_id} does not exist."
            )
            return

        result_frame.pack(
            padx=30,
            pady=15,
            fill="both",
            expand=True
        )

        result_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        result_box.delete(
            "1.0",
            tk.END
        )

        first_record = history[0].data
        current_stage = history[-1].data.get(
            "stage",
            "harvested"
        )

        result_box.insert(
            tk.END,
            "🍯  HONEY BATCH JOURNEY\n"
        )

        result_box.insert(
            tk.END,
            "=" * 65 + "\n\n"
        )

        result_box.insert(
            tk.END,
            f"CURRENT STAGE : {current_stage.upper()}\n\n"
        )

        result_box.insert(
            tk.END,
            f"Batch ID       : {first_record['batch_id']}\n"
        )

        result_box.insert(
            tk.END,
            f"Beekeeper      : {first_record['beekeeper']}\n"
        )

        result_box.insert(
            tk.END,
            f"Quantity       : {first_record['quantity']}\n"
        )

        result_box.insert(
            tk.END,
            f"Harvest Site   : {first_record['location']}\n\n"
        )

        result_box.insert(
            tk.END,
            "SUPPLY CHAIN JOURNEY\n"
        )

        result_box.insert(
            tk.END,
            "-" * 65 + "\n"
        )

        for number, block in enumerate(history, start=1):

            data = block.data

            result_box.insert(
                tk.END,
                f"\n[{number}]  {data.get('stage', '').upper()}\n"
            )

            result_box.insert(
                tk.END,
                f"Location : {data.get('location', '')}\n"
            )

            if data.get("handler"):
                result_box.insert(
                    tk.END,
                    f"Handler  : {data.get('handler')}\n"
                )

            if data.get("quality"):
                result_box.insert(
                    tk.END,
                    f"Quality  : {data.get('quality')}\n"
                )

            if data.get("seal_id"):
                result_box.insert(
                    tk.END,
                    f"Seal ID  : {data.get('seal_id')}\n"
                )

            result_box.insert(
                tk.END,
                f"Time     : {block.timestamp}\n"
            )

            result_box.insert(
                tk.END,
                "\n" + "-" * 65 + "\n"
            )

    create_button(
        top,
        "TRACK",
        track,
        12
    ).pack(side="left")

    window.bind(
        "<Return>",
        lambda event: track()
    )


# =========================================================
# MAIN DASHBOARD
# =========================================================

root = tk.Tk()

root.title("Honey Chain - Digital Honey Traceability")
root.geometry("1000x700")
root.configure(bg=BG)
root.resizable(False, False)


# ---------------- HEADER ----------------

header = tk.Frame(
    root,
    bg=DARK,
    height=145
)

header.pack(
    fill="x"
)

header.pack_propagate(False)

tk.Label(
    header,
    text="🍯  HONEY CHAIN",
    font=("Segoe UI", 30, "bold"),
    bg=DARK,
    fg="#FFD54F"
).pack(pady=(25, 3))

tk.Label(
    header,
    text="DIGITAL HONEY TRACEABILITY SYSTEM",
    font=("Segoe UI", 12, "bold"),
    bg=DARK,
    fg="white"
).pack()

tk.Label(
    header,
    text="From beekeeper to consumer — one verifiable journey",
    font=("Segoe UI", 10),
    bg=DARK,
    fg="#E0E0E0"
).pack(pady=5)


# ---------------- MAIN CONTENT ----------------

content = tk.Frame(
    root,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=45,
    pady=30
)


tk.Label(
    content,
    text="TRACEABILITY CONTROL PANEL",
    font=("Segoe UI", 16, "bold"),
    bg=BG,
    fg=DARK
).pack()

tk.Label(
    content,
    text="Manage and verify every stage of the honey supply chain",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(
    pady=(3, 20)
)


# ---------------- BUTTON GRID ----------------

button_area = tk.Frame(
    content,
    bg=BG
)

button_area.pack()


def create_action_card(
    parent,
    row,
    column,
    icon,
    title,
    description,
    command
):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=390,
        height=150,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.grid(
        row=row,
        column=column,
        padx=12,
        pady=12
    )

    card.grid_propagate(False)

    tk.Label(
        card,
        text=icon,
        font=("Segoe UI Emoji", 25),
        bg=CARD
    ).place(
        x=20,
        y=20
    )

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 14, "bold"),
        bg=CARD,
        fg=DARK
    ).place(
        x=75,
        y=20
    )

    tk.Label(
        card,
        text=description,
        font=("Segoe UI", 9),
        bg=CARD,
        fg=MUTED,
        justify="left"
    ).place(
        x=75,
        y=50
    )

    button = tk.Button(
        card,
        text="OPEN",
        command=command,
        font=("Segoe UI", 9, "bold"),
        bg=HONEY,
        fg="white",
        activebackground="#B57C00",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=12
    )

    button.place(
        x=75,
        y=100
    )


create_action_card(
    button_area,
    0,
    0,
    "＋",
    "Register Batch",
    "Create a new honey batch\nand record its origin.",
    register_batch_window
)

create_action_card(
    button_area,
    0,
    1,
    "↻",
    "Update Batch",
    "Move the batch through\nits supply-chain stages.",
    update_batch_window
)

create_action_card(
    button_area,
    1,
    0,
    "✓",
    "Verify Batch",
    "Check blockchain integrity\nand detect tampering.",
    verify_batch_window
)

create_action_card(
    button_area,
    1,
    1,
    "⌖",
    "Track Batch",
    "View the complete honey\njourney from origin onward.",
    track_batch_window
)


# ---------------- SUPPLY CHAIN FLOW ----------------

flow_frame = tk.Frame(
    content,
    bg=BG
)

flow_frame.pack(
    pady=(25, 0)
)

tk.Label(
    flow_frame,
    text="SUPPLY CHAIN",
    font=("Segoe UI", 10, "bold"),
    bg=BG,
    fg=MUTED
).pack(
    pady=(0, 8)
)

flow = tk.Frame(
    flow_frame,
    bg=BG
)

flow.pack()

stages = [
    "🐝 Harvest",
    "Extraction",
    "Processing",
    "Packaging",
    "Dispatch"
]

for i, stage in enumerate(stages):

    tk.Label(
        flow,
        text=stage,
        font=("Segoe UI", 9, "bold"),
        bg=HONEY_LIGHT,
        fg=DARK,
        padx=12,
        pady=6
    ).pack(
        side="left",
        padx=3
    )

    if i < len(stages) - 1:

        tk.Label(
            flow,
            text="→",
            font=("Segoe UI", 12, "bold"),
            bg=BG,
            fg=HONEY
        ).pack(
            side="left"
        )


# ---------------- FOOTER ----------------

footer = tk.Frame(
    root,
    bg=DARK,
    height=35
)

footer.pack(
    side="bottom",
    fill="x"
)

footer.pack_propagate(False)

tk.Label(
    footer,
    text="Blockchain-backed provenance  •  SQLite database  •  QR-enabled traceability",
    font=("Segoe UI", 9),
    bg=DARK,
    fg="#E0E0E0"
).pack(
    pady=8
)


root.mainloop()

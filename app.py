# FINAL GUI - HONEY CHAIN

import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

from honey_chain import honey_chain


# ============================================================
# COLORS
# ============================================================

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


# ============================================================
# DATABASE
# ============================================================

DATABASE = "honey_chain_database.db"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def style_entry(entry):
    entry.configure(
        font=("Segoe UI", 11),
        bg="white",
        fg=TEXT,
        relief="solid",
        bd=1
    )


def make_label(parent, text, size=10, bold=False, color=TEXT):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", size, "bold" if bold else "normal"),
        bg=parent.cget("bg"),
        fg=color
    )


def create_button(parent, text, command, bg_color=HONEY):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 11, "bold"),
        bg=bg_color,
        fg="white",
        activebackground=bg_color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=20,
        height=2
    )


# ============================================================
# REGISTER BATCH WINDOW
# ============================================================

def register_batch_window():

    window = tk.Toplevel(root)
    window.title("Register New Honey Batch")
    window.geometry("500x450")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="🐝 REGISTER NEW HONEY BATCH",
        font=("Segoe UI", 18, "bold"),
        bg=DARK,
        fg="white",
        pady=15
    ).pack(fill="x")

    form = tk.Frame(window, bg=BG)
    form.pack(pady=25)

    make_label(
        form,
        "Batch ID",
        10,
        True
    ).grid(row=0, column=0, sticky="w", pady=8)

    batch_entry = tk.Entry(form, width=32)
    style_entry(batch_entry)
    batch_entry.grid(row=0, column=1, pady=8, padx=10)

    make_label(
        form,
        "Beekeeper / Farm Name",
        10,
        True
    ).grid(row=1, column=0, sticky="w", pady=8)

    beekeeper_entry = tk.Entry(form, width=32)
    style_entry(beekeeper_entry)
    beekeeper_entry.grid(row=1, column=1, pady=8, padx=10)

    make_label(
        form,
        "Harvest Location",
        10,
        True
    ).grid(row=2, column=0, sticky="w", pady=8)

    location_entry = tk.Entry(form, width=32)
    style_entry(location_entry)
    location_entry.grid(row=2, column=1, pady=8, padx=10)

    make_label(
        form,
        "Quantity",
        10,
        True
    ).grid(row=3, column=0, sticky="w", pady=8)

    quantity_entry = tk.Entry(form, width=32)
    style_entry(quantity_entry)
    quantity_entry.grid(row=3, column=1, pady=8, padx=10)

    def register():

        batch_id = batch_entry.get().strip()
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
            messagebox.showerror(
                "Duplicate Batch",
                "This Batch ID already exists."
            )
            return

        try:

            honey_chain.register_batch(
                batch_id,
                beekeeper,
                location,
                quantity
            )

            messagebox.showinfo(
                "Success",
                f"Batch {batch_id} registered successfully."
            )

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to register batch.\n\n{e}"
            )

    create_button(
        window,
        "REGISTER BATCH",
        register,
        GREEN
    ).pack(pady=15)


# ============================================================
# UPDATE BATCH WINDOW
# ============================================================

# ============================================================
# UPDATE BATCH WINDOW
# ============================================================

def update_batch_window():

    window = tk.Toplevel(root)
    window.title("Update Honey Batch")
    window.geometry("520x500")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="🔄 UPDATE HONEY BATCH",
        font=("Segoe UI", 18, "bold"),
        bg=DARK,
        fg="white",
        pady=15
    ).pack(fill="x")

    form = tk.Frame(window, bg=BG)
    form.pack(pady=20)

    # --------------------------------------------------------
    # BATCH ID
    # --------------------------------------------------------

    make_label(
        form,
        "Batch ID",
        10,
        True
    ).grid(row=0, column=0, sticky="w", pady=8)

    batch_entry = tk.Entry(form, width=32)
    style_entry(batch_entry)
    batch_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=8
    )

    # --------------------------------------------------------
    # STAGE
    # --------------------------------------------------------

    make_label(
        form,
        "Stage",
        10,
        True
    ).grid(row=1, column=0, sticky="w", pady=8)

    stage_var = tk.StringVar(value="extracted")

    stage_menu = tk.OptionMenu(
        form,
        stage_var,
        "extracted",
        "processed",
        "packaged",
        "dispatched"
    )

    stage_menu.config(
        font=("Segoe UI", 10),
        bg="white",
        width=25,
        relief="solid"
    )

    stage_menu.grid(
        row=1,
        column=1,
        padx=10,
        pady=8
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    make_label(
        form,
        "Location",
        10,
        True
    ).grid(row=2, column=0, sticky="w", pady=8)

    location_entry = tk.Entry(form, width=32)
    style_entry(location_entry)
    location_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=8
    )

    # --------------------------------------------------------
    # HANDLER
    # --------------------------------------------------------

    make_label(
        form,
        "Handler",
        10,
        True
    ).grid(row=3, column=0, sticky="w", pady=8)

    handler_entry = tk.Entry(form, width=32)
    style_entry(handler_entry)
    handler_entry.grid(
        row=3,
        column=1,
        padx=10,
        pady=8
    )

    # --------------------------------------------------------
    # QUALITY - ONLY FOR PROCESSED
    # --------------------------------------------------------

    quality_label = make_label(
        form,
        "Quality",
        10,
        True
    )

    quality_entry = tk.Entry(
        form,
        width=32
    )

    style_entry(quality_entry)

    # --------------------------------------------------------
    # SEAL ID - ONLY FOR PACKAGED
    # --------------------------------------------------------

    seal_label = make_label(
        form,
        "Seal ID",
        10,
        True
    )

    seal_entry = tk.Entry(
        form,
        width=32
    )

    style_entry(seal_entry)

    # --------------------------------------------------------
    # SHOW/HIDE STAGE-SPECIFIC FIELDS
    # --------------------------------------------------------

    def update_fields(*args):

        # Hide both fields first
        quality_label.grid_remove()
        quality_entry.grid_remove()

        seal_label.grid_remove()
        seal_entry.grid_remove()

        # Processed → Quality
        if stage_var.get() == "processed":

            quality_label.grid(
                row=4,
                column=0,
                sticky="w",
                pady=8
            )

            quality_entry.grid(
                row=4,
                column=1,
                padx=10,
                pady=8
            )

        # Packaged → Seal ID
        elif stage_var.get() == "packaged":

            seal_label.grid(
                row=4,
                column=0,
                sticky="w",
                pady=8
            )

            seal_entry.grid(
                row=4,
                column=1,
                padx=10,
                pady=8
            )

    stage_var.trace_add(
        "write",
        update_fields
    )

    # Set initial state
    update_fields()

    # --------------------------------------------------------
    # UPDATE FUNCTION
    # --------------------------------------------------------

    def update():

        batch_id = batch_entry.get().strip()
        stage = stage_var.get()
        location = location_entry.get().strip()
        handler = handler_entry.get().strip()
        quality = quality_entry.get().strip()
        seal_id = seal_entry.get().strip()

        if not batch_id:

            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter Batch ID."
            )

            return

        if not honey_chain.find_batch(batch_id):

            messagebox.showerror(
                "Batch Not Found",
                "No batch exists with this Batch ID."
            )

            return

        if not location or not handler:

            messagebox.showwarning(
                "Missing Information",
                "Location and Handler are required."
            )

            return

        # Quality required ONLY for processed
        if stage == "processed" and not quality:

            messagebox.showwarning(
                "Missing Quality",
                "Please enter quality information."
            )

            return

        # Seal ID required ONLY for packaged
        if stage == "packaged" and not seal_id:

            messagebox.showwarning(
                "Missing Seal ID",
                "Please enter Seal ID."
            )

            return

        try:

            honey_chain.update_batch(
                batch_id,
                stage,
                location,
                handler,
                quality,
                seal_id
            )

            messagebox.showinfo(
                "Success",
                "Batch updated successfully.\n\n"
                "A new blockchain block and QR code have been generated."
            )

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to update batch.\n\n{e}"
            )

    # --------------------------------------------------------
    # UPDATE BUTTON
    # --------------------------------------------------------

    create_button(
        window,
        "UPDATE BATCH",
        update,
        HONEY
    ).pack(pady=15)

def verify_batch_window():

    window = tk.Toplevel(root)
    window.title("Verify Honey Batch")
    window.geometry("700x600")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="✓ VERIFY HONEY BATCH",
        font=("Segoe UI", 18, "bold"),
        bg=DARK,
        fg="white",
        pady=15
    ).pack(fill="x")

    input_frame = tk.Frame(
        window,
        bg=BG
    )

    input_frame.pack(
        pady=20
    )

    tk.Label(
        input_frame,
        text="Batch ID:",
        font=("Segoe UI", 11, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        side="left",
        padx=5
    )

    batch_entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 11),
        width=25
    )

    batch_entry.pack(
        side="left",
        padx=5
    )

    # Result frame is NOT created initially.
    # It will appear only after verification.

    def verify():

        batch_id = batch_entry.get().strip()

        if not batch_id:

            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter Batch ID."
            )

            return

        if not honey_chain.find_batch(batch_id):

            messagebox.showerror(
                "Batch Not Found",
                "No batch exists with this Batch ID."
            )

            return

        # Remove old result area if it exists
        for widget in window.winfo_children():

            if getattr(widget, "is_result_frame", False):
                widget.destroy()

        result_frame = tk.Frame(
            window,
            bg=BG
        )

        result_frame.is_result_frame = True

        result_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        result_box = tk.Text(
            result_frame,
            font=("Consolas", 10),
            bg="white",
            fg=TEXT,
            relief="solid",
            bd=1,
            wrap="word"
        )

        result_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            result_frame,
            command=result_box.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        result_box.config(
            yscrollcommand=scrollbar.set
        )

        try:

            data = honey_chain.find_batch(batch_id)

            result_box.insert(
                tk.END,
                "HONEY BATCH DETAILS\n"
            )

            result_box.insert(
                tk.END,
                "=" * 65 + "\n\n"
            )

            if isinstance(data, dict):

                result_box.insert(
                    tk.END,
                    f"Batch ID     : {data.get('batch_id', batch_id)}\n"
                )

                result_box.insert(
                    tk.END,
                    f"Beekeeper    : {data.get('beekeeper', 'N/A')}\n"
                )

                result_box.insert(
                    tk.END,
                    f"Location     : {data.get('location', 'N/A')}\n"
                )

                result_box.insert(
                    tk.END,
                    f"Quantity     : {data.get('quantity', 'N/A')}\n\n"
                )

            history = honey_chain.load_batch_from_database(
                batch_id
            )

            result_box.insert(
                tk.END,
                "SUPPLY CHAIN JOURNEY\n"
            )

            result_box.insert(
                tk.END,
                "-" * 65 + "\n"
            )

            for block in history:

                stage = block.data.get(
                    "stage",
                    "N/A"
                )

                location = block.data.get(
                    "location",
                    "N/A"
                )

                handler = block.data.get(
                    "handler",
                    "N/A"
                )

                result_box.insert(
                    tk.END,
                    f"Block {block.index} → "
                    f"{stage.upper()}\n"
                )

                result_box.insert(
                    tk.END,
                    f"  Location : {location}\n"
                )

                if stage != "harvested":

                    result_box.insert(
                        tk.END,
                        f"  Handler  : {handler}\n"
                    )

                result_box.insert(
                    tk.END,
                    "\n"
                )

            valid = honey_chain.is_valid(
                batch_id
            )

            result_box.insert(
                tk.END,
                "=" * 65 + "\n"
            )

            if valid:

                result_box.insert(
                    tk.END,
                    "\n✓ BLOCKCHAIN STATUS: VALID\n"
                )

                result_box.insert(
                    tk.END,
                    "The batch history is authentic and has "
                    "not been tampered with.\n"
                )

            else:

                result_box.insert(
                    tk.END,
                    "\n⚠ BLOCKCHAIN STATUS: TAMPERED\n"
                )

                result_box.insert(
                    tk.END,
                    "Possible data tampering detected.\n"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to verify batch.\n\n{e}"
            )

    tk.Button(
        input_frame,
        text="VERIFY",
        command=verify,
        font=("Segoe UI", 10, "bold"),
        bg=GREEN,
        fg="white",
        activebackground="#1B5E20",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=12
    ).pack(
        side="left",
        padx=10
    )


# ============================================================
# TRACK BATCH WINDOW
# ============================================================

def track_batch_window():

    window = tk.Toplevel(root)
    window.title("Track Honey Batch")
    window.geometry("700x600")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="📦 TRACK HONEY BATCH",
        font=("Segoe UI", 18, "bold"),
        bg=DARK,
        fg="white",
        pady=15
    ).pack(fill="x")

    input_frame = tk.Frame(
        window,
        bg=BG
    )

    input_frame.pack(
        pady=20
    )

    tk.Label(
        input_frame,
        text="Batch ID:",
        font=("Segoe UI", 11, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        side="left",
        padx=5
    )

    batch_entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 11),
        width=25
    )

    batch_entry.pack(
        side="left",
        padx=5
    )

    def track():

        batch_id = batch_entry.get().strip()

        if not batch_id:

            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter Batch ID."
            )

            return

        if not honey_chain.find_batch(batch_id):

            messagebox.showerror(
                "Batch Not Found",
                "No batch exists with this Batch ID."
            )

            return

        # Remove old result area
        for widget in window.winfo_children():

            if getattr(widget, "is_result_frame", False):
                widget.destroy()

        result_frame = tk.Frame(
            window,
            bg=BG
        )

        result_frame.is_result_frame = True

        result_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        result_box = tk.Text(
            result_frame,
            font=("Consolas", 10),
            bg="white",
            fg=TEXT,
            relief="solid",
            bd=1,
            wrap="word"
        )

        result_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            result_frame,
            command=result_box.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        result_box.config(
            yscrollcommand=scrollbar.set
        )

        try:

            data = honey_chain.find_batch(batch_id)

            history = honey_chain.load_batch_from_database(
                batch_id
            )

            result_box.insert(
                tk.END,
                "HONEY BATCH TRACKING\n"
            )

            result_box.insert(
                tk.END,
                "=" * 65 + "\n\n"
            )

            if isinstance(data, dict):

                result_box.insert(
                    tk.END,
                    f"Batch ID  : {data.get('batch_id', batch_id)}\n"
                )

                result_box.insert(
                    tk.END,
                    f"Beekeeper : {data.get('beekeeper', 'N/A')}\n"
                )

                result_box.insert(
                    tk.END,
                    f"Location  : {data.get('location', 'N/A')}\n"
                )

                result_box.insert(
                    tk.END,
                    f"Quantity  : {data.get('quantity', 'N/A')}\n\n"
                )

            if history:

                current_stage = history[-1].data.get(
                    "stage",
                    "N/A"
                )

                result_box.insert(
                    tk.END,
                    f"CURRENT STAGE: {current_stage.upper()}\n\n"
                )

            result_box.insert(
                tk.END,
                "SUPPLY CHAIN JOURNEY\n"
            )

            result_box.insert(
                tk.END,
                "-" * 65 + "\n"
            )

            for block in history:

                stage = block.data.get(
                    "stage",
                    "N/A"
                )

                location = block.data.get(
                    "location",
                    "N/A"
                )

                handler = block.data.get(
                    "handler",
                    "N/A"
                )

                result_box.insert(
                    tk.END,
                    f"Block {block.index} → "
                    f"{stage.upper()}\n"
                )

                result_box.insert(
                    tk.END,
                    f"  Location : {location}\n"
                )

                if stage != "harvested":

                    result_box.insert(
                        tk.END,
                        f"  Handler  : {handler}\n"
                    )

                result_box.insert(
                    tk.END,
                    "\n"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to track batch.\n\n{e}"
            )

    tk.Button(
        input_frame,
        text="TRACK",
        command=track,
        font=("Segoe UI", 10, "bold"),
        bg=HONEY,
        fg="white",
        activebackground="#B57C00",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=12
    ).pack(
        side="left",
        padx=10
    )


# ============================================================
# VERIFY BLOCKCHAIN WINDOW
# ============================================================

# ============================================================
# VERIFY BLOCKCHAIN WINDOW
# ============================================================

def verify_blockchain_window():

    window = tk.Toplevel(root)
    window.title("Blockchain Verification")
    window.geometry("650x300")
    window.configure(bg=BG)
    window.resizable(False, False)

    tk.Label(
        window,
        text="🔗 BLOCKCHAIN VERIFICATION",
        font=("Segoe UI", 18, "bold"),
        bg=DARK,
        fg="white",
        pady=15
    ).pack(fill="x")

    input_frame = tk.Frame(
        window,
        bg=BG
    )

    input_frame.pack(pady=25)

    tk.Label(
        input_frame,
        text="Batch ID:",
        font=("Segoe UI", 11, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(side="left", padx=5)

    batch_entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 11),
        width=25
    )

    batch_entry.pack(side="left", padx=5)

    def verify():

        batch_id = batch_entry.get().strip()

        if not batch_id:

            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter a Batch ID."
            )

            return

        if not honey_chain.find_batch(batch_id):

            messagebox.showerror(
                "Batch Not Found",
                "No batch exists with this Batch ID."
            )

            return

        # Remove previous result
        for widget in window.winfo_children():

            if getattr(widget, "is_result_frame", False):
                widget.destroy()

        result_frame = tk.Frame(
            window,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        result_frame.is_result_frame = True

        result_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        try:

            valid = honey_chain.is_valid(batch_id)

            if valid:

                result_label = tk.Label(
                    result_frame,
                    text=(
                        "✓ BLOCKCHAIN IS VALID\n\n"
                        "No tampering detected."
                    ),
                    font=("Segoe UI", 15, "bold"),
                    bg=GREEN_LIGHT,
                    fg=GREEN,
                    pady=25
                )

            else:

                result_label = tk.Label(
                    result_frame,
                    text=(
                        "⚠ BLOCKCHAIN IS TAMPERED\n\n"
                        "Data modification detected."
                    ),
                    font=("Segoe UI", 15, "bold"),
                    bg=RED_LIGHT,
                    fg=RED,
                    pady=25
                )

            result_label.pack(
                fill="x",
                padx=2,
                pady=2
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to verify blockchain.\n\n{e}"
            )

    tk.Button(
        input_frame,
        text="VERIFY",
        command=verify,
        font=("Segoe UI", 10, "bold"),
        bg=GREEN,
        fg="white",
        activebackground="#1B5E20",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=12
    ).pack(
        side="left",
        padx=10
    )

def alter_blockchain_window():
    window = tk.Toplevel(root)
    window.title("Alter Blockchain Data")
    window.geometry("650x430")
    window.configure(bg=BG)
    window.resizable(False, False)

    tk.Label(
        window,
        text="🔧 ALTER BLOCKCHAIN DATA",
        font=("Arial", 20, "bold"),
        bg=DARK,
        fg="white",
        pady=15
    ).pack(fill="x")

    form = tk.Frame(window, bg=BG)
    form.pack(pady=30)

    tk.Label(
        form,
        text="Batch ID",
        font=("Arial", 12, "bold"),
        bg=BG,
        fg=TEXT
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    batch_entry = tk.Entry(
        form,
        font=("Arial", 12),
        width=30
    )
    batch_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        form,
        text="New Quantity",
        font=("Arial", 12, "bold"),
        bg=BG,
        fg=TEXT
    ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

    quantity_entry = tk.Entry(
        form,
        font=("Arial", 12),
        width=30
    )
    quantity_entry.insert(0, "1000 kg")
    quantity_entry.grid(row=1, column=1, padx=10, pady=10)

    result_frame = tk.Frame(
        window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    result_frame.pack(fill="x", padx=35, pady=10)

    result_label = tk.Label(
        result_frame,
        text="Enter a Batch ID and new quantity.",
        font=("Arial", 11),
        bg=CARD,
        fg=MUTED,
        justify="left",
        wraplength=550
    )
    result_label.pack(padx=15, pady=15)

    def alter_data():

        batch_id = batch_entry.get().strip()
        new_quantity = quantity_entry.get().strip()

        if not batch_id:
            result_label.config(
                text="⚠ Please enter Batch ID.",
                fg=RED
            )
            return

        if not new_quantity:
            result_label.config(
                text="⚠ Please enter new quantity.",
                fg=RED
            )
            return

        batch = honey_chain.find_batch(batch_id)

        if not batch:
            result_label.config(
                text=f"❌ Batch '{batch_id}' not found.",
                fg=RED
            )
            return

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT quantity FROM batches WHERE batch_id = ?",
            (batch_id,)
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            result_label.config(
                text=f"❌ Batch '{batch_id}' not found.",
                fg=RED
            )
            return

        old_quantity = row[0]

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE batches
            SET quantity = ?
            WHERE batch_id = ?
            """,
            (new_quantity, batch_id)
        )

        connection.commit()
        connection.close()

        result_label.config(
            text=(
                "⚠ DEMO DATA ALTERED\n\n"
                f"Batch ID: {batch_id}\n"
                f"Quantity changed: {old_quantity} → {new_quantity}\n\n"
                "The blockchain record was not changed.\n"
                "Now use VERIFY BLOCKCHAIN to detect the tampering."
            ),
            fg=RED
        )

    tk.Button(
        window,
        text="🔧 ALTER DATA",
        command=alter_data,
        width=20,
        height=2,
        bg=RED,
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2"
    ).pack(pady=15)

# ============================================================
# MAIN DASHBOARD
# ============================================================

root = tk.Tk()

root.title(
    "Honey Chain - Digital Honey Traceability"
)

root.geometry(
    "1000x700"
)

root.minsize(
    900,
    650
)

root.configure(
    bg=BG
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=DARK,
    height=115
)

header.pack(
    fill="x"
)

header.pack_propagate(False)

tk.Label(
    header,
    text="🍯 HONEY CHAIN",
    font=("Segoe UI", 25, "bold"),
    bg=DARK,
    fg="white"
).pack(
    pady=(18, 2)
)

tk.Label(
    header,
    text="DIGITAL HONEY TRACEABILITY SYSTEM",
    font=("Segoe UI", 11, "bold"),
    bg=DARK,
    fg="#F5D76E"
).pack()

tk.Label(
    header,
    text="From beekeeper to consumer — one verifiable journey",
    font=("Segoe UI", 9),
    bg=DARK,
    fg="#DDDDDD"
).pack(
    pady=(4, 0)
)


# ============================================================
# MAIN CONTENT
# ============================================================

content = tk.Frame(
    root,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=25
)


tk.Label(
    content,
    text="TRACEABILITY CONTROL PANEL",
    font=("Segoe UI", 15, "bold"),
    bg=BG,
    fg=DARK
).pack(
    pady=(0, 15)
)


# ============================================================
# FOUR MAIN CARDS
# ============================================================

cards_frame = tk.Frame(
    content,
    bg=BG
)

cards_frame.pack()


def create_card(
    parent,
    title,
    description,
    button_text,
    command
):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=390,
        height=125,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 14, "bold"),
        bg=CARD,
        fg=DARK
    ).pack(
        pady=(12, 2)
    )

    tk.Label(
        card,
        text=description,
        font=("Segoe UI", 9),
        bg=CARD,
        fg=MUTED
    ).pack()

    tk.Button(
        card,
        text=button_text,
        command=command,
        font=("Segoe UI", 9, "bold"),
        bg=HONEY,
        fg="white",
        activebackground="#B57C00",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=18
    ).pack(
        pady=8
    )

    return card


# Register

card1 = create_card(
    cards_frame,
    "🐝 Register Batch",
    "Create a new honey batch",
    "REGISTER BATCH",
    register_batch_window
)

card1.grid(
    row=0,
    column=0,
    padx=10,
    pady=8
)


# Update

card2 = create_card(
    cards_frame,
    "🔄 Update Batch",
    "Add the next supply-chain stage",
    "UPDATE BATCH",
    update_batch_window
)

card2.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# Verify

card3 = create_card(
    cards_frame,
    "✓ Verify Batch",
    "Check authenticity and history",
    "VERIFY BATCH",
    verify_batch_window
)

card3.grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)


# Track

card4 = create_card(
    cards_frame,
    "📦 Track Batch",
    "View the complete journey",
    "TRACK BATCH",
    track_batch_window
)

card4.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# SUPPLY CHAIN FLOW
# ============================================================

flow_frame = tk.Frame(
    content,
    bg=HONEY_LIGHT,
    highlightbackground=BORDER,
    highlightthickness=1
)

flow_frame.pack(
    fill="x",
    pady=(20, 0),
    ipady=10
)

tk.Label(
    flow_frame,
    text="SUPPLY CHAIN",
    font=("Segoe UI", 10, "bold"),
    bg=HONEY_LIGHT,
    fg=DARK
).pack(
    pady=(3, 5)
)

tk.Label(
    flow_frame,
    text="🐝 Harvest   →   Extraction   →   Processing   →   Packaging   →   Dispatch",
    font=("Segoe UI", 11, "bold"),
    bg=HONEY_LIGHT,
    fg=DARK
).pack()


# ============================================================
# BOTTOM TECHNICAL BUTTONS
# ============================================================

technical_buttons = tk.Frame(
    content,
    bg=BG
)

technical_buttons.pack(
    pady=(12, 0)
)


# Verify Blockchain

tk.Button(
    technical_buttons,
    text="🔗 VERIFY BLOCKCHAIN",
    command=verify_blockchain_window,
    font=("Segoe UI", 9, "bold"),
    bg=HONEY,
    fg="white",
    activebackground="#B57C00",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=22,
    height=1
).pack(
    side="left",
    padx=5
)


# Alter Blockchain

tk.Button(
    technical_buttons,
    text="🔧 ALTER BLOCKCHAIN",
    command=alter_blockchain_window,
    font=("Segoe UI", 9, "bold"),
    bg=RED,
    fg="white",
    activebackground="#8E0000",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=22,
    height=1
).pack(
    side="left",
    padx=5
)


# ============================================================
# FOOTER
# ============================================================

tk.Label(
    content,
    text="Blockchain-backed provenance • SQLite database • QR-enabled traceability",
    font=("Segoe UI", 8),
    bg=BG,
    fg=MUTED
).pack(
    pady=(10, 0)
)


# ============================================================
# START
# ============================================================

root.mainloop()
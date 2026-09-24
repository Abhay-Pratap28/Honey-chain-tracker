#For Gui interface

import tkinter as tk
from tkinter import messagebox
from honey_chain import honey_chain


# Register batch window
def register_batch_window():

    window = tk.Toplevel(root)
    window.title("Register New Honey Batch")
    window.geometry("500x450")

    tk.Label(
        window,
        text="REGISTER NEW BATCH",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Batch ID").pack()
    batch_id_entry = tk.Entry(window, width=35)
    batch_id_entry.pack(pady=5)

    tk.Label(window, text="Beekeeper / Farm Name").pack()
    beekeeper_entry = tk.Entry(window, width=35)
    beekeeper_entry.pack(pady=5)

    tk.Label(window, text="Harvest Location").pack()
    location_entry = tk.Entry(window, width=35)
    location_entry.pack(pady=5)

    tk.Label(window, text="Quantity").pack()
    quantity_entry = tk.Entry(window, width=35)
    quantity_entry.pack(pady=5)

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
                "This Batch already exists"
            )
            return

        honey_chain.register_batch(
            batch_id , beekeeper , location , quantity
        )

        messagebox.showinfo(
            "Success" ,
            f"Batch {batch_id} registered successfully"
        )

        window.destroy

    tk.Button(
        window,
        text="REGISTER BATCH",
        command=register,
        width=20
    ).pack(pady=25)


#Update batch window

def update_batch_window():

    window = tk.Toplevel(root)
    window.title("Update Honey Batch")
    window.geometry("550x500")

    tk.Label(
        window,
        text="UPDATE BATCH",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    # Batch ID
    tk.Label(window, text="Batch ID").pack()

    batch_id_entry = tk.Entry(window, width=35)
    batch_id_entry.pack(pady=5)

    # Stage
    tk.Label(window, text="Select Next Stage").pack(pady=(10, 5))

    stage_var = tk.StringVar()
    stage_var.set("extracted")

    stages = [
        "extracted",
        "processed",
        "packaged",
        "dispatched"
    ]

    stage_menu = tk.OptionMenu(
        window,
        stage_var,
        *stages
    )

    stage_menu.config(width=25)
    stage_menu.pack()

    # Location
    tk.Label(window, text="Location").pack(pady=(10, 5))

    location_entry = tk.Entry(window, width=35)
    location_entry.pack(pady=5)

    # Handler
    tk.Label(window, text="Handler / Unit Name").pack(pady=(10, 5))

    handler_entry = tk.Entry(window, width=35)
    handler_entry.pack(pady=5)

    # These frames will appear only when required
    quality_frame = tk.Frame(window)
    seal_frame = tk.Frame(window)

    # Quality
    quality_label = tk.Label(
        quality_frame,
        text="Quality / Test Status"
    )

    quality_entry = tk.Entry(
        quality_frame,
        width=35
    )

    # Seal ID
    seal_label = tk.Label(
        seal_frame,
        text="Seal ID"
    )

    seal_entry = tk.Entry(
        seal_frame,
        width=35
    )

    def change_stage(*args):

        # Remove optional fields first
        quality_frame.pack_forget()
        seal_frame.pack_forget()

        # Processed → show Quality/Test
        if stage_var.get() == "processed":

            quality_frame.pack(pady=10)

            quality_label.pack()
            quality_entry.pack(pady=5)

        # Packaged → show Seal ID
        elif stage_var.get() == "packaged":

            seal_frame.pack(pady=10)

            seal_label.pack()
            seal_entry.pack(pady=5)

    stage_var.trace_add("write", change_stage)

    def update():

        batch_id = batch_id_entry.get().strip()
        stage = stage_var.get().strip()
        location = location_entry.get().strip()
        handler = handler_entry.get().strip()

        quality = None
        seal_id = None

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

        if not batch_id:
            messagebox.showwarning(
                "Missing Batch ID",
                "Please enter Batch ID."
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
            "Success",
            f"Batch {batch_id} updated to {stage.upper()}.\n\n"
            "A new QR code has been generated."
        )

        window.destroy()

    # UPDATE BUTTON
    tk.Button(
        window,
        text="UPDATE BATCH",
        command=update,
        width=25,
        height=2
    ).pack(pady=20)


# Verify batch window
def verify_batch_window():

    window = tk.Toplevel(root)
    window.title("Verify Honey Batch")
    window.geometry("700x600")

    tk.Label(
        window,
        text="VERIFY BATCH",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    # Batch ID - visible from the beginning
    tk.Label(
        window,
        text="Enter Batch ID"
    ).pack()

    batch_id_entry = tk.Entry(
        window,
        width=35
    )
    batch_id_entry.pack(pady=5)

    # Verify button
    verify_button = tk.Button(
        window,
        text="VERIFY BATCH",
        width=25,
        height=2
    )
    verify_button.pack(pady=10)

    # Result box - CREATED but NOT SHOWN initially
    result_box = tk.Text(
        window,
        width=75,
        height=25
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

        # Show result box ONLY after valid Batch ID
        result_box.pack(pady=15)

        result_box.delete("1.0", tk.END)

        first_record = history[0].data

        result_box.insert(
            tk.END,
            "========== HONEY CHAIN ==========\n\n"
        )

        result_box.insert(
            tk.END,
            f"Batch ID     : {first_record['batch_id']}\n"
        )

        result_box.insert(
            tk.END,
            f"Beekeeper    : {first_record['beekeeper']}\n"
        )

        result_box.insert(
            tk.END,
            f"Quantity     : {first_record['quantity']}\n"
        )

        result_box.insert(
            tk.END,
            f"Harvest Site : {first_record['location']}\n\n"
        )

        result_box.insert(
            tk.END,
            "--------- JOURNEY ---------\n\n"
        )

        for block in history:

            data = block.data

            result_box.insert(
                tk.END,
                f"Stage     : {data.get('stage', '')}\n"
            )

            result_box.insert(
                tk.END,
                f"Location  : {data.get('location', '')}\n"
            )

            result_box.insert(
                tk.END,
                f"Handler   : {data.get('handler', '')}\n"
            )

            if data.get("quality"):
                result_box.insert(
                    tk.END,
                    f"Quality   : {data.get('quality')}\n"
                )

            if data.get("seal_id"):
                result_box.insert(
                    tk.END,
                    f"Seal ID   : {data.get('seal_id')}\n"
                )

            result_box.insert(
                tk.END,
                f"Time      : {block.timestamp}\n"
            )

            result_box.insert(
                tk.END,
                "----------------------------\n"
            )

        status = honey_chain.is_valid()

        result_box.insert(
            tk.END,
            "\nBLOCKCHAIN STATUS: "
        )

        if status:
            result_box.insert(
                tk.END,
                "VALID"
            )
        else:
            result_box.insert(
                tk.END,
                "TAMPERED"
            )

    # Connect button to verify function
    verify_button.config(command=verify)

#Track window
def track_batch_window():

    window = tk.Toplevel(root)
    window.title("Track Honey Batch")
    window.geometry("700x600")

    tk.Label(
        window,
        text="TRACK BATCH",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    # Batch ID
    tk.Label(
        window,
        text="Enter Batch ID"
    ).pack()

    batch_id_entry = tk.Entry(
        window,
        width=35
    )
    batch_id_entry.pack(pady=5)

    # Track button
    track_button = tk.Button(
        window,
        text="TRACK BATCH",
        width=25,
        height=2
    )
    track_button.pack(pady=10)

    # Result area - hidden initially
    result_box = tk.Text(
        window,
        width=75,
        height=25
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

        # Show results only after valid Batch ID
        result_box.pack(pady=15)

        result_box.delete("1.0", tk.END)

        first_record = history[0].data

        result_box.insert(
            tk.END,
            "========== BATCH JOURNEY ==========\n\n"
        )

        result_box.insert(
            tk.END,
            f"Batch ID     : {first_record['batch_id']}\n"
        )

        result_box.insert(
            tk.END,
            f"Beekeeper    : {first_record['beekeeper']}\n"
        )

        result_box.insert(
            tk.END,
            f"Quantity     : {first_record['quantity']}\n"
        )

        result_box.insert(
            tk.END,
            f"Harvest Site : {first_record['location']}\n\n"
        )

        result_box.insert(
            tk.END,
            "------------- JOURNEY -------------\n\n"
        )

        for block in history:

            data = block.data

            result_box.insert(
                tk.END,
                f"Stage    : {data.get('stage', 'Harvested')}\n"
            )

            result_box.insert(
                tk.END,
                f"Location : {data.get('location', '')}\n"
            )

            result_box.insert(
                tk.END,
                f"Handler  : {data.get('handler', '')}\n"
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
                "\n-----------------------------------\n\n"
            )

    track_button.config(command=track)



# MAIN WINDOW----


root = tk.Tk()

root.title("Honey Chain - Traceability System")
root.geometry("900x600")

title = tk.Label(
    root , text="🍯 HONEY CHAIN", font=("Arial", 28, "bold")
)

title.pack(pady = 30)

subtitle = tk.Label(
    root, text="Digital Honey Traceability System", font=("Arial", 16)
)

subtitle.pack(pady = 20)

# Register button

register_button = tk.Button(
    root,
    text="REGISTER BATCH",
    command=register_batch_window,
    width=25,
    height=2
)

register_button.pack(pady=25)


# Update button

update_button = tk.Button(
    root,
    text="UPDATE BATCH",
    command=update_batch_window,
    width=25,
    height=2
)

update_button.pack(pady=10)

# Verify button

verify_button = tk.Button(
    root,
    text="VERIFY BATCH",
    command=verify_batch_window,
    width=25,
    height=2
)

verify_button.pack(pady=10)

# Track button

track_button = tk.Button(
    root,
    text="TRACK BATCH",
    command=track_batch_window,
    width=25,
    height=2
)

track_button.pack(pady=10)



root.mainloop()
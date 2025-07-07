import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DATA_FILE = "tickets.json"

# Load tickets from JSON file
def load_tickets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save tickets to JSON file
def save_tickets(tickets):
    with open(DATA_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

# Initialize ticket list and next ID
tickets = load_tickets()
next_id = max([t["id"] for t in tickets], default=0) + 1

st.title("🎫 Ticketing System")

# Sidebar filters
st.sidebar.header("🔍 Filter Tickets")
show_resolved = st.sidebar.checkbox("Show Resolved", value=True)
category_filter = st.sidebar.text_input("Category")
search_term = st.sidebar.text_input("Search Title or Description")
sort_by_due = st.sidebar.checkbox("Sort by Due Date")

# Create ticket form
st.subheader("➕ Create New Ticket")
with st.form("create_ticket"):
    title = st.text_input("Title")
    category = st.text_input("Category")
    due_date = st.date_input("Due Date")
    description = st.text_area("Description")
    submitted = st.form_submit_button("Create Ticket")
    if submitted and title:
        new_ticket = {
            "id": next_id,
            "title": title,
            "category": category,
            "due_date": due_date.isoformat(),
            "description": description,
            "status": "open"
        }
        tickets.append(new_ticket)
        save_tickets(tickets)
        st.success("Ticket created!")
        st.experimental_rerun()

# Convert to DataFrame for editing
df = pd.DataFrame(tickets)

# Apply filters
if not show_resolved:
    df = df[df["status"] == "open"]
if category_filter:
    df = df[df["category"].str.contains(category_filter, case=False, na=False)]
if search_term:
    df = df[
        df["title"].str.contains(search_term, case=False, na=False)
        | df["description"].str.contains(search_term, case=False, na=False)
    ]
if sort_by_due and "due_date" in df.columns:
    df["due_date"] = pd.to_datetime(df["due_date"], errors="coerce")
    df = df.sort_values("due_date")

# Editable table
st.subheader("✏️ Edit Tickets")
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    key="editor"
)

# Save edits
if st.button("💾 Save Changes"):
    updated_tickets = edited_df.to_dict(orient="records")
    save_tickets(updated_tickets)
    st.success("Changes saved!")
    st.experimental_rerun()

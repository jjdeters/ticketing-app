import streamlit as st
import json
import os
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

# App title
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
    description = st.text_area("Description")  # New field
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

# Apply filters
filtered = [
    t for t in tickets
    if (show_resolved or t["status"] == "open")
    and (category_filter.lower() in t["category"].lower())
    and (
        search_term.lower() in t["title"].lower()
        or search_term.lower() in t.get("description", "").lower()
    )
]

if sort_by_due:
    filtered.sort(key=lambda x: x["due_date"])

# Display tickets
st.subheader("📋 Tickets")
for t in filtered:
    with st.expander(f'#{t["id"]}: {t["title"]}'):
        st.write(f'**Category:** {t["category"]}')
        st.write(f'**Due Date:** {t["due_date"]}')
        st.write(f'**Status:** {t["status"].capitalize()}')
        st.write(f'**Description:** {t.get("description", "(no description)")}')
        if st.button(f'Toggle Status (#{t["id"]})'):
            t["status"] = "resolved" if t["status"] == "open" else "open"
            save_tickets(tickets)
            st.experimental_rerun()

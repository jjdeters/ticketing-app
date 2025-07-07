import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "tickets.json"

# Load tickets
def load_tickets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save tickets
def save_tickets(tickets):
    with open(DATA_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

# Initialize
tickets = load_tickets()
next_id = max([t["id"] for t in tickets], default=0) + 1

st.title("🎫 Ticketing System")

# Sidebar filters
st.sidebar.header("🔍 Filter Tickets")
show_resolved = st.sidebar.checkbox("Show Resolved", value=True)
category_filter = st.sidebar.text_input("Category")
search_term = st.sidebar.text_input("Search Title")
sort_by_due = st.sidebar.checkbox("Sort by Due Date")

# Ticket creation
st.subheader("➕ Create New Ticket")
with st.form("create_ticket"):
    title = st.text_input("Title")
    category = st.text_input("Category")
    due_date = st.date_input("Due Date")
    submitted = st.form_submit_button("Create Ticket")
    if submitted and title:
        new_ticket = {
            "id": next_id,
            "title": title,
            "category": category,
            "due_date": due_date.isoformat(),
            "status": "open"
        }
        tickets.append(new_ticket)
        save_tickets(tickets)
        st.success("Ticket created!")
        st.experimental_rerun()

# Filter and sort
filtered = [
    t for t in tickets
    if (show_resolved or t["status"] == "open")
    and (category_filter.lower() in t["category"].lower())
    and (search_term.lower() in t["title"].lower())
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
        if st.button(f'Toggle Status (#{t["id"]})'):
            t["status"] = "resolved" if t["status"] == "open" else "open"
            save_tickets(tickets)
            st.experimental_rerun()

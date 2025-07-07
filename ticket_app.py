import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

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

# Initialize
tickets = load_tickets()
next_id = max([t["id"] for t in tickets], default=0) + 1

st.title("🎫 Ticketing System")

# Sidebar filters
st.sidebar.header("🔍 Filter Tickets")
show_resolved = st.sidebar.checkbox("Show Resolved", value=True)
category_filter = st.sidebar.text_input("Category")
search_term = st.sidebar.text_input("Search Title or Description")
sort_by_due = st.sidebar.checkbox("Sort by Due Date")

# Filtered ticket list
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

# Select ticket to edit
ticket_titles = [f'#{t["id"]}: {t["title"]}' for t in filtered]
selected_label = st.selectbox("✏️ Select a ticket to edit (or leave blank to create new)", [""] + ticket_titles)
selected_ticket = None
if selected_label:
    selected_id = int(selected_label.split(":")[0][1:])
    selected_ticket = next((t for t in tickets if t["id"] == selected_id), None)

# Ticket form (Create or Edit)
st.subheader("📝 " + ("Edit Ticket" if selected_ticket else "Create New Ticket"))
with st.form("ticket_form"):
    title = st.text_input("Title", value=selected_ticket["title"] if selected_ticket else "")
    category = st.text_input("Category", value=selected_ticket["category"] if selected_ticket else "")
    due_date = st.date_input("Due Date", value=datetime.fromisoformat(selected_ticket["due_date"]) if selected_ticket else datetime.today())
    description = st.text_area("Description", value=selected_ticket.get("description", "") if selected_ticket else "")
    status = st.selectbox("Status", ["open", "resolved"], index=0 if not selected_ticket or selected_ticket["status"] == "open" else 1)
    submitted = st.form_submit_button("Save Ticket")

    if submitted and title:
        if selected_ticket:
            # Update existing ticket
            selected_ticket["title"] = title
            selected_ticket["category"] = category
            selected_ticket["due_date"] = due_date.isoformat()
            selected_ticket["description"] = description
            selected_ticket["status"] = status
            st.success("Ticket updated!")
        else:
            # Create new ticket
            new_ticket = {
                "id": next_id,
                "title": title,
                "category": category,
                "due_date": due_date.isoformat(),
                "description": description,
                "status": status
            }
            tickets.append(new_ticket)
            st.success("Ticket created!")
        save_tickets(tickets)
        st.experimental_rerun()

# Display tickets
st.subheader("📋 Tickets")
for t in filtered:
    with st.expander(f'#{t["id"]}: {t["title"]}'):
        st.write(f'**Category:** {t["category"]}')
        st.write(f'**Due Date:** {t["due_date"]}')
        st.write(f'**Status:** {t["status"].capitalize()}')
        st.write(f'**Description:** {t.get("description", "(no description)")}')

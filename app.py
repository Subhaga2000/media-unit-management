import streamlit as st
from supabase import create_client
from datetime import date

# ------------------------------
# Connect to Supabase
# ------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Media Unit Management System")

# ------------------------------
# Fetch members from Supabase
# ------------------------------
members = supabase.table("members").select("*").execute().data or []

st.subheader("Current Members")
if members:
    for m in members:
        st.write(f"Name: {m['name']} | Role: {m['role']} | Status: {m['status']}")
else:
    st.write("No members yet!")

# ------------------------------
# Add New Member Form
# ------------------------------
st.header("Add New Member")
with st.form("add_member_form"):
    name = st.text_input("Member Name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["photographer", "editor", "both"])
    submitted_member = st.form_submit_button("Add Member")
    
    if submitted_member:
        res = supabase.table("members").insert({
            "name": name,
            "email": email,
            "role": role,
            "status": "free"
        }).execute()
        
        if res.data is None:
            st.error("Error adding member. Check your table setup.")
        else:
            st.success(f"Member {name} added successfully!")
            members = supabase.table("members").select("*").execute().data or []

# ------------------------------
# Create New Event Form
# ------------------------------
st.header("Create New Event")
with st.form("add_event_form"):
    event_name = st.text_input("Event Name")
    event_date = st.date_input("Event Date", min_value=date.today())
    
    available_members = [m for m in members if m["status"] == "free"]
    selected_members = st.multiselect(
        "Assign 2 Members",
        options=[f"{m['name']} ({m['role']})" for m in available_members],
        max_selections=2
    )
    
    submitted_event = st.form_submit_button("Create Event")
    
    if submitted_event:
        if len(selected_members) != 2:
            st.error("Please select exactly 2 members for this event.")
        else:
            # Get the correct UUIDs (strings)
            member_ids = [
                str(m["id"]) for m in available_members
                if f"{m['name']} ({m['role']})" in selected_members
            ]
            
            # Insert event with proper UUIDs
            res_event = supabase.table("events").insert({
                "event_name": event_name,
                "date": str(event_date),
                "assigned_members": member_ids,  # <-- list of strings
                "status": "pending"
            }).execute()
            
            if res_event.data is None:
                st.error("Error creating event. Check your table columns.")
            else:
                # Set members to busy
                for m_id in member_ids:
                    supabase.table("members").update({"status": "busy"}).eq("id", m_id).execute()
                st.success(f"Event '{event_name}' created with members: {', '.join(selected_members)}")

# ------------------------------
# Running Events
# ------------------------------
st.header("Running Events")
events = supabase.table("events").select("*").execute().data or []

if events:
    for e in events:
        event_name_display = e.get("event_name") or "Unnamed Event"
        # Make sure assigned_members is a list
        member_ids = e.get("assigned_members") or []
        if isinstance(member_ids, str):
            # Convert stringified list to Python list
            import ast
            member_ids = ast.literal_eval(member_ids)

        member_names = []
        for m_id in member_ids:
            m_id_str = str(m_id)  # ensure it's a string
            m_data = supabase.table("members").select("name").eq("id", m_id_str).execute().data or []
            if m_data:
                member_names.append(m_data[0]["name"])
        
        st.write(
            f"Event: {event_name_display} | "
            f"Date: {e.get('date', 'N/A')} | "
            f"Members: {', '.join(member_names) if member_names else 'None'} | "
            f"Status: {e.get('status', 'N/A')}"
        )

        # Button to mark event as done
        if e.get("status") != "done":
            if st.button(f"Mark '{event_name_display}' as done"):
                # Update event status
                supabase.table("events").update({"status": "done"}).eq("id", e["id"]).execute()
                # Free members
                for m_id in member_ids:
                    supabase.table("members").update({"status": "free"}).eq("id", str(m_id)).execute()
                st.success(f"Event '{event_name_display}' completed. Members are now free.")

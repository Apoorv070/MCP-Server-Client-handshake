import sys
import uuid
from mcp.server.fastmcp import FastMCP


# 1. Initialize the Server
# This name "Hotel Reservation System" is what shows up in logs
mcp = FastMCP("Hotel Reservation System", host="localhost", port=8000)

#  2. Define the Tool
# The @mcp.tool() decorator automatically adds this to the "Menu"
@mcp.tool()
def book_hotel_room(hotel_name: str, location: str, date: str) -> str:
    """
    Books a reservation at a specific hotel.

    Args:
        hotel_name: The name of the hotel (e.g. "Taj Mahal Palace")
        location: The city or location (e.g. "Mumbai")
        date: The check-in date in YYYY-MM-DD format.

    Returns:
        A confirmation string with a reservation ID.
    """
    
    # --- LOGGING (For your visibility) ---
    # We print to stderr because stdout is used for the MCP protocol itself.
    print(f"LOG: Received booking request for {hotel_name} in {location} on {date}", file=sys.stderr)

    # --- MOCK LOGIC ---
    # In a real app, this is where you'd call the Amadeus/Booking.com API.
    reservation_id = str(uuid.uuid4())[:8].upper()
    
    status = "CONFIRMED"
    
    # Return the result to the Agent
    return (
        f"SUCCESS: Hotel '{hotel_name}' in {location} has been booked for {date}. "
        f"Reservation ID: {reservation_id}. Status: {status}"
    )


# 3. Run the Server
# ... (Keep all your tool definitions same as before) ...

if __name__ == "__main__":
    # Default to SSE so running `python mcp_hotel_server.py` from a terminal
    # does not try to parse blank stdin as MCP JSON-RPC messages.
    if len(sys.argv) > 1 and sys.argv[1] == "stdio":
        mcp.run()
    else:
        mcp.run(transport="sse")

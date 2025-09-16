import pandas as pd
import sys
from .config import OD_BASE, OBSERVER_WARD_DURATION
from .opendota_api import get_json

def collect_wards_from_match(match_id: int, team_id: int = None):
    """
    Collects observer ward data from a specific match via the OpenDota API.
    
    If a team_id is provided, it only collects data if that team played
    on the Radiant side.
    """
    match_url = f"{OD_BASE}/matches/{match_id}"
    match_data = get_json(match_url)

    if not match_data:
        print(f"Could not fetch data for match {match_id}.", file=sys.stderr)
        return pd.DataFrame(), "Unknown Team"

    team_name = "All Teams"
    # If a team_id is specified, ensure they were the Radiant team
    if team_id:
        radiant_team_info = match_data.get("radiant_team", {})
        if radiant_team_info.get("team_id") != team_id:
            print(f"Team {team_id} was not Radiant in match {match_id}. No data processed.", file=sys.stderr)
            return pd.DataFrame(), radiant_team_info.get("name", f"Team ID: {team_id}")
        team_name = radiant_team_info.get("name", f"Team ID: {team_id}")

    ward_events = []
    for player in match_data.get("players", []):
        # Process only Radiant players
        if not player.get("isRadiant"):
            continue

        # Extract observer ward logs
        for ward in player.get("obs_log", []):
            x_raw, y_raw = ward.get("x"), ward.get("y")
            if x_raw is None or y_raw is None:
                continue
            
            placement_time = ward.get("time")
            
            # Coordinate transformation: shift origin and flip Y-axis
            x_coord = x_raw - 64.0
            y_coord = 128.0 - (y_raw - 64.0)

            ward_events.append({
                "time_seconds": placement_time,
                "expiration_time": placement_time + OBSERVER_WARD_DURATION,
                "x": x_coord,
                "y": y_coord,
                "type": "observer"
            })

    if not ward_events:
        return pd.DataFrame(), team_name

    df = pd.DataFrame(ward_events)
    # Clip coordinates to ensure they are within the 0-128 map bounds
    if not df.empty:
        df["x"] = df["x"].clip(0, 127.999)
        df["y"] = df["y"].clip(0, 127.999)
    return df, team_name

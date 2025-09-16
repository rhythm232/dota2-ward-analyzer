# Dota 2 Ward Analyzer

This project is a Python-based tool to fetch and visualize observer ward placements from Dota 2 matches.

## Features
- Fetches observer ward data for a specific match from the OpenDota API.
- Generates a self-contained, interactive HTML file to display wards on the map.
- Allows filtering by team ID.
- Includes a time slider to see ward placements over the course of the game.

## How to Run
1.  Ensure you have Python and the required packages (`requests`, `pandas`) installed.
2.  Run the script from your terminal:
    ```sh
    python generate_report.py <match_id> --team_id <optional_team_id>
    ```
3.  An HTML file named `ward_map_<match_id>.html` will be generated in the `dota2ward` directory.

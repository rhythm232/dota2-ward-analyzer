import argparse
import sys
from src.data_processing import collect_wards_from_match
from src.html_generator import generate_html

def main():
    """
    Main function to parse command-line arguments, fetch data,
    and generate an HTML report.
    """
    parser = argparse.ArgumentParser(
        description="Fetch observer ward data from OpenDota and generate an HTML visualization."
    )
    parser.add_argument("match_id", type=int, help="The match ID to query.")
    parser.add_argument("--team_id", type=int, help="(Optional) The team ID to filter for.", required=False)
    args = parser.parse_args()

    print(f"Fetching ward data for match {args.match_id}...", file=sys.stderr)
    if args.team_id:
        print(f"Filtering for team: {args.team_id} (Radiant only)", file=sys.stderr)

    wards_df, team_name = collect_wards_from_match(args.match_id, args.team_id)

    if wards_df.empty:
        print("No qualifying ward data found.", file=sys.stderr)
        return

    output_html = generate_html(args.match_id, team_name, wards_df)
    
    # Save the generated HTML to a file
    team_suffix = f"_{args.team_id}" if args.team_id else ""
    output_filename = f"ward_map_{args.match_id}{team_suffix}.html"
    output_path = f"e:\\DOTAdata\\dota2ward\\{output_filename}"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"\nSuccessfully processed {len(wards_df)} observer wards.", file=sys.stderr)
    print(f"Visualization map generated: {output_path}", file=sys.stderr)

if __name__ == "__main__":
    main()

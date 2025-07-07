"""
Created on Mon Jul 07 13:50:45 2025

CLI version to run Social Interaction Analysis
####

@author: @madmaxpython
"""
import argparse
from sit_analysis.analyzer import Experience

def main():
    parser = argparse.ArgumentParser(description="Run SIT analysis")
    parser.add_argument("--project_path", required=True)
    parser.add_argument("--conditions_path", required=True)
    parser.add_argument("--arena_path", required=True)
    parser.add_argument("--siz_path", required=True)
    parser.add_argument("--fps", type=float, default=30)
    parser.add_argument("--px_size", type=float, default=1.0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    analyzer = Experience(
        project_path=args.project_path,
        conditions_path=args.conditions_path,
        arena_path=args.arena_path,
        SIZ_path=args.siz_path,
        fps=args.fps,
        PX_SIZE=args.px_size,
    )

    results_df = analyzer.run_all()
    results_df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"Saved results to {args.output}")

if __name__ == "__main__":
    main()

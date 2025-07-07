import os

from sit_analysis.analyzer import Experience


def main(PROJECT_PATH : str,
         CONDITIONS_PATH : str,
         ARENA_PATH : str,
         SIZ_PATH : str,
         FPS: float,
         PX_SIZE: float,
         output_path: str,
         save_output : bool = True):

    analyzer = Experience(PROJECT_PATH, CONDITIONS_PATH, ARENA_PATH, SIZ_PATH, FPS, PX_SIZE)

    results_df = analyzer.run_all()

    if save_output:
        results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return results_df

if __name__ == "__main__":
    BASE_PATH = "/Users/max/Desktop/THESE/PROJECTS/jose_data/Shama_replication/"
    PROJECT_PATH = os.path.join(BASE_PATH, "CSDS_DeepOF")
    ARENA_PATH = os.path.join(BASE_PATH, "Data/arena_params_bodygraph14.txt")
    SIZ_PATH = os.path.join(BASE_PATH, "Data/SIZ_params.txt")
    CONDITIONS_PATH = os.path.join(BASE_PATH, "Data/test_conditions.csv")
    FPS = 30
    pixel_size = 1.2

    results = main(PROJECT_PATH=PROJECT_PATH,
                   CONDITIONS_PATH=CONDITIONS_PATH,
                   ARENA_PATH=ARENA_PATH,
                   SIZ_PATH=SIZ_PATH,
                   FPS=FPS,
                   PX_SIZE=pixel_size,
                   output_path=str(os.path.join(PROJECT_PATH,"final_summary_no_ke.csv")),
                   save_output=True
                   )





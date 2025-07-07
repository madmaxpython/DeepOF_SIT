from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import pandas as pd
import matplotlib.path as mpath
from data_loader import read_tuples_file, load_deepof_project, match_params_to_videos

class SITAnalyzer:
    """
    Analyze Social Interaction Test (SIT) behavior from tracking data.

    Parameters
    ----------
    arena_coords : list of tuple of float
        Coordinates of the arena corners in the following order:
        [top-left, bottom-left, bottom-right, top-right].
    siz_coords : list of tuple of float
        Coordinates of the Social Interaction Zone (SIZ) in the same order.
    fps : float, optional
        Video frame rate in frames per second. Default is 30.
    """

    def __init__(
        self,
        arena_coords: List[Tuple[float, float]],
        siz_coords: List[Tuple[float, float]],
        fps: float = 30) -> None:

        self.FPS: float = fps

        # Arena corners
        self.top_left_arena, self.bottom_left_arena, self.bottom_right_arena, self.top_right_arena = arena_coords

        # SIZ corners
        self.top_left_SIZ, self.bottom_left_SIZ, self.bottom_right_SIZ, self.top_right_SIZ = siz_coords

        # Define SIZ polygon for point-in-polygon tests
        self.siz_vertices: np.ndarray = np.array([
            self.bottom_left_SIZ,
            self.bottom_right_SIZ,
            self.top_right_SIZ,
            self.top_left_SIZ
        ])
        self.siz_path: mpath.Path = mpath.Path(self.siz_vertices)

        # Define point of interest (POI): top-center of the arena
        self.POI: np.ndarray = np.mean([self.top_left_arena, self.top_right_arena], axis=0)

    def distance_to_poi(self,
        body_part: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        Compute absolute and normalized distance of a body part to the POI.

        Parameters
        ----------
        body_part : pd.DataFrame
            DataFrame of shape (n_frames, 2) with [x, y] coordinates.

        Returns
        -------
        tuple of pd.Series
            Absolute and normalized distance to the POI for each frame.
        """
        if body_part.shape[1] != 2:
            raise ValueError("body_part DataFrame must have two columns: x and y.")

        max_dist: float = np.linalg.norm(self.POI - np.array(self.bottom_left_arena))
        distances: np.ndarray = np.linalg.norm(body_part.values - self.POI, axis=1)
        normalized: np.ndarray = distances / max_dist

        return (
            pd.Series(distances, index=body_part.index),
            pd.Series(normalized, index=body_part.index)
        )

    def total_distance_traveled(
        self,
        body_part: pd.DataFrame,
        px_size: float) -> float:
        """
        Calculate the total distance traveled by a body part.

        Parameters
        ----------
        body_part : pd.DataFrame
            DataFrame of shape (n_frames, 2) with [x, y] coordinates.
        px_size : float
            Physical size of one pixel.

        Returns
        -------
        float
            Total distance traveled in physical units.
        """
        if body_part.shape[1] != 2:
            raise ValueError("body_part DataFrame must have two columns: x and y.")

        diffs: np.ndarray = np.diff(body_part.values, axis=0)
        dists: np.ndarray = np.linalg.norm(diffs * px_size, axis=1)

        return float(np.sum(dists))

    def time_in_SIZ(
        self,
        body_part: pd.DataFrame) -> float:
        """
        Calculate the total time spent in the Social Interaction Zone (SIZ).

        Parameters
        ----------
        body_part : pd.DataFrame
            DataFrame of shape (n_frames, 2) with [x, y] coordinates.

        Returns
        -------
        float
            Time in seconds spent within the SIZ.
        """
        if body_part.shape[1] != 2:
            raise ValueError("body_part DataFrame must have two columns: x and y.")

        points: np.ndarray = body_part.values
        in_zone: np.ndarray = self.siz_path.contains_points(points)

        return float(np.sum(in_zone)) / self.FPS




class Experience:
    """
    Manage and analyze a DeepOF experiment with arena and SIZ definitions.

    Parameters
    ----------
    project_path : str
        Path to the DeepOF project directory.
    conditions_path : str
        Path to the experiment conditions file.
    arena_path : str
        Path to a file defining arena corner coordinates.
    SIZ_path : str
        Path to a file defining SIZ corner coordinates.
    fps : float, optional
        Video frame rate in frames per second. Default is 30.
    PX_SIZE : float, optional
        Physical size of one pixel. Default is 0.1.
    """

    def __init__(
        self,
        project_path: str,
        conditions_path: str,
        arena_path: str,
        SIZ_path: str,
        fps: float = 30,
        PX_SIZE: float = 0.1) -> None:

        self.project: Any = load_deepof_project(project_path, conditions_path)
        self.arena_params: Any = read_tuples_file(arena_path)
        self.siz_params: Any = read_tuples_file(SIZ_path, single_object=True)

        self.pixel_size: float = PX_SIZE
        self.fps: float = fps

        # Map each video name to its arena and SIZ coordinates
        self.arena_map, self.siz_map = match_params_to_videos(
            self.project._videos, self.arena_params, self.siz_params
        )

    @staticmethod
    def _interpolate(df: pd.DataFrame) -> pd.DataFrame:
        """
        Linearly interpolate missing values if any.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame possibly containing NaNs.

        Returns
        -------
        pd.DataFrame
            Interpolated DataFrame (or original if no NaNs).
        """
        return df.interpolate() if df.isnull().any().any() else df

    @staticmethod
    def results_to_df(results_dict: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert a nested results dict into a clean DataFrame with SIR metrics.

        Parameters
        ----------
        results_dict : dict
            Mapping Animal_ID → metrics dict for each session.

        Returns
        -------
        pd.DataFrame
            DataFrame indexed by Animal_ID, with SIZ and distance ratios added.
        """
        df = pd.DataFrame.from_dict(results_dict, orient="index")

        # Compute Social Interaction Ratios (SIR)
        df["Time_SIR_typeA"] = (
            df["Time_in_SIZ_Session2"] / df["Time_in_SIZ_Session1"]
        )
        df["Time_SIR_typeB"] = (
            df["Time_in_SIZ_Session2"] /
            (df["Time_in_SIZ_Session1"] + df["Time_in_SIZ_Session2"])
        )
        df["Distance_SIR_typeA"] = (
            df["Normalized_distance_to_POI_Session2"] /
            df["Normalized_distance_to_POI_Session1"]
        )
        df["Distance_SIR_typeB"] = (
            df["Normalized_distance_to_POI_Session2"] /
            (df["Normalized_distance_to_POI_Session1"] +
             df["Normalized_distance_to_POI_Session2"])
        )

        # Reorder columns for readability
        df = df.reindex(columns=[
            "Animal_ID",
            "Time_in_SIZ_Session1", "Time_in_SIZ_Session2",
            "Normalized_distance_to_POI_Session1", "Normalized_distance_to_POI_Session2",
            "Total_Distance_Traveled_Session1", "Total_Distance_Traveled_Session2",
            "Time_SIR_typeA", "Time_SIR_typeB",
            "Distance_SIR_typeA", "Distance_SIR_typeB",
        ])

        # Ensure numeric types where possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="ignore")

        return df

    def analyze_animal(self, animal_name: str) -> Optional[Dict[str, Any]]:
        """
        Compute metrics for one animal-video pairing.

        Parameters
        ----------
        animal_name : str
            Video filename or key in project tables.

        Returns
        -------
        dict or None
            Metrics dict for this animal, or None if missing arena/SIZ.
        """
        base_name, session = animal_name.split("_SIT")[0], animal_name.split(".")[-1]

        if animal_name not in self.arena_map or animal_name not in self.siz_map:
            return None

        arena_coords = self.arena_map[animal_name]
        siz_coords = self.siz_map[animal_name]
        sit = SITAnalyzer(arena_coords=arena_coords, siz_coords=siz_coords)

        center = self._interpolate(
            self.project._tables[animal_name][[("Center", "x"), ("Center", "y")]]
        )
        nose = self._interpolate(
            self.project._tables[animal_name][[("Nose", "x"), ("Nose", "y")]]
        )

        time_in_siz = sit.time_in_SIZ(center)
        dist_to_poi, norm_dist_to_poi = sit.distance_to_poi(nose)
        total_dist = sit.total_distance_traveled(center, self.pixel_size)

        return {
            "Animal_ID": base_name,
            f"Time_in_SIZ_Session{session}": time_in_siz,
            f"Normalized_distance_to_POI_Session{session}": norm_dist_to_poi.mean(),
            f"Distance_to_POI_Session{session}": dist_to_poi.mean(),
            f"Total_Distance_Traveled_Session{session}": total_dist,
        }

    def run_all(self) -> pd.DataFrame:
        """
        Analyze all animals in the project and compile results.

        Returns
        -------
        pd.DataFrame
            Combined results for all animals, with SIR ratios appended.
        """
        results: Dict[str, Dict[str, Any]] = {}

        for animal in self.project.get_exp_conditions:
            data = self.analyze_animal(animal)
            if data is None:
                continue

            key = data["Animal_ID"]
            if key not in results:
                results[key] = {"Animal_ID": key}
            else:
                print(f"{key} already analyzed, updating metrics")

            # Merge new session metrics
            results[key].update({
                k: v for k, v in data.items() if k != "Animal_ID"
            })

        return self.results_to_df(results)
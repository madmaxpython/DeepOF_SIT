import ast
import deepof.data



def read_tuples_file(path: str,
                     single_object: bool=False):
    with open(path, 'r') as f:
        content = f.read()
        return ast.literal_eval(content) if single_object else [
            ast.literal_eval(line.strip()) for line in content.strip().split('\n') if line.strip()
        ]

def load_deepof_project(project_path: str,
                        conditions_path: str):
    project = deepof.data.load_project(project_path)
    if conditions_path:
        project.load_exp_conditions(conditions_path)
        for animal in project._exp_conditions:
            project._exp_conditions[animal] = project._exp_conditions[animal].astype({
                'CSDS': 'category',
                'Cohort': 'category',
                'SIT_session': 'category'
            })
    return project

def match_params_to_videos(videos,
                           arena_params,
                           siz_params):
    cleaned_names = ['_'.join(x.split('DLC')[:1]) for x in videos]
    return dict(zip(cleaned_names, arena_params)), dict(zip(cleaned_names, siz_params))
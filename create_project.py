from __future__ import division
from __future__ import print_function
from typing import List, Any
from absl import flags
from absl import app
from absl import logging

import os
import shutil

FLAGS = flags.FLAGS
flags.DEFINE_string('mlp_project', None, 'The name of the project. Will be the root directory of the project.')
flags.DEFINE_string('mlp_subproject', None, 'The name of the subproject. Will be a sub directory inside the project directory.')
flags.DEFINE_string('gcp_project', None, 'The name of the GCP project. Any GCP services will be used with the account corresponding to this project.')
flags.DEFINE_string('gcp_bucket', None, 'The name of the GCP bucket to store the files generated by running a pipeline.')

flags.DEFINE_string('dir', './', 'The directory to place the example project.')
flags.mark_flag_as_required('mlp_project')
flags.mark_flag_as_required('mlp_subproject')
flags.mark_flag_as_required('gcp_project')
flags.mark_flag_as_required('gcp_bucket')


def replace_strings_in_dir(dir, string_map):
  for dir_name, dirs, files in os.walk(dir):
    for file_name in files:
      file_path = os.path.join(dir_name, file_name)

      with open(file_path) as f:
        text = f.read()

      for old_string in string_map:
        text = text.replace(old_string, string_map[old_string])

      with open(file_path, "w") as f:
        f.write(text)


def main(argv: List[Any]):
  os.path.makedirs(FLAGS.dir, exist_ok=True)

  string_map = {
    'gcp_project': FLAGS.gcp_project,
    'example_project': FLAGS.example_project,
    'example_subproject': FLAGS.example_subproject
  }

  example_project_dir = os.path.join(os.path.dirname(__file__), 'example_project')
  example_subproject_dir = os.path.join(os.path.dirname(__file__), 'example_project', 'example_subproject_dir')

  subproject_dir = os.path.join(FLAGS.dir, FLAGS.mlp_project, FLAGS.mlp_subproject)

  project_dir = os.path.join(FLAGS.dir, FLAGS.mlp_project)
  subproject_dir = os.path.join(FLAGS.dir, FLAGS.mlp_project, FLAGS.mlp_subproject)

  if os.path.exists(project_dir):
    logging.info('{} already exists. Will not alter any files outside of {}'.format(project_dir, subproject_dir))

    if os.path.exists(subproject_dir):
      logging.info('{} already exists. Nothing to be done. Exiting'.format(subproject_dir))
      return

    shutil.copytree(example_subproject_dir, subproject_dir)
    replace_strings_in_dir(subproject_dir, string_map)
  else:
    shutil.copytree(example_project_dir, project_dir)
    replace_strings_in_dir(project_dir, string_map)

if __name__ == "__main__":
  app.run(main)

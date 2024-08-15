# Copyright 2024 R. Kent James <kent@caspia.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from catkin_pkg.package import Url
import rosdistro

logger = logging.getLogger('rosdoc2')


def package_repo_url(package):
    """Add a package url from rosdistro if missing."""
    for url in package.urls:
        if url.type == 'repository':
            return

    # Only include repo url if ROS_DISTRO is known
    distro = os.environ.get('ROS_DISTRO')
    if not distro:
        return
    try:
        index = rosdistro.get_index(rosdistro.get_index_url())
        dist_file = rosdistro.get_distribution_file(index, distro)
        rosdistro_package = dist_file.release_packages[package.name]
        repo_name = rosdistro_package.repository_name
        repo = dist_file.repositories[repo_name]
        if repo.source_repository and repo.source_repository.url:
            url = repo.source_repository.url
            logger.info(f'Adding package repository url from rosdisto: {url}')
            package.urls.append(Url(url, 'repository'))
    except (KeyError, RuntimeError):
        logger.info('No package repo url found from rosdistro')

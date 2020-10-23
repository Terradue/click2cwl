FROM centos:7


MAINTAINER Terradue S.r.l
USER root

## yum
ADD install-yum.bash /tmp/install-yum.bash
ADD yum.list /tmp/yum.list
RUN set -x && chmod 755 /tmp/install-yum.bash && /tmp/install-yum.bash

ENV NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100 \
    SHELL=bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    CONDA_DIR=/opt/anaconda \
    NB_PYTHON_PREFIX=/opt/anaconda/envs/env_vi
    
ENV USER=${NB_USER} \
    NB_UID=${NB_UID} \
    HOME=/home/${NB_USER} 

ADD fix-permissions /usr/local/bin/fix-permissions

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    chmod g+w /etc/passwd /etc/group && \
    fix-permissions $HOME

# conda installation via miniforge
ADD install-miniforge.bash /tmp/install-miniforge.bash

ADD environment.yml /tmp/environment.yml

RUN chmod 755 /tmp/install-miniforge.bash && /tmp/install-miniforge.bash

ENV PATH=$NB_PYTHON_PREFIX/bin:$CONDA_DIR/bin:$PATH

# clean-up
RUN rm -f /tmp/install-*.bash && rm -f /tmp/environment.yml 

# fix permissions
RUN chown -R $NB_USER:$NB_GID ${HOME} 

USER ${NB_USER}

# setup conda activate/deactivate
#RUN ${CONDA_DIR}/bin/conda init bash && source ${HOME}/.bashrc && ${CONDA_DIR}/bin/conda activate env_default

# workdir for binder
COPY --chown=jovyan:100 . ${HOME}

RUN cd ${HOME} && ${NB_PYTHON_PREFIX}/bin/python setup.py install

ENV PREFIX /opt/anaconda/envs/env_vi

ENV PATH /opt/anaconda/envs/env_vi/bin:$PATH

WORKDIR ${HOME}
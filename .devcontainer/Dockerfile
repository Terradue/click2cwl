FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

ENV BASH_ENV=~/.bashrc                                       \
    MAMBA_ROOT_PREFIX=/srv/conda                             \
    PATH=/srv/conda/envs/env_click2cwl/bin:${PATH}                  \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update                                                      && \
    apt-get install -y ca-certificates wget bash bzip2  git  curl  sudo jq  git-flow vim 

ARG USERNAME=linus
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install basic commands and mamba
RUN wget -qO- https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj bin/micromamba --strip-components=1 && \
    ./micromamba shell init -s bash -p ~/micromamba                     && \
    apt-get clean autoremove --yes                                      && \
    rm -rf /var/lib/{apt,dpkg,cache,log}                                && \
    cp ./micromamba /usr/bin                                           

ADD .devcontainer/environment.yml /tmp/environment.yml

RUN micromamba create -f /tmp/environment.yml                           && \                                              
    cd /tmp                                                             && \
    rm -fr /srv/conda/pkgs                                              && \
    rm -fr /tmp/*   

RUN chown -R linus:1000 /srv/conda/

USER $USERNAME

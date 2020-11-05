FROM ubuntu:18.04

ARG USER_ID
ARG GROUP_ID

RUN apt -y update && \
    apt -y install git wget zip make g++ gcc clang build-essential && \
	wget https://dl.bintray.com/boostorg/release/1.63.0/source/boost_1_63_0.zip && \
	unzip boost_1_63_0.zip && \
	mv boost_1_63_0 /usr/local/bin && \
	git clone https://github.com/facebookresearch/Starspace.git && \
	cd Starspace && \
	make

RUN addgroup --gid $GROUP_ID balbes
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID balbes

USER balbes

WORKDIR /Starspace

CMD ./starspace train -trainFile /home/balbes/task_1/financer_formatted.txt -model /home/balbes/task_1/starspace_balbes -trainMode 5


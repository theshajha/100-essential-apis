FROM nginx:1.9-alpine

ARG FILE
ENV FILE=${FILE}
RUN echo ${FILE}

RUN rm /etc/nginx/conf.d/default.conf/
COPY ./${FILE}.conf /etc/nginx/conf.d/default.conf
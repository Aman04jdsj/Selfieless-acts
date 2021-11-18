FROM alpine:3.7
WORKDIR /app
COPY . /app
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install requests
EXPOSE 80
ENV TEAM_ID=CC_42_50_52_712
CMD ["python3", "acts.py"]

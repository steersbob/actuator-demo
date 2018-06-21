FROM brewblox/brewblox-devcon-spark:latest

RUN mkdir -p /pkg
COPY ./pkg/* /pkg/

EXPOSE 5000

RUN pip3 install /pkg/* || true \
    && pip3 install actuator-demo \
    && pip3 show actuator-demo

ENTRYPOINT ["python3", "-m", "actuator_demo"]

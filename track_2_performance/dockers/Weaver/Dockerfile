#
##############################################################################
# MappingWeaver-java
# https://github.com/RMLio/MappingWeaver-java
################################################################################
# Example of custom Java runtime using jlink in a multi-stage container build

FROM maven:latest AS maven-build
RUN apt update
RUN apt upgrade -y
RUN apt update && apt install -y git

# Download BURP repo
RUN git clone https://github.com/RMLio/MappingWeaver-java
RUN git clone https://github.com/RMLio/Algebraic-Mapping-Operators
RUN git clone https://github.com/RMLio/dataio
RUN cd dataio && git checkout development && mvn install -DskipTests
RUN cd Algebraic-Mapping-Operators && git checkout development && mvn install -DskipTests
RUN cd MappingWeaver-java && git checkout development && mvn clean package -DskipTests


FROM eclipse-temurin:25 AS jre-build

# Create a custom Java runtime
RUN $JAVA_HOME/bin/jlink \
         --add-modules java.base,java.xml \
         --strip-debug \
         --no-man-pages \
         --no-header-files \
         --compress=2 \
         --output /javaruntime

# Define your base image
FROM debian:trixie-slim
# Configure the RMLStreamer version to use
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"
COPY --from=jre-build /javaruntime $JAVA_HOME

# Continue with your application deployment
#RUN mkdir /opt/app
#COPY japp.jar /opt/app
#CMD ["java", "-jar", "/opt/app/japp.jar"]


# Install latest updates and dependencies
RUN apt update
RUN apt upgrade -y


RUN mkdir weaver 
COPY --from=maven-build MappingWeaver-java/target/MappingWeaver*SNAPSHOT.jar  weaver/weaver.jar
# Expose data folder

RUN mkdir /data


# Silent
CMD ["tail", "-f", "/dev/null"]


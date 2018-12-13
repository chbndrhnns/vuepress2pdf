FROM jfloff/alpine-python:3.6-onbuild

WORKDIR /app

# cf. https://github.com/GoogleChrome/puppeteer/blob/master/docs/troubleshooting.md
RUN apk update && apk upgrade && \
  echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories && \
  echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories && \
  apk add --no-cache \
  chromium@edge \
  nss@edge \
  ttf-freefont

RUN addgroup -S pptruser && adduser -S -g pptruser pptruser \
  && mkdir -p /home/pptruser/Downloads \
  && chown -R pptruser:pptruser /home/pptruser \
  && chown -R pptruser:pptruser /app

USER pptruser

# virtualenv is created in user space and this path is not in $PATH
ENV PATH="/home/pptruser/.local/bin:${PATH}"
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN pip install --user --no-cache-dir pipenv

COPY --chown=pptruser:pptruser . ./

RUN pipenv install

ENTRYPOINT ["python", "vuepress2pdf.py"]

CMD [ "" ]
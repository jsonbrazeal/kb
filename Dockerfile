FROM python:3-alpine

WORKDIR /src

ENV KB_COLORS true
ENV KB_PATH "~/Drive/Notes/"
ENV KB_EX_PATH "~/Backup/Notes/ex/"

COPY . /src
RUN pip install --no-cache-dir -e /src

EXPOSE 5000

CMD ["python", "-m", "http.server"]


# docker build -t kb .
# docker run --rm -it -p 5000:8000 --name=kb kb
# docker run --rm -it -p 5000:8000 --name=kb -v $(pwd):/src kb

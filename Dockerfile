FROM python:3.10-alpine

RUN apk add --no-cache git build-base libffi-dev graphviz g++
# install a bunch of fonts for graphviz
RUN apk add --no-cache \
    font-noto font-noto-adlam font-noto-arabic font-noto-armenian \
    font-noto-bamum font-noto-bengali font-noto-buhid font-noto-chakma font-noto-cherokee \
    font-noto-devanagari font-noto-emoji font-noto-ethiopic font-noto-extra \
    font-noto-georgian font-noto-gujarati font-noto-gurmukhi font-noto-hebrew \
    font-noto-kannada font-noto-kayahli font-noto-khmer font-noto-lao font-noto-lisu \
    font-noto-myanmar font-noto-nko font-noto-olchiki font-noto-oldturkic font-noto-oriya \
    font-noto-osage font-noto-sinhala font-noto-tamil font-noto-telugu font-noto-malayalam \
    font-noto-thaana font-noto-thai font-noto-tibetan font-noto-tifinagh font-noto-vai

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /TestWorkBot
WORKDIR /TestWorkBot

ENTRYPOINT ["python", "-u", "main.py"]

from flask import Flask, request, make_response
from wordcloud import WordCloud
import jieba
from collections import defaultdict
import io
import base64

app = Flask(__name__)


@app.route("/wordcloud", methods=["get", "post"])
def getWordImage(width=300, height=300):
    if request.method == "POST":  
        print("request:",request,request.args,request.files, request.form)
        file = request.files["file"]
        segs = jieba.cut(file.read())

        stop_words = []
        try:
            with open("./data/stop_words_chinese.txt", 'r', encoding="utf8") as f:
                for line in f:
                    stop_words.append(line.strip())
        except Exception as e:
            print("error", e)
        word_freqs = defaultdict(int)
        for seg in segs:
            if seg not in stop_words:
                word_freqs[seg] += 1

        print("", word_freqs)
        wc = WordCloud(width=width, height=height)
        wc.generate_from_frequencies(word_freqs)
        print("test ", wc.to_image(), type(wc.to_image()))
        wc_image = wc.to_image()

        img_stream = io.BytesIO()
        wc_image.save(img_stream, "png")  
        headers = {
            "Access-Control-Allow-Origin":"*",
            "test":123
        }

        return  make_response( "data:image/png;base64," + base64.b64encode(img_stream.getvalue()).decode('ascii'),200,headers)
    else:
        print(request,request.form)
        return "please upload a text file"


if __name__ == "__main__":
    app.run(debug=True)

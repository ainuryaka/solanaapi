from flask import Flask, request, render_template
import requests
import psycopg2

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        address = request.form.get('address')
        url = 'https://solana-gateway.moralis.io/nft/mainnet/' + address + '/metadata'
        headers = {
            "accept": "application/json",
            "X-API-Key": "f4WKTk8kzroo8iBlEcAIo08EKAjV22tVmrUponb2NzTTTSaYD7BHuI55fQG6GzD9"
        }
        response = requests.get(url, headers=headers)
        print(response.text)



        conn = psycopg2.connect(
            database="nft", user='postgres', password='sunset', host='localhost', port='5433'
        )

        cursor = conn.cursor()

create_script = ''' CREATE TABLE IF NOT EXISTS NFT
(
  address character varying(1000)
    name character varying(200))'''

        cursor.execute(create_script)

        insert_script = "INSERT INTO NFT (name, address) VALUES (%s, %s)"
        insert_value = ("NFT name", response.text)

        cursor.execute(insert_script, insert_value)

        conn.commit()

        conn.close()



if __name__ == '__main__':
    app.run(debug=True, port=5000)




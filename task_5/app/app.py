import stock_prophet.model.btc_model as model_api

from flask import Flask
from flask import request, render_template


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def base():
    print(request)
    if request.method == 'POST':
        form = request.form.to_dict()
        print(form)
        n_steps = int(form['forecast_steps'])
        plot = bool(form['plot'])
        retrain = bool(int(form['retrain']))

        if retrain:
            model_api.train_model()

        forecast = model_api.get_preidction(n_steps)
        return render_template('child.html', plot=plot, df=forecast.to_html())
    else:
        return render_template('base.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)